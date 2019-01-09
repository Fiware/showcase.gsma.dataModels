#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Converts an NGSI v2 Simplified Representation (a.k.a. keyValues)
into a Normalized Representation

Copyright (c) 2018 FIWARE Foundation e.V.

Author: José Manuel Cantera

"""

import sys
import json
import ntpath

from entity_print import print_json_string


def keyValues_2_normalized(entity):
    out = {}

    for key in entity:
        if key == 'id' or key == 'type':
            out[key] = entity[key]
            continue

        out[key] = {
            'value': entity[key]
        }

        if key == 'location':
            out[key]['type'] = 'geo:json'

        if key.startswith('date'):
            out[key]['type'] = 'DateTime'

        if key == 'address':
            out[key]['type'] = 'PostalAddress'

        if key.startswith('ref'):
            out[key]['type'] = 'Relationship'

        if key.startswith('has'):
            out[key]['type'] = 'Relationship'

    return out


def read_json(infile):
    with open(infile) as data_file:
        data = json.loads(data_file.read())

    return data


def write_json(data, outfile):
    with open(outfile, 'w') as data_file:
        data_file.write(print_json_string(data))
        data_file.write("\n")


def main(args):
    data = read_json(args[1])
    result = keyValues_2_normalized(data)
    file_name = ntpath.basename(args[1])
    write_json(result, 'example-normalized.json')


if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: keyvalues2Normalized [file]")
        exit(-1)

    main(sys.argv)
