#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from typing import List

from boxtools.Color import ShellColor
from boxtools.dto.FieldDto import FieldDto
from boxtools.Logs import LogDisplay


class GridLayout:
    def __init__(self, frame):
        self.frame = frame

    def show_action_feature(self, action_title, action_row: int, action_command, description=None) -> int:
        Label(self.frame, text=action_title).grid(row=action_row, column=0, sticky=W, padx=5)
        if description:
            action_row = action_row + 1
            Label(self.frame, text=description).grid(row=action_row, column=0, columnspan=2, sticky=W, padx=10)
        button = Button(self.frame, text='Run', width=15, command=action_command)
        button.grid(row=action_row, column=1, sticky=E, padx=5)
        return action_row + 1

    def show_input_feature(self, action_title, action_row: int, default_value=None, description=None) -> int:
        Label(self.frame, text=action_title).grid(row=action_row, column=0, sticky=W, padx=5)
        if description:
            action_row = action_row + 1
            Label(self.frame, text=description).grid(row=action_row, column=0, columnspan=2, sticky=W, padx=10)
        entry = Entry(self.frame)
        entry.grid(row=action_row, column=1, sticky=E, padx=5)
        if default_value:
            entry.insert(len(str(default_value)), default_value)
        return action_row + 1

    def show_separator(self, action_row: int, colspan=None) -> int:
        separator = Canvas(self.frame, width=80, height=20)
        separator.create_line(0, 10, 80, 10)
        if colspan:
            separator.grid(row=action_row, columnspan=colspan)
        else:
            separator.grid(row=action_row, column=0, sticky=W, padx=10)
        return action_row + 1

    def show_title(self, title_text, title_font, action_row: int) -> int:
        Label(self.frame, text=title_text, font=title_font).grid(row=action_row, columnspan=2, sticky=S, padx=5, pady=5)
        return action_row + 1


class PackLayout:
    def __init__(self, root):
        self.root = root

    def show_input_feature(self, action_title, default_value=None, description=None):
        input_frame = Frame(self.root)
        label = Label(input_frame, width=15, text=action_title, anchor='w')
        input_frame.pack(side=TOP, fill=X, padx=5, pady=5)
        is_checkbox = False
        if default_value in ('True', 'False'):
            entry = ttk.Checkbutton(input_frame, onvalue=True, offvalue=False)
            entry.state(['selected' if default_value == 'True' else '!alternate'])
        else:
            entry = Entry(input_frame)
            entry.insert(len(str(default_value)), default_value)
        if description:
            desc_frame = Frame(input_frame)
            desc_frame.pack(side=BOTTOM, fill=X, pady=5)
            desc = Label(desc_frame, text=' => ' + description)
            desc.pack(side=LEFT)
        label.pack(side=LEFT)
        entry.pack(side=RIGHT, expand=YES, fill=X)
        return entry

    def make_form(self, fields: List[FieldDto]):
        entries = []
        for field in fields:
            entries.append((field, self.show_input_feature(field.label, field.value, field.description)))
        return entries


def strip_colours(text, log_level):
    log: LogDisplay = LogDisplay().get_log_display()
    color_vars = vars(ShellColor)
    for color_name, color in color_vars.items():
        if not color_name.startswith('__'):
            if color in text:
                log.show_debug_log('color found: ' + color + ' (' + color_name + ')')
                text = text.replace(color, '')
    log.show_debug_log('\ntext: ' + text)
    return text
