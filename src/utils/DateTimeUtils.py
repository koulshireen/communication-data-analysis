import datetime
import math

from dateutil import parser


def convert_string_date(date):
    date = parser.parse(date)
    return date


def off_working_hours_deviation(date):
    start_time = datetime.time(8, 0, 0)
    stop_time = datetime.time(18, 0, 0)
    time = date.time()
    ref_date = datetime.date(1, 1, 1)
    combined_time = datetime.datetime.combine(ref_date, time)
    combined_start_time = datetime.datetime.combine(ref_date, start_time)
    combined_stop_time = datetime.datetime.combine(ref_date, stop_time)
    if time < start_time:
        return math.ceil((combined_time - combined_start_time).total_seconds() / 3600)
    if time > stop_time:
        return math.ceil((combined_stop_time - combined_time).total_seconds() / 3600)
    return 0
