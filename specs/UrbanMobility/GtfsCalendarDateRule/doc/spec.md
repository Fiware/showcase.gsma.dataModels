# GtfsCalendarDateRule

## Description

See
[https://developers.google.com/transit/gtfs/reference/#calendar_datestxt](https://developers.google.com/transit/gtfs/reference/#calendar_datestxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be
        `urn:ngsi-ld:GtfsCalendarDateRule:<calendar_date_rule_identifier>`.

-   `type`: Entity Type

    -   It shall be equal to `GtfsCalendarDateRule`

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

-   `hasService` : Service to which this rule applies to. Derived from
    `service_id`.

    -   Attribute type: Relationship. It shall point to an entity of Type
        [GtfsService](../../GtfsService/doc/spec.md)
    -   Mandatory

-   `name` : Name given to this rule.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `description`: Description given to this rule.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `appliesOn`: Date (in YYYY-MM-DD format) this rule applies to. It shall be
    obtained from the GTFS `date` field.

    -   Attribute type: Property. [Date](https://schema.org/Date).
    -   Mandatory

-   `exceptionType`: Same as GTFS `exception_type` field. Allowed values:
    (`"1"`, `"2"`)
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsCalendarDateRule:Malaga:Rule67",
    "type": "GtfsCalendarDateRule",
    "name": {
        "value": "Rule Fair Area"
    },
    "exceptionType": {
        "value": "1"
    },
    "hasService": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsService:Malaga:FairArea_1"
    },
    "appliesOn": {
        "value": "2018-03-19"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsCalendarDateRule:Malaga:Rule67",
    "type": "GtfsCalendarDateRule",
    "name": "Rule Fair Area",
    "hasService": "urn:ngsi-ld:GtfsService:Malaga:FairArea_1",
    "appliesOn": "2018-03-19",
    "exceptionType": "1"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:CalendarDateRule:Malaga:Rule67",
    "type": "GtfsCalendarDateRule",
    "name": {
        "type": "Property",
        "value": "Rule Fair Area"
    },
    "exceptionType": {
        "type": "Property",
        "value": "1"
    },
    "hasService": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsService:Malaga:FairArea_1"
    },
    "appliesOn": {
        "type": "Property",
        "value": "2018-03-19"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

| GTFS Field       | NGSI Attribute  | LinkedGTFS           | Comment |
| :--------------- | :-------------- | :------------------- | :------ |
|                  | `name`          | `schema:name`        |         |
|                  | `description`   | `schema:description` |         |
| `date`           | `appliesOn`     | `dct:date`           |         |
| `exception_type` | `exceptionType` |                      |         |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS     | Comment                                             |
| :--------- | :------------- | :------------- | :-------------------------------------------------- |
|            | `hasService`   | `gtfs:service` | Shall point to another Entity of Type `GtfsService` |

## Open issues
