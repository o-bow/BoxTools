#!/usr/bin/env python3

import base64

def to_b64(file_path: str) -> str:
    """Encode the content of a file to a base64 string.

    Args:
        file_path (str): The path to the file to be encoded.

    Returns:
        str: The base64 encoded string of the file content.
    """
    with open(file_path, 'rb') as f:
        b64_content = base64.b64encode(f.read()).decode('utf-8')
    return b64_content