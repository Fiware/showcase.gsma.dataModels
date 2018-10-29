# -*- coding: utf-8 -*-
"""

Serializes an NGSI Entity into JSON ordering the fields properly

Copyright (c) 2018 FIWARE Foundation e.V.

Author: José Manuel Cantera

"""

import json
from copy import deepcopy

# Prints the JSON string but with the proper member order


def print_json_string(entity):
    entity_only_id = {
        'id': entity['id'],
    }

    out = json.dumps(entity_only_id, indent=4)[:-2]

    entity_only_type = {
        'type': entity['type'],
    }

    # with -2 it is removed the new line char as well
    out += "," + json.dumps(entity_only_type, indent=4)[1:-2]

    entity_cloned = deepcopy(entity)

    del entity_cloned['id']
    del entity_cloned['type']
    if '@context' in entity_cloned:
        del entity_cloned['@context']

    # Now the rest of the entity without the '@context
    out += "," + json.dumps(entity_cloned, indent=4)[1:-2]

    # Last go the '@context'
    if '@context' in entity:
        only_ld_context = {
            '@context': entity['@context']
        }

        out += "," + json.dumps(only_ld_context, indent=4)[1:]
    else:
        out += "\n}"

    return out
