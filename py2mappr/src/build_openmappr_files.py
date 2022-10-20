#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 08:14:03 2021

@author: ericberlow
"""

import sys
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
import pathlib as pl
#from pandas.api.types import is_numeric_dtype


def write_network_to_excel (ndf, ldf, outname):
    writer = pd.ExcelWriter(outname,
                          engine='xlsxwriter', 
                          options={'strings_to_urls': False})
    ndf.to_excel(writer,'Nodes', index=False, encoding = 'utf-8-sig')
    ldf.to_excel(writer,'Links', index=False, encoding = 'utf-8-sig')
    writer.save()  

def get_default_column_types_openmappr(ndf):
    typeDict = {} # dictionary of column name: (attrType, renderType, searchable) 
    countThresh = 0.02*len(ndf) # number of records to evaluate type (e.g. 2% of total)
    for col in ndf.columns.tolist():
        if is_string_dtype(ndf[col]):
            typeDict[col] = ("string", "wide-tag-cloud", "TRUE")  # fill all strings, then below modify specific ones
        if sum(ndf[col].apply(lambda x: len(str(x)) > 200)) > countThresh: # long text
            typeDict[col] = ("string", "text", "TRUE")
        if sum(ndf[col].apply(lambda x:"http" in str(x))) > countThresh: # urls
            typeDict[col] = ("url", "default", "FALSE")
        if sum(ndf[col].apply(lambda x:"|" in str(x))) > countThresh:  # tags
            typeDict[col] = ("liststring", "tag-cloud", "TRUE")
        if sum(ndf[col].apply(lambda x:"png" in str(x))) > countThresh: # images
            typeDict[col] = ("picture", "default", "FALSE") 
        if sum(ndf[col].apply(lambda x:"jpg" in str(x))) > countThresh: # images
            typeDict[col] = ("picture", "default", "FALSE")                 
        if ndf[col].dtype == 'float64':           # float
            typeDict[col] = ("float", "histogram", "FALSE")
        if ndf[col].dtype == 'int64':             # integer
            typeDict[col] = ("integer", "histogram", "FALSE")
        if ndf[col].dtype == np.int64: #'Int64':             # integer
            typeDict[col] = ("integer", "histogram", "FALSE")
        if ndf[col].dtype == 'bool':             # integer
            typeDict[col] = ("string", "tag-cloud", "FALSE")    
        #TODO:  need to add timestamp, year, video
    return typeDict
        
    
def write_openmappr_files(ndf, ldf, playerpath, 
                    x, y, # attr for clustered layout coordinates
                    labelCol='Name', 
                    hide = [],  # list custom attributes to hide from filters
                    hideProfile =[], # list custom attributes to hide from right profile
                    hideSearch = [], # list custom attributes to hide from search
                    keepSearch = None, # list to keep for global search (over-ride 'hideSearch')
                    liststring = [], # list attributes to treat as liststring 
                    tag_cloud = [],  # list of custom attrubtes to render as tag-cloud (4 tags per row)
                    tag_cloud_3 = [],  # list of custom attrubtes to render as tag-cloud (3 tags per row)
                    tag_cloud_2 = [],  # list of custom attrubtes to render as tag-cloud (2 tags per row)
                    wide_tags = [], # list of custom attribs to render wide tag-cloud (1 tag per row)
                    horizontal_bars = [], # list of string attrs to render as horizontal bar chart
                    text_str = [],  # list of custom attribs to render as long text in profile
                    email_str = [], # list of custom attribs to render as email link
                    showSearch = [], # list of custom attribs to show in search
                    years = [], # list of attributes to format as year not integer
                    low_priority = [], # list of attributes to move to 'additional attributes' in left panel
                    axis_select = None, # custom list of numeric attributes to show in scatterplot axis dropdown (if none all visible numeric will show)
                    color_select = [], # attributes for color_by selection dropdown - must include colorby attr (or show none)
                    size_select = [], # attributes for size_by selection dropdown that are not already hidden (default here is show none)
                    ):  
    '''
    Write files for py2mappr: 
        nodes.csv
        links.csv
        node_attrs_template.csv (template for specifying attribute rendering settings in openmappr)
    '''
    print('\nWriting openMappr files')
    ## generate csv's for py2mappr

    # prepare and write nodes.csv
    ndf['label'] = ndf[labelCol] 
    ndf['OriginalLabel'] = ndf['label']
    ndf['OriginalX'] = ndf[x] # clustered layout coordinates
    ndf['OriginalY'] = ndf[x] # clustered layout coordinates
    ndf['OriginalSize'] = 10
    
    playerpath = pl.Path(playerpath)
    playerpath.mkdir(parents=True, exist_ok=True) # create directory  for results if it doesn't exist
    datapath = playerpath/"data_in"
    datapath.mkdir(exist_ok=True) # create directory  for results if it doesn't exist
    ndf.to_csv(datapath/"nodes.csv", index=False)

    # prepare and write links.csv
    ldf['isDirectional'] = True
    ldf.to_csv(datapath/"links.csv", index=False)

    # prepare and write note attribute settings template (node_attrs_template.csv)
        
       # create node attribute metadata template:
    node_attr_df = ndf.dtypes.reset_index()
    node_attr_df.columns = ['id', 'dtype']


        # map automatic default attrType, renderType, searchable based on column types
        # get dictionary of default mapping of column to to attrType, renderType, searchable
    typeDict =  get_default_column_types_openmappr(ndf)  
    node_attr_df['attrType'] = node_attr_df['id'].apply(lambda x: typeDict[x][0])
    node_attr_df['renderType'] = node_attr_df['id'].apply(lambda x: typeDict[x][1])
    node_attr_df['searchable'] = node_attr_df['id'].apply(lambda x: typeDict[x][2])

        # custom string renderType settings for string attributes
    node_attr_df['attrType'] = node_attr_df.apply(lambda x: 'liststring' if str(x['id']) in liststring
                                                               else 'string' if str(x['id']) in (text_str + email_str + horizontal_bars)
                                                               else 'year' if str(x['id']) in (years)
                                                               else x['attrType'], axis=1)

    node_attr_df['renderType'] = node_attr_df.apply(lambda x: 'wide-tag-cloud' if str(x['id']) in wide_tags  # 1 tag per row
                                                               else 'tag-cloud_2' if str(x['id']) in tag_cloud_2 # 2 tags per row
                                                               else 'tag-cloud_3' if str(x['id']) in tag_cloud_3 # 3 tags per row                                                                                                                         else 'tag-cloud' if str(x['id']) in tag_cloud
                                                               else 'tag-cloud' if str(x['id']) in tag_cloud # 4 tags per row
                                                               else 'horizontal-bars' if str(x['id']) in horizontal_bars
                                                               else 'text' if str(x['id']) in text_str
                                                               else 'email' if str(x['id']) in email_str
                                                               else x['renderType'], axis=1)
       # additional attributes to hide from filters
    if hide != None:
        hide = list(set(['label', 'OriginalLabel', 'OriginalSize', 'OriginalY', 'OriginalX', 'id'] + hide))
    else:
         hide = list(set(['label', 'OriginalLabel', 'OriginalSize', 'OriginalY', 'OriginalX', 'id']))
         
    node_attr_df['visible'] = node_attr_df['id'].apply(lambda x: 'FALSE' if str(x) in hide else 'TRUE')
 
       # additional attributes to hide from profile
    hideProfile = list(set(hide + hideProfile))
    node_attr_df['visibleInProfile'] = node_attr_df['id'].apply(lambda x: 'FALSE' if str(x) in hideProfile else 'TRUE')
    
       # additional attributes to hide from search
    hideSearch = list(set(hide + hideSearch))
    node_attr_df['searchable'] = node_attr_df.apply(lambda x: 'FALSE' if str(x['id']) in hideSearch else x['searchable'], axis=1)
    node_attr_df['searchable'] = node_attr_df.apply(lambda x: 'TRUE' if str(x['id']) in text_str else x['searchable'], axis=1)
    
    if keepSearch:
        node_attr_df['searchable'] = node_attr_df.apply(lambda x: 'TRUE' if str(x['id']) in keepSearch else 'FALSE', axis=1)
        
        # attributes to show in scatterplot axis selection menu
    if axis_select == None: # default show all numeric attributes in the axis dropdowns 
        node_attr_df['axis'] = node_attr_df.apply(lambda x: 'all' if str(x['renderType']) == 'histogram' else 'none', axis=1)
    else: # otherwise only show selected attributes in axis selector dropdown menus
        node_attr_df['axis'] = node_attr_df.apply(lambda x: 'all' if str(x['id']) in axis_select else 'none', axis=1)

    # attributes to show in color_by dropdown menu
    node_attr_df['colorSelectable'] = node_attr_df.apply(lambda x: True if str(x['id']) in color_select else False, axis=1) 

    # attributes to show in size_by dropdown menu
    node_attr_df['sizeSelectable'] = node_attr_df.apply(lambda x: True if str(x['id']) in size_select else False, axis=1) 
    
       # add default alias title and node metadata description columns
    node_attr_df['title'] = node_attr_df['id']
    defaultcols = ['descr', 'maxLabel', 'minLabel', 'overlayAnchor']
    for col in defaultcols: 
        node_attr_df[col] = ''   

       # add attribute priority for display (low priority moves to 'additional attributes')
    node_attr_df['priority'] = node_attr_df.apply(lambda x: 'low' if str(x['id']) in low_priority 
                                                               else 'high', axis=1)

       # re-order final columns and write template file
    meta_cols = ['id', 'visible', 'visibleInProfile', 'searchable', 'title', 'attrType', 'renderType', 
    'descr', 'maxLabel', 'minLabel', 'overlayAnchor', 'priority', 'axis', 'colorSelectable', 'sizeSelectable']
    node_attr_df = node_attr_df[meta_cols]
    node_attr_df.to_csv(datapath/"node_attrs.csv", index=False)


#####################################################################################


        
if __name__ == '__main__':
    # test script
    nw_name = "name_of_network_file.xlsx"
    df = pd.read_excel('test_data.xlsx', engine='openpyxl')
 
    ndf = pd.read_excel(nw_name, engine='openpyxl', sheet_name = 'Nodes') # projects funding
    ldf = pd.read_excel(nw_name, engine='openpyxl', sheet_name = 'Links') # projects funding
    
    # write_openmappr_files(ndf, ldf, ref.openMappr_path)
    
    