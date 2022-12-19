import py2mappr._core as core
from pandas import DataFrame

_current_project: core.OpenmapprProject = None

def has_project():
    """
    Utility method to check if there is a project created.

    Returns
    -------
    `bool`: True if there is a project created, False otherwise.
    """
    global _current_project
    return _current_project is not None

def get_project(data_frame: DataFrame = None, network_data_frame: DataFrame = None):
    """
    Returns the current project. If there is no current project, it creates a
    new project with the provided data frame.

    Parameters
    ----------
    data_frame: DataFrame, optional. The data frame of datapoints with its
    attributes (columns) to be used in the project. If not provided, the
    current project's data frame will be used. Should be provided if there is
    no current project.

    network_data_frame: DataFrame, optional. The data frame of edges with its
    attributes (columns) to be used in the project. If not provided, the
    current project's network data frame will be used. Should be provided if
    there is no current project.

    Returns
    -------
    `OpenmapprProject`: The current project.

    Examples
    --------
    Creating a new project with a clustered layout:

    >>> project = mappr.get_project(datapoints, network)
    >>> project.set_display_data(title="My Project")
    >>> mappr.show()

    Exceptions
    ----------
    ValueError: If no data frame was provided and there is no current project.
    """
    global _current_project
    if _current_project is not None:
        return _current_project
    
    if data_frame is None:
        raise ValueError('No data frame was provided')

    _current_project = core.OpenmapprProject(data_frame, network_data_frame)
    return _current_project