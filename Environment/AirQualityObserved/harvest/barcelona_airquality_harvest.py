#!../bin/python
# -*- coding: utf-8 -*-

'''
  Peforms a data harvesting of air quality official data from the city of Barcelona.

  Data source is Catalonia's Government (http://dtes.gencat.cat/)

  Copyright (c) 2016 Telefónica Investigación y Desarrollo S.A.U.

  LICENSE: MIT

'''

from __future__ import with_statement
from __future__ import print_function
import datetime
import json
import urllib2
import logging
import logging.handlers
import re
from pytz import timezone
import contextlib

import sys

AIRQUALITY_TYPE_NAME = 'AirQualityObserved'

FIWARE_SERVICE = 'AirQuality'
FIWARE_SPATH = '/Spain_Barcelona'

MIME_JSON = 'application/json'

# Orion service that will store the data
orion_service = 'http://localhost:1030'

barcelona_tz = timezone('CET')

pollutant_descriptions = {
    'SO2': 'Sulfur Dioxide',
    'CO': 'Carbon Monoxide',
    'NO': 'Nitrogen Monoxide',
    'NO2': 'Nitrogen Dioxide',
    'PM2.5': 'Particles less than 2.5',
    'PM10': 'Particles less than 10',
    'NOx': 'Nitrogen oxides',
    'O3': 'Ozone',
    'TOL': 'Toluene',
    'BEN': 'Benzene',
    'C6H6': 'Benzene',
    'EBE': 'Etilbenzene',
    'MXY': 'Metaxylene',
    'PXY': 'Paraxylene',
    'OXY': 'Orthoxylene',
    'TCH': 'Total Hydrocarbons',
    'CH4': 'Hydrocarbons (Methane)',
    'NHMC': 'Non-methane hydrocarbons (Hexane)'
}

# Station codes of the Barcelona metropolitan area
station_codes = ['08019050', '08015021', '08019044', '08019004', '08019042',
                 '08089005', '08019057', '08019054', '08019043',
                 '08194008', '08169009', '08169008', '08101001',
                 '08245012', '08263007', '08263001', '08211004', '08221004',
                 '08301004']

# Provides air quality station information (probably in the future we are
# not going to need this call)
dataset_url = 'http://dtes.gencat.cat/icqa/AppJava/getEstacio.do?codiEOI={}'
# Provides per hour data for the current day, per station
dataset_url2 = 'http://dtes.gencat.cat/icqa/AppJava/getDadesDiaries.do?codiEOI={}'

persisted_entities = 0
in_error_entities = 0


# Sanitize string to avoid forbidden characters by Orion
def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;]", "", str_in)


