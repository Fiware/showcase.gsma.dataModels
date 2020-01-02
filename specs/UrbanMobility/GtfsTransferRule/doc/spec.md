# GtfsTransferRule

## Description

See
[https://developers.google.com/transit/gtfs/reference/#transferstxt](https://developers.google.com/transit/gtfs/reference/#transferstxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID.

    -   It shall be `urn:ngsi-ld:GtfsTransferRule:<transfer_rule_identifier>`.

-   `type`: Entity type.

    -   It shall be equal to `GtfsTransfer`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name` : Name given to this transfer rule.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to
        [name](https://schema.org/name)
    -   Optional

-   `description`: Description given to this transfer rule.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `hasOrigin`: Trip associated to this Entity.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsStop](../../GtfsStop/doc/spec.md) or
        [GtfsStation](../../GtfsStation/doc/spec.md)
    -   Mandatory

-   `hasDestination`: Trip associated to this Entity.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsStop](../../GtfsStop/doc/spec.md) or
        [GtfsStation](../../GtfsStation/doc/spec.md)
    -   Mandatory

-   `transferType`: Same as GTFS `transfer_type`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Allowed values: (`"0"`,`"1"`,`"2"`,`"3"`)
    -   Mandatory

-   `minimumTransferTime`: Same as GTFS `min_transfer_time`.
    -   Attribute type: Property. [Integer](https://schema.org/Integer).
    -   Default unit: seconds
    -   Optional

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsTransferRule:Malaga:Linea1_Linea5",
    "type": "GtfsTransferRule",
    "transferType": {
        "value": "0"
    },
    "minimumTransferTime": {
        "value": 10
    },
    "hasDestination": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsStop:Malaga_508"
    },
    "hasOrigin": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsStop:Malaga_101"
    },
    "name": {
        "value": "L1_L5"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsTransferRule:Malaga:Linea1_Linea5",
    "type": "GtfsTransferRule",
    "name": "L1_L5",
    "hasOrigin": "urn:ngsi-ld:GtfsStop:Malaga_101",
    "hasDestination": "urn:ngsi-ld:GtfsStop:Malaga_508",
    "transferType": "0",
    "minimumTransferTime": 10
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsTransferRule:Malaga:Linea1_Linea5",
    "type": "GtfsTransferRule",
    "transferType": {
        "type": "Property",
        "value": "0"
    },
    "minimumTransferTime": {
        "type": "Property",
        "value": 10
    },
    "hasDestination": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsStop:Malaga_508"
    },
    "hasOrigin": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsStop:Malaga_101"
    },
    "name": {
        "type": "Property",
        "value": "L1_L5"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field            | NGSI Attribute     | LinkedGTFS                 | Comment |
| :-------------------- | :----------------- | :------------------------- | :------ |
| `transfer_type`       | `transferType`     | `gtfs:transferType`        |         |
| `minimumTransferTime` | `min_tranfer_time` | `gtfs:minimumTransferTime` |         |
|                       | `name`             | `schema:name`              |         |
|                       | `description`      | `schema:description`       |         |

### Relationships

| GTFS Field     | NGSI Attribute   | LinkedGTFS             | Comment                                                         |
| :------------- | :--------------- | :--------------------- | :-------------------------------------------------------------- |
| `from_stop_id` | `hasOrigin`      | `gtfs:originStop`      | It shall point to an Entity of Type `GtfsStop` or `GtfsStation` |
| `to_stop_id`   | `hasDestination` | `gtfs:destinationStop` | It shall point to an Entity of Type `GtfsStop` or `GtfsStation` |

### Open issues
