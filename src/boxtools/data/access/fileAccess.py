#!/usr/bin/env python3
import glob
import os
from pathlib import PurePath, Path
from typing import Pattern, Match

from boxtools.exception.Exceptions import ParseException
from boxtools.data.parser.iniParser import set_properties


def delete_dir_content(path):
    from boxtools.env.environment import get_path_separator
    files = glob.glob(path + get_path_separator() + '*')
    for f in files:
        os.remove(f)


# NOT Recursive
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def get_caller_path():
    import sys
    try:
        return sys.modules['__main__'].__file__
    except KeyError:
        print('libray not loaded from script')
    except AttributeError:
        print('script not loaded from file')
    return None


# Recursive
def glob_find(name, path):
    return glob.glob(str(path) + '/**/' + name, recursive=True)


def glob_partial_name_ind(part: str, path):
    return glob.glob(str(path) + '/**/*' + part + '*', recursive=True)


def insert_before_eof(file_path: str, lines_from_bottom: int, lines_to_insert: list):
    # Insert text n lines before the end of file
    try:
        with open(file_path) as file:
            lines = file.readlines()
            insert_position = len(lines) - lines_from_bottom
            idx: int = 0
            for line in lines_to_insert:
                lines.insert(insert_position + idx, lines_to_insert[idx])
                idx += 1
        with open(file_path, 'w') as new_file:
            for line in lines:
                new_file.write(line)
    except TypeError as te:
        raise ParseException('insert_before_eof: Failed to  read content at file path ' + str(file_path)) from te


def write_to_file(file_path, content, mode: str = "w"):
    file_content = open(file_path, mode)
    file_content.writelines(content)
    file_content.close()


def cleanup_file(file_path: str):
    create_if_not_exists(PurePath(file_path))
    f = open(file_path, 'r+')
    f.truncate(0) # need '0' when using r+
    f.seek(0)
    f.close()


def cleanup_and_write_file(file_path: str, text: str):
    create_if_not_exists(PurePath(file_path))
    f = open(file_path, "a") # Create a blank file
    f.seek(0)  # sets  point at the beginning of the file
    f.truncate()  # Clear previous content
    f.write(text) # Write file
    f.close() # Close file


def get_file_as_str(file_path: PurePath):
    # Store trd file content in a string
    try:
        with open(file_path, 'r') as file:
            # read all content of a file
            content = file.read()
    except TypeError as te:
        raise ParseException('get_file_as_str: Failed to read content at file path ' + str(file_path)) from te
    return content


def get_file_as_list(file_path: PurePath, do_strip: bool = True):
    lines = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                lines.append(line.strip() if do_strip else line)
    except TypeError as te:
        raise ParseException('get_file_as_list: Failed to read content at file path ' + str(file_path)) from te
    return lines


def match_in_file(file_path: PurePath, compiled_regex: Pattern[str], group_id: int):
    try:
        with open(file_path) as file:
            lines = file.readlines()
            for line in lines:
                result: Match[str] | None = compiled_regex.search(line)
                if result is not None and result.groups() is not None and len(result.groups()) >= group_id:
                    return result.group(group_id)
    except TypeError as te:
        raise ParseException('match_in_file: Failed to read content at file path ' + str(file_path)) from te
    return None


def rename_all_files(root_path: str, original_text: str, value: str):
    for path, sub_dirs, files in os.walk(root_path):
        for name in files:
            old_name = os.path.join(path, name)
            new_name = os.path.join(path, name.replace(original_text, value))
            print('Renaming .: ' + old_name + ' :. to .: ' + new_name + ' :.')
            os.rename(old_name, new_name)

def file_exists(file_path: PurePath):
    return os.path.exists(file_path)


def create_if_not_exists(file_path: PurePath):
    if not file_exists(file_path):
        open(file_path, 'w').close()


def get_box_root_path() -> PurePath:
    path: PurePath = PurePath(get_caller_path())
    while path.name != 'src':
        path = path.parent
        if path.name is None:
            raise ParseException('Box path can\'t be determined: your box implementation project MUST contain an src folder at root level')
    # root > src
    return path.joinpath('..')


def get_box_path() -> PurePath:
    # file > module > src > root (boxname) > calling script
    return PurePath(get_caller_path()).parent


def get_python_box_path() -> PurePath:
    # file > module > src > root - index start at 0
    return get_box_path().joinpath('pythonBox')


def get_legacy_box_path() -> PurePath:
    return get_box_path().joinpath('zshBox')


def get_box_config_ini_file_path(file_name: str) -> PurePath:
    return get_python_box_path().joinpath('resources', 'config', file_name)


def write_configuration(conf_file_name, config):
    set_properties(get_box_config_ini_file_path(file_name=conf_file_name), config)


def get_zshrc_path() -> PurePath:
    return PurePath(str(Path.home())).joinpath('.zshrc')