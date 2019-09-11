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
import gzip
import logging
from datetime import datetime
from os.path import isfile, join
from pathlib import Path

import aioftp
from pytz import timezone

from .model import FTPConfigurationModel, PathInfoModel


logger = logging.getLogger(__name__)


async def update_file(
    config: FTPConfigurationModel,
    path: Path,
    filename: str,
    last_checked: datetime,
    local_tz: timezone,
    compress: bool = True,
) -> None:
    """
    Retrieve a file from an FTP server if it is newer than a local version.

    Parameters
    ----------
    config : dict
        Connection paramters.
    path : str
        Working directory where files are searched and stored.
    filename : str
        The file to retrieve relative to the working directory on the server.
    last_checked : datetime
        The date and time when this script was last run.
    local_tz : pytz.timezone
    compress : bool, optional
        Whether or not to gzip the files.

    """
    async with aioftp.ClientSession(config.host) as client:
        await client.change_directory(config.directory)
        info = PathInfoModel(**await client.stat(filename))
        info.localize(local_tz)
        logger.info(
            f"Remote file '%s' last modified on %s.", filename, info.modify.isoformat()
        )
        if compress:
            local_filename = join(path, f"{filename}.gz")
        else:
            local_filename = join(path, filename)
        if (not isfile(local_filename)) or (info.modify > last_checked):
            logger.info("Retrieving updated file version.")
            try:
                if compress:
                    handle = gzip.open(local_filename, mode="wb")
                else:
                    handle = open(local_filename)
                transferred = 0
                async with client.download_stream(filename) as stream:
                    async for block in stream.iter_by_block():
                        handle.write(block)
                        transferred += len(block)
                assert transferred == info.size, "Not all bytes were transferred."
            except IOError as error:
                logger.error("Failed to download '%s'.", filename)
                logger.debug("", exc_info=error)
            finally:
                handle.close()
        else:
            logger.info("Local file version is up to date.")


async def update_tables(
    config: FTPConfigurationModel,
    path: Path,
    last_checked: datetime,
    local_tz: timezone,
):
    tasks = [
        update_file(
            config,
            path,
            filename,
            last_checked,
            local_tz,
            compress=filename.endswith(".tsv"),
        )
        for filename in config.files
    ]
    await asyncio.gather(*tasks)
