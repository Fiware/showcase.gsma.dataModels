# -*- coding: utf-8 -*-


def element_dict(response):
    elelment = response['contextElement']
    return {'id': element['id'],
            'location': {
                'type': 'geo:point',
                'value': element['attributes'][0]['value']}}


def parse(ngsi_obj):
    return [element_dict(response) for response
            in ngsi_obj.get('contextResponses', [])]
