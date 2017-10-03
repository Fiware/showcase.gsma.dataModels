# -*- coding: utf-8 -*-


def parse(ngsi_obj):
    out = []
    if 'contextResponses' in ngsi_obj:
        responses = ngsi_obj['contextResponses']
        for response in responses:
            element = response['contextElement']
            attributes = element['attributes']
            out.append({
                'id': element['id'],
                'location': {
                    'type': 'geo:point',
                    'value': attributes[0]['value']
                }
            })

    return out
