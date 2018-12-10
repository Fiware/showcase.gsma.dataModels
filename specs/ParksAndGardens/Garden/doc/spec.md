# Garden

## Description

A garden is a distinguishable planned space, usually outdoors, set aside for the
display, cultivation, and enjoyment of plants and other forms of nature.

## Data Model

A JSON Schema corresponding to this data model can be found
{{add link to JSON Schema}}

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `Garden`.

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `location` : Location of this garden represented by a GeoJSON geometry.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.
-   `address` : Civic address of this garden.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `name` : Garden's name.
    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory
-   `alternateName` : Garden's alternate name.
    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional
-   `description` : Garden's description

    -   Normative References: [https://schema.org/description]
    -   Optional

-   `category` : Garden's category.
    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed Values: (`public`, `private`, `botanical`, `castle`,
        `community`, `monastery`, `residential`, `fencedOff`) or any other value
        needed by an application.
    -   Optional
-   `style` : Garden's style.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Allowed values: See
        [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Key:garden:style)
    -   Optional

-   `openingHours` : Opening hours of this garden.
    -   Normative references: [https://schema.org/openingHours]
    -   Optional
-   `areaServed` : Higher level area to which the garden belongs to. It can be
    used to group gardens per responsible, district, neighbourhood, etc.
    -   Attribute type: [Text](https://schema.org/Text) Optional
-   `dateLastWatering` : Timestamp which corresponds to the last watering of
    this garden.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `nextWateringDeadline` : Deadline for next watering operation to be done on
    this garden.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Optional
-   `refRecord` : List of records which contain measurements related to this
    garden.
    -   Attribute type: List of references to entities of type
        `GreenspaceRecord`
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

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

## Use it with a real service

Soon to be available

## Open Issues
