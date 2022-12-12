from typing import List
import pandas as pd
import numpy as np
import warnings

images=['image', 'picture', 'photo', 'img', 'img_url', 'imgurl']
labels = ['name', 'title', 'label']

def _find_most_filled_column(df: pd.DataFrame, column_names: List[str]) -> str:
    non_empty = df[column_names]
    non_empty = non_empty.isnull().sum()

    return non_empty.sort_values(ascending=True).index[0]

def find_node_image_attr(df: pd.DataFrame) -> str:
    columns: List[str] = df.columns.values.tolist()

    match_columns = [col for col in columns if col.lower() in images]

    if len(match_columns) == 0:
        return None

    return _find_most_filled_column(df, match_columns)

def find_node_label_attr(df: pd.DataFrame) -> str:
    columns: List[str] = df.columns.values.tolist()

    match_columns = [col for col in columns if col.lower() in labels]

    if len(match_columns) == 0:
        return None

    return _find_most_filled_column(df, match_columns)

def find_node_size_attr(df: pd.DataFrame, exclude: List[str] = []) -> str:
    columns = [col for col in df.select_dtypes(include=np.number).columns.tolist() if col.lower() not in exclude]

    if len(columns) == 0:
        return None

    return _find_most_filled_column(df, columns)

def find_node_color_attr(df: pd.DataFrame) -> str:
    unique_counts = df.nunique()
    lowest_distinct = unique_counts.min()
    lowest_distinct_columns = unique_counts[unique_counts == lowest_distinct].index.tolist()

    return _find_most_filled_column(df, lowest_distinct_columns)

def find_node_xy_attr(df: pd.DataFrame, pattern_x = "x", pattern_y = "y") -> str:
    columns = df.columns.tolist()
    xcolumns = [col for col in columns if pattern_x in col.lower()]
    
    if len(xcolumns) == 0:
        warnings.warn(f"No columns found with {pattern_x} in the name. X,Y coordinates must be specified explicitly")
        return None
    
    for col in xcolumns:
        ycol_name = col.lower().replace(pattern_x, pattern_y)
        for ycol in columns:
            if ycol.lower() == ycol_name:
                return col, ycol

    return None