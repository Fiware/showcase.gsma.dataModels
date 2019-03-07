#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiohttp import ClientSession, client_exceptions
from argparse import ArgumentTypeError, ArgumentParser
from asyncio import Semaphore, ensure_future, gather, run
from copy import deepcopy
from datetime import datetime, timedelta
from json import dumps, load
from pytz import timezone
from re import sub
from requests import get, exceptions
from sys import stdout
from time import sleep
from xml.dom.minidom import parseString
from yaml import safe_load
import logging


default_latest = False
default_limit_entities = 50
default_limit_source = 10
default_limit_target = 50
default_log_level = 'INFO'
default_orion = 'http://orion:1026'
default_path = '/Spain'
default_service = 'weather'
default_timeout = -1

http_ok = [200, 201, 204]
log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None
matches = list()
stations = dict()
stations_file = 'stations.json'
tz_cet = timezone('Europe/Madrid')
tz_wet = timezone('Atlantic/Canary')
tz = timezone('UTC')
url_observation = "http://www.aemet.es/xml/municipios/localidad_{}.xml"
url_stations = ("https://raw.githubusercontent.com/"
                "FIWARE/dataModels/master/specs/PointOfInterest/WeatherStation/stations.json")

schema_template = {
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


def decode_weather_type(weather_type):
    if weather_type is None:
        return None

    param = weather_type.lower()

    trailing = ''
    if param.endswith('noche'):
        trailing = ', night'
        param = param[0:param.index('noche')].strip()

    out = {
        'despejado': 'sunnyDay',
        'poco nuboso': 'slightlyCloudy',
        'intervalos nubosos': 'partlyCloudy',
        'nuboso': 'cloudy',
        'muy nuboso': 'veryCloudy',
        'cubierto': 'overcast',
        'nubes altas': 'highClouds',
        'intervalos nubosos con lluvia escasa': 'partlyCloudy,drizzle',
        'nuboso con lluvia escasa': 'cloudy, drizzle',
        'muy nuboso con lluvia escasa': 'veryCloudy, drizzle',
        'cubierto con lluvia escasa': 'overcast, drizzle',
        'intervalos nubosos con lluvia': 'partlyCloudy,lightRain',
        'nuboso con lluvia': 'cloudy,lightRain',
        'muy nuboso con lluvia': 'veryCloudy, lightRain',
        'cubierto con lluvia': 'overcast, lightRain',
        'intervalos nubosos con nieve escasa': 'partlyCloudy, lightSnow',
        'nuboso con nieve escasa': 'cloudy, lightSnow',
        'muy nuboso con nieve escasa': 'veryCloudy, lightSnow',
        'cubierto con nieve escasa': 'overcast, lightSnow',
        'intervalos nubosos con nieve': 'partlyCloudy,snow',
        'nuboso con nieve': 'cloudy, snow',
        'muy nuboso con nieve': 'veryCloudy, snow',
        'cubierto con nieve': 'overcast, snow',
        'intervalos nubosos con tormenta': 'partlyCloudy, thunder',
        'nuboso con tormenta': 'cloudy, thunder',
        'muy nuboso con tormenta': 'veryCloudy,thunder',
        'cubierto con tormenta': 'overcast, thunder',
        'intervalos nubosos con tormenta y lluvia escasa': 'partlyCloudy, thunder, lightRainShower',
        'nuboso con tormenta y lluvia escasa': 'cloudy, thunder, lightRainShower',
        'muy nuboso con tormenta y lluvia escasa': 'veryCloudy, thunder, lightRainShower',
        'cubierto con tormenta y lluvia escasa': 'overcast, thunder, lightRainShower',
        'despejado noche': 'clearNight'}.get(param, None)
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
    result = dict()
    result['id'] = station
    result['forecasts'] = dict()

    try:
        async with session.get(stations[station]['url']) as response:
            content = await response.read()
    except client_exceptions.ClientConnectorError:
        logger.error('Harvesting info about station %s failed due to the connection problem', station)
        return False

    if response.status not in http_ok:
        logger.error('Harvesting info about station %s failed due to the return code %s', station, response.status)
        return False

    content = parseString(content).documentElement

    element = content.getElementsByTagName('elaborado')[0].firstChild.nodeValue
    result['issued'] = datetime.strptime(element, '%Y-%m-%dT%H:%M:%S')

    element = datetime.now().replace(microsecond=0)
    result['retrieved'] = element

    forecasts = content.getElementsByTagName('prediccion')[0].getElementsByTagName('dia')
    for forecast in forecasts:
        date = forecast.getAttribute('fecha')
        result['forecasts'][date] = dict()

        # uv
        element = forecast.getElementsByTagName('uv_max')
        if len(element) > 0:
            element = forecast.getElementsByTagName('uv_max')[0]

            if element.firstChild and element.firstChild.nodeValue:
                value = element.firstChild.nodeValue
            else:
                value = None

            result['forecasts'][date]['uv'] = value

        # precipitationProbability
        elements = forecast.getElementsByTagName('prob_precipitacion')
        for element in elements:
            period = element.getAttribute('periodo')
            if not period:
                period = '0-24'

            if period not in result['forecasts'][date]:
                result['forecasts'][date][period] = dict()

            if element.firstChild and element.firstChild.nodeValue:
                value = element.firstChild.nodeValue
            else:
                value = None

            result['forecasts'][date][period]['prob_precipitacion'] = value

        # weatherType
        elements = forecast.getElementsByTagName('estado_cielo')
        for element in elements:
            period = element.getAttribute('periodo')
            if not period:
                period = '0-24'

            if period not in result['forecasts'][date]:
                result['forecasts'][date][period] = dict()

            if element.firstChild and element.firstChild.nodeValue:
                value = element.getAttribute('descripcion')
            else:
                value = None

            result['forecasts'][date][period]['estado_cielo'] = value

        # windDirection, windSpeed
        elements = forecast.getElementsByTagName('viento')
        for element in elements:
            period = element.getAttribute('periodo')
            if not period:
                period = '0-24'

            if period not in result['forecasts'][date]:
                result['forecasts'][date][period] = dict()

            wind_direction = element.getElementsByTagName('direccion')[0]
            wind_speed = element.getElementsByTagName('velocidad')[0]

            if wind_speed.firstChild and wind_speed.firstChild.nodeValue:
                value = wind_speed.firstChild.nodeValue
            else:
                value = None

            result['forecasts'][date][period]['velocidad'] = value

            if wind_direction.firstChild and wind_direction.firstChild.nodeValue:
                value = wind_direction.firstChild.nodeValue
            else:
                value = None

            result['forecasts'][date][period]['direccion'] = value

        # temperature, feelsLikeTemperature, relativeHumidity
        for tag in ['temperatura', 'sens_termica', 'humedad_relativa']:
            # limits
            element = forecast.getElementsByTagName(tag)[0]
            result['forecasts'][date][tag] = dict()

            for subtag in ['maxima', 'minima']:
                if element.getElementsByTagName(subtag)[0].firstChild is not None:
                    value = element.getElementsByTagName(subtag)[0].firstChild.nodeValue
                else:
                    value = None
                result['forecasts'][date][tag][subtag] = value

            # periods
            elements = element.getElementsByTagName('dato')
            for element in elements:
                period = element.getAttribute('hora')

                if period not in result['forecasts'][date]:
                    result['forecasts'][date][period] = dict()

                if element.firstChild and element.firstChild.nodeValue:
                    value = float(element.firstChild.nodeValue)
                else:
                    value = None

                result['forecasts'][date][period][tag] = value

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
    tz_local = None
    ft_period = None
    valid_from = None
    valid_to = None

    today = datetime.now(tz).strftime("%Y-%m-%d")
    tomorrow = (datetime.now(tz) + timedelta(days=1)).strftime("%Y-%m-%d")

    if stations[id_local]['timezone'] == 'cet':
        tz_local = tz_cet
    if stations[id_local]['timezone'] == 'wet':
        tz_local = tz_wet

    issued = tz_local.localize(source['issued']).astimezone(tz).isoformat()
    retrieved = source['retrieved'].replace(tzinfo=tz).isoformat()

    for date in source['forecasts']:
        if date not in [today, tomorrow]:
            continue
        for period in ['06', '12', '18', '24']:
            item = deepcopy(schema_template)

            ft = source['forecasts'][date]

            ft_date = datetime.strptime(date + '00:00:00', '%Y-%m-%d%H:%M:%S')

            if period == '06':
                valid_from = tz_local.localize(ft_date)
                valid_to = tz_local.localize(ft_date + timedelta(hours=6))
                ft_period = '00-06'
            if period == '12':
                valid_from = tz_local.localize(ft_date + timedelta(hours=6))
                valid_to = tz_local.localize(ft_date + timedelta(hours=12))
                ft_period = '06-12'
            if period == '18':
                valid_from = tz_local.localize(ft_date + timedelta(hours=12))
                valid_to = tz_local.localize(ft_date + timedelta(hours=18))
                ft_period = '12-18'
            if period == '24':
                valid_from = tz_local.localize(ft_date + timedelta(hours=18))
                valid_to = tz_local.localize(ft_date + timedelta(hours=24))
                ft_period = '18-24'

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

            if ft['sens_termica']['maxima'] is not None:
                item['dayMaximum']['value']['feelsLikeTemperature'] = float(ft['sens_termica']['maxima'])

            if ft['temperatura']['maxima'] is not None:
                item['dayMaximum']['value']['temperature'] = float(ft['temperatura']['maxima'])

            if ft['humedad_relativa']['maxima'] is not None:
                item['dayMaximum']['value']['relativeHumidity'] = float(ft['humedad_relativa']['maxima']) / 100

            if ft['sens_termica']['minima'] is not None:
                item['dayMinimum']['value']['feelsLikeTemperature'] = float(ft['sens_termica']['minima'])

            if ft['temperatura']['minima'] is not None:
                item['dayMinimum']['value']['temperature'] = float(ft['temperatura']['minima'])

            if ft['humedad_relativa']['minima'] is not None:
                item['dayMinimum']['value']['relativeHumidity'] = float(ft['humedad_relativa']['minima']) / 100

            if ft[period]['sens_termica'] is not None:
                item['feelsLikeTemperature']['value'] = float(ft[period]['sens_termica'])

            if ft[ft_period]['prob_precipitacion'] is not None:
                item['precipitationProbability']['value'] = float(ft[ft_period]['prob_precipitacion']) / 100

            if ft[period]['humedad_relativa'] is not None:
                item['relativeHumidity']['value'] = float(ft[period]['humedad_relativa']) / 100

            if ft[period]['temperatura'] is not None:
                item['temperature']['value'] = float(ft[period]['temperatura'])

            item['validFrom']['value'] = valid_from

            item['validTo']['value'] = valid_to

            item['validity']['value'] = valid_from_iso + '/' + valid_to_iso

            if ft[ft_period]['estado_cielo'] is not None:
                item['weatherType']['value'] = decode_weather_type(ft[ft_period]['estado_cielo'])

            if ft[ft_period]['direccion'] is not None:
                item['windDirection']['value'] = decode_wind_direction(ft[ft_period]['direccion'])

            if ft[ft_period]['velocidad'] is not None:
                item['windSpeed']['value'] = round(float(ft[ft_period]['velocidad']) * 0.28, 2)

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


def setup_config_re(station):
    fix = sub('-', '', station.group()).strip()
    matches.append(fix)
    return "- '{}'\n".format(fix)


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
    resp = None
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
        try:
            logger.info('Station file is not present, trying to download it from the GitHub')
            resp = get(url_stations)
        except exceptions.ConnectionError:
            logger.error('Harvesting init data from the stations failed due to the connection problem')
            exit(1)

        if resp.status_code in http_ok:
            source = safe_load(resp.text)
            logger.info('Station file downloaded')
        else:
            logger.error('Harvesting init data from the stations failed due to the connection problem')
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
            p = source['municipalities'][station]['province']
            c = source['provinces'][p]['community']
            result[station] = dict()
            result[station]['postalCode'] = station
            result[station]['addressLocality'] = sanitize(source['municipalities'][station]['name'])
            result[station]['timezone'] = source['communities'][c]['timezone']
            result[station]['url'] = url_observation.format(station)

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
