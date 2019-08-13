# Parking Group

**Note: The latest version of this Data Model can be 
found at [https://github.com/smart-data-models/dataModel.Parking](https://github.com/smart-data-models/dataModel.Parking)**

## Description

A group of parking spots. Granularity level can vary. It can be an storey on a
parking garage, an specific zone belonging to a big parking lot, or just a group
of spots intended for parking a certain vehicle type or subject to certain
restrictions (disabled, residents, ...). For the sake of simplicity only one
vehicle type per parking group is allowed. Similarly, one required permit is
only allowed per group type.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `ParkingGroup`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `category` : Parking Group's category.

    -   Attribute type: Property. List of [Text](http://schema.org/Text)
    -   Allowed values:
        -   `onstreet` if the parking group belongs to an `OnStreetParking`.
        -   `offstreet` if the parking group belongs to an `OffStreetParking`.
        -   (`adjacentSpaces`, `nonAdjacentSpaces`, `completeFloor`,
            `statisticsOnly`, `vehicleTypeSpaces`, `particularConditionsSpaces`)
        -   (`onlyDisabled`, `onlyResidents`, `onlyWithPermit`,
            `onlyELectricalCharging`)
        -   (`free`, `feeCharged`)
        -   (`blueZone`, `greenZone`, `loadUnloadZone`)
        -   (`shortTerm`, `mediumTerm`, `longTerm`)
        -   Any value not covered by the above enumeration and meaningful for
            the application.
    -   Mandatory

-   `refParkingSite` : Parking site to which this zone belongs to. A group
    cannot be orphan. A group cannot have subgroups.

    -   Attribute type: Relationship. Reference to an
        [OffStreetParking](../../OffStreetParking/doc/spec.md) or to an
        [OnStreetParking](../../OnStreetParking/doc/spec.md) entity.
    -   Mandatory

-   `allowedVehicleType` : Vehicle type allowed (a parking group only allows one
    vehicle type).

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Allowed Values: The following values defined by _VehicleTypeEnum_
        [DATEX 2 version 2.3](http://d2docs.ndwcloud.nu/downloads/modelv23.html)
        :
        -   (`agriculturalVehicle`, `bicycle`, `bus`, `car`, `caravan`,
            `carWithCaravan`, `carWithTrailer`,
            `constructionOrMaintenanceVehicle`, `lorry`, `moped`, `motorcycle`,
            `motorcycleWithSideCar`, `motorscooter`, `tanker`, `trailer`, `van`,
            `anyVehicle`)
    -   Mandatory

-   `location` : Geolocation of the parking group represented by a GeoJSON
    (Multi)Polygon or Point.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Optional

-   `address` : Registered parking group civic address.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Optional

-   `name` : Name given to the parking group.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Optional

-   `description` : Description about the parking group.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `maximumParkingDuration` : Maximum allowed stay encoded as a ISO8601
    duration. When non present or equals to the empty string it means
    indefinite. Applications _SHOULD_ inspect the value of this property at
    parent's level if it is not defined.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Optional

-   `chargeType` : Type of charge performed when parking on any of the spots
    pertaining to this group.

    -   Attribute type: Property. List of [Text](http://schema.org/Text)
    -   Allowed values: Some of those defined by the DATEX II version 2.3
        _ChargeTypeEnum_ enumeration:
        -   (`flat`, `minimum`, `maximum`, `additionalIntervalPrice`
            `seasonTicket` `temporaryPrice` `firstIntervalPrice`,
            `annualPayment`, `monthlyPayment`, `free`, `other`)
        -   Any other application-specific
    -   Mandatory

-   `requiredPermit` : This attribute captures what permit is needed to park in
    any of the spots of this group. For the sake of simplicity only one permit
    can be associated to a parking group. When a permit is composed by more than
    one item they can be combined by separating them with a ",". For instance
    "residentPermit,disabledPermit" stays that both a resident and a disabled
    permit are needed to park. If empty string, no permit is needed.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Allowed values: The following, defined by the _PermitTypeEnum_
        enumeration of DATEX II version 2.3.
        -   oneOf (`employeePermit`, `studentPermit`, `fairPermit`,
            `governmentPermit`, `residentPermit`,
            `specificIdentifiedVehiclePermit`, `disabledPermit`,
            `visitorPermit`, `blueZonePermit`, `careTakingPermit`,
            `carpoolingPermit`, `carSharingPermit`, `emergencyVehiclePermit`,
            `maintenanceVehiclePermit`, `roadWorksPermit`, `taxiPermit`,
            `transportationPermit`, `noPermitNeeded`)
        -   Any other application-specific
    -   Mandatory

-   `permitActiveHours` : This attribute allows to capture situations when a
    permit is only needed at specific hours or days of week. It is an structured
    value which must contain a subproperty per each required permit, indicating
    when the permit is active. If nothing specified for a permit it will mean
    that a permit is always required. Empty object means always active. The
    syntax must be conformant with schema.org
    [opening hours specification](https://schema.org/openingHours). For
    instance, a blue zone which is only active on dayweeks will be encoded as
    "blueZonePermit": "Mo,Tu,We,Th,Fr,Sa 09:00-20:00". Applications _SHOULD_
    inspect the value of this property at parent's level if it is not defined.

    -   Attribute type: Property. [StructuredValue](http://schema.org/StructuredValue)
    -   Mandatory.

-   `reservationType` : Conditions for reservation. Applications _SHOULD_
    inspect the value of this property at parent's level if it is not defined.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Allowed values: The following specified by _ReservationTypeEnum_ of
        DATEX II version 2.3:
        -   one Of (`optional`, `mandatory`, `notAvailable`, `partly`).
    -   Optional

-   `areBordersMarked` : Denotes whether parking spots are delimited (with blank
    lines or similar) or not. Applications _SHOULD_ inspect the value of this
    property at parent's level if it is not defined.

    -   Attribute type: Property. [Boolean](https://schema.org/Boolean)
    -   Optional

-   `totalSpotNumber` : The total number of spots pertaining to this group.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: Any positive integer number or 0.
    -   Normative references: DATEX 2 version 2.3 attribute
        _parkingNumberOfSpaces_ of the _ParkingRecord_ class.
    -   Optional

-   `availableSpotNumber` : The number of spots available in this group.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: A positive integer number, including 0. It must lower or
        equal than `totalSpotNumber`.
    -   Metadata:
        -   `timestamp` : Timestamp of the last attribute update
        -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `occupancyDetectionType` : Occupancy detection method.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Allowed values: The following from DATEX II version 2.3
        _OccupancyDetectionTypeEnum_:
        -   (`none`, `balancing`, `singleSpaceDetection`, `modelBased`,
            `manual`)
        -   Or any other application-specific
    -   Mandatory

-   `parkingMode` : Parking mode(s). Applications _SHOULD_ inspect the value of
    this property at parent's level if it is not defined.

    -   Attribute type: Property. List of [Text](http://schema.org/Text)
    -   Allowed values: Those defined by the DATEX II version 2.3
        _ParkingModeEnum_ enumeration:
        -   (`perpendicularParking`, `parallelParking`, `echelonParking`)
    -   Optional

-   `averageSpotWidth` : The average width of parking spots. Applications
    _SHOULD_ inspect the value of this property at parent's level if it is not
    defined.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `averageSpotLength` : The average length of parking spots. Applications
    _SHOULD_ inspect the value of this property at parent's level if it is not
    defined.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `maximumAllowedHeight` : Maximum allowed height for vehicles. Applications
    _SHOULD_ inspect the value of this property at parent's level if it is not
    defined.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `maximumAllowedWidth` : Maximum allowed width for vehicles. Applications
    _SHOULD_ inspect the value of this property at parent's level if it is not
    defined.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `image` : A URL containing a photo of this parking group.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `refParkingSpot` : Parking spots belonging to this group.
    -   Attribute type: Property. List of references to
        [ParkingSpot](../../ParkingSpot/doc/spec.md)
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "daoiz-velarde-1-5-disabled",
    "type": "ParkingGroup",
    "category": {
        "value": ["onstreet", "adjacentSpaces", "onlyDisabled"]
    },
    "refParkingSite": {
        "type": "Relationship",
        "value": "daoiz-velarde-1-5"
    },
    "permitActiveHours": {
        "value": ""
    },
    "requiredPermit": {
        "value": "disabledPermit"
    },
    "allowedVehicleType": {
        "value": "car"
    },
    "availableSpotNumber": {
        "value": 1,
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2018-09-12T12:00:00"
            }
        }
    },
    "totalSpotNumber": {
        "value": 2
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-3.80356167695194, 43.46296641666926],
                    [-3.803161973253841, 43.46301091092682],
                    [-3.803147082548618, 43.462879859445884],
                    [-3.803536474744068, 43.462838666196674],
                    [-3.80356167695194, 43.46296641666926]
                ]
            ]
        }
    },
    "chargeType": {
        "value": ["free"]
    },
    "description": {
        "value": "Two parking spots reserved for disabled people"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

A group of parking spots especially for disabled people.

```json
{
    "id": "daoiz-velarde-1-5-disabled",
    "type": "ParkingGroup",
    "category": ["onstreet", "adjacentSpaces", "onlyDisabled"],
    "allowedVehicleType": "car",
    "chargeType": ["free"],
    "refParkingSite": "daoiz-velarde-1-5",
    "description": "Two parking spots reserved for disabled people",
    "totalSpotNumber": 2,
    "availableSpotNumber": 1,
    "location": {
        "type": "Polygon",
        "coordinates": [
            [
                [-3.80356167695194, 43.46296641666926],
                [-3.803161973253841, 43.46301091092682],
                [-3.803147082548618, 43.462879859445884],
                [-3.803536474744068, 43.462838666196674],
                [-3.80356167695194, 43.46296641666926]
            ]
        ]
    },
    "requiredPermit": "disabledPermit",
    "permitActiveHours": "" /* Always permit is needed */
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:ParkingGroup:daoiz-velarde-1-5-disabled",
    "type": "ParkingGroup",
    "category": {
        "type": "Property",
        "value": ["onstreet", "adjacentSpaces", "onlyDisabled"]
    },
    "refParkingSite": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:ParkingSite:daoiz-velarde-1-5"
    },
    "permitActiveHours": {
        "type": "Property",
        "value": ""
    },
    "requiredPermit": {
        "type": "Property",
        "value": "disabledPermit"
    },
    "allowedVehicleType": {
        "type": "Property",
        "value": "car"
    },
    "availableSpotNumber": {
        "type": "Property",
        "value": 1,
        "observedAt": "2018-09-12T12:00:00Z"
    },
    "totalSpotNumber": {
        "type": "Property",
        "value": 2
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-3.80356167695194, 43.46296641666926],
                    [-3.803161973253841, 43.46301091092682],
                    [-3.803147082548618, 43.462879859445884],
                    [-3.803536474744068, 43.462838666196674],
                    [-3.80356167695194, 43.46296641666926]
                ]
            ]
        }
    },
    "chargeType": {
        "type": "Property",
        "value": ["free"]
    },
    "description": {
        "type": "Property",
        "value": "Two parking spots reserved for disabled people"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

A group of parking spots especially for loading and unloading goods. From 10:00
to 14:00, Monday-Saturday.

```json
{
    "id": "daoiz-velarde-23-load",
    "type": "ParkingGroup",
    "category": ["onstreet", "adjacentSpaces", "loadUnloadZone"],
    "allowedVehicleType": "car,van,lorry",
    "chargeType": ["free"],
    "refParkingSite": "daoiz-velarde-23",
    "description": "Three parking spots reserved for load and unload",
    "totalSpotNumber": 3,
    "availableSpotNumber": 2,
    "location": {
        "type": "Polygon",
        "coordinates": [
            [
                [-3.80356167695194, 43.46296641666926 ],
                [-3.803161973253841,43.46301091092682 ],
                [-3.803147082548618,43.462879859445884],
                [-3.803536474744068,43.462838666196674],
                [-3.80356167695194, 43.46296641666926]
            ]
        ]
    },
    "requiredPermit": "transportPermit",
    "permitActiveHours": {
        "transportPermit": “Mo, Tu, We, Th, Fr, Sa 10:00-14:00"
    }
}
```

## Test it with a real service

## Open issues
