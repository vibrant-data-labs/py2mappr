
from typing import Any, Dict, Literal
from ._settings import LayoutSettings
import uuid

PLOT_TYPE = Literal["original", "scatterplot", "clustered-scatterplot", "geo"]

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

    def calculate_layout(self, project):
        pass

    def toDict(self) -> Dict[str, Any]:
        pass