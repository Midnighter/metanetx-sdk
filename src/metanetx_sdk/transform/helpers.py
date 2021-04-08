# Copyright (c) 2021, Moritz E. Beber.
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


"""Provide helper functions to the transformation modules."""


from typing import Mapping, Set

import pandas as pd


def drop_namespace(namespaces: Set[str], name: str) -> None:
    """Drop a namespace name from a common set in a fail-safe manner."""
    try:
        namespaces.remove(name)
    except KeyError:
        pass


def transform_deprecated_identifiers(
    references: pd.DataFrame, prefix_mapping: Mapping
) -> pd.DataFrame:
    """Transform deprecated MetaNetX identifiers."""
    df = references.copy()
    return df
