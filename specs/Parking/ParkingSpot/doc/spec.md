# Parking Spot

**Note: The latest version of this Data Model can be found at
[https://github.com/smart-data-models/dataModel.Parking](https://github.com/smart-data-models/dataModel.Parking)**

## Description

A parking spot is an area well delimited where _one_ vehicle can be parked. The
aim of this entity type is to monitor the status of parking spots individually.
Thus, an entity of type `ParkingSpot` cannot exist without a containing entity
of type (`OnStreetParking`, `OffStreetParking`). A parking spot might belong to
_one_ group.

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier.

-   `type` : Entity type. It must be equal to `ParkingSpot`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateCreated` : Entity creation date.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateCreated` : Entity creation date.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name` : Name of this parking spot. It can denote the number or label used
    to identify it within a parking site.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to
        [name](https://schema.org/name)
    -   Optional

-   `description` : Description about the parking spot.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `location` : Geolocation of the parking spot, represented by a GeoJSON
    Point.

    -   Attribute type: Property. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory. (if `address` is not defined).

-   `address` : Registered parking spot civic address.

    -   Attribute type: Property. [Address](https://schema.org/address)
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory. (if `location` is not defined).

-   `status` : Status of the parking spot from the point of view of occupancy.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed Values: one Of (`occupied`, `free`, `closed`, `unknown`)
    -   Metadata:
        -   `timestamp` : Timestamp which reflects the date when the attribute
            value was obtained.
            -   Type: [DateTime](https://schema.org/DateTime)
            -   Optional
    -   `TimeInstant` :
        [Timestamp](https://github.com/telefonicaid/iotagent-node-lib#TimeInstant)
        saved by FIWARE's IoT Agents. Note: This attribute has not been
        harmonized to keep backwards compatibility with current FIWARE reference
        implementations.
        -   Type: [DateTime](https://schema.org/DateTime). here can be
            production environmments where the attribute type is equal to the
            `ISO8601` string. If so, it must be considered as a synonym of
            `DateTime`.
        -   Optional
    -   Mandatory

-   `width` : Width of the parking spot.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Optional

-   `length` : Length of the parking spot.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Optional

-   `refParkingGroup` : Group to which the parking spot belongs to. For model
    simplification purposes only one group is allowed per parking spot.

    -   Attribute type: Relationship. Reference to an entity of type
        `ParkingGroup`.
    -   Optional

-   `refParkingSite` : Parking site to which the parking spot belongs to.

    -   Attribute type: Relationship. Reference to an entity of type
        `OnStreetParking` or type `OffStreetParking`, depending on the value of
        the `category` attribute.
    -   Mandatory

-   `category` : Category(ies) of the parking spot.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values:
        -   `onstreet` : The parking spot belongs to an onstreet parking site.
        -   `offstreet` : The parking spot belongs to an onstreet parking site.
        -   Other values as per application needs
    -   Mandatory

-   `TimeInstant` :
    [Timestamp](https://github.com/telefonicaid/iotagent-node-lib#TimeInstant)
    saved by FIWARE's IoT Agent. Note: This attribute has not been harmonized to
    keep backwards compatibility with current FIWARE reference implementations.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime). There
        can be production environmments where the attribute type is equal to the
        `ISO8601` string. If so, it must be considered as a synonym of
        `DateTime`.
    -   Optional

-   `refDevice` : The device representing the physical sensor used to monitor
    this parking spot.
    -   Attribute type: Relationship. Reference to entity of type
        [Device](../../../Device/Device/doc/spec.md)
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "santander:daoiz_velarde_1_5:3",
    "type": "ParkingSpot",
    "status": {
        "value": "free",
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2018-09-21T12:00:00"
            }
        }
    },
    "category": {
        "value": ["onstreet"]
    },
    "refParkingSite": {
        "type": "Relationship",
        "value": "santander:daoiz_velarde_1_5"
    },
    "name": {
        "value": "A-13"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.80356167695194, 43.46296641666926]
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "santander:daoiz_velarde_1_5:3",
    "type": "ParkingSpot",
    "name": "A-13",
    "location": {
        "type": "Point",
        "coordinates": [-3.80356167695194, 43.46296641666926]
    },
    "status": "free",
    "category": ["onstreet"],
    "refParkingSite": "santander:daoiz_velarde_1_5"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
    "type": "ParkingSpot",
    "status": {
        "type": "Property",
        "value": "free",
        "observedAt": "2018-09-21T12:00:00Z"
    },
    "category": {
        "type": "Property",
        "value": ["onstreet"]
    },
    "refParkingSite": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:ParkingSite:santander:daoiz_velarde_1_5"
    },
    "name": {
        "type": "Property",
        "value": "A-13"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-3.80356167695194, 43.46296641666926]
        }
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

## Open issues
