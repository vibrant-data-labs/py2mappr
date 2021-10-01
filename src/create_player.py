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
from build_openmappr_files import write_openmappr_files # from py2mappr - create openmappr files
from map_utils import create_map, create_snapshot # from py2mappr
import pathlib as pl
import launch_upload_player # from py2mappr


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
                {"col": "#BDBFC1"},# min 
                {"col": "#BC2020"} # max 
                ]


def build_clustered_snapshot(node_color = 'Cluster',
                             node_size = "ClusterCentrality",                              
                             node_size_scaling = (5,15,.8), #min size, max size, multiplier
                             cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                             num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                             image_show = False, # show image in node
                             image_attr = "Photo",  # image attr name
                             links_show = True, # display links
                             link_direction = 'outgoing', # "outgoing", "incoming", "all"
                             neighbors = 1, # number of neighbors on hover/select
                             title = "Thematic Clusters",
                             subtitle = "Nodes clustered into themes",
                             description_intro = "<p>This is a map of ...... Each node is a .... ",
                             thumbnail = "https://www.dl.dropboxusercontent.com/s/1jdc4hvp5zw6as9/Screen%20Shot%202021-03-31%20at%206.59.23%20AM.png?dl=0",                             
                             ):   
    default_description = "<p><span>\
                Colored clusters are groups of nodes that 'huddle' together into themes based on similarity in their keywords.\
                Each theme is auto-labeled by the three most commonly shared keywords in the cluster. \
                While the clusters reflect combinations of keywords that tend to go together, any one keyword can occur in multiple themes.\
                Use the left panel to browse and select nodes by one or more keywords, tags, or other attributes. \
                If you click <i>Summarize</i>, the left <b>Summary</b> panel will summarize the attributes for the selected group.\
                </span></p>"
                
    snap = create_snapshot(
        name=title,
        subtitle=subtitle,
        summaryImg= thumbnail,
        description= description_intro + default_description, 
        layout_params={
            "plotType": "original",  # "scatterplot",
            "settings": {
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
                "edgeCurvature": .6,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "weight",  # size by
                "edgeSizeMultiplier": 0.8,
                "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
                "edgeColorAttr": "OriginalColor",
                # neighbor rendering
                "nodeSelectionDegree": neighbors,
                # labels
                "drawGroupLabels": True,
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
                             node_size_scaling = (5,15,.8), #min size, max size, multiplier
                             cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                             num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                             image_show = False, # show image in node
                             image_attr = "Photo",  # image attr name
                             links_show = False, # display links
                             link_direction = 'outgoing', # "outgoing" | "incoming" | "all"
                             neighbors = 1, # degree of neighbors on hover/select
                             title = "Scatterplot", 
                             subtitle = "",
                             description_intro = "<p>This view shows.... Each node is a .... ",
                             thumbnail = "https://www.dl.dropboxusercontent.com/s/0y9ccfw3ps91oy4/scatterplot.png?dl=0",                             
                             ):   

    default_description = "<p><span>\
                Nodes are sorted horizontally by " + x + " and vertically by " + y + ".</span></p>\
                <p><span>\
                Use the left panel to browse and select nodes by one or more keywords, tags, or other attributes. \
                If you click <i>Summarize</i>, the left <b>Summary</b> panel will summarize the attributes for the selected group.\
                </span></p>"

    snap = create_snapshot(
        name=title,
        subtitle=subtitle,
        summaryImg= thumbnail,
        description= description_intro + default_description, 
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
                "edgeCurvature": 0.6,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "weight",  # size by
                "edgeSizeMultiplier": 0.8,
                "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
                "edgeColorAttr": "OriginalColor",
                # neighbor rendering
                "nodeSelectionDegree": neighbors,
                # labels
                "drawGroupLabels": False,
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
                    link_direction = 'outgoing', # "outgoing" | "incoming" | "all"
                    neighbors = 1, # degree of neighbors on hover/select
                    title = "Geographic View", 
                    subtitle = "",
                    descr_intro = "This is a geographic view of each....  ",
                    thumbnail = "https://www.dl.dropboxusercontent.com/s/0y9ccfw3ps91oy4/scatterplot.png?dl=0",                             
                    ):   

    default_description = "<p><span>\
                You can select a group of points on the map by holding 'shift' while you drag the cursor. \
                If you click <i>Summarize Selectin</i>, the left <b>Summary</b> panel will summarize the attributes for the selected group.\
                In the <b>Summary</b> panel, if you hover over a keyword or tag you can see it's geographic dispersion. \
                </span></p>"

    # snapshot - scatterplot
    snap = create_snapshot(
        name="Geographic Map",
        subtitle="Company and Organization Locationw",
        summaryImg="https://www.dl.dropboxusercontent.com/s/lfa3a2w44k0t2kw/Screen%20Shot%202021-03-31%20at%207.01.37%20AM.png?dl=0",
        description= descr_intro + default_description,
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
                "edgeCurvature": 0.6,
                "edgeDirectionalRender": link_direction,  # "outgoing", "incoming", "all"
                "edgeSizeStrat": "fixed",  #  "attr" // "fixed"
                "edgeSizeAttr": "weight",  # size by
                "edgeSizeMultiplier": 0.8,
                "edgeColorStrat": "gradient",  # source / target / gradient / attr / select
                "edgeColorAttr": "OriginalColor",
                # neighbor rendering
                "nodeSelectionDegree": neighbors,
                # labels
                "drawGroupLabels": False,  # cluster labels
                # node right panel
                "nodeFocusShow": True,
            },
        },
    )
    return snap
    

