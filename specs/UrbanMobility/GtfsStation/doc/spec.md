# GtfsStation

## Description

See
[https://developers.google.com/transit/gtfs/reference/#stopstxt](https://developers.google.com/transit/gtfs/reference/#stopstxt)

It is a GTFS `stop` which `location_type` is equal to `1`.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:gtfs:Station:<station_identifier>` being
        `station_identifier` a value that can derived from the `stop_id` field.

-   `type`: Entity Type

    -   It shall be equal to `GtfsStation`

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

-   `hasStop` : It shall point to another Entity(ies) of type `GtfsStop`

    -   Type: Relationship. List of [GtfsStop](../../GtfsStop/doc/spec.md).
    -   Mandatory

-   `hasAccessPoint` : It shall point to another Entity(ies) of type
    `GtfsAccessPoint`
    -   Type: Relationship. List of
        [GtfsAccessPoint](../../GtfsAccessPoint/doc/spec.md).
    -   Optional

The specification for the following attributes is the one mandanted by
[GtfsStop](../../GtfsStop/doc/spec.md):

-   `name`
-   `code`
-   `page`
-   `description`
-   `location`
-   `wheelChairAccessible`
-   `zoneCode`
-   `address`
-   `hasParentStation`

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsStation:Madrid:est_90_21",
    "type": "GtfsStation",
    "code": {
        "value": "21"
    },
    "name": {
        "value": "Intercambiador de Plaza de Castilla"
    },
    "hasStop": {
        "type": "Relationship",
        "value": ["urn:ngsi-ld:GtfsStop:Madrid_par_4_1"]
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.6892, 40.4669]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Madrid",
            "addressCountry": "ES",
            "streetAddress": "Paseo de la Castellana 189"
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsStation:Madrid:est_90_21",
    "type": "GtfsStation",
    "code": "21",
    "name": "Intercambiador de Plaza de Castilla",
    "location": {
        "type": "Point",
        "coordinates": [-3.6892, 40.4669]
    },
    "address": {
        "streetAddress": "Paseo de la Castellana 189",
        "addressLocality": "Madrid",
        "addressCountry": "ES"
    },
    "hasStop": ["urn:ngsi-ld:GtfsStop:Madrid_par_4_1"]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsStation:Madrid:est_90_21",
    "type": "GtfsStation",
    "code": {
        "type": "Property",
        "value": "21"
    },
    "name": {
        "type": "Property",
        "value": "Intercambiador de Plaza de Castilla"
    },
    "hasStop": {
        "type": "Relationship",
        "object": ["urn:ngsi-ld:GtfsStop:Madrid_par_4_1"]
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-3.6892, 40.4669]
        }
    },
    "address": {
        "type": "Property",
        "value": {
            "addressLocality": "Madrid",
            "addressCountry": "ES",
            "streetAddress": "Paseo de la Castellana 189",
            "type": "PostalAddress"
        }
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

### Properties

Same as [GtfsStop](../../GtfsStop/doc/spec.md)

### Relationships

| GTFS Field | NGSI Attribute     | LinkedGTFS | Comment                                           |
| :--------- | :----------------- | :--------- | :------------------------------------------------ |
|            | `hasStop`          |            | shall point to Entities of type `GtfsStop`        |
|            | `hasAccessPoint`   |            | shall point to Entities of type `GtfsAccessPoint` |
|            | `hasParentStation` |            | shall point to an Entity of type `GtfsStation`    |

## Open issues
