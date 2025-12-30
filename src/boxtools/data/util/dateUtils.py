#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

"""
Date utility functions
"""


def month_range(start_date, duration_in_months):
    start_date_obj = datetime.strptime(start_date, '%m-%Y')
    return pd.date_range(start_date_obj, start_date_obj + pd.DateOffset(months=int(duration_in_months)),
                         freq='MS').strftime("%Y-%m").tolist()


def month_date_to_date_month_format(date):
    return format_switcher(date, '%Y-%m', '%m-%Y')


def date_month_to_month_date_format(date):
    return format_switcher(date, '%m-%Y', '%Y-%m')


def format_switcher(date, src_format, output_format):
    date_obj = datetime.strptime(date, src_format)
    return date_obj.strftime(output_format)


def next_month_date(start_date):
    return start_date + pd.DateOffset(months=1)


def day_count(start_date, end_date):
    return (end_date - start_date).days


# yyyy/mm/dd HH:MM:SS
def full_date_format(date):
    return date.strftime("%Y/%m/%d %H:%M:%S")


def add_years(date, nb_years):
    return date + pd.DateOffset(months=int(nb_years*12))


def today_minus_n_months(nb_minus):
    return datetime.now() - relativedelta(months=12)

