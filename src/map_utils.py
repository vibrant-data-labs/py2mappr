from typing import Any, List, Dict
from pathlib import Path
import shutil
import json
import uuid
from src.build_dataset import build_attrDescriptors, build_datapoints
from src.build_network import build_nodes, build_links, build_nodeAttrDescriptors, build_linkAttrDescriptors
from src.build_settings import build_settings
from src.utils import load_templates, merge


def __write_dataset_file(datapointsPath: str, datapointAttrPath: str, out_data_dir: Path):
    # collect datapoint attributes
    datapointAttribs = build_attrDescriptors(datapointAttrPath)
    datapointAttrTypes = {row["id"]: row["attrType"] for row in datapointAttribs}
    # print(f"\t- processed {len(datapointAttribs)} datapoint attributes {[at['id'] for at in datapointAttribs]}")

    # collect datapoints
    datapoints = build_datapoints(datapointsPath, datapointAttrTypes)
    print(
        f"\t- processed {len(datapoints)} datapoints with {datapoints[0].keys()} where attr={list(datapoints[0]['attr'].keys())}"
    )

    # merge into dataset
    datasetTpl = load_templates("dataset")
    data = {**datasetTpl, **{"attrDescriptors": datapointAttribs, "datapoints": datapoints}}
    with open(out_data_dir / "nodes.json", mode="w") as f:
        json.dump(data, f, indent=4)


def __write_network_file(
    datapointsPath: str,
    linksPath: str,
    node_attr_map: Dict[str, str],
    link_attr_map: Dict[str, str],
    out_data_dir: Path,
):
    # collect nodes
    nodes = build_nodes(dpPath=datapointsPath, attr_map=node_attr_map)
    print(f"\t- processed {len(nodes)} nodes with {nodes[0].keys()} where attr={list(nodes[0]['attr'].keys())}")

    # collect links
    links = build_links(linksPath=linksPath, attr_map=link_attr_map)
    print(f"\t- processed {len(links)} links with {links[0].keys()} where attr={list(links[0]['attr'].keys())}")

    # collect node attributes
    nodeAttribs = build_nodeAttrDescriptors()
    print(f"\t- processed {len(nodeAttribs)} node attributes {[at['id'] for at in nodeAttribs]}")

    # collect link attribs
    linkAttribs = build_linkAttrDescriptors()
    print(f"\t- processed {len(linkAttribs)} link attributes {[at['id'] for at in linkAttribs]}")

    # write network file
    networkTpl = load_templates("network")
    data = {
        **networkTpl,
        **{"nodes": nodes, "links": links, "nodeAttrDescriptors": nodeAttribs, "linkAttrDescriptors": linkAttribs},
    }
    # pprint.pprint(data)

    with open(out_data_dir / "links.json", mode="w") as f:
        json.dump([data], f, indent=4)


def __write_settings_file(snapshots: List[Dict], playerSettings: Dict[str, Any], out_data_dir: Path):
    data = build_settings(snapshots, playerSettings)
    with open(out_data_dir / "settings.json", mode="w") as f:
        json.dump(data, f, indent=4)
    return data


def create_map(
    datapointsPath: str,
    linksPath: str,
    datapointAttrPath: str,
    node_attr_map: Dict[str, str],
    link_attr_map: Dict[str, str],
    snapshots: List[Dict] = [],
    playerSettings: Dict[str, Any] = {},
    outFolder: str = "data_out",
):
    """Creates a map renderable in a browser.
       Outputs a folder with formatted data folder, index.html and run utility

    Args:
        datapointsPath (str): filepath for the datapoints
        linksPath (str): filepath for the edges
        datapointAttrPath (str): filespath for the datapoint attributes
        node_attr_map (Dict[str, str]): map of {required params: column-names} for the nodes
        link_attr_map (Dict[str, str]): map of {required params: column-names} for the links
        snapshots (List[Dict], optional): list of snapshots. Defaults to []
        playerSettings (Dict[str, str], optional): settings to customize the player (info, theme etc). Defaults to {}
        outFolder (str, optional): name of the output folder. Defaults to "data_out".
    """

    # create folders and copy the index file
    print(f">> creating folders")
    out_dir = Path(outFolder)
    out_data_path = out_dir / "data"
    if not out_data_path.exists():
        print(f"\t- new folder - {out_data_path}")
        out_data_path.mkdir(parents=True, exist_ok=True)
    else:
        print(f"\t- found existing. overwriting - {out_data_path}")

    # copy the index and run scripts to out directory
    shutil.copy("src/index.html", out_dir)
    print(f"\t- copied {out_dir}/index.html")

    shutil.copy("src/run_local.sh", out_dir)
    print(f"\t- copied {out_dir}/run_local.sh\n")

    # write the files
    print(f">> building dataset")
    __write_dataset_file(datapointsPath, datapointAttrPath, out_data_path)
    print(f"\t- new dataset file written to {out_data_path / 'nodes.json'}.\n")

    print(f">> building network")
    __write_network_file(datapointsPath, linksPath, node_attr_map, link_attr_map, out_data_path)
    print(f"\t- new network file written to {out_data_path / 'links.json'}.\n")

    print(f">> building settings")
    __write_settings_file(snapshots, playerSettings, out_data_path)
    print(f"\t- new settings file written to {out_data_path / 'settings.json'}.\n")


def create_snapshot(name: str, subtitle: str, summaryImg: str = "", description: str = "", layout_params: Dict = {}):
    """creates a snapshot object

    Args:
        name (str): snapshot title
        subtitle (str): snapshot subtitle
        summaryImg (str, optional): link to an image (ratio:110x80). Defaults to "".
        description (str, optional): description of snapshot. html ok.[description]. Defaults to "".
        layout_params (Dict, optional): see templates/snapshot.yaml. Defaults to {}.

    Returns:
        [Dict[str,Any]]: a snapshot object
    """
    snapTpl = load_templates("snapshot")

    # inject layout settings
    snapTpl["layout"] = merge(snapTpl["layout"], layout_params)

    # set name and subtitle
    snapTpl = merge(
        snapTpl,
        {
            "id": str(uuid.uuid4()),
            "snapName": name,
            "subtitle": subtitle,
            "summaryImg": summaryImg,
            "descr": description,
        },
    )

    return snapTpl