#!bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask, jsonify, request, Response
import urllib2
import StringIO
import csv
import datetime
import json

weather_observed = "http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_{}_datos-horarios.csv?k=cle&l={}&datos=det&w=0&f=temperatura&x=h6"

def get_data(row, index, conversion=float, factor=1.0):
  out = None
  
  value = row[index]
  if(value != ''):
    out = conversion(value) / factor
    
  return out

def get_weather_observed(request):    
    query = request.args.get('q')
    
    if not query:
      return Response(json.dumps([]), mimetype='application/json')
    
    tokens  = query.split(';')
    
    station_code = ''
    country = ''
    
    for token in tokens:
      items = token.split(':')
      if items[0] == 'stationCode':
        station_code = items[1]
      elif items[0] == 'country':
        country = items[1]
    
    if not station_code or not country or country != 'ES':
      return Response(json.dumps([]), mimetype='application/json')
    
    source = weather_observed.format(station_code, station_code)
    
    req = urllib2.Request(url=source)
    f = urllib2.urlopen(req)
    csv_data = f.read()
    
    csv_file = StringIO.StringIO(csv_data)
    reader = csv.reader(csv_file, delimiter=',')
    
    out = []
    index = 0
    for row in reader:
      if index == 0:
        address = row[0]
        
      if index < 4:
        index += 1
        continue
      
      print(row)
      
      observation = {
        'type': 'WeatherObserved'
      }
      if len(row) < 2:
        continue
      
      observation['temperature'] = get_data(row, 1)
      observation['windSpeed'] = get_data(row, 2, int)
      observation['windDirection'] = row[3] or None
      observation['precipitation'] = get_data(row, 6)
      observation['pressure'] = get_data(row, 7)
      observation['pressureTendency'] =  get_data(row, 8)
      observation['relativeHumidity'] = get_data(row, 9, factor=100.0)
      
      observation['dateObserved'] = datetime.datetime.strptime(row[0], '%d/%m/%Y %H:%M').isoformat()
      observation['source'] = 'http://www.aemet.es'
      observation['address'] = {
        'addressLocality': address.decode('latin-1'),
        'addressCountry': country
      }
      
      out.append(observation)
    
    print(out)
    return Response(json.dumps(out), mimetype='application/json')