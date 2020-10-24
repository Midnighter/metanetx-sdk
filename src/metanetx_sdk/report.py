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


"""Provide reporting and plotting functions."""


from typing import Literal

import humanize
import pandas as pd
from plotly import graph_objects as go


__all__ = (
    "report_value_count",
    "report_duplicates",
    "plot_bincount",
    "plot_frequency",
)


def report_value_count(data_frame: pd.DataFrame, column: str, digits: int = 2) -> str:
    """
    Report the number and percentage of non-empty values in the column.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        A data frame with one or more columns.
    column : str
        The name of the column to report on.
    digits : int, optional
        The number of digits to report in the percentage (default 2).

    Returns
    -------
    str
        The number of non-empty cells and a percentage of the total number of rows.

    """
    count = data_frame[column].notnull().sum()
    # The type of `count` is `numpy.int64` which when divided by zero yields `nan`.
    # This is undesired and we rather raise an exception here.
    if len(data_frame) == 0:
        raise ZeroDivisionError("The data frame is empty!")
    return f"{humanize.intcomma(count)} ({count / len(data_frame):.{digits}%})"


def report_duplicates(data_frame: pd.DataFrame, column: str) -> pd.Series:
    """
    Report the number of times elements occur in a column.

    Warnings
    --------
    Missing values in the column are ignored.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        A data frame with one or more columns.
    column : str
        The name of the column to report on.

    Returns
    -------
    pandas.Series
        A series whose index contains the unique elements of the column and whose
        values are counts of the number of times an element occurred.

    """
    return (
        data_frame.loc[data_frame[column].notnull(), :]
        .groupby(column, sort=False)
        .size()
    )


def plot_frequency(
    series: pd.Series,
    xaxis_title: str,
    yaxis_title: str = "Frequency",
    yaxis_scale: Literal["log", "linear"] = "log",
) -> go.Figure:
    """
    Compute a histogram of the given data points.

    Parameters
    ----------
    series : pandas.Series
        The data points to create a histogram of.
    xaxis_title : str
        The title for the horizontal plot axis.
    yaxis_title : str, optional
        The title for the vertial plot axis (default 'Frequency').
    yaxis_scale : {'log', 'linear'}, optional
        The vertical axis scale (default 'log').

    Returns
    -------
    plotly.graph_objects.Figure
        A simple histogram of the values as a bar plot.

    """
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=series,
        )
    )
    fig.update_layout(
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title,
        yaxis_type=yaxis_scale,
    )
    return fig


def plot_bincount(
    series: pd.Series,
    xaxis_title: str,
    yaxis_title: str = "Frequency",
    yaxis_scale: Literal["log", "linear"] = "log",
) -> go.Figure:
    """
    Generate a bar plot of the given values. Uses the index as tick labels.

    Parameters
    ----------
    series : pandas.Series
        The data points to create a histogram of.
    xaxis_title : str
        The title for the horizontal plot axis.
    yaxis_title : str, optional
        The title for the vertial plot axis (default 'Frequency').
    yaxis_scale : {'log', 'linear'}, optional
        The vertical axis scale (default 'log').

    Returns
    -------
    plotly.graph_objects.Figure
        A simple bar plot of the passed values. Uses the index of the series as tick
        labels on the horizontal axis.

    """
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=series.index,
            y=series,
        )
    )
    fig.update_layout(
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title,
        yaxis_type=yaxis_scale,
    )
    return fig
