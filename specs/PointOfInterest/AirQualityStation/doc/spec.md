# Air quality station

The formal documentation is not available yet. In the meantime please check some of the examples of use.

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

    {
      "address": {
        "addressCountry": "ES",
        "addressLocality": "Madrid",
        "streetAddress": "Plaza de España"
      },
      "category": "AirQualityStation",
      "location": {
        "type": "Point",
        "coordinates": [
          -3.712247222222222,
          40.423852777777775
        ]
      },
      "name": "Pza. de España",
      "source": "http://datos.madrid.es",
      "type": "PointOfInterest",
      "id": "AirQualityStation-ES-Madrid-004"
    }