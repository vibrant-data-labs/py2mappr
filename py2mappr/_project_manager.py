import py2mappr._core as core
from pandas import DataFrame

_current_project: core.OpenmapprProject = None

def has_project():
    global _current_project
    return _current_project is not None

def get_project(data_frame: DataFrame = None, network_data_frame: DataFrame = None):
    global _current_project
    if _current_project is not None:
        return _current_project
    
    if data_frame is None:
        raise ValueError('No data frame was provided')

    _current_project = core.OpenmapprProject(data_frame, network_data_frame)
    return _current_project