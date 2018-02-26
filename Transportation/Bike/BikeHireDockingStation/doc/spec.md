# Bike Hire Docking Station

## Description

Many cities provide a bike hiring system for citizens. These can hire a bike base on different types of subscriptions. A bike hire docking station where subscribed users can hire and return a bike. It provides data about its main
features and availability of bikes and free slots.

## Data Model


A JSON Schema corresponding to this data model can be found [here](http://fiware.github.io/dataModels/Transportation/BikeHire/schema.json).

+   `id` : Unique identifier.

+   `type` : Entity type. It must be equal to `BikeHireDockingStation`.

+   `dateCreated` : Entity's creation timestamp.
    +   Attribute type: [DateTime](https://schema.org/DateTime)
    +   Normative References:
        [http://schema.org/DateTime](http://schema.org/DateTime)[
        ](http://schema.org/DateTime)
    +   Optional

+   `dateModified` : Last update timestamp of this entity.
    +   Attribute type: [DateTime](https://schema.org/DateTime)
    +   Normative References:
        [http://schema.org/DateTime](http://schema.org/DateTime)[
        ](http://schema.org/DateTime)
    +   Optional

+   `location` : Geolocation of the station represented by a GeoJSON
    (Multi)Polygon or Point.
    +   Attribute type: `geo:json`.
    +   Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    +   Mandatory if `address` is not defined.

+   `address` : Registered docking station site civic address.
    +   Normative References: [https://schema.org/address](https://schema.org/address)
    +   Mandatory if `location` is not defined.

+   `name` : Name given to the docking station.
    +   Attribute type: [Text](http://schema.org/Number)
    +   Normative References: [https://schema.org/name](https://schema.org/name)
    +   Mandatory

+   `description` : Description about the bike hire docking station.
    +   Attribute type: [Text](http://schema.org/Number)
    +   Normative References: [https://schema.org/description](https://schema.org/description)
    +   Optional

+   `image` : A URL containing a photo of this docking station.
    +   Attribute type: [image (URL)](http://schema.org/Number)
    +   Normative References: [https://schema.org/image](https://schema.org/image)
    +   Optional

+   `totalSlotNumber` : The total number of slots offered by this bike docking
    station.
    +   Attribute type: [Number](http://schema.org/Number)
    +   Allowed values: Any positive integer number or 0.
    +   Optional

+   `freeSlotNumber` : The number of slots available for returning and parking
    bikes. It must lower or equal than `totalSlotNumber`.
    +   Attribute type: [Number](http://schema.org/Number)
    +   Allowed values: A positive integer number, including 0. It must lower or
        equal than `totalSlotNumber`.
    +   Metadata:
        +   `timestamp` : Timestamp of the last attribute update.
        +   Type: [DateTime](https://schema.org/DateTime)
    +   Optional

+   `outOfServiceSlotNumber` : The number of slots that are out of order and
    cannot be used to hire or park a bike. It must lower or equal than
    `totalSlotNumber`.
    +   Attribute type: [Number](http://schema.org/Number)
    +   Allowed values: A positive integer number, including 0.
    +   Metadata:
        +   `timestamp` : Timestamp of the last attribute update
        +   Type: [DateTime](https://schema.org/DateTime)
    +   Optional

+   `availableBikeNumber` : The number of bikes available in the bike hire
    docking station to be hired by users.
    +   Attribute type: [Number](http://schema.org/Number)
    +   Allowed values: A positive integer number, including 0.
    +   Metadata:
        +   `timestamp` : Timestamp of the last attribute update.
        +   Type: [DateTime](https://schema.org/DateTime)
    +   Optional

+   `openingHours` : Opening hours of the docking station.
    +   Normative references: [http://schema.org/openingHours](http://schema.org/openingHours)
    +   Optional

+   `status` : Status of the bike hire docking station.
    +   Attribute type: List of [Text](http://schema.org/Text)
    +   Metadata:
        +   `timestamp` : Timestamp of the last attribute update.
        +   Type: [DateTime](https://schema.org/DateTime)
    +   Allowed values:
        +   (`working`, `outOfService`, `withIncidence`, `full`, `almostFull`)
        +   Or any other application+specific.
    +   Optional

+   `areaServed` : Area served by this docking station. Precise semantics can
    depend on the application or target city. For instance, it can be a
    neighbourhood, burough or district.
    +   Attribute type: [Text](http://schema.org/Text)
    +   Optional

+   `owner` : Bike hire docking station's owner.
    +   Attribute type: [Text](http://schema.org/Text)
    +   Optional

+   `provider` : Bike hire service provider.
    +   Normative references: [https://schema.org/provider](https://schema.org/provider)
    +   Optional

+   `contactPoint` : Bike hire service contact point.
    +   Normative references: [https://schema.org/contactPoint](https://schema.org/contactPoint)
    +   Optional

## Examples of use

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

Ongoing implementation in Cedus project for Rennes and Málaga. Expected by 2017Q2.

## Open Issues

Municipalities do not have a specific tariff or access requirements per station. Therefore, this information has not been specified in this model so far.
