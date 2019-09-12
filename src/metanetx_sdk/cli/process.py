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


import logging

import click

from .. import extract, transform
from ..model import TableConfigurationModel


logger = logging.getLogger(__name__)


OUTPUT_ATTR = {"sep": "\t", "index": False, "header": True}


@click.group()
@click.help_option("--help", "-h")
def process():
    pass


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<CHEM PROP FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<PROCESSED FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def chem_prop(filename, output):
    config = TableConfigurationModel.load()
    logger.info("Parsing chemical properties.")
    chem_prop = extract.extract_table(
        filename, config.chem_prop.columns, config.chem_prop.skip
    )
    mapping = extract.extract_chemical_registry_mapping()
    processed = transform.transform_chemical_properties(chem_prop, mapping)
    processed.to_csv(output, **OUTPUT_ATTR)


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<CHEM XREF FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<PROCESSED FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def chem_xref(filename, output):
    config = TableConfigurationModel.load()
    logger.info("Parsing chemical cross-references.")
    chem_xref = extract.extract_table(
        filename, config.chem_xref.columns, config.chem_xref.skip
    )
    mapping = extract.extract_chemical_registry_mapping()
    processed = transform.transform_chemical_cross_references(chem_xref, mapping)
    processed.to_csv(output, **OUTPUT_ATTR)


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<COMP PROP FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<PROCESSED FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def comp_prop(filename, output):
    config = TableConfigurationModel.load()
    logger.info("Parsing compartment properties.")
    comp_prop = extract.extract_table(
        filename, config.comp_prop.columns, config.comp_prop.skip
    )
    mapping = extract.extract_compartment_registry_mapping()
    processed = transform.transform_compartment_properties(comp_prop, mapping)
    processed.to_csv(output, **OUTPUT_ATTR)


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<COMP XREF FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<PROCESSED FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def comp_xref(filename, output):
    config = TableConfigurationModel.load()
    logger.info("Parsing compartment cross-references.")
    comp_xref = extract.extract_table(
        filename, config.comp_xref.columns, config.comp_xref.skip
    )
    mapping = extract.extract_compartment_registry_mapping()
    processed = transform.transform_compartment_cross_references(comp_xref, mapping)
    processed.to_csv(output, **OUTPUT_ATTR)


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<REAC PROP FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<PROCESSED FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def reac_prop(filename, output):
    config = TableConfigurationModel.load()
    logger.info("Parsing reaction properties.")
    reac_prop = extract.extract_table(
        filename, config.reac_prop.columns, config.reac_prop.skip
    )
    mapping = extract.extract_reaction_registry_mapping()
    processed = transform.transform_reaction_properties(reac_prop, mapping)
    processed.to_csv(output, **OUTPUT_ATTR)


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<REAC XREF FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<PROCESSED FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def reac_xref(filename, output):
    config = TableConfigurationModel.load()
    logger.info("Parsing reaction cross-references.")
    reac_xref = extract.extract_table(
        filename, config.reac_xref.columns, config.reac_xref.skip
    )
    mapping = extract.extract_reaction_registry_mapping()
    processed = transform.transform_reaction_cross_references(reac_xref, mapping)
    processed.to_csv(output, **OUTPUT_ATTR)
