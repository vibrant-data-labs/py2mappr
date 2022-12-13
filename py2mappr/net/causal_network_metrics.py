# -*- coding: utf-8 -*-


import pandas as pd
import networkx as nx
from .trophiclevel import rootedTL
import random
from collections import defaultdict

import sys
from tag2network.Network import BuildNetwork as bn # tag2network: build network and layout functions
from tag2network.Network import ClusterLayout as cl   #tag2network: new cluster layout function
from tag2network.Network.BuildNetwork import addLouvainClusters # tag2network: directed louvain
from tag2network.Network.ClusteringProperties import basicClusteringProperties
from tag2network.Network.DrawNetwork import draw_network_categorical
#from py2mappr.src.similarity import jaccardianSim




#---------------------------------------------
# Custom Metrics
#---------------------------------------------

def buildNetworkX(linksdf, id1='Source', id2='Target', directed=True):
    # build networkX graph object from links dataframe with 'Source' and 'Target' ids
    # generate list of links from dataframe
    linkdata = [(getattr(link, id1), getattr(link, id2)) for link in linksdf.itertuples()]
    g = nx.DiGraph() if directed else nx.Graph()
    g.add_edges_from(linkdata)
    return g


# compute number of second degree outgoing neighbors
def outoutdegree(nw):
    outout = {n:set() for n in nw.nodes()}
    for n in nw.nodes():
        for n2 in nw.successors(n):
            outout[n].update(nw.successors(n2))
    return {n:len(outout[n]) for n in nw.nodes()}

# compute number of second degree incoming neighbors
def inindegree(nw):
    inin = {n:set() for n in nw.nodes()}
    for n in nw.nodes():
        for n2 in nw.predecessors(n):
            inin[n].update(nw.predecessors(n2))
    return {n:len(inin[n]) for n in nw.nodes()}

# summarize fraction of positive incoming and outgoung links
# beware that in_edges and out_edges return data in different formats, looks like a networkx bug
def fracoutpositive(nw):
    result = {}
    for n in nw.nodes():
        e = list(nw.out_edges(n, data='ispos'))
        if len(e) > 0:
            ispos = list(zip(*e))[2]  #*e zips element by element [(A,B,1), (X,Y,2)] >>  [(A,X), (B,Y), (1,2)]
            result[n] = sum(ispos)/float(len(ispos))
        else:
            result[n] = 0
    return result

def fracinpositive(nw):
    result = {}
    for n in nw.nodes():
        e = list(nw.in_edges(n, data='ispos'))
        if len(e) > 0:
            #ispos_l = list(zip(*e)[2])
            #ispos = [d['ispos'] for d in ispos_l]
            ispos = list(zip(*e))[2]
            result[n] = sum(ispos)/float(len(ispos))
        else:
            result[n] = 0
    return result

def fracOutNeg(nw):
    result = {}
    for n in nw.nodes():
        e = list(nw.out_edges(n, data='isneg'))
        if len(e) > 0:
            isneg = list(zip(*e))[2]  #*e zips element by element [(A,B,1), (X,Y,2)] >>  [(A,X), (B,Y), (1,2)]
            result[n] = sum(isneg)/float(len(isneg))
        else:
            result[n] = 0
    return result

def fracInNeg(nw):
    result = {}
    for n in nw.nodes():
        e = list(nw.in_edges(n, data='isneg'))
        if len(e) > 0:
            #ispos_l = list(zip(*e)[2])
            #ispos = [d['ispos'] for d in ispos_l]
            isneg = list(zip(*e))[2]
            result[n] = sum(isneg)/float(len(isneg))
        else:
            result[n] = 0
    return result

def avg_votes(nw):
    result = {}
    for n in nw.nodes():
        e = list(nw.edges(n, data='votes'))
        if len(e) > 0:
            votes = list(zip(*e))[2]
            result[n] = sum(votes)/float(len(votes))
        else:
            result[n] = 0
    return result

