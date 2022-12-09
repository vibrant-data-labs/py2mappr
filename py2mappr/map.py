from typing import Union
from ._project_manager import get_project
from ._layout import OriginalLayout, PLOT_TYPE
from pandas import DataFrame
from pathlib import Path

def create_map(data_frame: DataFrame):
    project = get_project(data_frame)
    project.snapshots.append(OriginalLayout(project))
    return project

def create_layout(data_frame: DataFrame, layout_type: PLOT_TYPE = "original"):
    project = get_project(data_frame)

    if layout_type == "original":
        project.snapshots.append(OriginalLayout(project))
    else:
        raise ValueError("Unknown layout type: " + layout_type)

def show():
    project = get_project()
    project.show()

def export_attributes(data_frame: DataFrame, out_path: Union[Path, str]):
    project = get_project(data_frame)
    # project.export_attributes(out_path)