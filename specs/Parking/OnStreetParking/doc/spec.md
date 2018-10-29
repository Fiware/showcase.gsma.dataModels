# On Street Parking

## Description

A site, open space zone, on street, (metered or not) with direct access from a
road, intended to park vehicles. In DATEX 2 version 2.3 terminology it
corresponds to a _UrbanParkingSite_ of type _onStreetParking_.

A data dictionary for DATEX II terms can be found at
[http://datexbrowser.tamtamresearch.com/](http://datexbrowser.tamtamresearch.com/).

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `OnStreetParking`.

-   `dateCreated` : Entity's creation timestamp

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `category` : Street parking category.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values:
        -   (`forDisabled`, `forResidents`, `forLoadUnload`, `onlyWithPermit`,
            `forELectricalCharging`)
        -   (`free`, `feeCharged`)
        -   (`blueZone`, `greenZone`)
        -   (`taxiStop`)
        -   (`shortTerm`, `mediumTerm`)
        -   Any value not covered by the above enumeration and meaningful for
            the application.
    -   Mandatory

-   `location` : Geolocation of the parking site represented by a GeoJSON
    (Multi)Polygon.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address`is not defined.

-   `address` : Registered onstreet parking civic address.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if location not defined

-   `name` : Name given to the onstreet parking zone.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `chargeType` : Type of charge(s) performed by the parking site.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: Some of those defined by the DATEX II version 2.3
        _ChargeTypeEnum_ enumeration:
        -   (`flat`, `minimum`, `maximum`, `additionalIntervalPrice`
            `seasonTicket` `temporaryPrice` `firstIntervalPrice`,
            `annualPayment`, `monthlyPayment`, `free`, `unknown`, `other`)
        -   Any other application-specific
    -   Mandatory

-   `requiredPermit` : This attribute captures what permit(s) might be needed to
    park at this site. Semantics is that at least _one of_ these permits is
    needed to park. When a permit is composed by more than one item (and) they
    can be combined with a ",". For instance "residentPermit,disabledPermit"
    stays that both, at the same time, a resident and a disabled permit are
    needed to park. If empty or `null`, no permit is needed. + Attribute type:
    List of [Text](http://schema.org/Text) + Allowed values: The following,
    defined by the _PermitTypeEnum_ enumeration of DATEX II version 2.3. + oneOf
    (`fairPermit`, `governmentPermit`, `residentPermit`, `disabledPermit`,
    `blueZonePermit`, `careTakingPermit`, `carpoolingPermit`,
    `carSharingPermit`, `emergencyVehiclePermit`, `maintenanceVehiclePermit`,
    `roadWorksPermit`, `taxiPermit`, `transportationPermit`, `noPermitNeeded`) +
    Any other application-specific + Mandatory. It can be `null`.

-   `permitActiveHours` : This attribute allows to capture situations when a
    permit is only needed at specific hours or days of week. It is an structured
    value which must contain a subproperty per each required permit, indicating
    when the permit is active. If nothing specified (or `null`) for a permit it
    will mean that a permit is always required. `null`or empty object means
    always active. The syntax must be conformant with schema.org (opening hours
    specification)[https://schema.org/openingHours]. For instance, a blue zone
    which is only active on dayweeks will be encoded as "blueZonePermit":
    "Mo,Tu,We,Th,Fr,Sa 09:00-20:00". + Attribute type:
    [StructuredValue](http://schema.org/StructuredValue) + Mandatory. It can be
    `null`.

-   `allowedVehicleType` : Vehicle type allowed (only one per on street
    parking).

    -   Attribute type: [Text](http://schema.org/Text)
    -   Allowed Values: The following values defined by _VehicleTypeEnum_
        [DATEX 2 version 2.3](http://www.datex2.eu/sites/www.datex2.eu/files/DATEXIISchema_2_2_2_1.zip)
        : + (`bicycle`, `bus`, `car`, `caravan`, `carWithCaravan`,
        `carWithTrailer`, `constructionOrMaintenanceVehicle`, `lorry`, `moped`,
        `motorcycle`, `motorcycleWithSideCar`, `motorscooter`, `tanker`,
        `trailer`, `van`, `anyVehicle`)
    -   Mandatory

-   `maximumParkingDuration` : Maximum allowed stay at site encoded as a ISO8601
    duration. A `null` or empty value indicates an indefinite duration. +
    Attribute type: [Text](http://schema.org/Text) + Optional

-   `usageScenario` : Usage scenario. Gives more details about the `category`
    attribute.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: Those defined by the enumeration
        _ParkingUsageScenarioEnum_ of DATEX II version 2.3:
        -   (`parkAndRide`, `parkAndCycle`, `parkAndWalk`, `kissAndRide`,
            `liftshare`, `carSharing`, `vehicleLift`, `loadingBay`, `dropOff`,
            `overnightParking`, `other`)
        -   Or any other value useful for the application and not covered above.
    -   Optional

-   `description` : Description about the onstreet parking zone.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `areBordersMarked` : Denotes whether parking spots are delimited (with blank
    lines or similar) or not.

    -   Attribute type: [Boolean](https://schema.org/Boolean)
    -   Optional

-   `totalSpotNumber` : The total number of spots offered by this parking site.
    This number can be difficult to be obtained for those parking locations on
    which spots are not clearly marked by lines. + Attribute type:
    [Number](http://schema.org/Number) + Allowed values: Any positive integer
    number or 0. + Normative references: DATEX 2 version 2.3 attribute
    _parkingNumberOfSpaces_ of the _ParkingRecord_ class. + Optional

-   `availableSpotNumber` : The number of spots available globally, including
    reserved spaces, such as those for disabled people, long term parkers and so
    on. This might be harder to estimate at those parking locations on which
    spots borders are not clearly marked by lines. + Attribute type:
    [Number](http://schema.org/Number) + Allowed values: A positive integer
    number, including 0. It must lower or equal than `totalSpotNumber`. +
    Metadata: + `timestamp` : Timestamp of the last attribute update + Type:
    [DateTime](https://schema.org/DateTime) + Optional

-   `extraSpotNumber` : The number of extra spots _available_, i.e. free. Extra
    spots are those reserved for special purposes and usually require a permit.
    Permit details will be found at parking group level (entity of type
    `ParkingGroup`). This value must aggregate free spots from all groups
    devoted to special parking conditions. + Attribute type:
    [Number](http://schema.org/Number) + Allowed values: A positive integer
    number, including 0. `extraSpotNumber` plus `availableSpotNumber` must be
    lower than or equal to `totalSpotNumber`. + Metadata: + `timestamp` :
    Timestamp of the last attribute update + Type:
    [DateTime](https://schema.org/DateTime)

-   `occupancyDetectionType` : Occupancy detection method(s).

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: The following from DATEX II version 2.3
        _OccupancyDetectionTypeEnum_:
        -   (`none`, `balancing`, `singleSpaceDetection`, `modelBased`,
            `manual`)
        -   Or any other application-specific
    -   Mandatory

-   `parkingMode` : Parking mode(s).

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: Those defined by the DATEX II version 2.3
        _ParkingModeEnum_ enumeration:
        -   (`perpendicularParking`, `parallelParking`, `echelonParking`)
    -   Optional

-   `averageSpotWidth` : The average width of parking spots.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `averageSpotLength` : The average length of parking spots.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `acceptedPaymentMethod` : Accepted payment method(s)

    -   Normative references: https://schema.org/acceptedPaymentMethod
    -   Optional

-   `image` : A URL containing a photo of this parking site.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `refParkingSpot` : Individual parking spots belonging to this on street
    parking site.

    -   Attribute type: List of references to
        [ParkingSpot](../../ParkingSpot/doc/spec.md)
    -   Optional

-   `refParkingGroup` : Reference to the parking group(s) (if any) belonging to
    this onstreet parking zone.

    -   Attribute type: List of references to
        [ParkingGroup](../../ParkingGroup/doc/spec.md)
    -   Optional

-   `areaServed` : Area served by this onstreet parking. Precise semantics can
    depend on the application or target city. For instance, it can be a
    neighbourhood, burough or district.
    -   Attribute type: [Text](http://schema.org/Text)
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use 1 (Normalized Format)

```json
{
    "id": "santander:daoiz_velarde_1_5",
    "type": "OnStreetParking",
    "category": {
        "value": ["blueZone", "shortTerm", "forDisabled"]
    },
    "permitActiveHours": {
        "value": {
            "blueZonePermit": "Mo, Tu, We, Th, Fr, Sa 09:00-20:00"
        }
    },
    "requiredPermit": {
        "value": ["blueZonePermit", "disabledPermit"]
    },
    "allowedVehicleType": {
        "value": "car"
    },
    "chargeType": {
        "value": ["temporaryFee"]
    },
    "refParkingGroup": {
        "type": "Relationship",
        "value": ["daoiz-velarde-1-5-main", "daoiz-velarde-1-5-disabled"]
    },
    "totalSpotNumber": {
        "value": 6
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
    "areaServed": {
        "value": "Zona Centro"
    },
    "maximumAllowedStay": {
        "value": "PT2H"
    },
    "dateModified": {
        "type": "DateTime",
        "value": "2016-06-02T09:25:55.00Z"
    },
    "extraSpotNumber": {
        "value": 2
    },
    "availableSpotNumber": {
        "value": 3,
        "metadata": {
            "timestamp": {
                "value": "2018-09-12T12:00:00",
                "type": "DateTime"
            }
        }
    }
}
```

## Examples of use 2

An on street parking which contains a group of parking spots reserved for
disabled people. At root entity level is announced that special parking spots
for disabled are present and two of them free.

Main `OnstreetParking` entity.

```
    {
      "id": "santander:daoiz_velarde_1_5",
      "type": "OnStreetParking",
      "category": ["blueZone", "shortTerm", "forDisabled"],
      "allowedVehicleType": "car",
      "chargeType": ["temporaryFee"],
      "requiredPermit": ["blueZonePermit", "disabledPermit"],
      "permitActiveHours": {
        "blueZonePermit": "Mo, Tu, We, Th, Fr, Sa 09:00-20:00"
      },
      "maximumAllowedStay": "PT2H",
      "availableSpotNumber": 3,
      "totalSpotNumber": 6,
      "extraSpotNumber": 2,
      "dateModified": "2016-06-02T09:25:55.00Z",
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
      "areaServed": "Zona Centro",
      "refParkingGroup": ["daoiz-velarde-1-5-main", "daoiz-velarde-1-5-disabled"]
    }
```

Two different parking groups are needed in this case:

A/ Subrogated `ParkingGroup` which gives details about the regular parking spots

```
    {
      "id": "daoiz-velarde-1-5-main",
      "type": "ParkingGroup",
      "category": ["onstreet", "blueZone", "shortTerm"],
      "allowedVehicleType": "car",
      "chargeType": ["temporaryFee"],
      "refParkingSite": "daoiz-velarde-1-5",
      "totalSpotNumber": 4,
      "availableSpotNumber": 1,
      "requiredPermit": "blueZonePermit"
      /* Other required attributes */
    }
```

B/ Subrogated `ParkingGroup`. `refPArkingSite` is a pointer to the root entity.
All the parking spots are free.

```
    {
      "id": "daoiz-velarde-1-5-disabled",
      "type": "ParkingGroup",
      "category": ["onstreet", "blueZone", "shortTerm", "onlyDisabled"],
      "allowedVehicleType": "car",
      "chargeType": ["temporaryFee"],
      "refParkingSite": "daoiz-velarde-1-5",
      "description": "Two parking spots reserved for disabled people",
      "totalSpotNumber": 2,
      "availableSpotNumber": 2,
      "requiredPermit": "disabledPermit,blueZonePermit"
      /* Other required attributes */
    }
```

## Test it with a real service

## Open issues

-   How to model tariffs
