# Air Quality Observed

This folder contains scripts that give support to expose air quality observed
data as NGSI version 2.

The data provided corresponds to different cities in Spain being the original
data source different
[air quality stations](../../PointOfInterest/AirQualityStation/README.md)
managed by municipalities or regional governments.

Please check the original data source before making use of this data in an
application.

The following scripts are present:

-   `madrid_air_quality_harvest.py`.- A data harvest and harmonization program
    for official Madrid's Air Quality Data provided by Madrid's City Council.
-   `barcelona_air_quality_harvest.py`.- A data harvest and harmonization
    program for official Barcelona's Air Quality Data provided by Catalonia's
    Government.
-   `madrid_air_quality.py` .- Offers both an NGSI v2 endpoint and NGSI10 to
    provide ambient observed data (outdated)
-   `ngsi_helper.py` .- Contains helper functions to support the NGSI protocol
    (outdated)

## Public instance

You can read about public instance offering information about observed air quality
[here](../../gsma.md).

## Examples of Use

What was the latest observed air quality at the "Parque Juan Carlos I frente oficinas mantenimiento"
(Madrid) air quality station?

```bash
curl -X GET \
  'https://streams.lab.fiware.org/v2/entities?id=Madrid-AirQualityObserved-28079059-latest&options=keyValues' \
  -H 'fiware-service: environment' | python -m json.tool
```

```json
[
    {
        "NO": 2,
        "NO2": 8,
        "NOx": 11,
        "O3": 115,
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Madrid",
            "streetAddress": "Parque Juan Carlos I frente oficinas mantenimiento"
        },
        "dataProvider": "TEF",
        "dateObserved": "2019-06-13T12:00:00.00Z",
        "hour": "13:00",
        "id": "Madrid-AirQualityObserved-28079059-latest",
        "location": {
            "coordinates": [
                -3.609072222,
                40.46525
            ],
            "type": "Point"
        },
        "measurand": [
            "NO,2.0,GQ,Nitrogen Monoxide",
            "NO2,8.0,GQ,Nitrogen Dioxide",
            "NOx,11.0,GQ,Nitrogen oxides",
            "O3,115.0,GQ,Ozone"
        ],
        "source": "http://datos.madrid.es",
        "stationCode": "28079059",
        "stationName": "Juan Carlos I",
        "type": "AirQualityObserved",
        "validity": {
            "from": "2019-06-13T13:00:00+01:00",
            "to": "2019-06-13T14:00:00+01:00"
        }
    }
]
```
