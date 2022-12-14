from typing import List
from py2mappr._layout.clustered_scatterplot import ClusteredScatterplotLayout
from py2mappr._layout.geo import GeoLayout

from py2mappr._layout.scatterplot import ScatterplotLayout
from ._project_manager import get_project, has_project
from ._layout import ClusteredLayout, PLOT_TYPE, Layout
from ._builder import build_map
from .publish import upload_to_s3
from pandas import DataFrame

_debug = False

def create_map(data_frame: DataFrame, network_df: DataFrame = None, layout_type: PLOT_TYPE = "clustered"):
    project = get_project(data_frame, network_df)
    project.set_debug(_debug)
    layout = create_layout(data_frame, layout_type)
    return project, layout

def create_layout(data_frame: DataFrame = None, layout_type: PLOT_TYPE = "clustered"):
    project = get_project(data_frame)
    project.set_debug(_debug)

    result_layout = None
    if layout_type == "clustered":
        result_layout = ClusteredLayout(project)
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

def show(PORT=8080):
    project = get_project()
    build_map(project, start=True, PORT=PORT)

def build(detach: List[Layout] = []):
    project = get_project()
    build_map(project, start=False, detach=detach)

def set_debug(debug: bool = True):
    global _debug
    _debug = debug
    if has_project():
        project = get_project()
        project.set_debug(debug)

def publish(s3_bucket: str, show=False):
    project = get_project()
    path = build_map(project, start=False)
    upload_to_s3(path, s3_bucket, show)
