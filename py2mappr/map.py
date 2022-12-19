from pathlib import Path
from typing import List, Tuple
from py2mappr._core.project import OpenmapprProject
from py2mappr._layout.clustered_scatterplot import ClusteredScatterplotLayout
from py2mappr._layout.geo import GeoLayout

from py2mappr._layout.scatterplot import ScatterplotLayout
from ._project_manager import get_project, has_project
from ._layout import ClusteredLayout, PLOT_TYPE, Layout
from ._builder import build_map
import py2mappr.publish as publisher
from pandas import DataFrame

_debug = False


def create_map(
    data_frame: DataFrame,
    network_df: DataFrame = None,
    layout_type: PLOT_TYPE = "clustered",
) -> Tuple[OpenmapprProject, Layout]:
    """
    Creates a new mappr project with the layout and returns the project and the
    layout.

    Parameters
    ----------
    data_frame: DataFrame, required. The data frame of datapoints with its
    attributes (columns) to be used in the project.

    network_df: DataFrame, optional. The data frame of edges with its
    attributes (columns) to be used in the project. Noting that the network_df
    is optional in this method, it is expected to be set later using
    :func:`set_network`.

    layout_type: str, optional. The type of the layout to be created as the
    first layout in the project. The default is "clustered".

    Returns
    -------
    `Tuple[OpenmapprProject, Layout]`: The project and the created layout.

    Examples
    --------
    Creating and running a new project with a clustered layout:

    >>> project, layout = mappr.create_map(datapoints, network)
    >>> layout.name = "First Layout"
    >>> project.set_display_data(title="My Project")
    >>> mappr.show()
    """
    project = get_project(data_frame, network_df)
    project.set_debug(_debug)
    layout = create_layout(data_frame, layout_type)
    return project, layout


def create_layout(
    data_frame: DataFrame = None, layout_type: PLOT_TYPE = "clustered"
):
    """
    Creates a new layout in the current project.

    Parameters
    ----------
    data_frame: DataFrame, optional. The data frame of datapoints with its
    attributes (columns) to be used in the project. If not provided, the
    current project's data frame will be used. Should be provided if there is
    no current project.

    layout_type: `PLOT_TYPE`, optional. The type of the layout to be created.
    The default is "clustered". The available types are: "clustered",
    "scatterplot", "clustered-scatterplot", "geo".

    Returns
    -------
    `Layout`: The created layout.

    Examples
    --------
    Creating a new layout in the current project:

    >>> layout = mappr.create_layout(datapoints, layout_type="scatterplot")
    >>> layout.name = "My Custom Scatterplot"
    >>> mappr.show()
    """
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
    """
    Sets the network data frame of the current project. Must be called if the
    network data frame was not provided in the :func:`create_map` method.

    Parameters
    ----------
    network_df: DataFrame, required. The data frame of edges with its
    attributes (columns) to be used in the project.

    Examples
    --------
    Setting the network data frame of the current project:

    >>> project, layout = mappr.create_map(datapoints)
    >>> mappr.set_network(network)
    """
    project = get_project()
    project.set_network(network_df)


def show(PORT=8080, out_folder: Path = "data_out", detach: List[Layout] = []):
    """
    Builds and runs the current project. Shortcut for calling :func:`build` and
    :func:`run` with :func:`local` type.

    Parameters
    ----------
    PORT: int, optional. The port to be used in the local server. The default
    is 8080.

    out_folder: Path, optional. The output folder to be used in the build
    process. The default is "data_out".

    detach: List[Layout], optional. The list of layouts to be detached from the
    project. The default is empty list.

    Examples
    --------
    Building and running the current project:

    >>> project, layout = mappr.create_map(datapoints)
    >>> mappr.set_network(network)
    >>> mappr.show()
    """
    project = get_project()
    build_map(
        project, out_folder=out_folder, start=True, PORT=PORT, detach=detach
    )
    publisher.set_player_directory(out_folder)
    publisher.run([publisher.local(out_folder, PORT=PORT)])


def build(out_folder: Path = "data_out", detach: List[Layout] = []):
    """
    Builds the current project.

    Parameters
    ----------
    out_folder: Path, optional. The output folder to be used in the build
    process. The default is "data_out".

    detach: List[Layout], optional. The list of layouts to be detached from the
    project. The default is empty list.

    Examples
    --------
    Building the current project:

    >>> project, layout = mappr.create_map(datapoints, network)
    >>> mappr.build()
    """
    project = get_project()
    build_map(project, out_folder=out_folder, start=False, detach=detach)
    publisher.set_player_directory(out_folder)


def set_debug(debug: bool = True):
    """
    Sets the debug mode of the current project. This turns on the console output
    of the project during the build time.

    Parameters
    ----------
    debug: bool, optional. The debug mode to be set. The default is True.

    Examples
    --------
    Setting the debug mode of the current project:

    >>> project, layout = mappr.create_map(datapoints, network)
    >>> mappr.set_debug()
    """
    global _debug
    _debug = debug
    if has_project():
        project = get_project()
        project.set_debug(debug)


def launch_publish(s3_bucket: str):
    """
    Builds and publishes the current project to the given S3 bucket. Shortcut
    for calling :func:`build` and :func:`publish` with :func:`s3` type.
    The AWS configuration must be set in the `config.ini` file.

    Parameters
    ----------
    s3_bucket: str, required. The S3 bucket to be used in the publishing
    process.

    Examples
    --------
    Building and publishing the current project:

    >>> project, layout = mappr.create_map(datapoints, network)
    >>> mappr.launch_publish("my-bucket")
    """
    project = get_project()
    path = build_map(project, start=False)
    publisher.set_player_directory(path)
    publisher.run([publisher.s3(s3_bucket, path)])
