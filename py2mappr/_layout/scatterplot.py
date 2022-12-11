from ._layout import Layout, LayoutSettings
from .._attributes import utils as attrutils

scatterplot_base_settings: LayoutSettings = LayoutSettings(
    drawNodes=True,
    borderRatio=0.15,
    bigOnTop=False,
    nodeImageShow=False,
    nodeImageAttr="", # to calculate
    nodeUnselectedOpacity=0.25,
    nodeHighlightRatio=1.2,
    nodeHighlightBorderOffset=6,
    nodeHighlightBorderWidth=1,
    nodeSelectionRatio=1.2,
    nodeSelectionBorderOffset=0,
    nodeSelectionBorderWidth=3,
    nodeSelectionDegree=1,
    isShowSelectedNodeTab=True,
    selectedNodeCommonTitle="Neighbors",
    selectedNodeIncomingTitle="Incoming",
    selectedNodeOutgoingTitle="Outgoing",
    neighbourListHoverDegree=1,
    nodePopSize=10,
    nodePopImageShow=True,
    nodePopImageAttr="", # to calculate
    nodePopShow=False,
    nodePopDelay=1500,
    nodePopRepositionNeighbors=True,
    drawEdges=False,
    edgeDirectional=True,
    edgeTaper=False,
    edgeTaperScale=0.5,
    edgeSaturation=1,
    edgeUnselectedOpacity=0.2,
    edgeDirectionalRender="outgoing",
    drawLabels=True,
    drawGroupLabels=True,
    labelColor="#000000",
    labelOutlineColor="#ffffff",
    labelSize="proportional",
    labelScale=1,
    labelSizeRatio=0.5,
    defaultLabelSize=12,
    minLabelSize=12,
    maxLabelSize=16,
    labelThreshold=1,
    labelMaxCount=300,
    labelDefaultShow=True,
    labelAttr="OriginalLabel", # to calculate
    labelHoverAttr="OriginalLabel", # to calculate
    labelDegree=0,
    labelOpacity=1,
    labelUnselectedOpacity=0,
    zoomLock=False,
    panLock=False,
    maxZoomLevel=10,
    minZoomLevel=-10,
    savedZoomLevel=-2,
    zoomingRatio=1.7,
    mouseZoomDuration=500,
    # valid for scatterplot only
    xAxShow=True,
    yAxShow=True,
    xAxTickShow=True,
    yAxTickShow=True,
    xAxLabel="",
    yAxLabel="",
    xAxTooltip="",
    yAxTooltip="",
    # valid for scatterplot only
    invertX=False,
    invertY=True,
    scatterAspect=0.5,
    # valid for geo only
    mapboxMapID="",
    nodeSizeStrat="attr",
    nodeSizeAttr="", # to calculate
    nodeSizeScaleStrategy="log",
    nodeSizeScaleInvert=False,
    nodeSizeDefaultValue=10,
    nodeSizeMin=2,
    nodeSizeMax=20,
    nodeSizeMultiplier=0.5,
    nodeColorStrat="attr",
    nodeColorAttr="", # to calculate
    nodeColorScaleStrategy="linear",
    nodeColorScaleInvert=False,
    nodeColorScaleExponent=2.5,
    nodeColorScaleBase=10,
    nodeColorDefaultValue="rgb(200,200,200)",
    nodeColorCycleCategoryColors=True,
    nodeColorPaletteNumeric=[
      { "col": "#ee4444"},
      { "col": "#3399ff"}
    ],
    nodeColorPaletteOrdinal=[
        { "col": "#bd0f0f" },
        { "col": "#5b41a3" },
        { "col": "#0099ff" },
        { "col": "#ffcc00" },
        { "col": "#66cccc" },
        { "col": "#99cc00" },
        { "col": "#993399" },
        { "col": "#b23333" },
        { "col": "#077861" },
        { "col": "#0073bf" },
        { "col": "#bf9900" },
        { "col": "#4c9999" },
        { "col": "#739900" },
        { "col": "#732673" }
    ],
    edgeSizeStrat="fixed",
    edgeSizeAttr="", # to calculate
    edgeSizeScaleStrategy="linear",
    edgeSizeScaleInvert=False,
    edgeSizeDefaultValue=0.2,
    edgeSizeMin=0.1,
    edgeSizeMax=10,
    edgeSizeMultiplier=1,
    edgeColorStrat="gradient",
    edgeColorAttr="", # to calculate
    edgeColorScaleStrategy="linear",
    edgeColorScaleInvert=False,
    edgeColorScaleExponent=2.5,
    edgeColorScaleBase=10,
    edgeColorDefaultValue="rgb(200,200,200)",
    edgeColorCycleCategoryColors=True,
    edgeColorPaletteNumeric=[
      { "col": "#ee4444"},
      { "col": "#3399ff"}
    ],
    edgeColorPaletteOrdinal=[
        { "col": "#bd0f0f" },
        { "col": "#5b41a3" },
        { "col": "#0099ff" },
        { "col": "#ffcc00" },
        { "col": "#66cccc" },
        { "col": "#99cc00" },
        { "col": "#993399" },
        { "col": "#b23333" },
        { "col": "#077861" },
        { "col": "#0073bf" },
        { "col": "#bf9900" },
        { "col": "#4c9999" },
        { "col": "#739900" },
        { "col": "#732673" }
    ],
    nodeClusterAttr="",
    isGeo=False
    )

class ScatterplotLayout(Layout):
    def __init__(self, project, settings = scatterplot_base_settings, x_axis = "X", y_axis = "Y", name=None, descr=None, subtitle=None, image=None):
        super().__init__(settings, "scatterplot", x_axis, y_axis, name, descr, subtitle, image)
        self.calculate_layout(project)

    def calculate_layout(self, project):
        self.x_axis, self.y_axis = attrutils.find_node_xy_attr(project.dataFrame)
        self.settings["nodeImageAttr"] = attrutils.find_node_image_attr(project.dataFrame)
        self.settings["nodePopImageAttr"] = attrutils.find_node_image_attr(project.dataFrame)
        self.settings["labelAttr"] = attrutils.find_node_label_attr(project.dataFrame)
        self.settings["labelHoverAttr"] = attrutils.find_node_label_attr(project.dataFrame)
        self.settings["nodeColorAttr"] = attrutils.find_node_color_attr(project.dataFrame)
        self.settings["nodeSizeAttr"] = attrutils.find_node_size_attr(project.dataFrame)

        if (project.network is not None):
            self.settings["edgeColorAttr"] = attrutils.find_node_color_attr(project.network)
            self.settings["edgeSizeAttr"] = attrutils.find_node_size_attr(project.network)

    def toDict(self):
        return {
          "id": self.id,
          "descr": self.descr,
          "snapName": self.name,
          "subtitle": self.subtitle,
          "summaryImg": self.image,
          "isEnabled": True,
          "isDeleted": False,
          "camera": {
              "normalizeCoords": True,
              "r": 1.3347904373327948,
              "x": 0,
              "y": 0
          },
          "layout": {
            "plotType": "scatterplot",
            "xaxis": self.x_axis,
            "yaxis": self.y_axis,
            "settings": self.settings
          }
        }