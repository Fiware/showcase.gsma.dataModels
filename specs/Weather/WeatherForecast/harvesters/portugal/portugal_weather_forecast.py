#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This program collects Portugal weather forecasts from IPMA and uploads them to the Orion Context Broker.
    It uploads the list of stations on the fly from
      - http://api.ipma.pt/json/locations.json.

    Legal notes:
      - http://www.ipma.pt/en/siteinfo/index.html?page=index.xml

    Examples:
      - get the weather forecast from IPMA:
        curl -X GET --header 'Accept: application/json' \
            'http://api.ipma.pt/json/alldata/1110600.json'

    AsyncIO name convention:
    async def name - entry point for asynchronous data processing/http requests and post processing
    async def name_bounded - intermediate step to limit amount of parallel workers
    async def name_one - worker process
"""

from aiohttp import ClientSession, ClientConnectorError
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run, TimeoutError, set_event_loop_policy
from copy import deepcopy
from datetime import datetime, timedelta
from pytz import timezone
from re import sub
from requests import get, exceptions
from sys import stdout
from time import sleep
from uvloop import EventLoopPolicy
from yajl import dumps, loads
from yaml import safe_load as load
import logging

default_latest = False                # preserve only latest values
default_limit_entities = 50           # amount of entities per 1 request to Orion
default_limit_source = 10             # amount of parallel request to IPMA
default_limit_target = 50             # amount of parallel request to Orion
default_log_level = 'INFO'
default_orion = 'http://orion:1026'   # Orion Contest Broker endpoint
default_timeout = -1                  # if value != -1, then work as a service

http_ok = [200, 201, 204]

log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None

stations = dict()                     # preprocessed list of stations

tz = timezone('UTC')
tz_wet = 'Europe/Lisbon'
tz_azot = 'Atlantic/Azores'
tz_azot_codes = ['3490100', '3480200', '3470100', '3460200', '3450200', '3440100', '3420300', '3410100']

url_observation = 'http://api.ipma.pt/json/alldata/{}.json'
url_stations = 'http://api.ipma.pt/json/locations.json'

template = {
    'id': 'urn:ngsi-ld:WeatherForecast:Portugal-WeatherForecast-',
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
        'type': 'StructuredValue',
        'value': {
            'temperature': None
        }
    },
    'dayMinimum': {
        'type': 'StructuredValue',
        'value': {
            'temperature': None
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


def decode_weather_type(item):
    out = {
        0: None,
        1: 'clearSky',
        2: 'partlyCloudy',
        3: 'sunnyIntervals',
        4: 'cloudy',
        5: 'highClouds',
        6: 'showers',
        7: 'lightShowers',
        8: 'heavyShowers',
        9: 'rain',
        10: 'lightRain',
        11: 'heavyRain',
        12: 'intermittentRain',
        13: 'intermittentLightRain',
        14: 'intermittentHeavyRain',
        15: 'drizzle',
        16: 'mist',
        17: 'fog',
        18: 'snow',
        19: 'thunderstorms',
        20: 'showersAndThunderstorms',
        21: 'hail',
        22: 'frost',
        23: 'rainAndThunderstorms',
        24: 'convectiveClouds',
        25: 'partyCloudy',
        26: 'fog',
        27: 'cloudy'
    }.get(item, None)

    if out is None and item != 0:
        logger.error('Unknown value of WeatherType detected, %s', item)

    return out if out else None


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

    return out if out else None


async def collect():
    logger.debug('Connecting data from IPMA started')

    tasks = list()

    sem = Semaphore(limit_source)

    async with ClientSession() as session:
        for station in stations:
            task = ensure_future(collect_bounded(station, sem, session))
            tasks.append(task)

        result = await gather(*tasks)

    while False in result:
        result.remove(False)

    logger.debug('Collecting data from IPMA ended')
    return result


async def collect_bounded(station, sem, session):
    async with sem:
        return await collect_one(station, session)


async def collect_one(station, session):

    try:
        async with session.get(stations[station]['url']) as response:
            result = await response.text()
            status = response.status
    except ClientConnectorError:
        logger.error('Collecting data from IPMA station %s failed due to the connection problem', station)
        return False
    except TimeoutError:
        logger.error('Collecting link from IPMA station %s failed due to the timeout problem', station)
        return False

    if status not in http_ok:
        logger.error('Collecting data from IPMA station %s failed due to the return code %s', station, status)
        return False

    content = loads(result)

    result = dict()
    result['id'] = station
    result['retrieved'] = datetime.now().replace(microsecond=0)
    result['forecasts'] = dict()

    today = datetime.now(tz).strftime("%Y-%m-%d") + 'T00:00:00'
    tomorrow = (datetime.now(tz) + timedelta(days=1)).strftime("%Y-%m-%d") + 'T00:00:00'

    for forecast in content:
        if forecast['idPeriodo'] != 24:
            continue

        date = forecast['dataPrev']

        if date not in [today, tomorrow]:
            continue

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
    except TimeoutError:
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

    return [j for i in result for j in i]


async def prepare_schema_one(source):
    result = list()
    id_local = source['id']

    today = datetime.now(tz).strftime("%Y-%m-%d") + 'T00:00:00'
    tomorrow = (datetime.now(tz) + timedelta(days=1)).strftime("%Y-%m-%d") + 'T00:00:00'
    retrieved = source['retrieved'].replace(tzinfo=tz).isoformat().replace('+00:00', 'Z')

    for date in source['forecasts']:

        item = deepcopy(template)

        forecast = source['forecasts'][date]

        issued = forecast['issued'].replace(tzinfo=tz).isoformat().replace('+00:00', 'Z')

        forecast_date = datetime.strptime(date, '%Y-%m-%dT00:00:00')

        valid_from = forecast_date.replace(tzinfo=tz)
        valid_to = valid_from + timedelta(hours=24)

        valid_from_iso = valid_from.isoformat().replace('+00:00', 'Z')
        valid_from_short = valid_from.strftime('%H:%M:%S')

        valid_to_iso = valid_to.isoformat().replace('+00:00', 'Z')
        valid_to_short = valid_to.strftime('%H:%M:%S')

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

        if 'tMax' in forecast:
            item['dayMaximum']['value']['temperature'] = float(forecast['tMax'])
        else:
            del item['dayMaximum']

        if 'tMin' in forecast:
            item['dayMinimum']['value']['temperature'] = float(forecast['tMin'])
        else:
            del item['dayMinimum']

        if forecast['feelsLikeTemperature'] is not None:
            item['feelsLikeTemperature']['value'] = float(forecast['feelsLikeTemperature'])
        else:
            del item['feelsLikeTemperature']

        if forecast['precipitationProbability'] is not None:
            item['precipitationProbability']['value'] = float(forecast['precipitationProbability'] / 100)
        else:
            del item['precipitationProbability']

        if forecast['relativeHumidity'] is not None:
            item['relativeHumidity']['value'] = float(forecast['relativeHumidity'])
        else:
            del item['relativeHumidity']

        if forecast['temperature'] is not None:
            item['temperature']['value'] = float(forecast['temperature'])
        else:
            del item['temperature']

        item['validFrom']['value'] = valid_from_iso

        item['validTo']['value'] = valid_to_iso

        item['validity']['value'] = valid_from_iso + '/' + valid_to_iso

        if forecast['weatherType'] is not None:
            item['weatherType']['value'] = decode_weather_type(forecast['weatherType'])

        if item['weatherType']['value'] is None:
            del item['weatherType']

        if forecast['windDirection'] is not None:
            item['windDirection']['value'] = decode_wind_direction(forecast['windDirection'])

        if item['windDirection']['value'] is None:
            del item['windDirection']

        if forecast['windSpeed'] is not None:
            item['windSpeed']['value'] = round(float(forecast['windSpeed']) * 0.28, 2)
        else:
            del item['windSpeed']

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
    resp = None

    if 'include' in stations_limit:
        limit_on = True
    if 'exclude' in stations_limit:
        limit_off = True

    try:
        resp = get(url_stations)
    except exceptions.ConnectionError:
        exit(1)

    if resp.status_code not in http_ok:
        logger.error('Collecting the list of stations from IPMA failed due to the return code %s', resp.status_code)
        exit(1)

    content = loads(resp.text)

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
                for item in source['exclude']:
                    local_stations['exclude'].append(item)

            if 'include' in source:
                local_stations['include'] = list()
                for item in source['include']:
                    local_stations['include'].append(item)

        except TypeError:
            logging.error('Config file  is empty or wrong')
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
    parser.add_argument('--latest',
                        action='store_true',
                        default=default_latest,
                        dest='latest',
                        help='Collect only latest forecast')
    parser.add_argument('--limit-entities',
                        default=default_limit_entities,
                        dest='limit_entities',
                        help='Limit amount of entities per 1 request to orion')
    parser.add_argument('--limit-source',
                        default=default_limit_source,
                        dest='limit_source',
                        help='Limit amount of parallel requests to IPMA')
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
    limit_source = int(args.limit_source)
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
        res = run(collect())
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
