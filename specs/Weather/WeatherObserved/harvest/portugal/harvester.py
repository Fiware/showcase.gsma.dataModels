#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import io
import requests
import re
import sys
import argparse
import logging
import json
import yaml

default_orion = 'http://orion:1026'
default_latest = False
default_log_level = 'INFO'
default_path = '/Portugal'
default_service = 'weather'
default_timeout = -1

http_ok = [200, 201, 204]
limit_off = False
limit_on = False
log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None
stations = dict()
stations_off = list()
stations_on = list()
url_observation = 'https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json'
url_stations = 'https://www.ipma.pt/resources.www/transf/obs-sup/stations.json'


def decode_wind_direction(direction):
    return {
        '9': 180,  # North
        '5': 0,    # South
        '3': -90,  # East
        '7': 90,   # West
        '2': -135,  # Northeast
        '8': 135,  # Northwest
        '4': -45,  # Southeast
        '6': 45    # Southwest
    }.get(direction, None)


def get_data(value, scale=1):
    return None if value < 0 else value / scale


def harvest():
    result = dict()
    last = ''

    try:
        request = requests.get(url_observation)
    except requests.exceptions.ConnectionError:
        logger.error('Harvesting info failed due to the connection problem')
        return False

    if request.status_code in http_ok:
        data = json.loads(request.text)
    else:
        logger.error('Harvesting info failed due to the return code')
        return False

    if latest:
        last = sorted(data.items(), reverse=True)[0][0]

    for date in data:
        if latest and date != last:
            continue
        for station_code in data[date]:
            if limit_on:
                if station_code not in stations_on:
                    continue

            if limit_off:
                if station_code in stations_off:
                    continue

            if station_code not in stations:
                logger.error('Harvesting info about station %s failed due unknown station_code ', station_code)
                continue

            if station_code not in result:
                result[station_code] = list()

            observation = dict()

            observation['stationCode'] = {
                'value': station_code
            }
            observation['stationName'] = {
                'value': stations[station_code]['name']
            }
            observation['type'] = 'WeatherObserved'

            if not data[date][station_code]:
                logger.info('Harvesting info about station %s skipped', station_code)
                continue

            observation['atmosfericPressure'] = {
                'value': get_data(data[date][station_code]['pressao'])
            }
            observation['dataProvider'] = {
                'value': 'FIWARE'
            }
            observation['dateObserved'] = {
                'value': date,
                'type': 'DateTime'
            }
            observation['id'] = 'Portugal-WeatherObserved-' + station_code + '-' + date
            observation['location'] = {
                'value': stations[station_code]['location'],
                'type': 'geo:json'
            }
            observation['precipitation'] = {
                'value': get_data(data[date][station_code]['precAcumulada'])
            }
            observation['relativeHumidity'] = {
                'value': get_data(data[date][station_code]['humidade'], 100)
            }
            observation['source'] = {
                'value': 'https://www.ipma.pt/',
                'type': 'URL'
            }
            observation['temperature'] = {
                'value': get_data(data[date][station_code]['temperatura'])
            }
            observation['windDirection'] = {
                'value': decode_wind_direction(str(data[date][station_code]['idDireccVento']))
            }
            observation['windSpeed'] = {
                'value': get_data(data[date][station_code]['intensidadeVento'])
            }

            if latest:
                observation['id'] = 'Portugal-WeatherObserved-' + station_code + '-latest'

            result[station_code].append(observation)

    return result


def log_level_to_int(log_level_string):
    if log_level_string not in log_levels:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, log_levels)
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.ERROR)

    return log_level_int


def post(body):
    headers = {
        'Content-Type': 'application/json'
    }
    if service:
        headers['FIWARE-SERVICE'] = service
    if path:
        headers['FIWARE-SERVICEPATH'] = path

    for station_code in body:
        if len(body[station_code]) == 0:
            continue

        data = {
            'actionType': 'APPEND',
            'entities': body[station_code]
        }

        data = json.dumps(data)

        try:
            resp = requests.post(orion + '/v2/op/update', headers=headers, data=data)
        except requests.exceptions.ConnectionError:
            logger.error('Posting data to %s failed due to the connection problem', orion)
            return False

        if resp.status_code in http_ok:
            logger.debug('Context %s was successfully updated', station_code)
        else:
            logger.error('Context %s failed to update', station_code)
            return False

    return True


def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;-]", "", str_in)


def setup_logger():
    local_logger = logging.getLogger('root')
    local_logger.setLevel(log_level_to_int(args.log_level))

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level_to_int(args.log_level))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ')
    handler.setFormatter(formatter)
    local_logger.addHandler(handler)

    local_logger_req = logging.getLogger('requests')
    local_logger_req.setLevel(logging.WARNING)

    return local_logger, local_logger_req


def setup_stations():
    local_stations = dict()

    resp = requests.get(url_stations)

    if resp.status_code in http_ok:
        data = json.loads(resp.text)
    else:
        logger.error('Harvesting data from the stations failed due to the connection problem')
        sys.exit(1)

    for station in data:
        station_code = str(station['properties']['idEstacao'])

        if limit_on:
            if station_code not in stations_on:
                continue
        if limit_off:
            if station_code in stations_off:
                continue

        local_stations[station_code] = dict()
        local_stations[station_code]['name'] = sanitize(station['properties']['localEstacao'])
        local_stations[station_code]['location'] = station['geometry']

    return local_stations


def setup_stations_config(f):
    local_limit_off = False
    local_limit_on = False
    local_stations_off = list()
    local_stations_on = list()

    if f:
        try:
            with io.open(f, 'r', encoding='utf8') as source_file:
                temp = yaml.safe_load(source_file)
                if 'exclude' in temp:
                    for el in temp['exclude']:
                        local_stations_off.append(str(el))

                if 'include' in temp:
                    for el in temp['include']:
                        local_stations_on.append(str(el))
        except TypeError:
            logging.error('List of stations to be excluded is empty or wrong')
            sys.exit(1)

    if len(local_stations_off) > 0:
        local_limit_off = True
    if len(local_stations_on) > 0:
        local_limit_on = True

    return local_limit_on, local_limit_off, local_stations_on, local_stations_off


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

    logger, logger_req = setup_logger()
    limit_on, limit_off, stations_on, stations_off = setup_stations_config(args.config)
    stations = setup_stations()
    setup_status()

    while True:
        res = harvest()
        if res:
            logger.debug('Harvesting info succeeded')
            post(res)
        if timeout == -1:
            break
        else:
            logger.debug('Sleeping for the %s seconds', timeout)
            time.sleep(timeout)
