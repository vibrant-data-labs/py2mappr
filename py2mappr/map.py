from typing import Union
from py2mappr._layout.clustered import ClusteredScatterplotLayout
from py2mappr._layout.geo import GeoLayout

from py2mappr._layout.scatterplot import ScatterplotLayout
from ._project_manager import get_project
from ._layout import OriginalLayout, PLOT_TYPE
from ._builder import build_map
from pandas import DataFrame

def create_map(data_frame: DataFrame, network_df: DataFrame = None, layout_type: PLOT_TYPE = "original"):
    project = get_project(data_frame, network_df)
    layout = create_layout(data_frame, layout_type)
    return project, layout

def create_layout(data_frame: DataFrame = None, layout_type: PLOT_TYPE = "original"):
    project = get_project(data_frame)

    result_layout = None
    if layout_type == "original":
        result_layout = OriginalLayout(project)
        pass
    elif layout_type == "scatterplot":
        result_layout = ScatterplotLayout(project)
    elif layout_type == "clustered-scatterplot":
        result_layout = ClusteredScatterplotLayout(project)
    elif layout_type == "geo":
        result_layout = GeoLayout(project)
    else:
        raise ValueError("Unknown layout type: " + layout_type)

    project.snapshots.append(result_layout)
    return result_layout

def set_network(network_df: DataFrame):
    project = get_project()
    project.set_network(network_df)

def show():
    project = get_project()
    build_map(project, start=True)

def build():
    project = get_project()
    build_map(project, start=False)

def publish(s3_bucket: str):
    pass