#!/usr/bin/env python3

def upper_first_letter(text: str):
    return text[0:1].upper() + text[1:]

def lower_first_letter(text: str):
    return text[0:1].lower() + text[1:]

def concat_str_list(to_add: list, host: list):
    for line in to_add:
        host.append(line)

def new_line():
    return '\n'

def none_or_empty(value):
    return value is None or value == ''

def none_safe(value):
    return None if value == 'None' else value

def bool_safe(value):
    return False if (value != True and value != 'True' and value != 'true') else True

