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


def transform_cell_cycle_ontology_registry(table: pd.DataFrame):
    """Transform all CCO terms."""
    mask = table["registry"] == "cco"
    table.loc[mask, "accession"] = "CCO:" + table.loc[mask, "accession"]


def transform_go_registry(table: pd.DataFrame):
    """Transform all GO terms."""
    mask = table["registry"] == "go"
    table.loc[mask, "accession"] = "GO:" + table.loc[mask, "accession"]


def transform_metanetx_registry(table: pd.DataFrame):
    """Transform all MetaNetX identifiers."""
    # MetaNetX identifiers themselves have no registry. So we add it.
    mnx_mask = table["accession"].isnull()
    table.loc[mnx_mask, "accession"] = table.loc[mnx_mask, "registry"]
    table.loc[mnx_mask, "registry"] = "metanetx.compartment"


def transform_compartment_properties(
    compartments: pd.DataFrame, registry_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX compartment properties."""
    df = compartments.copy()
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
    transform_cell_cycle_ontology_registry(df)
    transform_go_registry(df)
    transform_metanetx_registry(df)
    del df["source"]
    logger.debug(df.head())
    return df


def transform_compartment_cross_references(
    references: pd.DataFrame, registry_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX compartment cross-references."""
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
    transform_cell_cycle_ontology_registry(df)
    transform_go_registry(df)
    transform_metanetx_registry(df)
    del df["xref"]
    logger.debug(df.head())
    return df
