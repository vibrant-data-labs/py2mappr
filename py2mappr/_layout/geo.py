from ._layout import Layout, LayoutSettings
from ._settings import base_layout_settings
from .._attributes import utils as attrutils
import copy

geo_base_settings: LayoutSettings = {
    **copy.deepcopy(base_layout_settings),
    **LayoutSettings(
        # valid for geo only
        mapboxMapID="mapbox/light-v10",
        drawGroupLabels=False,
        isGeo=True,
    ),
}


class GeoLayout(Layout):
    """
    Describes the attributes for the geo layout. "plotType": "geo"
    """

    def __init__(
        self,
        project,
        settings=copy.deepcopy(geo_base_settings),
        x_axis="Latitude",
        y_axis="Longitude",
        name=None,
        descr=None,
        subtitle=None,
        image=None,
    ):
        super().__init__(
            settings, "geo", x_axis, y_axis, name, descr, subtitle, image
        )
        self.calculate_layout(project)

    def calculate_layout(self, project):
        self.x_axis, self.y_axis = attrutils.find_node_xy_attr(
            project.dataFrame, "lat", "long"
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
                "plotType": "geo",
                "xaxis": self.x_axis,
                "yaxis": self.y_axis,
                "settings": self.settings,
            },
        }
