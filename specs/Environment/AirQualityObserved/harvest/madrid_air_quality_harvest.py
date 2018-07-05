#!../bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import datetime
import json
import urllib2
import StringIO
import logging
import logging.handlers
import re
from pytz import timezone
import contextlib
import copy


try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

# Entity type
AMBIENT_TYPE_NAME = 'AirQualityObserved'

# List of known air quality stations
station_dict = {}

# Orion service that will store the data
orion_service = 'http://localhost:1030'

logger = None

madrid_tz = timezone('CET')

pollutant_dict = {
    '01': 'SO2',
    '06': 'CO',
    '07': 'NO',
    '08': 'NO2',
    '09': 'PM2.5',
    '10': 'PM10',
    '12': 'NOx',
    '14': 'O3',
    '20': 'TOL',
    '30': 'BEN',
    '35': 'EBE',
    '37': 'MXY',
    '38': 'PXY',
    '39': 'OXY',
    '42': 'TCH',
    '43': 'CH4',
    '44': 'NHMC'
}

pollutant_descriptions = {
    '01': 'Sulfur Dioxide',
    '06': 'Carbon Monoxide',
    '07': 'Nitrogen Monoxide',
    '08': 'Nitrogen Dioxide',
    '09': 'Particles lower than 2.5',
    '10': 'Particles lower than 10',
    '12': 'Nitrogen oxides',
    '14': 'Ozone',
    '20': 'Toluene',
    '30': 'Benzene',
    '35': 'Etilbenzene',
    '37': 'Metaxylene',
    '38': 'Paraxylene',
    '39': 'Orthoxylene',
    '42': 'Total Hydrocarbons',
    '43': 'Hydrocarbons - Methane',
    '44': 'Non-methane hydrocarbons - Hexane'
}

other_dict = {
    '80': 'ultravioletRadiation',
    '81': 'windSpeed',
    '82': 'windDirection',
    '83': 'temperature',
    '86': 'relativeHumidity',
    '87': 'atmosphericPressure',
    '88': 'solarRadiation',
    '89': 'precipitation',
    '92': 'acidRainLevel'
}

other_descriptions = {
    '80': 'Ultraviolet Radiation',
    '81': 'Wind Speed',
    '82': 'Wind Direction',
    '83': 'temperature',
    '86': 'Relative Humidity',
    '87': 'Atmospheric Pressure',
    '88': 'Solar Radiation',
    '89': 'Precipitation',
    '92': 'Acid Rain Level'
}

dataset_url = 'http://datos.madrid.es/egob/catalogo/212531-7916318-calidad-aire-tiempo-real.txt'

# Statistics for tracking purposes
persisted_entities = 0
in_error_entities = 0

MIME_JSON = 'application/json'
FIWARE_SERVICE = 'AirQuality'
FIWARE_SPATH = '/Spain_Madrid'

# Sanitize string to avoid forbidden characters by Orion


def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;]", "", str_in)


# Obtains air quality data and harmonizes it, persisting to Orion
def get_air_quality_madrid():
    req = urllib2.Request(url=dataset_url)
    with contextlib.closing(urllib2.urlopen(req)) as f:
        csv_data = f.read()
        csv_file = StringIO.StringIO(csv_data)
        reader = csv.reader(csv_file, delimiter=',')

        # Dictionary with station data indexed by station code
        # An array per station code containing one element per hour
        stations = {}

        for row in reader:
            station_code = str(row[0]) + str(row[1]) + str(row[2])

            station_num = row[2]
            if not station_dict[station_num]:
                continue

            if station_code not in stations:
                stations[station_code] = []

            magnitude = row[3]

            if (magnitude not in pollutant_dict) and (
                    magnitude not in other_dict):
                continue

            is_other = None
            if magnitude in pollutant_dict:
                property_name = pollutant_dict[magnitude]
                property_desc = pollutant_descriptions[magnitude]
                is_other = False

            if magnitude in other_dict:
                property_name = other_dict[magnitude]
                property_desc = other_descriptions[magnitude]
                is_other = True

            hour = 0

            for x in xrange(9, 57, 2):
                value = row[x]
                value_control = row[x + 1]

                if value_control == 'V':
                    # A new entity object is created if it does not exist yet
                    if (len(stations[station_code]) < hour + 1):
                        stations[station_code].append(build_station(
                            station_num, station_code, hour, row))
                    elif ('id' not in stations[station_code][hour]):
                        stations[station_code][hour] = build_station(
                            station_num, station_code, hour, row)

                    param_value = float(value)

                    if not is_other:
                        unit_code = 'GQ'
                        if property_name == 'CO':
                            unit_code = 'GP'

                        measurand_data = [
                            property_name, str(param_value), unit_code, property_desc]
                        stations[station_code][hour]['measurand']['value'].append(
                            ','.join(measurand_data))
                    else:
                        if property_name == 'relativeHumidity':
                            param_value = param_value / 100

                    stations[station_code][hour][property_name] = {
                        'value': param_value
                    }
                else:
                    # ensure there are no holes in the data
                    if (len(stations[station_code]) < hour + 1):
                        stations[station_code].append({})

                hour += 1

            print(len(stations[station_code]))

        # Now persisting data to Orion Context Broker
        for station in stations:
            station_data = stations[station]
            data_array = []
            for data in station_data:
                if 'id' in data:
                    data_array.append(data)
            if len(data_array) > 0:
                logger.debug("Retrieved data for %s at %s (last hour)",
                             station, data_array[-1]['dateObserved']['value'])
                # Last measurement is duplicated to have an entity with the
                # latest measurement obtained
                last_measurement = data_array[-1]
                last_measurement['id'] = 'Madrid-AirQualityObserved-' + \
                    last_measurement['stationCode']['value'] + '-' + 'latest'
            else:
                logger.warn('No data retrieved for: %s', station)

            post_station_data(station, data_array)

