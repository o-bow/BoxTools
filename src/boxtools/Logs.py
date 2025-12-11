#!/usr/bin/env python3
from pathlib import PurePath
from subprocess import CompletedProcess

from boxtools.Color import ShellColor as Color
import collections.abc

from boxtools.dto.Exceptions import ParseException
from boxtools.dto.Settings import Settings
from boxtools.fileAccess import get_box_config_ini_file_path
from boxtools.stringUtils import new_line


class LogLevel:
    SILENT = 1
    INFO = 2
    DEBUG = 3


class LogDisplay:
    def __init__(self, app_log_level: int = LogLevel.SILENT, box_file_path: PurePath = None):
        self.app_log_level = app_log_level
        self.box_file_path = box_file_path

    def show_log(self, value, log_level: int = LogLevel.SILENT):
        if log_level <= self.app_log_level:
            print(value, flush=True)

    def show_array(self, value: list, log_level: int = LogLevel.SILENT):
        separator = ' | '
        if log_level <= self.app_log_level:
            from os import get_terminal_size
            t_size = get_terminal_size().columns
            c_size = 0
            # calculate min-widths on all columns
            column_widths: [int] = []
            for idx, row in enumerate(value):
                if isinstance(row, list):
                    for v in range(0, len(row)):
                        str_len: int = len(row[v])
                        if len(column_widths) <= v:
                            column_widths.append(str_len)
                        elif column_widths[v] < str_len:
                            column_widths[v] = str_len

            # Fix last column size so that it doesn't exceed terminal size
            separators_space = (len(column_widths) - 1) * len(separator)
            c_tot_space = sum(column_widths) + separators_space
            if c_tot_space > t_size:
                column_widths[-1] = column_widths[-1] - (c_tot_space - t_size)

            # show result accordingly
            for idx, row in enumerate(value):
                if isinstance(row, list):
                    row_str = row[0].ljust(column_widths[0])
                    last_col_offset = 0
                    for col in range(1, len(row)):
                        # evaluate last column offset
                        last_col_offset = len(row_str) + separators_space
                        row_str += separator + row[col].ljust(column_widths[col])
                    if len(row_str) > t_size:
                        # Result is too long for terminal: split last column content on multiple lines
                        rows = [row_str[i:i + t_size] for i in range(0, len(row_str), t_size)]
                        print(rows[0], flush=True)
                        for r in rows[1:]:
                            print(' ' * last_col_offset + r, flush=True)
                    else:
                        print(row_str, flush=True)
                    if idx == 0:
                        print('-' * t_size, flush=True)
                # single column result - basically not an array
                else:
                    if idx == 0:
                        print(row, flush=True)
                        print('-' * t_size, flush=True)
                    print(row, flush=True)

    def show_info_log(self, value):
        self.show_log(value, LogLevel.INFO)

    def show_debug_log(self, value):
        self.show_log(value, LogLevel.DEBUG)

    def show_color_log(self, color, value, level=LogLevel.SILENT, color_end=Color.END):
        if int(level) <= self.app_log_level:
            print(color + value + color_end, flush=True)

    def show_info_color_log(self, value):
        self.show_color_log(Color.C_BG_BLUE_TXT + Color.C_PALE_WHITE_TXT + Color.EFFECT_ITALIC, value, LogLevel.INFO)

    def show_debug_color_log(self, value):
        self.show_color_log(Color.CYAN_BGD + Color.BLACK_TXT, value, LogLevel.DEBUG)

    def show_critical_log(self, value):
        self.show_color_log(Color.RED_BGD + Color.LIGHT_GRAY_TXT, value)

    def show_help_log(self, value):
        self.show_color_log(Color.YELLOW_BGD + Color.FORCED_BLACK, value)

    def show_title_log(self, value):
        self.show_color_log(Color.OK_GREEN, value, LogLevel.INFO)

    # {1} MUST be user_input placeholder in feedback_text
    def show_input_feedback_log(self, feedback_text, user_input, log_level: int = LogLevel.SILENT):
        self.show_log(feedback_text.replace('{1}', Color.OK_GREEN + user_input + Color.END), log_level)

    # {1} MUST be user_input placeholder in feedback_text
    def show_info_input_feedback_log(self, feedback_text, user_input):
        self.show_input_feedback_log(feedback_text, user_input, LogLevel.INFO)

    # {1} MUST be user_input placeholder in feedback_text
    def show_debug_input_feedback_log(self, feedback_text, user_input):
        self.show_input_feedback_log(feedback_text, user_input, LogLevel.DEBUG)

    def show_command_log(self, command, result=None):
        self.show_input_feedback_log("Command:\n{1}", command if type(command) is str or not isinstance(command, collections.abc.Sequence) else ' '.join(command))
        self.show_log(new_line())
        if result is not None:
            self.show_input_feedback_log("Output:\n{1}", result)

    def show_process_log(self, result: CompletedProcess):
        self.show_command_log(result.args, result.stdout.decode("utf-8") if not isinstance(result.stdout, str) else result.stdout)
        self.show_input_feedback_log('Return code:\n{1}', str(result.returncode))

    def get_log_level(self):
        return self.app_log_level

    def get_log_display(self, app_ini_file: str = 'app.ini'):
        if self.box_file_path is None:
            return LogDisplay(LogLevel.SILENT)
        app_settings: Settings = Settings(get_box_config_ini_file_path(app_ini_file, self.box_file_path))
        try:
            return LogDisplay(app_settings.get_int_setting('SETTINGS', 'LOG_LEVEL'))
        except ParseException:
            print('Invalid log level in app.ini. Defaulting to SILENT.')
            return LogDisplay(LogLevel.SILENT)
