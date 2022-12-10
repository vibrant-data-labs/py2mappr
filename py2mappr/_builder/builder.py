import re
from typing import Any, Dict, List, Union
from pathlib import Path
import shutil
import json
import os
import pandas as pd
from py2mappr._core.config import AttributeConfig
from py2mappr._core.project import OpenmapprProject
from .build_dataset import build_attrDescriptors, build_datapoints
from .build_network import build_nodes, build_links, build_nodeAttrDescriptors, build_linkAttrDescriptors
from .build_settings import build_settings

'''
from .utils import load_templates, merge
'''

def __noop_printer(*args, **kwargs):
    pass

def _printer(project: OpenmapprProject):
    if not project.debug:
        return __noop_printer
    return print

_debug_print = None
template_path = Path(os.path.join(os.path.dirname(__file__), '..', '_templates'))

def __write_dataset_file(df_datapoints: pd.DataFrame, datapointAttrs: Dict[str, AttributeConfig], out_data_dir: Path):
    # collect datapoint attributes
    datapointAttribs = build_attrDescriptors(df_datapoints, datapointAttrs)
    datapointAttrTypes = {row["id"]: row["attrType"] for row in datapointAttribs}

    # collect datapoints
    datapoints = build_datapoints(df_datapoints, datapointAttrTypes)
    
    _debug_print(
        f"\t- processed {len(datapoints)} datapoints with {datapoints[0].keys()} where attr={list(datapoints[0]['attr'].keys())}"
    )

    # merge into dataset
    data = {"attrDescriptors": datapointAttribs, "datapoints": datapoints}

    with open(Path(out_data_dir) / "nodes.json", mode="w+") as f:
        json.dump(data, f, indent=4)

def __write_network_file(
    df_datapoints: pd.DataFrame,
    datapointAttrs: Dict[str, AttributeConfig],
    df_links: pd.DataFrame,
    linkAttrs: Dict[str, Any],
    out_data_dir: Path,
):
    # collect nodes
    nodes = build_nodes(df_datapoints, datapointAttrs)
    _debug_print(f"\t- processed {len(nodes)} nodes with {nodes[0].keys()} where attr={list(nodes[0]['attr'].keys())}")

    # collect links
    links = build_links(df_links, linkAttrs)
    _debug_print(f"\t- processed {len(links)} links with {links[0].keys()} where attr={list(links[0]['attr'].keys())}")

    # collect node attributes
    nodeAttribs = build_nodeAttrDescriptors()
    _debug_print(f"\t- processed {len(nodeAttribs)} node attributes {[at['id'] for at in nodeAttribs]}")

    # collect link attribs
    linkAttribs = build_linkAttrDescriptors()
    _debug_print(f"\t- processed {len(linkAttribs)} link attributes {[at['id'] for at in linkAttribs]}")

    # write network file
    data = {
        **{"nodes": nodes, "links": links, "nodeAttrDescriptors": nodeAttribs, "linkAttrDescriptors": linkAttribs},
    }

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
    with open(template_path/'ga_template.html', 'r') as f:
        ga_template = f.read()
        ga_template = ga_template.replace('#{gtag_id}', gtag_id)

    index_tmpl = ''
    with open(index_path, 'r') as f:
        index_tmpl = f.read()
    with open(index_path, 'w') as f:
        index_tmpl = index_tmpl.replace('<!-- #{gtag} -->', ga_template)
        f.write(index_tmpl)
    
    _debug_print(f"\t- gtag added")

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
    with open(template_path/'og_template.html', 'r') as f:
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
    
    _debug_print(f"\t- opengraph tags modified")

def build_map(project: OpenmapprProject, outFolder: Union[Path, str] = "data_out"):
    global _debug_print
    if not _debug_print:
        _debug_print = _printer(project)
     # create folders and copy the index file
    _debug_print(f">> creating folders")
    
    out_dir = Path(os.getcwd()) / outFolder
    out_data_dir = out_dir / "data"

    if not os.path.exists(Path(out_data_dir)):
        os.makedirs(Path(out_data_dir))

    # copy the index and run scripts to out directory
    shutil.copy(template_path /"index.html", out_dir)
    _debug_print(f"\t- copied {out_dir}/index.html")

    shutil.copy(template_path/"run_local.sh", out_dir)
    _debug_print(f"\t- copied {out_dir}/run_local.sh\n")

    # write the files
    _debug_print(f">> building dataset")
    __write_dataset_file(project.dataFrame, project.attributes, out_data_dir)
    _debug_print(f"\t- new dataset file written to {out_data_dir / 'nodes.json'}.\n")

    _debug_print(f">> building network")
    __write_network_file(project.dataFrame, project.attributes, project.network, project.net_attributes)
    _debug_print(f"\t- new network file written to {out_data_dir / 'links.json'}.\n")

    _debug_print(f">> building settings")
    __write_settings_file(project.snapshots, project.configuration, out_data_dir)
    _debug_print(f"\t- new settings file written to {out_data_dir / 'settings.json'}.\n")

def build_map_old(
    project: OpenmapprProject,
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
    global _debug_print
    if not _debug_print:
        _debug_print = _printer(project)
    
    # create folders and copy the index file
    _debug_print(f">> creating folders")
    out_dir = Path(outFolder)
    out_data_path = out_dir / "data"
    if not out_data_path.exists():
        _debug_print(f"\t- new folder - {out_data_path}")
        out_data_path.mkdir(parents=True, exist_ok=True)
    else:
        _debug_print(f"\t- found existing. overwriting - {out_data_path}")

    # copy the index and run scripts to out directory
    shutil.copy(template_path /"index.html", out_dir)
    _debug_print(f"\t- copied {out_dir}/index.html")

    shutil.copy(template_path/"run_local.sh", out_dir)
    _debug_print(f"\t- copied {out_dir}/run_local.sh\n")

    # write the files
    _debug_print(f">> building dataset")
    __write_dataset_file(datapointsPath, datapointAttrPath, out_data_path)
    _debug_print(f"\t- new dataset file written to {out_data_path / 'nodes.json'}.\n")

    _debug_print(f">> building network")
    __write_network_file(datapointsPath, linksPath, node_attr_map, link_attr_map, out_data_path)
    _debug_print(f"\t- new network file written to {out_data_path / 'links.json'}.\n")

    _debug_print(f">> building settings")
    __write_settings_file(snapshots, playerSettings, out_data_path)
    _debug_print(f"\t- new settings file written to {out_data_path / 'settings.json'}.\n")

    __add_analytics(out_dir / 'index.html', gtag_id)

    __set_opengraph_tags(out_dir / 'index.html', playerSettings)

    _debug_print = None

