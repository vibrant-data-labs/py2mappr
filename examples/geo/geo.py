import pandas as pd
import numpy as np
import py2mappr as mappr
import os

# dataset is taken from https://www.kaggle.com/datasets/0b157d370b5b46f60235fee6bfe7d8be3581a5c030fd0cd87c8ba4b32cee4684

datapoints_path = os.path.join(os.path.dirname(__file__), ".", "raw_data.csv")
datapoints = pd.read_csv(datapoints_path)

# add the id column for the datapoints
datapoints["id"] = np.arange(datapoints.shape[0])
datapoints["Label"] = datapoints["STATE"]
datapoints["Latitude"] = datapoints["lat"]
datapoints["Longitude"] = datapoints["long"]

# creating sample links
edges = pd.DataFrame()
edges["source"] = datapoints["id"]
edges["target"] = datapoints["id"].shift(10)
edges[edges["target"].isna()] = 0

# preparing the project
project, layout = mappr.create_map(datapoints, edges, layout_type="geo")

layout.set_nodes(
    # coloring nodes by the estimated population with numeric scale
    node_color="POPESTIMATE2019",
    node_size="POPESTIMATE2019",
    # updating the minimum and maximum values for better display
    node_size_scaling=(5, 15, 1),
)

layout.set_display_data(
    title="Geo View",
    subtitle="US Population (2019) data visualization",
    description="<p>Nodes are colored by the estimated population</p>",
)

# updating the display name of the attribute
project.attributes["POPESTIMATE2019"]["title"] = "Population (2019)"

# hiding the start info
project.configuration.update({"showStartInfo": False, "startPage": "filter"})

# hiding the auxiliary attributes
attrs_to_hide = ["id", "lat", "long", "Latitude", "Longitude", "STATE"]
for attr in attrs_to_hide:
    project.attributes[attr]["visible"] = False


project.set_display_data(
    title="US Population 2019 | openmappr via py2mappr",
    description="TED Talks data visualization",
    how_to="""<p>
        Visualisation is created using 
        <a target="_blank" href="https://github.com/vibrant-data-labs/py2mappr">py2mappr</a> library 
        and displayed using 
        <a target="_blank" href="https://github.com/vibrant-data-labs/openmappr-player">openmappr</a> tool.
    </p>
    <p>
        Dataset is taken from 
        <a target="_blank" href="https://www.kaggle.com/datasets/0b157d370b5b46f60235fee6bfe7d8be3581a5c030fd0cd87c8ba4b32cee4684">Kaggle</a> 
    </p>""",
)

mappr.show()
