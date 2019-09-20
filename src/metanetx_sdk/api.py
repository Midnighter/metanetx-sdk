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


"""Expose the application programmer interface."""


import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Mapping

import pytz

from . import ftp
from .extract import extract_table
from .model import FTPConfigurationModel, SingleTableConfigurationModel


logger = logging.getLogger(__name__)


OUTPUT_OPTIONS = {"sep": "\t", "index": False, "header": True}
ZURICH_TIME = pytz.timezone("Europe/Zurich")


def pull(
    directory: Path,
    files: List[Path] = None,
    configuration: FTPConfigurationModel = None,
    last_checked: datetime = None,
    server_tz=ZURICH_TIME,
    compress: bool = True,
) -> datetime:
    """
    Pull in changes from one or more files from the MetaNetX FTP server.

    Parameters
    ----------
    directory : pathlib.Path
        The working directory where files are updated.
    files : list of pathlib.Path
    configuration
    last_checked
    server_tz
    compress

    Returns
    -------
    datetime

    """
    if last_checked is None:
        logger.info("Pulling new MetaNetX content.")
        last_checked = datetime.fromordinal(1).replace(tzinfo=server_tz)
    else:
        logger.info("MetaNetX content last checked on %s.", last_checked.isoformat())
    if configuration is None:
        configuration = FTPConfigurationModel.load()
    if files is None:
        files = configuration.files
    pull_on = datetime.now(server_tz)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        ftp.update_tables(
            configuration.host,
            configuration.directory,
            directory,
            [Path(f) for f in files],
            last_checked,
            server_tz,
            compress,
        )
    )
    loop.close()
    return pull_on


def process_table(
    filename: Path,
    output: Path,
    configuration: SingleTableConfigurationModel,
    mapping: Mapping,
    transform: Callable,
) -> None:
    """
    Transform a MetaNetX table and store the processed output.

    Parameters
    ----------
    filename : Path
        The table to extract and transform.
    output : Path
        Where to store the processed output.
    configuration : metanetx_sdk.model.SingleTableConfigurationModel
        The configuration to use for extracting the specific file.
    mapping : Mapping
        A mapping between MetaNetX resources and Identifiers.org registries.
    transform : Callable
        The table-specific transformation function to apply.

    """
    logger.info("Extracting...")
    data = extract_table(filename, configuration.columns, configuration.skip)
    logger.info("Transforming...")
    processed = transform(data, mapping)
    logger.info("Storing...")
    processed.to_csv(output, **OUTPUT_OPTIONS)
