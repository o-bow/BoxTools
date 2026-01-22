#!/usr/bin/env python3

import os
import platform
import posixpath
import re
import subprocess
from pathlib import PurePath

from boxtools.Logs import LogDisplay

"""
A set of environment related utility functions
"""

def is_windows():
    return platform.system().lower() == 'windows'


# 11.0.10 ...
def get_java_full_version():
    search = re.search(
        r'\"(\d+\.\d+.\d+).*\"',
        str(subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT))
    ).groups()
    if len(search) > 0:
        return search[0]
    else:
        return None


# 1.8 / 9 / 10 / 11 ...
def get_java_major_version():
    version = get_java_full_version()
    if version is not None:
        parts = version.split('.')
        version_major = int(parts[0])
        # Below v9, it was 1.8 & so on. Afterwards, it became single digit.
        if len(parts) > 1:
            if version_major > 8:
                return version_major
            else:
                return parts[0] + '.' + parts[1]
    return version


def ping(host, show_log=True, package_count=1):
    is_win = platform.system().lower() == 'windows'
    ping.param = "-n" if is_win else "-c"
    result = subprocess.run(['ping', ping.param, str(package_count), host],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output = result.stdout
    if show_log and not is_win:
        logger: LogDisplay = LogDisplay().get_log_display()
        logger.show_process_log(result)
    return result.returncode == 0 and (b'TTL=' in output or b'ttl=' in output)


def mk_dir(output_path: PurePath, new_folder: str):
    new_full_path = str(output_path) + get_path_separator() + new_folder
    logger: LogDisplay = LogDisplay().get_log_display()
    logger.show_debug_log('mk_dir: ' + new_full_path)
    if not os.path.exists(new_full_path):
        os.mkdir(new_full_path)
        logger.show_info_log("\n - Folder did not exist. Path created ( " + str(new_full_path) + " )")


# file_name should contain path, or it'll create the file at the place the command is run at.
def mk_file(folder_path: PurePath, file_name: str):
    mk_file_at_fullpath(str(folder_path.joinpath(file_name)))


# file_name should contain path, or it'll create the file at the place the command is run at.
def mk_file_at_fullpath(file_name: str):
    logger: LogDisplay = LogDisplay().get_log_display()
    try:
        open(file_name, 'a').close()
    except OSError:
        logger.show_info_log('Failed creating the file')
    else:
        logger.show_info_log('File created')


def get_path_separator():
    return ('/', '\\')[is_windows()]


def get_line_break():
    return ('\n', '\r\n')[is_windows()]


def get_parent_folder(path: str) -> posixpath:
    return os.path.dirname(path)


def list_dir_files(folder_path: posixpath):
    return sorted(os.listdir(folder_path))


def has_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(name) is not None


def validate_tool(name):
    if not has_tool(name):
        logger: LogDisplay = LogDisplay().get_log_display()
        logger.show_log(' -> Aborted: ' + name + ' tool not found')
        import sys
        sys.exit(1)

def has_alias(alias_name: str, src_file: str = ".zshrc") -> bool | None:
    """
    :return: True if it's found, False if not found, None if src_file (default .zshrc) does not exist
    """
    from pathlib import Path
    zshrc_path = Path.home() / src_file
    if zshrc_path.exists():
        with open(zshrc_path, 'r') as f:
            content = f.read()
        if f"alias {alias_name}=" in content:
            return True
        else:
            return False
    return None