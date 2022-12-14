from typing import Any, Dict
import pandas as pd
import numpy as np
from .attr_types import ATTR_TYPE, RENDER_TYPE

def calculate_attr_types(df: pd.DataFrame) -> Dict[str, ATTR_TYPE]:
    attr_types = dict()
    # for each column, determine the type of attribute it is
    for column in df.columns.values:
        if df[column].dtype == np.number or df[column].dtype == np.int64:
            attr_types[column] = _detect_number_column(df, column)
        elif df[column].apply(lambda x: '|' in str(x)).any():
            attr_types[column] = "liststring"
        else:
            attr_types[column] = "string"

    return attr_types

def _detect_number_column(df: pd.DataFrame, column: str) -> ATTR_TYPE:
    if df[column].min() >= 1800 and df[column].max() <= 2100:
        return "year"
    if df[column].min() >= 1000000000 and df[column].max() <= 9999999999:
        return "timestamp"
    
    if df[column].min() % 1 == 0 and df[column].max() % 1 == 0:
        return "integer"
    
    return "float"

def calculate_render_type(df: pd.DataFrame, attr_types: Dict[str, ATTR_TYPE]) -> Dict[str, RENDER_TYPE]:
    render_types = dict()
    # for each column, determine the type of attribute it is
    for column in df.columns.values:
        if attr_types[column] == "integer" or attr_types[column] == "float" or attr_types[column] == "year":
            render_types[column] = "histogram"
        elif attr_types[column] == "liststring" or attr_types[column] == "string":
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
    elif len(str_set) > 40: #typical string length rather than number of tags
        return "wide-tag-cloud"
    else:
        return "horizontal-bars"