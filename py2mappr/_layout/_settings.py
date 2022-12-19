from typing import List, Literal, TypedDict

HEX_COLOR = str


class PaletteColor(TypedDict):
    col: HEX_COLOR


class LayoutSettings(TypedDict):
    drawNodes: bool
    borderRatio: float
    bigOnTop: bool
    nodeImageShow: bool
    nodeImageAttr: str
    nodeUnselectedOpacity: float
    nodeHighlightRatio: float
    nodeHighlightBorderOffset: float
    nodeHighlightBorderWidth: float
    nodeSelectionRatio: float
    nodeSelectionBorderOffset: float
    nodeSelectionBorderWidth: float
    nodeSelectionDegree: int
    isShowSelectedNodeTab: bool
    selectedNodeCommonTitle: str
    selectedNodeIncomingTitle: str
    selectedNodeOutgoingTitle: str
    neighbourListHoverDegree: int
    nodePopSize: int
    nodePopImageShow: bool
    nodePopImageAttr: str
    nodePopShow: bool
    nodePopDelay: int
    nodePopRepositionNeighbors: bool
    drawEdges: bool
    edgeDirectional: bool
    edgeTaper: bool
    edgeTaperScale: float
    edgeSaturation: float
    edgeUnselectedOpacity: float
    edgeDirectionalRender: Literal["outgoing", "incoming", "all"]
    drawLabels: bool
    drawGroupLabels: bool
    labelColor: HEX_COLOR
    labelOutlineColor: HEX_COLOR
    labelSize: Literal["proportional"]
    labelScale: float
    labelSizeRatio: float
    defaultLabelSize: int
    minLabelSize: int
    maxLabelSize: int
    labelThreshold: int
    labelMaxCount: int
    labelDefaultShow: bool
    labelAttr: str
    labelHoverAttr: str
    labelDegree: int
    labelOpacity: float
    labelUnselectedOpacity: float
    zoomLock: bool
    panLock: bool
    maxZoomLevel: int
    minZoomLevel: int
    savedZoomLevel: int
    zoomingRatio: float
    mouseZoomDuration: int
    xAxShow: bool
    yAxShow: bool
    xAxTickShow: bool
    yAxTickShow: bool
    xAxLabel: str
    yAxLabel: str
    xAxTooltip: str
    yAxTooltip: str
    invertX: bool
    invertY: bool
    scatterAspect: float
    mapboxMapID: str
    nodeSizeStrat: Literal["attr", "fixed"]
    nodeSizeAttr: str
    nodeSizeScaleStrategy: Literal["linear", "log"]
    nodeSizeScaleInvert: bool
    nodeSizeDefaultValue: int
    nodeSizeMin: int
    nodeSizeMax: int
    nodeSizeMultiplier: float
    nodeColorStrat: Literal["attr", "select", "fixed"]
    nodeColorAttr: str
    nodeColorScaleStrategy: Literal["linear", "log"]
    nodeColorScaleInvert: bool
    nodeColorScaleExponent: float
    nodeColorScaleBase: int
    nodeColorDefaultValue: HEX_COLOR
    nodeColorNumericScalerType: Literal["RGB"]
    nodeColorCycleCategoryColors: bool
    nodeColorPaletteNumeric: List[PaletteColor]
    nodeColorPaletteOrdinal: List[PaletteColor]
    edgeSizeStrat: Literal["attr", "fixed"]
    edgeSizeAttr: str
    edgeSizeScaleStrategy: Literal["linear", "log"]
    edgeSizeScaleInvert: bool
    edgeSizeDefaultValue: float
    edgeSizeMin: float
    edgeSizeMax: float
    edgeSizeMultiplier: float
    edgeColorStrat: Literal["attr", "gradient"]
    edgeColorAttr: str
    edgeColorScaleStrategy: Literal["linear", "log"]
    edgeColorScaleInvert: bool
    edgeColorScaleExponent: float
    edgeColorScaleBase: int
    edgeColorDefaultValue: HEX_COLOR
    edgeColorCycleCategoryColors: bool
    edgeColorPaletteNumeric: List[PaletteColor]
    edgeColorPaletteOrdinal: List[PaletteColor]
    edgeCurvature: int
    nodeClusterAttr: str
    drawClustersCircle: bool
    isGeo: bool


base_layout_settings: LayoutSettings = LayoutSettings(
    drawNodes=True,
    borderRatio=0.15,
    bigOnTop=False,
    nodeImageShow=False,
    nodeImageAttr="",  # to calculate
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
    nodePopImageAttr="",  # to calculate
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
    labelAttr="OriginalLabel",  # to calculate
    labelHoverAttr="OriginalLabel",  # to calculate
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
    xAxShow=False,
    yAxShow=False,
    xAxTickShow=False,
    yAxTickShow=False,
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
    nodeSizeAttr="",  # to calculate
    nodeSizeScaleStrategy="log",
    nodeSizeScaleInvert=False,
    nodeSizeDefaultValue=10,
    nodeSizeMin=2,
    nodeSizeMax=20,
    nodeSizeMultiplier=0.5,
    nodeColorStrat="attr",
    nodeColorAttr="",  # to calculate
    nodeColorScaleStrategy="linear",
    nodeColorScaleInvert=False,
    nodeColorScaleExponent=2.5,
    nodeColorScaleBase=10,
    nodeColorDefaultValue="rgb(200,200,200)",
    nodeColorNumericScalerType="RGB",
    nodeColorCycleCategoryColors=True,
    nodeColorPaletteNumeric=[{"col": "#ee4444"}, {"col": "#3399ff"}],
    nodeColorPaletteOrdinal=[
        {"col": "#bd0f0f"},
        {"col": "#5b41a3"},
        {"col": "#0099ff"},
        {"col": "#ffcc00"},
        {"col": "#66cccc"},
        {"col": "#99cc00"},
        {"col": "#993399"},
        {"col": "#b23333"},
        {"col": "#077861"},
        {"col": "#0073bf"},
        {"col": "#bf9900"},
        {"col": "#4c9999"},
        {"col": "#739900"},
        {"col": "#732673"},
    ],
    edgeSizeStrat="fixed",
    edgeSizeAttr="",  # to calculate
    edgeSizeScaleStrategy="linear",
    edgeSizeScaleInvert=False,
    edgeSizeDefaultValue=0.2,
    edgeSizeMin=0.1,
    edgeSizeMax=10,
    edgeSizeMultiplier=0.1,
    edgeColorStrat="gradient",
    edgeColorAttr="",  # to calculate
    edgeColorScaleStrategy="linear",
    edgeColorScaleInvert=False,
    edgeColorScaleExponent=2.5,
    edgeColorScaleBase=10,
    edgeColorDefaultValue="rgb(200,200,200)",
    edgeColorCycleCategoryColors=True,
    edgeColorPaletteNumeric=[{"col": "#ee4444"}, {"col": "#3399ff"}],
    edgeColorPaletteOrdinal=[
        {"col": "#bd0f0f"},
        {"col": "#5b41a3"},
        {"col": "#0099ff"},
        {"col": "#ffcc00"},
        {"col": "#66cccc"},
        {"col": "#99cc00"},
        {"col": "#993399"},
        {"col": "#b23333"},
        {"col": "#077861"},
        {"col": "#0073bf"},
        {"col": "#bf9900"},
        {"col": "#4c9999"},
        {"col": "#739900"},
        {"col": "#732673"},
    ],
    nodeClusterAttr="",
    drawClustersCircle=False,
    isGeo=False,
)
