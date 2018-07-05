'use strict';

// Port on which the server will listen to
const PORT              = 9003;
// Needed for subscriptions
const SERVER_ADDRESS    = '130.206.83.68';

const SANTANDER_SERVER  = 'http://mu.tlmat.unican.es:8099/v1';
const BROKER_SERVER     = 'http://' + SERVER_ADDRESS + ':1026' + '/v1';

var URL = require('url');
var QueryString = require('querystring');
var fs = require('fs');

var Orion = require('fiware-orion-client');
var SantanderClient = new Orion.Client({
  url: SANTANDER_SERVER,
  service: 'smartsantander'
});
var OrionHelper = Orion.NgsiHelper;

var OrionClient = new Orion.Client({
  url: BROKER_SERVER
});

var loggerStream = fs.createWriteStream('./log.txt', {
  flags: 'a',
  encoding: 'utf-8',
  mode: '0666'
});

var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');

var app = express();

// Configuration needed to deal with sensor changes
var configuration = null;

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));
app.use(bodyParser.json());

app.use(morgan('dev',{
  stream: loggerStream
}));


// Invoked when a change in context happens (a notification is received)
app.post('/on_context_change', function(req, resp) {
  console.log('on context change!!!', req.body.subscriptionId);
  var ngsiData = OrionHelper.parse(req.body);

  var sensorId = ngsiData.id;
  // Now it is needed to update the status of the corresponding polygon
  var polygonId = configuration.sensor2Polygon[sensorId];
  if (!polygonId) {
    console.log('No polygon Id for the sensor: ', sensorId);
    resp.sendStatus(200);
    return;
  }
  
  var entityId = 'santander' + ':' + polygonId;
  
  console.log('Changes: ', sensorId, polygonId);
  
  OrionClient.queryContext({
    id: entityId,
    attributes: [
      'availableSpotNumber',
      'totalSpotNumber'
    ]
  }).then(function(streetParking) {
      var status = ngsiData['presenceStatus:parking'];
      
      var total = streetParking.totalSpotNumber;
      var available = streetParking.availableSpotNumber;
      if (status === 'false') {
        available++;
      }
      else if (status === 'true') {
        available--;
      }
      
      console.log('New value for available: ', available, '/', total);
      
      if (available < 0) {
        available = 0;
      }
      
      if (available > total) {
        available = total;
      }
      
      return OrionClient.updateContext({
        id: entityId,
        availableSpotNumber: available,
        updated: new Date()
      }, { updateAction: 'UPDATE' }).then(function() {
          console.log('Entity: ', entityId, ' updated');
      }).catch(function(err) {
          console.error('Error while updating: ', err);
      });
  }).catch(function(err) {
      console.error('Error while updating parking info: ', err);
  });
  
  resp.sendStatus(200);
});

// Subscribes to context changes creating or renewing a subscription
function registerSubscription(forceCreate) {
  return new Promise(function (resolve, reject) {
    var FILE_SUBSCRIPTION = 'subscription.id';
    var subscriptionId;
    try {
      subscriptionId = fs.readFileSync(__dirname + '/' + FILE_SUBSCRIPTION,
                                       'UTF-8');
    }
    catch(e) {
      console.log('Subscription id not present');
    }

    var subscription = {
      type:    'urn:smartsantander:entityType:parkingSensor',
      pattern: 'urn:x-iot:smartsantander:u7jcfa:fixed:np.*',
    };

    var options = {
      callback: 'http://' + SERVER_ADDRESS + ':' + PORT + '/on_context_change',
      throttling: 'PT30S',
      attributes: [
        'presenceStatus:parking'
      ]
    };

    if (subscriptionId && !forceCreate) {
      console.log('Using existing subscription id: ', subscriptionId);
      options.subscriptionId = subscriptionId;
    }

    SantanderClient.subscribeContext(subscription, options, {
      path: '/parking/#'
    }).then(function(data) {
      if (!data) {
        reject({
          code: 404
        });
        return;
      }

      fs.writeFileSync(__dirname + '/' + FILE_SUBSCRIPTION,
                       data.subscriptionId);
      resolve(data.subscriptionId);

    }).catch(function(err) {
      reject(err);
    });
  });
}

function onSubscribed(subscriptionId) {
  console.log('Subscribed to context changes: ', subscriptionId);
  console.log('App Web Server up and running on port: ', PORT);
  app.listen(PORT);
}

function onSubscribedError(err) {
  if (err && err.code == 404) {
    console.warn('Cannot update existing subscription');
    registerSubscription(true).then(onSubscribed);
    return;
  }
  console.error('Cannot subscribe to context changes: ', err);
}

function readConfig() {
  return new Promise(function(resolve, reject) {
    OrionClient.queryContext({
      id: 'parking_config_1'
    }).then(function(result) {
      configuration = result.data;
      resolve();
    }).catch(reject);
  });
}

readConfig().then(function() {
  console.log('Configuration read properly: ', typeof configuration.sensor2Polygon);
  registerSubscription().then(onSubscribed, onSubscribedError);
}, function(err) {
    console.error('Error while reading configuration: ', err);
}).catch(function(err) {
    console.error('Start up error: ', err);
});
