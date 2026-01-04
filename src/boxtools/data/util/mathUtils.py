#!/usr/bin/env python3
from math import ceil, floor
from decimal import Decimal


def round_decimals_up(number: float, decimals: int = 2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return ceil(number)

    factor = 10 ** decimals
    return ceil(number * factor) / factor


def round_decimals_down(number: float, decimals: int = 2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return floor(number)

    factor = 10 ** decimals
    return floor(number * factor) / factor


def get_decimal_places(number: float) -> int:
    exp = Decimal(str(number)).as_tuple().exponent
    return -exp if exp < 0 else 0


def format_number_suffix(value: float, right_align: bool = True) -> str:
    """
    Format a number with single-character suffixes (K, M, G, T, etc.).
    - At most 1 decimal
    - Optional right-align (width 5)
    """
    suffixes = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    num = abs(value)
    sign = '-' if value < 0 else ''

    index = 0
    while index + 1 < len(suffixes) and num >= 1000 ** (index + 1):
        index += 1

    factor = 1000 ** index
    display_num = num / factor

    # Round to at most 1 decimal
    if display_num >= 10:
        display_num = int(round(display_num))
    else:
        display_num = round(display_num, 1)

    # Promote suffix if rounding reaches 1000
    if display_num >= 1000 and index + 1 < len(suffixes):
        display_num /= 1000
        index += 1

        # Round again if necessary
        if display_num >= 10:
            display_num = int(round(display_num))
        else:
            display_num = round(display_num, 1)

    # Convert to string
    if display_num % 1 == 0:
        display_str = str(int(display_num))
    else:
        display_str = str(display_num)

    result = f"{sign}{display_str}{suffixes[index]}"

    if right_align:
        result = result.rjust(5)

    return result
