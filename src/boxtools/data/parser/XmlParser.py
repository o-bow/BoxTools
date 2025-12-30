#!/usr/bin/env python3

from xml.etree.ElementTree import ParseError, Element, fromstring, tostring, indent
from boxtools.Logs import LogDisplay


class XmlParser:
    def __init__(self):
        self.logger: LogDisplay = LogDisplay().get_log_display()

    def parse(self, sql: str)-> Element | None:
        self.logger.show_debug_log(' - Parsing SQL: {}'.format(sql))
        try:
            return fromstring(sql.strip())
        except ParseError as e:
            self.logger.show_log('')
            self.logger.show_critical_log(' => Error while parsing SQL (1): {}'.format(str(e)))
            self.logger.show_log('')
            return None

    def format(self, sql: str, do_print: bool = True)->str:
        statement: Element = self.parse(sql)
        if statement is None:
            return ''
        indent(statement)
        output: str = tostring(statement, encoding='unicode', method='xml')
        if do_print:
            self.logger.show_command_log(output)
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
        pyperclip.copy(formatted)
        if show_result:
            self.logger.show_command_log(' - Formatted SQL copied to clipboard')
        return formatted