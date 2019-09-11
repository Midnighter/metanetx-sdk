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


"""Extract the MetaNetX data tables."""


from pathlib import Path
from typing import List

import pandas as pd


def extract_table(filename: Path, columns: List[str]) -> pd.DataFrame:
    """
    Extract tabular MetaNetX data.

    The tables dumped by MetaNetX have their column names in comments and are not
    always appropriate for the given table.

    Parameters
    ----------
    filename : pathlib.Path
        The filesystem location of the table.
    columns : list of str
        The column headers to use for this table.

    Returns
    -------
    pandas.DataFrame

    """
    return pd.read_csv(filename, sep="\t", comment="#", header=None, names=columns)
