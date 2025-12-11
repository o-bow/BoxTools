#!/usr/bin/env python3
from typing import List

import sqlparse
from sqlparse.sql import Statement
from boxtools.Logs import LogDisplay, LogLevel

class SqlParser:
    def __init__(self, app_log_level: int = LogLevel.SILENT):
        self.logger: LogDisplay = LogDisplay().get_log_display()

    def parse(self, sql: str)->List[Statement]:
        self.logger.show_debug_log(' - Parsing SQL: {}'.format(sql))
        try:
            return sqlparse.parse(sql.strip())
        except TypeError as e:
            self.logger.show_log('')
            self.logger.show_critical_log(' => Error while parsing SQL (1): {}'.format(str(e)))
            self.logger.show_log('')
            return []


    def format(self, sql: str, do_print: bool = True)->List[str]:
        statements: List[Statement] = self.parse(sql)
        if statements is None:
            return []
        if len(statements) <= 0:
            self.logger.show_critical_log(' => No SQL statement found')
        output: List[str] = []
        for statement in statements:
            s_statement = sqlparse.format(str(statement), reindent=True, keyword_case='upper')
            output.append(s_statement)
            if do_print:
                self.logger.show_command_log(s_statement)
        return output

    def memory_format(self, show_result: bool = True):
        import pyperclip
        clipboard_content = pyperclip.paste()
        try:
            formatted = self.format(clipboard_content, show_result)
        except TypeError as e:
            self.logger.show_log('')
            self.logger.show_critical_log(' => Error while parsing SQL (2): {}'.format(str(e)))
            self.logger.show_log('')
            return None
        output: str = '\n'.join(formatted)
        pyperclip.copy(output)
        if show_result:
            self.logger.show_command_log(' - Formatted SQL copied to clipboard')
        return output

