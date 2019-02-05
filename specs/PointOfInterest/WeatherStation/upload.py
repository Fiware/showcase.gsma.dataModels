#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiohttp import ClientSession, client_exceptions
from argparse import ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run
from copy import deepcopy
from json import dumps, load
from re import sub
from sys import stdout
import logging

default_limit = 50
default_log_level = 'INFO'
default_orion = 'http://orion:1026'
default_path = '/Spain'
default_service = 'poi'

http_ok = [200, 201, 204]
logger = None
logger_req = None
matches = list()
stations = None
stations_file = 'stations.json'

schema_template = {
    'id': 'Spain-WeatherStations-',
    'type': 'PointOfInterest',
    'category': {
        'type': 'Text',
        'value': 'WeatherStation'
    },
    'address': {
        'type': 'PostalAddress',
        'value': {
            'addressCountry': 'ES',
            'addressLocality': None
        }
    },
    'location': {
        'type': 'geo:json',
        'value': {
            'type': 'Point',
            'coordinates': None
        }
    }
}


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

    sem = Semaphore(limit)

    i = 0
    j = 0
    body_divided = dict()
    body_divided[i] = list()
    while True:
        if len(body) > 0:
            if j < limit:
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

    payload = dumps(payload, ensure_ascii=False)

    url = orion + '/v2/op/update'
    try:
        async with session.post(url, headers=headers, data=payload) as response:
            await response.read()
    except client_exceptions.ClientConnectorError:
        return 'connection problems'

    if response.status not in http_ok:
        return 'return code ' + str(response.status)

    return True


async def prepare_schema():
    logger.debug('Schema preparation started')

    tasks = list()

    for item in stations['stations']:
        task = ensure_future(prepare_schema_one(item))
        tasks.append(task)

    result = await gather(*tasks)

    logger.debug('Schema preparation ended')

    return result


async def prepare_schema_one(station):

    item = deepcopy(schema_template)

    item['id'] = item['id'] + station
    longitude = float(stations['stations'][station]['longitude'])
    latitude = float(stations['stations'][station]['latitude'])
    item['location']['value']['coordinates'] = [longitude, latitude]

    if 'municipality' in stations['stations'][station]:
        municipality_id = stations['stations'][station]['municipality']
        item['address']['value']['addressLocality'] = sanitize(stations['municipalities'][municipality_id]['name'])
        province_id = stations['municipalities'][municipality_id]['province']
        if stations['provinces'][province_id]['type'] != '3':
            item['address']['value']['addressProvince'] = stations['provinces'][province_id]['name']
            community_id = stations['provinces'][province_id]['community']
            item['address']['value']['addressCommunity'] = stations['communities'][community_id]['name']

    return item


def reply_status():
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Limit: %s', str(limit))
    logger.info('Started')


def sanitize(str_in):
    return sub(r"[<(>)\"\'=;-]", "", str_in)


def setup_logger():
    local_logger = logging.getLogger('root')
    local_logger.setLevel(20)

    handler = logging.StreamHandler(stdout)
    handler.setLevel(20)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ')
    handler.setFormatter(formatter)
    local_logger.addHandler(handler)

    local_logger_req = logging.getLogger('requests')
    local_logger_req.setLevel(logging.WARNING)

    return local_logger, local_logger_req


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--config',
                        dest='config',
                        help='JSON file with stations')
    parser.add_argument('--limit',
                        default=default_limit,
                        dest='limit',
                        help='Limit amount of entities per 1 post request to orion')
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

    args = parser.parse_args()

    limit = int(args.limit)
    orion = args.orion
    path = args.path
    service = args.service

    logger, logger_req = setup_logger()

    logger.info('Started')
    with open(stations_file) as f:
        stations = load(f)

    res = run(prepare_schema())
    run(post(res))
    logger.info('Finished')
