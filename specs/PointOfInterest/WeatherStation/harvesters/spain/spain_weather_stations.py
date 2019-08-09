#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This program collects information about Spain weather stations and Spain municipalities from AEMET and INE and
    prepares config that can be used by harvester itself to upload the list of Spain weather stations to
    Orion Context Broker or export data required by other weather harvesters:
      - https://github.com/FIWARE/dataModels/tree/master/specs/Weather/WeatherObserved
      - https://github.com/FIWARE/dataModels/tree/master/specs/Weather/WeatherForecast

    It also exports data to the CSV file (./stations.csv), that can be used to upload the list of weather stations
    to Google Maps:
      - https://www.google.com/maps/d/viewer?mid=1Sd5uNFd2um0GPog2EGkyrlzmBnEKzPQw .

    if AEMET data should be used, you must provide a valid API key, that can be obtained via email:
     - https://opendata.aemet.es/centrodedescargas/altaUsuario?.

    Legal notes:
      - http://www.aemet.es/en/nota_legal
      - http://ine.es/ss/Satellite?L=1&c=Page&cid=1254735849170&p=1254735849170&pagename=Ayuda%2FINELayout

    Examples:
      - get the list of stations from AEMET:
        curl -X GET --header 'Accept: application/json' --header "api_key: ${KEY}" \
            'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones'
      - get the list of Spain administrative units:
        curl -o list.zip \
            'http://www.ine.es/en/daco/inebase_mensual/febrero_2019/relacion_municipios_en.zip'

    AsyncIO name convention:
    async def name - entry point for asynchronous data processing/http requests and post processing
    async def name_bounded - intermediate step to limit amount of parallel workers
    async def name_one - worker process
