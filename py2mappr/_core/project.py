from typing import Dict, List, Union
from .config import AttributeConfig, ProjectConfig, Config, base_config, default_attr_config
from py2mappr._attributes.calculate import calculate_attr_types, calculate_render_type
from py2mappr._layout import Layout, LayoutSettings
from pandas import DataFrame

class OpenmapprProject:
    dataFrame: DataFrame
    network: Union[DataFrame, None] = None
    attributes: Dict[str, AttributeConfig]
    configuration: ProjectConfig
    snapshots: List[Layout] = []

    debug: bool = False

    def __init__(self, dataFrame: DataFrame, config: Config = base_config):
        self.dataFrame = dataFrame
        self.configuration = ProjectConfig(config)
        self.attributes = self._set_attributes()

    def _set_attributes(self) -> Dict[str, AttributeConfig]:
        attributes = dict()
        attr_types = calculate_attr_types(self.dataFrame)
        render_types = calculate_render_type(self.dataFrame, attr_types)

        for column in self.dataFrame.columns:
            attributes[column] = {
                **default_attr_config,
                'id': column,
                'title': column,
                'attrType': attr_types[column],
                'renderType': render_types[column],
            }

        return attributes

    def set_debug(self, debug: bool):
        self.debug = debug

    def set_data(self, dataFrame: DataFrame):
        self.dataFrame = dataFrame

    def set_network(self, network: DataFrame):
        self.network = network

