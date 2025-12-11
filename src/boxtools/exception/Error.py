#!/usr/bin/env python3
from typing import Type


class ToolboxException(Exception):
    """Base class for exceptions in this module."""
    pass


class InputException(ToolboxException):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message: str):
        self.expression = expression
        self.message = message


class GitException(ToolboxException):
    """Raised when a git operation failed.

    Attributes:
        log -- operation log to be shown (default: None
        message -- user explanation on what's failing
    """

    def __init__(self, log, message: str):
        self.log = log
        self.message = message


class CoreException(Exception):
    """Raised when a core operation failed.

    Attributes:
        message -- user explanation on what's failing
        error -- original Exception if any
    """

    def __init__(self, message: str, error: Type[Exception]):
        self.message = message
        self.error = error


class UnreachableException(Exception):
    """Raised when a parse operation failed.

    Attributes:
        message -- user explanation on what's failing
        error -- original Exception if any
    """

    def __init__(self, message: str):
        self.message = message
