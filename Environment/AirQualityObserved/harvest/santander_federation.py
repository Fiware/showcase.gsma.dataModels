# This simple Flask application allows to listen for incoming notification
# messages with air quality data from servers owned by the city of Santander
# The notification messages are listened and data is sent to FIWARE GSMA
# instance

from __future__ import print_function
import json
from flask import Flask, jsonify, request, Response
import urllib2
import contextlib
import logging
import logging.handlers
app = Flask(__name__)

orion_service = 'http://localhost:1030'
FIWARE_SERVICE = 'airquality'
FIWARE_SERVICE_PATH = '/Spain_Santander'
MIME_JSON = 'application/json'
SUBSCRIPTION_ID = '58a1ac701afd1c0f8f5a0d33'


# POST data to an Orion Context Broker instance using NGSIv2 API
def post_data(data):
    app.logger.debug('Going to post data %d', len(data))

    if len(data) == 0:
        return

    payload = {
        'actionType': 'APPEND',
        'entities': data
    }

    data_as_str = json.dumps(payload)

    headers = {
        'Content-Type': MIME_JSON,
        'Content-Length': len(data_as_str),
        'Fiware-Service': FIWARE_SERVICE,
        'Fiware-Servicepath': FIWARE_SERVICE_PATH
    }

    req = urllib2.Request(
        url=(
            orion_service +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    try:
        with contextlib.closing(urllib2.urlopen(req)) as f:
            app.logger.debug("Entity batch successfully created!")
    except urllib2.URLError as e:
        app.logger.error(
            'Error while POSTing data to Orion: %d %s',
            e.code,
            e.read())


def build_logger_handler():
    LOG_FILENAME = 'harvest_airquality_santander.log'

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    return handler


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/federate", methods=['POST'])
def process():
    data = request.get_json()
    # Check that subscription id is correct
    if 'subscriptionId' in data or not 'data' not in data:
        app.logger.warn('JSON payload seems not to be appropriate')
        return ('', 200)

    subscriptionId = data['subscriptionId']
    if subscriptionId != SUBSCRIPTION_ID:
        app.logger.warn(
            'Subscription id : %s. Not recognized!!',
            subscriptionId)
        return ('', 200)

    app.logger.debug('Subscription id is correct, posting data')
    # TODO: Validate the data using the JSON-Schema for air quality
    post_data(data['data'])

    return ('', 200)


if __name__ == "__main__":
    print('Running')
    handler = build_logger_handler()
    app.logger.addHandler(handler)

    print(handler)

    app.logger.debug('Starting server ....')

    app.run(debug=True, host="0.0.0.0", port=int("1050"))
