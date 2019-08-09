![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png) ​

# FIWARE harvester - Spain weather observations

## Overview

It performs data harvesting using AEMET's data site as the origin and Orion Context Broker as the destination. It uses 
predefined list of stations (./stations.yml), that can be obtained by other 
[harvester](https://github.com/FIWARE/dataModels/tree/master/specs/PointOfInterest/WeatherStation/harvesters/spain).

## How to run

```console
docker run -d -v ${PATH_TO_STATION_FILE}:/opt/stations.yml \
           fiware/harvesters:weather-observed-spain \
           --timeout ${TIMEOUT} \
           --latest \
           --orion ${ORION_ENDPOINT} \
           --service ${FIWARE_SERVICE} \
           --config ${PATH_TO_CONFIG} \
           --key ${AEMET_API_KEY}
```

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and
Orion. See parameters in the [harvester](./spain_weather_observed.py).

## API key

API key from AEMET should be provided. See the help at the header of the
[harvester](./spain_weather_observed.py).
