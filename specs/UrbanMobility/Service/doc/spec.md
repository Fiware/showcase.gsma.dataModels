# gtfs:Service

## Description

It represents a transportation service which is available for one or more routes
at certain dates.

## Data Model

The data model is defined as shown below:

-   `id`: Entity Id + It shall be
    `urn:ngsi-ld:gtfs:Service:<service_identifier>`. It can be derived from the
    `service_id` field of
    [trips.txt](https://developers.google.com/transit/gtfs/reference/#tripstxt)
    and/or
    [calendar.txt](https://developers.google.com/transit/gtfs/reference/#calendartxt)

-   `type`: Entity Type

    -   It shall be equal to `gtfs:Service`

-   `dateCreated`: Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified`: Last update timestamp of this Entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name`: Service name.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory

-   `description`: Service description.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `operatedBy`: Agency that operates this service.
    -   Attribute type: Relationship. It shall point to an Entity of Type
        [gtfs:Agency](../../Agency/doc/spec.md)
    -   Mandatory

### Examples of use 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:Service:Malaga:LAB",
    "type": "gtfs:Service",
    "operatedBy": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:gtfs:Agency:Malaga_EMT"
    },
    "name": {
        "value": "LAB"
    },
    "description": {
        "value": "Laborables"
    }
}
```

### Examples of use 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:Service:Malaga:LAB",
    "type": "gtfs:Service",
    "name": "LAB",
    "description": "Laborables",
    "operatedBy": "urn:ngsi-ld:gtfs:Agency:Malaga_EMT"
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field | NGSI Attribute | LinkedGTFS           | Comment |
| :--------- | :------------- | :------------------- | :------ |
|            | `name`         | `schema:name`        |         |
|            | `description`  | `schema:description` |         |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS    | Comment                                             |
| :--------- | :------------- | :------------ | :-------------------------------------------------- |
|            | `operatedBy`   | `gtfs:agency` | Shall point to another Entity of Type `gtfs:Agency` |

## Open issues
