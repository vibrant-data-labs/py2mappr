# -*- coding: utf-8 -*-
"""

"""

import sys

import pandas as pd
#import numpy as np
import pathlib as pl #path library

sys.path.append("../../Tag2Network/tag2network/")  # add Tag2Network directory
from Network import BuildNetwork as bn
#from Network.BuildNetwork import addLouvainClusters
#from Network.ClusteringProperties import basicClusteringProperties


pd.set_option('display.expand_frame_repr', False) # expand display of data columns if screen is wide

wd = pl.Path.cwd()
datapath = wd/"raw_data"/"10_yrs_of_TED_Network.xlsx"
resultspath = wd/"processed_data"

##  read network file 
ndf = pd.read_excel(datapath, sheet_name="Nodes")
ldf = pd.read_excel(datapath, sheet_name="Links")

# create networkx object
nw=bn.buildNetworkX(ldf)


def force_directed(ndf, ldf, iterations=100, plot = True):
    ## add force-directed layout coordinates and draw
    bn.add_force_directed_layout(ndf, linksdf=ldf, nw=None, iterations=iterations)
    if plot:
        bn.draw_network_categorical(nw, ndf, node_attr = "keyword_theme", x='x_force_directed', y= 'y_force_directed', plotfile="network_fd.pdf")
    return ndf

def tsne_layout(ndf, ldf, plot=True):   
    ## add tsne-layout coordinates and draw
    bn.add_layout(ndf, linksdf=ldf, nw=None)
    ndf.rename(columns={"x": "x_tsne", "y": "y_tsne"}, inplace=True)
    if plot:
        bn.draw_network_categorical(nw, ndf, node_attr = "keyword_theme", x='x_tsne', y= 'y_tsne', plotfile="network_tsne.pdf")
    return ndf


## add tsne coordinates
ndf = tsne_layout(ndf, ldf, plot=False)
# add force directed coordinates
ndf = force_directed(ndf, ldf, iterations = 1000, plot=False)

## generate csv's for py2mappr
ndf.to_csv(resultspath/"nodes.csv", index=False)
ldf.to_csv(resultspath/"links.csv", index=False)

# create node attribute metadata template:
node_attrs = ndf.columns.tolist()
ndf_meta = pd.DataFrame({'id':node_attrs})

meta_cols = ['visible', 'visibleInProfile', 'searchable', 'title', 'attrType', 'renderType', 'descr', 'maxLabel', 'minLabel', 'overlayAnchor']
for col in meta_cols:
    ndf_meta[col] = ''
ndf_meta.to_csv(resultspath/"node_attrs_template.csv", index=False)    
    
    