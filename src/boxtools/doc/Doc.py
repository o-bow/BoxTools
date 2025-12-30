#!/usr/bin/env python3

from configparser import ConfigParser

from boxtools.Logs import LogDisplay

"""
Class to display documentation out of configuration files (ini)
"""
class Doc:
    def __init__(self):
        self.logger: LogDisplay = LogDisplay().get_log_display()

    def show_fields(self, properties: ConfigParser):
        self.show_filtered_fields(properties, None, None)


    def show_filtered_fields(self, properties: ConfigParser, filter_column: str|None, filter_value: str|None):
        self.logger.show_debug_log(' - filter: ' + str(filter_column) + ' = ' + str(filter_value))
        sections = properties.sections()
        if len(sections) == 0 or filter_column is not None and len(sections) == 1:
            self.logger.show_log("No properties found in the file")
            return
        properties_names = properties[sections[0]]
        if filter_column is not None:
            sections.remove(filter_column)
        output_array = [sections]
        for k in properties_names:
            if filter_column is not None and properties[filter_column][k].lower() != filter_value:
                self.logger.show_debug_log(' - skipping ' + k)
                self.logger.show_debug_log('')
                continue
            new_row = []
            for section in sections:
                new_row.append(properties[section][k])
            output_array.append(new_row)
        self.logger.show_array(output_array)