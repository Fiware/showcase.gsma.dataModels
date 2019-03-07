#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiohttp import ClientSession, client_exceptions
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run
from copy import deepcopy
from datetime import datetime
from json import dumps
from pytz import timezone
from re import sub
from sys import stdout
from time import sleep
from yaml import safe_load
from requests import get, exceptions
import logging

default_latest = False
default_limit_entities = 50
default_limit_source = 50
default_limit_target = 50
default_log_level = 'INFO'
default_orion = 'http://orion:1026'
default_path = '/Portugal'
default_service = 'weather'
default_timeout = -1

http_ok = [200, 201, 204]
log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None
matches = list()
stations = dict()
stations_file = 'stations.json'
tz = timezone('UTC')
tz_wet = timezone('Europe/Lisbon')
tz_azot = timezone('Atlantic/Azores')
tz_azot_codes = ['932', '501', '502', '504', '506', '507', '510', '511', '512', '513', '515']
url_observation = 'https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json'
url_stations = 'http://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson'

schema_template = {
    'id': 'Portugal-WeatherObserved-',
    'type': 'WeatherObserved',
    'address': {
        'type': 'PostalAddress',
        'value': {
           'addressCountry': 'PT',
           "addressLocality": None
        }
    },
    'atmosphericPressure': {
        'type': 'Number',
        'value': None
    },
    'dataProvider': {
        'type': 'Text',
        'value': 'FIWARE'
    },
    'dateObserved': {
        'type': 'DateTime'
    },
    'location': {
        'type': 'geo:json',
        'value': {
            'type': 'Point',
            'coordinates': None
        }
    },
    'precipitation': {
        'type': 'Number',
        'value': None
    },
    'pressureTendency': {
        'type': 'Number',
        'value': None
    },
    'relativeHumidity': {
        'type': 'Number',
        'value': None
    },
    'source': {
        'type': 'URL',
        'value': 'https://www.ipma.pt'
    },
    'stationCode': {
        'type': 'Text'
    },
    'stationName': {
        'type': 'Text'
    },
    'temperature': {
        'type': 'Number',
        'value': None
    },
    'windDirection': {
        'type': 'Number',
        'value': None
    },
    'windSpeed': {
        'type': 'Number',
        'value': None
    }

}


def decode_wind_direction(direction):
    """
    North: 180
    North-West: 135
    West: 90
    South-West: 45
    South: 0
    South-East: -45
    East: -90
    North-East: -135

    """

    return {
        '9': 180,
        '8': 135,
        '7': 90,
        '6': 45,
        '5': 0,
        '4': -45,
        '3': -90,
        '2': -135,
        'N': 180,
        'NW': 135,
        'W': 90,
        'SW': 45,
        'S': 0,
        'SE': -45,
        'E': -90,
        'NE': -135
    }.get(direction, None)


def harvest():
    logger.debug('Harvesting info started')
    result = list()
    last = ''

    try:
        request = get(url_observation)
    except exceptions.ConnectionError:
        logger.error('Harvesting info failed due to the connection problem')
        return False

    if request.status_code in http_ok:
        content = safe_load(request.text)
    else:
        logger.error('Harvesting info failed due to the return code')
        return False

    if latest:
        last = sorted(content.items(), reverse=True)[0][0]

    for date in content:
        if latest and date != last:
            continue
        for station_code in content[date]:
            if station_code not in stations:
                continue

            if not content[date][station_code]:
                logger.info('Harvesting info about station %s skipped', station_code)
                continue

            item = dict()
            item['id'] = station_code
            item['atmosphericPressure'] = content[date][station_code]['pressao']
            item['dateObserved'] = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            item['precipitation'] = content[date][station_code]['precAcumulada']
            item['relativeHumidity'] = content[date][station_code]['humidade']
            item['temperature'] = content[date][station_code]['temperatura']
            item['windDirection'] = content[date][station_code]['idDireccVento']
            item['windSpeed'] = content[date][station_code]['intensidadeVento']

            result.append(item)

    logger.debug('Harvesting info ended')
    return result


def log_level_to_int(log_level_string):
    if log_level_string not in log_levels:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, log_levels)
        raise ArgumentTypeError(message)

    return getattr(logging, log_level_string, logging.ERROR)


async def post(body):
    logger.debug('Posting info started')

    tasks = list()

    headers = {
        'Content-Type': 'application/json'
    }
    if service:
        headers['FIWARE-SERVICE'] = service

    if path:
        headers['FIWARE-SERVICEPATH'] = path

    sem = Semaphore(limit_target)

    i = 0
    j = 0
    body_divided = dict()
    body_divided[i] = list()
    while True:
        if len(body) > 0:
            if j < limit_entities:
                body_divided[i].append(body.pop())
                j += 1
            else:
                j = 0
                i += 1
                body_divided[i] = list()
        else:
            break

    async with ClientSession() as session:
        for el in body_divided:
            task = ensure_future(post_bounded(body_divided[el], headers, sem, session))
            tasks.append(task)

        response = await gather(*tasks)

    response = list(set(response))
    if True in response:
        response.remove(True)

    for el in response:
        logger.error('Posting info failed due to %s', el)

    logger.debug('Posting info ended')


async def post_bounded(el, headers, sem, session):
    async with sem:
        return await post_one(el, headers, session)


async def post_one(el, headers, session):
    payload = {
        'actionType': 'APPEND',
        'entities': el
    }

    payload = dumps(payload)

    url = orion + '/v2/op/update'
    try:
        async with session.post(url, headers=headers, data=payload) as response:
            await response.read()
    except client_exceptions.ClientConnectorError:
        return 'connection problems'

    if response.status not in http_ok:
        return 'return code ' + str(response.status)

    return True


