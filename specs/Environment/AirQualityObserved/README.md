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

To get access to a public instance offering air quality observed data please
have a look at the
[GSMA's API Directory](http://apidirectory.connectedliving.gsma.com/api/air-quality-spain).

The instance described
[here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing)
has been set up by the FIWARE Community.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of Use

What was the air quality observed today at noon UTC at the "Plaza de España"
(Madrid) air quality station?

`curl -S -H 'fiware-service:airquality' -H 'fiware-servicepath:/Spain_Madrid' -H 'x-auth-token:<my_token>' "http://130.206.118.244:1027/v2/entities?options=keyValues&q=dateObserved:2016-11-28T12:00;stationCode:'28079004'"`

```json
{
    "id": "Madrid-AmbientObserved-28079004-2016-11-28T13:00:00",
    "type": "AirQualityObserved",
    "CO": 0.3,
    "NO": 18,
    "NO2": 46,
    "NOx": 73,
    "SO2": 4,
    "address": {
        "addressCountry": "ES",
        "addressLocality": "Madrid",
        "streetAddress": "Plaza de España"
    },
    "dateObserved": "2016-11-28T12:00:00.00Z",
    "hour": "13:00",
    "location": {
        "type": "Point",
        "coordinates": [-3.712247222, 40.423852778]
    },
    "precipitation": 0,
    "relativeHumidity": 0.69,
    "source": "http://datos.madrid.es",
    "stationCode": "28079004",
    "stationName": "Pza. de España",
    "temperature": 14.3,
    "windDirection": 352
}
```
