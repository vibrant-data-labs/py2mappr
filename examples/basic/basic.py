import pandas as pd
import py2mappr as mappr
import os

datapoints_path = os.path.join(os.path.dirname(__file__), '.', 'datapoints.csv')

datapoints = pd.read_csv(datapoints_path)
project = mappr.create_map(datapoints)

mappr.show()
