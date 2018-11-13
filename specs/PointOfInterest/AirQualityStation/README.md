# Point Of Interest - Air quality Stations

This folder contains code to generate a set of POIs which correspond to Air
Quality Stations owned by the City Council of Madrid.

Here you can find the following files:

-   `madrid_airquality_stations.csv`. This is a list of air quality stations
    owned by the council and available from
    [Madrid's open data portal](https://datos.madrid.es/portal/site/egob/)
-   `madrid-ngsi10.js`. This script allows to upload all the data to Orion
    Context Broker.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

```
curl http://130.206.83.68:1027/v2/entities?type=PointOfInterest&q=category:AirQualityStation
```

```json
{
    "address": {
        "addressCountry": "ES",
        "addressLocality": "Madrid",
        "streetAddress": "Plaza de España"
    },
    "category": "AirQualityStation",
    "location": {
        "type": "Point",
        "coordinates": [-3.712247222222222, 40.423852777777775]
    },
    "name": "Pza. de España",
    "source": "http://datos.madrid.es",
    "type": "PointOfInterest",
    "id": "AirQualityStation-ES-Madrid-004"
}
```

If you want to know the Air Quality Stations close to a certain location, for
instance Plaza de España

```
http://130.206.83.68:1027/v2/entities?type=PointOfInterest&q=category:AirQualityStation&limit=100&georel=near;maxDistance=2000&coords=40.42,-3.71
```
