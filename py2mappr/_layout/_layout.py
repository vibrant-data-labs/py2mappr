
from typing import Any, Dict, Literal, Tuple
from ._settings import LayoutSettings
import uuid

PLOT_TYPE = Literal["clustered", "scatterplot", "clustered-scatterplot", "geo"]

class Layout:
    id: str
    name: str
    descr: str
    subtitle: str
    image: str
    is_enabled: bool = True
    plot_type: PLOT_TYPE
    x_axis: str
    y_axis: str
    settings: LayoutSettings

    def __init__(
        self,
        settings: LayoutSettings,
        plot_type: PLOT_TYPE,
        x_axis: str,
        y_axis: str,
        name: str = None,
        descr: str = None,
        subtitle: str = None,
        image: str = None):
        self.id = str(uuid.uuid4())
        self.settings = settings
        self.plot_type = plot_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.name = name or "Untitled"
        self.descr = descr or "<p></p>"
        self.subtitle = subtitle or ""
        self.image = image

    def set_display_data(self, title: str, subtitle: str, description: str):
        self.name = title
        self.subtitle = subtitle
        self.descr = description

    def set_clusters(self, cluster_attr: str):
        self.settings.update({
            "drawClustersCircle": True,
            "nodeClusterAttr": cluster_attr,
        })

    def set_links(self, link_curve = 0, link_weight = 1, neighbors = 1, direction = "outgoing"):
        self.settings.update({
            "drawEdges": True,
            "edgeCurvature": link_curve,
            "edgeDirectionalRender": direction,
            "edgeSizeDefaultValue": link_weight,
            "nodeSelectionDegree": neighbors,
        })

    def set_nodes(self, node_color = '', node_size = '', node_size_scaling: Tuple[float, float, float] = None):
        if node_color:
            self.settings.update({
                "nodeColorAttr": node_color,
            })
        
        if node_size:
            self.settings.update({
                "nodeSizeAttr": node_size,
            })

        if node_size_scaling:
            self.settings.update({
                "nodeSizeMin": node_size_scaling[0],
                "nodeSizeMax": node_size_scaling[1],
                "nodeSizeMultiplier": node_size_scaling[2],
            })

    def calculate_layout(self, project):
        pass

    def toDict(self) -> Dict[str, Any]:
        return {
          "id": self.id,
          "descr": self.descr,
          "snapName": self.name,
          "subtitle": self.subtitle,
          "summaryImg": self.image,
          "isEnabled": True,
          "isDeleted": False,
          "camera": {
              "normalizeCoords": True,
              "r": 1.3347904373327948,
              "x": 0,
              "y": 0
          },
        }