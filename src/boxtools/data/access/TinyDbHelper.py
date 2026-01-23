#!/usr/bin/env python3

def str_to_bool(s):
    """Converts `s` to boolean. Assumes `s` is case-insensitive."""
    return s is not None and (s if isinstance(s, bool) else s.lower() in ['true', '1', 't', 'y', 'yes'])