#############


# Builds a new entity of type AirQualityObserved
def build_station(station_num, station_code, hour, row):
    station_data = {
        'type': AMBIENT_TYPE_NAME,
        'measurand': {
            'type': 'List',
            'value': []
        },
        'stationCode': {
            'value': station_code
        },
        'stationName': {
            'value': sanitize(station_dict[station_num]['name'])
        },
        'address': {
            'type': 'PostalAddress',
            'value': {
                'addressCountry': 'ES',
                'addressLocality': 'Madrid',
                'streetAddress': sanitize(station_dict[station_num]['address'])
            }
        },
        'location': {
            'type': 'geo:json',
            'value': station_dict[station_num]['location']['value'] or None
        },
        'source': {
            'type': 'URL',
            'value': 'http://datos.madrid.es'
        },
        'dataProvider': {
            'value': 'TEF'
        }
    }

    valid_from = datetime.datetime(int(row[6]), int(row[7]), int(row[8]), hour)
    station_data['id'] = 'Madrid-AirQualityObserved-' + \
        station_code + '-' + valid_from.isoformat()
    valid_to = (valid_from + datetime.timedelta(hours=1))

    # Adjust timezones
    valid_from = valid_from.replace(tzinfo=madrid_tz)
    valid_to = valid_to.replace(tzinfo=madrid_tz)

    station_data['validity'] = {
        'value': {
            'from': valid_from.isoformat(),
            'to': valid_to.isoformat()
        },
        'type': 'StructuredValue'
    }

    station_data['hour'] = {
        'value': str(hour) + ':' + '00'
    }

    observ_corrected_date = valid_from
    station_data['dateObserved'] = {
        'type': 'DateTime',
        'value': observ_corrected_date.isoformat()
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


# Reads station data from CSV file
def read_station_csv():
    with contextlib.closing(open('madrid_airquality_stations.csv', 'rU')) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        index = 0
        for row in reader:
            if index != 0:
                station_code = row[2]
                station_name = row[3]
                station_address = row[4]
                station_coords = {
                    'type': 'geo:json',
                    'value': {
                        'type': 'Point',
                        'coordinates': [float(row[0]), float(row[1])]
                    }
                }

                station_dict[station_code.zfill(3)] = {
                    'name': station_name,
                    'address': station_address,
                    'location': station_coords
                }
            index += 1

        station_dict['099'] = {
            'name': 'average',
            'address': None,
            'location': None
        }


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_madrid.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('Madrid')
    logger.setLevel(logging.DEBUG)

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logger()

    read_station_csv()

    logger.debug(
        '#### Starting a new harvesting and harmonization cycle ... ####')
    logger.debug(
        'Number of air quality stations known: %d', len(
            station_dict.keys()))

    get_air_quality_madrid()

    logger.debug('Number of entities persisted: %d', persisted_entities)
    logger.debug('Number of entities in error: %d', in_error_entities)
    logger.debug('#### Harvesting cycle finished ... ####')
