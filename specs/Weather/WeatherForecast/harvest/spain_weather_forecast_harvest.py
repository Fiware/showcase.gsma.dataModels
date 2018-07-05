#!bin/python
# -*- coding: utf-8 -*-

import urllib2
import xml.dom.minidom
import datetime
import json
import copy
from dateutil import parser
from pytz import timezone
import logging
import logging.handlers
import contextlib

country = 'Spain'
madrid_tz = timezone('CET')

MIME_JSON = 'application/json'
FIWARE_SERVICE = 'Weather'
FIWARE_SPATH = '/Spain'

# Orion service that will store the data
orion_service = 'http://localhost:1030'

postal_codes = {
    '47001': '47186',
    '28001': '28079',
    '39001': '39075',
    '34001': '34120',
    '34200': '34023',
    '05194': '05123',
    '33300': '33076',
    '41001': '41091',
    '46005': '46250',
    '08001': '08019',
    '50001': '50297',
    '38001': '38038',
    '35001': '35016',
    '29001': '29067',
    '07001': '07024',
    '15001': '15030'
}

localities = {
    'Valladolid': '47186',
    'Madrid': '28079',
    'Santander': '39075',
    'Palencia': '34120',
    u'Venta de Baños': '34023',
    'Mediana de Voltoya': '05123',
    'Villaviciosa': '33076',
    'Sevilla': '41091',
    'Valencia': '46250',
    'Barcelona': '08019',
    'Zaragoza': '50297',
    'Santa Cruz de Tenerife': '38038',
    'Las Palmas de Gran Canaria': '35016',
    'Malaga': '29067',
    'Formentera': '07024',
    u'Coruña, A': '15030'
}

# Statistics for tracking purposes
persisted_entities = 0
in_error_entities = 0

aemet_service = "http://www.aemet.es/xml/municipios/localidad_{}.xml"


def decode_wind_direction(direction):
    return {
        'Norte': 180,
        'Sur': 0,
        'Este': -90,
        'Oeste': 90,
        'Nordeste': -45,
        'Noroeste': 45,
        'Sureste': -135,
        'Suroeste': 135,
        'N': 180,
        'S': 0,
        'E': -90,
        'O': 90,
        'NE': -45,
        'NO': 45,
        'SE': -135,
        'SO': 135
    }.get(direction, None)

######


'''
GSMA enumerated values for weatherType

clearNight,
sunnyDay,
partlyCloudy,
mist,           --> neblina
fog,
cloudy,
lightRainShower,
drizzle,        --> llovizna
lightRain,
heavyRainShower,
heavyRain,
sleetShower,
sleet,         --> agua nieve
hailShower,
hail,          --> granizo
lightSnow,
shower,
lightSnow,
heavySnowShower,
heavySnow,
thunderShower,
thunder
'''


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


def get_weather_forecasted():
    # Indexed by postal code
    out = {}
    for postal_code in postal_codes:
        out[postal_code] = []

        param = postal_codes[postal_code]

        source = aemet_service.format(param)
        req = urllib2.Request(url=source)

        try:
            with contextlib.closing(urllib2.urlopen(req)) as f:
                xml_data = f.read()

                logger.debug('All AEMET data read for %s', postal_code)

                DOMTree = xml.dom.minidom.parseString(xml_data).documentElement

                address_locality = DOMTree.getElementsByTagName(
                    'nombre')[0].firstChild.nodeValue
                address = {}
                address['addressCountry'] = country
                address['postalCode'] = postal_code
                address['addressLocality'] = address_locality

                created = DOMTree.getElementsByTagName(
                    'elaborado')[0].firstChild.nodeValue

                forecasts = DOMTree.getElementsByTagName(
                    'prediccion')[0].getElementsByTagName('dia')

                for forecast in forecasts:
                    date = forecast.getAttribute('fecha')
                    normalizedForecast = parse_aemet_forecast(forecast, date)
                    counter = 1
                    for f in normalizedForecast:
                        f['type'] = 'WeatherForecast'
                        f['id'] = generate_id(
                            postal_code, country, f['validity']['value'])
                        f['address'] = {
                            'value': address,
                            'type': 'PostalAddress'
                        }
                        f['dateIssued'] = {
                            'type': 'DateTime',
                            'value': parser.parse(created).replace(
                                tzinfo=madrid_tz).isoformat()}
                        f['dateRetrieved'] = {
                            'type': 'DateTime',
                            'value': datetime.datetime.now(madrid_tz).replace(
                                microsecond=0).isoformat()}
                        f['source'] = {
                            'value': source,
                            'type': 'URL'
                        }
                        f['dataProvider'] = {
                            'value': 'FIWARE'
                        }
                        counter += 1
                        out[postal_code].append(f)
        except urllib2.URLError as e:
            logger.error(
                'Error while retrieving AEMET data for: %s. HTTP Error: %d',
                postal_code,
                e.code)

    return out


