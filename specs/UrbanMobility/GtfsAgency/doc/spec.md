# GtfsAgency

## Description

See
[https://developers.google.com/transit/gtfs/reference/#agencytxt](https://developers.google.com/transit/gtfs/reference/#agencytxt)

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID.

    -   It shall be `urn:ngsi-ld:GtfsAgency:<agency_identifier>` being
        `agency_identifier` a value that can be derived from GTFS `agency_id`.

-   `type`: Entity type.

    -   It shall be equal to `GtfsAgency`.

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

-   `source` : A sequence of characters giving the original source of the Entity
    data as a URL. It shall point to the URL of the original GTFS feed used to
    generate this Entity.
    -  Attribute type: Property. [URL](https://schema.org/URL)
    -  Mandatory

-   `name`: Same as GTFS `agency_name`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to [name](https://schema.org/name)
    -   Mandatory

-   `page`: Same as GTFS `agency_url`.

    -   Attribute type: Property. [URL](https://schema.org/URL).
    -   Optional

-   `timezone`: Same as GTFS `agency_timezone`.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Allowed values: See
        [GTFS](https://developers.google.com/transit/gtfs/reference/#agencytxt)
    -   Optional

-   `phone`: Same as GFTS `agency_phone`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `language`: Same as GTFS `agency_language`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: See
        [GTFS](https://developers.google.com/transit/gtfs/reference/#agencytxt)
    -   Optional

-   `address`: Agency's civic address.
    -   Attribute type: Property. [Address](https://schema.org/address)
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Optional

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:GtfsAgency:Malaga_EMT",
    "type": "GtfsAgency",
    "name": {
        "value": "Empresa Malague\u00f1a de Transportes"
    },
    "language": {
        "value": "ES"
    },
    "page": {
        "value": "http://www.emtmalaga.es/"
    },
    "source": {
        "value": "http://datosabiertos.malaga.eu/dataset/lineas-y-horarios-bus-google-transit/resource/24e86888-b91e-45bf-a48c-09855832fd52"
    },
    "timezone": {
        "value": "Europe/Madrid"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:GtfsAgency:Malaga_EMT",
    "type": "GtfsAgency",
    "name": "Empresa Malagueña de Transportes",
    "page": "http://www.emtmalaga.es/",
    "timezone": "Europe/Madrid",
    "language": "ES",
    "source": "http://datosabiertos.malaga.eu/dataset/lineas-y-horarios-bus-google-transit/resource/24e86888-b91e-45bf-a48c-09855832fd52"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:GtfsAgency:Malaga_EMT",
    "type": "GtfsAgency",
    "name": {
        "type": "Property",
        "value": "Empresa Malague\u00f1a de Transportes"
    },
    "language": {
        "type": "Property",
        "value": "ES"
    },
    "page": {
        "type": "Property",
        "value": "http://www.emtmalaga.es/"
    },
    "source": {
        "type": "Property",
        "value": "http://datosabiertos.malaga.eu/dataset/lineas-y-horarios-bus-google-transit/resource/24e86888-b91e-45bf-a48c-09855832fd52"
    },
    "timezone": {
        "type": "Property",
        "value": "Europe/Madrid"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field        | NGSI Attribute | LinkedGTFS      | Comment                                                    |
| :---------------- | :------------- | :-------------- | :--------------------------------------------------------- |
| `agency_name`     | `name`         | `foaf:name`     |                                                            |
| `agency_url`      | `page`         | `foaf:page`     |                                                            |
| `agency_timezone` | `timezone`     | `gtfs:timezone` |                                                            |
| `agency_phone`    | `phone`        | `foaf:phone`    |                                                            |
| `agency_lang`     | `language`     | `dct:language`  |                                                            |
|                   | `address`      |                 | Agency's [address](https://schema.org/address). Schema.org |

### Relationships

None

### Open issues
