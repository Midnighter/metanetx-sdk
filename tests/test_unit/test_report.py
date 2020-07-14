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


"""Ensure the expected outcomes of reporting functions."""


from string import ascii_lowercase

import pytest
from numpy import linspace
from pandas import DataFrame, Series

from metanetx_sdk import report


LETTERS = sorted(ascii_lowercase)[:5]


@pytest.mark.parametrize(
    "table, column, expected",
    [
        pytest.param(
            DataFrame({"z": []}),
            "foo",
            None,
            marks=pytest.mark.raises(exception=KeyError),
        ),
        pytest.param(
            DataFrame({"z": []}),
            "z",
            None,
            marks=pytest.mark.raises(exception=ZeroDivisionError),
        ),
        (DataFrame({"a": range(5)}), "a", "5 (100.00%)"),
        (DataFrame({"b": linspace(0.0, 1.0, 5)}), "b", "5 (100.00%)"),
        (DataFrame({"c": LETTERS}), "c", "5 (100.00%)"),
        (DataFrame({"d": [1, 1.5, None, "foo", "bar"]}), "d", "4 (80.00%)"),
        (DataFrame({"e": [None] * 5}), "e", "0 (0.00%)"),
    ],
)
def test_report_value_count(table: DataFrame, column: str, expected: str):
    """Expect the value counts to be accurate."""
    assert report.report_value_count(table, column) == expected


@pytest.mark.parametrize(
    "table, column, expected",
    [
        pytest.param(
            DataFrame({"z": []}),
            "foo",
            None,
            marks=pytest.mark.raises(exception=KeyError),
        ),
        (DataFrame({"a": []}), "a", Series([], dtype=int)),
        (
            DataFrame({"b": LETTERS + LETTERS}),
            "b",
            Series([2] * 5, index=LETTERS, dtype=int),
        ),
        (
            DataFrame({"c": ["foo", None, "bar"]}),
            "c",
            Series([1] * 2, index=["foo", "bar"], dtype=int),
        ),
    ],
)
def test_report_duplicates(table: DataFrame, column: str, expected: Series):
    """Expect the value counts to be accurate."""
    assert (report.report_duplicates(table, column).index == expected.index).all()
    assert (report.report_duplicates(table, column).values == expected.values).all()
