# Air quality station

The formal documentation is not available yet. In the meantime please check some
of the examples of use.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "AirQualityStation-ES-Madrid-004",
    "type": "PointOfInterest",
    "category": {
        "value": "AirQualityStation"
    }, 
    "name": {
        "value": "Pza. de Espa\u00f1a"
    }, 
    "source": {
        "value": "http://datos.madrid.es"
    }, 
    "location": {
        "type": "geo:json", 
        "value": {
            "type": "Point", 
            "coordinates": [
                -3.712247222222222, 
                40.423852777777775
            ]
        }
    }, 
    "address": {
        "type": "PostalAddress", 
        "value": {
            "addressCountry": "ES", 
            "addressLocality": "Madrid", 
            "streetAddress": "Plaza de Espa\u00f1a"
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

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
```
