import pandas as pd
import py2mappr as mappr
import os

datapoints_path = os.path.join(os.path.dirname(__file__), '.', 'datapoints.csv')
edges_path = os.path.join(os.path.dirname(__file__), '.', 'edges.csv')

datapoints = pd.read_csv(datapoints_path)
edges = pd.read_csv(edges_path)

project = mappr.create_map(datapoints)
mappr.set_network(edges)
project.set_debug(True)

mappr.show()