def build_player_settings(
                    start_page = "filter",  # filter // snapshots // list // legend 
                    project_title = "Landscape Map",
                    project_description = "<p>PROJECT DESCRIPTION...</p><p>can use <i>HTML</i> to format</p>"                    
                    ):
        
        playerSettings={
            "startPage": start_page,
            "headerTitle": project_title,
            "modalTitle": project_title,
            "headerImageUrl": "",
            "modalSubtitle": project_description + "<p>><b>Note:</b> \
                                                    <i>This visualization is designed for desktop viewing and has not been optimized for mobile. \
                                                    It works best in Chrome or Safari.</i></p>",
            "modalDescription": "<p>HOW TO NAVIGATE THIS MAP:</p>\
                            <ul>\
                            <li>Click on any data point to to see more details about it.\
                                </li>\
                            <li>Use the left panel tags and charts to select points by any combination of attributes. \
                                Selecting multiple tags within in attribute will highlight points with <i>any</i> of them (i.e. with either <i>x <b>OR</b> y</i>). \
                                Selecting multiple tags across attributes will highlight points with <i>all</i> of them (i.e. with both <i>x <b>AND</b> y</i>). \
                                </li>\
                            <li>If you click <i>Summarize Selectin</i>, the left <b>Summary</b> panel will summarize the attributes for the selected group.\
                                Any subsequent searching or selecting tags will then act only on the subsetted points. \
                                </li>\
                            <li>Click <i>Clear Selection</i> to reset/clear all selections.\
                                </li>\
                            <li>Use the <b>List</b> tab to see a sortable and searchable list of any points selected. \
                                You can can browse the details of each point by selecting them from the list.\
                                </li>\
                            <li>The <b>Legend</b> tab shows information about the current view including: \
                                the coloring and sizing of the points, as well as a brief description. \
                                </li>\
                            <li>If there are multiple snapshots - you can select other views from the pink <b>snapshot title</b> in the lower left.\
                                </li>\
                            <li>Click the <i><b>'i'</b></i> button to see more general information about this map.\
                                </li>\
                            </ul>"
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
                 hide_add = [],  # list custom attributes to hide from filters
                 hideProfile_add =[], # list custom attributes to hide from right profile
                 hideSearch_add = [], # list custom attribs to hide from search
                 liststring_add = [], # string attribs to force as liststring
                 tags_add = [],  # custom string attribs to render as tag-cloud
                 wide_tags_add = []  , # custom string attribs to render as wide tag-cloud
                 text_str_add = [],   # custom string attribs to render as long text in profile
                 email_str_add = [], # custom string attribs to render as email link  in profile
                 years_add = [], # format as year not integer
                 low_priority = [], # attributes to move to 'additional attributes' 
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
                    hide_add = hide_add,  # list custom attributes to hide from filters
                    hideProfile_add =hideProfile_add, # list custom attributes to hide from right profile
                    hideSearch_add = hideSearch_add, # list custom attribs to hide from search
                    liststring_add = liststring_add, # string attribs to force as liststring
                    tags_add = tags_add,  # custom string attribs to render as tag-cloud
                    wide_tags_add = wide_tags_add  , # custom string attribs to render as wide tag-cloud
                    text_str_add = text_str_add,   # custom string attribs to render as long text in profile
                    email_str_add = email_str_add, # custom string attribs to render as email link  in profile
                    years_add = years_add, # format as year not integer
                    low_priority = low_priority # attributes to move to 'additional attributes' 
                    )
    
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
        launch_upload_player.run_local(str(outFolder), PORT=5000)


