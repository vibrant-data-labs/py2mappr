from src.map_utils import create_map

# generate map folder
create_map(
    datapointsPath="data_in/datapoints.csv",
    linksPath="data_in/edges.csv",
    datapointAttrPath="data_in/datapoint_attrs.csv",
    node_attr_map={"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"},
    link_attr_map={"source": "Source", "target": "Target", "isDirectional": "isDirectional"},
    outFolder="data_out",
)
