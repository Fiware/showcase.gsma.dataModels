# Vehicle

## Description

A vehicle.

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier.

-   `type` : Entity type. It must be equal to `Vehicle`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `name` : Name given to this vehicle

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Optional

    -   Attribute type: Text or URL
    -   Optional

-   `description` : Vehicle description.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `vehicleType` : Type of vehicle from the point of view of its structural
    characteristics. This is different than the vehicle category (see below).

    -   Attribute type: [Text](https://schema.org/Text)
    -   Allowed Values: The following values defined by _VehicleTypeEnum_ and
        _VehicleTypeEnum2_,
        [DATEX 2 version 2.3](http://d2docs.ndwcloud.nu/_static/umlmodel/v2.3/index.htm):
        -   (`agriculturalVehicle`, `bicycle`, `bus`, `minibus`, `car`,
            `caravan`, `tram`, `tanker`, `carWithCaravan`, `carWithTrailer`,
            `lorry`, `moped`, `tanker`, `motorcycle`, `motorcycleWithSideCar`,
            `motorscooter`, `trailer`, `van`, `caravan`,
            `constructionOrMaintenanceVehicle`)
        -   (`trolley`, `binTrolley`, `sweepingMachine`, `cleaningTrolley`)
    -   Mandatory

-   `category` : Vehicle category(ies) from an external point of view. This is
    different than the vehicle type (car, lorry, etc.) represented by the
    `vehicleType` property.

    -   Attribute type: List of [Text](https:/schema.org/Text)
    -   Allowed values:
        -   (`public`, `private`, `municipalServices`, `specialUsage`).
        -   (`tracked`, `nonTracked`). Tracked vehicles are those vehicles which
            position is permanently tracked by a remote system.
        -   Or any other needed by an application They incorporate a GPS
            receiver together with a network connection to periodically update a
            reported position (location, speed, heading ...).
    -   Mandatory

-   `location` : Vehicle's last known location represented by a GeoJSON Point.
    Such point may contain the vehicle's _altitude_ as the third component of
    the `coordinates` array.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Attribute metadata:
        -   `timestamp`: Timestamp which captures when the vehicle was at that
            location. This value can also appear as a FIWARE
            [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/master/README.md#the-timeinstant-element)
        -   Type: [DateTime](http://schema.org/DateTime) or `ISO8601` (legacy).
        -   Mandatory
    -   Mandatory only if `category` contains `tracked`.

-   `previousLocation` : Vehicle's previous location represented by a GeoJSON
    Point. Such point may contain the previous vehicle's _altitude_ as the third
    component of the`coordinates` array.

    -   Attribute type: `geo:json`.
    -   Normative References:
    -   Attribute metadata:
        -   `timestamp`: Timestamp which captures when the vehicle was at that
            location.
        -   Type: [DateTime](http://schema.org/DateTime)
        -   Mandatory
    -   Optional

-   `speed` : Denotes the magnitude of the horizontal component of the vehicle's
    current velocity and is specified in Kilometers per Hour. If provided, the
    value of the speed attribute must be a non-negative real number. `null`
    _MAY_ be used if `speed` is transiently unknown for some reason.

    -   Attribute type: [Number](https:/schema.org/Number)
    -   Default unit: Kilometers per hour
    -   Attribute metadata:
        -   `timestamp` : Timestamp which captures when the vehicle was moving
            at that speed. This value can also appear as a FIWARE
            [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/master/README.md#the-timeinstant-element)
        -   Type: [DateTime](http://schema.org/DateTime) or `ISO8601` (legacy).
        -   Mandatory
    -   Mandatory only if `category` contains `tracked`.

-   `heading` : Denotes the direction of travel of the vehicle and is specified
    in decimal degrees, where 0° ≤ `heading` < 360°, counting clockwise relative
    to the true north. If the vehicle is stationary (i.e. the value of the
    `speed` attribute is `0`), then the value of the heading attribute must be
    equal to `null`. `null` _MAY_ be used if `heading` is transiently unknown
    for some reason.

    -   Attribute type: [Number](https://schema.org)
    -   Attribute metadata:
        -   `timestamp` : Timestamp which captures when the vehicle was heading
            towards such direction. This value can also appear as a FIWARE
            [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/master/README.md#the-timeinstant-element)
        -   Type: [DateTime](http://schema.org/DateTime) or `ISO8601` (legacy).
        -   Mandatory
    -   Mandatory only if `category` contains `tracked`.

-   `cargoWeight` : Current weight of the vehicle's cargo.

    -   Attribute type: [Number](https:/schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp associated to this measurement. This value
            can also appear as a FIWARE
            [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/master/README.md#the-timeinstant-element)
            -   Type: [DateTime](http://schema.org/DateTime) or `ISO8601`
                (legacy).
            -   Mandatory
    -   Default unit: Kilograms
    -   Optional

-   `vehicleIdentificationNumber` : The Vehicle Identification Number (VIN) is a
    unique serial number used by the automotive industry to identify individual
    motor vehicles.

    -   Normative References:
        [https://schema.org/vehicleIdentificationNumber](https://schema.org/vehicleIdentificationNumber)
    -   Mandatory if neither `vehiclePlateIdentifier` nor `fleetVehicleId` is
        defined.

-   `vehiclePlateIdentifier` : An identifier or code displayed on a vehicle
    registration plate attached to the vehicle used for official identification
    purposes. The registration identifier is numeric or alphanumeric and is
    unique within the issuing authority's region.

    -   Normative References: DATEXII `vehicleRegistrationPlateIdentifier`
    -   Attribute Type: [Text](https://schema.org/Text)
    -   Mandatory if neither `vehicleIdentificationNumber` nor `fleetVehicleId`
        is defined.

-   `fleetVehicleId` : The identifier of the vehicle in the context of the fleet
    of vehicles to which it belongs.

    -   Attribute Type: [Text](https://schema.org/Text)
    -   Mandatory if neither `vehiclePlateIdentifier` nor
        `vehicleIdentificationNumber` is defined.

-   `dateVehicleFirstRegistered` : The date of the first registration of the
    vehicle with the respective public authorities.

    -   Normative References:
        [https://schema.org/dateVehicleFirstRegistered](https://schema.org/dateVehicleFirstRegistered)
    -   Optional

-   `dateFirstUsed` : Timestamp which denotes when the vehicle was first used.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `purchaseDate` : The date the item e.g. vehicle was purchased by the current
    owner.

    -   Normative References:
        [https://schema.org/purchaseDate](https://schema.org/purchaseDate)
    -   Optional

-   `mileageFromOdometer` : The total distance travelled by the particular
    vehicle since its initial production, as read from its odometer.

    -   Normative References:
        [https://schema.org/mileageFromOdometer](https://schema.org/mileageFromOdometer)
    -   Attribute metadata:
        -   `timestamp`: Timestamp associated to this measurement. This value
            can also appear as a FIWARE
            [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/master/README.md#the-timeinstant-element)
            -   Type: [DateTime](http://schema.org/DateTime) or `ISO8601`
                (legacy).
            -   Mandatory
    -   Optional

-   `vehicleConfiguration` : A short text indicating the configuration of the
    vehicle, e.g. '5dr hatchback ST 2.5 MT 225 hp' or 'limited edition'.

    -   Normative References:
        [https://schema.org/vehicleConfiguration](https://schema.org/vehicleConfiguration)
    -   Optional

-   `color` : Vehicle's color.

    -   Normative References:
        [https://schema.org/color](https://schema.org/color)
    -   Optional

-   `owner` : Vehicle's owner.

    -   Attribute Type: [https://schema.org/Person](https://schema.org/Person)
        or [https://schema.org/Organization](https://schema.org/Organization)
    -   Optional

-   `feature` : Feature(s) incorporated by the vehicle.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (`gps`, `airbag`, `overspeed`, `abs`, `wifi`,
        `backCamera`, `proximitySensor`, `disabledRamp`, `alarm`,
        `internetConnection`) or any other needed by the application.
        -   In order to represent multiple instances of a feature it can be used
            the following syntax: `"<feature>,<occurences>"`. For example, a car
            with 4 airbags will be represented by `"airbag,4"`.
    -   Optional

-   `serviceProvided` : Service(s) the vehicle is capable of providing or it is
    assigned to.

    -   Attribute type: List of [Text](https:/schema.org/Text)
    -   Allowed values: (`garbageCollection`, `parksAndGardens`, `construction`,
        `streetLighting`, `roadSignalling`, `cargoTransport`, `urbanTransit`,
        `maintenance`, `streetCleaning`, `wasteContainerCleaning`,
        `auxiliaryServices` `goodsSelling`, `fairground`, `specialTransport`) or
        any other value needed by an specific application.
    -   Optional

-   `vehicleSpecialUsage` : Indicates whether the vehicle is been used for
    special purposes, like commercial rental, driving school, or as a taxi. The
    legislation in many countries requires this information to be revealed when
    offering a car for sale.

    -   Normative References:
        [https://auto.schema.org/vehicleSpecialUsage](https://auto.schema.org/vehicleSpecialUsage)
    -   Allowed values: (`taxi`, `ambulance`, `police`, `fireBrigade`,
        `schoolTransportation`, `military`)
    -   Optional

-   `refVehicleModel` : Vehicle's model.

    -   Attribute type: Reference to a
        [VehicleModel](../../VehicleModel/doc/spec.md) entity.
    -   Optional

-   `areaServed` : Higher level area served by this vehicle. It can be used to
    group vehicles per responsible, district, neighbourhood, etc.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Optional

-   `serviceStatus` : Vehicle status (from the point of view of the service
    provided, so it could not apply to private vehicles).

    -   Allowed values:
        -   `parked` : Vehicle is parked and not providing any service at the
            moment.
        -   `onRoute` : Vehicle is performing a mission. A comma-separated
            modifier(s) can be added to indicate what mission is currently
            delivering the vehicle. For instance `"onRoute,garbageCollection"`
            can be used to denote that the vehicle is on route and in a garbage
            collection mission.
        -   `broken` : Vehicle is suffering a temporary breakdown.
        -   `outOfService` : Vehicle is on the road but not performing any
            mission, probably going to its parking area.
    -   Attribute type: [Text](https://schema.org/Text)
    -   Attribute metadata:
        -   `timestamp` : Timestamp which reflects when the referred service
            status was captured.
            -   Type: [DateTime](https://schema.org/DateTime)
            -   Mandatory
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Creation timestamp of this entity.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "vehicle:WasteManagement:1",
    "type": "Vehicle",
    "category": {
        "value": ["municipalServices"]
    },
    "vehicleType": {
        "value": "lorry"
    },
    "name": {
        "value": "C Recogida 1"
    },
    "vehiclePlateIdentifier": {
        "value": "3456ABC"
    },
    "refVehicleModel": {
        "type": "Relationship",
        "value": "vehiclemodel:econic"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.164485591715449, 40.62785133667262]
        },
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2018-09-27T12:00:00"
            }
        }
    },
    "areaServed": {
        "value": "Centro"
    },
    "serviceStatus": {
        "value": "onRoute"
    },
    "cargoWeight": {
        "value": 314
    },
    "speed": {
        "value": 50,
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2018-09-27T12:00:00"
            }
        }
    },
    "serviceProvided": {
        "value": ["garbageCollection", "wasteContainerCleaning"]
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "vehicle:WasteManagement:1",
    "type": "Vehicle",
    "vehicleType": "lorry",
    "category": ["municipalServices"],
    "location": {
        "type": "Point",
        "coordinates": [-3.164485591715449, 40.62785133667262]
    },
    "name": "C Recogida 1",
    "speed": 50,
    "cargoWeight": 314,
    "serviceStatus": "onRoute",
    "serviceProvided": ["garbageCollection", "wasteContainerCleaning"],
    "areaServed": "Centro",
    "refVehicleModel": "vehiclemodel:econic",
    "vehiclePlateIdentifier": "3456ABC"
}
```

## Test it with a real service

T.B.D.

## Issues

-   Taxonomy of service types
-   Vehicle special usage categories as defined by different countries have not
    been clarified
