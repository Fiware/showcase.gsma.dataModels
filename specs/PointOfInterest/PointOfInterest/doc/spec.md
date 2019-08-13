# Point of interest

**Note: The latest version of this Data Model can be 
found at [https://github.com/smart-data-models/dataModel.PointOfInterest](https://github.com/smart-data-models/dataModel.PointOfInterest)**

## Description

This entity contains a harmonised geographic description of a Point of Interest.
This entity is used in applications that use spatial data and is applicable to
Automotive, Environment, Industry and Smart City vertical segments and related
IoT applications. This data model has been created in cooperation with the GSMA
and the members of the
[IoT Big Data Project](http://www.gsma.com/iot/iot-big-data/).

## Data Model

A JSON Schema corresponding to this data model can be found
[here](http://fiware.github.io/dataModels/specs/PointOfInterest/PointOfInterest/schema.json)

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `PointOfInterest`.

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
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

-   `name` : Name of this point of interest.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `alternateName` : Alternative name for this point of interest.

    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional

-   `description` : Description of this point of interest.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `location` : Location of the point of interest represented by a GeoJSON
    geometry, usually a `Point`.

    -   Attribute type: Property. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Civic address of this point of interest.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `category` : Category of this point of interest.

    -   Attribute type: Property. List of [Text](https://schema.org/Text)
    -   Allowed values: Those defined by the
        [Factual taxonomy](https://github.com/Factual/places/blob/master/categories/factual_taxonomy.json)
        together with the extended categories described by the present
        specification (see below). For instance the value `113` corresponds to
        beaches, and the value `311` corresponds to museums.
    -   Mandatory

-   `contactPoint` : Contact point of this point of interest.

    -   Normative references:
        [https://schema.org/contactPoint](https://schema.org/contactPoint)
    -   Optional

-   `refSeeAlso` : Reference to one or more related entities that may provide
    extra, specific information about this point of interest.

    -   Attribute type: Property. List of References
    -   Optional

## Extended POI Categories

| Category | Description                |
| :------- | :------------------------- |
| `1478`   | `Public drinking fountain` |
| `1479`   | `Public toilet`            |
| `1480`   | `Registry office`          |

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "PointOfInterest-A-Concha-123456",
    "type": "PointOfInterest",
    "category": {
        "value": ["113"]
    },
    "description": {
        "value": "La Playa de A Concha se presenta como una continuaci\u00f3n de la Playa de Compostela, una de las m\u00e1s frecuentadas de Vilagarc\u00eda."
    },
    "refSeeAlso": {
        "type": "Relationship",
        "value": ["Beach-A-Concha-123456"]
    },
    "source": {
        "value": "http://www.tourspain.es"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-8.768460000000001, 42.60214472222222]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressCountry": "ES",
            "addressLocality": "Vilagarc\u00eda de Arousa"
        }
    },
    "name": {
        "value": "Playa de a Concha"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "PointOfInterest-A-Concha-123456",
    "type": "PointOfInterest",
    "name": "Playa de a Concha",
    "description": "La Playa de A Concha se presenta como una continuación de la Playa de Compostela, una de las más frecuentadas de Vilagarcía.",
    "address": {
        "addressCountry": "ES",
        "addressLocality": "Vilagarcía de Arousa"
    },
    "category": ["113"],
    "location": {
        "type": "Point",
        "coordinates": [-8.768460000000001, 42.60214472222222]
    },
    "source": "http://www.tourspain.es",
    "refSeeAlso": ["Beach-A-Concha-123456"]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:PointOfInterest:PointOfInterest-A-Concha-123456",
    "type": "PointOfInterest",
    "category": {
        "type": "Property",
        "value": ["113"]
    },
    "description": {
        "type": "Property",
        "value": "La Playa de A Concha se presenta como una continuaci\u00f3n de la Playa de Compostela, una de las m\u00e1s frecuentadas de Vilagarc\u00eda."
    },
    "refSeeAlso": {
        "type": "Relationship",
        "object": ["urn:ngsi-ld:SeeAlso:Beach-A-Concha-123456"]
    },
    "source": {
        "type": "Property",
        "value": "http://www.tourspain.es"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-8.768460000000001, 42.60214472222222]
        }
    },
    "address": {
        "type": "Property",
        "value": {
            "addressCountry": "ES",
            "addressLocality": "Vilagarc\u00eda de Arousa",
            "type": "PostalAddress"
        }
    },
    "name": {
        "type": "Property",
        "value": "Playa de a Concha"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Use it with a real service

The instance described
[here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing)
has been set up by the FIWARE Community.

## Open Issues
