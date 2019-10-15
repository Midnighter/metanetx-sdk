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


"""Provide chemical data transformation functions."""


import logging
from typing import Mapping

import pandas as pd


logger = logging.getLogger(__name__)


def transform_chebi_prefix(table: pd.DataFrame):
    """Transform all ChEBI identifiers."""
    mask = table["prefix"] == "chebi"
    table.loc[mask, "identifier"] = "CHEBI:" + table.loc[mask, "identifier"]


def transform_swisslipid_prefix(table: pd.DataFrame):
    """Transform all swisslipid identifiers."""
    mask = table["prefix"] == "slm"
    table.loc[mask, "prefix"] = "swisslipid"
    table.loc[mask, "identifier"] = "SLM:" + table.loc[mask, "identifier"]


def transform_kegg_prefix(table: pd.DataFrame):
    """Transform all KEGG identifiers."""
    prefix_mapping = {
        "C": "kegg.compound",
        "D": "kegg.drug",
        "E": "kegg.environ",
        "G": "kegg.glycan",
    }
    mask = table["prefix"] == "kegg"
    id_prefix = table.loc[mask, "identifier"].str[:1].unique()
    for prefix in [str(i) for i in id_prefix]:
        table.loc[
            mask & table["identifier"].str.startswith(prefix), "prefix"
        ] = prefix_mapping[prefix]


def transform_metanetx_prefix(table: pd.DataFrame):
    """Transform all MetaNetX identifiers."""
    # MetaNetX identifiers themselves have no prefix. So we add it.
    mnx_mask = table["identifier"].isnull()
    table.loc[mnx_mask, "identifier"] = table.loc[mnx_mask, "prefix"]
    table.loc[mnx_mask, "prefix"] = "metanetx.chemical"


def transform_chemical_properties(
    chemicals: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX chemical cross-references."""
    df = chemicals.copy()
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
    transform_chebi_prefix(df)
    transform_swisslipid_prefix(df)
    transform_kegg_prefix(df)
    transform_metanetx_prefix(df)
    del df["source"]
    logger.debug(df.head())
    return df


def transform_chemical_cross_references(
    references: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX chemical cross-references."""
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
    transform_chebi_prefix(df)
    transform_swisslipid_prefix(df)
    transform_kegg_prefix(df)
    transform_metanetx_prefix(df)
    del df["xref"]
    logger.debug(df.head())
    return df
