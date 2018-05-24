#!../bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import datetime
import json
from flask import Flask, jsonify, request, Response
import urllib2
import StringIO

import sys

import ngsi_helper

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

app = Flask(__name__)

AMBIENT_TYPE_NAME = 'AmbientObserved'

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
    '09': 'Particles < 2.5',
    '10': 'Particles < 10',
    '12': 'Nitrogen oxides',
    '14': 'Ozone',
    '20': 'Toluene',
    '30': 'Benzene',
    '35': 'Etilbenzene',
    '37': 'Metaxylene',
    '38': 'Paraxylene',
    '39': 'Orthoxylene',
    '42': 'Total Hydrocarbons',
    '43': 'Hydrocarbons (Methane)',
    '44': 'Non-methane hydrocarbons (Hexane)'
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
orion_service = 'http://130.206.83.68:1026/v1/queryContext'


@app.route('/v1/queryContext', methods=['POST'])
def query_context():
    msg = json.dumps(request.get_json())
    # A post to Orion is issued in order to get the concerned entities

    req = urllib2.Request(url=orion_service, data=msg,
                          headers={
                              'Content-Type': 'application/json',
                              'Accept': 'application/json'
                          })
    f = urllib2.urlopen(req)
    orion_response = json.loads(f.read())
    f.close()

    elements = ngsi_helper.parse(orion_response)

    if len(elements) > 0:
        now = datetime.datetime.now()
        if now.minute < 30:
            target_hour = now.hour - 2
        else:
            target_hour = now.hour - 1

        if(target_hour < 0):
            target_hour = 0

        station_list = []
        for element in elements:
            station_code = element['id'].split('-')[2]
            station_list.append(station_code)

        entities = get_air_quality_madrid(station_list, target_hour)
    else:
        entities = []

    return Response(json.dumps(entities, sort_keys=True),
                    mimetype='application/json')


@app.route('/v2/entities', methods=['GET'])
def v2_end_point():
    entity_type = request.args.get('type')
    query = request.args.get('q')

    station_code = ''
    target_hour = -1
    if query:
        tokens = query.split(';')

        for token in tokens:
            items = token.split(':')
            if items[0] == 'stationCode':
                station_code = items[1].lower()
            elif items[0] == 'hour':
                target_hour = int(items[1])

    if entity_type == AMBIENT_TYPE_NAME:
        station_codes = None
        if station_code:
            station_codes = [station_code]

        return Response(
            json.dumps(
                get_air_quality_madrid(
                    station_codes,
                    target_hour),
                sort_keys=True),
            mimetype='application/json')
    else:
        return Response(json.dumps([]), mimetype='application/json')


def get_air_quality_madrid(target_stations, target_hour=-1):
    req = urllib2.Request(url=dataset_url)
    f = urllib2.urlopen(req)

    csv_data = f.read()
    csv_file = StringIO.StringIO(csv_data)
    reader = csv.reader(csv_file, delimiter=',')

    stations = {}

    for row in reader:
        station_code = str(row[0]) + str(row[1]) + str(row[2])
        if station_code and target_stations and station_code not in target_stations:
            continue

        station_num = row[2]
        if not station_dict[station_num]:
            continue

        if station_code not in stations:
            stations[station_code] = []

        magnitude = row[3]

        if (magnitude not in pollutant_dict) and (magnitude not in other_dict):
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

        print('processing')
        sys.stdout.flush()

        hour = 0
        for x in xrange(9, 57, 2):
            value = row[x]
            value_control = row[x + 1]
            if len(stations[station_code]) < hour + 1:
                station_data = {
                    'type': AMBIENT_TYPE_NAME,
                    'pollutants': {},
                    'stationCode': station_code,
                    'stationName': station_dict[station_num]['name'],
                    'address': {
                        'addressCountry': 'ES',
                        'addressLocality': 'Madrid',
                        'streetAddress': station_dict[station_num]['address']
                    },
                    'location': station_dict[station_num]['location'] or None,
                    'source': 'http://datos.madrid.es'
                    # According to read-only nature of dateCreated, it must not be added
                    #'dateCreated': datetime.datetime.now().isoformat()
                }
                valid_from = datetime.datetime(
                    int(row[6]), int(row[7]), int(row[8]), hour)
                valid_to = (valid_from + datetime.timedelta(hours=1))

                station_data['validity'] = {
                    'from': valid_from.isoformat(),
                    'to': valid_to.isoformat()
                }
                station_data['id'] = 'Madrid-AmbientObserved-' + \
                    station_code + '-' + valid_from.isoformat()

                stations[station_code].append(station_data)

            if value_control == 'V':
                param_value = float(value)

                if not is_other:
                    if property_name == 'CO':
                        param_value = param_value * 1000

                    stations[station_code][hour]['pollutants'][property_name] = {
                        'description': property_desc,
                        'concentration': param_value
                    }
                else:
                    stations[station_code][hour][property_name] = param_value
            hour += 1

    # Returning data as an array
    station_list = []

    for station in stations:
        index_from = 0
        index_to = len(station_data)
        station_data = stations[station]
        if target_hour != -1:
            index_from = target_hour
            index_to = index_from + 1

        data_list = station_data[index_from:index_to]

        for data in data_list:
            if data['pollutants'] or 'temperature' in data:
                station_list.append(data)
    return station_list


station_dict = {}


def read_station_csv():
    with open('madrid_airquality_stations.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        index = 0
        for row in reader:
            if index != 0:
                station_code = row[2]
                station_name = row[3]
                station_address = row[4]
                station_coords = {
                    'type': 'geo:point',
                    'value': row[1] + ',' + row[0]
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


if __name__ == '__main__':
    read_station_csv()
    app.run(host='0.0.0.0', port=1029, debug=True)
