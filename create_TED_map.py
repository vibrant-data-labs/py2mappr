#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:00:45 2020

@author: ericberlow
"""

import pathlib as pl #path library
from src.map_utils import create_map, create_snapshot


# configure the files and folders
wd = pl.Path.cwd()
nodesFile = wd/"TED_talks_demo"/"processed_data"/"nodes.csv"
linksFile = wd/"TED_talks_demo"/"processed_data"/"links.csv"
nodeAttrsFile = wd/"TED_talks_demo"/"processed_data"/"node_attrs.csv"
outFolder =  wd/"TED_talks_demo"/"map_data"

# configure the mapping for the read parameters
# maps are in the form of {"required param name": "name of column in datasheet"}
# the required param names are fixed and should not be changed.
node_attr_map = {"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"}
link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}

# create some snapshots
# snapshot - scatterplot
sn1 = create_snapshot(
    name="keyword themes",
    subtitle="another scatterplot",
    summaryImg="https://placekitten.com/220/160",
    description="A kitten is a <b>juvenile cat</b>. After being born, kittens display primary altriciality and are totally dependent on their mother for survival. They do not normally open their eyes until after seven to ten days. After about two weeks, kittens quickly develop and begin to explore the world outside the nest. After a further three to four weeks, they begin to eat solid food and grow adult teeth. Domestic kittens are highly social animals and usually enjoy human companionship.",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "OriginalX",
        "yaxis": "OriginalY",
        "settings": {"nodeSizeAttr": "popularity index", "nodeColorAttr": "keyword theme"},
    },
)

# snapshot - scatterplot
sn2 = create_snapshot(
    name="popularity by year",
    subtitle="scatterplot",
    summaryImg="https://placekitten.com/220/150",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "year published",
        "yaxis": "popularity index",
        "settings": {"nodeSizeAttr": "popularity index", "nodeColorAttr": "year published"},
    },
)


# snapshot - network with default layout settings (see layout templates/snapshot.yaml)
sn3 = create_snapshot(
    name="default settings",
    subtitle="network",
    summaryImg="https://placekitten.com/220/100",
)


# create map
create_map(
    nodesFile,
    linksFile,
    nodeAttrsFile,
    node_attr_map,
    link_attr_map,
    snapshots=[sn1, sn2, sn3],
    playerSettings={
        "modalTitle": "10 years of TED talks",
        "modalDescription": "<h6>This is a map of every talk on TED.com published from 2007 to 2017.  \
                            Keyword tags for each talk were enhanced by searching through the full transcript of each talk \
                            for the presence of any keyword from the TED's tag list, and adding it as a tag if was not already present. \
                            </h6><h6>Talks are linked if they have high overlap in their tags,  and they self-cluster into groups that \
                            tend to share similar *combinations* of tags. These Keyword Themes are auto-labeled by the 3 most commonly shared tags in the group. \
                            </h6>&#10;&#10;<h6>Data are from a public dataset on <a href=\"https://www.kaggle.com/rounakbanik/ted-talks/data \" target=\"_blank\">Kaggle</a>. \
                            <span>The network was generated using the open source python </span><a href=\"https://github.com/foodwebster/Tag2Network\" target=\"_blank\">'tag2network'</a><span> \
                            package, and visualized using <a href=\"http://openmappr.org\" target=\"_blank\">'openmappr'</a> - an open source network exploration tool. \
                            <br/></span></h6><h6><p><br/></p><p><i>This visualization is not optimized for mobile viewing and works best in Chrome browsers.   </i><br/></p></h6>",
                            
        "modalSubtitle": "<h5><span>How to Navigate this Network:</span><br/></h5><ul><li>Click on any node to see more details about that talk and watch the video. \
                            </li><li>Click the '<b>reset</b>' button to clear any selection.</li><li>Use the <b>Snapshots</b> panel to navigate between views.</li>\
                            <li>Use the <b>Filters</b> panel to select talks by any combination of traits (tags, views, event, talk duration, year published, etc).</li>\
                            <li>Click the '<b>Subset</b>' button to restrict the data to the selected nodes. The <b>Filters</b> panel will then summarize that <b>subset</b>. </li>\
                            <li>Use the <b>List</b> panel to see selected or subsetted talks as a sortable list - and to explore their details one by one by clicking on them.  </li></ul>",
    },
    outFolder=outFolder,
)
