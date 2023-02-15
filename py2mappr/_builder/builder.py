import re
from typing import Any, Dict, List, Union
from pathlib import Path
import shutil
import json
import os
import pandas as pd
import numpy as np
from py2mappr._core.config import AttributeConfig
from py2mappr._core.project import OpenmapprProject
from py2mappr._validation.validate_links import validate_source_target
from .._layout import Layout
from .build_dataset import build_attrDescriptors, build_datapoints
from .build_network import (
    build_nodes,
    build_links,
    build_nodeAttrDescriptors,
    build_linkAttrDescriptors,
)
from .build_settings import build_settings
from ._utils import flatten


class NpEncoder(json.JSONEncoder):
    """
    Special json encoder for numpy types
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def __noop_printer(*args, **kwargs):
    pass


def _printer(project: OpenmapprProject):
    """
    Returns a print function that prints only if project.debug is True

    Parameters
    ----------
    project : OpenmapprProject
        The project to check for debug flag

    Returns
    -------
    function
        A print function that prints only if project.debug is True
    """
    if not project.debug:
        return __noop_printer
    return print


_debug_print = None
template_path = Path(
    os.path.join(os.path.dirname(__file__), "..", "_templates")
)


def __write_dataset_file(
    df_datapoints: pd.DataFrame,
    datapointAttrs: Dict[str, AttributeConfig],
    out_data_dir: Path,
    exclude_md_attrs: List[str] = [],
):
    """
    Writes the dataset file `nodes.json` to the output directory

    Parameters
    ----------
    df_datapoints : pd.DataFrame
        The data frame of datapoints with its attributes (columns) to be used
        in the project.
    datapointAttrs : Dict[str, AttributeConfig]
        The attribute configurations for the datapoints
    out_data_dir : Path
        The output directory to write the file to
    """
    # collect datapoint attributes
    datapointAttribs = build_attrDescriptors(df_datapoints, datapointAttrs)
    datapointAttrTypes = {
        row["id"]: row["attrType"] for row in datapointAttribs
    }
    datapointRenderTypes = {
        row["id"]: row["renderType"] for row in datapointAttribs
    }

    # collect datapoints
    datapoints = build_datapoints(
        df_datapoints,
        datapointAttrTypes,
        datapointRenderTypes,
        exclude_md_attrs,
    )

    _debug_print(
        f"\t- processed {len(datapoints)} datapoints with {datapoints[0].keys()} where attr={list(datapointAttrs.keys())}"
    )

    # merge into dataset
    data = {"attrDescriptors": datapointAttribs, "datapoints": datapoints}

    with open(Path(out_data_dir) / "nodes.json", mode="w+") as f:
        json.dump(data, f, indent=4, cls=NpEncoder)

    return datapoints


def __write_network_file(
    df_datapoints: pd.DataFrame,
    datapointAttrs: Dict[str, AttributeConfig],
    df_links: pd.DataFrame,
    linkAttrs: Dict[str, Any],
    out_data_dir: Path,
):
    """
    Writes the network file `links.json` to the output directory

    Parameters
    ----------
    df_datapoints : pd.DataFrame
        The data frame of datapoints with its attributes (columns) to be used
        in the project.

    datapointAttrs : Dict[str, AttributeConfig]
        The attribute configurations for the datapoints

    df_links : pd.DataFrame
        The data frame of links with its attributes (columns) to be used
        in the project.

    linkAttrs : Dict[str, Any]
        The attribute configurations for the links

    out_data_dir : Path
        The output directory to write the file to
    """
    # collect nodes
    nodes = build_nodes(df_datapoints, datapointAttrs)
    _debug_print(
        f"\t- processed {len(nodes)} nodes with {nodes[0].keys()} where attr={list(nodes[0]['attr'].keys())}"
    )

    # collect links
    links = build_links(df_links, linkAttrs)
    _debug_print(
        f"\t- processed {len(links)} links with {links[0].keys()} where attr={list(links[0]['attr'].keys())}"
    )

    # collect node attributes
    nodeAttribs = build_nodeAttrDescriptors()
    _debug_print(
        f"\t- processed {len(nodeAttribs)} node attributes {[at['id'] for at in nodeAttribs]}"
    )

    # collect link attribs
    linkAttribs = build_linkAttrDescriptors(linkAttrs)
    _debug_print(
        f"\t- processed {len(linkAttribs)} link attributes {[at['id'] for at in linkAttribs]}"
    )

    # write network file
    data = {
        "id": "",
        "networkInfo": {},
        "clusterInfo": {},
        "nodes": nodes,
        "links": links,
        "nodeAttrDescriptors": nodeAttribs,
        "linkAttrDescriptors": linkAttribs,
    }

    with open(out_data_dir / "links.json", mode="w") as f:
        json.dump([data], f, indent=4, cls=NpEncoder)

    validate_source_target(links, nodes)

    return links


def __write_settings_file(
    snapshots: List[Dict],
    playerSettings: Dict[str, Any],
    datapoints: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    out_data_dir: Path,
):
    """
    Writes the settings file `settings.json` to the output directory

    Parameters
    ----------
    snapshots : List[Dict]
        The list of snapshots to be used in the project.

    playerSettings : Dict[str, Any]
        The player settings to be used in the project.

    out_data_dir : Path
        The output directory to write the file to
    """
    data = build_settings(snapshots, playerSettings, datapoints, links)
    with open(out_data_dir / "settings.json", mode="w") as f:
        json.dump(data, f, indent=4, cls=NpEncoder)
    return data


def __add_analytics(index_path: str, gtag_id: str = ""):
    """
    Adds the google analytics tracking code to the index.html file

    Parameters
    ----------
    index_path : str
        The path to the index.html file

    gtag_id : str, optional
        The google analytics tracking id, by default ""
    """
    if not gtag_id:
        return
    ga_template = ""
    with open(template_path / "ga_template.html", "r") as f:
        ga_template = f.read()
        ga_template = ga_template.replace("#{gtag_id}", gtag_id)

    index_tmpl = ""
    with open(index_path, "r") as f:
        index_tmpl = f.read()
    with open(index_path, "w") as f:
        index_tmpl = index_tmpl.replace("<!-- #{gtag} -->", ga_template)
        f.write(index_tmpl)

    _debug_print(f"\t- gtag added")


def __extract_sentence(text: str):
    """
    Utility method to extract the first sentence from the html text

    Parameters
    ----------
    text : str
        The html text

    Returns
    -------
    str
        The first sentence
    """
    if not text:
        return ""
    # clean text from html tags
    clean = re.compile("<.*?>")
    clear_text = re.sub(clean, "", text)
    sentences = clear_text.split(".")
    if len(sentences) > 1:
        return sentences[0] + "."
    return clear_text


def __set_opengraph_tags(index_path: str, player_settings: Dict[str, Any]):
    """
    Sets the opengraph tags (`og:title`, `og:description`, `og:image`) in the
    index.html file

    Parameters
    ----------
    index_path : str
        The path to the index.html file

    player_settings : Dict[str, Any]
        The player settings to be used in the project.
    """
    title = (
        player_settings.get("projectLogoTitle")
        or player_settings.get("headerTitle")
        or "openmappr | network exploration tool"
    )
    description = __extract_sentence(player_settings.get("headerSubtitle"))

    # find if there is an image in the project folder
    images = [
        *list(Path(index_path).parent.rglob("*.jpg")),
        *list(Path(index_path).parent.rglob("*.jpeg")),
        *list(Path(index_path).parent.rglob("*.png")),
        *list(Path(index_path).parent.rglob("*.gif")),
    ]

    image_url = (
        player_settings.get("sharingLogoUrl") or images[0].name
        if len(images) > 0
        else ""
    )
    og_template = ""
    with open(template_path / "og_template.html", "r") as f:
        og_template = f.read()
        og_template = og_template.replace("#{title}", title)
        og_template = og_template.replace("#{description}", description)
        og_template = og_template.replace("#{image}", image_url)

    index_tmpl = ""
    with open(index_path, "r") as f:
        index_tmpl = f.read()
    with open(index_path, "w") as f:
        index_tmpl = index_tmpl.replace("<!-- #{opengraph} -->", og_template)
        f.write(index_tmpl)

    _debug_print(f"\t- opengraph tags modified")


def build_map(
    project: OpenmapprProject,
    out_folder: Union[Path, str] = "data_out",
    start=False,
    PORT=8080,
    detach: List[Layout] = [],
):
    """
    Builds the map and saves it to the output folder

    Parameters
    ----------
    project : OpenmapprProject
        The project to be built

    out_folder : Union[Path, str], optional
        The output folder to save the project to, by default "data_out"

    start : bool, optional
        Whether to start the server after building the project, by default
        False


    PORT : int, optional
        The port to start the server on, by default 8080

    detach : List[Layout], optional
        The list of layouts to detach from the project, by default empty list
    Returns
    -------
    str
        The path to the player files
    """
    global _debug_print
    if not _debug_print:
        _debug_print = _printer(project)
    # create folders and copy the index file
    _debug_print(f">> creating folders")

    out_dir = Path(os.getcwd()) / out_folder
    out_data_dir = out_dir / "data"

    if not os.path.exists(Path(out_data_dir)):
        os.makedirs(Path(out_data_dir))

    # copy the index and run scripts to out directory
    shutil.copy(template_path / "index.html", out_dir)
    _debug_print(f"\t- copied {out_dir}/index.html")

    shutil.copy(template_path / "run_local.sh", out_dir)
    _debug_print(f"\t- copied {out_dir}/run_local.sh\n")

    # write the files
    _debug_print(f">> building dataset")
    exclude_md_attrs = [
        [snapshot.settings["labelAttr"], snapshot.settings["labelHoverAttr"]]
        for snapshot in project.snapshots
    ]

    out_nodes = __write_dataset_file(
        project.dataFrame,
        project.attributes,
        out_data_dir,
        flatten(exclude_md_attrs),
    )
    _debug_print(
        f"\t- new dataset file written to {out_data_dir / 'nodes.json'}.\n"
    )

    _debug_print(f">> building network")
    out_links = __write_network_file(
        project.dataFrame,
        project.attributes,
        project.network,
        project.network_attributes,
        out_data_dir,
    )
    _debug_print(
        f"\t- new network file written to {out_data_dir / 'links.json'}.\n"
    )

    _debug_print(f">> building settings")
    publish_snapshots = [
        snapshot for snapshot in project.snapshots if snapshot not in detach
    ]
    __write_settings_file(
        publish_snapshots,
        project.configuration,
        out_nodes,
        out_links,
        out_data_dir,
    )
    _debug_print(
        f"\t- new settings file written to {out_data_dir / 'settings.json'}.\n"
    )

    if project.publish_settings.get("gtag_id"):
        gtag_id = project.publish_settings.get("gtag_id")
        __add_analytics(out_dir / "index.html", gtag_id)

    __set_opengraph_tags(out_dir / "index.html", project.configuration)

    return out_dir
