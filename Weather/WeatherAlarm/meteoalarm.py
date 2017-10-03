# -*- coding: utf-8 -*-

"""
Get Europe WeatherAlarms as offered by Meteoalarm.eu
"""

import StringIO
import re
from flask import jsonify, request, Response
import urllib2
import xml.dom.minidom
import datetime
import json

awareness_type_dict = {
    '1': 'Wind',
    '2': 'Snow/Ice',
    '3': 'Thunderstorms',
    '4': 'Fog',
    '5': 'Extreme High Temperature',
    '6': 'Extreme Low Temperature',
    '7': 'Coastal Event',
    '8': 'Forest Fire',
    '9': 'Avalanches',
    '10': 'Rain',
    '11': 'Flood',
    '12': 'Rain-Flood'
}

awareness_level_dict = {
    '': 'White',
    '1': 'Green',
    '2': 'Yellow',
    '3': 'Orange',
    '4': 'Red'
}

weather_alarms = "http://www.meteoalarm.eu/documents/rss/{}.rss"

reg_exp = re.compile('<img(?P<group>.*?)>')


def get_weather_alarms(request):
    query = request.args.get('q')

    if not query:
        return Response(json.dumps([]), mimetype='application/json')

    tokens = query.split(';')

    country = ''

    for token in tokens:
        items = token.split(':')
        if items[0] == 'country':
            country = items[1].lower()

    source = weather_alarms.format(country)
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
                            'type': 'WeatherAlarm',
                            'id': 'WeatherAlarm' + '-' + uid + '-' + str(alarm_index),
                            'validity': {
                                'from': '',
                                'to': ''},
                            'awarenessType': alarm_data['awt'],
                            'awarenessLevel': alarm_data['levelColor'],
                            'address': {
                                'addressCountry': country.upper(),
                                'addressRegion': zone},
                            'source': 'http://www.meteoalarm.eu',
                            'dateCreated': pub_date}
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

                        out[alarm_index]['validity']['from'] = valid_from
                        out[alarm_index]['validity']['to'] = valid_to

    out = remove_duplicates(out)
    return Response(json.dumps(out), mimetype='application/json')


def remove_duplicates(array_data):
    # Dictionary for duplicate checking
    alarms_duplicates = {}
    out = []

    for data in array_data:
        key = data['address']['addressCountry'] + data['address']['addressRegion'] +\
            data['awarenessLevel'] + data['awarenessType'] +\
            data['validity']['from'] + data['validity']['to']

        if key not in alarms_duplicates:
            alarms_duplicates[key] = data
            out.append(data)

    return out


def parse_alarm(alarm_string):
    elements = alarm_string.split(' ')
    awt = elements[0].split(':')[1]
    level = elements[1].split(':')[1]

    if level:
        level_num = int(level)
    else:
        level_num = -1

    out = {
        'level': level_num,
        'levelColor': '',
        'awt': ''
    }

    if level in awareness_level_dict:
        out['levelColor'] = awareness_level_dict[level]

    if awt in awareness_type_dict:
        out['awt'] = awareness_type_dict[awt]

    return out
