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
projectPath = wd /("test_projects/digital_delta")
inDataPath = projectPath/"data_in"

nodesFile = inDataPath /"nodes.csv"
linksFile = inDataPath /"links.csv"
nodeAttrsFile = inDataPath/"node_attrs.csv"
outFolder = projectPath/"data_out"
# TODO: ?? linkAttrsFile = inDataPath/"link_attrs.csv"  ??? 



# configure the mapping for the read parameters
# maps are in the form of {"required param name": "name of column in datasheet"}
# the required param names are fixed and should not be changed.
node_attr_map = {"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"}
link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}

# create some snapshots
# snapshot - scatterplot

sn1 = create_snapshot(
    name="Consensus Network",
    
    subtitle="Root causes linked by what affects what",  
    summaryImg="https://www.dl.dropboxusercontent.com/s/t1idhxri5j0lihj/Screen%20Shot%202021-03-01%20at%209.16.13%20AM.png?dl=0",
    description="<p>Each node is a root cause and they are linked by what influences what.\
                </p><p><b>Node Size</b> - Total number of links</p><p><b>Node</b> <b>Color</b> - \
                Broad topic of the root cause.</p><p><b>Links</b><span> -  \
                Consensus of at least a 3 votes that one root cause has a strong influence on another, \
                and in the same way (positive vs negative). </span></p>\
                <p><b>Link direction </b><span>is</span><i> <b>clockwise influence from source to the target. </b></i></p>",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "category_cluster_X",
        "yaxis": "category_cluster_Y",
        "settings": {
            # node size
            "nodeSizeAttr": "Degree",
            "nodeSizeScaleStrategy": "linear", # "linear" or "log"
            "nodeSizeMin": 3,
            "nodeSizeMax": 15,
            "nodeSizeMultiplier": 1.3,
            "bigOnTop": False,
            # node color and images
            "nodeColorAttr": "Category",
            "nodeColorPaletteOrdinal": [
                        {
                            "col": "#61beac"
                        },
                        {
                            "col": "#f7e05f"
                        },
                        {
                            "col": "#beebf4"
                        },
                        {
                            "col": "#fbc9bb"
                        },
                        {
                            "col": "#d97c51"
                        },
                        {
                            "col": "#8f8e8f"
                        },
                        {
                            "col": "#84a484"
                        },
                        {
                            "col": "#b23333"
                        },
                        {
                            "col": "#994c00"
                        },
                        {
                            "col": "#0073bf"
                        },
                        {
                            "col": "#bf9900"
                        },
                        {
                            "col": "#4c9999"
                        },
                        {
                            "col": "#739900"
                        },
                        {
                            "col": "#732673"
                        }
                    ],
            "nodeImageShow": False,
            "nodeImageAttr": "",
            # link rendering
            "drawEdges": True,
            "edgeCurvature": 0.6,
            "edgeDirectionalRender": "all",
            "edgeSizeStrat": "fixed", #  "attr" // "fixed"
            "edgeSizeAttr": "votes", # size by 
            "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
            "edgeColorAttr": "OriginalColor",
            "edgeSizeMultiplier": 0.6,
            # neighbor rendering
            "nodeSelectionDegree": 1,
            # labels
            "drawGroupLabels": True,
            # layout rendering
            "xAxShow": False,
            "yAxShow": False,
            "invertX": False,
            "invertY": False,
            "scatterAspect": 0.3, # shigher than 0.5 spreads out the scatterplot horizontally
            "savedZoomLevel": 1,
        },
    },
)

