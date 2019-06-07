![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png)
​
# FIWARE harvester - Spain weather station 

## Overview

It performs data harvesting using AEMET's data site as the origin and Orion Context Broker as the destination.
    
## How to run

```console
docker run -d fiware/harvesters:weather-stations-spain \
           --timeout ${TIMEOUT} \
           --import \
           --orion ${ORION_ENDPOINT} \
           --path ${FIWARE_SERVICEPATH} \
           --service ${FIWARE_SERVICE}
```       

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and Orion and not to import the predefined list 
of stations, but download it on fly. See parameters in the
[harvester](./spain_weather_stations.py).
 
## API key

If you do not import the predefined list of stations, please provice an API key from AEMET. See the help at the header of 
[harvester](./spain_weather_stations.py).
​