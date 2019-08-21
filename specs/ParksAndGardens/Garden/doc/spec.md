# Garden

## Description

A garden is a distinguishable planned space, usually outdoors, set aside for the
display, cultivation, and enjoyment of plants and other forms of nature.

## Data Model

A JSON Schema corresponding to this data model can be found
{{add link to JSON Schema}}

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `Garden`.

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `location` : Location of this garden represented by a GeoJSON geometry.
    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.
-   `address` : Civic address of this garden.

    -   Attribute type: Property. [Address](https://schema.org/address)
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `name` : Garden's name.
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to [name](https://schema.org/name)
    -   Mandatory
-   `alternateName` : Garden's alternate name.
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional
-   `description` : Garden's description

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description` equivalent to [description](https://schema.org/description)
    -   Optional

-   `category` : Garden's category.
    -   Attribute type: Property. List of [Text](https://schema.org/Text)
    -   Allowed Values: (`public`, `private`, `botanical`, `castle`,
        `community`, `monastery`, `residential`, `fencedOff`) or any other value
        needed by an application.
    -   Optional
-   `style` : Garden's style.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: See
        [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Key:garden:style)
    -   Optional

-   `openingHours` : Opening hours of this garden.
    -   Normative references:
        [https://schema.org/openingHours](https://schema.org/openingHours)
    -   Optional
-   `areaServed` : Higher level area to which the garden belongs to. It can be
    used to group gardens per responsible, district, neighbourhood, etc.
    -   Attribute type: Property. [Text](https://schema.org/Text) Optional
-   `dateLastWatering` : Timestamp which corresponds to the last watering of
    this garden.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional

-   `nextWateringDeadline` : Deadline for next watering operation to be done on
    this garden.
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional
-   `refRecord` : List of records which contain measurements related to this
    garden.
    -   Attribute type: Relationship. List of references to entities of type
        `GreenspaceRecord`
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "Santander-Garden-Piquio",
    "type": "Garden",
    "category": {
        "value": ["public"]
    },
    "style": {
        "value": "french"
    },
    "description": {
        "value": "Jardines de Piquio. Zona El Sardinero"
    },
    "dateLastWatering": {
        "type": "DateTime",
        "value": "2017-03-31T:08:00"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.7836974, 43.4741091]
        }
    },
    "refRecord": {
        "type": "Relationship",
        "value": ["Santander-Garden-Piquio-Record-1"]
    },
    "areaServed": {
        "value": "El Sardinero"
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Santander",
            "postalCode": "39005",
            "streetAddress": "Avenida Casta\u00f1eda"
        }
    },
    "openingHours": {
        "value": "Mo-Su"
    },
    "name": {
        "value": "Jardines de Piquio"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "Santander-Garden-Piquio",
    "type": "Garden",
    "name": "Jardines de Piquio",
    "description": "Jardines de Piquio. Zona El Sardinero",
    "location": {
        "type": "Point",
        "coordinates": [-3.7836974, 43.4741091]
    },
    "address": {
        "streetAddress": "Avenida Castañeda",
        "addressLocality": "Santander",
        "postalCode": "39005"
    },
    "openingHours": "Mo-Su",
    "style": "french",
    "category": ["public"],
    "areaServed": "El Sardinero",
    "dateLastWatering": "2017-03-31T:08:00",
    "refRecord": ["Santander-Garden-Piquio-Record-1"]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:Garden:Santander-Garden-Piquio",
    "type": "Garden",
    "category": {
        "type": "Property",
        "value": ["public"]
    },
    "style": {
        "type": "Property",
        "value": "french"
    },
    "description": {
        "type": "Property",
        "value": "Jardines de Piquio. Zona El Sardinero"
    },
    "dateLastWatering": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2017-03-31T08:00:00Z"
        }
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-3.7836974, 43.4741091]
        }
    },
    "refRecord": {
        "type": "Relationship",
        "object": ["urn:ngsi-ld:Record:Santander-Garden-Piquio-Record-1"]
    },
    "areaServed": {
        "type": "Property",
        "value": "El Sardinero"
    },
    "address": {
        "type": "Property",
        "value": {
            "addressLocality": "Santander",
            "postalCode": "39005",
            "streetAddress": "Avenida Casta\u00f1eda",
            "type": "PostalAddress"
        }
    },
    "openingHours": {
        "type": "Property",
        "value": "Mo-Su"
    },
    "name": {
        "type": "Property",
        "value": "Jardines de Piquio"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Use it with a real service

Soon to be available

## Open Issues
