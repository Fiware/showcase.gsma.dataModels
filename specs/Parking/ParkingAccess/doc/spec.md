# Parking access

**Note: The latest version of this Data Model can be found at
[https://github.com/smart-data-models/dataModel.Parking](https://github.com/smart-data-models/dataModel.Parking)**

## Description

Represents an access point to a parking site, normally an offstreet parking.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `ParkingAccess`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `location` : Geolocation of the access point represented by a GeoJSON Point.

    -   Attribute type: GeoProperty. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `location` : Geolocation of the access point represented by a GeoJSON Point.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory

-   `address` : Registered civic address of the access point.

    -   Attribute type: Property. [Address](https://schema.org/address)
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Optional

-   `name` : Name given to the access point.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to
        [name](https://schema.org/name)
    -   Optional

-   `description` : Description of the access point.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `category` : Category of the access point (entrance, exit, etc.)

    -   Attribute type: Property. List of
        [https://schema.org/Text](https://schema.org/Text)
    -   Allowed values: Those specificed by the DATEX II _AccessCategoryEnum_. -
        Other values meaningful to the application.
    -   Mandatory

-   `refOffStreetParking` : The offstreet parking site this access point gives
    access to.

    -   Attribute type: Relationship. Reference to an entity of type
        [OffStreetParking](../../OffStreetParking/doc/spec.md)
    -   Mandatory

-   `features` : Equipment or facilities provided by the access point.

    -   Attribute type: Property. List of
        [https://schema.org/Text](https://schema.org/Text)
    -   Allowed values: Those specified by the DATEX II _essEquipmentEnum_ and
        by _AccessibilityEnum_.
        -   Other values meaningful to the application.
    -   Optional

-   `image` : A URL containing a photo of this access point.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `width` : Width of the access point.

    -   Normative References:
        [https://schema.org/width](https://schema.org/width)
    -   Optional

-   `height` : Height of the access point.

    -   Normative References:
        [https://schema.org/height](https://schema.org/height)
    -   Optional

-   `slope` : Slope of the access point (in relative terms).
    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Attribute Value: A number between 0 and 1.
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "accesspoint-trinidade-1",
    "type": "ParkingAccess",
    "category": {
        "value": ["vehicleEntrance"]
    },
    "name": {
        "value": "Trinidade main entrance"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-8.60961198807, 41.150691773]
        }
    },
    "refOffStreetParking": {
        "type": "Relationship",
        "value": "porto-OffStreetParking-23889"
    },
    "features": {
        "value": ["barrier"]
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "accesspoint-trinidade-1",
    "type": "ParkingAccess",
    "name": "Trinidade main entrance",
    "location": {
        "coordinates": [-8.60961198807, 41.150691773],
        "type": "Point"
    },
    "category": ["vehicleEntrance"],
    "refOffStreetParking": "porto-OffStreetParking-23889",
    "features": ["barrier"]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:ParkingAccess:accesspoint-trinidade-1",
    "type": "ParkingAccess",
    "category": {
        "type": "Property",
        "value": ["vehicleEntrance"]
    },
    "name": {
        "type": "Property",
        "value": "Trinidade main entrance"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-8.60961198807, 41.150691773]
        }
    },
    "refOffStreetParking": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:OffStreetParking:porto-OffStreetParking-23889"
    },
    "features": {
        "type": "Property",
        "value": ["barrier"]
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

## Open issues
