# Building Operation

## Description

This entity contains a harmonised description of a generic operation (related to
smart buildings) applied to the referenced building. The building operation
contains dynamic data reported by, or associated with a building or operations
applicable to the building. This entity is associated with the vertical segments
of smart homes, smart cities, industry and related IoT applications.

This data model has been partially developed in cooperation with mobile
operators and the [GSMA](https://www.gsma.com/iot/iot-big-data/), compared to
GSMA data model the following changes are introduced:

-   `refRelatedDeviceOperation` replaces `refRelatedOperation`

## Data Model

For a full description of the following attributes refer to GSMA
[IoT Big Data Harmonised Data Model](https://github.com/GSMADeveloper/NGSI-LD-Entities)

-   `id`

-   `type`: Entity type. It must be equal to `BuildingOperation`.`

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Relationship. [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `description`

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description` equivalent to [description](https://schema.org/description)
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

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Required

-   `endDate` : The planned end date for the operation.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Required

-   `dateStarted` : The actual start date for the operation.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional

-   `dateFinished` : The actual end date for the operation.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional

-   `refRelatedDeviceOperation` : Devices related to the current operation.
    -   Attribute type: Relationship. A list of references to an entity of type Device.

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "57b912ab-eb47-4cd5-bc9d-73abece1f1b3",
    "type": "BuildingOperation",
    "status": {
        "value": "finished"
    },
    "startDate": {
        "type": "DateTime",
        "value": "2016-08-08T10:18:16Z"
    },
    "operationSequence": {
        "value": ["fan_power%3D0", "set_temperature%3D24"]
    },
    "endDate": {
        "type": "DateTime",
        "value": "2016-08-20T10:18:16Z"
    },
    "description": {
        "value": "Air conditioning levels reduced due to out of hours"
    },
    "refRelatedDeviceOperation": {
        "type": "Relationship",
        "value": [
            "36744245-6716-4a28-84c7-0e3d7520f143",
            "33b2b713-9223-40a5-87a0-3f80a1264a6c"
        ]
    },
    "dateCreated": {
        "type": "DateTime",
        "value": "2016-08-08T10:18:16Z"
    },
    "dateModified": {
        "type": "DateTime",
        "value": "2016-08-08T10:18:16Z"
    },
    "refRelatedBuildingOperation": {
        "type": "Relationship",
        "value": [
            "b4fb8bff-1a8f-455f-8cc0-ca43c069f865",
            "55c24793-3437-4157-9bda-667c9e1531fc"
        ]
    },
    "source": {
        "value": "http://www.example.com"
    },
    "refBuilding": {
        "type": "Relationship",
        "value": "building-a85e3da145c1"
    },
    "result": {
        "value": "ok"
    },
    "operationType": {
        "value": "airConditioning"
    },
    "dateStarted": {
        "type": "DateTime",
        "value": "2016-08-08T10:18:16Z"
    },
    "dateFinished": {
        "type": "DateTime",
        "value": "2016-08-20T10:18:16Z"
    },
    "dataProvider": {
        "value": "OperatorA"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "57b912ab-eb47-4cd5-bc9d-73abece1f1b3",
    "type": "BuildingOperation",
    "dateCreated": "2016-08-08T10:18:16Z",
    "dateModified": "2016-08-08T10:18:16Z",
    "source": "http://www.example.com",
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
    "operationSequence": ["fan_power=0", "set_temperature=24"],
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

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:BuildingOperation:57b912ab-eb47-4cd5-bc9d-73abece1f1b3",
    "type": "BuildingOperation",
    "modifiedAt": "2016-08-08T10:18:16Z",
    "createdAt": "2016-08-08T10:18:16Z",
    "status": {
        "type": "Property",
        "value": "finished"
    },
    "startDate": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-08-08T10:18:16Z"
        }
    },
    "operationSequence": {
        "type": "Property",
        "value": ["fan_power%3D0", "set_temperature%3D24"]
    },
    "endDate": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-08-20T10:18:16Z"
        }
    },
    "description": {
        "type": "Property",
        "value": "Air conditioning levels reduced due to out of hours"
    },
    "refRelatedDeviceOperation": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:DeviceOperation:36744245-6716-4a28-84c7-0e3d7520f143",
            "urn:ngsi-ld:DeviceOperation:33b2b713-9223-40a5-87a0-3f80a1264a6c"
        ]
    },
    "refRelatedBuildingOperation": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:BuildingOperation:b4fb8bff-1a8f-455f-8cc0-ca43c069f865",
            "urn:ngsi-ld:BuildingOperation:55c24793-3437-4157-9bda-667c9e1531fc"
        ]
    },
    "source": {
        "type": "Property",
        "value": "http://www.example.com"
    },
    "refBuilding": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Building:building-a85e3da145c1"
    },
    "result": {
        "type": "Property",
        "value": "ok"
    },
    "operationType": {
        "type": "Property",
        "value": "airConditioning"
    },
    "dateStarted": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-08-08T10:18:16Z"
        }
    },
    "dateFinished": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-08-20T10:18:16Z"
        }
    },
    "dataProvider": {
        "type": "Property",
        "value": "OperatorA"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

T.B.D.
