import pandas as pd
import py2mappr as mappr
import py2mappr.publish as publisher
import os

datapoints_path = os.path.join(os.path.dirname(__file__), '.', 'datapoints.csv')
edges_path = os.path.join(os.path.dirname(__file__), '.', 'edges.csv')

datapoints = pd.read_csv(datapoints_path)
edges = pd.read_csv(edges_path)

project, original = mappr.create_map(datapoints, edges)
original.set_nodes(node_color="Journal")
original.set_links()

publisher.run([
    # publish to S3 as a website
    publisher.s3("p2m-basic-example"),
    # and then start locally
    publisher.local()
])