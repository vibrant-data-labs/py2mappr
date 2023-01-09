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
import numpy as np
from tag2network.Network import BuildNetwork as bn # tag2network: build network and layout functions
from tag2network.Network import ClusterLayout as cl   #tag2network: new cluster layout function
from tag2network.Network import DrawNetwork as dn  # tag2network: plot network function
from tag2network.Network.ClusteringProperties import basicClusteringProperties
from tag2network.Network.BuildNetwork import addLouvainClusters # tag2network: directed louvain

import networkx as nx
from collections import Counter
from pathlib import Path
#from pandas.api.types import is_string_dtype
#from pandas.api.types import is_numeric_dtype

# %%

def buildNetworkX(linksdf, id1='Source', id2='Target', directed=False):
    # build networkX graph object from links dataframe with 'Source' and 'Target' ids
    # generate list of links from dataframe
    linkdata = [(getattr(link, id1), getattr(link, id2)) for link in linksdf.itertuples()]
    g = nx.DiGraph() if directed else nx.Graph()
    g.add_edges_from(linkdata)
    return g


def add_random_layout(df): 
    # random circle packed 
    # returns 2 series of x and y coordinates
    rho = np.sqrt(np.random.uniform(0, 1, len(df)))
    phi = np.random.uniform(0, 2*np.pi, len(df))
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y

def add_cluster_metrics(nodesdf, nw, groupVars):
   # add bridging, cluster centrality etc. for one or more grouping variables
   for groupVar in groupVars:
       if len(nx.get_node_attributes(nw, groupVar)) == 0:
           vals = {k: v for k, v in dict(zip(nodesdf['id'], nodesdf[groupVar])).items() if k in nw}
           nx.set_node_attributes(nw, vals, groupVar)
       grpprop = basicClusteringProperties(nw, groupVar)
       for prop, vals in grpprop.items():
           nodesdf[prop] = nodesdf['id'].map(vals)


def add_cluster_layout(ndf, ldf, dists=None, maxdist=5, 
                       cluster_attr='Cluster', # name of cluster attrubute
                       size_attr=None,
                       overlap_frac=0.2,
                       max_expansion=1.5,
                       scale_factor=1.0,
                       x='x', # name of x coord col
                       y='y' # name of y coord col
                       ): 
    print("Running clustered graph layout")
    nw = buildNetworkX(ldf)
    layout, _ = cl.run_cluster_layout(nw, ndf, dists=dists, maxdist=maxdist, 
                       size_attr=size_attr, 
                       cluster_attr=cluster_attr,
                       overlap_frac=overlap_frac, 
                       max_expansion=max_expansion, 
                       scale_factor=scale_factor)
    ndf[x] = ndf['id'].apply(lambda x: layout[x][0] if x in layout else 0.0)
    ndf[y] = ndf['id'].apply(lambda x: layout[x][1] if x in layout else 0.0)
    return ndf

def tsne_layout(ndf, ldf, clusName="Cluster", rename_xy=False):   
    ## add tsne-layout coordinates and draw
    bn.add_layout(ndf, linksdf=ldf, nw=None, clustered=False, cluster=clusName)
    if rename_xy:
        ndf.rename(columns={"x": "x_tsne", "y": "y_tsne"}, inplace=True)
    return ndf

   
def spring_layout(ndf, ldf, iterations=1000):
    print("Running spring Layout")
    nw = buildNetworkX(ldf)
    # remove isolated nodes and clusters for layout
    giant_component_nodes  = max(nx.connected_components(nw), key = len)
    giant_component = nw.subgraph(giant_component_nodes)
    layout = nx.spring_layout(giant_component, k=0.2, weight='weight', iterations=iterations) # k is spacing 0-1, default 0.1
    x ={n:layout[n][0] for n in giant_component.nodes()}
    y= {n:layout[n][1] for n in giant_component.nodes()}
    ndf['x'] = ndf['id'].map(x)
    ndf['y'] = ndf['id'].map(y)
    # place all disconnected nodes at 0,0
    ndf['x'].fillna(0, inplace=True)
    ndf['y'].fillna(0, inplace=True)
    return ndf

def force_directed(ndf, ldf, iterations=1000):
    ## add force-directed layout coordinate
    bn.add_force_directed_layout(ndf, linksdf=ldf, nw=None, iterations=iterations)
    return ndf

