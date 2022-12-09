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
    isGeo: bool
