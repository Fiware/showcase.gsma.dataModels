![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png) ​

# FIWARE harvester - Portugal weather observations

## Overview

It performs data harvesting using IPMA's data site as the origin and Orion
Context Broker as the destination. It uses predefined list of stations
(./stations.yml), that can be obtained by other
[harvester](https://github.com/FIWARE/data-models/tree/master/specs/PointOfInterest/WeatherStation/harvesters/portugal).

## How to run

```console
docker run -d -v ${PATH_TO_STATION_FILE}:/opt/stations.yml \
           fiware/harvesters:weather-observed-portugal \
           --timeout ${TIMEOUT} \
           --latest \
           --orion ${ORION_ENDPOINT} \
           --service ${FIWARE_SERVICE} \
           --config ${PATH_TO_CONFIG}
```

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and
Orion. See parameters in the [harvester](./portugal_weather_observed.py).
