#!/usr/bin/env python3
from collections.abc import Sequence

from boxtools.Logs import LogDisplay
from boxtools.stringUtils import new_line


class HelpEntry:
    def __init__(self, group, names, description, usage, additional_informations):
        self.logger: LogDisplay = LogDisplay().get_log_display()
        self.help_entry_group = group
        self.help_entry_names = names
        self.help_entry_description = description
        self.help_entry_usage = usage
        self.help_entry_additional_information = additional_informations

    def get_text(self, indent: str):
        output: str = ''

        # Name
        output += new_line()
        if self._is_array(self.help_entry_names):
            output += indent + '- ' + self._array_to_str(self.help_entry_names)
        else:
            output += indent + '- ' + str(self.help_entry_names)
        output += ': '

        # description
        output += self.help_entry_description

        # usage
        if self.help_entry_usage is not None:
            output += new_line()
            output += indent + '  ~> usage: ' + self.help_entry_usage

        # additional information
        if self.help_entry_additional_information is not None:
            if self._is_array(self.help_entry_additional_information):
                self.logger.show_debug_log('    --> additional info detected ')
                for ai in self.help_entry_additional_information:
                    self.logger.show_debug_log('    --> additional info: ' + ai)
                    output += new_line()
                    output += indent + '  -> ' + ai
            else:
                self.logger.show_debug_log('    --> additional info not detected ' + str(self.help_entry_additional_information))
                output += new_line()
                output += indent + '  -> ' + str(self.help_entry_additional_information)
        #self.logger.show_debug_log('     ---> entry: \n ' + output + '\n')
        return output

    @staticmethod
    def _array_to_str(iterable):
        return " | ".join(iterable)

    @staticmethod
    def _is_array(value):
        return type(value) is not str and isinstance(value, Sequence)
