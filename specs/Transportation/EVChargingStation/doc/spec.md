# Electric Vehicle Charging Station

## Description

A public charging station supplying energy to electrical vehicles. The charge
time depends on the maximum power output of the station, the number of vehicles
currently charging and the current battery level.

## Data Model

A JSON Schema corresponding to this data model can be found
[here](https://fiware.github.io/dataModels/specs/Transportation/EVChargingStation/schema.json).

-   `id` : Unique identifier. It shall be a URN in the form
    `urn:ngsi-ld:EVChargingStation:<identifier>` where `<identifier>` shall be a
    unique ID string.

-   `type` : Entity type. It must be equal to `EVChargingStation`.

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Normative References:
        [http://schema.org/DateTime](http://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Normative References:
        [http://schema.org/DateTime](http://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `location` : Geolocation of the charging station represented by a GeoJSON
    (Multi)Polygon or Point.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Registered charging station site civic address.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not defined.

-   `name` : Name given to the charging station.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `description` : Description of this charging station.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `image` : A URL containing a photo of this charging station.

    -   Attribute type: Property. [image (URL)](http://schema.org/URL)
    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `capacity` : The total number of vehicles which can be charged at the same
    time. The total number of sockets can be higher.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: Any positive integer number.
    -   Mandatory

-   `allowedVehicleType` : Vehicle type(s) which can be charged.
    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed Values: ( `bicycle`, `bus`, `car`, `caravan`, `motorcycle`,
        `motorscooter`, `truck`)
    -   Mandatory
-   `socketType` : The type of sockets offered by this station.

    -   Attribute type: Property. List of [Text](http://schema.org/Text)
    -   Allowed values: (`Type2`, `CHAdeMO`, `CCS/SAE`, `Type3`, `Tesla`,
        `J-1772`, `Wall_Euro`, `Caravan_Mains_Socket`, `Dual_J-1772`,
        `Dual_CHAdeMO`, `Mennekes`, `Dual_Mennekes`, `Other`)
    -   Mandatory

-   `socketNumber` : The total number of sockets offered by this charging
    station.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: Any positive integer number.
    -   Optional

-   `availableCapacity` : The number of vehicles which currently can be charged.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: A positive integer number, including 0. It must lower or
        equal than `capacity`.
    -   Metadata:
        -   `timestamp`: Timestamp corresponding to the last attribute value.
            (`observeAt` in NGSI-LD) - Type:
            [DateTime](https://schema.org/DateTime)
    -   Optional

-   `amperage` : The total amperage offered by the charging station.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: Any positive number.
    -   Default Unit: Ampers (A)
    -   Optional

-   `voltage` : The total voltage offered by the charging station.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: Any positive number.
    -   Default Unit: Volts (V)
    -   Optional

-   `openingHours` : Opening hours of the charging station.

    -   Normative references:
        [http://schema.org/openingHours](http://schema.org/openingHours)
    -   Optional

-   `status` : Status of the charging station.

    -   Attribute type: Property. List of [Text](http://schema.org/Text)
    -   Allowed values:
        -   (`working`, `outOfService`, `withIncidence`, `full`, `almostFull`,
            `empty`, `almostEmpty`)
        -   Or any other application-specific.
    -   Metadata:
        -   `timestamp` : Timestamp corresponding to the last attribute value.
            (`observedAt` in NGSI-LD) - Type:
            [DateTime](https://schema.org/DateTime)
    -   Optional

-   `areaServed` : Area served by this charging station. Precise semantics can
    depend on the application or target city. For instance, it can be a
    neighbourhood, burough or district.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Optional

-   `owner` : Charging station's owner.

    -   Attribute type: Property. [Text](http://schema.org/Text) or
        [URL](http://schema.org/URL)
    -   Optional

-   `operator` : Charging station's operator.

    -   Attribute Type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `network` : The name of the Network, with that the operator cooperates.

    -   Attribute Type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `contactPoint` : Charging station contact point.

    -   Normative references:
        [https://schema.org/contactPoint](https://schema.org/contactPoint)
    -   Optional

-   `chargeType` : Type(s) of charge when using this station.

    -   Attribute type: Property. List of [Text](http://schema.org/Text)
    -   Allowed values: (`flat`, `annualPayment`, `monthlyPayment`, `free`,
        `other`)
        -   Any other application-specific
    -   Optional

-   `acceptedPaymentMethod` : Accepted payment method(s).
    -   Normative references: https://schema.org/acceptedPaymentMethod
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:EVChargingStation:ValladolI+D_Covaresa",
    "type": "EVChargingStation",
    "socketType": {
        "value": ["Wall_Euro"]
    },
    "capacity": {
        "value": 2
    },
    "name": {
        "value": "Agencia de Innovaci\u00f3n"
    },
    "allowedVehicleType": {
        "value": ["car"]
    },
    "source": {
        "value": "https://openchargemap.org/"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-4.747901, 41.618265]
        }
    },
    "chargeType": {
        "value": ["free"]
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Valladolid",
            "addressCountry": "Espa\u00f1a",
            "streetAddress": "Paseo de Zorrilla, 191"
        }
    },
    "operator": {
        "value": "Iberdrola"
    },
    "contactPoint": {
        "value": {
            "email": "vehiculoelectrico@ava.es"
        }
    }
}
```

## Examples of use 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:EVChargingStation:ValladolI+D_Covaresa",
    "type": "EVChargingStation",
    "name": "Agencia de Innovación",
    "location": {
        "coordinates": [-4.747901, 41.618265],
        "type": "Point"
    },
    "capacity": 2,
    "socketType": ["Wall_Euro"],
    "address": {
        "streetAddress": "Paseo de Zorrilla, 191",
        "addressLocality": "Valladolid",
        "addressCountry": "España"
    },
    "contactPoint": {
        "email": "vehiculoelectrico@ava.es"
    },
    "operator": "Iberdrola",
    "allowedVehicleType": ["car"],
    "chargeType": ["free"],
    "source": "https://openchargemap.org/"
}
```

## Use it with a real service

T.B.D.

## Open Issues

## See also

-   https://openchargemap.org/
-   https://wiki.openstreetmap.org/wiki/Tag:amenity=charging_station
-   https://www.plugshare.com/
