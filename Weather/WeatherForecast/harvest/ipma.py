# -*- coding: utf-8 -*-
"""
Gets weather forecast from the portuguese meteorological service, ipma.pt
"""
from __future__ import print_function

import urllib2
import json
from dateutil import parser
import datetime
import sys

iptma_codes = {
  'Lisboa': '1110600',
  'Porto':  '1131200',
  'Aveiro': '1010500'
}

weather_type_dict = {
  '1': 'Clear',
  '2': 'Slightly cloudy',
  '3': 'Partly Cloudy',
  '4': 'Overcast',
  '5': 'High clouds',
  '6': 'Light rain',
  '7': 'Drizzle',
  '11': 'Heavy rain',
  '9':  'Rain'
}

ipma_url = 'https://api.ipma.pt/json/alldata/{}.json'

def get_weather_forecasted_pt(locality):
  source = ipma_url.format(iptma_codes[locality])
  
  req = urllib2.Request(url=source)
  f = urllib2.urlopen(req)
  data = json.loads(f.read())
  
  print(data)
  out = []
  maxMinDay = { }
    
  for forecast in data:
    tMax = get_data(forecast, 'tMax')
    tMin = get_data(forecast, 'tMin')
    
    valid_from = parser.parse(forecast['dataPrev'])
    period = int(forecast['idPeriodo'])
    valid_to = valid_from + datetime.timedelta(hours=period)
    
    day = valid_from.date()
    key = day.isoformat()
    
    if key not in maxMinDay:
      maxMinDay[key] = { }
      
    if period == 24:
      maxMinDay[key]['tMax'] = tMax
      maxMinDay[key]['tMin'] = tMin
    
    if tMax is None:
      if 'tMax' in maxMinDay[key]:
        tMax =  maxMinDay[key]['tMax']  
  
    if tMin is None:
      if 'tMin' in maxMinDay[key]:
        tMin = maxMinDay[key]['tMin']
    
    now = datetime.datetime.now()
    
    if valid_to < now:
      continue
    
    # Only today's forecast
    day_now = now.date()
    day_wf = valid_to.date()
    
    if day_now != day_wf:
      continue
    
    obj = {
      'type': 'WeatherForecast',
      'feelsLikeTemperature': get_data(forecast, 'utci'),
      'temperature': get_data(forecast, 'tMed'),
    }
    
    if tMax is not None:
      obj['dayMaximum'] = {
        'temperature': tMax
      }
    
    if tMin is not None:
      obj['dayMinimum'] = {
        'temperature': tMin
      }
    
    hr = get_data(forecast, 'hR')
    if hr != None:
      hr = hr / 100
    else:
      hr = None
      
    obj['relativeHumidity'] = hr
    obj['dateCreated'] = forecast['dataUpdate']
    obj['validity'] = {
      'from': forecast['dataPrev'],
      'to':   valid_to.isoformat()
    }
    obj['address'] = {
      'addressCountry': 'PT',
      'addressLocality': locality
    }
    
    obj['windDirection'] = forecast['ddVento']
    obj['windSpeed'] = float(forecast['ffVento'])
    
    weather_type_id = str(forecast['idTipoTempo'])
    if weather_type_id in weather_type_dict:
      obj['weatherType'] = weather_type_dict[weather_type_id]
      
    obj['id'] = 'PT' + '-'  + locality + '-' + obj['validity']['from'] + '-' + obj['validity']['to']
      
    out.append(obj)
  
  return out


def get_data(forecast, item):
  value = float(forecast[item])
  if value == -99.0:
    value = None
  
  return value
