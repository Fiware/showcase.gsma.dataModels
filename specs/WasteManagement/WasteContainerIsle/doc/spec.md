# Waste Container Isle

**Note: The latest version of this Data Model can be found at
[https://github.com/smart-data-models/dataModel.WasteManagement](https://github.com/smart-data-models/dataModel.WasteManagement)**

## Description

A geographical area which keeps one or more waste containers.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `WasteContainerIsle`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `location` : Location of the isle represented by a GeoJSON Polygon.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory

-   `address` : Civic address where the isle is located.

    -   Attribute type: Property. [Address](https://schema.org/address)
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Optional

-   `name` : Name given to the isle

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to
        [name](https://schema.org/name)
    -   Optional

-   `description` : Description about the isle.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `insertHolesNumber` : Number of insert holes the isle has.

    -   Attribute type: Property. [Number](https://schema.org/Number).
    -   Optional

-   `features` : A list of features provided by the isle.

    -   Attribute type: Property. List of [Text](http://schema.org/Text).
    -   Allowed values:
        -   `containerFix`. Allows to fix containers to a permanent position.
        -   `fenced`. The isle is properly fenced.
        -   `underground`. The isle allows to hold buried containers.
    -   Any other value meaningful to the application.
    -   Optional

-   `refWasteContainer` : List of containers present in the isle.

    -   Attribute type: Relationship. List of references to
        [WasteContainer](../../WasteContainer/doc/spec.md) entities.
    -   Allowed values. Container's ID.
    -   Optional

-   `areaServed` : Higher level area to which the isle belongs to. It can be
    used to group isles per responsible, district, neighbourhood, etc.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

-   `dateModified` : Last update timestamp of this entity

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `availableSince` : Creation timestamp of the isle (This might different than
    the entity creation time)
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "wastecontainerisle:Fleming:12",
    "type": "WasteContainerIsle",
    "refWasteContainer": {
        "type": "Relationship",
        "value": ["wastecontainer:Fleming:12a", "wastecontainer:Fleming:12b"]
    },
    "features": {
        "value": ["underground"]
    },
    "description": {
        "value": "Container isle located downtown"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-3.164485591715449, 40.62785133667262],
                    [-3.164445130316209, 40.62787156737224],
                    [-3.164394553567159, 40.62777209976578],
                    [-3.164424899616589, 40.62775018317452],
                    [-3.164485591715449, 40.62785133667262]
                ]
            ]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Guadalajara",
            "addressCountry": "ES",
            "streetAddress": "Calle Dr. Fleming, 12"
        }
    },
    "name": {
        "value": "Dr. Fleming 12, Esquina Manuel Paez Xaramillo"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "wastecontainerisle:Fleming:12",
    "type": "WasteContainerIsle",
    "location": {
        "type": "Polygon",
        "coordinates": [
            [
                [-3.164485591715449, 40.62785133667262],
                [-3.164445130316209, 40.627871567372239],
                [-3.164394553567159, 40.627772099765778],
                [-3.164424899616589, 40.62775018317452],
                [-3.164485591715449, 40.62785133667262]
            ]
        ]
    },
    "address": {
        "streetAddress": "Calle Dr. Fleming, 12",
        "addressLocality": "Guadalajara",
        "addressCountry": "ES"
    },
    "features": ["underground"],
    "name": "Dr. Fleming 12, Esquina Manuel Paez Xaramillo",
    "description": "Container isle located downtown",
    "containers": ["wastecontainer:Fleming:12a", "wastecontainer:Fleming:12b"]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:WasteContainerIsle:wastecontainerisle:Fleming:12",
    "type": "WasteContainerIsle",
    "refWasteContainer": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:WasteContainer:wastecontainer:Fleming:12a",
            "urn:ngsi-ld:WasteContainer:wastecontainer:Fleming:12b"
        ]
    },
    "features": {
        "type": "Property",
        "value": ["underground"]
    },
    "description": {
        "type": "Property",
        "value": "Container isle located downtown"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-3.164485591715449, 40.62785133667262],
                    [-3.164445130316209, 40.62787156737224],
                    [-3.164394553567159, 40.62777209976578],
                    [-3.164424899616589, 40.62775018317452],
                    [-3.164485591715449, 40.62785133667262]
                ]
            ]
        }
    },
    "address": {
        "type": "Property",
        "value": {
            "addressLocality": "Guadalajara",
            "addressCountry": "ES",
            "streetAddress": "Calle Dr. Fleming, 12",
            "type": "PostalAddress"
        }
    },
    "name": {
        "type": "Property",
        "value": "Dr. Fleming 12, Esquina Manuel Paez Xaramillo"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

T.B.D.