def add_cluster_metrics(nodesdf, nw, groupVars):
   # add bridging, cluster centrality etc. for one or more grouping variables
   for groupVar in groupVars:
       if len(nx.get_node_attributes(nw, groupVar)) == 0:
           vals = {k: v for k, v in dict(zip(nodesdf['id'], nodesdf[groupVar])).items() if k in nw}
           nx.set_node_attributes(nw, vals, groupVar)
       grpprop = basicClusteringProperties(nw, groupVar)
       for prop, vals in grpprop.items():
           nodesdf[prop] = nodesdf['id'].map(vals)
    

def compute_node_pair_similarities(nw, id2labelDict, deleteIdentical=False):
    # todo: implement/delete this function
    pass
    # calcualte similarity between all pairs of nodes in their incomign and outgoing links
    # returns dataframe sorty by most similar node pairs
    # sims = jaccardianSim(nw, deleteIdentical = False)
    # simdf = pd.DataFrame(sims, columns=['id_1', 'id_2', 'jaccard_similarity'])
    # simdf['label_1'] = simdf['id_1'].map(id2labelDict)
    # simdf['label_2'] = simdf['id_2'].map(id2labelDict)
    # simdf['avg_frac_overlap'] = simdf['jaccard_similarity'].apply(lambda x: (2*x)/(1+x))
    # simdf.sort_values('jaccard_similarity', ascending=False, inplace=True)
    # return simdf

def add_percentile(df, col):
    #returns a series
    return df[col].rank(method='max').apply(lambda x: 100*(x-1)/(len(df)-1)) # percentile linear interpolation (0-100)

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

def trophic_level_normalized (ndf, nw):
    '''
    DESCRIPTION. compute rooted trophic level - root node added to bottom and connected to all to address looping.
    Then normalized the values from 0-1
    Returns: series
    '''
    ndf['Trophic_Level'] = ndf['id'].map(rootedTL(nw)) #rooted trophic level (root node added to base to deal with looping
    ndf['Trophic_Level'] = min_max_normalize_column (ndf, 'Trophic_Level') # normalize 0-1
    return ndf['Trophic_Level'] 
    

def flagKeystone_topFrac(df, leverage, reach, thresh):
    df['Top_Keystone_fracTrials'] = (df[leverage] >= thresh) & (df[reach] >= thresh)
    df['Size_keystones_topFrac'] =  df['Top_Keystone_fracTrials'].apply(lambda x:  8 if x else 1)
    
def flagKeystone_avgPctl(df, thresh, keystone='keystone_pctl_mean'):
    topKeystones = (df[keystone] >= thresh)   
    return topKeystones # series of boolean values for top percentile keystones

######################################
### network level stats
def compute_connectance(ndf, ldf):
    possible_links = len(ndf)*(len(ndf)-1) # possible links
    realized_links = len(ldf) # links with consensus votes
    return realized_links/possible_links

def compute_frac_isolated_nodes(ndf):
    n_isolated = sum(ndf['total_links'] == 0)
    return n_isolated/len(ndf) # frac isolated
    
########################
### Layouts coordinates

def plot_network(ndf, edf, plot_name, x='x_tsne', y='y_tsne', colorBy='Cluster', sizeBy='Keystone_Index', sizeScale=100):    
    # draw network colored by creative style and save image
    nw = bn.buildNetworkX(edf)
    node_sizes = ndf.loc[:,sizeBy]*sizeScale
    node_sizes_array = node_sizes.values # convert sizeBy col to array for sizing
    draw_network_categorical(nw, ndf, node_attr=colorBy, plotfile=plot_name, x=x, y=y, node_size=node_sizes_array)

def force_directed(nw, ndf, ldf, iterations=100, plot = True):
    ## add force-directed layout coordinates and draw
    bn.add_force_directed_layout(ndf, linksdf=ldf, nw=None, iterations=iterations)
    if plot:
        bn.draw_network_categorical(nw, ndf, node_attr = "Cluster", x='x_force_directed', y= 'y_force_directed', plotfile="network_fd.pdf")
    return ndf

def tsne_layout(nw, ndf, ldf, plot=True):   
    ## add tsne-layout coordinates and draw
    bn.add_layout(ndf, linksdf=ldf, nw=None)
    ndf.rename(columns={"x": "x_tsne", "y": "y_tsne"}, inplace=True)
    if plot:
         plot_network(ndf, ldf, "network_tsne.pdf", x='x_tsne', y='y_tsne', colorBy='Cluster', sizeBy='Keystone_Index')
    return ndf
   
