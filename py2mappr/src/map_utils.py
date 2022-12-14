from typing import Any, List, Dict, Union
from pathlib import Path
import shutil
import json
import uuid
import re
import os

from .build_dataset import build_attrDescriptors, build_datapoints
from .build_network import build_nodes, build_links, build_nodeAttrDescriptors, build_linkAttrDescriptors
from .build_settings import build_settings
from .utils import load_templates, merge
'''
from src.build_dataset import build_attrDescriptors, build_datapoints
from src.build_network import build_nodes, build_links, build_nodeAttrDescriptors, build_linkAttrDescriptors
from src.build_settings import build_settings
from src.utils import load_templates, merge
'''

def __write_dataset_file(datapointsPath: Union[Path, str], datapointAttrPath: Union[Path, str], out_data_dir: Path):
    # collect datapoint attributes
    datapointAttribs = build_attrDescriptors(str(datapointAttrPath))
    datapointAttrTypes = {row["id"]: row["attrType"] for row in datapointAttribs}
    # print(f"\t- processed {len(datapointAttribs)} datapoint attributes {[at['id'] for at in datapointAttribs]}")

    # collect datapoints
    datapoints = build_datapoints(str(datapointsPath), datapointAttrTypes)
    print(
        f"\t- processed {len(datapoints)} datapoints with {datapoints[0].keys()} where attr={list(datapoints[0]['attr'].keys())}"
    )

    # merge into dataset
    datasetTpl = load_templates("dataset")
    data = {**datasetTpl, **{"attrDescriptors": datapointAttribs, "datapoints": datapoints}}
    with open(out_data_dir / "nodes.json", mode="w") as f:
        json.dump(data, f, indent=4)


def __write_network_file(
    datapointsPath: Union[Path, str],
    linksPath: Union[Path, str],
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

def __add_analytics(index_path: str, gtag_id: str = ''):
    if not gtag_id:
        return
    ga_template = ''
    src_folder = os.path.dirname(__file__)
    with open(os.path.join(src_folder, 'ga_template.html'), 'r') as f:
        ga_template = f.read()
        ga_template = ga_template.replace('#{gtag_id}', gtag_id)

    index_tmpl = ''
    with open(index_path, 'r') as f:
        index_tmpl = f.read()
    with open(index_path, 'w') as f:
        index_tmpl = index_tmpl.replace('<!-- #{gtag} -->', ga_template)
        f.write(index_tmpl)
    
    print(f"\t- gtag added")

def __extract_sentence(text: str):
    if not text: 
        return ''
    # clean text from html tags
    clean = re.compile('<.*?>')
    clear_text = re.sub(clean, '', text)
    sentences = clear_text.split('.')
    if len(sentences) > 1:
        return sentences[0] + '.'
    return clear_text

def __set_opengraph_tags(index_path: str, player_settings: Dict[str, Any]):
    title = player_settings.get('projectLogoTitle') or \
                player_settings.get('headerTitle')  or \
                'openmappr | network exploration tool'
    description = __extract_sentence(player_settings.get('headerSubtitle'))
    image_url = player_settings.get('projectLogoImageUrl') or 'https://mappr-player.openmappr.org/img/openmappr_socialmedia.png'
    og_template = ''
    src_folder = os.path.dirname(__file__)
    with open(os.path.join(src_folder, 'og_template.html'), 'r') as f:
        og_template = f.read()
        og_template = og_template.replace('#{title}', title)
        og_template = og_template.replace('#{description}', description)
        og_template = og_template.replace('#{image}', image_url)

    index_tmpl = ''
    with open(index_path, 'r') as f:
        index_tmpl = f.read()
    with open(index_path, 'w') as f:
        index_tmpl = index_tmpl.replace('<!-- #{opengraph} -->', og_template)
        f.write(index_tmpl)
    
    print(f"\t- opengraph tags modified")

def create_map(
    datapointsPath: Union[Path, str],
    linksPath: Union[Path, str],
    datapointAttrPath: Union[Path, str],
    node_attr_map: Dict[str, str],
    link_attr_map: Dict[str, str],
    snapshots: List[Dict] = [],
    playerSettings: Dict[str, Any] = {},
    outFolder: Union[Path, str] = "data_out",
    gtag_id: str = None
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

    src_folder = os.path.dirname(__file__)
    # copy the index and run scripts to out directory
    shutil.copy(os.path.join(src_folder, "index.html"), out_dir)
    print(f"\t- copied {out_dir}/index.html")

    shutil.copy(os.path.join(src_folder, "run_local.sh"), out_dir)
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

    __add_analytics(out_dir / 'index.html', gtag_id)
    print(playerSettings)
    __set_opengraph_tags(out_dir / 'index.html', playerSettings)

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