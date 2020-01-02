# GtfsStop

## Description

See
[https://developers.google.com/transit/gtfs/reference/#stopstxt](https://developers.google.com/transit/gtfs/reference/#stopstxt)

It represents a GTFS `stop` which `location_type` shall be equal to `0`.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:GtfsStop:<stop_identifier>` being
        `stop_identifier` a value that can derived from the GTFS `stop_id`
        field.

-   `type`: Entity Type

    -   It shall be equal to `GtfsStop`

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

-   `name`: Same as GTFS `stop_name`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to
        [name](https://schema.org/name)
    -   Mandatory

-   `code`: Same as GTFS `stop_code`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `page`: Same as GTFS `stop_url`.

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `description`: Same as GTFS `stop_desc`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `location`: Stop's location encoded as GeoJSON Point which coordinates shall
    be in the form \[`stop_long`,`stop_lat`\].

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
        [GtfsStation](../../GtfsStation/doc/spec.md)
    -   Optional

-   `operatedBy` : Agency that operates this stop.
    -   Attribute type: List of Relationships. They shall point to an Entity of
        Type [GtfsAgency](../../GtfsAgency/doc/spec.md)
    -   Optional

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsStop:Malaga_101",
    "type": "GtfsStop",
    "code": {
        "value": "101"
    },
    "operatedBy": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
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
    "id": "urn:ngsi-ld:GtfsStop:Malaga_101",
    "type": "GtfsStop",
    "code": "101",
    "name": "Alameda Principal (Sur)",
    "location": {
        "type": "Point",
        "coordinates": [-4.424393, 36.716872]
    },
    "operatedBy": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsStop:Malaga_101",
    "type": "GtfsStop",
    "code": {
        "type": "Property",
        "value": "101"
    },
    "operatedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-4.424393, 36.716872]
        }
    },
    "name": {
        "type": "Property",
        "value": "Alameda Principal Sur"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
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

| GTFS Field       | NGSI Attribute     | LinkedGTFS           | Comment                                             |
| :--------------- | :----------------- | :------------------- | :-------------------------------------------------- |
| `parent_station` | `hasParentStation` | `gtfs:parentStation` | Shall point to another Entity of Type `GtfsStation` |
|                  | `operatedBy`       |                      | Shall point to another Entity of Type `GtfsAgency`  |

## Open issues
