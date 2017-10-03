#!bin/python
# -*- coding: utf-8 -*-

"""
Harmonises data from the city of Barcelona corresponding to the bicycle hiring stations
"""

import urllib2
# from pytz import timezone
import json
from datetime import datetime
from pytz import timezone
import re
from __future__ import print_function

# Origin of the Data (Barcelona's open data)
source = 'http://wservice.viabicing.cat/v2/stations'

status_dictionary = {
  'OPN': 'working',
  'CLS': 'outOfService'
}

barcelona_tz = timezone('CET')

MIME_JSON = 'application/json'
FIWARE_SERVICE = 'Bicycle'
FIWARE_SERVICE_PATH = "/Barcelona"

DATA_BROKER = 'http://localhost:1026'

# See http://fiware-datamodels.readthedocs.io/en/latest/Transportation/Bike/BikeHireDockingStation/doc/spec/index.html
BIKE_STATION_TYPE = 'BikeHireDockingStation'

# Sanitize string to avoid forbidden characters by the Orion Broker
def sanitize(str_in):
  return re.sub(r"[<(>)\"\'=;-]", "", str_in)


# Reads the data from the data source and returns a dictionary
def read_data():
  req = urllib2.Request(url=source)
  f = None
  try:
    f = urllib2.urlopen(req)
    json_data = f.read()
    f.close()
    return json_data
  except urllib2.URLError as e:
    print('Error while calling: %s : %s' % (source, e))
    if f != None:
      f.close()
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
        'streetAddress': sanitize(station_data['streetName'] +  ',' + station_data['streetNumber'])
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
  
  out['freeSlotNumber']['metadata'] = out['availableBikeNumber']['metadata'] = {
    'timestamp': {
      'type': 'DateTime',
      'value': datetime.now(barcelona_tz).replace(microsecond=0).isoformat()
    }
  }
  
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
      'Content-Type':   MIME_JSON,
      'Content-Length': len(data_as_str),
      'Fiware-Service': FIWARE_SERVICE,
      'Fiware-Servicepath': FIWARE_SERVICE_PATH
  }
    
  req = urllib2.Request(url=(DATA_BROKER + '/v2/op/update'), data=data_as_str, headers=headers)
  f = None
  try:
    f = urllib2.urlopen(req)
    f.close()
    print('Entities successfully created')
  except urllib2.URLError as e:
    print('Error while POSTing data to Orion: %d %s' % (e.code, e.read()))


# Main module
def main():
  data = read_data()
  
  if data is None:
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
