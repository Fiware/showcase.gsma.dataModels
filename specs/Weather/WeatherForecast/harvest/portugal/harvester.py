#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiohttp import ClientSession, client_exceptions
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run
from copy import deepcopy
from datetime import datetime, timedelta
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
default_limit_source = 35
default_limit_target = 50
default_log_level = 'INFO'
default_orion = 'http://orion:1026'
default_path = '/Portugal'
default_service = 'weather'
default_timeout = -1

data = dict()
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
tz_azot_codes = ['3490100', '3480200', '3470100', '3460200', '3450200', '3440100', '3420300', '3410100']
url_observation = 'http://api.ipma.pt/json/alldata/{}.json'
url_stations = 'http://api.ipma.pt/json/locations.json'

schema_template = {
    'id': 'Portugal-WeatherForecast-',
    'type': 'WeatherForecast',
    'address': {
        'type': 'PostalAddress',
        'value': {
            'addressCountry': 'PT',
            'addressLocality': None,
            'postalCode': None
        }
    },
    'dateIssued': {
        'type': 'DateTime',
        'value': None
    },
    'dataProvider': {
        'type': 'Text',
        'value': 'FIWARE'
    },
    'dateRetrieved': {
        'type': 'DateTime',
        'value': None
    },
    'dayMaximum': {
        'type': 'Object',
        'value': {
            'feelsLikeTemperature': None,
            'temperature': None,
            'relativeHumidity': None
        }
    },
    'dayMinimum': {
        'type': 'Object',
        'value': {
            'feelsLikeTemperature': None,
            'temperature': None,
            'relativeHumidity': None
        }
    },
    'feelsLikeTemperature': {
        'type': 'Number',
        'value': None
    },
    'precipitationProbability': {
        'type': 'Number',
        'value': None
    },
    'relativeHumidity': {
        'type': 'Number',
        'value': None
    },
    'source': {
        'type': 'URL',
        'value': 'http://www.ipma.pt'
    },
    'temperature': {
        'type': 'Number',
        'value': None
    },
    'validFrom': {
        'type': 'DateTime',
        'value': None
    },
    'validTo': {
        'type': 'DateTime',
        'value': None
    },
    'validity': {
        'type': 'Text',
        'value': None
    },
    'weatherType': {
        'type': 'Text',
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


def check_entity(forecast, item):
    if item in forecast:
        if forecast[item] != '-99.0' and forecast[item] != -99:
            return forecast[item]

    return None


def decode_weather_type(weather_type):
    return {
        1: 'clear',
        2: 'slightlyCloudy',
        3: 'partlyCloudy',
        4: 'overcast',
        5: 'highClouds',
        6: 'lightRain',
        7: 'drizzle',
        9: 'rain',
        11: 'heavyRain'
    }.get(weather_type, None)


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


async def harvest():
    logger.debug('Harvesting info started')

    tasks = list()

    sem = Semaphore(limit_source)

    async with ClientSession() as session:
        for station in stations:
            task = ensure_future(harvest_bounded(station, sem, session))
            tasks.append(task)

        result = await gather(*tasks)

    while False in result:
        result.remove(False)

    logger.debug('Harvesting info ended')
    return result


async def harvest_bounded(station, sem, session):
    async with sem:
        return await harvest_one(station, session)


async def harvest_one(station, session):

    try:
        async with session.get(stations[station]['url']) as response:
            content = await response.read()
    except client_exceptions.ClientConnectorError:
        logger.error('Harvesting info about station %s failed due to the connection problem', station)
        return False

    if response.status not in http_ok:
        logger.error('Harvesting info about station %s failed due to the return code %s', station, response.status)
        return False

    content = safe_load(content)

    result = dict()
    result['id'] = station
    result['retrieved'] = datetime.now().replace(microsecond=0)
    result['forecasts'] = dict()

    for forecast in content:
        date = forecast['dataPrev']
        if date not in result['forecasts']:
            result['forecasts'][date] = dict()

        result['forecasts'][date]['feelsLikeTemperature'] = check_entity(forecast, 'utci')
        result['forecasts'][date]['issued'] = datetime.strptime(forecast['dataUpdate'], '%Y-%m-%dT%H:%M:%S')
        result['forecasts'][date]['period'] = forecast['idPeriodo']
        result['forecasts'][date]['precipitationProbability'] = check_entity(forecast, 'probabilidadePrecipita')
        result['forecasts'][date]['relativeHumidity'] = check_entity(forecast, 'hR')
        result['forecasts'][date]['temperature'] = check_entity(forecast, 'tMed')
        result['forecasts'][date]['tMax'] = check_entity(forecast, 'tMax')
        result['forecasts'][date]['tMin'] = check_entity(forecast, 'tMin')
        result['forecasts'][date]['weatherType'] = check_entity(forecast, 'idTipoTempo')
        result['forecasts'][date]['windDirection'] = check_entity(forecast, 'ddVento')
        result['forecasts'][date]['windSpeed'] = check_entity(forecast, 'ffVento')

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

    return [j for i in result for j in i]


async def prepare_schema_one(source):
    result = list()
    id_local = source['id']

    today = datetime.now(tz).strftime("%Y-%m-%d") + 'T00:00:00'
    tomorrow = (datetime.now(tz) + timedelta(days=1)).strftime("%Y-%m-%d") + 'T00:00:00'

    if id_local in tz_azot_codes:
        tz_local = tz_azot
    else:
        tz_local = tz_wet

    retrieved = source['retrieved'].replace(tzinfo=tz).isoformat()

    for date in source['forecasts']:
        if date not in [today, tomorrow]:
            continue
        if source['forecasts'][date]['period'] != 24:
            continue

        item = deepcopy(schema_template)
        ft = source['forecasts'][date]

        ft_date = tz_local.localize(ft['issued'])
        issued = ft_date.astimezone(tz).isoformat()
        valid_from = tz_local.localize(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S'))
        valid_to = valid_from + timedelta(hours=24)

        valid_from_iso = valid_from.isoformat()
        valid_from_short = valid_from.strftime('%H:%M:%S%z')
        valid_from = valid_from.astimezone(tz).isoformat()
        valid_to_iso = valid_to.isoformat()
        valid_to_short = valid_to.strftime('%H:%M:%S%z')
        valid_to = valid_to.astimezone(tz).isoformat()

        if latest:
            if date == today:
                item['id'] = item['id'] + id_local + '_today_' + valid_from_short + '_' + valid_to_short
            if date == tomorrow:
                item['id'] = item['id'] + id_local + '_tomorrow_' + valid_from_short + '_' + valid_to_short
        else:
            item['id'] = item['id'] + id_local + '_' + valid_from_iso + '_' + valid_to_iso

        item['address']['value']['addressLocality'] = stations[id_local]['addressLocality']
        item['address']['value']['postalCode'] = stations[id_local]['postalCode']

        item['dateIssued']['value'] = issued

        item['dateRetrieved']['value'] = retrieved

        item['dayMaximum']['value']['temperature'] = float(ft['tMax'])

        item['dayMinimum']['value']['temperature'] = float(ft['tMin'])

        if ft['feelsLikeTemperature'] is not None:
            item['feelsLikeTemperature']['value'] = float(ft['feelsLikeTemperature'])

        if ft['precipitationProbability'] is not None:
            item['precipitationProbability']['value'] = float(ft['precipitationProbability'] / 100)

        if ft['relativeHumidity'] is not None:
            item['relativeHumidity']['value'] = float(ft['relativeHumidity'])

        if ft['temperature'] is not None:
            item['temperature']['value'] = float(ft['temperature'])

        item['validFrom']['value'] = valid_from

        item['validTo']['value'] = valid_to

        item['validity']['value'] = valid_from_iso + '/' + valid_to_iso

        if ft['weatherType'] is not None:
            item['weatherType']['value'] = decode_weather_type(ft['weatherType'])

        if ft['windDirection'] is not None:
            item['windDirection']['value'] = decode_wind_direction(ft['windDirection'])

        if ft['windSpeed'] is not None:
            item['windSpeed']['value'] = round(float(ft['windSpeed']) * 0.28, 2)

        result.append(item)

    return result


def reply_status():
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Timeout: %s', str(timeout))
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Latest: %s', str(latest))
    logger.info('Limit_source: %s', str(limit_source))
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
        content = safe_load(resp.text)
    else:
        logger.error('Harvesting init data from the stations failed due to the connection problem')
        exit(1)

    for station in content:
        station_code = str(station['globalIdLocal'])

        if limit_on:
            if station_code not in stations_limit['include']:
                continue
        if limit_off:
            if station_code in stations_limit['exclude']:
                continue

        result[station_code] = dict()
        result[station_code]['postalCode'] = station_code
        result[station_code]['addressLocality'] = sanitize(station['local'])
        result[station_code]['url'] = url_observation.format(station_code)

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
    parser.add_argument('--limit-source',
                        default=default_limit_source,
                        dest='limit_source',
                        help='Limit amount of parallel requests to aemet')
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
    limit_source = int(args.limit_source)
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
        res = run(harvest())
        res = run(prepare_schema(res))
        run(post(res))
        if timeout == -1:
            logger.info('Ended')
            break
        else:
            logger.debug('Sleeping for the %s seconds', timeout)
            sleep(timeout)
