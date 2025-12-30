#!/usr/bin/env python3
import traceback
from datetime import datetime
from pathlib import PurePath

from boxtools.data.util.dateUtils import get_date_str, get_hour_str
from boxtools.data.access.fileAccess import append_to_file


class Logable:
    def __init__(self, log_file_path: str, unit_test_mode: bool = False):
        self.log_file_path: str = log_file_path
        self.unit_test_mode: bool = unit_test_mode

    def log(self, content: str, log_file_path: str = None):
        if self.unit_test_mode:
            print(content)
        else:
            if log_file_path is not None and len(log_file_path.strip()) > 0:
                self.log(f'log -- forced log_file_path :: {log_file_path}')
                append_to_file(log_file_path, content)
            else:
                append_to_file(self.log_file_path, content)

    def log_error(self, error, method_name: str, error_type: str = None, log_file_path: str = None):
        c_error_type: str = ' #{}'.format(error_type) if error_type is not None else ''
        if self.unit_test_mode:
            print('/!\\ Error on {}(){}: {}'.format(method_name, c_error_type, repr(error)))
            print('- Error details: {}'.format(traceback.format_exc()))
        else:
            self.log(content='/!\\ Error on {}(){}: {}'.format(method_name, c_error_type, repr(error)),
                     log_file_path=log_file_path)
            self.log(content='- Error details: {}'.format(traceback.format_exc()),
                     log_file_path=log_file_path)

    def tlog(self, content: str, headers: list = None, log_file_path: str = None):
        f_content: str = '[{}'.format(get_hour_str(datetime.now()))
        for header in headers:
            f_content += ' - {}'.format(header)
        f_content += '] {}'.format(content)
        self.log(content=f_content,
                 log_file_path=log_file_path)

    def change_log_file_path(self, log_file_path: str):
        self.log_file_path = log_file_path

    def get_log_file_path(self):
        return self.log_file_path

    def init_log_file(self, monitoring_type: str, monitoring_folder: str,
                      date: datetime,
                      prefix: str = None,
                      symbol: str = None,
                      suffix: str = None):
        file_name: str = '{}_{}{}_{}{}.log'.format(prefix,
                                                   monitoring_type,
                                                   ('_' + symbol) if symbol is not None and symbol != '' else '',
                                                   get_date_str(date),
                                                   ('_' + suffix) if suffix is not None and suffix != '' else '')
        file_path = self.get_logs_file_path(monitoring_folder, file_name)
        from boxtools.data.access.fileAccess import create_if_not_exists
        create_if_not_exists(file_path)
        return file_path

    def get_logs_file_path(self, log_type: str, file_name: str) -> PurePath:
        pass