from typing import Dict, Literal, TypedDict

from py2mappr._attributes.attr_types import ATTR_TYPE, RENDER_TYPE

class Config(TypedDict):
    name: str
base_config: Config = {
    'name': 'openmappr | network exploration tool',
}

class ProjectConfig:
    _config: Config
    def __init__(self, config: Config) -> None:
        self._config = config

    def get(self, field: str):
        return self._config[field]

    def set(self, field: str, value: str):
        self._config[field] = value
    
class AttributeConfig(TypedDict):
    id: str
    title: str
    visible: bool
    visibleInProfile: bool
    searchable: bool
    attrType: ATTR_TYPE
    renderType: RENDER_TYPE
    metadata: Dict[str, str]
    overlayAnchor: str
    priority: Literal['high', 'medium', 'low']
    axis: Literal['x', 'y', 'none']
    colorSelectable: bool
    sizeSelectable: bool

default_attr_config: AttributeConfig = {
    'id': '',
    'title': '',
    'visible': True,
    'visibleInProfile': True,
    'searchable': True,
    'attrType': "string",
    'renderType': "default",
    'metadata': {
                "descr": "",
                "maxLabel": "",
                "minLabel": ""
            },
    'overlayAnchor': '',
    'priority': 'medium',
    'axis': 'none',
    'colorSelectable': True,
    'sizeSelectable': True,
}