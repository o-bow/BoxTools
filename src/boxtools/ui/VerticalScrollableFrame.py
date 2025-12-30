#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

from boxtools.env.environment import is_windows


class VerticalScrollableFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'scrollable_frame' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create frame id property
        self.scrollable_frame_id = None

        # Create a canvas object and a vertical scrollbar for scrolling it.
        v_scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        v_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        v_scrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.scrollable_frame = scrollable_frame = ttk.Frame(self.canvas)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_scrollable_frame(event):
            # Update the scrollbars to match the size of the inner frame.
            size_tuple = (0, 0, scrollable_frame.winfo_reqwidth(), scrollable_frame.winfo_reqheight())
            self.canvas.config(scrollregion=size_tuple)
            if scrollable_frame.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=scrollable_frame.winfo_reqwidth())

        scrollable_frame.bind('<Configure>', _configure_scrollable_frame)

        def _configure_canvas(event):
            if self.scrollable_frame.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(self.scrollable_frame_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

    def create(self):
        self.scrollable_frame_id = self.canvas.create_window(0, 0, window=self.scrollable_frame,
                                                             anchor=NW, tags="self.scrollable_frame")

    def get_frame(self):
        return self.scrollable_frame

    def _on_mousewheel(self, event):
        delta = (event.delta/120) if is_windows() else event.delta
        self.canvas.yview_scroll(-1 * delta, "units")

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
