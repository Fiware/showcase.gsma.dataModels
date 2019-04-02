# GtfsTrip

## Description

See
[https://developers.google.com/transit/gtfs/reference/#tripstxt](https://developers.google.com/transit/gtfs/reference/#tripstxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID.

    -   It shall be `urn:ngsi-ld:GtfsTrip:<trip_identifier>` being
        `trip_identifier` a value that can be derived from GTFS `trip_id`.

-   `type`: Entity type.

    -   It shall be equal to `GtfsTrip`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified`: Last update timestamp of this Entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `headSign`: Same as GTFS `trip_headsign`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Optional

-   `shortName`: Same as GTFS `trip_short_name`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Optional

-   `direction`: Same as GTFS `direction_id`.

    -   Attribute type: Property. [Number](https://schema.org/Number).
    -   Allowed Values: `0` and `1` as per GTFS `direction_id`.
    -   Optional

-   `block`: Same as GTFS `block_id`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `hasService`: Same as GTFS `service_id`.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsService](../../GtfsService/doc/spec.md)
    -   Optional

-   `hasShape`: Same as GTFS `shape_id`.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsShape](../../GtfsShape/doc/spec.md)
    -   Optional

-   `hasRoute`: Same as `route_id`.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsRoute](../../GtfsRoute/doc/spec.md)
    -   Mandatory

-   `wheelChairAccessible`: Same as GTFS `wheelchair_accessible`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: (`0`, `1`, `2`) as per the
        [GTFS](https://developers.google.com/transit/gtfs/reference/#tripstxt)
    -   Optional

-   `bikesAllowed`: Same as GTFS `bikes_allowed`.
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: (`0`, `1`, `2`) as per the
        [GTFS](https://developers.google.com/transit/gtfs/reference/#tripstxt)
    -   Optional

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsTrip:Spain:Malaga:1",
    "type": "GtfsTrip",
    "direction": {
        "value": 0
    },
    "headSign": {
        "value": "San Andr\u00e9s"
    },
    "hasRoute": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsRoute:Spain:Malaga:1"
    },
    "hasService": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsService:Malaga_LAB"
    },
    "hasShape": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsShape:Shape01"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsTrip:Spain:Malaga:1",
    "type": "GtfsTrip",
    "hasService": "urn:ngsi-ld:GtfsService:Malaga_LAB",
    "headSign": "San Andrés",
    "direction": "0",
    "hasRoute": "urn:ngsi-ld:gtfs:Route:Spain:Malaga:1",
    "hasShape": "urn:ngsi-ld:GtfsShape:Shape01"
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field              | NGSI Attribute         | LinkedGTFS                  | Comment |
| :---------------------- | :--------------------- | :-------------------------- | :------ |
| `trip_headsign`         | `headSign`             | `gtfs:headsign`             |         |
| `trip_short_name`       | `shortName`            | `gtfs:shortName`            |         |
| `direction_id`          | `direction`            | `gtfs:direction`            |         |
| `block_id`              | `block`                | `gtfs:block`                |         |
| `wheelchair_accessible` | `wheelchairAccessible` | `gtfs:wheelchairAccessible` |         |
| `bikes_allowed`         | `bikesAllowed`         | `gtfs:bikesAllowed`         |         |

### Relationships

| GTFS Field   | NGSI Attribute | LinkedGTFS     | Comment                                           |
| :----------- | :------------- | :------------- | :------------------------------------------------ |
| `route_id`   | `hasRoute`     |                |                                                   |
| `service_id` | `hasService`   | `gtfs:service` | It shall point to an Entity of Type `GtfsService` |
| `shape_id`   | `hasShape`     | `gtfs:shape`   | It shall point to an Entity of Type `GtfsShape`   |

### Open issues
