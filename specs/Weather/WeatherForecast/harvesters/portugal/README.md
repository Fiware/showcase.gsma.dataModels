![FIWARE Banner](https://nexus.lab.fiware.org/content/images/fiware-logo1.png) ​

# FIWARE harvester - Portugal weather forecasts

## Overview

It performs data harvesting using IPMA's data site as the origin and Orion Context Broker as the destination.

## How to run

```console
docker run -d fiware/harvesters:weather-forecast-portugal \
           --timeout ${TIMEOUT} \
           --latest \
           --orion ${ORION_ENDPOINT} \
           --service ${FIWARE_SERVICE} \
           --config ${PATH_TO_CONFIG}
```

## Optional parameters

It is possible to limit the amount of parallel requests to the sources and
Orion. See parameters in the [harvester](./portugal_weather_forecast.py).
