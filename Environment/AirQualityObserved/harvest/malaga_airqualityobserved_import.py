#!../bin/python
# -*- coding: utf-8 -*-

import csv
import json
import urllib2
import logging
import logging.handlers
import contextlib

pollutant_descriptions = {
    'NO2': 'Nitrogen Dioxide',
    'CO': 'Carbon Monoxide'
}

# Bootstrap data about districts in Malaga
districts_data = {}
# Bootstrap data about neighbourhoods in Malaga
neighbourhoods_data = {}

FIWARE_SERVICE = 'airquality'
FIWARE_SERVICE_PATH = '/Spain_Malaga'
MIME_JSON = 'application/json'

orion_service = 'http://localhost:1030'

persisted_entities = 0
in_error_entities = 0

# Entity data is indexed by "zone-zone type" and then by date/time
airquality_data = {}


def read_geojson_data():
    with contextlib.closing(open('Distritos.geojson', 'rU')) as data_file:
        data = json.load(data_file)

        features = data['features']
        for feature in features:
            properties = feature['properties']
            num_district = str(properties['NUMERO'])
            districts_data[num_district] = {
                'name': properties['NOMBRE'],
                'geometry': feature['geometry']
            }

    with contextlib.closing(open('Barrios.geojson', 'rU')) as data_file:
        data = json.load(data_file)

        features = data['features']
        for feature in features:
            properties = feature['properties']
            num_neighboourhood = str(properties['NUMBARRIO'])
            neighbourhoods_data[num_neighboourhood] = {
                'name': properties['NOMBARRIO'],
                'geometry': feature['geometry']
            }

# Processes a CSV entry which corresponds to a certain kind of pollutant


def process_csv_row(row, pollutant, unit_code):
    zone = row[0]
    zone_type = row[1]

    date = row[2].replace(' ', 'T')
    value = row[3]

    if value == '0':
        return

    if zone_type != '1' and zone_type != '2':
        return

    if zone_type == '1':
        # District
        area_data = districts_data
    elif zone_type == '2':
        # Neighbourhood
        area_data = neighbourhoods_data

    if zone not in area_data:
        return

    # geometry = area_data[zone]['geometry']
    # place_name = area_data[zone]['name']

    key = zone + '-' + zone_type + '-' + date
    if key not in airquality_data:
        entity = build_entity(zone, zone_type, date)
        airquality_data[key] = entity
    else:
        entity = airquality_data[key]

    if entity is None:
        return

    # Now adding the pollutant data
    pollutant_data = ','.join(pollutant, str(float(value)), unit_code,
                              pollutant_descriptions[pollutant])
    entity['measurand']['value'].append(pollutant_data)
    entity[pollutant] = {
        'value': float(value)
    }


# Builds entity data for the zone, zone type and data
def build_entity(zone, zone_type, date):
    if zone_type == '1':
        # District
        area_data = districts_data
    elif zone_type == '2':
        # Neighbourhood
        area_data = neighbourhoods_data

    if zone not in area_data:
        logger.warn('Zone data not found for: %s', zone)
        return None

    geometry = area_data[zone]['geometry']
    place_name = area_data[zone]['name']

    entity = {
        'id': 'Malaga-AirQualityObserved' + '-' + zone_type + '-' + zone + '-' + date,
        'type': 'AirQualityObserved',
        'location': {
            'type': 'geo:json',
            'value': geometry},
        'address': {
            'type': 'PostalAddress',
            'value': {
                'addressLocality': 'Malaga',
                'addressCountry': 'ES',
                'areaServed': place_name}},
        'dateObserved': {
            'type': 'DateTime',
                    'value': date},
        'measurand': {
            'type': 'List',
            'value': []},
        'source': {
            'type': 'URL',
            'value': 'http://www.edpingenieria.com/'},
    }

    return entity


# Reads data from CSV file (origin of data are public buses)
def get_malaga_airquality():
    with contextlib.closing(open('hourly_no2.csv', 'rU')) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        index = 0
        for row in reader:
            if index == 0:
                index += 1
                continue

            process_csv_row(row, 'NO2', 'GQ')

    with contextlib.closing(open('octohourly_co.csv', 'rU')) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        index = 0
        for row in reader:
            if index == 0:
                index += 1
                continue

            process_csv_row(row, 'CO', 'GP')

    logger.debug('Number of entities built: %d', len(airquality_data.keys()))
    # Entities are persisted on batches of 10 elements
    entity_buffer = []
    for entry in airquality_data:
        entity_buffer.append(airquality_data[entry])

        if len(entity_buffer) == 10:
            post_data(entity_buffer)
            entity_buffer = []

    # Last set of entities is persisted
    post_data(entity_buffer)


# POST data to an Orion Context Broker instance using NGSIv2 API
def post_data(data):
    if len(data) == 0:
        return

    entity_ids = []
    for entity in data:
        entity_ids.append(entity['id'])

    payload = {
        'actionType': 'APPEND',
        'entities': data
    }

    data_as_str = json.dumps(payload)

    headers = {
        'Content-Type': MIME_JSON,
        'Content-Length': len(data_as_str),
        'Fiware-Service': FIWARE_SERVICE,
        'Fiware-Servicepath': FIWARE_SERVICE_PATH
    }

    req = urllib2.Request(
        url=(
            orion_service +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    try:
        with contextlib.closing(urllib2.urlopen(req)) as f:  # noqa F841
            global persisted_entities
            logger.debug(
                "Entity batch successfully created: %s",
                ', '.join(entity_ids))
            persisted_entities = persisted_entities + 1
    except urllib2.URLError as e:
        global in_error_entities
        logger.error(
            'Error while POSTing data to Orion: %d %s',
            e.code,
            e.read())
        # logger.debug('Data which failed: %s', data_as_str)
        in_error_entities = in_error_entities + 1


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_airquality_malaga.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('Malaga')
    logger.setLevel(logging.DEBUG)

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logger()

    logger.debug(
        '#### Starting a new harvesting and harmonization cycle ... ####')

    read_geojson_data()

    logger.debug('Number of districts known: %d', len(districts_data.keys()))
    logger.debug('Number of neighbourhoods known: %d',
                 len(neighbourhoods_data.keys()))

    get_malaga_airquality()

    logger.debug('#### Harvesting and harmonization cycle ... finished ####')
