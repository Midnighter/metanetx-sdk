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


class CustomPath(PurePosixPath):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        return PurePosixPath(value)


class FTPConfigurationModel(BaseModel):

    host: str
    base_directory: CustomPath
    files: List[str]
    version: str

    @property
    def directory(self):
        return self.base_directory.joinpath(self.version)

    @classmethod
    def load(cls, version: Optional[str] = None):
        with open_text(data, "metanetx.toml") as handle:
            obj = toml.load(handle)
        if version is None:
            version = obj["latest"]
        return cls(version=version, **obj["ftp"])
