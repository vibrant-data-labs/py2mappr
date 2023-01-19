from typing import Any, Dict
import pandas as pd
import numpy as np
from .attr_types import ATTR_TYPE, RENDER_TYPE


def calculate_attr_types(df: pd.DataFrame) -> Dict[str, ATTR_TYPE]:
    """
    Calculates the attribute types of the columns of the given data frame.
    Based on the data type of the column, the attribute type is determined. If
    the column is a number, it is further analyzed to determine if it is a
    year, timestamp, integer or float. If the column is a string, it is further
    analyzed to determine if it is a list of strings or a single string.

    If column is of a number type, it checks the values of the column in the
    data frame. If the values are all integers, it is an `integer`. If the
    values are all floats, it is a `float`. If the values are all years, i.e.
    all values fall in range between 1800 and 2100, it is a `year`. If the
    values are all timestamps, i.e. all values fall in range between 1000000000
    and 9999999999, it is a `timestamp`.

    If the column is a string, it checks the values of the column in the data
    frame. If the values are all strings, it is a `string`. If the values are
    all lists of strings, i.e. any value contains a character '|', it is a
    `liststring`.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed.

    Returns
    -------
    `Dict[str, ATTR_TYPE]`: A dictionary with the column names as keys and the
    attribute types as values.
    """
    attr_types = dict()
    # for each column, determine the type of attribute it is
    for column in df.columns.values:
        if df[column].dtype == np.number or df[column].dtype == np.int64:
            attr_types[column] = _detect_number_column(df, column)
        elif df[column].apply(lambda x: "|" in str(x)).any():
            attr_types[column] = "liststring"
        else:
            attr_types[column] = "string"

    return attr_types


def _detect_number_column(df: pd.DataFrame, column: str) -> ATTR_TYPE:
    if df[column].min() >= 1800 and df[column].max() <= 2100:
        return "year"
    if df[column].min() >= 1000000000 and df[column].max() <= 9999999999:
        return "timestamp"

    min = df[column].min()
    max = df[column].max()

    if max - min == 1:
        return "float"

    if float(min).is_integer() and float(max).is_integer():
        return "integer"

    return "float"


def calculate_render_type(
    df: pd.DataFrame, attr_types: Dict[str, ATTR_TYPE]
) -> Dict[str, RENDER_TYPE]:
    """
    Calculates the render types of the columns of the given data frame. Based
    on the attribute type of the column, the render type is determined.

    * If the attribute type is `integer`, `float` or `year`, the render type is
    `histogram`.

    * If the attribute type is `liststring` or `string`, the render
    type is determined by the number of unique values in the column.

    * If the number of unique values is more than 100, the render type is
      `tag-cloud`.

    * If the number of unique values is more than 80, the render type is
    `tag-cloud_3`.

    * If the number of unique values is more than 60, the
    render type is `tag-cloud_2`.

    * If the number of unique values is more than 40, the render type is
    `wide-tag-cloud`.

    * Otherwise the render type is `horizontal-bars`.

    * If the attribute type is `timestamp`, the render type is `text`.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed. attr_types: Dict[str,
    ATTR_TYPE]. A dictionary with the column names as keys and the attribute
    types as values.

    Returns
    -------
    `Dict[str, RENDER_TYPE]`: A dictionary with the column names as keys and
    the render types as values.
    """
    render_types = dict()
    # for each column, determine the type of attribute it is
    for column in df.columns.values:
        if (
            attr_types[column] == "integer"
            or attr_types[column] == "float"
            or attr_types[column] == "year"
        ):
            render_types[column] = "histogram"
        elif (
            attr_types[column] == "liststring"
            or attr_types[column] == "string"
        ):
            render_types[column] = _detect_string_render_type(df, column)
        else:
            render_types[column] = "text"

    return render_types


def _detect_string_render_type(df: pd.DataFrame, column: str) -> RENDER_TYPE:
    str_set = set()
    df[column].apply(lambda x: str_set.update(str(x).split("|")))

    if len(str_set) > 100:
        return "tag-cloud"
    elif len(str_set) > 80:
        return "tag-cloud_3"
    elif len(str_set) > 60:
        return "tag-cloud_2"
    elif len(str_set) > 40:  # typical string length rather than number of tags
        return "wide-tag-cloud"
    else:
        return "horizontal-bars"
