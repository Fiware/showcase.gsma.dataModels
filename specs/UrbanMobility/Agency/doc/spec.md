# gtfs:Agency

## Description

See
[https://developers.google.com/transit/gtfs/reference/#agencytxt](https://developers.google.com/transit/gtfs/reference/#agencytxt)

## Data Model

The data model is defined as shown below:

- `id`: Entity ID.

  - It shall be `urn:ngsi-ld:gtfs:Agency:<agency_identifier>` being
        `agency_identifier` a value that can be derived from GTFS `agency_id`.

- `type`: Entity type.

  - It shall be equal to `gtfs:Agency`.

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

- `dateCreated` : Entity's creation timestamp.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `dateModified` : Last update timestamp of this Entity.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `source` : A sequence of characters giving the original source of the Entity
    data as a URL. It shall point to the URL of the original GTFS feed used to
    generate this Entity. + Attribute type: [URL](https://schema.org/URL) +
    Mandatory

- `name`: Same as GTFS `agency_name`.

  - Attribute type: Property. [Text](https://schema.org/Text).
  - Mandatory

- `page`: Same as GTFS `agency_url`.

  - Attribute type: Property. [URL](https://schema.org/URL).
  - Optional

- `timezone`: Same as GTFS `agency_timezone`.

  - Attribute type: Property. [Text](https://schema.org/Text).
  - Allowed values: See
        [GTFS](https://developers.google.com/transit/gtfs/reference/#agencytxt)
  - Optional

- `phone`: Same as GFTS `agency_phone`.

  - Attribute type: Property. [Text](https://schema.org/Text)
  - Optional

- `language`: Same as GTFS `agency_language`.

  - Attribute type: Property. [Text](https://schema.org/Text)
  - Allowed values: See
        [GTFS](https://developers.google.com/transit/gtfs/reference/#agencytxt)
  - Optional

- `address`: Agency's civic address.
  - Attribute type: Property.
        [PostalAddress](https://schema.org/PostalAddress)
  - Optional

### Example of use 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:gtfs:Agency:Malaga_EMT",
    "type": "gtfs:Agency",
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

### Example of use 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:gtfs:Agency:Malaga_EMT",
    "type": "gtfs:Agency",
    "name": "Empresa Malagueña de Transportes",
    "page": "http://www.emtmalaga.es/",
    "timezone": "Europe/Madrid",
    "language": "ES",
    "source": "http://datosabiertos.malaga.eu/dataset/lineas-y-horarios-bus-google-transit/resource/24e86888-b91e-45bf-a48c-09855832fd52"
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
