'use strict';

/* Sets up all the data needed for Madrid Ambient Data */

const ORION_SERVER = 'http://130.206.83.68:1026/v1';
const SERVER_ADDRESS = '130.206.83.68';     // Needed for providing data
const AIR_QUALITY_SERVER = 'http://130.206.83.68:1029/v1';

var csv = require('ya-csv');

var fs = require('fs');

var Orion = require('fiware-orion-client'),
    OrionClient = new Orion.Client({
      url: ORION_SERVER,
      userAgent: 'Test'
    }),
    AirQualityClient = new Orion.Client({
      url: AIR_QUALITY_SERVER,
      userAgent: 'experimental'
    });

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

// Provider registration for the 'boilerStatus' attribute
function registerProvider(forceCreate) {
  return Promise.resolve();
  /*
  return new Promise(function (resolve, reject) {
    var FILE_REGISTRATION = 'registration.id';
    var registrationId;
    try {
      registrationId = fs.readFileSync(__dirname + '/' + FILE_REGISTRATION,
                                       'UTF-8');
    }
    catch(e) {
      console.log('Registration id not present');
    }

    var registration = {
      pattern: 'Madrid-AmbientObserved-.*',
      type: 'AmbientObserved',
      attributes: ['temperature']
    };

    var options = {
      callback: 'http://' + SERVER_ADDRESS + ':' + '1029' + '/ngsi10/data'
    };

    if (registrationId && !forceCreate) {
      console.log('Using existing registration id: ', registrationId);
      options.registrationId = registrationId;
    }

    OrionClient.registerContext(registration, options).then(function(data) {
      if (!data) {
        reject({
          code: 404
        });
        return;
      }

      fs.writeFileSync(__dirname + '/' + FILE_REGISTRATION,
                       data.registrationId);
      resolve(data.registrationId);

    }).catch(function(err) {
      reject(err);
    });
  });
  */
}

function zpad(number, numZeroes) {
  var strNumber = number + '';
  var outArray = [];
  for(var j = 0; j < strNumber.length; j++) {
    outArray.push(strNumber.charAt(j));
  }
  
  while (outArray.length < numZeroes) {
    outArray.unshift('0');
  }
  
  return outArray.join('');
}

function loadAmbientData() {
  return new Promise(function(resolve, reject) {
    readCsv('madrid_airquality_stations.csv').then(function(data) {
      var entitiesToBeCreated = [];
      
      data.forEach(function(aStation) {
        var location = aStation.Y + ', ' + aStation.X;
         
        var ambientObserved = {
          type: 'AmbientObserved',
          location: new Orion.Attribute(location, 'geo:point'),
          id: 'Madrid-AmbientObserved-' + '28079' + zpad(aStation['NÚMERO'],3),
          source: 'http://datos.madrid.es'
        };
        
        var airQualityStation = {
          type: 'PointOfInterest',
          id: 'AirQualityStation' + '-' + 'ES' + '-' + 'Madrid' + '-' + zpad(aStation['NÚMERO'],3),
          location: new Orion.Attribute(location, 'geo:point'),
          category: 'AirQualityStation',
          name: aStation['ESTACIÓN'],
          address: {
            addressCountry: 'ES',
            addressLocality: 'Madrid',
            streetAddress: aStation['DIRECCIÓN'].replace(/[\(\)]/g, '')
          },
          source: 'http://datos.madrid.es'
        };
        
        // Add here the capabilities of the station
        
        entitiesToBeCreated.push(ambientObserved);
        entitiesToBeCreated.push(airQualityStation);
      });
      
      // Average ambient observed
      entitiesToBeCreated.push({
        type: 'AmbientObserved',
        id: 'Madrid-AmbientObserved-' + '099',
      });
      
      console.log(JSON.stringify(entitiesToBeCreated));
      
      return OrionClient.updateContext(entitiesToBeCreated);
    
    }).then(function(result) {
        console.log('Ambient data loaded OK');
        return registerProvider();
    }).then(function() {
        console.log('Provider registered properly');
        resolve();
    }).catch(function(err) {
        console.error('Error: ', err);
        reject(err);
    });
  });  
}

loadAmbientData().then(function() {
  return AirQualityClient.queryContext({
    type: 'AmbientObserved'
  }, {
      location: {
        coords:  '40.423279, -3.712402',
        geometry: 'Circle',
        radius: 1000
      }
  });
}).then(function(result) {
    console.log(JSON.stringify(result));
});
