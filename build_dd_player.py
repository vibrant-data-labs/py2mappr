#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 19:33:18 2021

@author: ericberlow
"""

import pathlib as pl  # path library
from src.map_utils import create_map, create_snapshot
import os
import http.server
import socketserver
import webbrowser


# configure the files and folders
wd = pl.Path.cwd()
projectPath = wd /"projects"/"dd_demo"
inDataPath = projectPath/"digitaldelta_data"

nodesFile = inDataPath /"nodes.csv"
linksFile = inDataPath /"links.csv"
nodeAttrsFile = inDataPath/"node_attrs.csv"
projectFolder = "DigitalDelta_player"
outFolder = projectPath/projectFolder



# configure the mapping for the read parameters
# maps are in the form of {"required param name": "name of column in datasheet"}
# the required param names are fixed and should not be changed.
node_attr_map = {"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"}
link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}

# create some snapshots
# snapshot - scatterplot

sn1 = create_snapshot(
    name="Causal Clusters",
    subtitle="blah blah",
    summaryImg="https://www.dl.dropboxusercontent.com/s/oocyibrvojcmieg/Screen%20Shot%202020-11-25%20at%207.20.12%20AM.png?dl=0",
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
        "xaxis": "x_tsne",
        "yaxis": "y_tsne",
        "settings": {
            # node size
            "nodeSizeAttr": "ClusterCentrality",
            "nodeSizeScaleStrategy": "linear", # "linear" or "log"
            "nodeSizeMin": 1,
            "nodeSizeMax": 20,
            "nodeSizeMultiplier": .5,
            "bigOnTop": True,
            # node color and images
            "nodeColorAttr": "Cluster",
            "nodeImageShow": False,
            "nodeImageAttr": "",
            # link rendering
            "drawEdges": True,
            "edgeCurvature": 0.6,
            "edgeDirectionalRender": "outgoing",
            "edgeSizeStrat": "fixed", # or "fixed"
            "edgeSizeAttr": "weight", # size by similarity
            "edgeSizeMultiplier": .7,
            # labels
            "drawGroupLabels": False,
            # layout rendering
            "xAxShow": False,
            "yAxShow": False,
            "scatterAspect": 0.4, # shigher than 0.5 spreads out the scatterplot horizontally
        },
    },
)

# snapshot - scatterplot
sn2 = create_snapshot(
    name="reach vs leverage",
    subtitle=".",
    summaryImg="https://www.dl.dropboxusercontent.com/s/4v0kkfjkjmjn5zz/Screen%20Shot%202020-11-25%20at%207.19.54%20AM.png?dl=0",
    description="<p>Talks are sorted horizontally by date published and vertically by &#34;popularity&#34;. \
                Since some topics (e.g. pop psychology or business leadership) are more inherently more popular than others (e.g. physics), \
                the views of each talk are indexed relative to the median views of its keyword theme. \
                Talks above the zero line had more views than expected relative to the typical talk of its keyword theme. \
                If you hover on or select a talk, the links display other talks with the most similar keywords. \
                If you hover over Keyword Theme or any other tags in the <b>Filters</b>, \
                you can see the popularity trends for that theme or tag over time. </p><p><br/></p>\
                <p><i>Colored by:  </i>Keyword Theme</p><p><i>Sized by: </i>Total Views</p>",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "leverage_pctl_mean",
        "yaxis": "reach_mean",
        "settings": {
            # node sizing
            "nodeSizeAttr": "keystone_mean", 
            "nodeSizeScaleStrategy": "linear", # "linear" or "log"
            "nodeSizeMin": 2,
            "nodeSizeMax": 10,
            "nodeSizeMultiplier": 1,
            # node color and images
            "nodeColorAttr": "Keystone",
            "nodeImageShow": False,
            "nodeImageAttr": "",
            # link rendering
            "drawEdges": False,
            "edgeCurvature": 0.6,
            "edgeDirectionalRender": "outgoing",
            "edgeSizeStrat": "fixed", # or "fixed"
            "edgeSizeAttr": "weight", # size by similarity
            "edgeSizeMultiplier": .7,
            # labels
            "drawGroupLabels": False, # don't show color-by labels
            # layout rendering
            "xAxShow": True,
            "yAxShow": True,
            "scatterAspect": 0.6, # shigher than 0.5 spreads out the scatterplot horizontally
            
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
    snapshots=[sn1,sn2], #,sn3],
    playerSettings={
        "modalTitle": "10 years of TED talks",
        "modalSubtitle": '<h6>This is a map of every talk on TED.com published from 2007 to 2017.  \
                            Keyword tags for each talk were enhanced by searching through the full transcript of each talk \
                            for the presence of any keyword from the TED\'s tag list, and adding it as a tag if was not already present.</h6>\
                            <h6>Talks are linked if they have high overlap in their tags,  and they self-cluster into groups that \
                            tend to share similar *combinations* of tags. These Keyword Themes are auto-labeled by the 3 most commonly shared tags in the group.</h6>\
                            &#10;&#10;<h6>Data are from a public dataset on <a href="https://www.kaggle.com/rounakbanik/ted-talks/data " target="_blank">Kaggle</a>. \
                            <span>The network was generated using the open source python </span><a href="https://github.com/foodwebster/Tag2Network" target="_blank">\'tag2network\'</a><span> \
                            package, and visualized using <a href="http://openmappr.org" target="_blank">\'openmappr\'</a> - an open source network exploration tool. \
                            <br/></span></h6><h6><p><br/></p><p><i>This visualization is not optimized for mobile viewing and works best in Chrome browsers.   </i><br/></p></h6>',
        "modalDescription": "<h5><span>How to Navigate this Network:</span><br/></h5><ul><li>Click on any node to see more details about that talk and watch the video. \
                            </li><li>Click the '<b>reset</b>' button to clear any selection.</li><li>Use the <b>Snapshots</b> panel to navigate between views.</li>\
                            <li>Use the <b>Filters</b> panel to select talks by any combination of traits (tags, views, event, talk duration, year published, etc).</li>\
                            <li>Click the '<b>Subset</b>' button to restrict the data to the selected nodes. The <b>Filters</b> panel will then summarize that <b>subset</b>. </li>\
                            <li>Use the <b>List</b> panel to see selected or subsetted talks as a sortable list - and to explore their details one by one by clicking on them.  </li></ul>",
    },
    outFolder=outFolder,
)

    
# launch local server and open browser to display map
def launch_map_in_browser(project_directory, PORT=5000): 
    '''
    launches a new tab in active browswer with the map
    project_directory : string, the directory with the project data (index.html and 'data' folder)
    '''
    web_dir = os.path.join(os.getcwd(), project_directory)
    os.chdir(web_dir) # change to project directory where index.html and data folder are
        
    webbrowser.open_new_tab('http://localhost:'+str(PORT)) # open new tab in browswer
    
    Handler = http.server.SimpleHTTPRequestHandler 
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT, "go to http://localhost:%s \nCTL_C to quit\n"%str(PORT))
        httpd.serve_forever()  
    
    
launch_map_in_browser(str(outFolder), PORT=5000)

    