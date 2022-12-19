from pathlib import Path
import pandas as pd
from typing import Any, List, Dict, Union

from py2mappr._core.config import AttributeConfig

_from_keys = ["source", "Source", "from", "From"]
_to_keys = ["target", "Target", "to", "To"]


def __build_node(
    node: pd.Series, attr_map: Dict[str, AttributeConfig]
) -> Dict[str, Any]:
    # form the final datapoint with template

    title = (
        node.get("label")
        or node.get("id")
        or node.get("OriginalLabel")
        or "Node"
    )

    nd = {
        "dataPointId": f'{node["id"]}',
        "id": f'{node["id"]}',
        "attr": {
            "OriginalLabel": title,
            "OriginalX": node.get(attr_map.get("OriginalX", ""), 0),
            "OriginalY": node.get(attr_map.get("OriginalY", ""), 0),
        },
    }
    return nd


def build_nodes(
    df_datapoints: pd.DataFrame, attr_map: Dict[str, AttributeConfig]
) -> List[Dict[str, Any]]:
    """
    Build nodes from a dataframe of datapoints.

    Parameters
    ----------
    df_datapoints : pd.DataFrame. Dataframe of datapoints

    attr_map : Dict[str, AttributeConfig]. Attribute map for the nodes

    Returns
    -------
    List[Dict[str, Any]]. List of nodes

    Exceptions
    ----------
    ValueError. If the dataframe does not contain the source and target keys.
    """
    nodes = [__build_node(dp, attr_map) for _, dp in df_datapoints.iterrows()]

    return nodes


def __build_link(idx, link: pd.Series, attr_map: Dict[str, str]):
    edgeAttrs: Dict[str, Any] = dict(link)
    otherAttrs = {
        at: val
        for at, val in edgeAttrs.items()
        if at.lower() not in ["id", "source", "target", "isdirectional"]
    }

    source_key = next((k for k in _from_keys if k in edgeAttrs), None)
    target_key = next((k for k in _to_keys if k in edgeAttrs), None)

    if source_key is None or target_key is None:
        raise ValueError(
            f"Source or Target key not found in edge attributes. Keys found: {edgeAttrs.keys()}"
        )

    result_link = {
        "id": f"{idx}",
        "source": f"{int(edgeAttrs[source_key])}",
        "target": f"{int(edgeAttrs[target_key])}",
        "isDirectional": edgeAttrs.get(
            attr_map.get("isDirectional", ""), False
        ),
        "attr": {
            "OriginalLabel": f"{idx}",
            **otherAttrs,
        },
    }

    return result_link


def build_links(
    df_links: pd.DataFrame, attr_map: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Build links from a dataframe of edges.

    Parameters
    ----------
    df_links : pd.DataFrame. Dataframe of edges

    attr_map : Dict[str, str]. Attribute map for the links

    Returns
    -------
    List[Dict[str, Any]]. List of links
    """
    links = [
        __build_link(idx, link, attr_map) for idx, link in df_links.iterrows()
    ]
    return links


def build_nodeAttrDescriptors() -> List[Dict[str, Any]]:
    attrDescriptorTpl = {
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
            "visible": False,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "liststring",
            "renderType": "tag-cloud",
            "metadata": {},
        },
        {
            "id": "OriginalSize",
            "title": "OriginalSize",
            "visible": False,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "integer",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalX",
            "title": "OriginalX",
            "visible": False,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "float",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalY",
            "title": "OriginalY",
            "visible": False,
            "visibleInProfile": False,
            "searchable": False,
            "attrType": "float",
            "renderType": "histogram",
            "metadata": {},
        },
        {
            "id": "OriginalColor",
            "title": "OriginalColor",
            "visible": False,
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
        attrs["title"] = (
            attrs["id"] if attrs["title"] == "" else attrs["title"]
        )

        # merge with template to form the full descriptor
        at = {**attrDescriptorTpl, **attrs}

        # collect attr descriptor
        attrDescriptors.append(at)

    return attrDescriptors


def build_linkAttrDescriptors(
    linkAttrs: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Build link attribute descriptors from a dictionary of link attributes.

    Parameters
    ----------
    linkAttrs : Dict[str, Any]. Dictionary of link attributes

    Returns
    -------
    List[Dict[str, Any]]. List of link attribute descriptors
    """
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

    for row in [*required_attrs, *linkAttrs.values()]:
        # extract the attr (each row) data as a dict
        attrs: Dict[str, Any] = dict(row)

        # if title doesnt exist. copy from id.
        attrs["title"] = (
            attrs["id"] if attrs["title"] == "" else attrs["title"]
        )

        # merge with template to form the full descriptor
        at = {**linkAttrbTpl, **attrs}

        # collect attr descriptor
        attrDescriptors.append(at)

    return attrDescriptors