async def prepare_schema(source):
    logger.debug('Schema preparation started')

    tasks = list()

    for item in source:
        task = ensure_future(prepare_schema_one(item))
        tasks.append(task)

    result = await gather(*tasks)

    logger.debug('Schema preparation ended')

    return result


async def prepare_schema_one(source):
    id_local = source['id']

    if id_local in tz_azot_codes:
        tz_local = tz_azot
    else:
        tz_local = tz_wet

    date_local = tz_local.localize(source['dateObserved']).astimezone(tz).isoformat()

    result = deepcopy(schema_template)

    if latest:
        result['id'] = result['id'] + id_local + '-' + 'latest'
    else:
        result['id'] = result['id'] + id_local + '-' + date_local

    result['address']['value']['addressLocality'] = stations[id_local]['name']

    if 'atmosphericPressure' in source:
        result['atmosphericPressure']['value'] = float(source['atmosphericPressure'])

    result['dateObserved']['value'] = date_local

    result['location']['value']['coordinates'] = stations[id_local]['coordinates']

    if 'precipitation' in source:
        result['precipitation']['value'] = float(source['precipitation'])

    if 'pressureTendency' in source:
        result['pressureTendency']['value'] = float(source['pressureTendency'])

    if 'relativeHumidity' in source:
        result['relativeHumidity']['value'] = float(source['relativeHumidity']) / 100

    result['stationCode']['value'] = id_local

    result['stationName']['value'] = stations[id_local]['name']

    if 'temperature' in source:
        result['temperature']['value'] = float(source['temperature'])

    if 'windDirection' in source:
        result['windDirection']['value'] = decode_wind_direction(str(source['windDirection']))

    if 'windSpeed' in source:
        result['windSpeed']['value'] = float(source['windSpeed']) * 0.28

    return result


def reply_status():
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Timeout: %s', str(timeout))
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Latest: %s', str(latest))
    logger.info('limit_target: %s', str(limit_target))
    logger.info('Log level: %s', args.log_level)
    logger.info('Started')


def sanitize(str_in):
    return sub(r"[<(>)\"\'=;-]", "", str_in)


def setup_logger():
    local_logger = logging.getLogger('root')
    local_logger.setLevel(log_level_to_int(args.log_level))

    handler = logging.StreamHandler(stdout)
    handler.setLevel(log_level_to_int(args.log_level))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ')
    handler.setFormatter(formatter)
    local_logger.addHandler(handler)

    local_logger_req = logging.getLogger('requests')
    local_logger_req.setLevel(logging.WARNING)

    return local_logger, local_logger_req


def setup_stations(stations_limit):
    result = dict()
    limit_on = False
    limit_off = False
    content = None
    resp = None

    if 'include' in stations_limit:
        limit_on = True
    if 'exclude' in stations_limit:
        limit_off = True

    try:
        resp = get(url_stations)
    except exceptions.ConnectionError:
        logger.error('Harvesting init data from the stations failed due to the connection problem')
        exit(1)

    if resp.status_code in http_ok:
        content = safe_load(resp.text)['features']
    else:
        logger.error('Harvesting init data from the stations failed due to the connection problem')
        exit(1)

    for station in content:
        station_code = str(station['properties']['idEstacao'])

        if limit_on:
            if station_code not in stations_limit['include']:
                continue
        if limit_off:
            if station_code in stations_limit['exclude']:
                continue

        result[station_code] = dict()
        result[station_code]['name'] = sanitize(station['properties']['localEstacao'])
        result[station_code]['coordinates'] = station['geometry']['coordinates']

    if limit_on:
        if len(result) != len(stations_limit['include']):
            logger.error('Errors in the list of stations (stations_on) detected')
            exit(1)

    return result


def setup_stations_config(f):
    local_stations = dict()

    if f:
        try:
            with open(f, 'r', encoding='utf8') as f:
                content = f.read()
                config = sub(r'-.*\n?',  setup_config_re, content)
            f.close()

            source = safe_load(config)

            if 'exclude' in source and 'include' in source:
                logging.error('List of stations is empty or wrong')
                exit(1)

            if 'exclude' in source:
                local_stations['exclude'] = list()
                for el in source['exclude']:
                    local_stations['exclude'].append(el)

            if 'include' in source:
                local_stations['include'] = list()
                for el in source['include']:
                    local_stations['include'].append(el)

        except TypeError:
            logging.error('List of stations is empty or wrong')
            exit(1)
        except FileNotFoundError:
            logging.error('Config file not found')
            exit(1)

    return local_stations


def setup_config_re(station):
    fix = sub('-', '', station.group()).strip()
    matches.append(fix)
    return "- '{}'\n".format(fix)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--config',
                        dest='config',
                        help='YAML file with list of stations to be harvested or excluded from harvesting')
    parser.add_argument('--latest',
                        action='store_true',
                        default=default_latest,
                        dest='latest',
                        help='Harvest only latest observation')
    parser.add_argument('--limit-entities',
                        default=default_limit_entities,
                        dest='limit_entities',
                        help='Limit amount of entities per 1 post request to orion')
    parser.add_argument('--limit-target',
                        default=default_limit_target,
                        dest='limit_target',
                        help='Limit amount of parallel requests to orion')
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
    limit_entities = int(args.limit_entities)
    limit_target = int(args.limit_target)
    orion = args.orion
    path = args.path
    service = args.service
    timeout = int(args.timeout)

    logger, logger_req = setup_logger()
    res = setup_stations_config(args.config)
    stations = setup_stations(res)
    reply_status()

    while True:
        res = harvest()
        res = run(prepare_schema(res))
        run(post(res))
        if timeout == -1:
            logger.info('Ended')
            break
        else:
            logger.debug('Sleeping for the %s seconds', timeout)
            sleep(timeout)
