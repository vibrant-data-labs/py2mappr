from typing import Dict, List, Union
from .config import AttributeConfig, ProjectConfig, base_config, default_attr_config, default_net_attr_config
from py2mappr._attributes.calculate import calculate_attr_types, calculate_render_type
from py2mappr._layout import Layout, LayoutSettings
from pandas import DataFrame

class OpenmapprProject:
    dataFrame: DataFrame
    network: Union[DataFrame, None] = None
    network_attributes: Dict[str, AttributeConfig]
    attributes: Dict[str, AttributeConfig]
    configuration: ProjectConfig
    snapshots: List[Layout] = []

    debug: bool = False

    def __init__(self, dataFrame: DataFrame, config: ProjectConfig = base_config):
        self.dataFrame = dataFrame
        self.configuration = config
        self.attributes = self._set_attributes()

    def set_debug(self, debug: bool):
        self.debug = debug

    def set_data(self, dataFrame: DataFrame):
        self.dataFrame = dataFrame
        self.attributes = self._set_attributes()
        for layout in self.snapshots:
            layout.calculate_layout(self)

    def set_network(self, network: DataFrame):
        self.network = network
        self.network_attributes = self._set_network_attributes()
        for layout in self.snapshots:
            layout.calculate_layout(self)

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

    def _set_network_attributes(self) -> Dict[str, AttributeConfig]:
        attributes = dict()
        attr_types = calculate_attr_types(self.network)
        render_types = calculate_render_type(self.network, attr_types)

        for column in self.network.columns:
            attributes[column] = {
                **default_net_attr_config,
                'id': column,
                'title': column,
                'attrType': attr_types[column],
                'renderType': render_types[column],
            }

        return attributes    
