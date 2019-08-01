#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This program collects Portugal weather observations from IPMA and uploads them to the Orion Context Broker.
    It uploads the list of stations on the fly from
      - http://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson.

    Legal notes:
      - http://www.ipma.pt/en/siteinfo/index.html?page=index.xml

    Examples:
      - get the weather observation from IPMA:
        curl -X GET --header 'Accept: application/json' \
            'https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json'

    AsyncIO name convention:
    async def name - entry point for asynchronous data processing/http requests and post processing
    async def name_bounded - intermediate step to limit amount of parallel workers
    async def name_one - worker process
"""

from aiohttp import ClientSession, ClientConnectorError
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run, TimeoutError as ToE, set_event_loop_policy
from copy import deepcopy
from datetime import datetime
from pytz import timezone
from re import sub
from sys import stdout
from time import sleep
from uvloop import EventLoopPolicy
from yajl import dumps, loads
from yaml import safe_load as load
from requests import get, exceptions
import logging

default_latest = False                # preserve only latest values
default_limit_entities = 50           # amount of entities per 1 request to Orion
default_limit_target = 50             # amount of parallel request to Orion
default_log_level = 'INFO'
default_orion = 'http://orion:1026'   # Orion Contest Broker endpoint
default_timeout = -1                  # if value != -1, then work as a service

http_ok = [200, 201, 204]

log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None

stations = dict()                     # preprocessed list of stations
stations_file = 'stations.json'       # source file with list of stations

tz = timezone('UTC')
tz_wet = timezone('Europe/Lisbon')
tz_azot = timezone('Atlantic/Azores')
tz_azot_codes = ['932', '501', '502', '504', '506', '507', '510', '511', '512', '513', '515']

url_observation = 'https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json'
url_stations = 'http://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson'

template = {
    'id': 'urn:ngsi-ld:WeatherObserved:Portugal-WeatherObserved-',
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


def collect():
    logger.debug('Collecting data from IPMA started')
    result = list()
    last = ''

    try:
        request = get(url_observation)
    except exceptions.ConnectionError:
        logger.error('Collecting data from IPMA failed due to the connection problem')
        return False

    if request.status_code in http_ok:
        content = loads(request.text)
    else:
        logger.error('Collecting data from IPMA failed due to the return code')
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
                logger.info('Collecting data about station %s skipped', station_code)
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

    logger.debug('Collecting data from IPMA ended')
    return result


def decode_wind_direction(item):
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

    out = {
        '9': 180,
        '8': 135,
        '7': 90,
        '6': 45,
        '5': 0,
        '4': -45,
        '3': -90,
        '2': -135,
        '1': 180,
        '0': 'Calm',
        'N': 180,
        'NW': 135,
        'W': 90,
        'SW': 45,
        'S': 0,
        'SE': -45,
        'E': -90,
        'NE': -135
    }.get(item, None)

    if out is None:
        logger.error('Unknown value of WindDirection detected, %s', item)

    if out == 'Calm':
        out = None

    return out if out else None


def log_level_to_int(log_level_string):
    if log_level_string not in log_levels:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, log_levels)
        raise ArgumentTypeError(message)

    return getattr(logging, log_level_string, logging.ERROR)


async def post(body):
    logger.debug('Posting data to Orion started')

    tasks = list()

    headers = {
        'Content-Type': 'application/json'
    }
    if service:
        headers['FIWARE-SERVICE'] = service

    if path:
        headers['FIWARE-SERVICEPATH'] = path

    sem = Semaphore(limit_target)

    # splitting list to list of lists to fit into limits
    block = 0
    items = 0
    body_divided = dict()
    body_divided[0] = list()
    while True:
        if len(body) > 0:
            if items < limit_entities:
                body_divided[block].append(body.pop())
                items += 1
            else:
                items = 0
                block += 1
                body_divided[block] = list()
        else:
            break

    async with ClientSession() as session:
        for item in body_divided:
            task = ensure_future(post_bounded(body_divided[item], headers, sem, session))
            tasks.append(task)

        response = await gather(*tasks)

    response = list(set(response))
    if True in response:
        response.remove(True)

    for item in response:
        logger.error('Posting data to Orion failed due to the %s', item)

    logger.debug('Posting data to Orion ended')


async def post_bounded(item, headers, sem, session):
    async with sem:
        return await post_one(item, headers, session)


async def post_one(item, headers, session):
    payload = {
        'actionType': 'APPEND',
        'entities': item
    }

    payload = dumps(payload)

    url = orion + '/v2/op/update'
    try:
        async with session.post(url, headers=headers, data=payload) as response:
            status = response.status
    except ClientConnectorError:
        return 'connection problem'
    except ToE:
        return 'timeout problem'

    if status not in http_ok:
        return 'response code ' + str(status)

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

    date_local = source['dateObserved'].replace(tzinfo=tz).isoformat().replace('+00:00', 'Z')

    result = deepcopy(template)

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
    else:
        del result['precipitation']

    if 'pressureTendency' in source:
        result['pressureTendency']['value'] = float(source['pressureTendency'])
    else:
        del result['pressureTendency']

    if 'relativeHumidity' in source:
        result['relativeHumidity']['value'] = float(source['relativeHumidity']) / 100
    else:
        del result['relativeHumidity']

    result['stationCode']['value'] = id_local

    result['stationName']['value'] = stations[id_local]['name']

    if 'temperature' in source:
        result['temperature']['value'] = float(source['temperature'])
    else:
        del result['temperature']

    if 'windDirection' in source:
        result['windDirection']['value'] = decode_wind_direction(str(source['windDirection']))

    if result['windDirection']['value'] is None:
        del result['windDirection']

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
        logger.error('Collecting the list of stations from IPMA failed due to connection problem')
        exit(1)

    if resp.status_code in http_ok:
        content = loads(resp.text)['features']
    else:
        logger.error('Collecting the list of stations from IPMA failed due to the return code %s', resp.status_code)
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

        if station_code in tz_azot_codes:
            result[station_code]['timezone'] = tz_azot
        else:
            result[station_code]['timezone'] = tz_wet

    if limit_on:
        if len(result) != len(stations_limit['include']):
            logger.error('Errors in the list of stations detected')
            exit(1)

    return result


def setup_stations_config(f):
    local_stations = dict()

    if f:
        try:
            with open(f, 'r', encoding='utf8') as f:
                content = f.read()
                config = sub(r'-.*\n?', setup_config_re, content)
            f.close()

            source = load(config)

            if 'exclude' in source and 'include' in source:
                logging.error('Config file is empty or wrong')
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
            logging.error('Config file is empty or wrong')
            exit(1)
        except FileNotFoundError:
            logging.error('Config file not found')
            exit(1)

    return local_stations


def setup_config_re(station):
    fix = sub('-', '', station.group()).strip()
    return "- '{}'\n".format(fix)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--config',
                        dest='config',
                        help='YAML file with list of stations to be harvested or excluded from collecting')
    parser.add_argument('--latest',
                        action='store_true',
                        default=default_latest,
                        dest='latest',
                        help='Collect only latest observation')
    parser.add_argument('--limit-entities',
                        default=default_limit_entities,
                        dest='limit_entities',
                        help='Limit amount of entities per 1 post request to Orion')
    parser.add_argument('--limit-target',
                        default=default_limit_target,
                        dest='limit_target',
                        help='Limit amount of parallel requests to Orion')
    parser.add_argument('--log-level',
                        default=default_log_level,
                        dest='log_level',
                        help='Set the logging output level. {0}'.format(log_levels),
                        nargs='?')
    parser.add_argument('--orion',
                        action='store',
                        default=default_orion,
                        dest='orion',
                        help='Orion Context Broker endpoint')
    parser.add_argument('--path',
                        action='store',
                        dest='path',
                        help='FIWARE Service Path')
    parser.add_argument('--service',
                        action='store',
                        dest="service",
                        help='FIWARE Service')
    parser.add_argument('--timeout',
                        action='store',
                        default=default_timeout,
                        dest='timeout',
                        help='Run as a service')

    args = parser.parse_args()

    latest = args.latest
    limit_entities = int(args.limit_entities)
    limit_target = int(args.limit_target)
    orion = args.orion
    timeout = int(args.timeout)

    if 'path' in args:
        path = args.path
    if 'service' in args:
        service = args.service

    logger, logger_req = setup_logger()

    set_event_loop_policy(EventLoopPolicy())

    res = setup_stations_config(args.config)
    stations = setup_stations(res)

    reply_status()

    while True:
        res = collect()
        if res:
            res = run(prepare_schema(res))
            run(post(res))
        if timeout == -1:
            break
        else:
            logger.debug('Sleeping for the %s seconds', timeout)
            sleep(timeout)

    logger.info('Ended')
    exit(0)
