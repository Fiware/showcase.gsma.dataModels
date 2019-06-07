![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png)
​
# FIWARE harvester - Spain weather forecast

## Overview

It performs data harvesting using AEMET's data site as the origin and Orion Context Broker as the destination.
    
## How to run

```console
docker run -d fiware/harvesters:weather-forecast-spain \
           --timeout ${TIMEOUT} \
           --latest \
           --orion ${ORION_ENDPOINT} \
           --path ${FIWARE_SERVICEPATH} \
           --service ${FIWARE_SERVICE} \
           --config ${PATH_TO_CONFIG} \
           --key ${AEMET_API_KEY}
```       

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and Orion. See parameters in the
[harvester](./spain_weather_forecast.py).
 
## API key

API key from AEMET should be provided. See the help at the header of the
[harvester](./spain_weather_forecast.py).
​