"""

from aiohttp import ClientSession, ClientConnectorError
from asyncio import Semaphore, ensure_future, gather, run, TimeoutError as ToE, set_event_loop_policy
from argparse import ArgumentTypeError, ArgumentParser
from copy import deepcopy
from csv import DictWriter
from datetime import datetime
from io import BytesIO
from re import sub
from requests import get, exceptions
from sys import stdout
from uvloop import EventLoopPolicy
from xlrd import open_workbook
from yajl import loads, dumps
from yaml import safe_load as load, dump
from zipfile import ZipFile
import logging

default_limit_entities = 50           # amount of entities per 1 request to Orion
default_limit_targets = 50            # amount of parallel request to Orion
default_log_level = 'INFO'
default_orion = 'http://orion:1026'

http_ok = [200, 201, 204]

log_levels = ['ERROR', 'INFO', 'DEBUG']
logger = None
logger_req = None

stations_file_yml = 'stations.yml'   # destination file for yml format
stations_file_csv = 'stations.csv'   # destination file for csv format

tz_africa = 'Africa/Ceuta'
tz_europe = 'Europe/Madrid'
tz_atlantic = 'Atlantic/Canary'

url_aemet = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones'
url_ine = 'http://www.ine.es/en/daco/inebase_mensual/febrero_{}/relacion_municipios_en.zip'

template = {
    'id': 'urn:ngsi-ld:PointOfInterest:WeatherStation-ES-',
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
            'addressCountry': 'ES',
            'addressRegion': None,
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
        'type': 'Text',
        'value': 'http://www.aemet.es'
    },
}


def collect_aemet(key):
    logger.debug("Collection data from AEMET started")

    try:
        result = get(url_aemet, headers={'api_key': key})
    except exceptions.ConnectionError:
        logger.error('Collecting data from AEMET failed due to the connection problem')
        return False

    if result.status_code not in http_ok:
        logger.error('Collecting data from AEMET failed due to the return code')
        return False

    logger.debug('Remaining requests %s', result.headers.get('Remaining-request-count'))
    result = loads(result.text)

    try:
        result = get(result['datos'])
    except exceptions.ConnectionError:
        logger.error('Collecting data from AEMET failed due to the connection problem')
        return False

    if result.status_code not in http_ok:
        logger.error('Collecting data from AEMET failed due to the return code')
        return False

    result = loads(result.text)

    logger.debug("Collection data from AEMET ended")
    return result


def collect_ine():
    logger.debug("Collection data from INE started")

    response = None

    result = dict()
    result['provinces'] = list()
    result['communities'] = list()
    result['municipalities'] = list()

    year = datetime.now().year
    url = url_ine.format(year)

    try:
        response = get(url)
    except exceptions.ConnectionError:
        logger.error('Collecting data from INE failed due to the connection problem')
        exit(1)

    if response.status_code not in http_ok:
        logger.error('Collecting data from INE failed due to the connection problem')
        exit(1)

    with ZipFile(BytesIO(response.content)) as archive:
        for f in archive.filelist:
            if f.filename == 'DATOS/relacion_municipios_' + str(year) + '/' + str(year)[2:] + '_cod_ccaa.xls':
                wb = open_workbook(file_contents=archive.read(f))
                sheet = wb.sheet_by_index(0)
                for row in range(1, sheet.nrows):
                    if not sheet.cell_value(row, 0).isdigit():
                        continue

                    if sheet.cell_value(row, 1) == 'Canarias':
                        tz = tz_atlantic
                    elif sheet.cell_value(row, 1) in ['Ceuta', 'Melilla']:
                        tz = tz_africa
                    else:
                        tz = tz_europe

                    result['communities'].append({
                        'id': sheet.cell_value(row, 0),
                        'name': sheet.cell_value(row, 1),
                        'timezone': tz})
                result['communities'] = sorted(result['communities'], key=lambda k: k['id'])

            if f.filename == 'DATOS/relacion_municipios_' + str(year) + '/' + str(year)[2:] + '_cod_prov.xls':
                wb = open_workbook(file_contents=archive.read(f))
                sheet = wb.sheet_by_index(0)
                for row in range(1, sheet.nrows):
                    if not sheet.cell_value(row, 0).isdigit():
                        continue
                    result['provinces'].append({'id': sheet.cell_value(row, 0), 'name': sheet.cell_value(row, 1)})

                result['provinces'] = sorted(result['provinces'], key=lambda k: k['id'])

            if f.filename == 'DATOS/relacion_municipios_' + str(year) + '/' + str(year)[2:] + 'codmun_en.xlsx':
                wb = open_workbook(file_contents=archive.read(f))
                sheet = wb.sheet_by_index(0)
                for row in range(1, sheet.nrows):
                    if not sheet.cell_value(row, 0).isdigit():
                        continue
                    result['municipalities'].append({
                        'id': sheet.cell_value(row, 2),
                        'name': sheet.cell_value(row, 4),
                        'community': sheet.cell_value(row, 0),
                        'province': sheet.cell_value(row, 1)})

    logger.debug("Collection data from INE ended")
    return result


def convert_coordinates(coordinate):
    direction = 1

    if coordinate.endswith('S') or coordinate.endswith('W'):
        direction = -1

    degrees = int(coordinate[:2])
    minutes = int(coordinate[2:4])
    seconds = int(coordinate[4:6])

    return round((degrees + (minutes / 60) + (seconds / 3600)) * direction, 6)


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
            status = response.status
    except ClientConnectorError:
        return 'connection problem'
    except ToE:
        return 'timeout problem'

    if status not in http_ok:
        return 'response code ' + str(status)

    return True


async def prepare_data(aemet_data, ine_data):
    logger.debug('Data preparation started')

    tasks_municipality = list()
    tasks_forecast = list()
    result = dict()
    ine_san = dict()
    ine_san['provinces'] = dict()
    ine_san['communities'] = dict()
    ine_san['municipalities'] = dict()

    for item in ine_data['municipalities']:
        tasks_municipality.append(ensure_future(prepare_data_municipalities(item, ine_data)))

    logger.debug('Municipality preparation started')

    municipalities = await gather(*tasks_municipality)

    result['municipalities'] = dict()
    for item in municipalities:
        result['municipalities'][item['id']] = deepcopy(item)
        result['municipalities'][item['id']].pop('id')

    logger.debug('Municipality preparation ended')

    for item in aemet_data:
        tasks_forecast.append(ensure_future(prepare_data_forecasts(item, result['municipalities'])))

    logger.debug('Station preparation started')

    stations = await gather(*tasks_forecast)

    result['stations'] = dict()
    for item in stations:
        result['stations'][item['id']] = deepcopy(item)
        result['stations'][item['id']].pop('id')

    logger.debug('Station preparation ended')
    logger.debug('Data preparation ended')

    return result


async def prepare_data_forecasts(station, municipalities):

    result = dict()

    mapping = {
        'a coruña': 'Coruña, A',
        'alicante': 'Alicante/Alacant',
        'almeria': 'Almería',
        'araba/alava': 'Araba/Álava',
        'avila': 'Ávila',
        'caceres': 'Cáceres',
        'cadiz': 'Cádiz',
        'castellon': 'Castellón/Castelló',
        'cordoba': 'Córdoba',
        'illes balears': 'Balears, Illes',
        'jaen': 'Jaén',
        'la rioja': 'Rioja, La',
        'las palmas': 'Palmas, Las',
        'leon': 'León',
        'malaga': 'Málaga',
        'sta. cruz de tenerife': 'Santa Cruz de Tenerife',
        'valencia': 'Valencia/València'
    }

    result['id'] = station['indicativo']
    result['longitude'] = convert_coordinates(station['longitud'])
    result['latitude'] = convert_coordinates(station['latitud'])
    result['locality'] = sanitize(station['nombre']).title()
    result['province'] = sanitize(station['provincia']).lower()

    status = False

    # There is a difference in names in AEMET and INE sources, so fix it
    if result['province'] in mapping:
        result['province'] = mapping[result['province']]

    for municipality in municipalities:
        if municipalities[municipality]['province'].lower() == result['province'].lower():
            result['province'] = municipalities[municipality]['province']
            result['community'] = municipalities[municipality]['community']
            result['timezone'] = municipalities[municipality]['timezone']
            status = True

    if not status:
        logger.warning('Forecast, unknown province: %s', result['province'])

    return result


async def prepare_data_municipalities(municipality, ine_data):
    result = dict()

    result['id'] = municipality['province'] + str(municipality['id']).split('.')[0]
    result['name'] = sanitize(municipality['name'])
    for item in ine_data['provinces']:
        if item['id'] == municipality['province']:
            result['province'] = sanitize(item['name'])
    for item in ine_data['communities']:
        if item['id'] == municipality['community']:
            result['community'] = sanitize(item['name'])
            result['timezone'] = item['timezone']

    return result


async def prepare_schema(src_file, csv_flag=False):
    logger.debug('Schema preparation started')

    tasks = list()

    for item in src_file['stations']:
        task = ensure_future(prepare_schema_one(item, src_file['stations'][item], csv_flag))
        tasks.append(task)

    result = await gather(*tasks)

    logger.debug('Schema preparation finished')

    return result


async def prepare_schema_one(local_id, station, csv_flag):

    if not csv_flag:
        item = deepcopy(template)

        item['location']['value']['coordinates'] = [station['longitude'], station['latitude']]
        item['address']['value']['addressRegion'] = station['province']
        item['address']['value']['addressLocality'] = station['locality']
        item['id'] = item['id'] + local_id
    else:
        item = deepcopy(station)

        item['id'] = local_id
        item['country'] = 'ES'

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
    return sub(r"[<(>)\"\'=;]", "", str_in)


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
    parser.add_argument('--key',
                        action='store',
                        dest='key',
                        help='API Key to access to AEMET Open Data Portal')
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
        if not args.key:
            logger.error('API Key is not provided')
            exit(1)

        logger.debug('Initial data collection started')

        aemet = collect_aemet(args.key)
        ine = collect_ine()

        res = run(prepare_data(aemet, ine))

        logger.debug('Initial data collection ended')
    else:
        try:
            with open(stations_file_yml, 'r') as file:
                res = load(file)

        except FileNotFoundError:
            logger.error('Station file is not present')
            exit(1)

    if args.csv:
        fieldnames = ['id', 'country', 'community', 'province', 'locality', 'latitude', 'longitude', 'timezone']

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
