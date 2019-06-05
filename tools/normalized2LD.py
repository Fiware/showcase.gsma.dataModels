#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Converts an NGSI v2 Normalized Representation 
into an NGSI-LD Representation

Copyright (c) 2018 FIWARE Foundation e.V.

Author: José Manuel Cantera

"""

import sys
import json

from rfc3987 import parse
from entity_print import print_json_string

ld_context = 'https://fiware.github.io/dataModels/ldContext/fiware-ld-context.jsonld'


def ngsild_uri(type_part, id_part):
    template = 'urn:ngsi-ld:{}:{}'

    return template.format(type_part, id_part)


# Generates an Entity Id as a URI
def ld_id(entity_id, entity_type):
    out = entity_id
    try:
        d = parse(entity_id, rule='URI')
        if d['authority'] is None:
            out = ngsild_uri(entity_type, entity_id)
    except ValueError:
        out = ngsild_uri(entity_type, entity_id)

    return out


# Generates a Relationship's object as a URI
def ld_object(attribute_name, entity_id):
    out = entity_id
    try:
        d = parse(entity_id, rule='URI')
    except ValueError:
        entity_type = ''
        if attribute_name.startswith('ref'):
            entity_type = attribute_name[3:]

        out = ngsild_uri(entity_type, entity_id)

    return out


# Do all the transformation work
def normalized_2_LD(entity):
    out = {
        '@context': ld_context
    }

    for key in entity:
        if key == 'id':
            out[key] = ld_id(entity['id'], entity['type'])
            continue

        if key == 'type':
            out[key] = entity[key]
            continue

        attr = entity[key]
        out[key] = {}
        ld_attr = out[key]

        if not('type' in attr) or attr['type'] != 'Relationship':
            ld_attr['type'] = 'Property'
            ld_attr['value'] = attr['value']
        else:
            ld_attr['type'] = 'Relationship'
            ld_attr['object'] = ld_object(key, attr['value'])

        if key == 'location':
            ld_attr['type'] = 'GeoProperty'

        if 'type' in attr and attr['type'] == 'DateTime':
            ld_attr['value'] = {
                '@type': 'DateTime',
                '@value': attr['value']
            }

        if 'type' in attr and attr['type'] == 'PostalAddress':
            ld_attr['value']['type'] = 'PostalAddress'

        if 'metadata' in attr:
            metadata = attr['metadata']

            for mkey in metadata:
                if mkey == 'timestamp':
                    ld_attr['observedAt'] = metadata[mkey]['value']
                elif mkey == 'unitCode':
                    ld_attr['unitCode'] = metadata[mkey]['value']
                else:
                    sub_attr = {}
                    # Metadata which are Relationships is assumed not to be there
                    sub_attr['type'] = 'Property'
                    sub_attr['value'] = metadata[mkey]['value']
                    ld_attr[mkey] = sub_attr

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
    result = normalized_2_LD(data)
    write_json(result, 'example-LD.jsonld')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: normalized2LD [file]")
        exit(-1)

    main(sys.argv)