def plot_network(ndf, edf, plot_name, x='x', y='y', colorBy='Cluster', sizeBy='ClusterCentrality', sizeScale=100):    
    # draw network colored by creative style and save image
    # ndf = nodes dataframe
    # ldf = links dataframe 
    # plotname = name of file to save image (pdf)
    ndf['x'] = ndf[x]
    ndf['y'] = ndf[y]
    nw = buildNetworkX(edf) # build networkX graph object
    node_sizes = ndf.loc[:,sizeBy]*sizeScale
    node_sizes_array = node_sizes.values # convert sizeBy col to array for sizing
    dn.draw_network_categorical(nw, ndf, node_attr=colorBy, plotfile=plot_name, node_size=node_sizes_array)


def write_network_to_excel(ndf, ldf, outname):
    writer = pd.ExcelWriter(outname,
                          engine='xlsxwriter')
    # Don't convert url-like strings to urls.
    writer.book.strings_to_urls = False
    ndf.to_excel(writer,'Nodes', index=False)
    ldf.to_excel(writer,'Links', index=False)
    writer.close()  

def write_network_to_excel_simple (ndf, ldf, outname):
    writer = pd.ExcelWriter(outname)
    ndf.to_excel(writer,'Nodes', index=False, encoding = 'utf-8-sig')
    ldf.to_excel(writer,'Links', index=False, encoding = 'utf-8-sig')
    writer.close()  

def normalized_difference(df, attr):
    # compute normalizd difference relative to the mean
    avg_attr = df[attr].mean()
    normalized_diff = ((df[attr]-avg_attr)/(df[attr]+avg_attr)).round(4)
    return normalized_diff

def max_min_normalize(df, attr):
    max_min = (df[attr]-df[attr].min())/(df[attr].max()-df[attr].min())
    return max_min

def add_group_fracs (ndf,  
                       group_col, # grouping attribute (e.g. 'cluster')
                       attr,  # column with value compute % (e.g. 'org typ') 
                       value): # value to tally if present (e.g. 'non-profit')
    # summarize fraction of nodes each cluster where a value is present
    groups = list(ndf[group_col].unique())
    df = ndf[[group_col, attr]]
    grp_fracs = {}
    for group in groups:
        df_grp = df[df[group_col]==group] # subset cluster
        nodata = df_grp[attr].apply(lambda x: (x == None or x == ''))
        df_grp = df_grp[~nodata] # remove missing data
        grp_size = len(df_grp)
        n_value = sum(df_grp[attr] == value)  # total cases where value is true
        frac_value = np.round(n_value/grp_size, 2)
        grp_fracs[group] = frac_value
    group_value_fracs = df[group_col].map(grp_fracs)
    return group_value_fracs # series

def add_group_relative_fracs (ndf,  
                           group_col, # grouping attribute (e.g. 'cluster')
                           attr,  # column with value compute % (e.g. 'org typ') 
                           value,# value to tally if present (e.g. 'non-profit')
                           normalized =True # convert relative fract to normalized difference
                           ): 
    # summarize fraction (relative to global frac) 
    # of nodes each cluster where a value is present
    total = sum(ndf[attr].apply(lambda x: (x != None) and (x != '') and pd.notnull(x)))
    n_value = sum(ndf[attr]==value)
    global_frac = n_value/total

    groups = list(ndf[group_col].unique())
    # subset the dataframe columns
    df = ndf[['id', group_col, attr]]

    grp_fracs = {} # dict to hold fracs for each group
    grp_rel_fracs = {} # dict to hold relative fracs for each group

    for group in groups:
        df_grp = df[df[group_col]==group] # subset cluster
        w_data = df_grp[attr].apply(lambda x: (x != None) and (x != '') and pd.notnull(x))
        df_grp = df_grp[w_data] # remove missing data
        grp_size = len(df_grp)
        n_value = sum(df_grp[attr] == value)  # total cases where value is true
        # compute values for the group
        if grp_size == 0:
            frac = 0
        else:
            frac = np.round(n_value/grp_size, 2) # fraction of cases where value is tru
        if normalized:
            rel_frac = np.round(((frac - global_frac)/(frac + global_frac)),4) # normalized to global
        else:
            rel_frac = np.round((frac/global_frac), 2) # frac relative to global
        # map the values to the group dictionary
        grp_fracs[group] = frac # dict to hold fracs for each group
        grp_rel_fracs[group] = rel_frac # relative fracs for each group
    # map the group values to the dataframe
    df = df.reset_index(drop=True)
    df['frac_'+ value] = df[group_col].map(grp_fracs)
    df['rel_frac_'+ value] = df[group_col].map(grp_rel_fracs)
    return df # dataframe of just group, attr, and fracs by group

      
