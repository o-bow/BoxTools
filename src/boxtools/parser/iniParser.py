#!/usr/bin/env python3

import configparser
from pathlib import PurePath
from typing import Any

from boxtools.dto.Exceptions import ParseException

from boxtools.dto.ConfigurationChangeDto import ConfigurationChangeDto


def get_properties(conf_file_path: PurePath) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(str(conf_file_path))
    return config


def get_string_property(conf_file_path: PurePath, property_group: str, property_name: str) -> str:
    try:
        return get_properties(conf_file_path)[property_group][property_name]
    except KeyError as ke:
        raise ParseException('Failed to retrieve string property ' + property_name + ' of group ' + property_group) \
            from ke


def get_boolean_property(conf_file_path: PurePath, property_group: str, property_name: str) -> bool:
    try:
        return get_properties(conf_file_path)[property_group].getboolean(property_name)
    except KeyError as ke:
        raise ParseException('Failed to retrieve boolean property ' + property_name + ' of group ' + property_group) \
            from ke


def get_int_property(conf_file_path: PurePath, property_group: str, property_name: str) -> int:
    try:
        return get_properties(conf_file_path)[property_group].getint(property_name)
    except KeyError as ke:
        raise ParseException('Failed to retrieve int property ' + property_name + ' of group ' + property_group) \
            from ke


def get_float_property(conf_file_path: PurePath, property_group: str, property_name: str) -> float:
    try:
        return get_properties(conf_file_path)[property_group].getfloat(property_name)
    except KeyError as ke:
        raise ParseException('Failed to retrieve float property ' + property_name + ' of group ' + property_group) \
            from ke


def get_list_property(conf_file_path: PurePath, property_group: str, property_name: str) -> list[str] | list[Any]:
    try:
        b_property: str = get_properties(conf_file_path)[property_group].get(property_name)
        if b_property is None:
            return []
        return b_property.split(',')
    except KeyError as ke:
        raise ParseException('Failed to retrieve list property ' + property_name + ' of group ' + property_group) \
            from ke


# Use set_property instead if you have a single property to set
def set_properties(conf_file_path: PurePath, config):
    with open(str(conf_file_path), 'w') as configfile:
        config.write(configfile)


def get_configuration_change(conf_file_path: PurePath) -> ConfigurationChangeDto:
    return ConfigurationChangeDto(conf_file_path)


# User should only use this one for save operations
# Use get_configuration_change to retrieve initial object, then use its add_property_change method
def apply_configuration_change(conf_file_path: PurePath, configuration_change: ConfigurationChangeDto):
    properties = get_properties(conf_file_path)
    for change in configuration_change.get_changes():
        properties[change.property_group][change.property_name] = change.property_value
    set_properties(conf_file_path, properties)


def has_property(conf_file_path: PurePath, property_group: str, property_name: str):
    return get_properties(conf_file_path).has_option(property_group, property_name)
