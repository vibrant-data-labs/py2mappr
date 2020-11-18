import pandas as pd
from typing import Any, List, Dict
from src.utils import load_templates, merge


def build_nodes(dpPath: str, attr_map: Dict[str, str]) -> List[Dict[str, Any]]:
    df_datapoints: pd.DataFrame = pd.read_csv(dpPath)

    # load the template - node.yaml
    nodeTpl = load_templates("node")

    nodes = []
    for _, dp in df_datapoints.iterrows():

        # form the final datapoint with template
        nd = merge(
            nodeTpl,
            {
                "dataPointId": f'{dp["id"]}',
                "id": f'{dp["id"]}',
                "attr": {
                    "OriginalLabel": dp.get(attr_map.get("OriginalLabel", ""), "Node"),
                    "OriginalX": dp.get(attr_map.get("OriginalX", ""), 0),
                    "OriginalY": dp.get(attr_map.get("OriginalY", ""), 0),
                },
            },
        )
        # collect corresponding node for the datapoint
        nodes.append(nd)
    return nodes


def build_links(linksPath: str, attr_map: Dict[str, str]) -> List[Dict[str, Any]]:
    df_links: pd.DataFrame = pd.read_csv(linksPath)

    # load the template - link.yaml
    linkTpl = load_templates("link")

    links = []
    for idx, link in df_links.iterrows():
        # extract the link data (each row) as a dict
        edgeAttrs: Dict[str, Any] = dict(link)

        # required main params
        link = merge(
            linkTpl,
            {
                "id": f"{idx}",
                "source": f"{int(edgeAttrs[attr_map['source']])}",
                "target": f"{int(edgeAttrs[attr_map['target']])}",
                "isDirectional": edgeAttrs.get(attr_map.get("isDirectional", ""), False),
                "attr": {"OriginalLabel": f"{idx}"},
            },
        )

        # params other than ["id", "source", "target", "isdirectional"] in the datasheet
        # row gets pooled inside the 'attr' key. see template at link.yaml
        otherAttrs = {
            at: val for at, val in edgeAttrs.items() if at.lower() not in ["id", "source", "target", "isdirectional"]
        }
        linkMerged = merge(linkTpl, {"attr": otherAttrs})

        # collect link
        links.append(dict(linkMerged))

    return links


def build_nodeAttrDescriptors() -> List[Dict[str, Any]]:

    attrDescriptorTpl = load_templates("nodeAttribs")
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


def build_linkAttrDescriptors() -> List[Dict[str, Any]]:
    linkAttrbTpl = load_templates("linkAttribs")
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
