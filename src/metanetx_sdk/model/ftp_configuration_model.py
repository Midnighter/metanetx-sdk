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


"""Provide an FTP configuration data model."""


from importlib.resources import open_text
from pathlib import PurePosixPath
from typing import List, Optional

import toml
from pydantic import BaseModel

from .. import data


class FTPPath(PurePosixPath):
    """Define an FTP path data type."""

    @classmethod
    def __get_validators__(cls):
        """
        Follow the pydantic guide for custom types.

        See https://pydantic-docs.helpmanual.io/#custom-data-types

        """
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> PurePosixPath:
        """Transform the given path string into an object."""
        return PurePosixPath(value)


class FTPConfigurationModel(BaseModel):
    """Define the FTP configuration data model."""

    host: str
    base_directory: FTPPath
    files: List[str]
    version: str

    @property
    def directory(self) -> PurePosixPath:
        """Return the compound working directory for the FTP server."""
        return self.base_directory / self.version

    @classmethod
    def load(cls, version: Optional[str] = None) -> "FTPConfigurationModel":
        """Load the packaged FTP configuration."""
        with open_text(data, "metanetx.toml") as handle:
            obj = toml.load(handle)
        if version is None:
            version = obj["latest"]
        return cls(version=version, **obj["ftp"])
