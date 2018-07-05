# Building Operation

This entity contains a harmonised description of a generic operation (related
to smart buildings) applied to the referenced building. The building operation
contains dynamic data reported by, or associated with a building or operations
applicable to the building. This entity is associated with the vertical segments
of smart homes, smart cities, industry and related IoT applications.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

```
{
  "id": "57b912ab-eb47-4cd5-bc9d-73abece1f1b3",
  "type": "BuildingOperation",
  "dateCreated": "2016-08-08T10:18:16Z",
  "dateModified": "2016-08-08T10:18:16Z",
  "source":  "http://www.example.com",
  "dataProvider": "OperatorA",
  "refBuilding": "building-a85e3da145c1",
  "operationType": "airConditioning",
  "description": "Air conditioning levels reduced due to out of hours",
  "result": "ok",
  "startDate": "2016-08-08T10:18:16Z",
  "endDate": "2016-08-20T10:18:16Z",
  "dateStarted": "2016-08-08T10:18:16Z",
  "dateFinished": "2016-08-20T10:18:16Z",
  "status": "finished",
  "operationSequence": [
   "fan_power=0",
   "set_temperature=24"
  ],
  "refRelatedBuildingOperation": [
    "b4fb8bff-1a8f-455f-8cc0-ca43c069f865",
    "55c24793-3437-4157-9bda-667c9e1531fc"
  ],
  "refRelatedDeviceOperation": [
    "36744245-6716-4a28-84c7-0e3d7520f143",
    "33b2b713-9223-40a5-87a0-3f80a1264a6c"
  ]
}
```
