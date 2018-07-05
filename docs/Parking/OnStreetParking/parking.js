'use strict';

/* Exports all parking sensors from Santander */

const SANTANDER_SERVER = 'http://mu.tlmat.unican.es:8099/v1';

var Orion = require('fiware-orion-client'),
    OrionTestBedClient = new Orion.Client({
      url: SANTANDER_SERVER,
      userAgent: 'Test',
      service: 'smartsantander'
    });

var csv = require('ya-csv');

function getParkingData() {
  var query = {
    pattern: 'urn:x-iot:smartsantander:u7jcfa:fixed:np.*'
  };
  
  OrionTestBedClient.queryContext(query, {
    path: '/parking/#',
    limit: 1000
  }).then(function(result) {
    var writer = csv.createCsvStreamWriter(process.stdout);
    if (result !== null) {
      // Take element 0 to determine keys
      var keys = Object.keys(result[0]);
      keys.push('latitude');
      keys.push('longitude');
      writer.writeRecord(keys);
      result.forEach(function(aSensor) {
        var data = [];
        Object.keys(aSensor).forEach(function(aKey) {
          data.push(aSensor[aKey]);
        });
        var geoCoords = aSensor.position.split(',');
        data.push(geoCoords[0]);
        data.push(geoCoords[1]);
        writer.writeRecord(data);
      });
    }
    else {
      console.log('No data found');
    }
  }).catch(function(err) {
      console.  error('Error while querying parking data: ', err);
  });
}

getParkingData();