# Point Of Interest - Weather Stations

This folder contains the following scripts:

-   `harvesters/spain/spain_weather_stations.py` - Performs data harvesting
    using AEMET's data site as the origin and Orion Context Broker as the
    destination. It also prepares a configuration file for other harvesters.

The list of weather stations in Spain provided by
[Spanish National Meteorology Agency](http://aemet.es), the list of Spain
municipalities provided by
[The National Statistics Institute](http://ine.es/en/).

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

You can read about public instance offering information about weather stations
[here](../../gsma.md).

## Example of use

```bash
curl -X GET \
  'https://streams.lab.fiware.org/v2/entities?type=PointOfInterest&id=WeatherStation-ES-C929I' \
  -H 'fiware-service: poi' \
  -H 'fiware-servicepath: /Spain' | python -m json.tool
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
