from typing import Any, Dict, List, Literal, TypedDict

from py2mappr._attributes.attr_types import ATTR_TYPE, RENDER_TYPE


class SponsorInfo(TypedDict):
    """
    The SponsorInfo class is a TypedDict that contains the information for a
    sponsor of the project.
    """

    iconUrl: str
    linkUrl: str
    linkTitle: str


class FeedbackInfo(TypedDict):
    """
    The FeedbackInfo class is a TypedDict that contains the information for
    feedback of the project.
    """

    type: Literal["email", "link"]
    link: str
    text: str


class ProjectConfig(TypedDict):
    """
    The ProjectConfig class is a TypedDict that contains the configuration for
    the project.
    """

    fontClass: str
    showModal: bool
    simpleSplash: bool
    showHeader: bool
    headerType: str
    shareTitle: str
    shareTitleCompare: str
    shareTitleSelect: str
    shareEnableSelect: bool
    showExportBtn: bool
    facebookShare: bool
    twitterShare: bool
    colorTheme: str
    showPanels: bool
    showSearch: bool
    showTimeline: bool
    showSnapDescrs: bool
    infoClickToParent: bool
    showSnapTooltips: bool
    panelLayoutType: str
    autoPlay: bool
    snapTransition: str
    snapDuration: int
    timelineType: str
    totalDuration: int
    headerTitle: str
    headerImageUrl: str
    headerHtml: str
    highlightColor: str
    modalDescription: str
    modalBackground: str
    modalLogo: str
    modalSubtitle: str
    searchAlg: str
    modalTitle: str
    modalIntroHtml: str
    allowJoin: bool
    displayTooltipCard: bool
    startPage: Literal["filter", "legend", "list"]
    showStartInfo: bool
    defaultPanel: str
    sponsors: List[SponsorInfo]
    projectLogoTitle: str
    projectLogoUrl: str
    sharingLogoUrl: str
    displayExportButton: bool
    beta: bool
    sponsorsTxt: str
    feedback: FeedbackInfo
    socials: List[Literal["twitter", "linkedin", "facebook"]]
    footer: Any


base_config: ProjectConfig = {
    "fontClass": "Roboto",
    "showModal": True,
    "simpleSplash": True,
    "showHeader": True,
    "headerType": "simple",
    "shareTitle": "Check out this map",
    "shareTitleCompare": "Check out my node",
    "shareTitleSelect": "Check out these nodes",
    "shareEnableSelect": False,
    "showExportBtn": True,
    "facebookShare": False,
    "twitterShare": False,
    "colorTheme": "light",
    "showPanels": True,
    "showSearch": True,
    "showTimeline": True,
    "showSnapDescrs": True,
    "infoClickToParent": False,
    "showSnapTooltips": False,
    "panelLayoutType": "interactive",
    "autoPlay": False,
    "snapTransition": "tween",
    "snapDuration": 10,
    "timelineType": "bottom",
    "totalDuration": 1000,
    "headerTitle": "map title",
    "headerImageUrl": "",
    "headerHtml": "<h1>map header</h1>",
    "highlightColor": "#e21186",
    "modalDescription": "<p>map description</p>",
    "modalBackground": "",
    "modalLogo": "",
    "modalSubtitle": "<p>map subtitle</p>",
    "searchAlg": "matchSorter",
    "modalTitle": "document network",
    "modalIntroHtml": "<h1>document_network_test</h1><div>Each of the 1000 nodes in this mapp represents ...</div><div>They are linked with each other if they are similar across the following attributes</div><div>a) Attribute 1</div><div>b) Attribute 2</div><h1></h1>",
    "allowJoin": False,
    "displayTooltipCard": False,
    "startPage": "legend",
    "showStartInfo": True,
    "defaultPanel": "Map Information",
    "sponsors": [],
    "projectLogoTitle": "openmappr | network exploration tool",
    "projectLogoUrl": None,
    "sharingLogoUrl": None,
    "displayExportButton": False,
    "beta": False,
    "sponsorsTxt": "Sponsored by",
    "feedback": {"type": "email", "link": "mailto:", "text": "Feedback"},
    "footer": None,
    "socials": [],
}


class AttributeConfig(TypedDict):
    """
    The AttributeConfig class is a TypedDict that contains the configuration for
    an attribute to be used in the project.
    """

    id: str
    title: str
    visible: bool
    visibleInProfile: bool
    searchable: bool
    attrType: ATTR_TYPE
    renderType: RENDER_TYPE
    metadata: Dict[str, str]
    overlayAnchor: str
    priority: Literal["high", "medium", "low"]
    axis: Literal["x", "y", "none"]
    tooltip: str
    colorSelectable: bool
    sizeSelectable: bool


class NetworkAttributeConfig(TypedDict):
    """
    The NetworkAttributeConfig class is a TypedDict that contains the configuration for
    an edge attribute to be used in the project.
    """

    id: str
    title: str
    visible: bool
    searchable: bool
    attrType: ATTR_TYPE
    renderType: RENDER_TYPE
    visibleInProfile: bool
    metadata: Dict[str, str]


default_attr_config: AttributeConfig = {
    "id": "",
    "title": "",
    "visible": True,
    "visibleInProfile": True,
    "searchable": True,
    "attrType": "string",
    "renderType": "default",
    "metadata": {"descr": "", "maxLabel": "", "minLabel": ""},
    "overlayAnchor": "",
    "priority": "medium",
    "axis": "none",
    "tooltip": "",
    "colorSelectable": False,
    "sizeSelectable": False,
}

default_net_attr_config: NetworkAttributeConfig = {
    "id": "OriginalLabel",
    "title": "OriginalLabel",
    "visible": False,
    "searchable": False,
    "attrType": "liststring",
    "renderType": "tag-cloud",
    "visibleInProfile": False,
    "metadata": {},
}
