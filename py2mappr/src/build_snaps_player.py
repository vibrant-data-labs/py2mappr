#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 05:45:43 2021

@author: ericberlow
basic templates for building player including:
> create opnemappr files from nodes and links
> add snapshots from one of 3 types:- Clustered, Scatterplot, Geo
> add player settings and descriptions
> build and launch player, with option to upload to s3
> the script at the bottom is an example  template of how to combine all into one 'build player' function 

"""

import pandas as pd
from .build_openmappr_files import write_openmappr_files # from py2mappr - create openmappr files
from .map_utils import create_map, create_snapshot # from py2mappr
import pathlib as pl
from . import launch_upload_player # from py2mappr


# default colors
cat_palette= [ # default categorical color palette
                {"col": "#1F4B8E"},
                {"col": "#DE432F"},
                {"col": "#7BA1DB"},
                {"col": "#B4E026"},
                {"col": "#7E8F49"},
                {"col": "#2A768F"},
                {"col": "#DE2F5C"},
                {"col": "#7BC3DB"},
                ]
num_palette=[# default numeric color palette endpoints
                {"col": "#BDBFC1"},# min grey
                {"col": "#750031"} # max dark red 
               # {"col": "#BC2020"} # max bright red
                ]
default_cluster_description = "<p><span>\
            Colored clusters are groups of points that 'huddle' together into themes based on similarity in their keywords.\
            Each theme is auto-labeled by the three most commonly shared keywords in the cluster. \
            While the clusters reflect combinations of keywords that tend to go together, any one keyword can occur in multiple themes.\
            </span></p>"

default_snap_howto = "<p><span>\
                Use the <b>Summary</b> tab to browse and select points by one or more keywords, tags, or other attributes. \
                If you click <i>Summarize</i>, the left panel will summarize the attributes for the selected group.\
                Use the <b>List</b> tab to see any selected points as a sortable list.\
                </span></p>"

default_geo_howto = "<p><span>\
            You can select a group of points on the map by holding 'shift' while you drag the cursor. \
            If you click <i>Summarize Selectin</i>, the left <b>Summary</b> panel will summarize the attributes for the selected group.\
            In the <b>Summary</b> panel, if you hover over a keyword or tag you can see it's geographic dispersion. \
            </span></p>"


def build_clustered_snapshot(node_color = 'Cluster',
                             cluster = None, # cluster by attr
                             node_size = "ClusterCentrality",                              
                             node_size_scaling = (5,15,.8), #min size, max size, multiplier
                             cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                             num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                             image_show = False, # show image in node
                             image_attr = "Photo",  # image attr name
                             links_show = True, # display links
                             link_curve = 0.6, # link curvature 0-1
                             link_weight = 1, # link thickness 
                             link_direction = 'outgoing', # "outgoing", "incoming", "all"
                             link_color_strategy = "gradient", # source / target / gradient / attr / select
                             link_color_attr = "OriginalColor", # or other categorical link attribute
                             neighbors = 1, # number of neighbors on hover/select
                             group_labels = True, # True = show group labels
                             node_labels = True, # True = show node labels
                             clusterCircles = False, # draw circles around clusters
                             title = "Thematic Clusters",
                             subtitle = "Nodes clustered into themes",
                             description_intro = "<p>This is a map of ...... Each node is a .... ",
                             cluster_description = default_cluster_description,
                             snap_howto = default_snap_howto,
                             thumbnail = "https://www.dl.dropboxusercontent.com/s/1jdc4hvp5zw6as9/Screen%20Shot%202021-03-31%20at%206.59.23%20AM.png?dl=0",                             
                             ):   
    if cluster == None:
        nodeClusterAttr = node_color
    else:
        nodeClusterAttr = cluster            
    snap = create_snapshot(
        name=title,
        subtitle=subtitle,
        summaryImg= thumbnail,
        description= description_intro + cluster_description + snap_howto, 
        layout_params={
            "plotType": "original",  # "scatterplot",
            "settings": {
                # node color and images
                "nodeColorAttr": node_color,
                "nodeClusterAttr": nodeClusterAttr,
                "nodeColorPaletteOrdinal": cat_palette,
                "nodeColorPaletteNumeric": num_palette,
                "nodeColorNumericScalerType": "RGB", # "HCL", "HCL Long", "LAB", "HSL"
                # node size
                "nodeSizeAttr":  node_size, 
                "nodeSizeScaleStrategy": "linear",  # "linear" or "log"
                "nodeSizeMin": node_size_scaling[0],
                "nodeSizeMax": node_size_scaling[1],
                "nodeSizeMultiplier": node_size_scaling[2],
                "bigOnTop": False,
                # image rendering
                "nodeImageShow": image_show,
                "nodeImageAttr": image_attr,
                # link rendering
                "drawEdges": links_show,
                "edgeCurvature": link_curve,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "OriginalSize", #"weight",  # size by
                "edgeSizeDefaultValue": link_weight, #0.2
                "edgeSizeMultiplier": 1, 
                "edgeColorStrat": link_color_strategy,  # gradient / source / target / gradient / attr / select
                "edgeColorAttr": link_color_attr, #"OriginalColor",
                "edgeColorPaletteNumeric":num_palette,
                "edgeColorPaletteOrdinal":cat_palette,
                # neighbor rendering
                "nodeSelectionDegree": neighbors,
                "isShowSelectedNodeTab": True, # right profile selected neighbors
                "neighbourListHoverDegree": 0,  # degree to show when hover on node in list              
                "selectedNodeCommonTitle": 'Neighbors', # tab title for neighbors list
                # labels
                "drawLabels": node_labels, # show/hide node labels
                "drawGroupLabels": group_labels, # show/hide group labels 
                "drawClustersCircle": clusterCircles, # show/hide cluster circles
                },
            },
        )
    return snap


def build_scatterplot_snapshot(
                               x,  # x axis attribute name
                               y, # y axis attribute name
                             axes_show = True,
                             x_invert = False,
                             y_invert = True,
                             aspect_ratio = 0.7, # 0.5 is square, >0.5 spreads out the scatterplot horizontally
                             node_color = "Cluster",
                             node_size = "ClusterCentrality",
                             cluster = None, # cluster by attr
                             clusterCircles = False,                            
                             node_size_scaling = (5,15,.8), #min size, max size, multiplier
                             cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                             num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                             image_show = False, # show image in node
                             image_attr = "Photo",  # image attr name
                             links_show = False, # display links
                             link_curve = 0.6, # link curvature 0-1
                             link_weight = 0.8, # link thickness 
                             link_direction = 'outgoing', # "outgoing" | "incoming" | "all"
                             link_color_strategy = "select", # source / target / gradient / attr / select
                             link_color_attr = "OriginalColor", # or other categorical link attribute
                             neighbors = 1, # degree of neighbors on hover/select
                             group_labels = False, # True = show group labels
                             node_labels = True, # True = show node labels                             
                             title = "Scatterplot", 
                             subtitle = "",
                             description_intro = "<p>This view shows.... Each node is a .... ",
                             snap_howto = default_snap_howto,                             
                             ):   

    if cluster == None:
        nodeClusterAttr = node_color
    else:
        nodeClusterAttr = cluster            

    snap = create_snapshot(
        name=title,
        subtitle=subtitle,
        summaryImg= "",
        description= description_intro + snap_howto, 
        layout_params={
            "plotType": "scatterplot",
            "xaxis": x,
            "yaxis": y,
            "settings": {
                # layout rendering
                "xAxShow": axes_show,
                "yAxShow": axes_show,
                "invertX": x_invert,
                "invertY": y_invert,
                "axis": "all", # "all", "none", "x", "y"  show dropdown selector
                "scatterAspect": aspect_ratio,  # higher than 0.5 spreads out the scatterplot horizontally
                # node color and images
                "nodeColorAttr": node_color,
                "nodeColorPaletteOrdinal": cat_palette,
                "nodeColorPaletteNumeric": num_palette,
                "nodeColorNumericScalerType": "RGB", # "HCL", "HCL Long", "LAB", "HSL"
                # node size
                "nodeSizeAttr":  node_size, 
                "nodeSizeScaleStrategy": "linear",  # "linear" or "log"
                "nodeSizeMin": node_size_scaling[0],
                "nodeSizeMax": node_size_scaling[1],
                "nodeSizeMultiplier": node_size_scaling[2],
                "bigOnTop": False,
                # image rendering
                "nodeImageShow": image_show,
                "nodeImageAttr": image_attr,
                # link rendering
                "drawEdges": links_show,
                "edgeCurvature": link_curve,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "OriginalSize", #"weight",  # size by
                "edgeSizeDefaultValue": link_weight, #0.2
                "edgeSizeMultiplier": 1, 
                "edgeColorStrat": link_color_strategy,  # gradient / source / target / gradient / attr / select
                "edgeColorAttr": link_color_attr, #"OriginalColor",
                "edgeColorPaletteNumeric":num_palette,
                "edgeColorPaletteOrdinal":cat_palette,
                "edgeColorDefaultValue": "rgb(145,145,145)",
                # neighbor rendering
                "nodeSelectionDegree": neighbors,
                "isShowSelectedNodeTab": True, # right profile selected neighbors
                "neighbourListHoverDegree": 0,  # degree to show when hover on node in list 

                # labels
                "drawGroupLabels": group_labels,
                "drawClustersCircle": clusterCircles,
                "drawLabels": node_labels, # show/hide node labels
           },
        },
    )
    return snap


def build_clustered_scatterplot_snapshot(
                               cluster_x,  # x axis cluster center attribute name
                               cluster_y, # y axis cluster center attribute name
                               x = 'OriginalX', # node position in cluster 
                               y = 'OriginalY', # node position in cluster 
                             axes_show = True,
                             x_invert = False,
                             y_invert = True,
                             aspect_ratio = 0.7, # 0.5 is square, >0.5 spreads out the scatterplot horizontally
                             node_color = "Cluster",
                             node_size = "ClusterCentrality",
                             cluster = None, # cluster by attr if diff from color by
                             clusterCircles = True, # draw circles around clusters                           
                             node_size_scaling = (5,15,.8), #min size, max size, multiplier
                             cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                             num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                             image_show = False, # show image in node
                             image_attr = "Photo",  # image attr name
                             links_show = False, # display links
                             link_curve = 0.6, # link curvature 0-1
                             link_weight = 0.8, # link thickness 
                             link_direction = 'outgoing', # "outgoing" | "incoming" | "all"
                             link_color_strategy = "gradient", # source / target / gradient / attr / select
                             link_color_attr = "OriginalColor", # or other categorical link attribute
                             neighbors = 1, # degree of neighbors on hover/select
                             group_labels = True, # True = show group labels
                             node_labels = True, # True = show node labels                             
                             title = "Clustered Scatterplot", 
                             subtitle = "",
                             description_intro = "<p>This view shows.... Each node is a .... ",
                             cluster_description = default_cluster_description,
                             snap_howto = default_snap_howto,                              
                             ):   

    if cluster == None:
        nodeClusterAttr = node_color
    else:
        nodeClusterAttr = cluster            

    snap = create_snapshot(
        name=title,
        subtitle=subtitle,
        summaryImg= "",
        description= description_intro + cluster_description + snap_howto, 
        layout_params={
            "plotType": "clustered-scatterplot",
            "clusterXAttr": cluster_x,
            "clusterYAttr": cluster_y,
            "nodeXAttr": x,
            "nodeYAttr": y,
            "settings": {
                # layout rendering
                "xAxShow": axes_show,
                "yAxShow": axes_show,
                "invertX": x_invert,
                "invertY": y_invert,
                "axis": "all", # "all", "none", "x", "y"  show dropdown selector
                "scatterAspect": aspect_ratio,  # higher than 0.5 spreads out the scatterplot horizontally
                # node color and images
                "nodeColorAttr": node_color,
                "nodeClusterAttr": nodeClusterAttr,
                "nodeColorPaletteOrdinal": cat_palette,
                "nodeColorPaletteNumeric": num_palette,
                "nodeColorNumericScalerType": "RGB", # "HCL", "HCL Long", "LAB", "HSL"
                # node size
                "nodeSizeAttr":  node_size, 
                "nodeSizeScaleStrategy": "linear",  # "linear" or "log"
                "nodeSizeMin": node_size_scaling[0],
                "nodeSizeMax": node_size_scaling[1],
                "nodeSizeMultiplier": node_size_scaling[2],
                "bigOnTop": False,
                # image rendering
                "nodeImageShow": image_show,
                "nodeImageAttr": image_attr,
                # link rendering
                "drawEdges": links_show,
                "edgeCurvature": link_curve,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "OriginalSize", #"weight",  # size by
                "edgeSizeDefaultValue": link_weight, #0.2
                "edgeSizeMultiplier": 1, 
                "edgeColorStrat": link_color_strategy,  # gradient / source / target / gradient / attr / select
                "edgeColorAttr": link_color_attr, #"OriginalColor",
                "edgeColorPaletteNumeric":num_palette,
                "edgeColorPaletteOrdinal":cat_palette,
                 # neighbor rendering
                "nodeSelectionDegree": neighbors,
                "isShowSelectedNodeTab": True, # right profile selected neighbors
                "neighbourListHoverDegree": 0,  # degree to show when hover on node in list 

                # labels
                "drawGroupLabels": group_labels,
                "drawClustersCircle": clusterCircles,
                "drawLabels": node_labels, # show/hide node labels
           },
        },
    )
    return snap


summaryImg="https://www.dl.dropboxusercontent.com/s/lfa3a2w44k0t2kw/Screen%20Shot%202021-03-31%20at%207.01.37%20AM.png?dl=0",
def build_geo_snapshot(
                    node_color = "Cluster",
                    node_size = "ClusterCentrality",                              
                    node_size_scaling = (5,15,.8), #min size, max size, multiplier
                    cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                    num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                    image_show = False, # show image in node
                    image_attr = "Photo",  # image attr name
                    links_show = False, # display links
                    link_curve = 0.6, # link curvature 0-1                         
                    link_weight = 0.8, # link thickness 
                    link_direction = 'outgoing', # "outgoing" | "incoming" | "all"
                    link_color_strategy = "gradient", # source / target / gradient / attr / select
                    link_color_attr = "OriginalColor", # or other categorical link attribute
                    neighbors = 1, # degree of neighbors on hover/select
                    title = "Geographic View", 
                    subtitle = "",
                    descr_intro = "This is a geographic view of each....  ",
                    snap_howto = default_geo_howto,
                    thumbnail = "https://www.dl.dropboxusercontent.com/s/0y9ccfw3ps91oy4/scatterplot.png?dl=0",  
                    node_labels = True                           
                    ):   


    # snapshot - scatterplot
    snap = create_snapshot(
        name= title,
        subtitle= subtitle,
        summaryImg="https://www.dl.dropboxusercontent.com/s/lfa3a2w44k0t2kw/Screen%20Shot%202021-03-31%20at%207.01.37%20AM.png?dl=0",
        description= descr_intro + snap_howto,
        layout_params={
            "plotType": "geo",
            "xaxis": "Latitude",
            "yaxis": "Longitude",
            "camera": {"normalizeCoords": True, "x": 0, "y": 43.9873417721519, "r": 1.5},
            "settings": {
                # layout rendering
                "isGeo": True,  # geographic layout
                # node color and images
                "nodeColorAttr": node_color,
                "nodeColorPaletteOrdinal": cat_palette,
                "nodeColorPaletteNumeric": num_palette,
                "nodeColorNumericScalerType": "RGB", # "HCL", "HCL Long", "LAB", "HSL"
                # node size
                "nodeSizeAttr":  node_size, 
                "nodeSizeScaleStrategy": "linear",  # "linear" or "log"
                "nodeSizeMin": node_size_scaling[0],
                "nodeSizeMax": node_size_scaling[1],
                "nodeSizeMultiplier": node_size_scaling[2],
                "bigOnTop": False,
                # image rendering
                "nodeImageShow": image_show,
                "nodeImageAttr": image_attr,
                # link rendering
                "drawEdges": links_show,
                "edgeCurvature": link_curve,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "OriginalSize", #"weight",  # size by
                "edgeSizeDefaultValue": link_weight, #0.2
                "edgeSizeMultiplier": 1, 
                "edgeColorStrat": link_color_strategy,  # gradient / source / target / gradient / attr / select
                "edgeColorAttr": link_color_attr, #"OriginalColor",
                "edgeColorPaletteNumeric":num_palette,
                "edgeColorPaletteOrdinal":cat_palette,
                 # neighbor rendering
                "nodeSelectionDegree": neighbors,
                "isShowSelectedNodeTab": True, # right profile selected neighbors
                "neighbourListHoverDegree": 0,  # degree to show when hover on node in list              
                # labels
                "drawGroupLabels": False,  # cluster labels
                "drawLabels": node_labels, # show/hide node labels
                # node right panel
                "nodeFocusShow": True,
            },
        },
    )
    return snap
    


## default project description templates
default_mobile_caveat = "<p>Note: \
                <i>This visualization is designed for desktop viewing and has not been optimized for mobile. \
                It works best in Chrome or Safari.</i></p>"

default_project_how_to = "<p>HOW TO NAVIGATE THIS MAP:</p>\
                            <ul>\
                            <li>Click on any point to to see more details about it. Click the white space to deselect.\
                                </li>\
                            <li>Use the left panel tags and charts to select points by any combination of attributes. \
                                Selecting multiple tags within in attribute will highlight points with <i>any</i> of them (i.e. with either tag a <i>or</i> tag b). \
                                Selecting multiple tags across attributes will highlight points with <i>all</i> of them (i.e. with both tag a <i>and</i> tag b). \
                                </li>\
                            <li>If you click <i>Summarize Selection</i>, the left <b>Summary</b> panel will summarize the tags and charts for the selected group.\
                                Any subsequent searching or selecting tags will then act only on the subsetted points. \
                                </li>\
                            <li>Click <i>Clear All</i> to reset/clear all selections. (or click <i>Undo</i> to undo the selection step.)\
                                </li>\
                            <li>Use the <b>List</b> tab to see a sortable list of any points selected. \
                                You can can browse the details of each point by selecting them from the list.\
                                </li>\
                            <li>The <b>Legend</b> tab shows information about the current view including: \
                                the coloring and sizing of the points, as well as a brief description. \
                                </li>\
                            <li>If there are multiple snapshots - you can select other views from the pink <b>snapshot title</b>.\
                                </li>\
                            </ul>"


def build_player_settings(
                    start_page = "filter",  # filter // snapshots // list // legend 
                    show_start_info = True, # display main info panel on launch
                    project_title = "Landscape Map",
                    project_description = "<p>Project summary description goes here... </p><p>can use <i>HTML</i> to format</p>", 
                    mobile_caveat = default_mobile_caveat,
                    how_to = default_project_how_to,
                    displayTooltip = False                   
                    ):
        playerSettings={
            "startPage": start_page,
            "showStartInfo": show_start_info,
            "headerTitle": project_title,
            "modalTitle": project_title,
            "headerImageUrl": "",
            "displayTooltipCard": displayTooltip,
            "modalSubtitle": project_description + mobile_caveat,
            "modalDescription": how_to
            }
        return playerSettings
    
    

def build_player(ndf, ldf, # nodes and links dataframes
                 playerpath, # pathlib object - directory to store player data
                 playerSettings, # player-level settings
                 snapshots_list, # list of snapshots
                 x = 'x', # layout attribute for clustered 'original layout' 
                 y = 'y', # layout attribute for clustered 'original layout'
                 ### node attribute style settings ###
                 labelCol='label', 
                 hide = [],  # list custom attributes to hide from filters
                 hideProfile =[], # list custom attributes to hide from right profile
                 hideSearch = [], # list custom attribs to hide from search
                 keepSearch = None, # simpler list of attribs to keep in search (override 'hideSearch')
                 liststring = [], # string attribs to force as liststring
                 tag_cloud = [],  # custom string attribs to render as tag-cloud
                 tag_cloud_3 = [],  # list of custom attrubtes to render as tag-cloud (3 tags per row)
                 tag_cloud_2 = [],  # list of custom attrubtes to render as tag-cloud (2 tags per row)
                 wide_tags = []  , # custom string attribs to render as wide tag-cloud
                 horizontal_bars = [], # custom string attribs to render as horizontal bar chart
                 text_str = [],   # custom string attribs to render as long text in profile
                 email_str = [], # custom string attribs to render as email link  in profile
                 years = [], # format as year not integer
                 low_priority = [], # attributes to move to 'additional attributes' 
                 axis_select = None, # custom list of numeric attributes to show in scatterplot axis dropdown (if none all visible numeric will show)
                 ### launch / upload settings
                 launch_local=True, 
                 upload_s3=False,
                 player_s3_bucket = "my-s3-bucket-name"
                 ):
    
    # Write openMappr files
    write_openmappr_files(ndf, ldf, 
                    playerpath, 
                    x, y, # network layout coordinates
                    labelCol='label', 
                    hide = hide,  # list custom attributes to hide from filters
                    hideProfile =hideProfile, # list custom attributes to hide from right profile
                    hideSearch = hideSearch, # list custom attribs to hide from search
                    keepSearch = keepSearch, # simpler list of attribs to keep in search (override 'hideSearch')
                    liststring = liststring, # string attribs to force as liststring
                    tag_cloud = tag_cloud,  # custom string attribs to render as tag-cloud
                    tag_cloud_3 = tag_cloud_3,  # list of custom attrubtes to render as tag-cloud (3 tags per row)
                    tag_cloud_2 = tag_cloud_2,  # list of custom attrubtes to render as tag-cloud (2 tags per row)
                    wide_tags = wide_tags  , # custom string attribs to render as wide tag-cloud
                    horizontal_bars = horizontal_bars, # custom string attribs to render as horizontal bar chart
                    text_str = text_str,   # custom string attribs to render as long text in profile
                    email_str = email_str, # custom string attribs to render as email link  in profile
                    years = years, # format as year not integer
                    low_priority = low_priority, # attributes to move to 'additional attributes' 
                    axis_select = axis_select, # custom list of numeric attributes to show in scatterplot axis dropdown (if none all visible numeric will show)
                    )
    playerpath = pl.Path(playerpath) # convert from string to path object
    # configure the files and folders  
    inDataPath = playerpath / "data_in"
    nodesFile = inDataPath / "nodes.csv"
    linksFile = inDataPath / "links.csv"
    nodeAttrsFile = inDataPath / "node_attrs.csv"
    outFolder = playerpath / "data_out"
    
    # configure the mapping for the read parameters
    # maps are in the form of {"required param name": "name of column in datasheet"}
    # the required param names are fixed and should not be changed.
    node_attr_map = {"OriginalLabel": "label", "OriginalX": x, "OriginalY": y}
    link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}
    
    # create map
    create_map(
        nodesFile,
        linksFile,
        nodeAttrsFile,
        node_attr_map,
        link_attr_map,
        snapshots=snapshots_list,
        playerSettings= playerSettings,
        outFolder=outFolder,
    )
    
    if upload_s3:
        launch_upload_player.upload_to_s3(str(outFolder), player_s3_bucket)

    if launch_local:
        launch_upload_player.run_local(str(outFolder), PORT=8080)


############################

