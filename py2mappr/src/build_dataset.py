from pathlib import Path
import pandas as pd
from typing import Any, List, Dict, Union
from .utils import load_templates

#from src.utils import load_templates


def build_attrDescriptors(datapointAttrPath: Union[Path, str]) -> List[Dict[str, Any]]:

    df_attrs: pd.DataFrame = pd.read_csv(str(datapointAttrPath))
    attrDescriptorTpl = load_templates("datapointAttribs")

    df_attrs.fillna(value="", inplace=True)
    attrDescriptors = []
    for _, row in df_attrs.iterrows():
        # extract the attr (each row) data as a dict
        attrs: Dict[str, Any] = dict(row)

        # metadata
        # meta_attrs = dict((k, attrs[k]) for k in attrDescriptorTpl["metadata"])
        # other_attrs = dict((k, attrs[k]) for k in attrs if k not in meta_attrs)
        # attrs = {**other_attrs, **{"metadata": meta_attrs}}
        meta_tpl = attrDescriptorTpl["metadata"]
        meta_attrs = dict((k, attrs[k]) for k in meta_tpl if k in attrs)
        other_attrs = dict((k, attrs[k]) for k in attrs if k not in meta_attrs)
        attrs = {**other_attrs, **{"metadata": {**meta_tpl, **meta_attrs}}}

        # if title doesnt exist. copy from id.
        attrs["title"] = attrs["id"] if attrs["title"] == "" else attrs["title"]
        # merge with template to form the full descriptor
        at = {**attrDescriptorTpl, **attrs}

        # collect attr descriptor
        attrDescriptors.append(at)

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