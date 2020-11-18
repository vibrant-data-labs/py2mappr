from src.map_utils import create_map, create_snapshot

# configure the files and folders
nodesFile = "data_in/datapoints.csv"
linksFile = "data_in/edges.csv"
nodeAttrsFile = "data_in/datapoint_attrs.csv"
outFolder = "data_out"

# configure the mapping for the reqd parameters
# maps are in the form of {"required param name": "name of column in datasheet"}
# the required param names are fixed and should not be changed.
node_attr_map = {"OriginalLabel": "label", "OriginalX": "x_tsne", "OriginalY": "y_tsne"}
link_attr_map = {"source": "Source", "target": "Target", "isDirectional": "isDirectional"}

# create some snapshots
# snapshot - scatterplot
sn1 = create_snapshot(
    name="oh kittens",
    subtitle="another scatterplot",
    summaryImg="https://placekitten.com/220/160",
    description="A kitten is a <b>juvenile cat</b>. After being born, kittens display primary altriciality and are totally dependent on their mother for survival. They do not normally open their eyes until after seven to ten days. After about two weeks, kittens quickly develop and begin to explore the world outside the nest. After a further three to four weeks, they begin to eat solid food and grow adult teeth. Domestic kittens are highly social animals and usually enjoy human companionship.",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "OriginalX",
        "yaxis": "OriginalY",
        "settings": {"nodeSizeAttr": "Citations per Year", "nodeColorAttr": "Journal"},
    },
)

# snapshot - scatterplot
sn2 = create_snapshot(
    name="scattered and battered",
    subtitle="scatterplot",
    summaryImg="https://placekitten.com/220/150",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "Year",
        "yaxis": "Citations per Year",
        "settings": {"nodeSizeAttr": "Degree", "nodeColorAttr": "Year"},
    },
)

# snapshot - network with default layout settings (see layout templates/snapshot.yaml)
sn3 = create_snapshot(
    name="the network is strong",
    subtitle="network",
    summaryImg="https://placekitten.com/220/100",
)

# snapshot - fixed size, fixed color
sn4 = create_snapshot(
    name="scatman is back",
    subtitle="another scatterplot",
    summaryImg="https://placekitten.com/220/160",
    layout_params={
        "plotType": "scatterplot",
        "xaxis": "OriginalX",
        "yaxis": "OriginalY",
        "settings": {
            "nodeSizeStrat": "fixed",  # default value = "attr"
            "nodeSizeDefaultValue": 10,  # default value = 7
            "nodeColorStrat": "fixed",  # default value = "attr"
            "nodeColorDefaultValue": "rgb(200,0,0)",  # default value = "rgb(200,200,200)"
        },
    },
)

# create map
create_map(
    nodesFile,
    linksFile,
    nodeAttrsFile,
    node_attr_map,
    link_attr_map,
    snapshots=[sn1, sn2, sn3, sn4],
    playerSettings={
        "modalTitle": "this is a document network",
        "modalDescription": "this is the map description",
        "modalSubtitle": "this is the map subtitle",
    },
    outFolder=outFolder,
)
