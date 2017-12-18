'use strict';

/* Sets up all the data needed for smart parking in Santander */

const ORION_SERVER = 'http://localhost:1026/v1';
const ORION_SERVER_V2 = 'http://localhost:1026/v2';

const SANTANDER_SERVER = 'http://mu.tlmat.unican.es:8099/v1';

var csv = require('ya-csv');
var Request = require('request');

var Orion = require('fiware-orion-client'),
    OrionClient = new Orion.Client({
      url: ORION_SERVER,
      userAgent: 'Test',
      service: 'Santander',
      servicePath: 'parking'
    }),
    SantanderClient = new Orion.Client({
      url: SANTANDER_SERVER,
      userAgent: 'Test',
      service: 'smartsantander'
    });

function setupConfig() {
  return new Promise(function(resolve, reject) {
    
    console.log('Starting process ...');
    
    var sensor2Polygon = Object.create(null);
    var polygon2Sensor = Object.create(null);
  
    var obj = null;
    readCsv('sensors_polygons_refined.csv').then(function(data) {
      console.log('CSV read');
      
      data.forEach(function(aRecord) {
        var sensorId = aRecord.id;
        var polygonId = aRecord.sensor_id;
        sensor2Polygon[sensorId] = polygonId;
        if (!polygon2Sensor[polygonId]) {
          polygon2Sensor[polygonId] = [];
        }
        polygon2Sensor[polygonId].push(sensorId);
      });
      
      obj = {
        'sensor2Polygon': sensor2Polygon,
        'polygon2Sensor': polygon2Sensor
      };
      
      console.log('Data: ', JSON.stringify(obj));
      
      return OrionClient.updateContext({
        type: 'santander:smartparking:config',
        id:   'parking_config_1',
        data: obj
      });
    }).then(function() {
        resolve(obj);
    }).catch(reject);
  });
}

function readCsv(file) {
  return new Promise(function(resolve, reject) {
    var collection = [];
    
    var reader = csv.createCsvFileReader(file, {
      'columnsFromHeader': true,
      'separator': ','
    });
    
    reader.addListener('data', function(data) {
      collection.push(data);
    });
    
    reader.addListener('end', function() {
      resolve(collection);
    });
    
    reader.addListener('error', function() {
      reject();
    });
  });
}

function readJson(file) {
  var fs = require('fs');
  var obj = JSON.parse(fs.readFileSync(file, 'utf8'));
  
  return obj;
}

function createEntitiesV2(entityList) {
  console.log(JSON.stringify(entityList));
  
  return new Promise(function(resolve, reject) {
    Request.post({
      baseUrl: ORION_SERVER_V2,
      url: '/op/update/',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Fiware-Service': 'santander',
        'Fiware-Servicepath': '/parking'
      },
      body: {
        "actionType": "APPEND",
        "entities": entityList
      },
      json: true
    }, function(err, response, body) {
        console.log('Here ...');
        if (err) {
          console.error('Error while creating: ', err);
          reject(err);
          return;
        }
        if (response.statusCode !== 204) {
          console.error('Error while creating: ', body);
          reject(body.description);
        }
        resolve();
    });
  });
}

process.on('uncaughtException', function(error) {
  console.error('Error: '. JSON.stringify(error));
});

// Iterates over the street parking list (polygon GeoJSON)

setupConfig().then(function(config) {
  console.log('Data updated properly');
  
  var data = readJson('polygons_geojson_refined.geojson');
  // Array to hold the list of entities to be created
  var entitiesToCreate = [];
  // Array fo promises for querying sensor status
  var querySensorStatus = [];
  
  data.features.forEach(function(aFeature) {
    var properties = aFeature.properties;
    var polygonId = properties.sensor_id;
    
    var obj = {
      id:   'santander' + ':' + polygonId,
      type: 'OnStreetParking',
      allowedVehicles: {
        value: ['Car']
      },
      totalSpotNumber: {
        value: config.polygon2Sensor[polygonId].length
      }
    };
    
    var coordinates = aFeature.geometry.coordinates;
    
    obj.location = {
      value: {
        type: 'Polygon',
        coordinates: coordinates
      },
      type: 'geo:json'
    };
    entitiesToCreate.push(obj);
    
    console.log(obj);
    
    var sensors = config.polygon2Sensor[polygonId];
    var queryData = [];
    sensors.forEach(function(aSensor) {
      queryData.push({
        id: aSensor
      });
    });
    
    console.log(JSON.stringify(queryData));
    
    // Enquee a promise to get status
    querySensorStatus.push(SantanderClient.queryContext(queryData,{
      path: '/parking/#'
    }));
  });
  
  Promise.all(querySensorStatus).then(function(results) {
    console.log('Promise.all finished: ', results.length, entitiesToCreate.length);
    
    entitiesToCreate.forEach(function(aEntity, index) {
      console.log(index);
      if (index == 27) {
        console.log(aEntity);
      }
      var freeSpots = aEntity.totalSpotNumber.value;
      var sensorData = results[index];
      if (sensorData) {
        sensorData.forEach(function (aSensor) {
          if (aSensor['presenceStatus:parking'] === 'true') {
              freeSpots--;
          }
        });
      }
      aEntity.availableSpotNumber = {
        value: freeSpots
      };
      aEntity.dateUpdated = {
        value: new Date(),
        type: 'DateTime'
      };
    });
    
    console.log('Going to create entities');
    
    return createEntitiesV2(entitiesToCreate);
    // return OrionClient.updateContext(entitiesToCreate);
  
  }).then(function() {
      console.log('Santander street parking created OK');
    }).catch(function(err) {
        console.error('Error while setting up Santander data', err);
    });
}).catch(function(err) {
    console.error('Error while setting up configuration: ', err);
});