# Retrieves all the data from the target stations
def get_air_quality_barcelona(target_stations):
    # Will keep all the data indexed by station code
    # An array with one element per hour
    entity_data = {}

    f = f2 = None
    for station in target_stations:
        entity_data[station] = []

        logger.debug('Going to harvest data coming from : %s', station)

        service_url1 = dataset_url.format(station)

        # Request to obtain station data
        station_req = urllib2.Request(
            url=service_url1, headers={
                'Accept': MIME_JSON})
        try:
            f = urllib2.urlopen(station_req)
        except urllib2.URLError as e:
            logger.error('Error while calling: %s : %s', service_url1, e)
            if f is not None:
                f.close()
            continue

        # deal with wrong encoding
        json_str = f.read().replace("'", '"')
        data = json.loads(json_str, encoding='ISO-8859-15')
        f.close()

        service_url2 = dataset_url2.format(station)
        # Request to obtain pollutants data
        data_req = urllib2.Request(
            url=service_url2, headers={
                'Accept': MIME_JSON})
        try:
            f2 = urllib2.urlopen(data_req)
        except urllib2.URLError as e:
            logger.error('Error while calling: %s : %s', service_url2, e)
            if f2 is not None:
                f2.close()
            continue

        logger.debug("All data from %s retrieved properly", station)

        # deal with wrong encoding
        json_pollutants_str = f2.read().replace("'", '"')
        pollutant_data_st = json.loads(
            json_pollutants_str, encoding='ISO-8859-15')
        f2.close()

        station_code = data['codiEOI']

        pollutant_data = pollutant_data_st['contaminants']

        for pollutant_info in pollutant_data.values():
            values = pollutant_info['dadesMesuresDiaria']
            # It comes with units between parenthesis
            pollutant_name = pollutant_info['abreviatura'].split('(')[0]
            pollutant_unit = 'GQ'
            if pollutant_name == 'CO':
                pollutant_unit = 'GP'

            counter = 0
            hour = 0
            for v in values:
                if v['valor'] != '':
                    # Last three values are averages and should be discarded
                    if counter >= (len(values) - 3):
                        break

                    hour = counter
                    station_data = None
                    if len(entity_data[station_code]) > hour:
                        station_data = entity_data[station_code][hour]

                    if station_data is None:
                        station_data = build_station(station_code, data)
                        entity_data[station_code].append(station_data)
                        # 'data' in catalan is 'date'
                        observ_date = datetime.datetime.strptime(
                            pollutant_data_st['data'], '%d/%m/%Y')
                        observ_date = observ_date.replace(
                            hour=hour, minute=0, second=0, microsecond=0)

                        # Include proper timezone info
                        observ_corrected_date = observ_date.replace(
                            tzinfo=barcelona_tz)

                        station_data['dateObserved'] = {
                            'value': observ_corrected_date.isoformat(),
                            'type': 'DateTime'
                        }

                        # Entity id corresponds to the observed date starting
                        # period (in local time)
                        station_data['id'] = 'Barcelona-AirQualityObserved' + \
                            '-' + station_code + '-' + observ_date.isoformat()

                        # Convenience data for filtering by target hour
                        station_data['hour'] = {
                            'value': str(hour) + ':' + '00'
                        }

                    value = v['valor']

                    measurand_data = [
                        pollutant_name,
                        value,
                        pollutant_unit,
                        pollutant_descriptions[pollutant_name]]
                    station_data['measurand']['value'].append(
                        ','.join(measurand_data))
                    station_data[pollutant_name] = {
                        'value': float(value)
                    }

                counter += 1

        if len(entity_data[station]) > 0:
            logger.debug("Retrieved data for %s at %s (last hour)",
                         station, entity_data[station][-1]['dateObserved']['value'])
        else:
            logger.warn('No data found for station: %s', station)

    # Now persisting data to Orion Context Broker
    for a_station in entity_data:
        data_for_station = entity_data[a_station]
        print(len(data_for_station))
        if len(data_for_station):
            last_measurement = data_for_station[-1]
            last_measurement['id'] = 'Barcelona-AirQualityObserved' + \
                '-' + last_measurement['stationCode']['value'] + '-' + 'latest'

        post_station_data(a_station, data_for_station)


def build_station(station_code, data):
    station_data = {
        'type': AIRQUALITY_TYPE_NAME,
        'stationCode': {
            'value': station_code
        },
        'stationName': {
            'value': sanitize(data['nom'])
        },
        'address': {
            'value': {
                'addressCountry': 'ES',
                'addressLocality': sanitize(data['municipi']),
                'streetAddress': sanitize(data['direccioPostal'])
            },
            'type': 'PostalAddress'
        },
        'location': {
            'value': {
                'type': 'Point',
                'coordinates': [float(data['longitud']), float(data['latitud'])]
            },
            'type': 'geo:json',
        },
        # Source of the data Generalitat of Catalonia
        'source': {
            'value': 'http://dtes.gencat.cat/',
            'type': 'URL'
        },
        # Provider operator TEF
        'dataProvider': {
            'value': 'TEF'
        },
        'measurand': {
            'value': [],
            'type': 'List'
        }
    }

    return station_data


# POST data to an Orion Context Broker instance using NGSIv2 API
def post_station_data(station_code, data):
    if len(data) == 0:
        return

    payload = {
        'actionType': 'APPEND',
        'entities': data
    }

    data_as_str = json.dumps(payload)

    headers = {
        'Content-Type': MIME_JSON,
        'Content-Length': len(data_as_str),
        'Fiware-Service': FIWARE_SERVICE,
        'Fiware-Servicepath': FIWARE_SPATH
    }

    req = urllib2.Request(
        url=(
            orion_service +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    logger.debug(
        'Going to persist %s to %s - %d',
        station_code,
        orion_service,
        len(data))

    try:
        with contextlib.closing(urllib2.urlopen(req)) as f:
            global persisted_entities
            logger.debug("Entity successfully created: %s", station_code)
            persisted_entities = persisted_entities + 1
    except urllib2.URLError as e:
        global in_error_entities
        logger.error(
            'Error while POSTing data to Orion: %d %s',
            e.code,
            e.read())
        logger.debug('Data which failed: %s', data_as_str)
        in_error_entities = in_error_entities + 1


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_barcelona.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('Barcelona')
    logger.setLevel(logging.DEBUG)

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logger()

    logger.debug(
        '#### Starting a new harvesting and harmonization cycle ... ####')
    logger.debug(
        'Number of air quality stations known: %d',
        len(station_codes))

    get_air_quality_barcelona(station_codes)

    logger.debug('Number of entities persisted: %d', persisted_entities)
    logger.debug('Number of entities in error: %d', in_error_entities)
    logger.debug('#### Harvesting cycle finished ... ####')
