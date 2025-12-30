#!/usr/bin/env python3

class FieldDto:
    def __init__(self, label, value, settings_instance=None, property_section=None, property_name=None,
                 description=None):
        self.label = label
        self.value = value
        self.settings_instance = settings_instance
        self.property_section = property_section
        self.property_name = property_name
        self.description = description
