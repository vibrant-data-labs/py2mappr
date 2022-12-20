import pandas as pd
import py2mappr as mappr
import os

datapoints_path = os.path.join(os.path.dirname(__file__), ".", "nodes.csv")
edges_path = os.path.join(os.path.dirname(__file__), ".", "links.csv")

datapoints = pd.read_csv(datapoints_path)
edges = pd.read_csv(edges_path)

# prepare the project
project, layout = mappr.create_map(datapoints, edges)

# ---------------------------------------- #
# Keyword Theme layout
# ---------------------------------------- #

layout.set_nodes(
    # by default 'year published' is selected for node color
    # change it to 'keyword_theme'
    node_color="keyword_theme",
    # by default 'views' is selected for node size
    # change it to 'comments'
    node_size="comments",
    # make the node size difference more visible
    node_size_scaling=(1, 15, 1),
)

# enabling the images to be shown on the nodes
layout.settings.update({"nodeImageShow": True})

# styling the layout
layout.set_display_data(
    title="TED Talks by Keyword Theme",
    subtitle="Nodes are colored by Keyword Theme",
    description="""<p>This layout has a title of <b>Keyword Theme</b> "
        and shows the TED talks colored by Keyword Theme</p>""",
)

# ---------------------------------------- #
# Scatterplot Layout
# ---------------------------------------- #

scatterplot = mappr.create_layout(layout_type="scatterplot")

# make the nodes on scatterplot to be placed according to the published year and views
scatterplot.x_axis = "year_published"
scatterplot.y_axis = "views"
# enabling the images to be shown on the scatterplot layout as well
scatterplot.settings.update({"nodeImageShow": True})

# styling the layout
scatterplot.set_display_data(
    title="Views by Year Published",
    subtitle="Scatterplot of views by year published",
    description="<p>This layout represents the number of views by year published</p>",
)

# ---------------------------------------- #
# Attributes data
# ---------------------------------------- #

# adding the url link to the right panel
project.attributes["TED_url"]["attrType"] = "url"
project.attributes["TED_url"]["renderType"] = "default"

# enabling videos in the node right panel
project.attributes["video"]["attrType"] = "video"
project.attributes["video"]["renderType"] = "default"

# adding the description to the node right panel
project.attributes["description"]["attrType"] = "string"
project.attributes["description"]["renderType"] = "text"

# removing filter by photo and label attributes
project.attributes["photo"]["renderType"] = "default"
project.attributes["label"]["renderType"] = "default"

# provide attributes with a nice title
title_map = {
    "keyword_theme": "Keyword Theme",
    "keywords": "Keywords",
    "event": "Event",
    "speaker(s)": "Speaker(s)",
    "other_tags": "Other Tags",
    "speaker_occupation": "Speaker Occupation",
    "views": "Views",
    "comments": "Comments",
    "popularity_index": "Popularity Index",
    "video": "TED Video",
    "description": "Description",
    "year_published": "Published (Year)",
    "date_published": "Published (Date)",
    "year_filmed": "Year Filmed",
    "#_languages": "# Languages",
    "duration_(min)": "Duration (min)",
    "TED_url": "TED URL",
    "label": "Label",
    "photo": "Photo",
}

for attr in title_map:
    project.attributes[attr]["title"] = title_map[attr]

# hiding the auxiliary attributes
attrs_to_hide = [
    "id",
    "x_tsne",
    "y_tsne",
    "x_force_directed",
    "y_force_directed",
]
for attr in attrs_to_hide:
    project.attributes[attr]["visible"] = False

# ---------------------------------------- #
# Project display configuration
# ---------------------------------------- #

project.set_display_data(
    title="TED Talks | openmappr via py2mappr",
    description="TED Talks data visualization",
    how_to="""<p>
        Visualisation is created using 
        <a target="_blank" href="https://github.com/vibrant-data-labs/py2mappr">py2mappr</a> library 
        and displayed using 
        <a target="_blank" href="https://github.com/vibrant-data-labs/openmappr-player">openmappr</a> tool.
    </p>"""
)

mappr.show()
