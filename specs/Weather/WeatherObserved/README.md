# Weather Observed

The Weather observed in Spain is provided by 
[Spanish National Meteorology Agency](http://aemet.es), from Portugal by 
[Instituto Português do Mar e da Atmosfera](http://www.ipma.pt/pt). 
[Harvesters](./harvesters) transform this data to NGSI v2.

This folder contains the following scripts:
-   `harvesters/spain/spain_weather_observed.py` - Performs data harvesting using
    AEMET's data site as the origin and Orion Context Broker as the destination.
-   `harvesters/portugal/portugal_weather_observed.py` - Performs data harvesting using
    IPMA's data site as the origin and Orion Context Broker as the destination.

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).

## Examples of use

```bash
curl -X GET \
  'https://streams.lab.fiware.org/v2/entities?type=WeatherObserved&options=keyValues&q=address.addressLocality:Barcelona' \
  -H 'fiware-service: weather' \
  -H 'fiware-servicepath: /Spain' | python -m json.tool
```

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Barcelona"
        },
        "atmosphericPressure": null,
        "dataProvider": "FIWARE",
        "dateObserved": "2019-05-27T21:00:00.00Z",
        "id": "Spain-WeatherObserved-0201D-latest",
        "location": {
            "coordinates": [
                2.2,
                41.3906
            ],
            "type": "Point"
        },
        "precipitation": 0,
        "pressureTendency": null,
        "relativeHumidity": 90,
        "source": "http://www.aemet.es",
        "stationCode": "0201D",
        "stationName": "Barcelona",
        "temperature": 17,
        "type": "WeatherObserved",
        "windDirection": 105,
        "windSpeed": 3.5
    }
]
```
