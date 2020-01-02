# Point Of Interest - Weather Stations

This folder contains the following scripts:

-   `harvesters/spain/spain_weather_stations.py` - Performs data harvesting
    using AEMET's data site as the origin and Orion Context Broker as the
    destination. It also prepares a configuration file for other harvesters.
-   `harvesters/portugal/portugal_weather_stations.py` - Performs data
    harvesting using IPMA's data site as the origin and Orion Context Broker as
    the destination.

The list of weather stations in Spain provided by
[Spanish National Meteorology Agency](http://aemet.es), the list of Spain
municipalities provided by
[The National Statistics Institute](http://ine.es/en/), the list of weather
stations in Portugal provided by
[The Portuguese Institute for Sea and Atmosphere](http://www.ipma.pt/en)

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

You can read about public instance offering information about weather stations
[here](../../gsma.md).

## Example of use

```bash
curl -X GET \
  'https://streams.lab.fiware.org/v2/entities?id=WeatherStation-ES-C929I&options=keyValues' \
  -H 'fiware-service: poi'| python -m json.tool
```

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Hierro Aeropuerto",
            "addressRegion": "Santa Cruz de Tenerife"
        },
        "category": ["WeatherStation"],
        "id": "WeatherStation-ES-C929I",
        "location": {
            "coordinates": [-17.8889, 27.8189],
            "type": "Point"
        },
        "source": "http://www.aemet.es",
        "type": "PointOfInterest"
    }
]
```
