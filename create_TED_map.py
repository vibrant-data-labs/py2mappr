# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:00:45 2020

@author: ericberlow
"""

import pathlib as pl  # path library
from src.map_utils import create_map, create_snapshot


# configure the files and folders
wd = pl.Path.cwd()
nodesFile = wd / "TED_talks_demo" / "processed_data" / "nodes.csv"
linksFile = wd / "TED_talks_demo" / "processed_data" / "links.csv"
nodeAttrsFile = wd / "TED_talks_demo" / "processed_data" / "node_attrs.csv"
outFolder = wd / "TED_talks_demo" / "map_data"

# configure the mapping for the read parameters
# maps are in the form of {"required param name": "name of column in datasheet"}
# the required param names are fixed and should not be changed.
node_attr_map = {"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"}
link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}

# create some snapshots
# snapshot - scatterplot
'''
sn1 = create_snapshot(
    name="Keyword Themes",
    subtitle="Clusters of talks linked by shared keywords.",
    summaryImg="https://www.dl.dropboxusercontent.com/s/d9vdgqouelb2oq7/Screen%20Shot%202020-11-23%20at%202.45.08%20PM.png?dl=0",
    description="<p>Talks are linked if they have high overlap in their keywords. Similar talks self-cluster into <b>&#34;Keyword Themes&#34;</b>\
                - or groups of talks that tend to co-share similar tags. These clusters are auto-labeled by the 3 most commonly shared tags in the group.  \
                If you hover over or select a talk on the map, it's top most similar talks are also highlighted. </p><p><i>Colored by</i> \
                - Keyword Theme</p><p><i>Sized by</i> - Total Views</p><p><i>How to Navigate this Network:</i></p><\
                ul><li>Click on any node to see more details about that talk and watch the video. </li>\
                <li>Click the 'reset' button to clear any selection.</li>\
                <li>Use the <b>Slides</b> panel to navigate between views.</li>\
                <li>Use the <b>Filters</b> panel to select talks by any combination of traits (tags, views, event, talk duration, year published, etc).</li>\
                <li>Use the <b>Subset</b> button to restrict the data to the selected talks. The <b>Filters</b> panel will then summarize that <b>subset</b>. </li>\
                <li>Use the <b>List</b> panel to see selected talks as a sortable list - and to explore their details one by one.  </li></ul>",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "OriginalX",
        "yaxis": "OriginalY",
        "settings": {
            "nodeSizeAttr": "popularity_index",
            "nodeColorAttr": "keyword_theme",
            "nodeImageShow": True,
            "nodeImageAttr": "photo",
            "xAxShow": False,
            "yAxShow": False,
        },
    },
)
'''
# snapshot - scatterplot
sn2 = create_snapshot(
    name="popularity by year",
    subtitle="See which talks were most popular in a given year.",
    summaryImg="https://www.dl.dropboxusercontent.com/s/uepgmm7mwi5mxtj/Screen%20Shot%202020-11-23%20at%202.49.03%20PM.png?dl=0",
    description="<p>Talks are sorted horizontally by date published and vertically by &#34;popularity&#34;. \
                Since some topics (e.g. pop psychology or business leadership) are more inherently more popular than others (e.g. physics), \
                the views of each talk are indexed relative to the median views of its keyword theme. \
                Talks above the zero line had more views than expected relative to the typical talk of its keyword theme. \
                If you hover on or select a talk, the links display other talks with the most similar keywords. \
                If you hover over Keyword Theme in the <b>Legend</b>, or any tags in the <b>Filters</b>, \
                you can see the popularity trends for that theme or tag over time. </p><p><br/></p>\
                <p><i>Colored by:  </i>Keyword Theme</p><p><i>Sized by: </i>Total Views</p>",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "year_published",
        "yaxis": "popularity_index",
        "settings": {
            "nodeSizeAttr": "popularity_index", 
            "nodeColorAttr": "year_published"
        },
    },
)

'''
# snapshot - network with default layout settings (see layout templates/snapshot.yaml)
sn3 = create_snapshot(
    name="default settings",
    subtitle="network",
    summaryImg="https://placekitten.com/220/100",
)
'''

# create map
create_map(
    nodesFile,
    linksFile,
    nodeAttrsFile,
    node_attr_map,
    link_attr_map,
    snapshots=[sn2],# sn2, sn3],
    playerSettings={
        "modalTitle": "10 years of TED talks",
        "modalDescription": '<h6>This is a map of every talk on TED.com published from 2007 to 2017.  \
                            Keyword tags for each talk were enhanced by searching through the full transcript of each talk \
                            for the presence of any keyword from the TED\'s tag list, and adding it as a tag if was not already present. \
                            </h6><h6>Talks are linked if they have high overlap in their tags,  and they self-cluster into groups that \
                            tend to share similar *combinations* of tags. These Keyword Themes are auto-labeled by the 3 most commonly shared tags in the group. \
                            </h6>&#10;&#10;<h6>Data are from a public dataset on <a href="https://www.kaggle.com/rounakbanik/ted-talks/data " target="_blank">Kaggle</a>. \
                            <span>The network was generated using the open source python </span><a href="https://github.com/foodwebster/Tag2Network" target="_blank">\'tag2network\'</a><span> \
                            package, and visualized using <a href="http://openmappr.org" target="_blank">\'openmappr\'</a> - an open source network exploration tool. \
                            <br/></span></h6><h6><p><br/></p><p><i>This visualization is not optimized for mobile viewing and works best in Chrome browsers.   </i><br/></p></h6>',
        "modalSubtitle": "<h5><span>How to Navigate this Network:</span><br/></h5><ul><li>Click on any node to see more details about that talk and watch the video. \
                            </li><li>Click the '<b>reset</b>' button to clear any selection.</li><li>Use the <b>Snapshots</b> panel to navigate between views.</li>\
                            <li>Use the <b>Filters</b> panel to select talks by any combination of traits (tags, views, event, talk duration, year published, etc).</li>\
                            <li>Click the '<b>Subset</b>' button to restrict the data to the selected nodes. The <b>Filters</b> panel will then summarize that <b>subset</b>. </li>\
                            <li>Use the <b>List</b> panel to see selected or subsetted talks as a sortable list - and to explore their details one by one by clicking on them.  </li></ul>",
    },
    outFolder=outFolder,
)