def add_group_sums (df,  
                    group_col, # grouping attribute (e.g. 'cluster')
                    attr, # column with value summarize % (e.g. 'total funding')  
                    sum_type  # 'sum', 'mean', 'median'
                    ):   
    # summarize total, mean, median value for each cluster
    group_means  = df.groupby(group_col)[attr].transform(sum_type)
    group_means = np.round(group_means, 2)
    return group_means #series



def add_group_frac_sums (ndf,  
                       group_col, # grouping attribute (e.g. 'cluster')
                       cat_col, # col with categorical attr to summarize by (e.g. 'funding type')
                       cat_value, # category value to compute frac of total for (e.g. 'venture')
                       num_attr,  # column with numberic value compute frac of total (e.g. total funding)
                       ): 
    # summarize fraction of total value for a group in each cluster
    # for example, for each cluster, what is the fraction of total funding that is funding type = venture
    groups = list(ndf[group_col].unique())
    df = ndf[[group_col, cat_col, num_attr]]
    grp_fracs = {}
    for group in groups:
        df_grp = df[df[group_col]==group] # subset cluster
        nodata = df_grp[cat_col].apply(lambda x: (x == None or x == ''))
        df_grp = df_grp[~nodata] # remove missing data
        grp_tot = df_grp[num_attr].sum() # sum of numeric attribute
        df_cat = df_grp[df_grp[cat_col]==cat_value] # subset those whith category value
        n_value = df_cat[num_attr].sum()  # sum of numeric attribute for subset within category
        frac_value = np.round(n_value/grp_tot, 2)
        grp_fracs[group] = frac_value
    group_value_fracs = df[group_col].map(grp_fracs)
    return group_value_fracs # series

def build_network(df, attr, blacklist=[], idf=False, linksPer=3, minTags=1): 
    '''
    Run basic 'build tag network' without any plotting or layouts or file outputs.
    Resulting network can then be enriched and decorated before writing final files. 
    
    df = nodes dataframe
    attr = tag attribute to use for linking
    blacklist = tags to blacklist from linking
    linksPer = avg links per node
    minTags = exclude any nodes with fewer than min Tags

    Returns: nodes and links dataframes
    '''
    print("\nBuild Network")
    df[attr] = df[attr].fillna("")
    df = df[df[attr] != '']  # remove any recipients which have no tags for linking
    df = df.reset_index(drop=True)
    taglist = attr+"_list"  # name new column of tag attribute converted into list
    df[taglist] = df[attr].apply(lambda x: x.split('|'))  # convert tag string to list
    df[taglist] = df[taglist].apply(lambda x: [s for s in x if s not in blacklist])   # only keep keywords not in blacklist
    df[attr] = df[taglist].apply(lambda x: "|".join(x)) # re-join tags into string with blacklist removed
    ndf, ldf = bn.buildTagNetwork(df, tagAttr=taglist, dropCols=[], outname=None,
                                  nodesname=None, edgesname=None, plotfile=None,  # str(networkpath/'RecipientNetwork.pdf'), 
                                  idf=idf, toFile=False, doLayout=False, linksPer=linksPer, minTags=1)
    return ndf, ldf


