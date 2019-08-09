#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This program collects Spain weather observations from AEMET and uploads them to the Orion Context Broker.
    It uses predefined list of stations (./stations.yml), that can be obtained by other harvester:
      - https://github.com/FIWARE/dataModels/tree/master/specs/PointOfInterest/WeatherStation/harvesters/spain

    You must provide a valid API key to collect data from AEMET data portal. That key can be obtained via email
      - https://opendata.aemet.es/centrodedescargas/altaUsuario?.

    Legal notes:
      - http://www.aemet.es/en/nota_legal

    Examples:
      - get the weather observation:
        curl -X GET --header 'Accept: application/json' --header "api_key: ${KEY}" \
            'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones'

    AsyncIO name convention:
    async def name - entry point for asynchronous data processing/http requests and post processing
    async def name_bounded - intermediate step to limit amount of parallel workers
    async def name_one - worker process

    Warning! AEMET open data portal has a requests limit. So you can't make more then 149 requests from one try.
    This limit will be removed in the next version.
"""

from aiohttp import ClientSession, ClientConnectorError
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run, TimeoutError as ToE, set_event_loop_policy
from copy import deepcopy
from re import sub
from requests import get, exceptions
from sys import stdout
from time import sleep
from uvloop import EventLoopPolicy
from yajl import dumps, loads
from yaml import safe_load as load
import logging

default_latest = False                 # preserve only latest values
default_limit_entities = 50            # amount of entities per 1 request to Orion
default_limit_targets = 50             # amount of parallel request to Orion
default_log_level = 'INFO'
default_orion = 'http://orion:1026'    # Orion Contest Broker endpoint
default_station_file = 'stations.yml'  # source file with list of municipalities
default_timeout = -1                   # if value != -1, then work as a service

http_ok = [200, 201, 204]

log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None

stations = dict()                      # preprocessed list of stations

url_aemet = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'

template = {
    'id': 'urn:ngsi-ld:WeatherObserved:Spain-WeatherObserved-',
    'type': 'WeatherObserved',
    'address': {
        'type': 'PostalAddress',
        'value': {
            'addressCountry': 'ES',
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
    'relativeHumidity': {
        'type': 'Number',
        'value': None
    },
    'source': {
        'type': 'URL',
        'value': 'http://www.aemet.es'
    },
    'stationCode': {
        'type': 'Text',
        'value': None
    },
    'stationName': {
        'type': 'Text',
        'value': None
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


def collect(key):
    logger.debug('Collecting data from AEMET started')

    try:
        result = get(url_aemet, headers={'api_key': key})
    except exceptions.ConnectionError:
        logger.error('Collecting link from AEMET failed due to the connection problem')
        return False

    if result.status_code not in http_ok:
        logger.error('Collecting link from AEMET failed due to the return code %s', result.status_code)
        return False

    logger.debug('Remaining requests %s', result.headers.get('Remaining-request-count'))
    result = loads(result.text)

    try:
        result = get(result['datos'])
    except exceptions.ConnectionError:
        logger.error('Collecting data from AEMET failed due to the connection problem')
        return False

    if result.status_code not in http_ok:
        logger.error('Collecting data from AEMET failed due to the return code %s', result.status_code)
        return False

    result = loads(result.text)

    for i in range(len(result) - 1, -1, -1):
        if result[i]['idema'] not in stations:
            del result[i]

    if latest:
        check = list()
        result = sorted(result, key=lambda k: (k['idema'], k['fint']), reverse=True)

        for item in range(len(result) - 1, -1, -1):
            if result[item]['idema'] in check:
                del result[item]
            else:
                check.append(result[item]['idema'])

    logger.debug("Collection data from AEMET ended")
    return result


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

    sem = Semaphore(limit_targets)

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
    return True


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
        if item['idema'] in stations:
            task = ensure_future(prepare_schema_one(item))
            tasks.append(task)

    result = await gather(*tasks)

    logger.debug('Schema preparation ended')

    return result


async def prepare_schema_one(source):
    result = None
    id_local = source['idema']

    if id_local in stations:
        date_local = source['fint'] + 'Z'

        result = deepcopy(template)

        if latest:
            result['id'] = result['id'] + id_local + '-' + 'latest'
        else:
            result['id'] = result['id'] + id_local + '-' + date_local

        result['address']['value']['addressLocality'] = stations[id_local]['name']

        if 'pres' in source:
            result['atmosphericPressure']['value'] = source['pres']
        else:
            del result['atmosphericPressure']

        result['dateObserved']['value'] = date_local

        result['location']['value']['coordinates'] = stations[id_local]['coordinates']

        if 'prec' in source:
            result['precipitation']['value'] = source['prec']
        else:
            del result['precipitation']

        if 'hr' in source:
            result['relativeHumidity']['value'] = source['hr']
        else:
            del result['relativeHumidity']

        result['stationCode']['value'] = id_local

        result['stationName']['value'] = stations[id_local]['name']

        if 'ta' in source:
            result['temperature']['value'] = source['ta']
        else:
            del result['temperature']

        if 'dv' in source:
            result['windDirection']['value'] = 180 - source['dv']
        else:
            del result['windDirection']

        if 'vv' in source:
            result['windSpeed']['value'] = source['vv']
        else:
            del result['windSpeed']

    return result


def reply_status():
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Latest: %s', str(latest))
    logger.info('limit_entities: %s', str(limit_entities))
    logger.info('limit_targets: %s', str(limit_targets))
    logger.info('Log level: %s', args.log_level)
    logger.info('Timeout: %s', str(timeout))


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


def setup_stations(stations_limit, station_file):
    result = dict()
    source = None
    limit_off = False
    limit_on = False

    if 'include' in stations_limit:
        limit_on = True
    if 'exclude' in stations_limit:
        limit_off = True

    try:
        with open(station_file, 'r') as f:
            source = load(f)

    except FileNotFoundError:
        logger.error('Station file is not present')
        exit(1)

    for station in source['stations']:
        check = True
        if limit_on:
            if station not in stations_limit['include']:
                check = False
        if limit_off:
            if station in stations_limit['exclude']:
                check = False

        if check:

            result[station] = dict()

            result[station]['coordinates'] = [source['stations'][station]['longitude'],
                                              source['stations'][station]['latitude']]
            result[station]['name'] = source['stations'][station]['locality']

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
                for item in source['exclude']:
                    local_stations['exclude'].append(item)

            if 'include' in source:
                local_stations['include'] = list()
                for item in source['include']:
                    local_stations['include'].append(item)

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
                        help='YAML file with list of stations to be collected or excluded from collecting')
    parser.add_argument('--key',
                        action='store',
                        dest='key',
                        help='API Key to access to AEMET Open Data Portal',
                        required=True)
    parser.add_argument('--latest',
                        action='store_true',
                        default=default_latest,
                        dest='latest',
                        help='Collect only latest observation')
    parser.add_argument('--limit-entities',
                        default=default_limit_entities,
                        dest='limit_entities',
                        help='Limit amount of entities per 1 request to Orion')
    parser.add_argument('--limit-targets',
                        default=default_limit_targets,
                        dest='limit_targets',
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
    parser.add_argument('--stations',
                        action='store',
                        default=default_station_file,
                        dest="station_file",
                        help='Station file')
    parser.add_argument('--timeout',
                        action='store',
                        default=default_timeout,
                        dest='timeout',
                        help='Run as a service')

    args = parser.parse_args()

    latest = args.latest
    limit_entities = int(args.limit_entities)
    limit_targets = int(args.limit_targets)
    orion = args.orion
    timeout = int(args.timeout)

    if 'path' in args:
        path = args.path
    if 'service' in args:
        service = args.service

    logger, logger_req = setup_logger()

    set_event_loop_policy(EventLoopPolicy())

    res = setup_stations_config(args.config)
    stations = setup_stations(res, args.station_file)

    reply_status()

    while True:
        res = collect(args.key)
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
