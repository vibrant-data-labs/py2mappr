from pathlib import Path
import pandas as pd
from typing import Any, List, Dict, Union

from py2mappr._core.config import AttributeConfig
# from .utils import load_templates, merge
#from src.utils import load_templates, merge

def __build_node(node: pd.Series, attr_map: Dict[str, AttributeConfig]) -> Dict[str, Any]:
    # form the final datapoint with template
    nd = {
            "dataPointId": f'{node["id"]}',
            "id": f'{node["id"]}',
            "attr": {
                "OriginalLabel": node.get(attr_map.get("OriginalLabel", ""), "Node"),
                "OriginalX": node.get(attr_map.get("OriginalX", ""), 0),
                "OriginalY": node.get(attr_map.get("OriginalY", ""), 0),
            },
        }
    return nd

def build_nodes(df_datapoints: pd.DataFrame, attr_map: Dict[str, AttributeConfig]) -> List[Dict[str, Any]]:
    nodes = [__build_node(dp, attr_map) for _, dp in df_datapoints.iterrows()]

    return nodes

def __build_link(idx, link: pd.Series, attr_map: Dict[str, str]):
    edgeAttrs: Dict[str, Any] = dict(link)
    otherAttrs = {
        at: val for at, val in edgeAttrs.items() if at.lower() not in ["id", "source", "target", "isdirectional"]
    }
    result_link = {
                "id": f"{idx}",
                "source": f"{int(edgeAttrs[attr_map['source']])}",
                "target": f"{int(edgeAttrs[attr_map['target']])}",
                "isDirectional": edgeAttrs.get(attr_map.get("isDirectional", ""), False),
                "attr": {
                    "OriginalLabel": f"{idx}",
                    **otherAttrs,
                    },
            }

    return result_link

def build_links(df_links: pd.DataFrame, attr_map: Dict[str, str]) -> List[Dict[str, Any]]:
    links = [__build_link(idx, link, attr_map) for idx, link in df_links.iterrows()]
    return links


def build_nodeAttrDescriptors() -> List[Dict[str, Any]]:
    attrDescriptorTpl ={
            "id": "attrib id",
            "title": "attrib title",
            "visible": True,
            "visibleInProfile": False,
            "searchable": True,
            "attrType": "string",
            "renderType": "text",
            "metadata": {},
        }

    required_attrs = [
        {
            "id": "OriginalLabel",
            "title": "OriginalLabel",
            "visible": True,
            "visibleInProfile": False,
            "searchable": True,
            "attrType": "liststring",
            "renderType": "tag-cloud",
            "metadata": {},
        },
        {
            "id": "OriginalSize",
            "title": "OriginalSize",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "integer",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalX",
            "title": "OriginalX",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "float",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalY",
            "title": "OriginalY",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "float",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalColor",
            "title": "OriginalColor",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "color",
            "renderType": "categorybar",
            "metadata": {},
        },
    ]
    attrDescriptors = []

    for row in required_attrs:
        # extract the attr (each row) data as a dict
        attrs: Dict[str, Any] = {**row}

        # metadata
        meta_tpl = {
            "descr": "",
            "maxLabel": "",
            "ZminLabel": "",
        }
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


def build_linkAttrDescriptors() -> List[Dict[str, Any]]:
    linkAttrbTpl = {
        "id": "attrib id",
        "title": "attrib title",
        "visible": True,
        "searchable": True,
        "attrType": "string",
        "renderType": "text",
    }
    required_attrs = [
        {
            "id": "OriginalLabel",
            "title": "OriginalLabel",
            "visible": True,
            "visibleInProfile": False,
            "searchable": True,
            "attrType": "liststring",
            "renderType": "tag-cloud",
            "metadata": {},
        },
        {
            "id": "OriginalSize",
            "title": "OriginalSize",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "integer",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalColor",
            "title": "OriginalColor",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "color",
            "renderType": "categorybar",
            "metadata": {},
        },
        {
            "id": "weight",
            "title": "weight",
            "visible": True,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "float",
            "renderType": "histogram",
            "metadata": {},
        },
    ]
    attrDescriptors = []

    for row in required_attrs:
        # extract the attr (each row) data as a dict
        attrs: Dict[str, Any] = dict(row)

        # if title doesnt exist. copy from id.
        attrs["title"] = attrs["id"] if attrs["title"] == "" else attrs["title"]

        # merge with template to form the full descriptor
        at = {**linkAttrbTpl, **attrs}

        # collect attr descriptor
        attrDescriptors.append(at)

    return attrDescriptors
