# Weather Forecast

The Weather forecast in Spain is provided by 
[Spanish National Meteorology Agency](http://aemet.es), from Portugal by 
[Instituto Português do Mar e da Atmosfera](http://www.ipma.pt/pt). 
[Harvesters](./harvesters) transform this data to NGSI v2.

This folder contains the following scripts:
-    `harvest/spain/harvester.py` - Performs data harvesting using
    AEMET's data site as the origin and Orion Context Broker as the destination.
-    `harvest/portugal/harvester.py` - Performs data harvesting using
    IPMA's data site as the origin and Orion Context Broker as the destination.

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).


## Examples of use

```bash
curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' "https://orion.lab.fiware.org/v2/entities?type=WeatherForecast&q=address.addressLocality:Madrid&options=keyValues&limit=1"
```

```json
[
    {
        "id": "Spain-WeatherForecast-28079_tomorrow_18:00:00+0100_00:00:00+0100",
        "type": "WeatherForecast",
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Madrid",
            "postalCode": "28079"
        },
        "dataProvider": "FIWARE",
        "dateIssued": "2019-02-21T10:44:01.00Z",
        "dateRetrieved": "2019-02-21T11:31:32.00Z",
        "dayMaximum": {
            "feelsLikeTemperature": 19,
            "temperature": 19,
            "relativeHumidity": 0.55
        },
        "dayMinimum": {
            "feelsLikeTemperature": 0,
            "temperature": 3,
            "relativeHumidity": 0.2
        },
        "feelsLikeTemperature": 8,
        "precipitationProbability": 0,
        "relativeHumidity": 0.35,
        "source": "http://www.aemet.es",
        "temperature": 8,
        "validFrom": "2019-02-22T17:00:00.00Z",
        "validTo": "2019-02-22T23:00:00.00Z",
        "validity": "2019-02-22T18:00:00+01:00/2019-02-23T00:00:00+01:00",
        "weatherType": "sunnyDay",
        "windDirection": null,
        "windSpeed": 0
    }
]
```
