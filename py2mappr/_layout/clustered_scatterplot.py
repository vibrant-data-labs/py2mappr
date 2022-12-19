from ._layout import Layout, LayoutSettings
from ._settings import base_layout_settings
from .._attributes import utils as attrutils
import copy

clustered_scatterplot_base_settings: LayoutSettings = {
    **copy.deepcopy(base_layout_settings),
    **LayoutSettings(
        # valid for scatterplot only
        xAxShow=True,
        yAxShow=True,
        xAxTickShow=True,
        yAxTickShow=True,
        xAxLabel="",
        yAxLabel="",
        xAxTooltip="",
        yAxTooltip="",
        # valid for scatterplot only
        invertX=False,
        invertY=True,
        scatterAspect=0.5,
        drawGroupLabels=False,
    ),
}


class ClusteredScatterplotLayout(Layout):
    """
    Describes the attributes for the clustered scatterplot layout. "plotType":
    "clustered-scatterplot"
    """

    clusterXAttr: str
    clusterYAttr: str

    def __init__(
        self,
        project,
        settings=copy.deepcopy(clustered_scatterplot_base_settings),
        x_axis="X",
        y_axis="Y",
        cluster_x="X",
        cluster_y="y",
        name=None,
        descr=None,
        subtitle=None,
        image=None,
    ):
        super().__init__(
            settings,
            "scatterplot",
            x_axis,
            y_axis,
            name,
            descr,
            subtitle,
            image,
        )
        self.clusterXAttr = cluster_x
        self.clusterYAttr = cluster_y
        self.calculate_layout(project)

    def calculate_layout(self, project):
        self.x_axis, self.y_axis = attrutils.find_node_xy_attr(
            project.dataFrame
        )
        self.clusterXAttr, self.clusterYAttr = attrutils.find_node_xy_attr(
            project.dataFrame
        )
        self.settings["nodeImageAttr"] = attrutils.find_node_image_attr(
            project.dataFrame
        )
        self.settings["nodePopImageAttr"] = attrutils.find_node_image_attr(
            project.dataFrame
        )
        self.settings["labelAttr"] = attrutils.find_node_label_attr(
            project.dataFrame
        )
        self.settings["nodeClusterAttr"] = attrutils.find_node_label_attr(
            project.dataFrame
        )
        self.settings["labelHoverAttr"] = attrutils.find_node_label_attr(
            project.dataFrame
        )
        self.settings["nodeColorAttr"] = attrutils.find_node_color_attr(
            project.dataFrame
        )
        self.settings["nodeSizeAttr"] = attrutils.find_node_size_attr(
            project.dataFrame
        )

        if project.network is not None:
            self.settings["edgeColorAttr"] = attrutils.find_node_color_attr(
                project.network
            )
            self.settings["edgeSizeAttr"] = attrutils.find_node_size_attr(
                project.network, ["source", "target"]
            )

    def toDict(self):
        return {
            **super().toDict(),
            "layout": {
                "plotType": "clustered-scatterplot",
                "nodeXAttr": self.x_axis,
                "nodeYAttr": self.y_axis,
                "clusterXAttr": self.clusterXAttr,
                "clusterYAttr": self.clusterYAttr,
                "settings": self.settings,
            },
        }
