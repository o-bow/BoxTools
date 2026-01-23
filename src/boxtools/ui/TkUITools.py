#!/usr/bin/env python3

import tkinter as tk

import customtkinter as ctk
from customtkinter import CTkFrame


def build_field(frame, row: int, field_label: str, field_var: tk.StringVar, do_sub_frame: bool = False,
                pad_x: int = 6, pad_y: int = 2, label_sticky: str = 'w', field_sticky: str = 'ew', editable: bool = False,
                colorable: bool = False):
    """
    Creates a label + label/entry combination
    :param editable: entry if True, label otherwise
    :param frame: the root frame
    :param row: the row in the root frame
    :param field_label: the field label
    :param field_var: the field var
    :param do_sub_frame: if true, creates a parent grid sub frame at row index
    :param pad_x: the x padding of both fields
    :param pad_y: the y padding of both fields
    :param field_sticky: the sticky value of the content field
    :param label_sticky: the sticky value of the label field
    :param colorable: uses a CTkFrame as a component so that we can set & toggle a background color to it
    :return the main frame, and the value component
    """
    c_frame = frame
    c_row: int = row
    if do_sub_frame:
        c_frame = ctk.CTkFrame(frame, fg_color=frame.cget("fg_color"))
        c_frame.grid(row=row, column=0, sticky="ew")
        c_frame.columnconfigure(0, weight=1)
        c_row = 0

    ctk.CTkLabel(c_frame, text=field_label).grid(
        row=c_row, column=0, sticky=label_sticky, padx=pad_x, pady=pad_y
    )
    if colorable:
        field = ctk.CTkFrame(c_frame)
        field.grid(
            row=c_row, column=1, sticky=field_sticky
        )
    elif editable:
        field = ctk.CTkEntry(c_frame, textvariable=field_var)
        field.grid(
            row=c_row, column=1, sticky=field_sticky, padx=pad_x, pady=pad_y
        )
    else:
        field = ctk.CTkLabel(c_frame, textvariable=field_var)
        field.grid(
            row=c_row, column=1, sticky=field_sticky, padx=pad_x, pady=pad_y
        )
    return c_frame, field


def create_grid_tab(tab: ctk.CTkFrame, col_1_weight: int = 1, col_2_weight: int = 0) -> tuple[ctk.CTkFrame, ctk.CTkScrollbar]:
    tab.columnconfigure(0, weight=1)
    tab.rowconfigure(0, weight=1)

    container = ctk.CTkFrame(tab)
    container.grid(row=0, column=0, sticky="nsew")

    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=0)

    canvas = tk.Canvas(container,
                       highlightthickness=0,
                       bd=0,
                       relief="flat")
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = ctk.CTkScrollbar(container, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # FILLER (always covers canvas)
    filler_frame = ctk.CTkFrame(
        canvas,
        corner_radius=0
    )

    filler_id = canvas.create_window(
        (0, 0),
        window=filler_frame,
        anchor="nw"
    )

    # CONTENT (Frame inside canvas for actual grid)
    grid_frame = ctk.CTkFrame(canvas,
                              corner_radius=0)
    # Ensure first column stretches
    grid_frame.columnconfigure(0, weight=col_1_weight)
    grid_frame.columnconfigure(1, weight=col_2_weight)

    # grid_frame.configure(style=grid_style_theme)
    window_id = canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox(window_id))

    def on_canvas_configure(event):
        canvas.itemconfigure(filler_id, width=event.width + 1, height=event.height + 1)
        # Stretch the grid_frame to the canvas size. +1 is a hack to avoid 1px wide dirty bars because of window mechanism
        canvas.itemconfigure(window_id, width=event.width + 1)

    grid_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    return grid_frame, scrollbar


def convert_input(value):
    """
    Convert a string from Entry into the appropriate Python type.
    Handles: bool, int, float, str
    """
    val = value.strip()

    # 1️ Boolean check
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False

    # 2️ Try int
    try:
        return int(val)
    except ValueError:
        pass

    # 3️ Try float
    try:
        return float(val)
    except ValueError:
        pass

    # 4️ Default to string
    return val

class YesNoDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Confirm", message="Are you sure?"):
        super().__init__(parent)
        self.result = False

        self.title(title)
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        # Message
        ctk.CTkLabel(self, text=message, wraplength=400, justify="center").pack(padx=20, pady=(20, 10))

        # Buttons
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=(0, 20))

        ctk.CTkButton(frame, text="YES", width=100, command=self._yes).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="NO", width=100, command=self._no).pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self._no)
        self._center(parent)
        self.wait_window()

    def _yes(self):
        self.result = True
        self.destroy()

    def _no(self):
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


def make_view_row(root_view: ctk.CTkFrame, row_idx: int) -> CTkFrame:
    row = ctk.CTkFrame(root_view, fg_color="transparent")
    row.grid(row=row_idx, column=0, sticky="ew", padx=0, pady=0)

    row.grid_columnconfigure(0, weight=1)
    row.grid_columnconfigure(1, weight=0)
    row.grid_columnconfigure(2, weight=0)

    return row

def get_theme_color(kind: str = "fg_color"):
    appearance = ctk.get_appearance_mode()  # "Light" or "Dark"
    base_color_list = ctk.ThemeManager.theme["CTkFrame"][kind]

    if isinstance(base_color_list, list):
        if appearance == "Light":
            base_color = base_color_list[0]
        else:
            base_color = base_color_list[1]
    else:
        base_color = base_color_list
    return base_color

def get_row_zebra_bg_color(root, row_idx: int):
    # Usually the background color for frames in the current theme
    base_color = color_name_to_hex(color_name=get_theme_color(), root=root)
    if row_idx % 2 == 1:
        return adjust_color(base_color, 0.9)
    return base_color

def color_name_to_hex(color_name, root):
    # convert Tk color name like 'gray86' to '#dcdcdc'
    r, g, b = root.winfo_rgb(color_name)
    # winfo_rgb returns 0-65535, scale to 0-255
    r //= 256
    g //= 256
    b //= 256
    return f"#{r:02x}{g:02x}{b:02x}"

def adjust_color(hex_color, factor=0.9):
    """
    Darken/lighten a hex color by factor
    factor < 1 → darker, factor > 1 → lighter
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))

    return f"#{r:02x}{g:02x}{b:02x}"