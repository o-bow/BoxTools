#!/usr/bin/env python3
import pyperclip

def clipboard_read() -> str:
    return pyperclip.paste()

def clipboard_write(value: str) -> str:
    return pyperclip.copy(value)