#!../bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from __future__ import print_function
import sys
import os
import xml.dom.minidom
import json
import re
import hashlib
import urllib2
import contextlib

DEFAULT_SOURCE_FOLDER =       'INECO'
BEACH_FOLDER =                '20170510_playas/playas'
MUSEUM_FOLDER =               '20170510_museos/museos'
TOURIST_INFO_FOLDER =         '20170510_oficinasturismo/oficina-turismo'

folders = [BEACH_FOLDER, MUSEUM_FOLDER, TOURIST_INFO_FOLDER]

categories_values = ['113', '311', '439']
categories_names = ['Beach', 'Museum', 'TouristInformationCenter']
cities = ['barcelona', 'coruna_a', 'malaga', 'sevilla', 'valencia']

description_nodes = ['TipoPlaya', 'TipoMuseo', 'TipoOficinaTurismo']
 
# Orion service that will store the data
orion_service = 'http://localhost:1030'

FIWARE_SERVICE = 'poi'
FIWARE_SPATH   = '/Spain'

MIME_JSON = 'application/json'

# Dictionary containing all the POIs
pois = { }

persisted_entities = 0
in_error_entities = 0

# Sanitize string to avoid forbidden characters by Orion
def sanitize(str_in):
  return re.sub(r"[<(>)\"\'=;\n\r]", "", str_in)

def transform_data(source_folder_param):
  index_poi_type = 0
  
  source_folder = source_folder_param
  if source_folder is None:
    source_folder = DEFAULT_SOURCE_FOLDER
  
  for folder in folders:
    poi_list = []
    pois[categories_names[index_poi_type]] = poi_list
    
    for city in cities: 
      city_folder = os.path.join(source_folder, folder, city)
      
      try:
        files = os.listdir(city_folder)
      except:
        continue
      
      num_processed = 0
      
      for a_file in files:
        full_file_path = os.path.join(city_folder, a_file)
        f = open(full_file_path, 'r')
        xml_data = f.read()
        f.close()
          
        DOMTree = xml.dom.minidom.parseString(xml_data).documentElement
        
        try:
          longitude = float(DOMTree.getElementsByTagName('longitud')[0].firstChild.nodeValue)
          latitude = float(DOMTree.getElementsByTagName('latitud')[0].firstChild.nodeValue)
        except:
          num_processed += 1
          continue
        
        municipality = sanitize(DOMTree.getElementsByTagName('municipio')[0].firstChild.nodeValue)
        province = sanitize(DOMTree.getElementsByTagName('provincia')[0].firstChild.nodeValue)
        
        id_input = categories_names[index_poi_type] + '-' + a_file + '-' + str(num_processed)
        m = hashlib.md5()
        m.update(id_input.decode())
        
        description_data = get_description(DOMTree, index_poi_type)
        
        name = description_data[0]
        description = description_data[1]
              
        poi_entity = {
          'id': categories_names[index_poi_type] + '-' + m.hexdigest(),
          'type': 'PointOfInterest',
          'name': {
            'value': name
          },
          'description': {
            'value': description
          },
          'category': {
            'type': 'List',
            'value': [
              categories_values[index_poi_type]
          ]},
          'location': {
            'type': 'geo:json',
            'value': {
              'type': 'Point',
              'coordinates': [longitude, latitude]
            }
          },
          'address': {
            'type': 'PostalAddress',
            'value': {
              'addressRegion': province,
              'addressLocality': municipality,
              'addressCountry': 'ES'
            }
          },
          'source': {
            'type': 'URL',
            'value': 'http://www.tourspain.es'
          },
          'dataProvider': {
            'value': 'FIWARE Foundation e.V.'
          }
        }
        
        poi_list.append(poi_entity)
        
        num_processed += 1
      
    index_poi_type += 1


# Obtains the POI description
def get_description(DOMTree, index_poi_type):
  description_node_name = description_nodes[index_poi_type]
  description = ''
  name = ''
  
  if description_node_name is None:
    return description
  
  tipo_nodes = DOMTree.getElementsByTagName(description_node_name)
  found = False
  
  for node in tipo_nodes:
    if found is True:
      break
    
    language = node.getAttribute('language')
    
    # Getting name
    if (language == 'es' or language == 'en'):
      candidate_name = node.getElementsByTagName('nombre')[1].firstChild.nodeValue
      # Give priority to name in Spanish
      if language == 'es' and len(candidate_name) > 0:
        name = sanitize(candidate_name).strip()
      elif language == 'en' and len(candidate_name) > 0 and len(name) == 0:
        name = sanitize(candidate_name).strip()
    
    # Obtaining a description in English or Spanish
    
      content_nodes = node.getElementsByTagName('content')
      for content_node in content_nodes:
        if content_node.firstChild != None and content_node.firstChild.nodeValue != None:
          text = content_node.firstChild.nodeValue
          text_filtered = text.strip()
          
          m = re.search('^\<p\>(.*?)\<\/p\>', text)
          if m != None:
            text_filtered = m.group(1).strip()
          else:
            m2 = re.search('^p(.*?)\/p', text)
            if m2 != None:
              text_filtered = m.group(1).strip()

          description = sanitize(text_filtered)
          # There are more spureous tags in the description
          # TODO: Remove any markup in the description by using an appropriate
          # regular expression
          description.replace('<strong>','').replace('</strong>','')
          if len(description) > 0:
            found = True
            break
       
  return (name, description)


def import_data():
  for poi_type in pois:
    poi_list = pois[poi_type]
    
    print(poi_type, len(poi_list))
    
    post_data(poi_list)


# POST data to an Orion Context Broker instance using NGSIv2 API
def post_data(data):
  if len(data) == 0:
    return
  
  payload = {
    'actionType': 'APPEND',
    'entities': data
  }
  
  data_as_str = json.dumps(payload)
  
  headers = {
    'Content-Type':   MIME_JSON,
    'Content-Length': len(data_as_str),
    'Fiware-Service': FIWARE_SERVICE,
    'Fiware-Servicepath': FIWARE_SPATH
  }
  
  req = urllib2.Request(url=(orion_service + '/v2/op/update'), data=data_as_str, headers=headers)
  
  try:
    with contextlib.closing(urllib2.urlopen(req)) as f:
      global persisted_entities
      persisted_entities = persisted_entities + 1
  except urllib2.URLError as e:
    global in_error_entities
    in_error_entities = in_error_entities + 1     



if __name__ == '__main__':
  transform_data(sys.argv[1])
  import_data()
  
  print("Persisted entities: ", persisted_entities)
  print("In error entities: ", in_error_entities)
