#!/usr/bin/env python3
from boxtools.Logs import LogDisplay, LogLevel
from boxtools.dto.HelpEntry import HelpEntry
from boxtools.stringUtils import new_line


class Help:
    def __init__(self, app_log_level: int = LogLevel.SILENT):
        self.logger: LogDisplay = LogDisplay(app_log_level=app_log_level).get_log_display()
        self.entries : list[HelpEntry] = []
        self.groups : list[str] = []

    def add_entry(self, group, names, description, usage, additional_informations):
        self.entries.append(HelpEntry(group, names, description, usage, additional_informations))

    def _build_groups(self):
        self.groups = []
        for entry in self.entries:
            if entry.help_entry_group not in self.groups:
                self.groups.append(entry.help_entry_group)

    def get_help_string(self):
        self.logger.show_debug_log(' - building groups')
        self._build_groups()
        output: str = ''
        indent: str = ' '
        # Add header to output
        output += new_line()
        output += '# Help'
        output += new_line()
        self.logger.show_debug_log(' - iterating over groups (' + str(len(self.groups)) + ')')
        for group in self.groups:
            output += new_line()
            self.logger.show_debug_log(' - group: ' + group)
            # Group name
            output += '[' + group + ']'
            # Group content
            self.logger.show_debug_log('  - iterating over filtered entries of group: ' + group)
            for entry in filter(lambda e: e.help_entry_group is group, self.entries):
                self.logger.show_debug_log('   - entry: ' + str(entry.help_entry_names))
                output += entry.get_text(indent)
            self.logger.show_debug_log('  - end of iteration')
            output += new_line()
        return output