def spring_layout(nw, ndf, iterations=1000):
    print("Running spring Layout")
    layout = nx.spring_layout(nw, iterations=iterations)
    x ={n:layout[n][0] for n in nw.nodes()}
    y= {n:layout[n][1] for n in nw.nodes()}
    ndf['x_spring'] = ndf['id'].map(x)
    ndf['y_spring'] = ndf['id'].map(y)
    return ndf

def cluster_layout(ndf, ldf, dists=None, maxdist=5, 
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


def add_network_metrics(nw, ndf, ldf, 
                        sign=True, # links have pos vs neg sign
                        add_clusters=True, # add directed louvain clusters 
                        add_clustered_layout=True, # add cluster layout coordinates
                        ):
    #---------------------------------------------
    # add metrics to node metadata
    #---------------------------------------------
    print ("Calculating network metrics")
    # Add standard metrics
    ndf['total_links'] = ndf['id'].map(dict(nx.degree(nw))) #calculate metric and map to column in dataframe
    ndf['betweenness'] = ndf['id'].map(dict(nx.betweenness_centrality(nw)))
    ndf['in_degree'] = ndf['id'].map(dict(nw.in_degree())) #note that in and out degree have diff format that the previous
    ndf['out_degree'] = ndf['id'].map(dict(nw.out_degree()))
    
    # Add 'leverage' metrics
    ndf['outout_degree'] = ndf['id'].map(outoutdegree(nw))
    ndf['inin_degree'] = ndf['id'].map(inindegree(nw))
    ndf['2_Degree_Leverage'] = ((ndf['outout_degree'] - ndf['in_degree'])/(ndf['outout_degree'] + ndf['in_degree']))
    ndf['2_Degree_Asymmetry'] = ((ndf['outout_degree'] - ndf['inin_degree'])/(ndf['outout_degree'] + ndf['inin_degree']))
    ndf['1_Degree_Asymmetry'] = ((ndf['out_degree'] - ndf['in_degree'])/(ndf['out_degree'] + ndf['in_degree'])) #normalized diff out vs in
    ndf['2_Degree_Reach'] = (ndf['outout_degree']/float(len(ndf)))*100 # % of network reached in 2 hops
    ndf['Keystone_Index_1'] = keystone_index(ndf, reach='2_Degree_Reach', leverage = '2_Degree_Leverage') # 
    ndf['Keystone_Index'] = keystone_index(ndf, reach='2_Degree_Reach', leverage = '2_Degree_Asymmetry') #
    #ndf['Keystone_Index'] = min_max_normalize_column (ndf, 'Keystone_Index') # normalize 0-1
    ndf['Keystone_Pctl'] = add_percentile(ndf, 'Keystone_Index')
    
    ndf.fillna(0, inplace=True)
    
    # Add trophic level - scaled 0-1 (rooting the network to a basal node)
    ndf['Trophic_Level'] = trophic_level_normalized (ndf, nw)
    
    if sign:
        # Add summaries of frac positive out and in and avg votes
        ndf['frac_negative_out'] = ndf['id'].map(fracOutNeg(nw))
        ndf['frac_negative_in'] = ndf['id'].map(fracInNeg(nw))
        ndf['avg_LinkVotes'] = ndf['id'].map(avg_votes(nw))
        
    # Add louvain clusters with directed modularity (from Tag2Network)
    if add_clusters:
        addLouvainClusters(ndf, nw=nw)
        add_cluster_metrics(ndf, nw, ['Cluster'])
    if add_clustered_layout:
        ## add clustered  layout coordinates
        ndf = cluster_layout(ndf, ldf, 
                              cluster_attr='Cluster', # name of cluster attrubute
                              overlap_frac=0.2,
                              max_expansion=1.5,
                              scale_factor=1.0)
        '''
        # add force directed layout coordinates
        ndf = force_directed(nw, ndf, ldf, iterations = 100, plot=False)
        ndf = spring_layout(nw, ndf)
        '''


