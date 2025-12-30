#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import PurePath

from boxtools.data.dto.ConfigurationChangeDto import ConfigurationChangeDto
from boxtools.data.parser import iniParser


class Settings:
    def __init__(self, file_path: PurePath):
        self.configuration_file_path = file_path

    def get_settings(self) -> ConfigParser:
        return iniParser.get_properties(self.configuration_file_path)

    def get_settings_change(self) -> ConfigurationChangeDto:
        return iniParser.get_configuration_change(self.configuration_file_path)

    def apply_settings_change(self, configuration_change: ConfigurationChangeDto):
        iniParser.apply_configuration_change(self.configuration_file_path, configuration_change)

    def apply_single_setting_change(self, property_group: str, property_name: str, property_value):
        change = self.get_settings_change()
        change.add_property_change(property_group, property_name, property_value)
        return self.apply_settings_change(change)

    def has_setting(self, property_group: str, property_name: str):
        return iniParser.has_property(self.configuration_file_path, property_group, property_name)

    def get_string_setting(self, property_group: str, property_name: str) -> str:
        return iniParser.get_string_property(self.configuration_file_path, property_group, property_name)

    def get_bool_setting(self, property_group: str, property_name: str) -> bool:
        return iniParser.get_boolean_property(self.configuration_file_path, property_group, property_name)

    def get_int_setting(self, property_group: str, property_name: str) -> int:
        return iniParser.get_int_property(self.configuration_file_path, property_group, property_name)

    def get_float_setting(self, property_group: str, property_name: str) -> float:
        return iniParser.get_float_property(self.configuration_file_path, property_group, property_name)

    def get_list_setting(self, property_group: str, property_name: str):
        return iniParser.get_list_property(self.configuration_file_path, property_group, property_name)

    def get_section(self, property_group: str):
        return self.get_settings()[property_group]
