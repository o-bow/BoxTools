#!/usr/bin/env python3

import tkinter as tk
from abc import abstractmethod

from boxtools.dto.Exceptions import ParseException
from boxtools.ui.UiTools import *
from boxtools.dto.FieldDto import FieldDto
from boxtools.ui.VerticalScrollableFrame import VerticalScrollableFrame


def get_label_from_key(key):
    return key.replace('_', ' ')


class IniEditor(tk.Frame):
    settings_entries = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)

        self.show_title_frame(self.get_section_name())
        self.show_settings_frame(self.get_section_name())
        self.rowconfigure(1, weight=1)
        self.show_save_action_frame()

    @abstractmethod
    def get_section_name(self):
        pass

    @abstractmethod
    def get_settings(self):
        pass

    @abstractmethod
    def get_desc_for_key(self, key):
        pass

    @abstractmethod
    def back_command(self):
        pass

    @abstractmethod
    def get_title_font(self):
        pass

    def show_title_frame(self, section_name):
        title_frame = Frame(self)
        title_frame.grid(row=0, column=0, sticky=N + W + E)
        label = tk.Label(title_frame, text=section_name + " settings", font=self.get_title_font())
        label.pack(side="top", fill="none", pady=10)

    def get_scrollable_canvas(self):
        s_view = VerticalScrollableFrame(self)
        s_view.grid(row=1, column=0, sticky="nswe")
        return s_view

    def show_settings_frame(self, section_name):
        user_settings = self.get_settings()
        s_view = self.get_scrollable_canvas()
        # Parent widget for the buttons
        settings_frame = s_view.get_frame()
        settings_frame.grid(row=0, column=0, sticky="nsew")
        pack_layout = PackLayout(settings_frame)
        fields = []
        for key, value in user_settings.get_section(section_name).items():
            setting_desc = ""
            try:
                setting_desc = self.get_desc_for_key(key)
            except ParseException:
                "*No description (" + section_name + "." + key + ")*"
            fields.append(FieldDto(get_label_from_key(key), value, user_settings, section_name, key,
                                   setting_desc))
        self.settings_entries = pack_layout.make_form(fields)
        s_view.create()

    def save_settings(self):
        for entry in self.settings_entries:
            field = entry[0]
            value = entry[1].get() if callable(getattr(entry[1], "get", None)) else str('selected' in entry[1].state())
            if field.settings_instance:
                settings = field.settings_instance
                settings.apply_single_setting_change(field.property_section, field.property_name, value)

    def show_save_action_frame(self):
        buttons_frame = Frame(self)
        buttons_frame.grid(row=2, column=0, padx=10, pady=10,
                           sticky=E + W + N + S)
        home_button = tk.Button(buttons_frame, text="Cancel",
                                command=lambda: self.back_command())
        save_button = tk.Button(buttons_frame, text="Save",
                                command=lambda: self.save_settings())
        save_button.pack(in_=buttons_frame, side=RIGHT)
        home_button.pack(in_=buttons_frame, side=RIGHT)
