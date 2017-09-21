# -*- coding: utf-8 -*-
"""
Gets weather forecast from the portuguese meteorological service, ipma.pt
"""

from __future__ import with_statement
import urllib2
import json
from dateutil import parser
import datetime
import sys
from pytz import timezone
import logging
import logging.handlers
import contextlib

# Orion service that will store the data
orion_service = 'http://localhost:1030'

# Statistics for tracking purposes
persisted_entities = 0
in_error_entities = 0


country = 'Portugal'
lisbon_tz = timezone('WET')

MIME_JSON = 'application/json'
FIWARE_SERVICE = 'Weather'
FIWARE_SPATH =   '/Portugal'


iptma_codes = {
  'Lisboa': '1110600',
  'Porto':  '1131200',
  'Aveiro': '1010500'
}


def decode_wind_direction(direction):
  dictionary = {
    'N': 180,
    'S': 0,
    'E': -90,
    'W': 90,
    'NE': -45,
    'NW': 45,
    'SE': -135,
    'SW': 135
  }
  
  if direction in dictionary: 
    return dictionary[direction]
  else: return None



weather_type_dict = {
  '1': 'clear',
  '2': 'slightlyCloudy',
  '3': 'partlyCloudy',
  '4': 'overcast',
  '5': 'highClouds',
  '6': 'lightRain',
  '7': 'drizzle',
  '11': 'heavyRain',
  '9':  'rain'
}

ipma_url = 'https://api.ipma.pt/json/alldata/{}.json'

def get_weather_forecasted():
  data = { }
  
  for locality in iptma_codes:
    code = iptma_codes[locality]
    
    data[code] = get_weather_forecasted_pt(locality)
    
  return data


def get_weather_forecasted_pt(locality):
  source = ipma_url.format(iptma_codes[locality])
  
  req = urllib2.Request(url=source)
  f = urllib2.urlopen(req)
  data = json.loads(f.read())
  
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
      'feelsLikeTemperature': {
        'value': get_data(forecast, 'utci')
      },
      'temperature': {
        'value': get_data(forecast, 'tMed')
      }
    }
    
    if tMax is not None:
      obj['dayMaximum'] = {
        'value': {
          'temperature': tMax
        }
      }
    
    if tMin is not None:
      obj['dayMinimum'] = {
        'value': {
          'temperature': tMin
        }
      }
    
    hr = get_data(forecast, 'hR')
    if hr != None:
      hr = hr / 100
    else:
      hr = None
      
    obj['relativeHumidity'] = {
      'value': hr
    }
    obj['dateIssued'] = {
      'value': forecast['dataUpdate'],
      'type': 'DateTime'
    }
    obj['dateRetrieved'] = {
      'type': 'DateTime',
      'value': datetime.datetime.now(lisbon_tz).replace(microsecond=0).isoformat()
    }
    obj['validFrom'] =  {
      'value': forecast['dataPrev'],
      'type': 'DateTime'
    }
    obj['validTo'] =    {
      'value': valid_to.isoformat(),
      'type': 'DateTime'
    }
    obj['validity'] =   {
      'value': obj['validFrom']['value'] + '/' + obj['validTo']['value']
    }
    obj['address'] = {
      'value': {
        'addressCountry': 'PT',
        'addressLocality': locality
      },
      'type': 'PostalAddress'
    }
    
    obj['windDirection'] = {
      'value': decode_wind_direction(forecast['ddVento'])
    }
    obj['windSpeed'] = {
      'value': float(forecast['ffVento']) * 0.28
    }
    
    weather_type_id = str(forecast['idTipoTempo'])
    if weather_type_id in weather_type_dict:
      obj['weatherType'] = {
        'value': weather_type_dict[weather_type_id]
      }
      
    obj['id'] = 'Portugal' + '-' + 'WeatherForecast' + '-'  + locality + '_' + obj['validFrom']['value'] + '_' + obj['validTo']['value']
    obj['source'] = {
      'type': 'URL',
      'value': 'https://www.ipma.pt'
    }
      
    out.append(obj)
  
  return out


def get_data(forecast, item):
  value = float(forecast[item])
  if value == -99.0:
    value = None
  
  return value

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
      'Content-Type':   MIME_JSON,
      'Content-Length': len(data_as_str),
      'Fiware-Service': FIWARE_SERVICE,
      'Fiware-Servicepath': FIWARE_SPATH
    }
  
    logger.debug('Going to persist %s (%d) to %s', a_postal_code, len(data[a_postal_code]), orion_service)
    
    req = urllib2.Request(url=(orion_service + '/v2/op/update'), data=data_as_str, headers=headers)
    
    try:
      with contextlib.closing(urllib2.urlopen(req)) as f:
        global persisted_entities
        persisted_entities = persisted_entities + len(data[a_postal_code])
        logger.debug('Entities successfully created for postal code: %s', a_postal_code)
    except urllib2.URLError as e:
      logger.error('Error!!! %s', a_postal_code)
      global in_error_entities
      logger.error('Error while POSTing data to Orion: %d %s', e.code, e.read())
      logger.debug('Data which failed: %s', data_as_str)
      in_error_entities = in_error_entities + 1


def setup_logger():
  global logger
  
  LOG_FILENAME = 'harvest_weather_forecast_portugal.log'

  # Set up a specific logger with our desired output level
  logger = logging.getLogger('WeatherForecast')
  logger.setLevel(logging.DEBUG)

  #  Add the log message handler to the logger
  handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000000, backupCount=3)
  formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
  handler.setFormatter(formatter)
  
  logger.addHandler(handler)
  
     
if __name__ == '__main__':
  setup_logger()
  
  logger.debug('#### Starting a new harvesting and harmonization cycle ... ####') 
  logger.debug('Number of localities known: %d', len(iptma_codes.keys()))
  
  data = get_weather_forecasted()
  
  post_data(data)
  
  logger.debug('Number of entities persisted: %d', persisted_entities)
  logger.debug('Number of entities in error: %d', in_error_entities)
  logger.debug('#### Harvesting cycle finished ... ####')
