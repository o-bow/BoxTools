from pathlib import PurePath

from boxtools.dto.PropertyDto import PropertyDto


class ConfigurationChangeDto:
    properties = []

    def __init__(self, configuration_file_path: PurePath):
        self.configuration_file_path = configuration_file_path

    def add_property_change(self, group_name: str, property_name: str, property_value: str):
        self.properties.append(PropertyDto(group_name, property_name, property_value))

    def get_changes(self) -> list[PropertyDto]:
        return self.properties
