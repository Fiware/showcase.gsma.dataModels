# GtfsAccessPoint

## Description

See
[https://developers.google.com/transit/gtfs/reference/#stopstxt](https://developers.google.com/transit/gtfs/reference/#stopstxt)

It is a GTFS `stop` which `location_type` is equal to `2`.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:GtfsAccessPoint:<access_point_identifier>`
        being `access_point_identifier` a value that can derived from the
        `stop_id` field.

-   `type`: Entity Type

    -   It shall be equal to `GtfsAccessPoint`

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

The following Attributes shall be as mandated by
[GtfsStop](../../GtfsStop/doc/spec.md):

-   `name`
-   `code`
-   `page`
-   `description`
-   `location`
-   `wheelChairAccessible`
-   `address`
-   `hasParentStation`

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsAccessPoint:Madrid:acc_4_1_3",
    "type": "GtfsAccessPoint",
    "name": {
        "value": "Bravo Murillo"
    },
    "hasParentStation": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsStation:Madrid:est_90_21"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.69036, 40.46629]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Madrid",
            "addressCountry": "ES",
            "streetAddress": "Calle de Bravo Murillo 377",
            "type": "PostalAddress"
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsAccessPoint:Madrid:acc_4_1_3",
    "type": "GtfsAccessPoint",
    "name": "Bravo Murillo",
    "location": {
        "type": "Point",
        "coordinates": [-3.69036, 40.46629]
    },
    "address": {
        "type": "PostalAddress",
        "streetAddress": "Calle de Bravo Murillo 377",
        "addressLocality": "Madrid",
        "addressCountry": "ES"
    },
    "hasParentStation": "urn:ngsi-ld:GtfsStation:Madrid:est_90_21"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:AccessPoint:Madrid:acc_4_1_3",
    "type": "GtfsAccessPoint",
    "name": {
        "type": "Property",
        "value": "Bravo Murillo"
    },
    "hasParentStation": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsStation:Madrid:est_90_21"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-3.69036, 40.46629]
        }
    },
    "address": {
        "type": "Property",
        "value": {
            "addressLocality": "Madrid",
            "addressCountry": "ES",
            "streetAddress": "Calle de Bravo Murillo 377",
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

Same as `GtfsStop`.

### Relationships

| GTFS Field | NGSI Attribute     | LinkedGTFS | Comment                                                  |
| :--------- | :----------------- | :--------- | :------------------------------------------------------- |
|            | `hasParentStation` |            | shall point to another Entity(ies) of type `GtfsStation` |

## Open issues
