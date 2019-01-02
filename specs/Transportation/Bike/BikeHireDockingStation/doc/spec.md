# Bike Hire Docking Station

## Description

Many cities provide a bike hiring system for citizens. These can hire a bike
base on different types of subscriptions. A bike hire docking station where
subscribed users can hire and return a bike. It provides data about its main
features and availability of bikes and free slots.

## Data Model

A JSON Schema corresponding to this data model can be found
[here](https://fiware.github.io/dataModels/specs/Transportation/Bike/BikeHireDockingStation/schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `BikeHireDockingStation`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Normative References:
        [http://schema.org/DateTime](http://schema.org/DateTime)[ ](http://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Normative References:
        [http://schema.org/DateTime](http://schema.org/DateTime)[ ](http://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `location` : Geolocation of the station represented by a GeoJSON
    (Multi)Polygon or Point.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Registered docking station site civic address.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not defined.

-   `name` : Name given to the docking station.

    -   Attribute type: [Text](http://schema.org/Number)
    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `description` : Description about the bike hire docking station.

    -   Attribute type: [Text](http://schema.org/Number)
    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `image` : A URL containing a photo of this docking station.

    -   Attribute type: [image (URL)](http://schema.org/Number)
    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `totalSlotNumber` : The total number of slots offered by this bike docking
    station.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: Any positive integer number or 0.
    -   Optional

-   `freeSlotNumber` : The number of slots available for returning and parking
    bikes. It must lower or equal than `totalSlotNumber`.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: A positive integer number, including 0. It must lower or
        equal than `totalSlotNumber`.
    -   Metadata: 
        - `timestamp` : Timestamp of the last attribute update. 
            - Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `outOfServiceSlotNumber` : The number of slots that are out of order and
    cannot be used to hire or park a bike. It must lower or equal than
    `totalSlotNumber`.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: A positive integer number, including 0.
    -   Metadata: 
        - `timestamp` : Timestamp of the last attribute update 
            - Type: [DateTime](https://schema.org/DateTime)
        -   Optional

-   `availableBikeNumber` : The number of bikes available in the bike hire
    docking station to be hired by users.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: A positive integer number, including 0.
    -   Metadata: 
        - `timestamp` : Timestamp of the last attribute update. 
            - Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `openingHours` : Opening hours of the docking station.

    -   Normative references:
        [http://schema.org/openingHours](http://schema.org/openingHours)
    -   Optional

-   `status` : Status of the bike hire docking station.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Metadata: 
        - `timestamp` : Timestamp of the last attribute update. 
            - Type: [DateTime](https://schema.org/DateTime)
    -   Allowed values: 
        - (`working`, `outOfService`, `withIncidence`, `full`,
        `almostFull`, `empty`, `almostEmpty`) 
        - Or any other application+specific.
    -   Optional

-   `areaServed` : Area served by this docking station. Precise semantics can
    depend on the application or target city. For instance, it can be a
    neighbourhood, burough or district.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Optional

-   `owner` : Bike hire docking station's owner.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Optional

-   `provider` : Bike hire service provider.

    -   Normative references:
        [https://schema.org/provider](https://schema.org/provider)
    -   Optional

-   `contactPoint` : Bike hire service contact point.
    -   Normative references:
        [https://schema.org/contactPoint](https://schema.org/contactPoint)
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use 1 (Normalized Format)

```json
{
    "id": "Bcn-BikeHireDockingStation-1",
    "type": "BikeHireDockingStation",
    "status": {
        "value": "working"
    },
    "availableBikeNumber": {
        "value": 20,
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2018-09-25T12:00:00"
            }
        }
    },
    "freeSlotNumber": {
        "value": 10
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [2.180042, 41.397952]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressCountry": "ES",
            "addressLocality": "Barcelona",
            "streetAddress": "Gran Via Corts Catalanes,760"
        }
    }
}
```

## Examples of use 2 (?options=keyValues simplified representation for data consumers)

Bike hire docking station real time data in Malaga

    {
       "id": "malaga-bici-7"
       "type": "BikeHireDockingStation",
       "name": "07-Diputacion",
       "location": {
    	 "coordinates": [-4.43573, 36.699694],
    	  "type": "Point"
       },
       "availableBikeNumber": 18,
       "freeSlotNumber": 10,
       "address": {
    	  "streetAddress": "Paseo Antonio Banderas (Diputación)",
    	  "addressLocality": "Malaga",
    	  "addressCountry": "España"
       },
       "description": "Punto de alquiler de bicicletas próximo a Diputación",
       "dateModified": "2017-05-09T09:25:55.00Z"
    }

## Use it with a real service

T.B.D.

## Open Issues

Municipalities do not have a specific tariff or access requirements per station.
Therefore, this information has not been specified in this model so far.
