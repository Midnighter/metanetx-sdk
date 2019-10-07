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


"""Provide compartment data transformation functions."""


import logging
from typing import Mapping

import pandas as pd


logger = logging.getLogger(__name__)


def transform_cell_cycle_ontology_prefix(table: pd.DataFrame):
    """Transform all CCO terms."""
    mask = table["prefix"] == "cco"
    table.loc[mask, "identifier"] = "CCO:" + table.loc[mask, "identifier"]


def transform_go_prefix(table: pd.DataFrame):
    """Transform all GO terms."""
    mask = table["prefix"] == "go"
    table.loc[mask, "identifier"] = "GO:" + table.loc[mask, "identifier"]


def transform_metanetx_prefix(table: pd.DataFrame):
    """Transform all MetaNetX identifiers."""
    # MetaNetX identifiers themselves have no prefix. So we add it.
    mnx_mask = table["identifier"].isnull()
    table.loc[mnx_mask, "identifier"] = table.loc[mnx_mask, "prefix"]
    table.loc[mnx_mask, "prefix"] = "metanetx.compartment"


def transform_compartment_properties(
    compartments: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX compartment properties."""
    df = compartments.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["prefix", "identifier"]] = df["source"].str.split(":", n=1, expand=True)
    # Map all source databases to MIRIAM compliant versions.
    for prefix in df.loc[df["identifier"].notnull(), "prefix"].unique():
        if prefix in prefix_mapping:
            df.loc[df["prefix"] == prefix, "prefix"] = prefix_mapping[prefix]
        else:
            logger.warning(
                "The resource prefix '%s' does not appear in the mapping.", prefix
            )
    transform_cell_cycle_ontology_prefix(df)
    transform_go_prefix(df)
    transform_metanetx_prefix(df)
    del df["source"]
    logger.debug(df.head())
    return df


def transform_compartment_cross_references(
    references: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX compartment cross-references."""
    df = references.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["prefix", "identifier"]] = df["xref"].str.split(":", n=1, expand=True)
    # Map all xref databases to MIRIAM compliant versions.
    for prefix in df.loc[df["identifier"].notnull(), "prefix"].unique():
        if prefix in prefix_mapping:
            df.loc[df["prefix"] == prefix, "prefix"] = prefix_mapping[prefix]
        else:
            logger.warning(
                "The resource prefix '%s' does not appear in the mapping.", prefix
            )
    transform_cell_cycle_ontology_prefix(df)
    transform_go_prefix(df)
    transform_metanetx_prefix(df)
    del df["xref"]
    logger.debug(df.head())
    return df
