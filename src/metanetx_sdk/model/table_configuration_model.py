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
from typing import List, Optional

import toml
from pydantic import BaseModel

from .. import data


class SingleTableConfigurationModel(BaseModel):
    """Describe the configuration needed for a single table."""

    columns: List[str]
    skip: int


class TableConfigurationModel(BaseModel):
    """Describe all table configuration models."""

    chem_prop: SingleTableConfigurationModel
    chem_xref: SingleTableConfigurationModel
    comp_prop: SingleTableConfigurationModel
    comp_xref: SingleTableConfigurationModel
    reac_prop: SingleTableConfigurationModel
    reac_xref: SingleTableConfigurationModel
    version: str

    @classmethod
    def load(cls, version: Optional[str] = None):
        """Load the configuration from the packaged file."""
        with open_text(data, "metanetx.toml") as handle:
            obj = toml.load(handle)
        if version is None:
            version = obj["latest"]
        return cls(version=version, **obj[version])
