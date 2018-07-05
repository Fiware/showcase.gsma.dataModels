'use strict';

const ORION_SERVER = 'http://130.206.83.68:1026/v1';

var csv = require('ya-csv');

var Orion = require('fiware-orion-client'),
    OrionClient = new Orion.Client({
      url: ORION_SERVER,
      userAgent: 'Test'
    });

function InsertTask(data) {
  this.data = data;
}

InsertTask.prototype.run = function() {
  console.log('Running: ', this.data);
  return OrionClient.updateContext(this.data);
};

console.log(typeof Promise.resolve);

function insertStations() {
  return new Promise(function(resolve, reject) {
    readCsv().then(function (data) {
      var adaptedData = adapt(data);
      
      var runnables = adaptedData.map(function(item) {
        return new InsertTask(item);
      });
      
      Promise.sequential(runnables).then(function(result) {
        resolve(result);
      }).catch(function(err) {
          console.error('Error inserting entities: ', err);
          reject(err);
      });
    }).catch(function(err) {
        console.error('Error while insert stations: ', err);
        reject(err);
    });
  });
}

function adapt(data) {
  return data.map(function(item) {
    var out = Object.create(null);
    out.id = 'WeatherStation' + '-' + 'ES' + '-' + item.ID;
    out.category = 'WeatherStation';
    out.type = 'PointOfInterest';
    
    out.location = new Orion.Attribute(item.Y + ',' + item.X, 'geo:point');
    // Avoid forbidden chars by Orion
    out.name = item.NOMBRE.replace(/'/g, '');
    
    out.postalAddress = {
      addressCountry: 'ES',
      // Avoid forbidden chars by Orion
      addressLocality: item.MUNICIPIO.replace(/'/g, ''),
      addressRegion: item.PROVINCIA
    };
    
    out.source = 'http://aemet.es';
    
    return out;
  });
}

function readCsv() {
  return new Promise(function(resolve, reject) {
    var collection = [];
    
    var reader = csv.createCsvFileReader('stations-normalized-wgs84.csv', {
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

// Run the passed runnables sequentially
Promise.sequential = function(runnables) {
  return new Promise(function(resolve, reject) {
    var results = [];
    var errors = [];

    runnables.reduce(function(sequence, aRunnable) {
      return sequence.then(function() {
        return aRunnable.run();
      }).then(function(data) {
          results.push(data);
          if (results.length + errors.length === runnables.length) {
            resolve({
              done: results,
              errors: errors
            });
          }
      }).catch(function(err) {
          console.error('Error while executing sequential op: ', err);
          errors.push({
            error: err,
            data: aRunnable.data
          });
      });
    }, Promise.resolve());
  });
};


insertStations().then(function(data) {
  console.log('Done: ', data.done.length, JSON.stringify(data.errors));
}).catch(function(err) {
    console.error('Error while inserting: ', err);
});