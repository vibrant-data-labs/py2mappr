
from typing import Literal
from ._settings import LayoutSettings
import uuid

PLOT_TYPE = Literal["original", "scatterplot", "clustered-scatterplot", "grid", "geo"]

class Layout:
    id: str
    name: str
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
        subtitle: str = None,
        image: str = None):
        self.id = str(uuid.uuid4())
        self.settings = settings
        self.plot_type = plot_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.name = name
        self.subtitle = subtitle
        self.image = image