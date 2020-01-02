# GtfsFrequency

## Description

See
[https://developers.google.com/transit/gtfs/reference/#frequenciestxt](https://developers.google.com/transit/gtfs/reference/#frequenciestxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID.

    -   It shall be `urn:ngsi-ld:GtfsFrequency:<frequency_identifier>`.

-   `type`: Entity type.

    -   It shall be equal to `GtfsFrequency`.

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

-   `name` : Name given to this frequency.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `description`: Description given to this frequency.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `hasTrip`: Trip associated to this Entity.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsTrip](../../GtfsTrip/doc/spec.md)
    -   Mandatory

-   `startTime`: Same as GTFS `start_time`. See
    [format](https://developers.google.com/transit/gtfs/reference/#frequenciestxt).

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Mandatory

-   `endTime`: Same as GTFS `end_time`. See
    [format](https://developers.google.com/transit/gtfs/reference/#frequenciestxt).

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Mandatory

-   `headwaySeconds`: Same as GTFS `headway_secs`.

    -   Attribute type: Property. [Integer](https://schema.org/Integer).
    -   Mandatory

-   `exactTimes`: Same as GTFS `exact_times` but encoded as a Boolean: `false`:
    Frequency-based trips are not exactly scheduled. `true`: Frequency-based
    trips are exactly scheduled.
    -   Attribute type: Property. [Boolean](https://schema.org/Boolean).
    -   Optional

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsFrequency:Malaga:Linea1",
    "type": "GtfsFrequency",
    "description": {
        "value": "Cada 10 minutos"
    },
    "hasTrip": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsTrip:Spain:Malaga:1"
    },
    "headwaySeconds": {
        "value": 600
    },
    "startTime": {
        "value": "07:00:00"
    },
    "endTime": {
        "value": "10:25:00"
    },
    "name": {
        "value": "Laborables"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsFrequency:Malaga:Linea1",
    "type": "GtfsFrequency",
    "name": "Laborables",
    "description": "Cada 10 minutos",
    "hasTrip": "urn:ngsi-ld:GtfsTrip:Spain:Malaga:1",
    "startTime": "07:00",
    "endTime": "10:00",
    "headwaySeconds": 600
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsFrequency:Malaga:Linea1",
    "type": "GtfsFrequency",
    "description": {
        "type": "Property",
        "value": "Cada 10 minutos"
    },
    "hasTrip": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsTrip:Spain:Malaga:1"
    },
    "headwaySeconds": {
        "type": "Property",
        "value": 600
    },
    "startTime": {
        "type": "Property",
        "value": "07:00:00"
    },
    "endTime": {
        "type": "Property",
        "value": "10:25:00"
    },
    "name": {
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

| GTFS Field     | NGSI Attribute   | LinkedGTFS            | Comment |
| :------------- | :--------------- | :-------------------- | :------ |
| `start_time`   | `startTime`      | `gtfs:startTime`      |         |
| `end_time`     | `endTime`        | `gtfs:endTime`        |         |
| `headway_secs` | `headwaySeconds` | `gtfs:headwaySeconds` |         |
| `exact_times`  | `exactTimes`     | `gtfs:exactTimes`     |         |
|                | `name`           | `schema:name`         |         |
|                | `description`    | `schema:description`  |         |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS | Comment                                        |
| :--------- | :------------- | :--------- | :--------------------------------------------- |
| `trip_id`  | `hasTrip`      |            | It shall point to an Entity of Type `GtfsTrip` |

### Open issues
