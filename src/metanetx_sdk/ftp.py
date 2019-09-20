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


"""Provide functions to interact with the MetaNetX FTP server."""


import asyncio
import gzip
import logging
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import List

import aioftp
from pytz import timezone

from .model import PathInfoModel


logger = logging.getLogger(__name__)


async def update_file(
    host: str,
    ftp_directory: Path,
    path: Path,
    filename: Path,
    last_checked: datetime,
    local_tz: timezone,
    compress: bool = True,
) -> None:
    """
    Retrieve a file from an FTP server if it is newer than a local version.

    Parameters
    ----------
    host : str
        The FTP host, for example, ftp.vital-it.ch.
    ftp_directory : pathlib.Path
    path : pathlib.Path
        Working directory where files are searched and stored.
    filename : pathlib.Path
        The file to retrieve relative to the working directory on the server.
    last_checked : datetime
        The date and time when this script was last run.
    local_tz : pytz.timezone
    compress : bool, optional
        Whether or not to gzip the files.

    """
    async with aioftp.ClientSession(host) as client:
        await client.change_directory(ftp_directory)
        info = PathInfoModel(**await client.stat(filename))
        info.localize(local_tz)
        logger.info(
            f"Remote file '%s' last modified on %s.", filename, info.modify.isoformat()
        )
        if compress:
            suffixes = filename.suffixes
            if suffixes[-1] != ".gz":
                suffixes.append(".gz")
            local_filename = filename.with_suffix("").with_suffix("".join(suffixes))
        else:
            local_filename = filename
        local_filename = path / local_filename

        if local_filename.is_file() and info.modify <= last_checked:
            logger.info("Local file version is up to date.")
            return

        logger.info("Retrieving updated file version.")
        try:
            if compress:
                handle = gzip.open(local_filename, mode="wb")
            else:
                handle = local_filename.open("wb")
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


async def update_tables(
    host: str,
    ftp_directory: PurePosixPath,
    output: Path,
    files: List[Path],
    last_checked: datetime,
    local_tz: timezone,
    compress: bool,
) -> None:
    """
    Load all given files if newer versions exist.

    Parameters
    ----------
    host : str
        The FTP host, for example, ftp.vital-it.ch.
    ftp_directory : pathlib.PurePosixPath
        The working directory on the host.
    output : pathlib.Path
        The output directory for the files. If a filename of any of the ``files``
        exists in that directory, it is only overwritten if the one on the host is
        more recent.
    files : list of pathlib.Path
        Pure filenames of files of interest to be loaded from the server.
    last_checked : datetime.datetime
        When the local files were last checked.
    local_tz : pytz.timezone
        A timezone that the FTP server is in, for example, Europe/Zurich.
    compress : bool
        Whether or not to gzip compress downloaded files.

    """
    tasks = [
        update_file(
            host,
            ftp_directory,
            output,
            filename,
            last_checked,
            local_tz,
            compress=compress,
        )
        for filename in files
    ]
    await asyncio.gather(*tasks)
