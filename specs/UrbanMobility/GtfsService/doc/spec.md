# GtfsService

## Description

It represents a transportation service which is available for one or more routes
at certain dates.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:GtfsService:<service_identifier>`. It can be
        derived from the `service_id` field of
        [trips.txt](https://developers.google.com/transit/gtfs/reference/#tripstxt)
        and/or
        [calendar.txt](https://developers.google.com/transit/gtfs/reference/#calendartxt)

-   `type`: Entity Type

    -   It shall be equal to `GtfsService`

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `dateCreated`: Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified`: Last update timestamp of this Entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name`: Service name.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory

-   `description`: Service description.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `operatedBy`: Agency that operates this service.
    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsAgency](../../GtfsAgency/doc/spec.md)
    -   Mandatory

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsService:Malaga:LAB",
    "type": "GtfsService",
    "operatedBy": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
    },
    "name": {
        "value": "LAB"
    },
    "description": {
        "value": "Laborables"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsService:Malaga:LAB",
    "type": "GtfsService",
    "name": "LAB",
    "description": "Laborables",
    "operatedBy": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:Service:Malaga:LAB",
    "type": "GtfsService",
    "operatedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
    },
    "name": {
        "type": "Property",
        "value": "LAB"
    },
    "description": {
        "type": "Property",
        "value": "Laborables"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field | NGSI Attribute | LinkedGTFS           | Comment |
| :--------- | :------------- | :------------------- | :------ |
|            | `name`         | `schema:name`        |         |
|            | `description`  | `schema:description` |         |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS    | Comment                                            |
| :--------- | :------------- | :------------ | :------------------------------------------------- |
|            | `operatedBy`   | `gtfs:agency` | Shall point to another Entity of Type `GtfsAgency` |

## Open issues
