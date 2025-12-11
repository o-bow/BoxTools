#!/usr/bin/env python3
from typing import Type


class LibException(Exception):
    """Base class for exceptions in this module."""
    pass


class ParseException(Exception):
    """Raised when a parse operation failed.

    Attributes:
        message -- user explanation on what's failing
        error -- original Exception if any
    """

    def __init__(self, message: str):
        self.message = message