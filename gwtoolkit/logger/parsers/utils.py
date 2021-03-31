import csv
import hashlib
from io import StringIO

from dateutil import parser


def get_datetime(row, mappings):
    datetime = do_get(row, mappings, "datetime")
    date = do_get(row, mappings, "date")
    time = do_get(row, mappings, "time")

    if not datetime and not date:
        raise Exception("Must contain either either datetime fields or date and time fields")
    if date:
        date = str(date).split()[0]  # TODO FIX
    if not datetime:
        if time:
            date = f"{date} {time}"
        datetime = date
    return parser.parse(str(datetime))


def do_get(row, mappings, key):
    col = mappings.get(key)
    if col and col != 'undefined':  #TODO fix data flow
        return getattr(row, col)

def get_float(row, mappings, key):
    col = mappings.get(key)
    if col and col != 'undefined':
        return float(getattr(row, col))

def get_csv_reader(f, header_row):
    for _ in range(header_row - 1):
        f.readline()
    decoded = StringIO(f.read().decode())
    return csv.DictReader(decoded)

def md5(f):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()