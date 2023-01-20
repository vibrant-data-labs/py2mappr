from typing import List, Dict, Any
from .warn import warn


def __no_attr(path: str, attr: str, datapoint: Dict[str, Any]):
    return attr not in datapoint[path] or datapoint[path][attr] is None


def has_no_attrs(attrs: List[str], datapoint: Dict[str, Any]):
    return any([__no_attr("attr", attr, datapoint) for attr in attrs])


def validate_layout_attr(attr: str, layout_dict: Dict[str, Any]):
    layout_name = layout_dict["snapName"]
    if __no_attr("layout", attr, layout_dict):
        warn(f"{layout_name}: {attr} is not set in layout")


def validate_layout_setting(attr: str, layout_dict: Dict[str, Any]):
    layout_name = layout_dict["snapName"]
    if __no_attr("settings", attr, layout_dict["layout"]):
        warn(f"{layout_name}: {attr} is not set in layout")


def validate_node_attributes(
    layout_name: str,
    attrs: List[str],
    datapoints: List[Dict[str, Any]],
    type: str = "datapoints",
):
    missed_dp = [
        datapoint for datapoint in datapoints if has_no_attrs(attrs, datapoint)
    ]

    if len(missed_dp) == len(datapoints):
        warn(f"{layout_name}: Attributes {attrs} are missing for all {type}.")
    elif len(missed_dp) > 0:
        warn(
            f"{layout_name}: {len(missed_dp)} {type} are missing one of {attrs} attributes."
        )


def validate_xy_attributes(
    layout_dict: Dict[str, Any], datapoints: List[Dict[str, Any]]
):
    layout_name = layout_dict["snapName"]
    # check x/y attributes
    plot_type = layout_dict["layout"]["plotType"]
    if plot_type != "clustered-scatterplot":
        validate_layout_attr("xaxis", layout_dict)
        validate_layout_attr("yaxis", layout_dict)
        x_attr = layout_dict["layout"]["xaxis"]
        y_attr = layout_dict["layout"]["yaxis"]

        attrs = list(filter(lambda x: x is not None, [x_attr, y_attr]))

        if len(attrs) == 0:
            return

        validate_node_attributes(layout_name, attrs, datapoints)
    else:  # plot_type == "clustered-scatterplot"
        validate_layout_attr("nodeXAttr", layout_dict)
        validate_layout_attr("nodeYAttr", layout_dict)
        validate_layout_attr("clusterXAttr", layout_dict)
        validate_layout_attr("clusterYAttr", layout_dict)

        node_x_attr = layout_dict["layout"]["nodeXAttr"]
        node_y_attr = layout_dict["layout"]["nodeYAttr"]
        cluster_x_attr = layout_dict["layout"]["clusterXAttr"]
        cluster_y_attr = layout_dict["layout"]["clusterYAttr"]

        attrs = list(
            filter(
                lambda x: x is not None,
                [node_x_attr, node_y_attr, cluster_x_attr, cluster_y_attr],
            )
        )

        if len(attrs) == 0:
            return

        validate_node_attributes(layout_name, attrs, datapoints)


def __validator(
    layout_dict: Dict[str, Any],
    datapoints: List[Dict[str, Any]],
    type: str = "datapoints",
):
    def validate(
        condition_setting: str, condition_value: Any, validate_attr: str
    ):
        layout_name = layout_dict["snapName"]

        if (
            layout_dict["layout"]["settings"][condition_setting]
            != condition_value
        ):
            return

        validate_layout_setting(validate_attr, layout_dict)
        attr = layout_dict["layout"]["settings"][validate_attr]
        if attr:
            validate_node_attributes(layout_name, [attr], datapoints, type)

    return validate


def validate_nodes(
    layout_dict: Dict[str, Any], datapoints: List[Dict[str, Any]]
):
    validate_xy_attributes(layout_dict, datapoints)
    node_validator = __validator(layout_dict, datapoints)
    node_validator("nodeImageShow", True, "nodeImageAttr")
    node_validator("drawLabels", True, "labelAttr")
    node_validator("nodeSizeStrat", "attr", "nodeSizeAttr")
    node_validator("nodeColorStrat", "attr", "nodeColorAttr")
    node_validator("nodeClusterAttr", None, "nodeClusterAttr")


def validate_links(layout_dict: Dict[str, Any], links: List[Dict[str, Any]]):
    link_validator = __validator(layout_dict, links, "edges")
    link_validator("edgeColorStrat", "attr", "edgeColorAttr")
    link_validator("edgeSizeStrat", "attr", "edgeSizeAttr")
