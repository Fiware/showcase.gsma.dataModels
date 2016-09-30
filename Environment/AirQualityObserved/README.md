# Ambient Observed

This folder contains scripts that give support to expose ambient observed data as NGSI version 2.

The data provided comes from the [air quality stations](../PointOfInterest/AirQualityStation) owned by Madrid City Council.

Please check the original data source before making use of this data in an application. 

The following scripts are present:

* `madrid_air_quality.py` .- Offers both an NGSIv2 end point and NGSI10 to provide ambient observed data
* `ngsi_helper.py` .- Contains helper functions to support the NGSI protocol

## Examples of Use

What was the ambient observed today at 11:00 AM at the "Plaza de España" air quality station?

```
curl http://130.206.83.68:1029/v2/entities?type=AmbientObserved&q=stationCode:28079004;hour:11
```

```json

{
    "address": {
      "addressCountry": "ES",
      "addressLocality": "Madrid",
      "streetAddress": "Plaza de España"
    },
    "dateCreated": "2016-03-15T13:29:30.894942",
    "id": "Madrid-AmbientObserved-28079004-2016-03-15T11:00:00",
    "location": {
      "type": "geo:point",
      "value": "40.423852777777775,-3.712247222222222"
    },
    "pollutants": {
      "CO": {
        "concentration": 500,
        "description": "Carbon Monoxide"
      },
      "NO": {
        "concentration": 45,
        "description": "Nitrogen Monoxide"
      },
      "NO2": {
        "concentration": 69,
        "description": "Nitrogen Dioxide"
      },
      "NOx": {
        "concentration": 139,
        "description": "Nitrogen oxides"
      },
      "SO2": {
        "concentration": 11,
        "description": "Sulfur Dioxide"
      }
    },
    "precipitation": 0,
    "relativeHumidity": 54,
    "source": "http://datos.madrid.es",
    "stationCode": "28079004",
    "stationName": "Pza. de España",
    "temperature": 12.2,
    "type": "AmbientObserved",
    "validity": {
      "from": "2016-03-15T11:00:00",
      "to": "2016-03-15T12:00:00"
    },
    "windDirection": 186,
    "windSpeed": 0.64
}

```