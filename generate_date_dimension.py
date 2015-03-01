#!/usr/bin/env python

import argparse
import datetime
from date_dimension import DateDimension


def iterate_calendar(start, end):
    curr = start
    one_day = datetime.timedelta(days=1)
    while curr < end:
        curr += one_day
        yield curr


def generate_date_dimension(start, end):
    e = {
        'year_number_in_epoch': 0,
        'half_number_in_epoch': 0,
        'quarter_number_in_epoch': 0,
        'month_number_in_epoch': 0,
        'week_number_in_epoch': 0,
        'day_number_in_epoch': 0,
    }
    prev_date_dim = DateDimension(start)
    for d in iterate_calendar(start, end):
        date_dim = DateDimension(d)
        if date_dim.columns['year_key'] != prev_date_dim.columns['year_key']:
            e['year_number_in_epoch'] += 1
        if date_dim.columns['half_number_in_year'] != prev_date_dim.columns['half_number_in_year']:
            e['half_number_in_epoch'] += 1
        if date_dim.columns['quarter_number_in_year'] != prev_date_dim.columns['quarter_number_in_year']:
            e['quarter_number_in_epoch'] += 1
        if date_dim.columns['month_number_in_year'] != prev_date_dim.columns['month_number_in_year']:
            e['month_number_in_epoch'] += 1
        if date_dim.columns['week_number_in_year'] != prev_date_dim.columns['week_number_in_year']:
            e['week_number_in_epoch'] += 1
        if date_dim.columns['day_number_in_year'] != prev_date_dim.columns['day_number_in_year']:
            e['day_number_in_epoch'] += 1
        for k in e.keys():
            date_dim.columns[k] = e[k]
        prev_date_dim = date_dim
        yield date_dim


def valid_date(s):
    try:
        dt = datetime.datetime.strptime(s, "%Y-%m-%d")
        return dt.date()
    except ValueError:
        msg = "invalid date: '{0}'".format(s)
        raise argparse.ArgumentTypeError(msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a date dimension schema and insertion script.')
    parser.add_argument('start_date', metavar='D', type=valid_date,
                        help='Epoch date for the generated dimension (yyyy-mm-dd format)')
    parser.add_argument('-e', '--end-date', type=valid_date, default='2020-12-31',
                        help='End date for generated dimension (yyyy-mm-dd format)')
    parser.add_argument('-o', '--output-file', type=argparse.FileType('w'), default='date_dimension_inserts.sql',
                        help='Output destination for the INSERT script')

    args = parser.parse_args()

    with args.output_file as out:
       for dim in generate_date_dimension(args.start_date, args.end_date):
           out.write(dim.generate_insert_statement())
