# gtfs:CalendarDateRule

## Description

See
[https://developers.google.com/transit/gtfs/reference/#calendar_datestxt](https://developers.google.com/transit/gtfs/reference/#calendar_datestxt)

## Data Model

The data model is defined as shown below:

- `id`: Entity ID

  - It shall be
        `urn:ngsi-ld:gtfs:CalendarDateRule:<calendar_date_rule_identifier>`.

- `type`: Entity Type

  - It shall be equal to `gtfs:CalendarDateRule`

- `source` : A sequence of characters giving the source of the entity data.
  - Attribute type: Text or URL
  - Optional

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

- `dateCreated` : Entity's creation timestamp.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `dateModified` : Last update timestamp of this Entity.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `hasService` : Service to which this rule applies to. Derived from
    `service_id`.

  - Attribute type: Relationship. It shall point to an entity of Type
        [gtfs:Service](../../Service/doc/spec.md)
  - Mandatory

- `name` : Name given to this rule.

  - Attribute type: Property. [Text](https://schema.org/Text)
  - Optional

- `description`: Description given to this rule.

  - Attribute type: Property. [Text](https://schema.org/Text)
  - Optional

- `appliesOn`: Date (in YYYY-MM-DD format) this rule applies to. It shall be
    obtained from the GTFS `date` field.

  - Attribute type: Property. [Date](https://schema.org/Date).
  - Mandatory

- `exceptionType`: Same as GTFS `exception_type` field. Allowed values:
    (`"1"`, `"2"`)
  - Attribute type: Property. [Text](https://schema.org/Text)
  - Mandatory

### Example of use 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:CalendarDateRule:Malaga:Rule67",
    "type": "gtfs:CalendarDateRule",
    "name": {
        "value": "Rule Fair Area"
    },
    "exceptionType": {
        "value": "1"
    },
    "hasService": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:Service:Malaga:FairArea_1"
    },
    "appliesOn": {
        "value": "2018-03-19"
    }
}
```

### Example of use 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:CalendarDateRule:Malaga:Rule67",
    "type": "gtfs:CalendarDateRule",
    "name": "Rule Fair Area",
    "hasService": "urn:ngsi-ld:Service:Malaga:FairArea_1",
    "appliesOn": "2018-03-19",
    "exceptionType": "1"
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

| GTFS Field | NGSI Attribute | LinkedGTFS     | Comment                                              |
| :--------- | :------------- | :------------- | :--------------------------------------------------- |
|            | `hasService`   | `gtfs:service` | Shall point to another Entity of Type `gtfs:Service` |

## Open issues
