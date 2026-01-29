#!/usr/bin/env python3

import base64

def str_to_b64(input_str: str) -> str:
    """Encode a string to a base64 string.

    Args:
        input_str (str): The input string to be encoded.

    Returns:
        str: The base64 encoded string.
    """
    return base64.b64encode(input_str.encode('utf-8')).decode('utf-8')

def file_to_b64(file_path: str) -> str:
    """Encode the content of a file to a base64 string.

    Args:
        file_path (str): The path to the file to be encoded.

    Returns:
        str: The base64 encoded string of the file content.
    """
    with open(file_path, 'rb') as f:
        b64_content = base64.b64encode(f.read()).decode('utf-8')
    return b64_content