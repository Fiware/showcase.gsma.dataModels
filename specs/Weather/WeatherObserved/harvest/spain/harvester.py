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
import yaml

default_csv = 'stations.csv'
default_orion = 'http://orion:1026'
default_latest = False
default_log_level = 'INFO'
default_path = '/Spain'
default_service = 'weather'
default_timeout = -1

http_ok = [200, 201, 204]
log_levels = ['ERROR', 'INFO', 'DEBUG']
tz = timezone('CET')
url_template = ("http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_{}_datos-horarios.csv"
                "?k=cle&l={}&datos=det&w=0&f=temperatura&x=h6")


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

    if request.status_code in http_ok:
        data = request.text
        if data.find('initial-scale') != -1:
            logger.info('Harvesting info about station %s skipped', station_code)
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

        observation['stationCode'] = {
            'value': station_code
        }
        observation['stationName'] = {
            'value': stations[station_code]['name']
        }
        observation['type'] = 'WeatherObserved'

        if len(row) < 2:
            logger.info('Harvesting info about station %s skipped', station_code)
            continue

        observation['address'] = {
            'value': {
                'addressLocality': stations[station_code]['address'],
                'addressCountry': 'ES'
            },
            'type': 'PostalAddress'
        }
        observation['atmosphericPressure'] = {
            'value': get_data(row, 7)
        }
        observation['dataProvider'] = {
            'value': 'FIWARE'
        }
        date_observed = datetime.datetime.strptime(row[0], '%d/%m/%Y %H:%M')
        observation['dateObserved'] = {
            'value': date_observed.replace(tzinfo=tz).isoformat(),
            'type': 'DateTime'
        }
        observation['id'] = 'Spain-WeatherObserved-' + station_code + '-' + date_observed.isoformat()
        observation['location'] = stations[station_code]['location']
        observation['precipitation'] = {
            'value': get_data(row, 6)
        }
        observation['pressureTendency'] = {
            'value': get_data(row, 8)
        }
        observation['relativeHumidity'] = {
            'value': get_data(row, 9, factor=100.0)
        }
        observation['source'] = {
            'value': 'http://www.aemet.es',
            'type': 'URL'
        }
        observation['temperature'] = {
            'value': get_data(row, 1)
        }
        observation['windDirection'] = {
            'value': decode_wind_direction(row[3])
        }
        observation['windSpeed'] = {
            'value': get_data(row, 2, float, 1 / 0.28)
        }

        if latest:
            observation['id'] = 'Spain-WeatherObserved-' + station_code + '-latest'
            break

    return observation


def log_level_to_int(log_level_string):
    if log_level_string not in log_levels:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, log_levels)
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.ERROR)

    return log_level_int


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

    if resp.status_code in http_ok:
        logger.debug('Context was successfully updated')
    else:
        logger.error('Context failed to update')
        return False

    return True


def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;-]", "", str_in)


def setup_logger():
    global logger

    logger = logging.getLogger('root')
    logger_req = logging.getLogger('requests')
    logger.setLevel(log_level_to_int(args.log_level))
    logger_req.setLevel(logging.WARNING)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level_to_int(args.log_level))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def setup_stations(csv_source):
    global stations

    stations = dict()

    with contextlib.closing(open(csv_source, 'r')) as csv_file:
        reader_orig = csv.reader(csv_file, delimiter=',')
        i = 0
        for el in reader_orig:
            check = True
            if i == 0:
                i += 1
                continue

            el_code = el[2]

            if limit_on:
                if el_code not in stations_on:
                    check = False
            if limit_off:
                if el_code in stations_off:
                    check = False

            if check:
                el_name = sanitize(el[3])
                el_address = sanitize(el[4])

                el_coords = dict()
                el_coords['type'] = 'geo:json'
                el_coords['value'] = {
                    'type': 'Point',
                    'coordinates': [float(el[0]), float(el[1])]
                }

                stations[el_code] = dict()
                stations[el_code]['name'] = el_name,
                stations[el_code]['address'] = el_address,
                stations[el_code]['location'] = el_coords

            i += 1

    if len(stations_on) > 0:
        if len(stations) != len(stations_on):
            logger.error('Errors in the list of stations (stations_on) detected')
            sys.exit(1)


def setup_stations_config(f):
    global stations_off
    global stations_on
    global limit_off
    global limit_on

    stations_off = list()
    stations_on = list()
    limit_off = False
    limit_on = False

    if f:
        try:
            with io.open(f, 'r', encoding='utf8') as source_file:
                temp = yaml.load(source_file)
                if 'exclude' in temp:
                    for el in temp['exclude']:
                        stations_off.append(str(el))

                if 'include' in temp:
                    for el in temp['include']:
                        stations_on.append(str(el))
        except TypeError:
            logging.error('List of stations to be excluded is empty or wrong')
            sys.exit(1)

    if len(stations_off) > 0:
        limit_off = True
    if len(stations_on) > 0:
        limit_on = True


def setup_status():
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Timeout: %s', str(timeout))
    logger.info('Latest: %s', str(latest))
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Log level: %s', args.log_level)
    logger.info('Started')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        dest='config',
                        help='YAML file with list of stations to be harvested or excluded from harvesting. ' +
                        'See https://jmcanterafonseca.carto.com/viz/e7ccc6c6-9e5b-11e5-a595-0ef7f98ade21/public_map')
    parser.add_argument('--csv',
                        action='store',
                        default=default_csv,
                        dest='csv',
                        help='Path to file with stations data')
    parser.add_argument('--latest',
                        action='store_true',
                        default=default_latest,
                        dest='latest',
                        help='Harvest only latest observation')
    parser.add_argument('--log-level',
                        default=default_log_level,
                        dest='log_level',
                        help='Set the logging output level. {0}'.format(log_levels),
                        nargs='?')
    parser.add_argument('--orion',
                        action='store',
                        default=default_orion,
                        dest='orion',
                        help='Orion Context Broker')
    parser.add_argument('--path',
                        action='store',
                        default=default_path,
                        dest='path',
                        help='FIWARE Service Path')
    parser.add_argument('--service',
                        action='store',
                        default=default_service,
                        dest="service",
                        help='FIWARE Service')
    parser.add_argument('--timeout',
                        action='store',
                        default=default_timeout,
                        dest='timeout',
                        help='Run harvester as a service')

    args = parser.parse_args()

    latest = args.latest
    orion = args.orion
    path = args.path
    service = args.service
    timeout = int(args.timeout)

    setup_logger()
    setup_stations_config(args.config)
    setup_stations(args.csv)
    setup_status()

    to_post = list()
    while True:
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
