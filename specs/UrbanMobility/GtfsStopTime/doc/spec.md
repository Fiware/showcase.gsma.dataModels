# GtfsStopTime

## Description

See
[https://developers.google.com/transit/gtfs/reference/#stop_timestxt](https://developers.google.com/transit/gtfs/reference/#stop_timestxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID.

    -   It shall be `urn:ngsi-ld:GtfsStopTime:<stop_time_identifier>` being
        `stop_time_identifier` a value that can be derived from GTFS `trip_id`
        and `stop_id`.

-   `type`: Entity type.

    -   It shall be equal to `GtfsStopTime`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified`: Last update timestamp of this Entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `hasTrip`: Same as GTFS `trip_id`.

    -   Attribute type: Relationship. It shall point to an Entity of type
        [GtfsTrip](../../GtfsTrip/doc/spec.md)
    -   Mandatory

-   `hasStop`: Same as GTFS `stop_id`

    -   Attribute type: Relationship. It shall point to an Entity of type
        [GtfsStop](../../GtfsStop/doc/spec.md)
    -   Mandatory

-   `arrivalTime`: Same as GTFS `arrival_time`

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Mandatory

-   `departureTime`: Same as GTFS `departure_time`

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Mandatory

-   `stopSequence`: Same as GTFS `stop_sequence`

    -   Attribute type: Property. [Integer](https://schema.org/Integer) starting
        with `1`.
    -   Mandatory

-   `stopHeadsign`: Same as GTFS `stop_headsign`

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Optional

-   `pickupType`: Same as GTFS `pickup_type`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Optional

-   `dropOffType`: Same as GTFS `drop_off_type`

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `distanceTravelled`: Same as GTFS `shape_dist_traveled`.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Optional

-   `timepoint`: Same as GTFS `timepoint`.
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

### Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsStopTime:Spain:Madrid:EMT:FE0010011_737",
    "type": "GtfsStopTime",
    "departureTime": {
        "value": "07:04:24"
    },
    "hasTrip": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsTrip:Madrid:EMT:FE0010011"
    },
    "stopSequence": {
        "value": 4
    },
    "distanceTravelled": {
        "value": 759
    },
    "arrivalTime": {
        "value": "07:04:24"
    },
    "hasStop": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsStop:Madrid:EMT:737"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsStopTime:Spain:Madrid:EMT:FE0010011_737",
    "type": "GtfsStopTime",
    "hasStop": "urn:ngsi-ld:GtfsStop:Madrid:EMT:737",
    "hasTrip": "urn:ngsi-ld:GtfsTrip:Madrid:EMT:FE0010011",
    "distanceTravelled": 759,
    "stopSequence": 4,
    "arrivalTime": "07:04:24",
    "departureTime": "07:04:24"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsStopTime:Spain:Madrid:EMT:FE0010011_737",
    "type": "GtfsStopTime",
    "departureTime": {
        "type": "Property",
        "value": "07:04:24"
    },
    "hasTrip": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsTrip:Madrid:EMT:FE0010011"
    },
    "stopSequence": {
        "type": "Property",
        "value": 4
    },
    "distanceTravelled": {
        "type": "Property",
        "value": 759
    },
    "arrivalTime": {
        "type": "Property",
        "value": "07:04:24"
    },
    "hasStop": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsStop:Madrid:EMT:737"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field             | NGSI Attribute      | LinkedGTFS               | Comment |
| :--------------------- | :------------------ | :----------------------- | :------ |
| `arrival_time`         | `arrivalTime`       | `gtfs:arrivalTime`       |         |
| `departure_time`       | `departureTime`     | `gtfs:departureTime`     |         |
| `stop_sequence`        | `stopSequence`      | `gtfs:stopSequence`      |         |
| `stop_headsign`        | `stopHeadsign`      | `gtfs:headsign`          |         |
| `pickup_type`          | `pickupType`        | `gtfs:pickupType`        |         |
| `drop_off_type`        | `dropOffType`       | `gtfs:dropOffType`       |         |
| `shape_dist_travelled` | `distanceTravelled` | `gtfs:distanceTravelled` |         |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS  | Comment |
| :--------- | :------------- | :---------- | :------ |
| `trip_id`  | `hasTrip`      | `gtfs:trip` |         |
| `stop_id`  | `hasStop`      | `gtfs:stop` |         |

### Open issues
