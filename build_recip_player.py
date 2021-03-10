##!/usr/bin/env python3
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
projectPath = wd / ("projects/private/TOG_20Q3")
inDataPath = projectPath / "data_in"

nodesFile = inDataPath / "nodes.csv"
linksFile = inDataPath / "links.csv"
nodeAttrsFile = inDataPath / "node_attrs.csv"
outFolder = projectPath / "data_out"


# configure the mapping for the read parameters
# maps are in the form of {"required param name": "name of column in datasheet"}
# the required param names are fixed and should not be changed.
node_attr_map = {"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"}
link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}

# create some snapshots
# snapshot - scatterplot

sn1 = create_snapshot(
    name="Grantee/Investee Keyword Themes",
    subtitle="Investments and Projects clustered into themes",
    summaryImg="https://www.dl.dropboxusercontent.com/s/zoyuukkrvx1d8mw/Screen%20Shot%202021-03-08%20at%201.56.19%20PM.png?dl=0",
    description="<p><span>This is an 'adjacency network' all active funding recipients from 8 companies - \
            Omidyar Network, Democracy Fund, Humanity United, Flourish, Luminate, Ulupono, Omidyar Network India, \
            and Imaginable Futures. Each node is a grantee, investee, or contractor (for direct activities). \
            If you hover over any one, it is linked to other recipients that are the most similar to it in the \
            keywords which describe what they do.  The keywords were assigned using text from each recipient's \
            website and LinkedIn profile as well as any available grant/investment descriptions. \
            </span><br/></p><p>The colored clusters are 'Keyword Themes' defined by groups of recipients that \
            tend to share similar combinations of tags. The Themes are auto-labeled by the three most common \
            keywords in the cluster. These clusters are a 'broad brush' view of themes across companies which \
            represent combinations of keywords that tend to be found together. Since each recipient has many tags \
            describing what they do, they don't always fit neatly in one box. So while the &#34;journalism, news, \
            media&#34; cluster contains recipients that <i>tend</i> to share those and other tags, some recipients \
            tagged &#34;journalism&#34; may have ended up in another thematic cluster because they have other tags \
            which linked them to recipients in that cluster. To search along one dimension (e.g. &#34;journalism&#34;) \
            open the <b>Filters</b> panel and select that tag, or search for that term in the <b>Search Bar.</b>   \
            </p><p><b>Node Color: </b>Keyword Theme</p><p>\
            <b>Node Size:</b>  Relative Funding Amount</p><p>\
            <b>Link Thickness:</b> Tag similarity</p>",
    layout_params={
        "plotType": "original",  # "scatterplot",
        # "xaxis": "Year(s) Funded",  # "x_tsne",
        # "yaxis": "# Investments",  # "y_tsne",
        "settings": {
            # node size
            "nodeSizeAttr": "Relative Amount",
            "nodeSizeScaleStrategy": "linear",  # "linear" or "log"
            "nodeSizeMin": 5,
            "nodeSizeMax": 15,
            "nodeSizeMultiplier": 0.9,
            "bigOnTop": False,
            # node color and images
            "nodeColorAttr": "Keyword Theme", 
            "nodeColorPaletteOrdinal": [
                {"col": "#ee4444"},
                {"col": "#4d82c4"},
                {"col": "#0099ff"},
                {"col": "#ffcc00"},
                {"col": "#66cccc"},
                {"col": "#99cc00"},
                {"col": "#993399"},
                {"col": "#b23333"},
                {"col": "#994c00"},
                {"col": "#0073bf"},
                {"col": "#bf9900"},
                {"col": "#4c9999"},
                {"col": "#739900"},
                {"col": "#732673"},
            ],
            "nodeImageShow": True,
            "nodeImageAttr": "Picture",
            # link rendering
            "drawEdges": True,
            "edgeCurvature": 0,
            "edgeDirectionalRender": "outgoing",  # "outgoing", "incoming", "all"
            "edgeSizeStrat": "attr",  #  "attr" // "fixed"
            "edgeSizeAttr": "weight",  # size by
            "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
            "edgeColorAttr": "OriginalColor",
            "edgeSizeMultiplier": 0.6,
            # neighbor rendering
            "nodeSelectionDegree": 1,
            # labels
            "drawGroupLabels": True,
            # layout rendering
            # "xAxShow": False,
            # "yAxShow": False,
            # "invertX": False,
            # "invertY": False,
            # "scatterAspect": 0.3,  # shigher than 0.5 spreads out the scatterplot horizontally
            "savedZoomLevel": 1,
        },
    },
)

