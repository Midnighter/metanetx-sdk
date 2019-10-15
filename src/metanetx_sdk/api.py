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
from typing import Callable, List, Mapping, Optional

from . import ftp
from .extract import extract_table
from .model import FTPConfigurationModel, SingleTableConfigurationModel


logger = logging.getLogger(__name__)


OUTPUT_OPTIONS = {"sep": "\t", "index": False, "header": True}


def pull(
    directory: Path,
    files: Optional[List[Path]] = None,
    configuration: Optional[FTPConfigurationModel] = None,
    last_checked: Optional[datetime] = None,
    compress: bool = True,
) -> datetime:
    """
    Pull in changes to one or more files from the MetaNetX FTP server.

    Parameters
    ----------
    directory : pathlib.Path
        The working directory where files are updated.
    files : list of pathlib.Path, optional
        A list of one or more filenames as they are found on the FTP server
        (basename only). By default all known files are checked.
    configuration : metanetx_sdk.model.FTPConfigurationModel, optional
        Configuration values encoded in an object. A default configuration is provided.
    last_checked : datetime, optional
        The time when the files were last checked for updates. By default it is
        assumed that the files have never been checked before.
    compress : bool, optional
        Whether or not to compress the downloaded files with gzip (default True).

    Returns
    -------
    datetime
        The current time (timezone of the FTP server) when files were checked for
        updates.

    """
    if configuration is None:
        configuration = FTPConfigurationModel.load()
    if last_checked is None:
        logger.info("Pulling new MetaNetX content.")
        last_checked = datetime.fromordinal(1).replace(tzinfo=configuration.timezone)
    else:
        logger.info("MetaNetX content last checked on %s.", last_checked.isoformat())
    if not files:
        files = configuration.files
    pull_on = datetime.now(configuration.timezone)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        ftp.update_tables(
            configuration.host,
            configuration.directory,
            directory,
            [Path(f) for f in files],
            last_checked,
            configuration.timezone,
            compress,
        )
    )
    loop.close()
    return pull_on


def etl_table(
    filename: Path,
    output: Path,
    configuration: SingleTableConfigurationModel,
    mapping: Mapping,
    transform: Callable,
) -> None:
    """
    Extract, transform, and load a MetaNetX table.

    Parameters
    ----------
    filename : pathlib.Path
        The table to extract and transform.
    output : pathlib.Path
        Where to store the processed output.
    configuration : metanetx_sdk.model.SingleTableConfigurationModel
        The configuration to use for extracting the specific file.
    mapping : typing.Mapping
        A mapping between MetaNetX resources and Identifiers.org registries.
    transform : typing.Callable
        The table-specific transformation function to apply.

    """
    logger.info("Extracting...")
    data = extract_table(filename, configuration.columns, configuration.skip)
    logger.info("Transforming...")
    processed = transform(data, mapping)
    logger.info("Loading...")
    processed.to_csv(output, **OUTPUT_OPTIONS)
