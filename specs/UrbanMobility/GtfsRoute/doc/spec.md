# GtfsRoute

## Description

See
[https://developers.google.com/transit/gtfs/reference/#routestxt](https://developers.google.com/transit/gtfs/reference/#routestxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID.

    -   It shall be `urn:ngsi-ld:GtfsRoute:<route_identifier>` being
        `route_identifier` a value that can be derived from GTFS `route_id`.

-   `type`: Entity type.

    -   It shall be equal to `GtfsRoute`.

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

-   `shortName`: Same as GTFS `route_short_name`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Mandatory

-   `name`: Same as GTFS `route_long_name`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Mandatory

-   `description`: Same as GTFS `route_desc`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Optional

-   `routeType`: Same as GTFS `route_type`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Allowed values: Those allowed for `route_type` as prescribed by
        [GTFS](https://developers.google.com/transit/gtfs/reference/#routestxt)
    -   Mandatory

-   `page`: Same as GTFS `route_url`.

    -   Attribute type: Property. [URL](https://schema.org/URL).
    -   Optional

-   `routeColor`: Same as GTFS `route_color`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Allowed values: See
        [GTFS](https://developers.google.com/transit/gtfs/reference/#routestxt)
    -   Optional

-   `routeTextColor`: Same as GFTS `route_text_color`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `routeSortOrder`: Same as GTFS `route_sort_order`.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Optional

-   `operatedBy` : Agency that operates this route.
    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsAgency](../../GtfsAgency/doc/spec.md)
    -   Mandatory

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsRoute:Spain:Malaga:1",
    "type": "GtfsRoute",
    "name": {
        "value": "Parque del Sur _ Alameda Principal _ San Andr\u00e9s"
    },
    "shortName": {
        "value": "1"
    },
    "page": {
        "value": "http://www.emtmalaga.es/emt-mobile/informacionLinea.html"
    },
    "routeType": {
        "value": "3"
    },
    "operatedBy": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsRoute:Spain:Malaga:1",
    "type": "GtfsRoute",
    "shortName": "1",
    "name": "Parque del Sur - Alameda Principal - San Andrés",
    "page": "http://www.emtmalaga.es/emt-mobile/informacionLinea.html",
    "routeType": "3",
    "operatedBy": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsRoute:Spain:Malaga:1",
    "type": "GtfsRoute",
    "name": {
        "type": "Property",
        "value": "Parque del Sur _ Alameda Principal _ San Andr\u00e9s"
    },
    "shortName": {
        "type": "Property",
        "value": "1"
    },
    "page": {
        "type": "Property",
        "value": "http://www.emtmalaga.es/emt-mobile/informacionLinea.html"
    },
    "routeType": {
        "type": "Property",
        "value": "3"
    },
    "operatedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsAgency:Malaga_EMT"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field         | NGSI Attribute   | LinkedGTFS        | Comment |
| :----------------- | :--------------- | :---------------- | :------ |
| `route_short_name` | `shortName`      | `gtfs:shortName`  |         |
| `route_long_name`  | `name`           | `gtfs:longName`   |         |
| `route_type`       | `routeType`      | `gtfs:routeType`  |         |
| `route_desc`       | `description`    | `dct:description` |         |
| `route_url`        | `page`           | `foaf:page`       |         |
| `route_color`      | `routeColor`     | `gtfs:color`      |         |
| `route_text_color` | `routeTextColor` | `gtfs:textColor`  |         |
| `route_sort_order` | `routeSortOrder` |                   |         |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS    | Comment                                            |
| :--------- | :------------- | :------------ | :------------------------------------------------- |
|            | `operatedBy`   | `gtfs:agency` | Shall point to another Entity of Type `GtfsAgency` |

### Open issues
