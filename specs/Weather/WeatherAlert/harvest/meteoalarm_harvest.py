# -*- coding: utf-8 -*-

"""
Get Europe WeatherAlarms as offered by Meteoalarm.eu
"""

import StringIO
import re
import urllib2
import xml.dom.minidom
import datetime
import json
import argparse
import logging
import logging.handlers
import unicodedata
import contextlib

awareness_type_dict = {
    '1': 'wind',
    '2': 'snow/ice',
    '3': 'thunderstorms',
    '4': 'fog',
    '5': 'highTemperature',
    '6': 'lowTemperature',
    '7': 'coastalEvent',
    '8': 'forestFire',
    '9': 'avalanches',
    '10': 'rain',
    '11': 'flood',
    '12': 'rain/flood'
}

awareness_level_dict = {
    '': 'informational',
    '1': 'low',
    '2': 'medium',
    '3': 'high',
    '4': 'critical'
}

weather_alarms = "http://www.meteoalarm.eu/documents/rss/{}.rss"

reg_exp = re.compile('<img(?P<group>.*?)>')

countries_to_retrieve = []


# Sanitize string to avoid forbidden characters by Orion
def sanitize(str_in):
    aux = re.sub(r"[<(>)\"\'=;-]", "", str_in)
    return unicodedata.normalize('NFD', aux).encode('ascii', 'ignore')


def get_weather_alarms(country):
    source = weather_alarms.format(country.lower())

    logger.debug("Going to GET %s", source)

    req = urllib2.Request(url=source)
    f = urllib2.urlopen(req)

    xml_data = f.read()
    final_data = xml_data
    DOMTree = xml.dom.minidom.parseString(final_data).documentElement

    out = []

    items = DOMTree.getElementsByTagName('item')[1:]

    alarm_index = -1

    for item in items:
        description = item.getElementsByTagName(
            'description')[0].firstChild.nodeValue
        # Enable description parsing
        description = description.replace('&nbsp;', '')
        description = re.sub(reg_exp, '<img\g<group>></img>', description)

        zone = item.getElementsByTagName(
            'title')[0].firstChild.nodeValue.strip()
        uid = item.getElementsByTagName('guid')[0].firstChild.nodeValue
        pub_date_str = item.getElementsByTagName(
            'pubDate')[0].firstChild.nodeValue
        pub_date = datetime.datetime.strptime(
            pub_date_str[:-6], '%a, %d %b %Y %H:%M:%S').isoformat()

        # It is needed to encode description as it is already unicode
        parsed_content = xml.dom.minidom.parseString(
            description.encode('utf-8')).documentElement
        rows = parsed_content.getElementsByTagName('tr')

        for row in rows:
            columns = row.getElementsByTagName('td')
            for column in columns:
                # img column contains the awareness level and type
                img_aux = column.getElementsByTagName('img')
                if img_aux.length > 0:
                    awareness_str = img_aux[0].getAttribute('alt')
                    alarm_data = parse_alarm(awareness_str)

                    if alarm_data['level'] > 1:
                        alarm_index += 1
                        obj = {
                            'type': 'Alert',
                            'category': {
                                'type': 'Property',
                                'value': 'weather'
                            },
                            'id': 'WeatherAlert-{}-{}'.format(uid, alarm_index),
                            'subCategory': {
                                'type': 'Property',
                                'value': alarm_data['awt']
                            },
                            'severity': {
                                'type': 'Property',
                                'value': alarm_data['levelColor']
                            },
                            'address': {
                                'type': 'Property',
                                'value': {
                                    'type': 'PostalAddress',
                                    'addressCountry': country.upper(),
                                    'addressRegion': sanitize(zone)
                                }
                            },
                            'alertSource': {
                                'type': 'Property',
                                'value': 'http://www.meteoalarm.eu'
                            },
                            'dateIssued': {
                                'value': pub_date,
                                'type': 'DateTime'
                            }
                        }
                        out.append(obj)
                else:
                    dates = column.getElementsByTagName('i')
                    if dates.length > 0:
                        valid_from_str = dates[0].firstChild.nodeValue
                        valid_to_str = dates[1].firstChild.nodeValue

                        valid_from = datetime.datetime.strptime(
                            valid_from_str, '%d.%m.%Y %H:%M %Z').isoformat()
                        valid_to = datetime.datetime.strptime(
                            valid_to_str, '%d.%m.%Y %H:%M %Z').isoformat()

                        out[alarm_index]['validFrom'] = {
                            'type': 'DateTime',
                            'value': valid_from
                        }
                        out[alarm_index]['validTo'] = {
                            'type': 'DateTime',
                            'value': valid_to
                        }

    out = remove_duplicates(out)
    return out


def remove_duplicates(array_data):
    # Dictionary for duplicate checking
    alarms_duplicates = {}
    out = []

    for data in array_data:
        key = ('{address[value][addressCountry]}{address[value][addressRegion]}'
               '{severity[value]}{subCategory[value]}'
               '{validFrom[value]}{validTo[value]}').format(**data)

        if key not in alarms_duplicates:
            alarms_duplicates[key] = data
            out.append(data)

    return out


def parse_alarm(alarm_string):
    elements = alarm_string.split(' ')
    awt = elements[0].split(':')[1]
    level = elements[1].split(':')[1]
    return {
        'level': int(level) if level else -1,
        'levelColor': awareness_level_dict.get(level, ''),
        'awt': awareness_type_dict.get(awt, '')
    }


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_weather_alarms.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('WeatherAlarms')
    logger.setLevel(logging.DEBUG)

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def persist_entities(data):
    data_to_be_persisted = data

    data_obj = {
        'actionType': 'APPEND',
        'entities': data_to_be_persisted
    }
    data_as_str = json.dumps(data_obj)

    headers = {
        'Content-Type': 'application/json',
        'Content-Length': len(data_as_str)
    }

    if fiware_service:
        headers['Fiware-Service'] = fiware_service

    if fiware_service_path:
        headers['Fiware-Servicepath'] = fiware_service_path

    req = urllib2.Request(
        url=(
            orion_service +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    try:
        with contextlib.closing(urllib2.urlopen(req)) as f:
            logger.debug('Entities successfully created')
    except urllib2.URLError as e:
        logger.error('Error!!!')
        logger.error(
            'Error while POSTing data to Orion: %d %s',
            e.code,
            e.read())
        logger.debug('Data which failed: %s', data_as_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Weather alarm harvester')
    parser.add_argument('--service', metavar='service',
                        type=str, help='FIWARE Service', required=True)
    parser.add_argument('--service-path', metavar='service_path',
                        type=str, nargs='?', help='FIWARE Service Path')
    parser.add_argument('--endpoint', metavar='endpoint',
                        type=str, required=True, help='Context Broker end point. Example. http://orion:1030')
    parser.add_argument('countries', metavar='countries', type=str, nargs='+',
                        help='Country Codes separated by spaces. ')

    args = parser.parse_args()

    fiware_service_path = None

    if args.service:
        fiware_service = args.service
        print('Fiware-Service: ' + fiware_service)

    if args.service_path:
        fiware_service_path = args.service_path
        print('Fiware-Servicepath: ' + fiware_service_path)

    if args.endpoint:
        orion_service = args.endpoint
        print('Context Broker: ' + orion_service)

    for s in args.countries:
        countries_to_retrieve.append(s)

    setup_logger()

    for c in countries_to_retrieve:
        logger.debug("Going to retrieve data from country: %s", c)
        alarms = get_weather_alarms(c)
        logger.debug("Going to persist data from country: %s", c)
        persist_entities(alarms)
