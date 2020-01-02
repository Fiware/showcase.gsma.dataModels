![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png)

# FIWARE harvester - Spain weather stations

## Overview

It performs data harvesting using AEMET's data site as the origin and Orion
Context Broker as the destination and prepares a config that can be used by
other harvesters, see the list in the [harvester](./spain_weather_stations.py).
It also exports data to the CSV file (./stations.csv), that can be used to
upload the list of weather stations to
[Google Maps](https://www.google.com/maps/d/viewer?mid=1Sd5uNFd2um0GPog2EGkyrlzmBnEKzPQw).

## How to run

```console
docker run -t --rm fiware/harvesters:weather-stations-spain \
           --orion ${ORION_ENDPOINT} \
           --service ${FIWARE_SERVICE}
```

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and
Orion. See parameters in the [harvester](./spain_weather_stations.py).

## API key

If you do not import the predefined list of stations, please provide an API key
from AEMET. See the help at the header of
[harvester](./spain_weather_stations.py).