def parse_aemet_forecast(forecast, date):
    periods = {}
    out = []

    parsed_date = parser.parse(date)

    pops = forecast.getElementsByTagName('prob_precipitacion')
    for pop in pops:
        period = pop.getAttribute('periodo')
        if not period:
            period = '00-24'
        if pop.firstChild and pop.firstChild.nodeValue:
            insert_into_period(
                periods, period, 'precipitationProbability', float(
                    pop.firstChild.nodeValue) / 100.0)

    period = None
    weather_types = forecast.getElementsByTagName('estado_cielo')
    for weather_type in weather_types:
        period = weather_type.getAttribute('periodo')
        if not period:
            period = '00-24'
        if weather_type.firstChild and weather_type.firstChild.nodeValue:
            insert_into_period(
                periods, period, 'weatherType', decode_weather_type(
                    weather_type.getAttribute('descripcion')))
            insert_into_period(
                periods,
                period,
                'weatherType_ES',
                weather_type.getAttribute('descripcion'))

    period = None
    wind_data = forecast.getElementsByTagName('viento')
    for wind in wind_data:
        period = wind.getAttribute('periodo')
        if not period:
            period = '00-24'
        wind_direction = wind.getElementsByTagName('direccion')[0]
        wind_speed = wind.getElementsByTagName('velocidad')[0]
        if wind_speed.firstChild and wind_speed.firstChild.nodeValue:
            insert_into_period(periods, period, 'windSpeed', round(
                float(wind_speed.firstChild.nodeValue) * 0.28, 2))
        if wind_direction.firstChild and wind_direction.firstChild.nodeValue:
            insert_into_period(
                periods, period, 'windDirection', decode_wind_direction(
                    wind_direction.firstChild.nodeValue))

    temperature_node = forecast.getElementsByTagName('temperatura')[0]
    max_temp = float(temperature_node.getElementsByTagName(
        'maxima')[0].firstChild.nodeValue)
    min_temp = float(temperature_node.getElementsByTagName(
        'minima')[0].firstChild.nodeValue)
    get_parameter_data(temperature_node, periods, 'temperature')

    temp_feels_node = forecast.getElementsByTagName('sens_termica')[0]
    max_temp_feels = float(temp_feels_node.getElementsByTagName(
        'maxima')[0].firstChild.nodeValue)
    min_temp_feels = float(temp_feels_node.getElementsByTagName(
        'minima')[0].firstChild.nodeValue)
    get_parameter_data(temp_feels_node, periods, 'feelsLikeTemperature')

    humidity_node = forecast.getElementsByTagName('humedad_relativa')[0]
    max_humidity = float(humidity_node.getElementsByTagName(
        'maxima')[0].firstChild.nodeValue) / 100.0
    min_humidity = float(humidity_node.getElementsByTagName(
        'minima')[0].firstChild.nodeValue) / 100.0
    get_parameter_data(humidity_node, periods, 'relativeHumidity', 100.0)

    for period in periods:
        period_items = period.split('-')
        period_start = period_items[0]
        period_end = period_items[1]
        end_hour = int(period_end)
        end_date = copy.deepcopy(parsed_date)
        if end_hour > 23:
            end_hour = 0
            end_date = parsed_date + datetime.timedelta(days=1)

        start_date = parsed_date.replace(
            hour=int(period_start), minute=0, second=0)
        end_date = end_date.replace(hour=end_hour, minute=0, second=0)

        objPeriod = periods[period]

        valid_from = start_date.replace(tzinfo=madrid_tz).isoformat()
        valid_to = end_date.replace(tzinfo=madrid_tz).isoformat()

        objPeriod['validity'] = {
            'value': valid_from + '/' + valid_to,
            'type': 'Text'
        }

        # Custom fields as Orion Context Broker does not support ISO8601
        # intervals
        objPeriod['validFrom'] = {
            'value': valid_from,
            'type': 'DateTime'
        }
        objPeriod['validTo'] = {
            'value': valid_to,
            'type': 'DateTime'
        }

        maximum = {}
        objPeriod['dayMaximum'] = {
            'value': maximum
        }
        minimum = {}
        objPeriod['dayMinimum'] = {
            'value': minimum
        }

        maximum['temperature'] = max_temp
        minimum['temperature'] = min_temp

        maximum['relativeHumidity'] = max_humidity
        minimum['relativeHumidity'] = min_humidity

        maximum['feelsLikeTemperature'] = max_temp_feels
        minimum['feelsLikeTemperature'] = min_temp_feels

        out.append(objPeriod)

    return out


