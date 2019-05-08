#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This program collects Spain weather forecast from AEMET and uploads it to the Orion Context Broker.
    It use predefined list of municipalities (./stations.yml), that can be obtained by other harvester:
    https://github.com/FIWARE/dataModels/tree/master/specs/PointOfInterest/WeatherStation

    You must provide a valid API key to collect data from AEMET data portal. That key can be obtained via email
    (https://opendata.aemet.es/centrodedescargas/altaUsuario?).

    You must provide a valid id of municipality, that can be found in stations.yml

    Source: https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{}
    Example: curl -X GET --header 'Accept: application/json' --header "api_key: ${KEY}" \
                 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/28079'

"""

from aiohttp import ClientSession, client_exceptions
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run
from copy import deepcopy
from datetime import datetime, timedelta
from pytz import timezone
from re import sub
from requests import get, exceptions
from sys import stdout
from time import sleep
from yajl import dumps, loads
from yaml import safe_load as load
import logging


default_latest = False                # preserve only latest values
default_limit_entities = 50           # amount of entities per 1 request to Orion
default_limit_source = 10             # amount of parallel request to AEMET
default_limit_target = 50             # amount of parallel request to Orion
default_log_level = 'INFO'
default_orion = 'http://orion:1026'   # Orion Contest Broker endpoint
default_path = '/Spain'               # header FIWARE-SERVICEPATH
default_service = 'weather'           # header FIWARE-SERVICE
default_timeout = -1                  # if value != -1, then work as a service

http_ok = [200, 201, 204]
log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None
stations = dict()                     # preprocessed list of stations
stations_file = 'stations.yml'
tz = timezone('UTC')
url_aemet = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{}"


template = {
    'id': 'Spain-WeatherForecast-',
    'type': 'WeatherForecast',
    'address': {
        'type': 'PostalAddress',
        'value': {
            'addressCountry': 'ES',
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
        'value': 'http://www.aemet.es'
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


"""
    async def name - entry point for asynchronous data processing/http requests and post processing
    async def name_bounded - intermediate step to limit amount of parallel workers
    async def name_one - worker process   
"""


async def collect(key):
    logger.debug('Collecting data from AEMET started')

    tasks = list()

    sem = Semaphore(limit_source)

    async with ClientSession() as session:
        for station in stations:
            task = ensure_future(collect_bounded(station, sem, session, key))
            tasks.append(task)

        result = await gather(*tasks)

    while False in result:
        result.remove(False)

    logger.debug("Collection data from AEMET ended")
    return result


async def collect_bounded(station, sem, session, key):
    async with sem:
        return await collect_one(station, session, key)


async def collect_one(station, session, key):

    try:
        async with session.get(stations[station]['url'], headers={'api_key': key}, ssl=False) as response:
            result = await response.read()
    except client_exceptions.ClientConnectorError:
        logger.error('Collecting link from AEMET station %s failed due to the connection problem', station)
        return False

    if response.status not in http_ok:
        logger.error('Collecting link from AEMET station %s failed due to the return code %s', station, str(response.status))
        return False

    logger.debug('Remaining requests %s', response.headers.get('Remaining-request-count'))
    result = loads(result.decode('UTF-8'))

    try:
        content = get(result['datos'])
    except exceptions.ConnectionError:
        logger.error('Collecting data from AEMET station %s failed due to the connection problem', station)
        return False

    if content.status_code not in http_ok:
        logger.error('Collecting data from AEMET station %s failed due to the return code', station, str(response.status))
        return False

    content = loads(content.text)

    result = dict()
    result['station'] = station
    result['issued'] = datetime.strptime(content[0]['elaborado'], "%Y-%m-%d").replace(tzinfo=tz).isoformat().replace('+00:00', 'Z')
    result['retrieved'] = datetime.now(tz).replace(tzinfo=tz).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

    content = sorted(content[0]['prediccion']['dia'], key=lambda k:(k['fecha']), reverse=False)

    result['today'] = content[0]
    result['tomorrow'] = content[1]

    return result


def decode_weather_type(item):

    """
    11 – Despejado
    11n – Despejado noche
    12 Poco nuboso
    12n – Poco nuboso noche
    13 – Intervalos nubosos
    13n – Intervalos nubosos noche
    14 – Nuboso
    14n – Nuboso noche
    15 – Muy nuboso
    16n – Muy nuboso
    16 – Cubierto
    16n – Cubierto
    17 – Nubes altas
    17n – Nubes altas noche
    23 – Intervalos nubosos con lluvia
    23n – Intervalos nubosos con lluvia noche
    24 – Nuboso con lluvia
    24n – Nuboso con lluvia noche
    25 – Muy nuboso con lluvia
    25n – Muy nuboso con lluvia
    26 – Cubierto con lluvia
    26n – Cubierto con lluvia
    33 – Intervalos nubosos con nieve
    33n – Intervalos nubosos con nieve noche
    34 – Nuboso con nieve
    34n – Nuboso con nieve noche
    35 – Muy nuboso con nieve
    35n – Muy nuboso con nieve
    36 – Cubierto con nieve
    36n – Cubierto con nieve
    43 – Intervalos nubosos con lluvia escasa
    43n – Intervalos nubosos con lluvia escasa noche
    44 – Nuboso con lluvia escasa
    44n – Nuboso con lluvia escasa noche
    45n – Muy nuboso con lluvia escasa
    46n – Cubierto con lluvia escasa
    51 – Intervalos nubosos con tormenta
    51n – Intervalos nubosos con tormenta noche
    52 – Nuboso con tormenta
    52n – Nuboso con tormenta noche
    53 – Muy nuboso con tormenta
    53n – Muy nuboso con tormenta
    54 – Cubierto con tormenta
    54n – Cubierto con tormenta
    61 – Intervalos nubosos con tormenta y lluvia escasa
    61n – Intervalos nubosos con tormenta y lluvia escasa noche
    62 Nuboso con tormenta y lluvia escasa
    62n – Nuboso con tormenta y lluvia escasa noche
    63 – Muy nuboso con tormenta y lluvia escasa
    63n – Muy nuboso con tormenta y lluvia escasa
    64 Cubierto con tormenta y lluvia escasa
    64n Cubierto con tormenta y lluvia escasa
    71 – Intervalos nubosos con nieve escasa
    71n – Intervalos nubosos con nieve escasa noche
    72 Nuboso con nieve escasa
    72n – Nuboso con nieve escasa noche
    73 – Muy nuboso con nieve escasa
    73n – Muy nuboso con nieve escasa
    74 Cubierto con nieve escasa
    74n Cubierto con nieve escasa
    """

    if item is None:
        return None

    if item == '11':
        return 'sunnyDay'

    if item == '11n':
        return 'cleanNight'

    if item.endswith('n'):
        trailing = ', night'
        item = item.split('n')[0]
    else:
        trailing = ''

    out = {
        '11': 'sunnyDay',
        '11n': 'clearNight',
        '12': 'slightlyCloudy',
        '13': 'partlyCloudy',
        '14': 'cloudy',
        '15': 'veryCloudy',
        '16': 'overcast',
        '17': 'highClouds',
        '23': 'partlyCloudy,lightRain',
        '24': 'cloudy,lightRain',
        '25': 'veryCloudy, lightRain',
        '26': 'overcast, lightRain',
        '33': 'partlyCloudy,snow',
        '34': 'cloudy, snow',
        '35': 'veryCloudy, snow',
        '36': 'overcast, snow',
        '43': 'partlyCloudy,drizzle',
        '44': 'cloudy, drizzle',
        '45': 'veryCloudy, drizzle',
        '46': 'overcast, drizzle',
        '51': 'partlyCloudy, thunder',
        '52': 'cloudy, thunder',
        '53': 'veryCloudy,thunder',
        '54': 'overcast, thunder',
        '61': 'partlyCloudy, thunder, lightRainShower',
        '62': 'cloudy, thunder, lightRainShower',
        '63': 'veryCloudy, thunder, lightRainShower',
        '64': 'overcast, thunder, lightRainShower',
        '71': 'partlyCloudy, lightSnow',
        '72': 'cloudy, lightSnow',
        '73': 'veryCloudy, lightSnow',
        '74': 'overcast, lightSnow'
        }.get(item, None)
    return (out + trailing) if out else None


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

    Speed of wind is 0: None
    """

    return {
        'Norte': 180,
        'Noroeste': 135,
        'Oeste': 90,
        'Suroeste': 45,
        'Sudoeste': 45,
        'Sur': 0,
        'Sureste': -45,
        'Sudeste': -45,
        'Este': -90,
        'Nordeste': -135,
        'Noreste': -135,
        'N': 180,
        'NO': 135,
        'O': 90,
        'SO': 45,
        'S': 0,
        'SE': -45,
        'E': -90,
        'NE': -135,
        'Calma': None,
        'C': None
    }.get(direction, None)


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
        logger.error('Posting data to Orion failed due to %s', item)

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
            await response.read()
    except client_exceptions.ClientConnectorError:
        return 'Posting data to Orion failed due to the connection problems'

    if response.status not in http_ok:
        return 'Posting data to Orion failed due to response code ' + str(response.status)

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
    id_local = source['station']

    for day in ['today', 'tomorrow']:

        ft_date = datetime.strptime(source[day]['fecha'],'%Y-%m-%d')
        for period in [0, 1, 2, 3]:

            item = deepcopy(template)
            valid_from = None
            valid_to = None

            if period == 0:
                valid_from = ft_date
                valid_to = ft_date + timedelta(hours=6)
            if period == 1:
                valid_from = ft_date + timedelta(hours=6)
                valid_to = ft_date + timedelta(hours=12)
            if period == 2:
                valid_from = ft_date + timedelta(hours=12)
                valid_to = ft_date + timedelta(hours=18)
            if period == 3:
                valid_from = ft_date + timedelta(hours=18)
                valid_to = ft_date + timedelta(hours=24)

            valid_from_iso = valid_from.astimezone(tz).isoformat().replace('+00:00', 'Z')
            valid_from_short = valid_from.strftime('%H:%M:%S%z')

            valid_to_iso = valid_to.astimezone(tz).isoformat().replace('+00:00', 'Z')
            valid_to_short = valid_to.strftime('%H:%M:%S%z')

            if latest:
                item['id'] = item['id'] + id_local + '_' + day + '_' + valid_from_short + '_' + valid_to_short
            else:
                item['id'] = item['id'] + id_local + '_' + valid_from_iso + '_' + valid_to_iso

            item['address']['value']['addressLocality'] = stations[id_local]['addressLocality']
            item['address']['value']['postalCode'] = stations[id_local]['postalCode']

            item['dateIssued']['value'] = source['issued']

            item['dateRetrieved']['value'] = source['retrieved']

            item['dayMaximum']['value']['feelsLikeTemperature'] = float(source[day]['sensTermica']['maxima'])

            item['dayMaximum']['value']['temperature'] = float(source[day]['temperatura']['maxima'])

            item['dayMaximum']['value']['relativeHumidity'] = float(source[day]['humedadRelativa']['maxima']) / 100

            item['dayMinimum']['value']['feelsLikeTemperature'] = float(source[day]['sensTermica']['minima'])

            item['dayMinimum']['value']['temperature'] = float(source[day]['temperatura']['minima'])

            item['dayMinimum']['value']['relativeHumidity'] = float(source[day]['humedadRelativa']['minima']) / 100

            item['feelsLikeTemperature']['value'] = float(source[day]['sensTermica']['dato'][period]['value'])

            item['precipitationProbability']['value'] = float(source[day]['probPrecipitacion'][period + 3]['value']) / 100

            item['relativeHumidity']['value'] = float(source[day]['humedadRelativa']['dato'][period]['value']) / 100

            item['temperature']['value'] = float(source[day]['temperatura']['dato'][period]['value'])

            item['validFrom']['value'] = valid_from_iso

            item['validTo']['value'] = valid_to_iso

            item['validity']['value'] = valid_from_iso + '/' + valid_to_iso

            item['weatherType']['value'] = decode_weather_type(source[day]['estadoCielo'][period + 3]['value'])

            item['windDirection']['value'] = decode_wind_direction(source[day]['viento'][period + 3]['direccion'])

            item['windSpeed']['value'] = round(float(source[day]['viento'][period + 3]['velocidad']) * 0.28, 2)

            result.append(item)

    return result


def reply_status():
    logger.info('Orion: %s', orion)
    logger.info('FIWARE Service: %s', service)
    logger.info('FIWARE Service-Path: %s', path)
    logger.info('Timeout: %s', str(timeout))
    logger.info('Stations: %s', str(len(stations)))
    logger.info('Latest: %s', str(latest))
    logger.info('limit_entities: %s', str(limit_entities))
    logger.info('Limit_source: %s', str(limit_source))
    logger.info('limit_target: %s', str(limit_target))
    logger.info('Log level: %s', args.log_level)
    logger.info('Started')


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
    source = None
    limit_off = False
    limit_on = False

    if 'include' in stations_limit:
        limit_on = True
    if 'exclude' in stations_limit:
        limit_off = True

    try:
        with open(stations_file, 'r') as f:
            source = load(f)

    except FileNotFoundError:
        logger.error('Station file is not present')
        exit(1)

    for station in source['municipalities']:
        check = True
        if limit_on:
            if station not in stations_limit['include']:
                check = False
        if limit_off:
            if station in stations_limit['exclude']:
                check = False

        if check:
            result[station] = dict()
            result[station]['postalCode'] = station
            result[station]['addressLocality'] = source['municipalities'][station]['name']
            result[station]['url'] = url_aemet.format(station)

    if limit_on:
        if len(result) != len(stations_limit['include']):
            logger.error('Errors in the list of municipalities detected')
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
                        help='YAML file with list of municipalities to be collected or excluded from collecting')
    parser.add_argument('--key',
                        action='store',
                        dest='key',
                        help='API Key to access to AEMET Open Data Portal',
                        required=True)
    parser.add_argument('--latest',
                        action='store_true',
                        default=default_latest,
                        dest='latest',
                        help='Collect only latest forecast')
    parser.add_argument('--limit-entities',
                        default=default_limit_entities,
                        dest='limit_entities',
                        help='Limit amount of entities per 1 request to Orion')
    parser.add_argument('--limit-source',
                        default=default_limit_source,
                        dest='limit_source',
                        help='Limit amount of parallel requests to AEMET')
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
                        help='Run as a service')

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
        res = run(collect(args.key))
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
