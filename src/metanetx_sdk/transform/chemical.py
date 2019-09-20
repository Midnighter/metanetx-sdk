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


def transform_chebi_registry(table: pd.DataFrame):
    """Transform all ChEBI identifiers."""
    mask = table["registry"] == "chebi"
    table.loc[mask, "accession"] = "CHEBI:" + table.loc[mask, "accession"]


def transform_kegg_registry(table: pd.DataFrame):
    """Transform all KEGG identifiers."""
    registry_mapping = {
        "C": "kegg.compound",
        "D": "kegg.drug",
        "E": "kegg.environ",
        "G": "kegg.glycan",
    }
    kegg_id_prefix = (
        table.loc[table["registry"] == "kegg", "accession"].str[:1].unique()
    )
    kegg_mask = table["registry"] == "kegg"
    for prefix in [str(i) for i in kegg_id_prefix]:
        table.loc[
            kegg_mask & table["accession"].str.startswith(prefix), "registry"
        ] = registry_mapping[prefix]


def transform_metanetx_registry(table: pd.DataFrame):
    """Transform all MetaNetX identifiers."""
    # MetaNetX identifiers themselves have no registry. So we add it.
    mnx_mask = table["accession"].isnull()
    table.loc[mnx_mask, "accession"] = table.loc[mnx_mask, "registry"]
    table.loc[mnx_mask, "registry"] = "metanetx.chemical"


def transform_chemical_properties(
    chemicals: pd.DataFrame, registry_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX chemical cross-references."""
    df = chemicals.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["registry", "accession"]] = df["source"].str.split(":", n=1, expand=True)
    # Map all source databases to MIRIAM compliant versions.
    for registry in df.loc[df["accession"].notnull(), "registry"].unique():
        if registry in registry_mapping:
            df.loc[df["registry"] == registry, "registry"] = registry_mapping[registry]
        else:
            logger.warning(
                "The resource prefix '%s' does not appear in the mapping.", registry
            )
    transform_chebi_registry(df)
    transform_kegg_registry(df)
    transform_metanetx_registry(df)
    del df["source"]
    logger.debug(df.head())
    return df


def transform_chemical_cross_references(
    references: pd.DataFrame, registry_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX chemical cross-references."""
    df = references.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["registry", "accession"]] = df["xref"].str.split(":", n=1, expand=True)
    # Map all xref databases to MIRIAM compliant versions.
    for registry in df.loc[df["accession"].notnull(), "registry"].unique():
        if registry in registry_mapping:
            df.loc[df["registry"] == registry, "registry"] = registry_mapping[registry]
        else:
            logger.warning(
                "The resource prefix '%s' does not appear in the mapping.", registry
            )
    transform_chebi_registry(df)
    transform_kegg_registry(df)
    transform_metanetx_registry(df)
    del df["xref"]
    logger.debug(df.head())
    return df