def decorate_network(df, ldf, tag_attr,
                     network_renameDict,  # column renaming
                     finalNodeAttrs,  # final columns to keep
                     outname,  # final network file name
                     labelcol,  # column to be used for node label
                     clusName,  # name of cluster attr
                     addLayout=True,
                     layout = 'cluster',  # other options: 'tsne', 'force-directed'
                     size_attr=None,
                     overlap_frac=0.2,  # cluster overlap
                     fd_iterations = 1000,  # iterations for force-directed layout
                     plot=False,  # option to plot network
                     x='x',
                     y='y',
                     writeFile=True,
                     removeSingletons=True):
    '''
    Decorate network from 'build_network'
    df = node dataframe (ndf) from build_network
    ldf = links dataframe
    tag_attr = name of tag column used for linking
    outname = name of final network file (excel file)
    writeFile = write final excel file with nodes and links sheets
    removeSinteltons = trim final keyword tag list to only inlcudes ones that occur at least twice

    Returns: cleaned/decorated nodes datframe plus original links dataframe
    '''
    print("\nDecorating Newtork")
    # tag_attr is the tag attribute used for linking

    # Add Cluster Counts, and additional Cluster Labels
    print("Adding Cluster Counts and short Cluster labels")
    df['Cluster_count'] = df.groupby(['Cluster'])['id'].transform('count')
    df[clusName] = df.cluster_name.str.split(', ').apply(lambda x: ', '.join(x[:3]))  # use top 3 tags as short name
    df['label'] = df[labelcol]
    df['x'] = np.random.uniform(0,1, df.shape[0]) # add random coordinates if no layout
    df['y'] = np.random.uniform(0,1, df.shape[0])  # add random coordinates if no layout
    ## add layouts
    if addLayout==True:
        if layout =='cluster':
            # add clustered layout coordinates
            df = add_cluster_layout(df, ldf,
                           cluster_attr=clusName,
                           size_attr=size_attr,
                           overlap_frac=overlap_frac, 
                           max_expansion=1.5, 
                           scale_factor=1.0)
        if layout == 'tsne':
            ## add tsne layout coordinates
            df = tsne_layout(df, ldf, clusName=clusName)
        if layout == 'force-directed':
            ## add force-directed layout coordinates
            df = spring_layout(df, ldf, iterations=fd_iterations)
     
    # add outdegree
    nw = buildNetworkX(ldf, directed=True)
    df['n_Neighbors'] = df['id'].map(dict(nw.out_degree()))
    
    if removeSingletons:
        print("Removing singleton keywords")
        #remove singleton tags
        # across entire dataset, count tag hist and remove singleton tags
        taglist_attr = tag_attr+"_list"
        df[taglist_attr].fillna('', inplace=True)
        # build master histogram of tags that occur at least twice 
        tagHist = dict([item for item in Counter([k for kwList in df[taglist_attr] for k in kwList]).most_common() if item[1] > 1])
        # filter tags to only include 'active' tags - tags which occur twice or more in the entire dataset
        df[taglist_attr] = df[taglist_attr].apply(lambda x: [k for k in x if k in tagHist])
        # double check to remove spaces and empty elements
        df[taglist_attr] = df[taglist_attr].apply(lambda x: [s.strip() for s in x if len(s)>0] )
        # join list back into string of unique pipe-sepparated tags
        df[tag_attr] = df[taglist_attr].apply(lambda x: "|".join(list(set(x)))) 
        df['nTags'] = df[tag_attr].apply(lambda x: len(x.split("|")))  

    if plot:
        # Plot Network
        plot_network(df, ldf, "Network_plot.pdf", 
                     colorBy = clusName,  # color by cluster
                     sizeBy='ClusterCentrality', 
                     x=x, 
                     y=y)
    
    ## Clean final columns
    print("Cleaning final columns")
    df.rename(columns=network_renameDict, inplace=True)        

    if finalNodeAttrs: # if custom list ot None, trim  columns
        df = df[finalNodeAttrs]                
    

    if writeFile and outname is not None:
        print("Writing Cleaned Network File")
        # Write back out to excel with 2 sheets. 
        Path("results/networks").mkdir(parents=True, exist_ok=True)
        df = df.reset_index(drop=True)
        write_network_to_excel(df, ldf, outname)
        
    return df, ldf


### MAIN FUNCTION TO BUILD AND DECORATE AFFINITY NETWORK ###
def build_decorate_plot_network(df, 
                                tag_attr, # tag col for linking
                                linksPer,# links per node
                                blacklist, # tags to blacklist for linjking
                                nw_name, # final filename for network
                                network_renameDict, # rename final node attribs
                                finalNodeAttrs = None,  # custom list of final columns, if None keep all
                                tagcols_nodata=[], # tag columns to replace empty with 'no data'
                                minTags=1, 
                                removeSingletons=True,
                                clusName = "Keyword_Theme", # name of cluster attribute
                                labelcol='profile_name', 
                                add_nodata = True,
                                addLayout=True,
                                layout='cluster', 
                                plot=False,
                                x='x', # x attrib from add_layout
                                y='y'): # y attrib from add_layout 
    '''
    build and decorate linkedin affinity network
    tagcols: columns to replace empty tags with 'no data' if add_nodata
    Returns:  ndf, ldf and plots/writes pdf of network viz 
    '''
    # Build Network
    ndf, ldf = build_network(df, tag_attr , idf=False, linksPer=linksPer, blacklist= blacklist, minTags=minTags)
    # Decorate network
    ndf, ldf = decorate_network(ndf, ldf, tag_attr,
                                 network_renameDict,  # column renaming
                                 finalNodeAttrs,  # final columns to keep
                                 nw_name,  # final network file name
                                 labelcol,
                                 clusName,
                                 addLayout=addLayout,
                                 layout=layout,
                                 plot=plot,
                                 x=x,
                                 y=y,
                                 writeFile=True,
                                 removeSingletons=True)
    if add_nodata:
        # add 'no data' to empty tags
        for col in tagcols_nodata:
            ndf[col].fillna('no data', inplace=True)
            ndf[col] = ndf[col].apply(lambda x: 'no data' if x == "" else x)

    return ndf, ldf

