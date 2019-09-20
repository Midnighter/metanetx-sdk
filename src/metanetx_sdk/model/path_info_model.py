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


from datetime import datetime

from dateutil import parser
from pydantic import BaseModel, validator
from pytz import timezone


class PathInfoModel(BaseModel):
    """Describe information found about FTP files."""

    type: str
    size: int
    modify: datetime

    @validator("modify", pre=True, always=True)
    def transform_modify(cls, value: str) -> datetime:
        """Transform the modify string to a datetime object."""
        # Modified time parsing according to https://stackoverflow.com/a/29027386.
        return parser.parse(value)

    def localize(self, local_tz: timezone) -> None:
        """Convert the modify timestamp into a timezone aware one."""
        self.modify = local_tz.localize(self.modify)