# snapshot - scatterplot
sn2 = create_snapshot(
    name="Catalysts",
    subtitle="Catalyst factors and their relative position in the problem hierarchy",
    summaryImg="https://www.dl.dropboxusercontent.com/s/ps973fk5pbsfhs9/Screen%20Shot%202021-03-01%20at%206.58.06%20PM.png?dl=0",
    description="<p><b>Node Color</b> - &#34;Top Catalysts&#34; - yellow nodes were in the top 75th percentile of catalyst scores \
                on average over 1000 random link deletion trials.</p><p><b>Node Size</b> - &#34;Catalyst Score&#34; - \
                larger nodes have both high leverage and high reach. These are root cause which have few others that influence them, \
                but if solved they have high primary and secondary effects on the rest of the network.  </p>\
                <p><b>Link Color</b> - Grey links are positive (an increase in the source leads to an increase in the target). \
                Red links are negative (an increase in the source leads to a decrease in the target). \
                <b>Link Direction</b><span> is </span><i>clockwise from source to the target. </i></p>\
                <p><b>&#34;Upstream &lt;&lt;--&gt;&gt; Downstream&#34;</b> is the relative position in the causal flow hierarchy\
                of the network.  Nodes on the far right tend to be the 'downstream' recipients of long chains of influences, \
                while nodes at the far left are more 'upstream' with shorter average incoming influence chains. \
                <br/><span><b>&#34;Average Catalyst Score&#34;</b> is a keystone index of 2 Degree Reach  and Leverage. \
                Nodes at the top are root factors which, relative to others have fewer root factors that influence them but \
                if solved they have high primary and secondary influence on the rest of the network. \
                Note that most of the top Catalysts tend to be 'upstream' problems in the causal hierarchy of the network.</span></p>\
                <p><span>To account for known error in link over-counting, we randomly thinned the network 1,000 times to \
                20% connected (from 38%). Each metric shown here is the average score across all 1,000 sampled networks.  </span><br/></p><p></p>",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "Upstream <<-->> Downstream (Pctl)",
        "yaxis": "Avg Keystone Score",
        "camera": {
                "normalizeCoords": True,
                "x": 0,
                "y": 43.9873417721519,
                "r": 1.5
            },
        "settings": {
            # node sizing
            "nodeSizeAttr": "Avg Keystone Score", 
            "nodeSizeScaleStrategy": "linear", # "linear" or "log"
            "nodeSizeMin": 3,
            "nodeSizeMax": 20,
            "nodeSizeMultiplier": 1.3,
            # node color and images
            "nodeColorAttr": "Top Keystones (75pctl)",
            "nodeColorPaletteOrdinal": [
                        {
                            "col": "#61beac"
                        },
                        {
                            "col": "#f7e05f"
                        },
                        {
                            "col": "#beebf4"
                        },
                        {
                            "col": "#fbc9bb"
                        },
                        {
                            "col": "#d97c51"
                        },
                        {
                            "col": "#8f8e8f"
                        },
                        {
                            "col": "#84a484"
                        },
                        {
                            "col": "#b23333"
                        },
                        {
                            "col": "#994c00"
                        },
                        {
                            "col": "#0073bf"
                        },
                        {
                            "col": "#bf9900"
                        },
                        {
                            "col": "#4c9999"
                        },
                        {
                            "col": "#739900"
                        },
                        {
                            "col": "#732673"
                        }
                    ],
            "nodeImageShow": False,
            "nodeImageAttr": "",
            # link rendering
            "drawEdges": False,
            "edgeCurvature": 0.6,
            "edgeDirectionalRender": "all",
            "edgeSizeStrat": "fixed", # or "attr"
            "edgeSizeAttr": "votes", # size by similarity
            "edgeSizeMultiplier": .7,
            "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
            "edgeColorAttr": "OriginalColor",
            
            # neighbor rendering
            "nodeSelectionDegree": 0,
            # labels
            "drawGroupLabels": False, # cluster labels
            # layout rendering
            "xAxShow": True,
            "yAxShow": True,
            "invertX": False,
            "invertY": True,
            "scatterAspect": 0.5, # shigher than 0.5 spreads out the scatterplot horizontally
            # node right panel
            "nodeFocusShow": False,
            
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
        "startPage": "filter", #filter // snapshots // list // legend // splash?
        "headerTitle": "Ditigal Delta",
        "modalTitle": "Digital Delta",
        "headerImageUrl": "https://www.dl.dropboxusercontent.com/s/jpwr6oynmy5q9y4/Screen%20Shot%202021-01-28%20at%208.18.28%20AM.png?dl=0",
        "modalSubtitle": '<h3>Making Digital Experiences More Beautiful for Young People</h3><p>Digital Delta is a crowdsourced research \
                        project working to discover the key opportunities that impact youth wellbeing in digital places and experiences. </p>\
                        <p>This is a free and public tool for your use. Digital Delta crowdsourced its data from over 800 community members, \
                        56% under 25 years old. We analyzed how 77 root factors influenced each other that created a network with a clear \
                        structure to better understand this complicated problem.  The analysis revealed  3 opportunity areas comprised of 13 \
                        catalysts with the best chances of creating more beautiful digital experiences for youth as they grow up.</p>\
                        <p>Now, together with our partners and all of you, we are working toward that transformation. \
                        We encourage you to explore and play with the data through Open Mapper. You can dive into our process and outcomes \
                        we found on the Digital Delta Website. </p><p><br/></p>',
        "modalDescription": "<h3>How to Navigate this Network:</h3><ul><li>Click on any node to to see more details about it. </li>\
                        <li>Click the whitespace or '<b>Reset</b>' button to clear any selection.</li><li>Use the <b>Filters</b> panel \
                        to select nodes by any  combination of tags. </li><li>Click the <b>'Apply'</b> button to subset the data to \
                        the selected nodes - The <b>Filters</b> panel will then show a summary of that subset.<br/></li>\
                        <li>Use the <b>List</b> panel to see a sortable list of any nodes selected or subset. \
                        You can also browse their details one by one by clicking on them in the list.</li>\
                        <li>Use the Snapshots panel to navigate between views.</li></ul><p><br/></p><p>\
                        This visualization is not optimized for mobile devices and is best viewed in Chrome or Safari browsers\ \
                        on the laptop/desktop. </p>&#10;",
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

    