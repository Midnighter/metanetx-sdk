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


"""Provide a command line interface for working with MetaNetX data."""


import logging
from pathlib import Path

import click
import click_log
from dateutil import parser

from .. import api
from .process import process


logger = logging.getLogger("metanetx_sdk")
click_log.basic_config(logger)


OUTPUT_ATTR = {"sep": "\t", "index": False, "header": True}


@click.group()
@click.help_option("--help", "-h")
@click_log.simple_verbosity_option(
    logger,
    default="INFO",
    show_default=True,
    type=click.Choice(["CRITICAL", "ERROR", "WARN", "INFO", "DEBUG"]),
)
def cli():
    """Command line interface for working with MetaNetX data."""
    pass


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--compress/--no-compress",
    default=True,
    show_default=True,
    help="Gzip the pulled in files.",
)
@click.argument(
    "working_dir",
    metavar="<METANETX DIRECTORY>",
    type=click.Path(exists=True, file_okay=False, writable=True),
)
@click.argument("files", metavar="[FILENAME] ...", type=click.Path(), nargs=-1)
def pull(compress, working_dir, files):
    """
    Load missing or outdated files from the MetaNetX FTP server.

    METANETX DIRECTORY is where existing files can be found and new ones should be
    stored.

    Name any number of FILENAMEs to pull from the FTP server. Can be omitted in
    order to pull all default files.

    """
    async_logger = logging.getLogger("asyncio")
    async_logger.setLevel(logger.level)
    # The MetaNetX FTP server is in Switzerland but does not support timezones.
    last = Path(working_dir) / "last.txt"
    if last.is_file():
        with last.open() as file_handle:
            last_checked = parser.parse(file_handle.read().strip())
    else:
        last_checked = None
    checked_on = api.pull(
        working_dir, files, last_checked=last_checked, compress=compress
    )
    with last.open("w") as file_handle:
        file_handle.write(checked_on.isoformat())


cli.add_command(process)
