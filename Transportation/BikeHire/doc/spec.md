Bike Hire Docking Station
=========================

Description
-----------

A bike hire docking station where subscribed users can hire and return a bike.
It provides data about its main features and availability of bikes and slots.

 

Data Model
----------

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `BikeHireDockingStation`.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)

    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)

    -   Optional

-   `location` : Geolocation of the station represented by a GeoJSON
    (Multi)Polygon or Point.

    -   Attribute type: `geo:json`.

    -   Normative References: <https://tools.ietf.org/html/rfc7946>

    -   Mandatory if `address` is not defined.

-   `address` : Registered docking station site civic address.

    -   Normative References: <https://schema.org/address>

    -   Mandatory if `location` is not defined.

-   `name` : Name given to the docking station.

    -   Normative References: <https://schema.org/name>

    -   Mandatory

-   `description` : Description about the bike hire docking station.

    -   Normative References: <https://schema.org/description>

    -   Optional

-   `image` : A URL containing a photo of this docking station.

    -   Normative References: <https://schema.org/image>

    -   Optional

-   `totalSlotNumber` : The total number of slots offered by this bike docking
    station.

    -   Attribute type: [Number](http://schema.org/Number)

    -   Allowed values: Any positive integer number or 0.

    -   Optional

-   `freeSlotNumber` : The number of slots available for returning and parking
    bikes.

    -   Attribute type: [Number](http://schema.org/Number)

    -   Allowed values: A positive integer number, including 0. It must lower or
        equal than `totalSpotNumber`.

    -   Metadata:

        -   `timestamp` : Timestamp of the last attribute update.

        -   Type: [DateTime](https://schema.org/DateTime)

    -   Optional

-   `outOfServiceSlotNumber` : The number of slots that are out of order and
    cannot be used to hire or park a bike.

    -   Attribute type: [Number](http://schema.org/Number)

    -   Allowed values: A positive integer number, including 0.

    -   Metadata:

        -   `timestamp` : Timestamp of the last attribute update

        -   Type: [DateTime](https://schema.org/DateTime)

    -   Optional

-   `availableBikeNumber` : The number of bikes available in the bike hire
    docking station to be hired by users.

    -   Attribute type: [Number](http://schema.org/Number)

    -   Allowed values: A positive integer number, including 0.

    -   Metadata:

        -   `timestamp` : Timestamp of the last attribute update.

        -   Type: [DateTime](https://schema.org/DateTime)

    -   Optional

-   `openingHours` : Opening hours of the docking station, if it is not 24h
    opened.

    -   Normative references: <http://schema.org/openingHours>

    -   Optional

-   `status` : Status of the bike hire docking station.

    -   Attribute type: List of [Text](http://schema.org/Text)

    -   Metadata:

        -   `timestamp` : Timestamp of the last attribute update.

        -   Type: [DateTime](https://schema.org/DateTime)

    -   Allowed values:

        -   (`operative`, `outOfService`, `withIncidence`, `full`, `almostFull`)

        -   Or any other application-specific.

    -   Optional

-   `owner` : Bike hire docking station's owner.

    -   Attribute type: [Text](http://schema.org/Text)

    -   Optional

-   `provider` : Bike hire service provider.

    -   Normative references: <https://schema.org/provider>

    -   Optional

-   `contactPoint` : Bike hire service contact point.

    -   Normative references: <https://schema.org/contactPoint>

    -   Optional

 

Examples of use
---------------

Bike hire docking station real time data in Malaga

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

 
-
