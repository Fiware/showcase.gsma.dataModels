#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import io
import requests
import re
import sys
import datetime
import argparse
import logging
import contextlib
import csv
import json
from pytz import timezone

default_csv = 'stations.csv'
default_orion = 'http://orion:1026'
default_latest = True
default_log_level = 'INFO'
default_path = '/Spain'
default_service = 'weather'
default_timeout = -1

log_levels = ['ERROR', 'INFO', 'DEBUG']
stations = dict()
stations_off = [
    '6332X',
    '76',
    '349',
    '367',
    '6381',
    '9174',
    '0171C',
    '0229I',
    '1036A',
    '1331D',
    '2331X',
    '2503X',
    '3125Y',
    '4492E',
    '6032B',
    '6205X',
    '6332X',
    '7012C',
    '7250X',
    '8290X',
    '9198A',
    '9263I',
    '9283X',
    '9443V',
    '9531X',
    '9574X',
    '9576C',
    '9814A',
    '9894X',
    '9918X',
    'C229X',
    'C315P',
    'C468B'
]
stations_on = list()
tz = timezone('CET')
url_template = ("http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_{}_datos-horarios.csv"
                "?k=cle&l={}&datos=det&w=0&f=temperatura&x=h6")


def log_level_to_int(log_level_string):
    if log_level_string not in log_levels:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, log_levels)
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.ERROR)

    return log_level_int


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


def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;-]", "", str_in)


def get_data(row, index, conversion=float, factor=1.0):
    value = row[index]
    return None if value == '' else conversion(value) / factor


def harvest(station_code):
    url = url_template.format(station_code, station_code)
    observation = dict()

    try:
        request = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.error('Harvesting info about station %s failed due to the connection problem', station_code)
        return False

    if request.status_code == 200:
        data = request.text
        if data.find('initial-scale') != -1:
            logger.debug('Harvesting info about station %s skipped', station_code)
            return False
    else:
        logger.error('Harvesting info about station %s failed due to the return code %s',
                     station_code, request.status_code)
        return False

    reader = csv.reader(io.StringIO(data), delimiter=',')
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
                'value': stations[station_code]['name']
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
        date_observed = datetime.datetime.strptime(row[0], '%d/%m/%Y %H:%M')
        observation['dateObserved'] = {
            'value': date_observed.replace(tzinfo=tz).isoformat(),
            'type': 'DateTime'
        }
        observation['source'] = {
            'value': 'http://www.aemet.es',
            'type': 'URL'
        }
        observation['dataProvider'] = {
            'value': 'FIWARE'
        }
        observation['address'] = {
            'value': {
                'addressLocality': stations[station_code]['address'],
                'addressCountry': 'ES'
            },
            'type': 'PostalAddress'
        }
        observation['location'] = stations[station_code]['location']
        observation['id'] = 'Spain-WeatherObserved' + '-' + station_code + '-' + date_observed.isoformat()
        if latest:
            observation['id'] = 'Spain-WeatherObserved' + '-' + station_code + '-' + 'latest'
            break
        logger.debug('Harvesting info for station %s succeeded', station_code)
    return observation


def post(body):
    data = {
        'actionType': 'APPEND',
        'entities': body
    }
    data = json.dumps(data)

    headers = {
        'Content-Type': 'application/json'
    }

    if service:
        headers['FIWARE-SERVICE'] = service

    if path:
        headers['FIWARE-SERVICEPATH'] = path

    try:
        resp = requests.post(orion + '/v2/op/update', headers=headers, data=data)
    except requests.exceptions.ConnectionError:
        logger.error('Posting data to %s failed due to the connection problem', orion)
        return False

    if resp.status_code == 204:
        logger.debug('Context was successfully updated')
    else:
        logger.error('Context failed to update')
        return False

    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--service',
                        dest="service",
                        default=default_service,
                        help='FIWARE Service',
                        action="store")
    parser.add_argument('--path',
                        dest="path",
                        default=default_path,
                        help='FIWARE Service Path',
                        action="store")
    parser.add_argument('--orion',
                        dest='orion',
                        default=default_orion,
                        help='Orion Context Broker',
                        action="store")
    parser.add_argument('--latest',
                        dest='latest',
                        default=default_latest,
                        help='Harvest only latest observation',
                        action="store_true")
    parser.add_argument('--timeout',
                        dest='timeout',
                        default=default_timeout,
                        help='Run harvester as a service',
                        action="store")
    parser.add_argument('--csv',
                        dest='csv',
                        default=default_csv,
                        help='Path to file with stations data',
                        action="store")
    parser.add_argument('--log-level',
                        default=default_log_level,
                        dest='log_level',
                        nargs='?',
                        help='Set the logging output level. {0}'.format(log_levels))
    parser.add_argument('stations',
                        metavar='stations',
                        type=str,
                        nargs='*',
                        help='Station codes separated by spaces. ' +
                        'See https://jmcanterafonseca.carto.com/viz/e7ccc6c6-9e5b-11e5-a595-0ef7f98ade21/public_map')
    args = parser.parse_args()

    service = args.service
    path = args.path
    orion = args.orion
    latest = args.latest
    timeout = int(args.timeout)

    logger = logging.getLogger('root')
    logger_req = logging.getLogger('requests')
    logger.setLevel(log_level_to_int(args.log_level))
    logger_req.setLevel(logging.WARNING)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level_to_int(args.log_level))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for s in args.stations:
        stations_on.append(s)

    with contextlib.closing(open(args.csv, 'r')) as csv_file:
        reader_orig = csv.reader(csv_file, delimiter=',')
        i = 0
        for el in reader_orig:
            check = True
            if i == 0:
                i += 1
                continue

            el_code = el[2]

            if len(stations_on) > 0:
                if el_code not in stations_on:
                    check = False

            if len(stations_off) > 0:
                if el_code in stations_off:
                    check = False

            if check:
                el_name = sanitize(el[3])
                el_address = sanitize(el[4])
                el_coords = {
                    'type': 'geo:json',
                    'value': {
                        'type': 'Point',
                        'coordinates': [float(el[0]), float(el[1])]
                    }
                }

                stations[el_code] = {
                    'name': el_name,
                    'address': el_address,
                    'location': el_coords
                }
            i += 1
    if len(stations_on) > 0:
        if len(stations) != len(stations_on):
            logger.error('Errors in the list of stations (stations_on) detected')
            sys.exit(1)

    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Timeout: %s', str(timeout))
    logger.info('Latest: %s', str(latest))
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Log level: %s', args.log_level)
    logger.info('Started')

    to_post = list()
    while True:
        # noinspection PyUnresolvedReferences
        to_post.clear()
        for station in stations:
            res = harvest(station)
            if res:
                logger.debug('Harvesting info about station %s succeeded', station)
                to_post.append(res)
        post(to_post)
        if timeout == -1:
            break
        else:
            logger.debug('Sleeping for the %s seconds', timeout)
            time.sleep(timeout)
