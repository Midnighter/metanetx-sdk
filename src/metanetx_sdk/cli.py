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


import asyncio
import logging
from datetime import datetime
from importlib.resources import open_text
from os.path import isfile, join

import click
import click_log
import pandas as pd
import pytz
from dateutil import parser

from . import data, extract, ftp, transform
from .model import FTPConfigurationModel, TableConfigurationModel


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"simple": {"format": "[%(levelname)s] [%(name)s] %(message)s"}},
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            }
        },
        "root": {"level": "WARNING", "handlers": ["console"]},
    }
)
logger = logging.getLogger("metanetx_sdk")
click_log.basic_config(logger)


@click.group()
@click.help_option("--help", "-h")
@click_log.simple_verbosity_option(
    logger,
    default="INFO",
    show_default=True,
    type=click.Choice(["CRITICAL", "ERROR", "WARN", "INFO", "DEBUG"]),
)
def cli():
    """Command line interface to update MetaNetX data.."""
    pass


@cli.command()
@click.argument(
    "working_dir",
    metavar="<METANETX PATH>",
    type=click.Path(exists=True, file_okay=False, writable=True),
)
def update(working_dir):
    # The MetaNetX FTP server is in Switzerland but does not support timezones.
    zurich_tz = pytz.timezone("Europe/Zurich")
    last = join(working_dir, "last.txt")
    if isfile(last):
        with open(last) as file_handle:
            last_checked = parser.parse(file_handle.read().strip())
    else:
        last_checked = datetime.fromordinal(1)
    logger.info("Updating MetaNetX content.")
    config = FTPConfigurationModel.load()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        ftp.update_tables(config, working_dir, last_checked, zurich_tz)
    )
    loop.close()
    with open(last, "w") as file_handle:
        file_handle.write(datetime.now(zurich_tz).isoformat())

