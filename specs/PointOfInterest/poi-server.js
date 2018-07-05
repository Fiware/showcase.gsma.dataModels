const PORT = 1050;    // Port on which the proxy will be listening to

var URL = require('url');
var fs = require('fs');

var Orion = require('fiware-orion-client');
var OrionHelper = Orion.NgsiHelper;

var OportoOST = require('./oporto-ost-module.js');

var loggerStream = fs.createWriteStream('./log.txt', {
  flags: 'a',
  encoding: 'utf-8',
  mode: '0666'
});

var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');

var app = express();

app.use(morgan('dev',{
  stream: loggerStream
}));

app.use(bodyParser.json());

var typesMap = {
  'PointOfInterest': 'pois'
};

var categoriesMap = {
  'OffStreetParking':         '418',
  'Restaurant':               '347',
  'Hotel':                    '436',
  'Museum':                   '311',
  'Beach':                    '113',
  'TouristInformationCenter': '439'
};

app.get('/v2/entities', function (req, resp) {
  var type = req.query.type;
  var limit = req.query.limit;
  var offset = req.query.offset;
  // Given by OST
  const OFFSET_INCR = 25;
  
  if (!type) {
    resp.sendStatus(404);
    return;
  }
  
  console.log('Type Requested: ', type);
  
  var category = categoriesMap[type];

  if (!category && type !== 'PointOfInterest') {
    resp.sendStatus(404);
    return;
  } 
  
  var geoRel = req.query.georel;
  var locationOptions = null;
  
  if (geoRel) {
    var coords = req.query.coords;
    if (coords && geoRel.indexOf('near') !== -1) {
      var components = geoRel.split(';');
      var distance = components[1];
      var maxDistance = parseInt(distance.split('=')[1], 10);
      locationOptions = {
        geometry: 'Circle',
        radius: maxDistance,
        coords: coords
      };
    }
  }
  
  var q = req.query.q;
  if (q) {
    var tokens = q.split(';');
    
    tokens.forEach(function(aToken) {
      var queryFields = aToken.split(':');
      if (queryFields[0] === 'category') {
        category = queryFields[1];
      }
    });
  }
    
  OportoOST.getData('pois', category, limit, offset, locationOptions).then(function(result) {
    var limited = result.data.slice(0, limit);
    var linkHeader;
    if (!offset) {
      offset = 0;
    }
    
    var next = Number(offset) + OFFSET_INCR;
    linkHeader = '</v2/entities?type=PointOfInterest' + '&' + 'offset' +
            '=' + next + '>;rel="next"';
    var prev = offset - OFFSET_INCR;
    var offsetParams = '';
    if (prev > 0) {
      offsetParams = '&offset=' + prev;
    }
    linkHeader += ', </v2/entities?type=PointOfInterest' + offsetParams + '>;rel="prev"';
    
    resp.setHeader('Link', linkHeader);
    resp.json(limited);
  }).catch(function(err) {
      console.error('Error while get data: ', err);
      resp.sendStatus(500);
  });
});

app.get('/v2/entities/:entityId', function (req, resp) {
  console.log(req.params.entityId);
  
  OportoOST.getEntity(req.params.entityId).then(function(result) {
    if (!result) {
      resp.sendStatus(404);
      return;
    }
    resp.json(result);
  }).catch(function(err) {
      console.error('Error while get entity: ', err);
      resp.sendStatus(500);
  });
});

console.log('GSMA proxy up and running on port: ', PORT);
app.listen(PORT);
