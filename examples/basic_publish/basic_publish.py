import pandas as pd
import py2mappr as mappr
import py2mappr.publish as publisher
import os

datapoints_path = os.path.join(os.path.dirname(__file__), '.', 'datapoints.csv')
edges_path = os.path.join(os.path.dirname(__file__), '.', 'edges.csv')

datapoints = pd.read_csv(datapoints_path)
edges = pd.read_csv(edges_path)

project, original = mappr.create_map(datapoints)
mappr.set_network(edges)

original.set_nodes(node_color="Journal")
original.set_links()

scatterplot = mappr.create_layout(datapoints, layout_type="scatterplot")
scatterplot.name = "My Custom Scatterplot"
scatterplot.set_nodes(node_color="Journal")
for attr in project.attributes:
    project.attributes[attr]['axis'] = 'all'

mappr.set_debug(False)

# mappr.show()

publisher.run([
    publisher.s3("p2m-basic-example"),
    publisher.cloudfront("p2m-basic.openmappr.org"),
    publisher.cloudflare("p2m-basic.openmappr.org")
])