#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This program collects information about Portugal weather stations from IPMA and prepares config that can be used by
    harvester itself to upload the list of Portugal weather stations to Orion Context Broker or export data required by
    other weather harvesters:
      - https://github.com/FIWARE/dataModels/tree/master/specs/Weather/WeatherObserved/harvesters/portugal

    It also exports data to the CSV file (./stations.csv), that can be used to upload the list of weather stations
    to Google Maps:
      - https://www.google.com/maps/d/viewer?mid=1Sd5uNFd2um0GPog2EGkyrlzmBnEKzPQw .

    Legal notes:
      - http://www.ipma.pt/en/siteinfo/index.html?page=index.xml

    Examples:
      - get the list of stations from IPMA:
        curl -X GET --header 'Accept: application/json' \
            'http://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson'

    AsyncIO name convention:
    async def name - entry point for asynchronous data processing/http requests and post processing
    async def name_bounded - intermediate step to limit amount of parallel workers
    async def name_one - worker process
"""

from aiohttp import ClientSession, ClientConnectorError
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run, TimeoutError as ToE, set_event_loop_policy
from copy import deepcopy
from csv import DictWriter
from re import sub
from sys import stdout
from uvloop import EventLoopPolicy
from yajl import dumps, loads
from yaml import safe_load as load, dump
from requests import get, exceptions
import logging

default_limit_entities = 50           # amount of entities per 1 request to Orion
default_limit_targets = 50            # amount of parallel request to Orion
default_log_level = 'INFO'
default_orion = 'http://orion:1026'   # Orion Contest Broker endpoint

http_ok = [200, 201, 204]

log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None

stations_file_yml = 'stations.yml'   # destination file for yml format
stations_file_csv = 'stations.csv'   # destination file for csv format

tz_wet = 'Europe/Lisbon'
tz_azot = 'Atlantic/Azores'
tz_azot_codes = ['932', '501', '502', '504', '506', '507', '510', '511', '512', '513', '515']

url_stations = 'http://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson'

template = {
    'id': 'urn:ngsi-ld:PointOfInterest:WeatherStation-PT-',
    'type': 'PointOfInterest',
    'category': {
        'type': 'array',
        'value': [
            'WeatherStation'
        ]
    },
    'address': {
        'type': 'PostalAddress',
        'value': {
            'addressCountry': 'PT',
            'addressLocality': None
        }
    },
    'location': {
        'type': 'geo:json',
        'value': {
            'type': 'Point',
            'coordinates': None
        }
    },
    'source': {
        'type': 'URL',
        'value': 'https://www.ipma.pt'
    }
}


def collect_stations():
    result = dict()
    result['stations'] = dict()
    content = None
    resp = None

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

        result['stations'][station_code] = dict()
        result['stations'][station_code]['locality'] = sanitize(station['properties']['localEstacao'])
        result['stations'][station_code]['longitude'] = station['geometry']['coordinates'][0]
        result['stations'][station_code]['latitude'] = station['geometry']['coordinates'][1]

        if station_code in tz_azot_codes:
            result['stations'][station_code]['timezone'] = tz_azot
        else:
            result['stations'][station_code]['timezone'] = tz_wet

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


async def prepare_schema(src_file, csv_flag=False):
    logger.debug('Schema preparation started')

    tasks = list()

    for item in src_file['stations']:
        task = ensure_future(prepare_schema_one(item, src_file['stations'][item], csv_flag))
        tasks.append(task)

    result = await gather(*tasks)

    logger.debug('Schema preparation ended')

    return result


async def prepare_schema_one(local_id, station, csv_flag):

    if not csv_flag:
        item = deepcopy(template)

        item['location']['value']['coordinates'] = [station['longitude'], station['latitude']]
        item['address']['value']['addressLocality'] = station['locality']
        item['id'] = item['id'] + local_id
    else:
        item = deepcopy(station)

        item['id'] = local_id
        item['country'] = 'PT'

    return item


def reply_status(stations):
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Stations: %s', str(len(stations['stations'])))
    logger.info('limit_entities: %s', str(limit_entities))
    logger.info('limit_targets: %s', str(limit_targets))
    logger.info('Log level: %s', args.log_level)


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


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--export_csv',
                        action='store_true',
                        dest='csv',
                        help='Export the list of stations to CSV file (./stations.csv) and exit')
    parser.add_argument('--export_yml',
                        action='store_true',
                        dest='yml',
                        help='Export the list of stations to YML file (./stations.yml) and exit')
    parser.add_argument('--import',
                        action='store_true',
                        dest='import_yml',
                        help='Import the list of stations from file (./stations.yml)')
    parser.add_argument('--limit-entities',
                        default=default_limit_entities,
                        dest='limit_entities',
                        help='Limit amount of entities per 1 post request to Orion')
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

    args = parser.parse_args()

    limit_entities = int(args.limit_entities)
    limit_targets = int(args.limit_targets)
    orion = args.orion

    if 'path' in args:
        path = args.path
    if 'service' in args:
        service = args.service

    logger, logger_req = setup_logger()

    set_event_loop_policy(EventLoopPolicy())

    logger.info('Started')

    res = None

    if not args.import_yml:
        logger.debug('Initial data collection started')

        res = collect_stations()

        logger.debug('Initial data collection ended')
    else:
        try:
            with open(stations_file_yml, 'r') as file:
                res = load(file)

        except FileNotFoundError:
            logger.error('Station file is not present')
            exit(1)

    if args.csv:
        fieldnames = ['id', 'country', 'locality', 'latitude', 'longitude', 'timezone']

        res = run(prepare_schema(res, True))

        with open(stations_file_csv, 'w', encoding='utf8') as file:
            writer = DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for element in res:
                writer.writerow(element)

    if args.yml:
        with open(stations_file_yml, 'w', encoding='utf8') as file:
            file.write(dump(res, indent=4, allow_unicode=True))

    if not args.yml and not args.csv:
        reply_status(res)

        res = run(prepare_schema(res))
        run(post(res))

    logger.info('Ended')
    exit(0)
