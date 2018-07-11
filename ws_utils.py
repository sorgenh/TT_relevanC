import sys
from datetime import datetime

SEPARATEUR="|"


def check_header(schema, header):
    header_tab = header.split(SEPARATEUR)
    if len(schema) != len(header_tab):
        return False
    for i in range(len(schema)):
        if list(schema.keys())[i] != header_tab[i]:
            return False
    return True


def get_header(schema):
    return SEPARATEUR.join(schema.keys())


def check_line(schema, line):
    line_tab = line.split(SEPARATEUR)
    if len(schema) != len(line_tab):
        return False
    for i in range(len(schema)):
        if not check_type(list(schema.values())[i], line_tab[i]):
            return False
    return True


def check_type(type_to_check, data):
    return getattr(sys.modules[__name__], 'check_type_'+type_to_check)(data)


def check_type_string(data):
    return data != ""


def check_type_int(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def check_type_date(data):
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False
