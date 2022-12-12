import pandas as pd
import py2mappr as mappr
import os

datapoints_path = os.path.join(os.path.dirname(__file__), '.', 'datapoints.csv')
edges_path = os.path.join(os.path.dirname(__file__), '.', 'edges.csv')

datapoints = pd.read_csv(datapoints_path)
edges = pd.read_csv(edges_path)

project, original = mappr.create_map(datapoints)
mappr.set_network(edges)

original.settings.update({
    'nodeColorAttr': 'Journal'
})

scatterplot = mappr.create_layout(datapoints, layout_type="scatterplot")
scatterplot.name = "Scatterplot"
scatterplot.settings.update({
    'nodeColorAttr': 'Journal',
})
for attr in project.attributes:
    project.attributes[attr]['axis'] = 'all'

project.set_debug(False)

mappr.build()
