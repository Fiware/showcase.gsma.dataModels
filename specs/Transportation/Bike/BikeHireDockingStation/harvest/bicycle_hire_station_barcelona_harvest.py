#!bin/python
# -*- coding: utf-8 -*-

"""
Harmonises data from the city of Barcelona corresponding to
the bicycle hiring stations
"""

from __future__ import print_function
import contextlib
import json
from datetime import datetime
from pytz import timezone
import re
try:                 # Python 3
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:  # Python 2
    from urllib2 import Request, URLError, urlopen


# Origin of the Data (Barcelona's open data)
SOURCE = 'http://wservice.viabicing.cat/v2/stations'

status_dictionary = {
    'OPN': 'working',
    'CLS': 'outOfService'
}

barcelona_tz = timezone('CET')

MIME_JSON = 'application/json'
FIWARE_SERVICE = 'Bicycle'
FIWARE_SERVICE_PATH = "/Barcelona"

DATA_BROKER = 'http://localhost:1026'

"""
See
# http://fiware-datamodels.readthedocs.io/en/latest/
Transportation/Bike/BikeHireDockingStation/doc/spec/index.html
"""

BIKE_STATION_TYPE = 'BikeHireDockingStation'

# Sanitize string to avoid forbidden characters by the Orion Broker


def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;-]", "", str_in)


# Reads the data from the data source and returns a dictionary
def read_data(source):
    req = Request(url=source)
    f = None
    try:
        with contextlib.closing(urlopen(req)) as f:
            json_data = f.read()
            return json_data
    except URLError as e:
        print('Error while calling: %s : %s' % (source, e))
        return None


# Harmonise the station data
def harmonize_station(station_data):
    out = {
        'type': BIKE_STATION_TYPE,
        'id': 'Bcn-BikeHireDockingStation-' + station_data['id'],
        'freeSlotNumber': {
            'type': 'Number',
            'value': int(station_data['slots'])
        },
        'availableBikeNumber': {
            'type': 'Number',
            'value': int(station_data['bikes'])
        },
        'address': {
            'type': 'PostalAddress',
            'value': {
                'addressCountry': 'ES',
                'addressLocality': 'Barcelona',
                'streetAddress': sanitize(station_data['streetName'] +
                                          ',' + station_data['streetNumber'])
            }
        },
        'location': {
            'type': 'geo:json',
            'value': {
                'type': 'Point',
                'coordinates': [
                    float(station_data['longitude']),
                    float(station_data['latitude']),
                    float(station_data['altitude'])
                ]
            }
        },
        'status': {
            'type': 'Text',
            'value': status_dictionary[station_data['status']]
        }
    }

    current_timestamp = datetime.now(barcelona_tz)

    out['freeSlotNumber']['metadata'] = {
        'timestamp': {
            'type': 'DateTime',
            'value': current_timestamp.replace(microsecond=0).isoformat()
        }
    }
    out['availableBikeNumber']['metadata'] = out['freeSlotNumber']['metadata']

    return out


# Persists the data to a Data Broker supporting FIWARE NGSI v2
def persist_data(entity_list):
    # print json.dumps(entity_list)

    data_obj = {
        'actionType': 'APPEND',
        'entities': entity_list
    }
    data_as_str = json.dumps(data_obj)

    headers = {
        'Content-Type': MIME_JSON,
        'Content-Length': len(data_as_str),
        'Fiware-Service': FIWARE_SERVICE,
        'Fiware-Servicepath': FIWARE_SERVICE_PATH
    }

    req = Request(
        url=(
            DATA_BROKER +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    try:
        with contextlib.closing(urlopen(req)) as f:
            print('Entities successfully created')
    except URLError as e:
        print('Error while POSTing data to Orion: %d %s' % (e.code, e.read()))


# Main module
def main():
    data = read_data(SOURCE)

    if data is None:
        print("Source data could not be read")
        exit()

    parsed_data = json.loads(data)

    station_list = parsed_data['stations']

    ngsi_data = []

    for station in station_list:
        h_station = harmonize_station(station)
        ngsi_data.append(h_station)

    persist_data(ngsi_data)


if __name__ == '__main__':
    main()