def get_parameter_data(node, periods, parameter, factor=1.0):
    param_periods = node.getElementsByTagName('dato')
    for param in param_periods:
        hour_str = param.getAttribute('hora')
        hour = int(hour_str)
        interval_start = hour - 6
        interval_start_str = '{:02}'.format(interval_start)
        period = interval_start_str + '-' + hour_str
        if param.firstChild and param.firstChild.nodeValue:
            param_val = float(param.firstChild.nodeValue)
            insert_into_period(periods, period, parameter, param_val / factor)


def insert_into_period(periods, period, attribute, value):
    if period not in periods:
        periods[period] = {}

    periods[period][attribute] = {
        'value': value
    }


def generate_id(postal_code, country, validity):
    # Remove timezone info from the validity string
    elements = validity.split('/')
    period_info = elements[0][0:elements[0].index(
        '+')] + '_' + elements[1][0:elements[1].index('+')]

    return country + '-' + 'WeatherForecast' + '-' + postal_code + '_' + period_info


def post_data(data):
    for a_postal_code in data:
        if len(data[a_postal_code]) == 0:
            continue

        data_obj = {
            'actionType': 'APPEND',
            'entities': data[a_postal_code]
        }
        data_as_str = json.dumps(data_obj)

        headers = {
            'Content-Type': MIME_JSON,
            'Content-Length': len(data_as_str),
            'Fiware-Service': FIWARE_SERVICE,
            'Fiware-Servicepath': FIWARE_SPATH
        }

        logger.debug(
            'Going to persist %s (%d) to %s', a_postal_code, len(
                data[a_postal_code]), orion_service)

        req = urllib2.Request(
            url=(
                orion_service +
                '/v2/op/update'),
            data=data_as_str,
            headers=headers)

        try:
            with contextlib.closing(urllib2.urlopen(req)) as f:  # noqa F841
                global persisted_entities
                persisted_entities += len(data[a_postal_code])
                logger.debug(
                    'Entities successfully created for postal code: %s',
                    a_postal_code)
        except urllib2.URLError as e:
            logger.error('Error!!! %s', a_postal_code)
            global in_error_entities
            logger.error(
                'Error while POSTing data to Orion: %d %s',
                e.code,
                e.read())
            logger.debug('Data which failed: %s', data_as_str)
            in_error_entities += 1


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_weather_forecast_spain.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('WeatherForecast')
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
    logger.debug('Number of localities known: %d', len(postal_codes.keys()))

    data = get_weather_forecasted()

    post_data(data)

    logger.debug('Number of entities persisted: %d', persisted_entities)
    logger.debug('Number of entities in error: %d', in_error_entities)
    logger.debug('#### Harvesting cycle finished ... ####')
