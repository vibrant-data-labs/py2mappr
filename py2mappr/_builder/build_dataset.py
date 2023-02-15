from pathlib import Path
import pandas as pd
from typing import Any, List, Dict, TypedDict

from py2mappr._core.config import AttributeConfig, default_attr_config
from py2mappr._builder._utils import md_to_html
import copy


class Datapoint(TypedDict):
    id: str
    attr: Dict[str, Any]


class Dataset(TypedDict):
    attrDescriptors: List[AttributeConfig]
    datapoints: List[Datapoint]


def build_attr_descriptor(column: str, override: pd.Series) -> AttributeConfig:
    """
    Build an attribute descriptor from a column in a dataframe.

    Parameters
    ----------
    column : str. The column name in the dataframe.

    override : pd.Series. The series containing the override values for the
    attribute descriptor.

    Returns
    -------
    AttributeConfig. The attribute descriptor.
    """
    attrs: AttributeConfig = dict(copy.deepcopy(default_attr_config))

    # if title doesnt exist. copy from id.
    attrs["id"] = column
    attrs["title"] = attrs["id"] if attrs["title"] == "" else attrs["title"]

    # use if override exists
    if override is not None:
        for key, val in override.items():
            if key in attrs:
                attrs[key] = val

    return attrs


def build_attrDescriptors(
    data: Dict[str, AttributeConfig], attrs_df: pd.DataFrame = None
) -> List[AttributeConfig]:
    """
    Build the attribute descriptors for the dataset.

    Parameters
    ----------
    data : Dict[str, AttributeConfig]. The attribute descriptors for the
    dataset.

    attrs_df : pd.DataFrame, optional. The dataframe containing the attribute
    descriptors, by default None

    Returns
    -------
    List[AttributeConfig] The attribute descriptors for the dataset.
    """
    attrDescriptors = [
        build_attr_descriptor(key, attrs_df[key]) for key in data.keys()
    ]

    return attrDescriptors


def __build_datapoint(
    dp: pd.Series,
    dpAttribTypes: Dict[str, str],
    dpRenderTypes: Dict[str, str],
    exclude_md_attrs: List[str] = [],
) -> Datapoint:
    attrs: Dict[str, Any] = dict(dp)

    # validate the attr vals based on type.
    for key, val in attrs.items():
        if dpAttribTypes[key] == "liststring":
            # check if value is NaN or not string type
            if isinstance(val, str):
                # convert any liststring attr into a list
                attrs[key] = (
                    [x.strip() for x in val.split("|")]
                    if "|" in val
                    else [val]
                )
            else:
                attrs[key] = ""
        elif (
            dpAttribTypes[key] == "float"
            or dpAttribTypes[key] == "integer"
            or dpAttribTypes[key] == "year"
        ):
            attrs[key] = val if not pd.isna(attrs[key]) else ""
        else:
            attrs[key] = val if not pd.isna(attrs[key]) else ""

        if (
            dpAttribTypes[key] == "string"
            and dpRenderTypes[key] == "text"
            and key not in exclude_md_attrs
        ):
            attrs[key] = md_to_html(attrs[key])

    # merge attrs with template
    return {"id": f'{dp["id"]}', "attr": attrs}


def build_datapoints(
    df_datapoints: pd.DataFrame,
    dpAttribTypes: Dict[str, str],
    dpRenderTypes: Dict[str, str],
    exclude_md_attrs: List[str] = [],
) -> List[Dict[str, Any]]:
    """
    Build the datapoints for the dataset.

    Parameters
    ----------
    df_datapoints : pd.DataFrame. The dataframe containing the datapoints.

    dpAttribTypes : Dict[str, str]. The attribute types for the datapoints.

    dpRenderTypes : Dict[str, str]. The render types for the datapoints.
    Returns
    -------
    List[Dict[str, Any]] The datapoints for the dataset.
    """
    datapoints = [
        __build_datapoint(dp, dpAttribTypes, dpRenderTypes, exclude_md_attrs)
        for _, dp in df_datapoints.iterrows()
    ]

    return datapoints
