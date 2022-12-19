from typing import Any, Dict, List, Literal, Tuple
from ._settings import LayoutSettings, PaletteColor
import uuid
import copy

PLOT_TYPE = Literal["clustered", "scatterplot", "clustered-scatterplot", "geo"]


class Layout:
    """
    The Layout class is the base class for all layouts. It contains the
    information for a single layout.
    """

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
        image: str = None,
    ):
        self.id = str(uuid.uuid4())
        self.settings = copy.deepcopy(settings)
        self.plot_type = plot_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.name = name or "Untitled"
        self.descr = descr or "<p></p>"
        self.subtitle = subtitle or ""
        self.image = image

    def set_display_data(
        self, title: str, subtitle: str, description: str, image=None
    ):
        """
        Set the display data for the layout.

        Parameters
        ----------
        title : str. The title of the layout.

        subtitle : str. The subtitle of the layout.

        description : str. The description of the layout.

        image : str. The image to be displayed in the layout.
        """
        self.name = title
        self.subtitle = subtitle
        self.descr = description
        self.image = image

    def set_clusters(self, cluster_attr: str = None):
        """
        Sets and enables the cluster settings for the layout.

        Parameters
        ----------
        cluster_attr : str. The attribute to be used for clustering.
        """
        self.settings.update(
            {
                "drawClustersCircle": True,
            }
        )

        if cluster_attr:
            self.settings.update(
                {
                    "nodeClusterAttr": cluster_attr,
                }
            )
        else:
            self.settings.update(
                {
                    "nodeClusterAttr": self.settings.get(
                        "nodeColorAttr", "Cluster"
                    ),
                }
            )

    def set_links(
        self,
        link_curve=0,
        link_weight=1,
        neighbors=1,
        direction="outgoing",
        edge_size_scaling: Tuple[float, float, float] = None,
    ):
        """
        Sets and enables the link settings for the layout.

        Parameters
        ----------
        link_curve : float. The curvature of the links.

        link_weight : float. The default weight of the links.

        neighbors : int. The number of neighbors to be displayed in the right
        panel.

        direction : all | outgoing | incoming. The direction of the links.

        edge_size_scaling : Tuple[float, float, float]. The scaling of the edge
        size.
        """
        self.settings.update(
            {
                "drawEdges": True,
                "edgeCurvature": link_curve,
                "edgeDirectionalRender": direction,
                "edgeSizeDefaultValue": link_weight,
                "nodeSelectionDegree": neighbors,
            }
        )

        if edge_size_scaling:
            self.settings.update(
                {
                    "edgeSizeMin": edge_size_scaling[0],
                    "edgeSizeMax": edge_size_scaling[1],
                    "edgeSizeMultiplier": edge_size_scaling[2],
                }
            )

    def set_nodes(
        self,
        node_color="",
        node_cluster="",
        node_size="",
        node_size_scaling: Tuple[float, float, float] = None,
    ):
        """
        Sets the node display settings for the layout. All attributes must be
        included in the source dataframe.

        Parameters
        ----------
        node_color : str. The attribute to be used for coloring the nodes.

        node_cluster : str. The attribute to be used for clustering the nodes.

        node_size : str. The attribute to be used for sizing the nodes.

        node_size_scaling : Tuple[float, float, float]. The scaling of the node
        size.
        """
        if node_color:
            self.settings.update(
                {
                    "nodeColorAttr": node_color,
                }
            )

        if node_cluster:
            self.settings.update(
                {
                    "nodeClusterAttr": node_cluster,
                }
            )

        if node_size:
            self.settings.update(
                {
                    "nodeSizeAttr": node_size,
                }
            )

        if node_size_scaling:
            self.settings.update(
                {
                    "nodeSizeMin": node_size_scaling[0],
                    "nodeSizeMax": node_size_scaling[1],
                    "nodeSizeMultiplier": node_size_scaling[2],
                }
            )

    def set_palette(
        self,
        ordinal_palette: List[PaletteColor] = None,
        numeric_palette: List[PaletteColor] = None,
    ):
        """
        Sets the palette for the layout.

        Parameters
        ----------
        ordinal_palette : List[PaletteColor]. The palette for ordinal attributes.

        numeric_palette : List[PaletteColor]. The palette for numeric attributes.
        """
        def _set_palette(palette: List[PaletteColor], palette_type: str):
            if palette:
                self.settings.update(
                    {
                        f"{palette_type}": palette,
                    }
                )
            else:
                return None

        _set_palette(ordinal_palette, "nodeColorPaletteOrdinal")
        _set_palette(numeric_palette, "nodeColorPaletteNumeric")
        _set_palette(ordinal_palette, "edgeColorPaletteOrdinal")
        _set_palette(numeric_palette, "edgeColorPaletteNumeric")

    def calculate_layout(self, project):
        """
        Recalculates the attributes for the layout.
        """
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
                "y": 0,
            },
        }
