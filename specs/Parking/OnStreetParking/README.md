# Street parking

This folder holds all the code needed to support datasets which expose
`StreetParking` instances as NGSIv2.

The list below provides a description of the files present in this folder:

-   `data-parking.csv`.- It is a snapshot of the parking sensors provided by the
    SmartSantander project.
-   `parking.js`.- Allows to obtain the former snapshot by querying an instance
    of Orion Context Broker.
-   `parking_polygons.geojson`.- It is a vector layer with the different street
    parking areas (modelled as polygons).
-   `sensors_polygons.csv` .- A data layer which keeps the correspondence
    between parking sensors and its containing polygon.
-   `setup-santander.js`.- This script sets up all the configuration and
    entities for supporting street parking areas in Santander
-   `auxiliary` .- This folder contains auxiliary stuff (GIS layers) which have
    been used to generate the artefacts described above.
-   `santander.js`.- This server subscribes to parking sensor status changes and
    updates the corresponding `StreetParking` entity.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

```bash
curl http://130.206.83.68:1026/v2/entities?type=StreetParking
```

```json
{
    "id": "santander:daoiz_velarde_1_5",
    "type": "StreetParking",
    "allowedVehicles": ["Car"],
    "availableSpotNumber": 1,
    "dateUpdated": "2016-06-02T09:25:55.00Z",
    "location": [
        "43.46296641666926,-3.80356167695194",
        "43.46301091092682,-3.803161973253841",
        "43.462879859445884,-3.803147082548618",
        "43.462838666196674,-3.803536474744068",
        "43.46296641666926,-3.80356167695194"
    ],
    "totalSpotNumber": 6
}
```
