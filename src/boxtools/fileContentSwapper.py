#!/usr/bin/env python3
from pathlib import PurePath

import boxtools.environment
from boxtools.Logs import LogDisplay
from boxtools.dto.Exceptions import ParseException
from boxtools.dto.Settings import Settings
from boxtools.environment import validate_tool
from boxtools.fileAccess import get_box_config_ini_file_path


def update_file(file_path, replace_map, if_not_exist: bool = False, is_append: bool = False):
    # Open file
    with open(file_path, "r") as file_content:
        # list all Lines for an update
        list_of_lines = file_content.readlines()
        # Find wanted line(s)
        for line_number, line in enumerate(list_of_lines):
            for k, v in replace_map.items():
                is_replace_line = str(k).endswith('.*') & line.startswith(k[0:len(k) - 2])
                if is_replace_line:
                    # Update the desired line(s)
                    list_of_lines[line_number] = v + boxtools.environment.get_line_break()
                elif k in line and ((if_not_exist and v not in line) or not if_not_exist):
                    new_str = v if not is_append else (k + v)
                    list_of_lines[line_number] = list_of_lines[line_number].replace(k, new_str)
    # Write it out
    replace_in_file(file_path, list_of_lines)


def add_to_file(file_path: str, list_of_lines):
    file_content = open(file_path, "a")
    file_content.writelines(list_of_lines)
    file_content.close()

def replace_in_file(file_path: str, list_of_lines):
    file_content = open(file_path, "w")
    file_content.writelines(list_of_lines)
    file_content.close()


# hierarchy_array: ['toto', 'tata', 'titi'] for
# toto:
#   tata:
#     titi: someValue
# Notes:
# - MUST be full hierarchy (aka first item must have a 0 space indent.
# - MUST be a correctly indented yml file (2 spaces indent added per level)
def get_line_by_yml_hierarchy(file_path, hierarchy_array):
    # Open file
    with open(file_path, "r") as file_content:
        # list all Lines for an update
        list_of_lines = file_content.readlines()
        # Find wanted line(s)
        match_lvl = None
        for line_number, line in enumerate(list_of_lines):
            no_match_lvl = match_lvl is None
            matcher = 0 if no_match_lvl else match_lvl + 1
            leading_spaces = len(line) - len(line.lstrip())
            if (no_match_lvl is False) & (leading_spaces < matcher * 2):
                # reset progress if we went up by one lvl
                match_lvl = None
                matcher = 0
            # Look for next hierarchy level
            matching_string = ' ' * (matcher * 2) + hierarchy_array[matcher]
            if line.startswith(matching_string):
                match_lvl = matcher
                if len(hierarchy_array) == match_lvl + 1:
                    return line_number
    # Close file
    file_content.close()
    return None


def update_line(file_path, line_number, value):
    file_content = open(file_path, "r")
    list_of_lines = file_content.readlines()
    list_of_lines[line_number] = value + "\n"
    replace_in_file(file_path, list_of_lines)

def add_lines(file_path: str, nb_lines: int, text: str):
    with open(file_path) as infile:
        lines = infile.readlines()
    with open(file_path, 'w') as outfile:
        for i,line in enumerate(lines):
            outfile.write(line)
            if not i%nb_lines:
                outfile.write(text + '\n')

def prepend_text(filename: str | PurePath, text: str):
    from fileinput import input
    with input(filename, inplace=True) as file:
        for line in file:
            if file.isfirstline():
                print(text)
            print(line, end="")


def t2s(path_to_convert: str):
    logger: LogDisplay = LogDisplay().get_log_display()
    validate_tool('expand')
    validate_tool('sponge')
    cmd: str = "expand -t 4 " + path_to_convert + " | sponge " + path_to_convert
    logger.show_command_log(cmd)
    from os import system
    system(cmd)


def dt2s(path_to_convert: str, user_ini_file: str = 'user.ini'):
    logger: LogDisplay = LogDisplay().get_log_display()
    validate_tool('find')
    validate_tool('expand')
    validate_tool('sponge')
    extensions: list = ['*.java']
    try:
        user_settings: Settings | None = Settings(get_box_config_ini_file_path(user_ini_file))
        if user_settings is None:
            print(f'Invalid user ini file: [{user_ini_file}]. Defaulting to *.java extension only')
        else:
            extensions = user_settings.get_list_setting('FILE', 'DT2S_EXTENSIONS')
            if len(extensions) == 0:
                print('No extensions configured. Defaulting to *.java extension only')
                extensions = ['*.java']
    except ParseException as pe:
        print(str(pe))
        print('Defaulting to *.java extension only')

    filename_cmd: str = '-iname '
    if len(extensions) > 0:
        filename_cmd += (' -o -iname '.join(extensions))
        filename_cmd = '\\( ' + filename_cmd + ' \\)'
    cmd: str = f"find {path_to_convert} -type f {filename_cmd} -execdir sh -c 'expand -t 4 \"{{}}\" | sponge \"{{}}\"' \\;"
    logger.show_command_log(cmd)
    from os import system
    res = system(cmd)
    if res != 0:
        logger.show_critical_log('Failure in dt2s command')
    else:
        logger.show_info_log(f'Success')