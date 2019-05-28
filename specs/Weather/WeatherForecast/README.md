# Weather Forecast

The Weather forecast in Spain is provided by 
[Spanish National Meteorology Agency](http://aemet.es), from Portugal by 
[Instituto Português do Mar e da Atmosfera](http://www.ipma.pt/pt). 
[Harvesters](./harvesters) transform this data to NGSI v2.

This folder contains the following scripts:
-   `harvest/spain/run.py` - Performs data harvesting using
    AEMET's data site as the origin and Orion Context Broker as the destination.
-   `harvest/portugal/hrun.py` - Performs data harvesting using
    IPMA's data site as the origin and Orion Context Broker as the destination.

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).

## Examples of use

```bash
curl -X GET \
  'http://streams.lab.fiware.org:1026/v2/entities?type=WeatherForecast&options=keyValues&q=address.addressLocality:Barcelona&limit=1' \
  -H 'fiware-service: weather' \
  -H 'fiware-servicepath: /Spain' | python -m json.tool
```

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Barcelona",
            "postalCode": "08019"
        },
        "dataProvider": "FIWARE",
        "dateIssued": "2019-05-28T00:00:00.00Z",
        "dateRetrieved": "2019-05-28T20:35:34.00Z",
        "dayMaximum": {
            "feelsLikeTemperature": 20,
            "relativeHumidity": 0.9,
            "temperature": 20
        },
        "dayMinimum": {
            "feelsLikeTemperature": 14,
            "relativeHumidity": 0.6,
            "temperature": 14
        },
        "feelsLikeTemperature": 15,
        "id": "Spain-WeatherForecast-08019_tomorrow_18:00:00_00:00:00",
        "precipitationProbability": 0,
        "relativeHumidity": 0.85,
        "source": "http://www.aemet.es",
        "temperature": 15,
        "type": "WeatherForecast",
        "validFrom": "2019-05-29T18:00:00.00Z",
        "validTo": "2019-05-30T00:00:00.00Z",
        "validity": "2019-05-29T18:00:00Z/2019-05-30T00:00:00Z",
        "weatherType": "slightlyCloudy",
        "windDirection": null,
        "windSpeed": 0
    }
]
```
