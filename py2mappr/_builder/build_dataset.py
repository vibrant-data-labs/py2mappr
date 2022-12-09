from pathlib import Path
import pandas as pd
from typing import Any, List, Dict, TypedDict, Union

from py2mappr._attributes.attr_types import ATTR_TYPE, RENDER_TYPE
from py2mappr._core.config import AttributeConfig, default_attr_config

class Datapoint(TypedDict):
    id: str
    attr: Dict[str, Any]

class Dataset(TypedDict):
    attrDescriptors: List[AttributeConfig]
    datapoints: List[Datapoint]

def build_attr_descriptor(column: str, override: pd.Series) -> AttributeConfig:
    attrs: AttributeConfig = dict(default_attr_config)

    # if title doesnt exist. copy from id.
    attrs["id"] = column
    attrs["title"] = attrs["id"] if attrs["title"] == "" else attrs["title"]

    #TODO: try predict attrType and renderType based on column type

    # use if override exists
    if override is not None:
        for key, val in override.items():
            if key in attrs:
                attrs[key] = val

    return attrs

def build_attrDescriptors(df: pd.DataFrame, attrs_df: pd.DataFrame = None) -> List[AttributeConfig]:
    attrDescriptors = map(
        df.columns.values,
        lambda column: build_attr_descriptor(column, attrs_df[column])
    )

    return attrDescriptors

def build_datapoints(dpPath: str, dpAttribTypes) -> List[Dict[str, Any]]:
    df_datapoints: pd.DataFrame = pd.read_csv(dpPath)

    # load datapoint template - datapoint.yaml
    datapointTpl = load_templates("datapoint")

    datapoints = []
    for _, dp in df_datapoints.iterrows():
        # structure the datapoint (each row) as a dict
        attrs: Dict[str, Any] = dict(dp)

        # validate the attr vals based on type.
        for key, val in attrs.items():
            if dpAttribTypes[key] == "liststring":
                # check if value is NaN or not string type
                if isinstance(val, str):
                    # convert any liststring attr into a list
                    attrs[key] = val.split("|") if "|" in val else [val]
                else:
                    attrs[key] = ""
            elif dpAttribTypes[key] == "float" or dpAttribTypes[key] == "integer" or dpAttribTypes[key] == "year":
                attrs[key] = val if not pd.isna(attrs[key]) else ""
            else:
                attrs[key] = val if not pd.isna(attrs[key]) else ""

        # merge attrs with template
        dp = {**datapointTpl, **{"id": f'{dp["id"]}', "attr": attrs}}

        # collect datapoint
        datapoints.append(dp)

    return datapoints