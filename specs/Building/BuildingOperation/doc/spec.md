# Building Operation

## Description

This entity contains a harmonised description of a generic operation (related to
smart buildings) applied to the referenced building. The building operation
contains dynamic data reported by, or associated with a building or operations
applicable to the building. This entity is associated with the vertical segments
of smart homes, smart cities, industry and related IoT applications.

This data model has been partially developed in cooperation with mobile
operators and the [GSMA](http://www.gsma.com/connectedliving/iot-big-data/),
compared to GSMA data model the following changes are introduced:

-   `refRelatedDeviceOperation` replaces `refRelatedOperation`

## Data Model

For a full description of the following attributes refer to GSMA
[IoT Big Data Harmonised Data Model](https://www.gsma.com/iot/wp-content/uploads/2016/06/CLP.26-v4.0.pdf)

-   `id`

-   `type`: Entity type. It must be equal to `BuildingOperation`.`

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `description`

    -   Optional

-   `refBuilding`

    -   Required

-   `refOperator`

    -   Required

-   `operationType`

    -   Optional

-   `result`

    -   Optional

-   `result`

    -   Optional

-   `operationSequence`

    -   Optional

-   `refRelatedBuildingOperation`
    -   Optional

These are the modified attributes compared to GSMA model:

-   `startDate` : The planned start date for the operation.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Required

-   `endDate` : The planned end date for the operation.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Required

-   `dateStarted` : The actual start date for the operation.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `dateFinished` : The actual end date for the operation.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `refRelatedDeviceOperation` : Devices related to the current operation.
    -   Attribute type: A list of references to an entity of type Device.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

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

## Test it with a real service

T.B.D.
