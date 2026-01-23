#!/usr/bin/env python3

from pathlib import PurePath
from subprocess import CompletedProcess

from boxtools.data.Color import ShellColor as Color
import collections.abc

from boxtools.exception.Exceptions import ParseException
from boxtools.data.util.Settings import Settings
from boxtools.data.access.fileAccess import get_box_config_ini_file_path, write_to_file
from boxtools.data.util.stringUtils import new_line


class LogLevel:
    SILENT = 1
    INFO = 2
    DEBUG = 3


class LogDisplay:
    def __init__(self, app_log_level: int = LogLevel.SILENT, box_file_path: PurePath = None):
        self.app_log_level = app_log_level
        if box_file_path is not None:
            self.box_file_path = box_file_path
        else:
            from boxtools.data.access.fileAccess import get_box_path
            self.box_file_path = get_box_path()

    def show_log(self, value, log_level: int = LogLevel.SILENT):
        if log_level <= self.app_log_level:
            print(value, flush=True)

    def show_array(self, value: list, log_level: int = LogLevel.SILENT):
        separator = ' | '
        if log_level <= self.app_log_level:
            from os import get_terminal_size
            try:
                t_size = get_terminal_size().columns
            except OSError as oe:
                self.show_debug_color_log(f'show_array - Error (using 200 as default value) :: \n{oe}')
                t_size = 200
            # calculate min-widths on all columns
            column_widths: list[int] = []
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
        app_settings: Settings = Settings(get_box_config_ini_file_path(app_ini_file))
        try:
            return LogDisplay(app_settings.get_int_setting('SETTINGS', 'LOG_LEVEL'))
        except ParseException:
            print('Invalid log level in app.ini. Defaulting to SILENT.')
            return LogDisplay(LogLevel.SILENT)


def i_info_msg(message: str):
    return f'ℹ️ {message}'

def i_error_msg(message: str):
    return f'❌️ {message}'

def i_warn_msg(message: str):
    return f'⚠️ {message}'

def i_success_msg(message: str):
    return f'✅ {message}'

def i_loading_msg(message: str):
    return f'⏳️ {message}'

def i_gear_msg(message: str):
    return f'⚙️️ {message}'

def print_str_array(str_lst: list[str] = None, a_str_lst: list[list[str]] = None, file_path: str = None,
                    logger: LogDisplay = None):
    if str_lst is None:
        str_lst = []
    if a_str_lst is None:
        a_str_lst = [[]]
    if file_path is not None:
        concat_lst: list[str] = []
        col_size: int = 15
        if len(a_str_lst) > 0:
            for i in range(len(a_str_lst)):
                separator: str = ' | '
                nb_col: int = len(a_str_lst[i])
                separator_spaces: int = (nb_col - 1) * len(separator)
                if i == 1:
                    concat_lst.append('-' * (col_size * nb_col + separator_spaces) + '\n')
                concat_lst.append(separator.join([f"{y:{_get_padding(col_size, x, i)}}" for x, y in enumerate(a_str_lst[i])]))
        f_output = str_lst + concat_lst
        for i in range(len(f_output)):
            if not f_output[i].endswith('\n'):
                f_output[i] += '\n'
        write_to_file(file_path=file_path,
                      content=f_output)

    if logger is not None:
        for line in str_lst:
            logger.show_log(line)
        logger.show_array(a_str_lst)


def _get_padding(col_size: int, column_id: int, line_id: int) -> str:
    return f'^{col_size}' if line_id == 0 else (f'{col_size}' if column_id == 0 else f'>{col_size}')

def object_to_2d_list(obj) -> list[list[str]]:
    return [[k, str(v)] for k, v in vars(obj).items()]