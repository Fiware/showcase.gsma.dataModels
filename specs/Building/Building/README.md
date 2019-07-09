# Building

This entity contains a harmonised description of a Building. This entity is
associated with the vertical segments of smart homes, smart cities, industry and
related IoT applications.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

```json
{
    "id": "building-a85e3da145c1",
    "type": "Building",
    "dateCreated": "2016-08-08T10:18:16Z",
    "dateModified": "2016-08-08T10:18:16Z",
    "source": "http://www.example.com",
    "dataProvider": "OperatorA",
    "category": ["office"],
    "containedInPlace": {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
    },
    "location": {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
    },
    "address": {
        "addressLocality": "London",
        "postalCode": "EC4N 8AF",
        "streetAddress": "25 Walbrook"
    },
    "owner": [
        "cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84",
        "1be9cd61-ef59-421f-a326-4b6c84411ad4"
    ],
    "occupier": ["9830f692-7677-11e6-838b-4f9fb3dc5a4f"],
    "floorsAboveGround": 7,
    "floorsBelowGround": 0,
    "description": "Office block",
    "mapUrl": "http://www.example.com",
    "openingHours": ["Mo-Fr 10:00-19:00", "Sa 10:00-22:00", "Su 10:00-21:00"]
}
```
