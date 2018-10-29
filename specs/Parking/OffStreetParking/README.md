# Parking lot

The entity type corresponding to parking lots is `ParkingLot`.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

# Examples of use

Below you can find an example of `ParkingLot`provided by the city of Santander.

```json
{
    "totalSpotNumber": "475",
    "location": {
        "value": "43.4628890000,-3.7949180000",
        "type": "geo:point"
    },
    "id": "urn:x-iot:smartsantander:parking:indoor:APAR1",
    "type": "ParkingLot",
    "name": "Parking de Puertochico"
}
```
