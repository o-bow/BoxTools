#!/usr/bin/env python3

import os

from boxtools.data.Color import ShellColor as Color
from boxtools.Logs import LogLevel, LogDisplay
from boxtools.env.environment import is_windows

log_display: LogDisplay = LogDisplay().get_log_display()

"""
Mostly shorcuts for common logging functions
Those shortcut functions are deprecated and are planned to be removed at some point
"""

def get_key(dic, val):
    for key, value in dic.items():
        if val == value:
            return key
    return None


def show_log(value, level: int = LogLevel.SILENT):
    log_display.show_log(value, level)


def show_info_log(value):
    log_display.show_log(value, LogLevel.INFO)


def show_debug_log(value):
    log_display.show_log(value, LogLevel.DEBUG)


def show_color_log(color, value, level: int = LogLevel.SILENT, color_end=Color.END):
    log_display.show_color_log(color, value, level, color_end)


def show_info_color_log(value):
    log_display.show_info_color_log(value)


def show_debug_color_log(value):
    log_display.show_debug_color_log(value)


def show_critical_log(value):
    log_display.show_critical_log(value)


def show_help_log(value):
    log_display.show_help_log(value)


def show_title_log(value):
    log_display.show_title_log(value)


def show_command_log(value, result=None):
    log_display.show_command_log(value, result)


def call_legacy_zsh(command, args):
    call_legacy_zsh_silent(command, False, args)


# {1} MUST be user_input placeholder in feedback_text
def show_input_feedback_log(feedback_text, user_input, log_level: int = LogLevel.SILENT):
    log_display.show_input_feedback_log(feedback_text, user_input, log_level)


# {1} MUST be user_input placeholder in feedback_text
def show_info_input_feedback_log(feedback_text, user_input):
    log_display.show_info_input_feedback_log(feedback_text, user_input)


# {1} MUST be user_input placeholder in feedback_text
def show_debug_input_feedback_log(feedback_text, user_input):
    log_display.show_debug_input_feedback_log(feedback_text, user_input)


def call_legacy_zsh_silent(command, args, skip_bad_os_msg=False):
    if is_windows():
        if not skip_bad_os_msg:
            show_log('This feature is not migrated yet. Please raise a request if you\'re in need of it')
    else:
        show_log('This feature is not migrated yet. Calling ZSH legacy command...')
        os.system(command + ' ' + ' '.join(args[0:]))


def show_array(value: list):
    log_display.show_array(value)


def handle_core_error(e):
    show_log(' --> Process Error:')
    show_critical_log(e.message)
    show_log(' ')
    show_debug_log(' --> Error log:')
    show_debug_log(e.__cause__)
    show_debug_log(' ')
    if hasattr(e, 'log'):
        show_info_log(e.log)
        show_info_log(' ')