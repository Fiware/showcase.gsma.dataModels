#!bin/python
# -*- coding: utf-8 -*-

import urllib2
import StringIO
import csv
import datetime
import json
import logging
import logging.handlers
from pytz import timezone
import contextlib
import re

# List of known weather stations
station_data = {}

# Orion service that will store the data
orion_service = 'http://localhost:1030'

# Stations in error so these are skipped when retrieving data
station_code_exceptions = [
    '9946X',
    '1658',
    '349',
    '9894X',
    '1010X',
    '9198A',
    '6381',
    '9720X',
    'C619Y',
    '1178Y',
    '9111',
    '9718X',
    '0244X',
    '6268X',
    '3254Y',
    '6340X',
    '3386A',
    '3391',
    '7012C',
    '9918X',
    '8191Y',
    '5192',
    '76',
    '4492E',
    '1331D',
    '0171C',
    '1583X',
    '8210Y',
    '9814A',
    '9994X',
    '9174',
    '2084Y',
    'C917E',
    '3337U',
    '2661',
    '367',
    '9263I',
    '5246',
    '7250X',
    '2182C',
    '0229I',
    '1735X',
    'C229X',
    '9531X',
    '1561I',
    '2150H',
    '0034X',
    '1036A']

logger = None

madrid_tz = timezone('CET')

weather_observed = ("http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_{}_datos-horarios.csv"
                    "?k=cle&l={}&datos=det&w=0&f=temperatura&x=h6")

# Statistics for tracking purposes
persisted_entities = 0
already_existing_entities = 0
in_error_entities = 0
persisted_stations = 0
total_stations = 0

MIME_JSON = 'application/json'
FIWARE_SERVICE = 'Weather'
FIWARE_SPATH = '/Spain'


def decode_wind_direction(direction):
    return {
        'Norte': 180,
        'Sur': 0,
        'Este': -90,
        'Oeste': 90,
        'Nordeste': -135,
        'Noroeste': 135,
        'Sureste': -45,
        'Suroeste': 45
    }.get(direction, None)


# Sanitize string to avoid forbidden characters by Orion
def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;-]", "", str_in)


def get_data(row, index, conversion=float, factor=1.0):
    value = row[index]
    return None if value == '' else conversion(value) / factor


def get_weather_observed_spain():
    for station_code in station_data:
        out = []
        if station_code in station_code_exceptions:
            continue

        source = weather_observed.format(station_code, station_code)

        logger.debug('Requesting data from station: %s', station_code)

        req = urllib2.Request(url=source)
        try:
            f = urllib2.urlopen(req)
        except urllib2.URLError as e:
            logger.error('Error while calling: %s : %s', source, e)
            if f is not None:
                f.close()
            continue

        csv_data = f.read()

        if csv_data.find('initial-scale') != -1:
            logger.debug('Skipping: %s', station_code)
            continue

        logger.debug('Data read successfully: %s', station_code)

        csv_file = StringIO.StringIO(csv_data)
        reader = csv.reader(csv_file, delimiter=',')

        index = 0
        for row in reader:
            if index < 4:
                index += 1
                continue

            observation = {
                'type': 'WeatherObserved',
                'stationCode': {
                    'value': station_code
                },
                'stationName': {
                    'value': sanitize(station_data[station_code]['name'])
                }
            }
            if len(row) < 2:
                continue

            observation['temperature'] = {
                'value': get_data(row, 1)
            }
            observation['windSpeed'] = {
                'value': get_data(row, 2, float, 1 / 0.28)
            }
            observation['windDirection'] = {
                'value': decode_wind_direction(row[3])
            }
            observation['precipitation'] = {
                'value': get_data(row, 6)
            }
            observation['atmosphericPressure'] = {
                'value': get_data(row, 7)
            }
            observation['pressureTendency'] = {
                'value': get_data(row, 8)
            }
            observation['relativeHumidity'] = {
                'value': get_data(row, 9, factor=100.0)
            }

            date_observed = datetime.datetime.strptime(
                row[0], '%d/%m/%Y %H:%M')
            observation['dateObserved'] = {
                'value': date_observed.replace(tzinfo=madrid_tz).isoformat(),
                'type': 'DateTime'
            }
            observation['source'] = {
                'value': 'http://www.aemet.es',
                'type': 'URL'
            }
            observation['dataProvider'] = {
                'value': 'TEF'
            }
            observation['address'] = {
                'value': {
                    'addressLocality': sanitize(
                        station_data[station_code]['address']),
                    'addressCountry': 'ES'},
                'type': 'PostalAddress'}
            observation['location'] = station_data[station_code]['location']

            observation['id'] = '-'.join('Spain', 'WeatherObserved',
                                         station_code, date_observed.isoformat())

            out.append(observation)

        f.close()

        # Last observation is tagged as 'latest'
        if len(out) > 0:
            latest_observation = out[-1]
            latest_observation['id'] = '-'.join('Spain', 'WeatherObserved',
                                                station_code, 'latest')

        # A batch of station data is persisted
        post_station_data_batch(station_code, out)


# POST data to an Orion Context Broker instance using NGSIv2 API
def post_station_data_batch(station_code, data):
    data_obj = {
        'actionType': 'APPEND',
        'entities': data
    }
    data_as_str = json.dumps(data_obj)

    headers = {
        'Content-Type': MIME_JSON,
        'Content-Length': len(data_as_str),
        'Fiware-Service': FIWARE_SERVICE,
        'Fiware-Servicepath': FIWARE_SPATH
    }

    logger.debug(
        'Going to persist %s (%d) to %s',
        station_code,
        len(data),
        orion_service)

    req = urllib2.Request(
        url=(
            orion_service +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    try:
        with contextlib.closing(urllib2.urlopen(req)) as f:  # noqa F841
            global persisted_entities
            global persisted_stations
            persisted_entities = persisted_entities + len(data)
            persisted_stations += 1
            logger.debug('Entities successfully created for station: %s %d/%d',
                         station_code, persisted_stations, total_stations)
    except urllib2.URLError as e:
        logger.error('Error!!! %s', station_code)
        global in_error_entities
        logger.error(
            'Error while POSTing data to Orion: %d %s',
            e.code,
            e.read())
        logger.debug('Data which failed: %s', data_as_str)
        in_error_entities += 1


# Reads station data from CSV file
def read_station_csv():
    with contextlib.closing(open('../stations-normalized-wgs84.csv', 'rU')) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        index = 0
        for row in reader:
            if index != 0:
                station_code = row[2]
                station_name = row[3]
                station_address = row[4]
                station_coords = {
                    'type': 'geo:json',
                    'value': {
                        'type': 'Point',
                        'coordinates': [float(row[0]), float(row[1])]
                    }
                }

                station_data[station_code] = {
                    'name': station_name,
                    'address': station_address,
                    'location': station_coords
                }
            index += 1


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_weather_observed_spain.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('WeatherObserved')
    logger.setLevel(logging.DEBUG)

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logger()

    read_station_csv()

    logger.debug(
        '#### Starting a new harvesting and harmonization cycle ... ####')
    logger.debug(
        'Number of weather stations known: %d', len(
            station_data.keys()))
    total_stations = len(station_data.keys()) - len(station_code_exceptions)

    get_weather_observed_spain()

    logger.debug('Number of entities persisted: %d', persisted_entities)
    logger.debug(
        'Number of entities already existed: %d',
        already_existing_entities)
    logger.debug('Number of stations in error: %d', in_error_entities)
    logger.debug('#### Harvesting cycle finished ... ####')
