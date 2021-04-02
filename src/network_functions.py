#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 08:14:03 2021
@author: ericberlow

network analysis functions to 
* build network from tags
* decorate nodes with network metrics 
* decroate nodes with tsnw or spring layout coordinates
* plot pdf of network
* convert network nodes and links file  into openmappr format
* create template of node attribute settigns for openmappr 

"""

import sys
import pandas as pd
sys.path.append("../../Tag2Network/tag2network/")  # add Tag2Network directory
import Network.BuildNetwork as bn
import Network.DrawNetwork as dn
from Network.BuildNetwork import addLouvainClusters
from Network.ClusteringProperties import basicClusteringProperties
import networkx as nx
from pandas.api.types import is_string_dtype
import pathlib as pl  # path library
#from pandas.api.types import is_numeric_dtype


def buildNetworkX(linksdf, id1='Source', id2='Target', directed=False):
    # build networkX graph object from links dataframe with 'Source' and 'Target' ids
    # generate list of links from dataframe
    linkdata = [(getattr(link, id1), getattr(link, id2)) for link in linksdf.itertuples()]
    g = nx.DiGraph() if directed else nx.Graph()
    g.add_edges_from(linkdata)
    return g


def tsne_layout(ndf, ldf):   
    ## add tsne-layout coordinates and draw
    # dependency: https://github.com/foodwebster/Tag2Network
    bn.add_layout(ndf, linksdf=ldf, nw=None)
    ndf.rename(columns={"x": "x_tsne", "y": "y_tsne"}, inplace=True)
    return ndf
   
def spring_layout(ndf, ldf, iterations=1000):
    print("Running spring Layout")
    nw = bn.buildNetworkX(ldf)
    # remove isolated nodes and clusters for layout
    giant_component_nodes  = max(nx.connected_components(nw), key = len)
    giant_component = nw.subgraph(giant_component_nodes)
    layout = nx.spring_layout(giant_component, k=0.2, weight='weight', iterations=iterations) # k is spacing 0-1, default 0.1
    x ={n:layout[n][0] for n in giant_component.nodes()}
    y= {n:layout[n][1] for n in giant_component.nodes()}
    ndf['x_spring'] = ndf['id'].map(x)
    ndf['y_spring'] = ndf['id'].map(y)
    # place all disconnected nodes at 0,0
    ndf['x_spring'].fillna(0)
    ndf['y_spring'].fillna(0)
    return ndf

def force_directed(ndf, ldf, iterations=1000):
    ## add force-directed layout coordinate
    bn.add_force_directed_layout(ndf, linksdf=ldf, nw=None, iterations=iterations)
    return ndf

def plot_network(ndf, edf, plot_name, x='x_tsne', y='y_tsne', colorBy='Cluster', sizeBy='ClusterCentrality', sizeScale=100):    
    # draw network colored by creative style and save image
    # ndf = nodes dataframe
    # ldf = links dataframe 
    # plotname = name of file to save image (pdf)
    # dependency: https://github.com/foodwebster/Tag2Network
    nw = bn.buildNetworkX(edf) # build networkX graph object
    node_sizes = ndf.loc[:,sizeBy]*sizeScale
    node_sizes_array = node_sizes.values # convert sizeBy col to array for sizing
    dn.draw_network_categorical(nw, ndf, node_attr=colorBy, plotfile=plot_name, x=x, y=y, node_size=node_sizes_array)

def min_max_normalize_column (df, col):
    return (df[col] - df[col].min()) / (df[col].max() - df[col].min())  


def keystone_index(df, reach='2_Degree_Reach', leverage='2_Degree_Leverage'):
    '''
    Description: scale leverage and reach from 0 to 1, then multiply
    Returns: series
    '''
    reach_normalized = min_max_normalize_column(df,reach)
    leverage_normalized = min_max_normalize_column(df, leverage)
    keystone = reach_normalized * leverage_normalized
    return keystone # series


def outoutdegree(nw):
    # compute number of second degree outgoing neighbors
    outout = {n:set() for n in nw.nodes()}
    for n in nw.nodes():
        for n2 in nw.successors(n):
            outout[n].update(nw.successors(n2))
    return {n:len(outout[n]) for n in nw.nodes()}

def inindegree(nw):
    # compute number of second degree incoming neighbors
    inin = {n:set() for n in nw.nodes()}
    for n in nw.nodes():
        for n2 in nw.predecessors(n):
            inin[n].update(nw.predecessors(n2))
    return {n:len(inin[n]) for n in nw.nodes()}

def add_cluster_metrics(nodesdf, nw, groupVars):
   # add bridging, cluster centrality etc. for one or more grouping variables
   # dependency: tag2network repository https://github.com/foodwebster/Tag2Network 
   for groupVar in groupVars:
       if len(nx.get_node_attributes(nw, groupVar)) == 0:
           vals = {k: v for k, v in dict(zip(nodesdf['id'], nodesdf[groupVar])).items() if k in nw}
           nx.set_node_attributes(nw, vals, groupVar)
       grpprop = basicClusteringProperties(nw, groupVar)
       for prop, vals in grpprop.items():
           nodesdf[prop] = nodesdf['id'].map(vals)


def write_network_to_excel (ndf, ldf, outname):
    writer = pd.ExcelWriter(outname)
    ndf.to_excel(writer,'Nodes', index=False)
    ldf.to_excel(writer,'Links', index=False)
    writer.save()  

def get_default_column_types_openmappr(ndf):
    typeDict = {} # dictionary of column name: (attrType, renderType, searchable) 
    countThresh = 0.02*len(ndf) # number of records to evaluate type (e.g. 2% of total)
    for col in ndf.columns.tolist():
        if is_string_dtype(ndf[col]):
            typeDict[col] = ("string", "wide-tag-cloud", "TRUE")  # fill all strings, then below modify specific ones
        if sum(ndf[col].apply(lambda x: len(str(x)) > 100)) > countThresh: # long text
            typeDict[col] = ("string", "text", "TRUE")
        if sum(ndf[col].apply(lambda x:"http" in str(x))) > countThresh: # urls
            typeDict[col] = ("url", "default", "FALSE")
        if sum(ndf[col].apply(lambda x:"|" in str(x))) > countThresh:  # tags
            typeDict[col] = ("liststring", "tag-cloud", "TRUE")
        if sum(ndf[col].apply(lambda x:"png" in str(x))) > countThresh: # images
            typeDict[col] = ("picture", "default", "FALSE")                
        if ndf[col].dtype == 'float64':           # float
            typeDict[col] = ("float", "histogram", "FALSE")
        if ndf[col].dtype == 'int64':             # integer
            typeDict[col] = ("integer", "histogram", "FALSE")
        if ndf[col].dtype == 'bool':             # integer
            typeDict[col] = ("string", "tag-cloud", "FALSE")
        
        #TODO:  need to add timestamp, year, video
    return typeDict
        
    
def write_openmappr_files(ndf, ldf, datapath, labelCol='Name', 
                    hide_add = [],  # list custom attributes to hide from filters
                    hideProfile_add =[], # list custom attributes to hide from right profile
                    hideSearch_add = [], # list custom attributes to hide from search
                    liststring_add = [], # list attributes to treat as liststring 
                    tags_add = [],  # list of custom attrubtes to render as tag-cloud
                    wide_tags_add = [], # list of custom attribs to render wide tag-cloud
                    text_str_add = [],  # list of custom attribs to render as long text in profile
                    showSearch_add = [] # list of custom attribs to show in search
                    ):  
    '''
    Write files for py2mappr: 
        nodes.csv
        links.csv
        node_attrs_template.csv (template for specifying attribute rendering settings in openmappr)
        line_att
    '''
    print('\nWriting openMappr files')
    ## generate csv's for py2mappr

    # prepare and write nodes.csv
    ndf['label'] = ndf[labelCol] 
    ndf['OriginalLabel'] = ndf['label']
    ndf['OriginalX'] = ndf['x_tsne']
    ndf['OriginalY'] = ndf['y_tsne']
    ndf['OriginalSize'] = 10

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
    node_attr_df['attrType'] = node_attr_df.apply(lambda x: 'liststring' if str(x['id']) in liststring_add
                                                               else 'string' if str(x['id']) in text_str_add 
                                                               else x['attrType'], axis=1)

    node_attr_df['renderType'] = node_attr_df.apply(lambda x: 'wide-tag-cloud' if str(x['id']) in wide_tags_add 
                                                               else 'tag-cloud' if str(x['id']) in tags_add
                                                               else 'text' if str(x['id']) in text_str_add
                                                               else x['renderType'], axis=1)
       # additional attributes to hide from filters
    hide = list(set(['label', 'OriginalLabel', 'OriginalSize', 'OriginalY', 'OriginalX', 'id'] + hide_add))
    node_attr_df['visible'] = node_attr_df['id'].apply(lambda x: 'FALSE' if str(x) in hide else 'TRUE')
 
       # additional attributes to hide from profile
    hideProfile = list(set(hide + hideProfile_add))
    node_attr_df['visibleInProfile'] = node_attr_df['id'].apply(lambda x: 'FALSE' if str(x) in hideProfile else 'TRUE')
    
       # additional attributes to hide from search
    hideSearch = list(set(hide + hideSearch_add))
    node_attr_df['searchable'] = node_attr_df.apply(lambda x: 'FALSE' if str(x['id']) in hideSearch else x['searchable'], axis=1)
    node_attr_df['searchable'] = node_attr_df.apply(lambda x: 'TRUE' if str(x['id']) in text_str_add else x['searchable'], axis=1)
    


       # add default alias title and node metadata description columns
    node_attr_df['title'] = node_attr_df['id']
    node_attr_df[['descr', 'maxLabel', 'minLabel', 'overlayAnchor']] = ''   
    node_attr_df[['descr', 'maxLabel', 'minLabel', 'overlayAnchor']] = ''

       # re-order final columns and write template file
    meta_cols = ['id', 'visible', 'visibleInProfile', 'searchable', 'title', 'attrType', 'renderType', 'descr', 'maxLabel', 'minLabel', 'overlayAnchor']
    node_attr_df = node_attr_df[meta_cols]
    node_attr_df.to_csv(datapath/"node_attrs.csv", index=False)


def build_network(df, attr, blacklist=[], idf=True, linksPer=3, minTags=1): 
    '''
    Run basic 'build tag network' without any plotting or layouts or file outputs.
    Resulting network can then be enriched and decorated before writing final files. 
    
    df = nodes dataframe
    attr = tag attribute to use for linking
    blacklist = tags to blacklist from linking
    linksPer = avg links per node
    minTags = exclude any nodes with fewer than min Tags
    
    Returns: nodes and links dataframes
    Dependency: https://github.com/foodwebster/Tag2Network
    '''
    print("\nBuild Network")       
    df[attr]=df[attr].fillna("")
    df = df[df[attr]!='']  # remove any recipients which have no tags for linking
    df = df.reset_index(drop=True)
    taglist = attr+"_list" # name new column of tag attribute converted into list
    df[taglist] = df[attr].apply(lambda x: x.split('|')) # convert tag string to list
    df[taglist] = df[taglist].apply(lambda x: [s for s in x if s not in blacklist])   # only keep keywords not in blacklist
    df[attr] = df[taglist].apply(lambda x: "|".join(x)) # re-join tags into string with blacklist removed
    ndf,ldf = bn.buildTagNetwork(df, tagAttr=taglist, dropCols=[], outname=None,
                            nodesname=None, edgesname=None, plotfile=None, #str(networkpath/'RecipientNetwork.pdf'), 
                            idf=idf, toFile=False, doLayout=False, linksPer=linksPer, minTags=1)
    
    return ndf,ldf
        
    