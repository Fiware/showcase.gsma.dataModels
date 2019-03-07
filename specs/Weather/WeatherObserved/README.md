# Weather Observed

The Weather observed in Spain is provided by 
[Spanish National Meteorology Agency](http://aemet.es), from Portugal by 
[Instituto Português do Mar e da Atmosfera](http://www.ipma.pt/pt). 
[Harvesters](./harvesters) transform this data to NGSI v2.

This folder contains the following scripts:
- `harvest/spain/harvester.py` - Performs data harvesting using
    AEMET's data site as the origin and Orion Context Broker as the destination.
- `harvest/portugal/harvester.py` - Performs data harvesting using
    IPMA's data site as the origin and Orion Context Broker as the destination.

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).

## Examples of use

```bash
curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' "https://orion.lab.fiware.org/v2/entities?type=WeatherObserved&q=address.addressLocality:'Madrid Aeropuerto'&options=keyValues"
```

```json
[
    {
        "id": "Spain-WeatherObserved-3129-latest",
        "type": "WeatherObserved",
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Madrid Aeropuerto"
        },
        "atmosphericPressure": 960.3,
        "dataProvider": "FIWARE",
        "dateObserved": "2019-02-21T11:00:00.00Z",
        "location": {
            "type": "Point",
            "coordinates": [
                -3.555555556,
                40.466666667
            ]
        },
        "precipitation": 0,
        "pressureTendency": 0.3,
        "relativeHumidity": 0.63,
        "source": "http://www.aemet.es",
        "stationCode": "3129",
        "stationName": "Madrid Aeropuerto",
        "temperature": 10.9,
        "windDirection": 0,
        "windSpeed": 1.12
    }
]
```