# snapshot - scatterplot
sn2 = create_snapshot(
    name="Grantee/Investee Headquarters",
    subtitle="Investments and Projects on a Geographic Map",
    summaryImg="https://www.dl.dropboxusercontent.com/s/q3o7388p6vwm47d/Screen%20Shot%202021-03-08%20at%202.12.33%20PM.png?dl=0",
    description="<p>This is a view of the geographic locations (city, state) of the headquarters of each funding \
                recipient.  The geographic focal area(s) of a given recipient may not be in the same place it is \
                headquartered. To see the patterns of geographic foci of work, open the <b>Filters</b> panel and scroll \
                down to the &#34;Geo Focus&#34; tags.  If you hover over a recipient, it will show links to its most \
                similar 'neighbors'. In the <b>Filters</b> panel, if you hover over a Funder tag you can see the \
                geographic dispersion of the organization headquarters they fund. \
                </p><p><b>Node Color: </b><span>Funder</span><br/></p><p>\
                <b>Node Size:</b>  Relative Funding</p><p>\
                <b>Link Thickness:</b> Tag similarity</p><p><br/></p>",
    layout_params={
        "plotType": "geo",
        "xaxis": "Latitude",
        "yaxis": "Longitude",
        "camera": {"normalizeCoords": True, "x": 0, "y": 43.9873417721519, "r": 1.5},
        "settings": {
            # node sizing
            "nodeSizeAttr": "Relative Amount",
            "nodeSizeScaleStrategy": "linear",  # "linear" or "log"
            "nodeSizeMin": 2,
            "nodeSizeMax": 10,
            "nodeSizeMultiplier": 1.3,
            # node color and images
            "nodeColorAttr": "Funder(s)",
            "nodeColorPaletteOrdinal": [
                {"col": "#ee4444"},
                {"col": "#4d82c4"},
                {"col": "#0099ff"},
                {"col": "#ffcc00"},
                {"col": "#66cccc"},
                {"col": "#99cc00"},
                {"col": "#993399"},
                {"col": "#b23333"},
                {"col": "#994c00"},
                {"col": "#0073bf"},
                {"col": "#bf9900"},
                {"col": "#4c9999"},
                {"col": "#739900"},
                {"col": "#732673"},
            ],
            "nodeImageShow": True,
            "nodeImageAttr": "Picture",
            # link rendering
            "drawEdges": False,
            "edgeCurvature": 0.6,
            "edgeDirectionalRender": "outgoing",
            "edgeSizeStrat": "fixed",  # or "attr"
            "edgeSizeAttr": "weight",  # size by similarity
            "edgeSizeMultiplier": 0.4,
            "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
            "edgeColorAttr": "OriginalColor",
            # neighbor rendering
            "nodeSelectionDegree": 1,
            # labels
            "drawGroupLabels": False,  # cluster labels
            # layout rendering
            "xAxShow": False,
            "yAxShow": False,
            "invertX": False,
            "invertY": True,
            "scatterAspect": 0.5,  # shigher than 0.5 spreads out the scatterplot horizontally
            "isGeo": True,  # geographic layout
            # node right panel
            "nodeFocusShow": False,
        },
    },
)

"""
# snapshot - network with default layout settings (see layout templates/snapshot.yaml)
sn3 = create_snapshot(
    name="default settings",
    subtitle="network",
    summaryImg="https://placekitten.com/220/100",
)
"""

# create map
create_map(
    nodesFile,
    linksFile,
    nodeAttrsFile,
    node_attr_map,
    link_attr_map,
    snapshots=[sn1, sn2],  # ,sn3],
    playerSettings={
        "startPage": "filter",  # filter // snapshots // list // legend // splash?
        "headerTitle": "Investment Landscape",
        "modalTitle": "Investment Landscape",
        "headerImageUrl": "",
        "modalSubtitle": "<p>This is an 'adjacency network' - or thematic landscape - of all active grantees, investees, and direct activity projects \
                        across 8 companies - Democracy Fund, Flourish, Humanity United, Imaginable Futures, Luminate, Omidyar Network, \
                        Omidyar Network India, and Ulupono.</p><p>These data were compiled at the end of Q3 2020. Recipients and projects \
                        were considered 'active' if they were funded within the past 2 yeras and their grant has not expired, \
                        or, if they received an investment they have not yet exited. \
                        </p><p>NOTE - This visualization is designed for desktop viewing and has not been optimized for mobile. \
                        It works best in Chrome or Safari. </p>",
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
    """
    launches a new tab in active browswer with the map
    project_directory : string, the directory with the project data (index.html and 'data' folder)
    """
    web_dir = os.path.join(os.getcwd(), project_directory)
    os.chdir(web_dir)  # change to project directory where index.html and data folder are

    webbrowser.open_new_tab("http://localhost:" + str(PORT))  # open new tab in browswer

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT, "go to http://localhost:%s \nCTL_C to quit\n" % str(PORT))
        httpd.serve_forever()


launch_map_in_browser(str(outFolder), PORT=5000)
