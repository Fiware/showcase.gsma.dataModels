# gtfs:Stop

## Description

See
[https://developers.google.com/transit/gtfs/reference/#stopstxt](https://developers.google.com/transit/gtfs/reference/#stopstxt)

It represents a GTFS `stop` which `location_type` shall be equal to `0`.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:gtfs:Stop:<stop_identifier>` being
        `stop_identifier` a value that can derived from the GTFS `stop_id`
        field.

-   `type`: Entity Type

    -   It shall be equal to `gtfs:Stop`

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

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name`: Same as GTFS `stop_name`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory

-   `code`: Same as GTFS `stop_code`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `page`: Same as GTFS `stop_url`.

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `description`: Same as GTFS `stop_desc`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `location`: Stop's location encoded as GeoJSON Point which coordinates shall
    be in the form [`stop_long`,`stop_lat`].

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References: [rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory

-   `wheelChairAccessible`: Same as GTFS `wheelchair_boarding`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: (`0`, `1`, `2`) as per the
        [GTFS](https://developers.google.com/transit/gtfs/reference/#stopstxt)
    -   Optional

-   `zoneCode` : Transport zone to which this stop belongs to. Same as GTFS
    `zone_id`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `address`: Stop's civic address.

    -   Attribute type: Property.
        [PostalAddress](https://schema.org/PostalAddress)
    -   Optional

-   `hasParentStation` : Same as GTFS `parent_station`.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [gtfs:Station](../../Station/doc/spec.md)
    -   Optional

-   `operatedBy` : Agency that operates this stop.
    -   Attribute type: Relationship. It shall point to an Entity of Type
        [gtfs:Agency](../../Agency/doc/spec.md)
    -   Mandatory

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:gtfs:Stop:Malaga_101",
    "type": "gtfs:Stop",
    "code": {
        "value": "101"
    },
    "operatedBy": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:gtfs:Agency:Malaga_EMT"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-4.424393, 36.716872]
        }
    },
    "name": {
        "value": "Alameda Principal Sur"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`


```json
{
    "id": "urn:ngsi-ld:gtfs:Stop:Malaga_101",
    "type": "gtfs:Stop",
    "code": "101",
    "name": "Alameda Principal (Sur)",
    "location": {
        "type": "Point",
        "coordinates": [-4.424393, 36.716872]
    },
    "operatedBy": "urn:ngsi-ld:gtfs:Agency:Malaga_EMT"
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field            | NGSI Attribute         | LinkedGTFS                  | Comment                                                  |
| :-------------------- | :--------------------- | :-------------------------- | :------------------------------------------------------- |
| `stop_name`           | `name`                 | `foaf:name`                 |                                                          |
| `stop_code`           | `code`                 | `gtfs:code`                 |                                                          |
| `stop_url`            | `page`                 | `foaf:page`                 |                                                          |
| `stop_desc`           | `description`          | `dct:description`           |                                                          |
| `stop_long,stop_lat`  | `location`             | `geo:long`,`geo:lat`        | Encoded as a GeoJSON Point.                              |
| `zone_id`             | `zoneCode`             |                             |                                                          |
| `wheelchair_boarding` | `wheelChairAccessible` | `gtfs:wheelChairAccessible` | `0`, `1`, `2` as per GTFS spec.                          |
|                       | `address`              |                             | Stop's [address](https://schema.org/address). Schema.org |

### Relationships

| GTFS Field       | NGSI Attribute     | LinkedGTFS           | Comment                                              |
| :--------------- | :----------------- | :------------------- | :--------------------------------------------------- |
| `parent_station` | `hasParentStation` | `gtfs:parentStation` | Shall point to another Entity of Type `gtfs:Station` |
|                  | `operatedBy`       |                      | Shall point to another Entity of Type `gtfs:Agency`  |

## Open issues
