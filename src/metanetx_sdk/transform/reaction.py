# Copyright (c) 2019, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide reaction data transformation functions."""


import logging
from typing import Mapping

import pandas as pd


logger = logging.getLogger(__name__)


def transform_metanetx_prefix(table: pd.DataFrame):
    """Transform all MetaNetX identifiers."""
    logger.debug("Transforming MetaNetX identifiers.")
    # MetaNetX identifiers themselves have no prefix. So we add it.
    mnx_mask = table["identifier"].isnull()
    table.loc[mnx_mask, "identifier"] = table.loc[mnx_mask, "prefix"]
    table.loc[mnx_mask, "prefix"] = "metanetx.reaction"


def transform_reaction_properties(
    reactions: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX reaction properties."""
    df = reactions.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["prefix", "identifier"]] = df["source"].str.split(":", n=1, expand=True)
    if (num_missing := df["identifier"].isnull().sum()) > 0:
        logger.error("There are %d entries without a namespace prefix.", num_missing)
    # Map all source databases to MIRIAM compliant versions.
    miriam_prefixes = set(prefix_mapping)
    for prefix in df.loc[df["identifier"].notnull(), "prefix"].unique():
        if prefix in miriam_prefixes:
            logger.info("Nothing to be done for '%s'.", prefix)
        elif prefix in prefix_mapping:
            df.loc[df["prefix"] == prefix, "prefix"] = prefix_mapping[prefix]
        else:
            logger.error("The resource prefix '%s' is unhandled.", prefix)
    del df["source"]
    logger.debug(df.head())
    return df


def transform_reaction_cross_references(
    references: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX reaction cross-references."""
    df = references.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["prefix", "identifier"]] = df["xref"].str.split(":", n=1, expand=True)
    if (num_missing := df["identifier"].isnull().sum()) > 0:
        logger.warning(
            "There are %d entries without a namespace prefix. Assumed to belong to "
            "'metanetx.reaction'.",
            num_missing,
        )
    # Map all xref databases to MIRIAM compliant versions.
    miriam_prefixes = set(prefix_mapping)
    for prefix in df.loc[df["identifier"].notnull(), "prefix"].unique():
        if prefix in miriam_prefixes:
            logger.info("Nothing to be done for '%s'.", prefix)
        elif prefix in prefix_mapping:
            df.loc[df["prefix"] == prefix, "prefix"] = prefix_mapping[prefix]
        else:
            logger.error("The resource prefix '%s' is unhandled.", prefix)
    transform_metanetx_prefix(df)
    del df["xref"]
    logger.debug(df.head())
    return df