############################
if __name__ == '__main__':
    # data paths
    wd = pl.Path.cwd()  # current working directory
    playerpath = wd/"player"
    nw_name = wd/"results"/"network.xlsx" 
    player_s3_bucket = "my-s3-bucket"

    #  read nodes file
    ndf = pd.read_excel(nw_name, engine='openpyxl', sheet_name='Nodes') # recipients with metadata including tags
    ldf = pd.read_excel(nw_name, engine='openpyxl', sheet_name='Links') # recipients with metadata including tags
    
    def build_climate_player(ndf,ldf,
                         playerpath = playerpath,
                         nw_name = nw_name,
                         player_bucket = player_s3_bucket,
                         launch_local=True,
                         upload_s3=False):   

        # clustered snapshot
        snap_clustered = build_clustered_snapshot(
                                 node_color = 'Climate Theme',
                                 node_size = "ClusterCentrality",                              
                                 node_size_scaling = (5,15,.6), #min size, max size, multiplier
                                 image_show = False, # show image in node
                                 image_attr = "Photo",  # image attr name
                                 links_show = False, # display links
                                 neighbors = 0, # number of neighbors on hover/select
                                 title = "Thematic Clusters",
                                 subtitle = "Nodes clustered into themes",
                                 description_intro = "This is a landscape map of ...",
                                 )
        # scatterplot snapshot
        snap_scatter = build_scatterplot_snapshot(
                                  "Stage",  # x axis attribute name
                                  "log Total Funding", # y axis attribute name
                                 axes_show = True,
                                 axes_invert = False,
                                 aspect_ratio = 0.7, # 0.5 is square, >0.5 spreads out the scatterplot horizontally
                                 node_color = "Climate Theme",
                                 node_size = "Relative Funding",                              
                                 node_size_scaling = (5,15,.8), #min size, max size, multiplier
                                 cat_palette = cat_palette, # List of dictionaries: [{"col": HEXCODE}]
                                 num_palette = num_palette, # List of dictionaries: [{"col": HEXCODE}]
                                 image_show = False, # show image in node
                                 links_show = False, # display links
                                 title = "Scatterplot", 
                                 subtitle = "",
                                 description_intro = "<p>This view shows.... Each node is a .... ",
                                 thumbnail = "https://www.dl.dropboxusercontent.com/s/0y9ccfw3ps91oy4/scatterplot.png?dl=0",                                    
                                )
        
        # geo snapshot    
        snap_geo = build_geo_snapshot(
                        node_color = 'Climate Theme',
                        node_size = "ClusterCentrality",                              
                        node_size_scaling = (5,15,.8), #min size, max size, multiplier
                        image_show = False, # show image in node
                        links_show = False, # display links
                        neighbors = 0, # degree of neighbors on hover/select
                        title = "Geographic View", 
                        subtitle = "",
                        descr_intro = "This is a geographic view of the office locations of each company and organization",        
                        )
        

        # geo snapshot    
        snapshots_list = [snap_clustered, snap_scatter, snap_geo]
        # add project title and description
        player_settings = build_player_settings(
                           #project_title = "Climate Solutions Landscape",
                           #project_description = "PROJECT DESCRIPTION"
                           )


        build_player(ndf, ldf, # nodes and links dataframes
                     playerpath, # pathlib object - directory to store player data
                     player_settings, # player-level settings
                     snapshots_list, # list of snapshots
                     x = 'x', # layout attribute for clustered 'original layout' 
                     y = 'y', # layout attribute for clustered 'original layout'
                     ### node attribute style settings ###
                     labelCol='label', 
                     hide_add = ref.hide_add,  # list custom attributes to hide from filters
                     hideProfile_add = ref.hideProfile_add, # list custom attributes to hide from right profile
                     hideSearch_add = ref.hideSearch_add, # list custom attribs to hide from search
                     liststring_add = ref.liststring_add, # string attribs to force as liststring
                     tags_add = ref.tags_add,  # custom string attribs to render as tag-cloud
                     wide_tags_add = ref.wide_tags_add  , # custom string attribs to render as wide tag-cloud
                     text_str_add = ref.text_str_add,   # custom string attribs to render as long text in profile
                     email_str_add = ref.email_str_add, # custom string attribs to render as email link  in profile
                     years_add = ref.years_add, # format as year not integer
                     low_priority = ref.low_priority, # attributes to move to 'additional attributes' 
                     ### launch / upload settings
                     launch_local=True, 
                     upload_s3=False,
                     player_s3_bucket = "my-s3-bucket-name"
                     )


    ########################    
    ## call to run and build snapshots and player
    build_climate_player(ndf,ldf,
                         playerpath = playerpath,
                         nw_name = nw_name,
                         player_bucket = player_s3_bucket,
                         launch_local=True,
                         upload_s3=False)


