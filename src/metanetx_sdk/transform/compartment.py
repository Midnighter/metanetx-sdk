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

from .helpers import drop_namespace


logger = logging.getLogger(__name__)


def transform_cell_cycle_ontology_prefix(table: pd.DataFrame):
    """Transform all CCO terms."""
    mask = table["prefix"] == "cco"
    table.loc[mask, "identifier"] = "CCO:" + table.loc[mask, "identifier"]


def transform_gene_ontology_prefix(table: pd.DataFrame):
    """Transform all GO terms."""
    mask = table["prefix"].str.lower() == "go"
    table.loc[mask, "prefix"] = "go"
    table.loc[mask, "identifier"] = "GO:" + table.loc[mask, "identifier"]


def transform_cell_type_ontology_prefix(table: pd.DataFrame):
    """Transform all CL terms."""
    mask = table["prefix"].str.lower() == "cl"
    table.loc[mask, "prefix"] = "cl"
    table.loc[mask, "identifier"] = "CL:" + table.loc[mask, "identifier"]


def transform_compartment_properties(
    compartments: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform the MetaNetX compartment properties."""
    df = compartments.copy()
    # Cross references have a prefix.
    # We split the prefixes so that we know the actual data sources.
    df[["prefix", "identifier"]] = df["source"].str.split(":", n=1, expand=True)
    if (num_missing := df["identifier"].isnull().sum()) > 0:
        logger.error("There are %d entries without a namespace prefix.", num_missing)
    namespaces = set(df.loc[df["identifier"].notnull(), "prefix"].unique())
    # Remove those namespaces that we handle specially.
    if "cco" in namespaces:
        logger.debug("Transforming Cell Cycle Ontology terms.")
        transform_cell_cycle_ontology_prefix(df)
        drop_namespace(namespaces, "cco")
    if "go" in namespaces or "GO" in namespaces:
        logger.debug("Transforming Gene Ontology terms.")
        transform_gene_ontology_prefix(df)
        drop_namespace(namespaces, "go")
        drop_namespace(namespaces, "GO")
    if "cl" in namespaces or "CL" in namespaces:
        logger.debug("Transforming Cell Type Ontology terms.")
        transform_cell_type_ontology_prefix(df)
        drop_namespace(namespaces, "cl")
        drop_namespace(namespaces, "CL")
    # Map all source databases to MIRIAM compliant versions.
    miriam_prefixes = set(prefix_mapping)
    for prefix in namespaces:
        if prefix in miriam_prefixes:
            logger.info("Nothing to be done for '%s'.", prefix)
        elif prefix in prefix_mapping:
            df.loc[df["prefix"] == prefix, "prefix"] = prefix_mapping[prefix]
        else:
            logger.error("The resource prefix '%s' is unhandled.", prefix)
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
    if (num_missing := df["identifier"].isnull().sum()) > 0:
        logger.error("There are %d entries without a namespace prefix.", num_missing)
    namespaces = set(df.loc[df["identifier"].notnull(), "prefix"].unique())
    # Remove those namespaces that we handle specially.
    if "cco" in namespaces:
        logger.debug("Transforming Cell Cycle Ontology terms.")
        transform_cell_cycle_ontology_prefix(df)
        namespaces.remove("cco")
    if "go" in namespaces:
        logger.debug("Transforming Gene Ontology terms.")
        transform_gene_ontology_prefix(df)
        drop_namespace(namespaces, "go")
        drop_namespace(namespaces, "GO")
    if "cl" in namespaces:
        logger.debug("Transforming Cell Type Ontology terms.")
        transform_cell_type_ontology_prefix(df)
        drop_namespace(namespaces, "cl")
        drop_namespace(namespaces, "CL")
    # Map all xref databases to MIRIAM compliant versions.
    miriam_prefixes = set(prefix_mapping)
    for prefix in namespaces:
        if prefix in miriam_prefixes:
            logger.info("Nothing to be done for '%s'.", prefix)
        elif prefix in prefix_mapping:
            df.loc[df["prefix"] == prefix, "prefix"] = prefix_mapping[prefix]
        else:
            logger.error("The resource prefix '%s' is unhandled.", prefix)
    del df["xref"]
    logger.debug(df.head())
    return df
