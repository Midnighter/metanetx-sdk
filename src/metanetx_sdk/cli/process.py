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


"""Provide MetaNetX table processing commands."""


import logging
from pathlib import Path

import click

from .. import api, extract, transform
from ..model import TableConfigurationModel


logger = logging.getLogger(__name__)


@click.group()
@click.help_option("--help", "-h")
def process():
    """Subcommand for processing MetaNetX tables."""
    pass


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<INPUT FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<OUTPUT FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def chem_prop(filename, output):
    """
    Extract and transform a chemical properties table.

    INPUT FILE is the path to the raw MetaNetX source table.

    OUTPUT FILE is the path for the transformed table output.

    """
    logger.info("Processing chemical properties.")
    config = TableConfigurationModel.load()
    mapping = extract.extract_chemical_registry_mapping()
    api.process_table(
        Path(filename),
        Path(output),
        config.chem_prop,
        mapping,
        transform.transform_chemical_properties,
    )
    logger.info("Complete.")


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<INPUT FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<OUTPUT FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def chem_xref(filename, output):
    """
    Extract and transform a chemical cross-references table.

    INPUT FILE is the path to the raw MetaNetX source table.

    OUTPUT FILE is the path for the transformed table output.

    """
    logger.info("Processing chemical cross-references.")
    config = TableConfigurationModel.load()
    mapping = extract.extract_chemical_registry_mapping()
    api.process_table(
        Path(filename),
        Path(output),
        config.chem_xref,
        mapping,
        transform.transform_chemical_cross_references,
    )
    logger.info("Complete.")


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<INPUT FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<OUTPUT FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def comp_prop(filename, output):
    """
    Extract and transform a compartment properties table.

    INPUT FILE is the path to the raw MetaNetX source table.

    OUTPUT FILE is the path for the transformed table output.

    """
    logger.info("Processing compartment properties.")
    config = TableConfigurationModel.load()
    mapping = extract.extract_compartment_registry_mapping()
    api.process_table(
        Path(filename),
        Path(output),
        config.comp_prop,
        mapping,
        transform.transform_compartment_properties,
    )
    logger.info("Complete.")


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<INPUT FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<OUTPUT FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def comp_xref(filename, output):
    """
    Extract and transform a compartment cross-references table.

    INPUT FILE is the path to the raw MetaNetX source table.

    OUTPUT FILE is the path for the transformed table output.

    """
    logger.info("Processing compartment cross-references.")
    config = TableConfigurationModel.load()
    mapping = extract.extract_compartment_registry_mapping()
    api.process_table(
        Path(filename),
        Path(output),
        config.comp_xref,
        mapping,
        transform.transform_compartment_cross_references,
    )
    logger.info("Complete.")


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<INPUT FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<OUTPUT FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def reac_prop(filename, output):
    """
    Extract and transform a reaction properties table.

    INPUT FILE is the path to the raw MetaNetX source table.

    OUTPUT FILE is the path for the transformed table output.

    """
    logger.info("Processing reaction properties.")
    config = TableConfigurationModel.load()
    mapping = extract.extract_reaction_registry_mapping()
    api.process_table(
        Path(filename),
        Path(output),
        config.reac_prop,
        mapping,
        transform.transform_reaction_properties,
    )
    logger.info("Complete.")


@process.command()
@click.help_option("--help", "-h")
@click.argument(
    "filename",
    metavar="<INPUT FILE>",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output",
    metavar="<OUTPUT FILE>",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
def reac_xref(filename, output):
    """
    Extract and transform a reaction cross-references table.

    INPUT FILE is the path to the raw MetaNetX source table.

    OUTPUT FILE is the path for the transformed table output.

    """
    logger.info("Processing reaction cross-references.")
    config = TableConfigurationModel.load()
    mapping = extract.extract_reaction_registry_mapping()
    api.process_table(
        Path(filename),
        Path(output),
        config.reac_xref,
        mapping,
        transform.transform_reaction_cross_references,
    )
    logger.info("Complete.")
