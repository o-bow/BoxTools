#!/usr/bin/env python3
from pathlib import PurePath

from boxtools.Logs import LogDisplay
from boxtools.environment import mk_dir, get_path_separator
from boxtools.fileAccess import glob_find, match_in_file
from boxtools.stringUtils import upper_first_letter, new_line
from typing import Pattern
from re import compile

class_declaration_pattern: Pattern[str] = compile(
    "public class ([a-zA-Z0-9_<>]*) extends ([a-zA-Z0-9._]*)[a-zA-Z0-9._<> ,]* ?(implements [a-zA-Z0-9._<>])? ?{")

abstract_class_declaration_pattern: Pattern[str] = compile(
    "public abstract class ([a-zA-Z0-9_]*)([a-zA-Z0-9._<> ,&]*)? ?{?")

def get_extended_class_name_for_line(class_declaration_line, logging = None):
    if logging is not None:
        logging.debug('get_extended_class_name --- class_declaration: ' + class_declaration_line)
    result = class_declaration_pattern.search(class_declaration_line)
    if result is None:
        if logging is not None:
            logging.debug(' - get_extended_class_name -- no match on class_declaration_pattern')
    elif result.groups() is not None and len(result.groups()) >= 3:
        entity_name = result.group(1).strip()
        extended_entity_name = result.group(2).strip()
        if logging is not None:
            logging.debug("    -> found match: " + result.group(0))
            logging.debug("    -> entity_name: " + entity_name)
            logging.debug("    -> extended_entity_name: " + extended_entity_name)
        return extended_entity_name
    return None

def extends_class_name(class_declaration_line, expected_class_name, logging = None):
    if logging is not None:
        logging.debug('extends_class_name --- class_declaration: ' + class_declaration_line)
    return 'extends ' + expected_class_name in class_declaration_line

def get_extended_class_name_for_file(file_path: PurePath, logging = None):
    logging.debug(get_indent() + '- get_extended_class_name_for_file -> Calling match_in_file for file ' + str(file_path))
    return match_in_file(file_path, class_declaration_pattern, 2)

def is_abstract_class(file_path: PurePath, logging = None) -> bool:
    logging.debug(get_indent() + '- is_abstract_class -> Calling match_in_file for file ' + str(file_path))
    return match_in_file(file_path, abstract_class_declaration_pattern, 2) is not None

def get_indent() -> str:
    return '    '

def get_java_class_package_value(file_path: str, package_str_to_match: str = 'package '):
    package_value = None
    if file_path is not None:
        entity_file = open(file_path, 'r')

        do_exit = False
        while not do_exit:
            # Get next line from file
            line = entity_file.readline()

            # if line is empty, end of file is reached
            if not line:
                break

            str_line = str(line).strip()
            semicolon_index = str_line.find(';')

            if package_str_to_match in line and semicolon_index > 0:
                start_index = str_line.find('package')
                package_value = str_line[start_index:semicolon_index].replace('package', '').strip()
                do_exit = True
        entity_file.close()
    return package_value


def add_getter(indent_count: int, property_name: str, property_class: str, to_list: list, add_override: bool = True,
               date_format: str | None = None):
    indent = get_indent()
    c_property_name = upper_first_letter(property_name)
    getter_line = indent * indent_count + 'public ' + property_class + ' get' + c_property_name + '() { ' + new_line()
    if getter_line not in to_list:
        if date_format is not None:
            to_list.append(indent + date_format + new_line())
        if add_override:
            to_list.append(indent * indent_count + '@Override' + new_line())
        to_list.append(getter_line)
        to_list.append(indent * (indent_count + 1) + 'return ' + property_name + '; ' + new_line())
        to_list.append(indent * indent_count + '} ' + new_line())
        to_list.append(new_line())


def make_getter(indent_count: int, property_name: str, property_class: str, add_override: bool = True):
    str_lst = []
    add_getter(indent_count, property_name, property_class, str_lst, add_override)
    return str_lst


def add_setter(indent_count: int, property_name: str, property_class: str, to_list: list, add_override: bool = True,
               optional_content: str = None):
    indent = get_indent()
    c_property_name = upper_first_letter(property_name)
    setter_line = indent * indent_count + 'public void set' + c_property_name + '(' + property_class + ' ' \
                  + property_name + ') { ' + new_line()
    if setter_line not in to_list:
        if add_override:
            to_list.append(indent * indent_count + '@Override' + new_line())
        if (property_class and (property_class.startswith('List') or property_class.startswith('Set')
            or property_class.startswith('Map'))):
           to_list.append(indent * indent_count + '@Schema(accessMode = Schema.AccessMode.READ_ONLY)' + new_line())
        to_list.append(setter_line)
        to_list.append(indent * (indent_count + 1) + 'this.' + property_name + ' = ' + property_name + '; ' + new_line())
        if optional_content is not None:
            to_list.append(indent * (indent_count + 1) + optional_content + new_line())
        to_list.append(indent * indent_count + '} ' + new_line())
        to_list.append(new_line())
    elif add_override:
        to_list.append(new_line())
        to_list.append(indent * indent_count + '@Override' + new_line())


def make_setter(indent_count: int, property_name: str, property_class: str, add_override: bool = True):
    str_lst = []
    add_setter(indent_count, property_name, property_class, str_lst, add_override)
    return str_lst


def add_constructor(indent_count: int, property_name: str, to_list: list,
                    optional_parameter_content: str = None,
                    optional_content: str = None):
    indent = get_indent()
    c_property_name = upper_first_letter(property_name)
    to_list.append(indent * indent_count + 'public ' + c_property_name
                   + '(' + (optional_parameter_content if optional_parameter_content is not None else '') + ') {' + new_line())
    if optional_content is not None:
        to_list.append(indent * (indent_count + 1) + optional_content + new_line())
    to_list.append(indent * indent_count + '}' + new_line())
    to_list.append(new_line())


def create_sub_folder(folder_path: PurePath, path_to_package: list, folder_name):
    mk_dir(folder_path, folder_name)
    path_to_package.append(folder_name)
    return folder_path.joinpath(folder_name)


def create_hierarchy(packages, folder_path, path_to_package: list):
    for package in packages:
        # create <package_name> dir if not exist
        folder_path = create_sub_folder(folder_path, path_to_package, package)
    return folder_path


def extract_class_path(file_path: str, root_element: str = 'com'):
    if file_path is None:
        return None
    class_path: str = file_path.replace(get_path_separator(), '.')
    class_path = class_path[class_path.index('.' + root_element + '.') + 1:]
    if class_path.endswith('.java'):
        class_path = class_path[:len(class_path) - 5]
    return class_path

def is_comment_line(str_line):
    return str_line.startswith("/*") and str_line.endswith("*/") or str_line.startswith("//")

def is_codeless_line(str_line):
    return is_comment_line(str_line) or len(str_line) == 0

def find_project_class(class_name: str, project_path: str):
    logger: LogDisplay = LogDisplay().get_log_display()
    c_file_name = class_name if class_name.endswith('.java') else class_name + '.java'
    logger.show_debug_log(' - searching file: ' + str(c_file_name))
    res = glob_find(c_file_name, project_path)
    if len(res) > 0:
        logger.show_debug_log(' - file found: ' + str(res))
        return res[0]
    return None
