![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png)

# FIWARE harvester - Portugal weather stations

## Overview

It performs data harvesting using IPMA's data site as the origin and Orion Context Broker as the destination and
prepares a config that can be used by other harvesters, see the list in the [harvester](./portugal_weather_stations.py).
It also exports data to the CSV file (./stations.csv), that can be used to upload the list of weather stations to
[Google Maps](https://www.google.com/maps/d/viewer?mid=1Sd5uNFd2um0GPog2EGkyrlzmBnEKzPQw).

## How to run

```console
docker run -t --rm fiware/harvesters:weather-stations-portugal \
           --orion ${ORION_ENDPOINT} \
           --service ${FIWARE_SERVICE}
```

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and Orion. See parameters in the
[harvester](./portugal_weather_stations.py).
