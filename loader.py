# Data loader.

import csv
import datetime

WARD6 = 'ward6.csv'
ALL_WARDS = 'all_wards.csv'


def read_csv(filename):
    """Read a CSV file into a list of lists."""
    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]


def to_dicts(csv_data):
    """Convert list of lists CSV representation to dicts."""
    names = csv_data[0]
    return [{n: v for n, v in zip(names, values)} for values in csv_data[1:]]


def try_type(type, values):
    try:
        for value in values:
            type(value)
        return True
    except ValueError:
        return False


def detect_type(values):
    partint = lambda v: int(v) if v else 0
    date = lambda v: datetime.datetime.strptime(v, '%d/%m/%Y')

    for type in [int, float, partint, date]:
        if try_type(type, values):
            return type

    return lambda v: v


def detect_types(dicts):
    return {name: detect_type([d[name] for d in dicts])
        for name in dicts[0].keys()}


def convert_types(dicts):
    types = detect_types(dicts)
    return [{name: types[name](value) for name, value in d.items()}
        for d in dicts]


def is_broken(d):
    return any(type(value) in [int, float] and value < 0
            for value in d.values())


def filter_broken(dicts):
    return [d for d in dicts if not is_broken(d)]
