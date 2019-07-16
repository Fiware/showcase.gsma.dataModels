![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png)

# FIWARE harvester - Spain weather stations

## Overview

It performs data harvesting using AEMET's data site as the origin and Orion Context Broker as the destination.

## How to run

```console
docker run -t --rm fiware/harvesters:weather-stations-spain \
           --import \
           --orion ${ORION_ENDPOINT} \
           --service ${FIWARE_SERVICE}
```       

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and Orion and not to import the predefined list 
of stations, but to download it on the fly. See parameters in the
[harvester](./spain_weather_stations.py).
 
## API key

If you do not import the predefined list of stations, please provide an API key from AEMET. See the help at the header of 
[harvester](./spain_weather_stations.py).
