# Off Street Parking

## Description

A site, off street, intended to park vehicles, managed independently and with
suitable and clearly marked access points (entrances and exits). If necessary,
and for management purposes or to deal with multi-location parking sites, it can
be divided into different zones modelled by the entity type
[ParkingGroup](../../ParkingGroup/doc/spec.md) . In DATEX 2 version 2.3
terminology it corresponds to a _UrbanParkingSite_ of type _offStreetParking_.

A data dictionary for DATEX II terms can be found at
[http://datexbrowser.tamtamresearch.com/](http://datexbrowser.tamtamresearch.com/).

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `OffStreetParking`.

-   `dateCreated` : Entity's creation timestamp

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `location` : Geolocation of the parking site represented by a GeoJSON
    (Multi)Polygon or Point.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Registered parking site civic address.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not defined.

-   `name` : Name given to the parking site.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `category` : Parking site's category(ies). The purpose of this field is to
    allow to tag, generally speaking, off street parking entities.
    Particularities and detailed descriptions should be found under the
    corresponding specific attributes. + Attribute type: List of
    [Text](http://schema.org/Text) + Allowed values: + (`public`, `private`,
    `publicPrivate`, `urbanDeterrentParking`, `parkingGarage`, `parkingLot`,
    `shortTerm`, `mediumTerm`, `longTerm`, `free`, `feeCharged`, `staffed`,
    `guarded`, `barrierAccess`, `gateAccess`, `freeAccess`,
    `forElectricalCharging`, `onlyResidents`, `onlyWithPermit`, `forEmployees`,
    `forVisitors`, `forCustomers`, `forStudents`, `forMembers`, `forDisabled`,
    `forResidents`, `underground`, `ground`) + The semantics of the `forxxx`
    values is that the parking offers specific spots subject to that particular
    condition. + The semantics of the `onlyxxx`values is that the parking only
    allows to park on that particular condition. + Other application-specific +
    Mandatory

-   `allowedVehicleType` : Vehicle type(s) allowed. The first element of this
    array _MUST_ be the principal vehicle type allowed. Free spot numbers of
    other allowed vehicle types might be reported under the attribute
    `extraSpotNumber` and through specific entities of type _ParkingGroup_. +
    Attribute type: List of [Text](http://schema.org/Text) + Allowed Values: The
    following values defined by _VehicleTypeEnum_,
    [DATEX 2 version 2.3](http://d2docs.ndwcloud.nu/): +
    (`agriculturalVehicle`, `bicycle`, `bus`, `car`, `caravan`,
    `carWithCaravan`, `carWithTrailer`, `constructionOrMaintenanceVehicle`,
    `lorry`, `moped`, `motorcycle`, `motorcycleWithSideCar`, `motorscooter`,
    `tanker`, `trailer`, `van`, `anyVehicle`) + Mandatory

-   `chargeType` : Type(s) of charge performed by the parking site.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: Some of those defined by the DATEX II version 2.3
        _ChargeTypeEnum_ enumeration:
        -   (`flat`, `minimum`, `maximum`, `additionalIntervalPrice`
            `seasonTicket` `temporaryPrice` `firstIntervalPrice`,
            `annualPayment`, `monthlyPayment`, `free`, `other`)
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
    (`employeePermit`, `studentPermit`, `fairPermit`, `governmentPermit`,
    `residentPermit`, `specificIdentifiedVehiclePermit`, `visitorPermit`,
    `noPermitNeeded`) + Any other application-specific + Mandatory

-   `occupancyDetectionType` : Occupancy detection method(s).

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: The following from DATEX II version 2.3
        _OccupancyDetectionTypeEnum_:
        -   (`none`, `balancing`, `singleSpaceDetection`, `modelBased`,
            `manual`)
        -   Or any other application-specific
    -   Mandatory

-   `acceptedPaymentMethod` : Accepted payment method(s).

    -   Normative references: https://schema.org/acceptedPaymentMethod
    -   Optional

-   `priceRatePerMinute` : Price rate per minute.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Optional

-   `priceCurrency` : Price currency of price rate per minute.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Normative references:
        [https://schema.org/priceCurrency](https://schema.org/priceCurrency)
    -   Optional

-   `description` : Description about the parking site.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `image` : A URL containing a photo of this parking site.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `layout` : Parking layout. Gives more details to the `category` attribute.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Allowed values: As per the _ParkingLayoutEnum_ of DATEX II version 2.3:
        -   one Of (`automatedParkingGarage`, `surface`, `multiStorey`,
            `singleLevel`, `multiLevel`, `openSpace`, `covered`, `nested`,
            `field`, `rooftop`, `sheds`, `carports`, `garageBoxes`, `other`).
            See also
            [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Tag:amenity%3Dparking).
        -   Or any other value useful for the application and not covered above.
    -   Optional

-   `usageScenario` : Usage scenario(s). Gives more details to the `category`
    attribute.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: Those defined by the enumeration
        _ParkingUsageScenarioEnum_ of DATEX II version 2.3:
        -   (`truckParking`, `parkAndRide`, `parkAndCycle`, `parkAndWalk`,
            `kissAndRide`, `liftshare`, `carSharing`, `restArea`, `serviceArea`,
            `dropOffWithValet`, `dropOffMechanical`, `eventParking`,
            `automaticParkingGuidance`, `staffGuidesToSpace`, `vehicleLift`,
            `loadingBay`, `dropOff`, `overnightParking`, `other`)
        -   Or any other value useful for the application and not covered above.
    -   Optional

-   `parkingMode` : Parking mode(s).

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Allowed values: Those defined by the DATEX II version 2.3
        _ParkingModeEnum_ enumeration:
        -   (`perpendicularParking`, `parallelParking`, `echelonParking`)
    -   Optional

-   `facilities` : Facilities provided by this parking site.

    -   Attributes: List of [Text](http://schema.org/Text)
    -   Allowed values: The following defined by the _EquipmentTypeEnum_
        enumeration of DATEX II version 2.3:
        -   (`toilet`, `shower`, `informationPoint`, `internetWireless`,
            `payDesk`, `paymentMachine`, `cashMachine`, `vendingMachine`,
            `faxMachineOrService`, `copyMachineOrService`, `safeDeposit`,
            `luggageLocker`, `publicPhone`, `elevator`, `dumpingStation`
            `freshWater`, `wasteDisposal`, `refuseBin`, `iceFreeScaffold`,
            `playground`, `electricChargingStation`, `bikeParking`,
            `tollTerminal`, `defibrillator`, `firstAidEquipment` `fireHose`
            `fireExtinguisher` `fireHydrant`)
        -   Any other application-specific
    -   Optional

-   `security` : Security aspects provided by this parking site.

    -   Attributes: List of [Text](http://schema.org/Text)
    -   Allowed values: The following, some of them, defined by
        _ParkingSecurityEnum_ of DATEX II version 2.3:
        -   (`patrolled`, `securityStaff`, `externalSecurity`, `cctv`, `dog`,
            `guard24hours`, `lighting`, `floodLight`, `fences`
            `areaSeperatedFromSurroundings`)
        -   Any other application-specific
    -   Optional

-   `highestFloor` : For parking sites with multiple floor levels, highest
    floor.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: An integer number. 0 is ground level. Upper floors are
        positive numbers. Lower floors are negative ones.
    -   Optional

-   `lowestFloor` : For parking sites with multiple floor levels, lowest floor.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Allowed values: An integer number.
    -   Optional

-   `maximumParkingDuration` : Maximum allowed stay at site, on a general basis,
    encoded as a ISO8601 duration. A `null` or empty value indicates an
    indefinite duration. + Attribute type: [Text](http://schema.org/Text) +
    Optional

-   `totalSpotNumber` : The total number of spots offered by this parking site.
    This number can be difficult to be obtained for those parking locations on
    which spots are not clearly marked by lines. + Attribute type:
    [Number](http://schema.org/Number) + Allowed values: Any positive integer
    number or 0. + Normative references: DATEX 2 version 2.3 attribute
    _parkingNumberOfSpaces_ of the _ParkingRecord_ class. + Optional

-   `availableSpotNumber` : The number of spots available (_including_ all
    vehicle types or reserved spaces, such as those for disabled people, long
    term parkers and so on). This might be harder to estimate at those parking
    locations on which spots borders are not clearly marked by lines. +
    Attribute type: [Number](http://schema.org/Number) + Allowed values: A
    positive integer number, including 0. It must lower or equal than
    `totalSpotNumber`. + Metadata: + `timestamp` : Timestamp of the last
    attribute update + Type: [DateTime](https://schema.org/DateTime) + Optional

-   `extraSpotNumber` : The number of extra spots _available_, i.e. free. This
    value must aggregate free spots from all groups mentioned below: A/ Those
    reserved for special purposes and usually require a permit. Permit details
    will be found at parking group level (entity of type `ParkingGroup`). B/
    Those reserved for other vehicle types different than the principal allowed
    vehicle type. C/ Any other group of parking spots not subject to the general
    condition rules conveyed by this entity. + Attribute type:
    [Number](http://schema.org/Number) + Allowed values: A positive integer
    number, including 0. + Metadata: + `timestamp` : Timestamp of the last
    attribute update + Type: [DateTime](https://schema.org/DateTime) + Optional

-   `openingHours` : Opening hours of the parking site.

    -   Normative references:
        [http://schema.org/openingHours](http://schema.org/openingHours)
    -   Optional

-   `firstAvailableFloor` : Number of the floor closest to the ground which
    currently has available parking spots.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Metadata:
        -   `timestamp` : Timestamp of the last attribute update
        -   Type: [DateTime](https://schema.org/DateTime)
    -   Allowed values: Stories are numbered between -n and n, being 0 ground
        floor.
    -   Optional

-   `specialLocation` : If the parking site is at a special location (airport,
    depatment store, etc.) it conveys what is such special location. + Attribute
    type: [Text](http://schema.org/Text) + Allowed values: Those defined by
    _ParkingSpecialLocationEnum_ of
    [DATEX II version 2.3](http://www.datex2.eu/content/parking-publications-extension-v10a): +
    (`airportTerminal`, `exhibitonCentre`, `shoppingCentre`, `specificFacility`,
    `trainStation`, `campground`, `themePark`, `ferryTerminal`,
    `vehicleOnRailTerminal`, `coachStation`, `cableCarStation`,
    `publicTransportStation`, `market`, `religiousCentre`, `conventionCentre`,
    `cinema`, `skilift`, `hotel`, `other`) + Optional

-   `status` : Status of the parking site.

    -   Attribute type: List of [Text](http://schema.org/Text)
    -   Metadata:
        -   `timestamp` : Timestamp of the last attribute update
        -   Type: [DateTime](https://schema.org/DateTime)
    -   Allowed values: The following defined by the following enumerations
        defined by DATEX II version 2.3 :
        -   _ParkingSiteStatusEnum_
        -   _OpeningStatusEnum_
        -   (`open`, `closed`, `closedAbnormal`,`openingTimesInForce`, `full`,
            `fullAtEntrance`, `spacesAvailable`, `almostFull`)
        -   Or any other application-specific
    -   Optional

-   `reservationType` : Conditions for reservation.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Allowed values: The following specified by _ReservationTypeEnum_ of
        DATEX II version 2.3:
        -   one Of (`optional`, `mandatory`, `notAvailable`, `partly`).
    -   Optional

-   `owner` : Parking site's owner.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Optional

-   `provider` : Parking site service provider.

    -   Normative references:
        [https://schema.org/provider](https://schema.org/provider)
    -   Optional

-   `measuresPeriod` : The measures period related to availableSpotNumber and
    priceRatePerMinute.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Optional

-   `measuresPeriodUnit` : The measures period unit related to
    availableSpotNumber and priceRatePerMinute.

    -   Attribute type: [unitText](http://schema.org/unitText)
    -   Optional

-   `contactPoint` : Parking site contact point.

    -   Normative references:
        [https://schema.org/contactPoint](https://schema.org/contactPoint)
    -   Optional

-   `averageSpotWidth` : The average width of parking spots.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `averageSpotLength` : The average length of parking spots.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Default unit: Meters
    -   Optional

-   `maximumAllowedHeight` : Maximum allowed height for vehicles. If there are
    multiple zones, it will be the minimum height of all the zones. + Attribute
    type: [Number](http://schema.org/Number) + Default unit: Meters + Optional

-   `maximumAllowedWidth` : Maximum allowed width for vehicles. If there are
    multiple zones, it will be the minimum width of all the zones. + Attribute
    type: [Number](http://schema.org/Number) + Default unit: Meters + Optional

-   `refParkingAccess` : Parking site's access point(s).

    -   Attribute type: List of references to
        [ParkingAccess](../../ParkingAccess/doc/spec.md)
    -   Optional

-   `refParkingGroup` : Parking site's identified group(s). A group can
    correspond to a zone, a complete storey, a group of spots, etc.

    -   Attribute type: List of references to
        [ParkingGroup](../../ParkingGroup/doc/spec.md)
    -   Optional

-   `refParkingSpot` : Individual parking spots belonging to this offstreet
    parking site.

    -   Attribute type: List of references to
        [ParkingSpot](../../ParkingSpot/doc/spec.md)
    -   Optional

-   `areaServed` : Area served by this parking site. Precise semantics can
    depend on the application or target city. For instance, it can be a
    neighbourhood, burough or district.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Optional

-   `aggregateRating` : Aggregated rating for this parking site.
    -   Normative References:
        [https://schema.org/aggregateRating](https://schema.org/aggregateRating)
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use 1 (Normalized Format)

```json
{
    "id": "porto-ParkingLot-23889",
    "type": "OffStreetParking",
    "category": {
        "value": [
            "underground",
            "public",
            "feeCharged",
            "mediumTerm",
            "barrierAccess"
        ]
    },
    "layout": {
        "value": ["multiLevel"]
    },
    "name": {
        "value": "Parque de estacionamento Trindade"
    },
    "requiredPermit": {
        "value": []
    },
    "allowedVehicleType": {
        "value": ["car"]
    },
    "availableSpotNumber": {
        "value": 132,
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2018-09-21T12:00:00"
            }
        }
    },
    "totalSpotNumber": {
        "value": 414
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-8.60961198807, 41.150691773]
        }
    },
    "chargeType": {
        "value": ["temporaryPrice"]
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Porto",
            "addressCountry": "Portugal",
            "streetAddress": "Rua de Fernandes Tom\u00e1s"
        }
    },
    "maximumParkingDuration": {
        "value": "PT8H"
    },
    "dateModified": {
        "type": "DateTime",
        "value": "2016-06-02T09:25:55.00Z"
    },
    "description": {
        "value": "Municipal car park located near the Trindade metro station and the Town Hall"
    }
}
```

## Examples of use 2

A public off street parking underground controlled by a barrier.

    {
      "id": "porto-ParkingLot-23889",
      "type": "OffStreetParking",
      "name": "Parque de estacionamento Trindade",
      "category": ["underground", "public", "feeCharged", "mediumTerm", "barrierAccess"],
      "chargeType": ["temporaryPrice"],
      "requiredPermit": [],
      "layout": ["multiLevel"],
      "maximumParkingDuration": "PT8H",
      "location": {
        "coordinates": [-8.60961198807, 41.150691773],
        "type": "Point"
      },
      "allowedVehicleType": ["car"],
      "totalSpotNumber": 414,
      "availableSpotNumber": 132,
      "address": {
        "streetAddress": "Rua de Fernandes Tomás",
        "addressLocality": "Porto",
        "addressCountry": "Portugal"
      },
      "description": "Municipal car park located near the Trindade metro station and the Town Hall",
      "dateModified": "2016-06-02T09:25:55.00Z"
    }

Urban Deterrent (xxxx and ride) parking. Free. 2 hours at a maximum.

    {
       "id": "pdu-valladolid-1",
       "type": "OffStreetParking",
       "name": "Parking Disuasorio 1",
       "category": ["public", "urbanDeterrentParking", "shortTerm", "ground", "parkingLot"],
       "usageScenario": ["parkAndRide", "parkAndCycle"],
       "layout": ["openSpace"],
       "chargeType": ["freeParking"],
       "allowedVehicleType": ["car"],
       "maximumParkingDuration": "PT2H",
       "requiredPermit": null,
       "areaServed": "Centro",
       "address": {
          "streetAddress": "Calle La India",
          "addressLocality": "Valladolid",
          "addressCountry": "ES"
      }
    }

Long stay parking. Maximum 4 days. Charging depends on time spent.

    {
      "id": "long-stay-valladolid-2",
      "type": "OffStreetParking",
      "name": "El Corte Ingles",
      "usageScenario": ["overnight"],
      "category": ["public", "longTerm", "underground", "parkingGarage"],
      "layout": ["singleLevel"],
      "chargeType": ["temporaryPrice"],
      "allowedVehicleType": ["car"],
      "maximumParkingDuration": "P4D",
      "requiredPermit": null,
      "address": {
          "streetAddress": "Paseo de Zorrilla, 96",
          "addressLocality": "Valladolid",
          "addressCountry": "ES"
      }
    }

Off street parking with an specific area devoted to residents (100 spots).

    {
       "id": "parking-example-234",
       "type": "OffStreetParking",
       "name": "La Farola 1",
       "category": ["public", "shortTerm", "longTerm", "forResidents"],
       "chargeType": ["temporaryPrice", "annualTax"],
       "totalSpotNumber": 250,
       "availableSpotNumber": 100,
       "extraSpotNumber": 60,
       "refParkingGroup": ["example-234-g-regular", "example-234-g-residents"],
       "requiredPermit": ["noPermit", "residentPermit"] /* Generally speaking no permit */
       /* Other required fields (Check model) */
    }

Two different groups are needed:

1/ Subrogated parking group to denote regular parking spots.

    {
      "id": "example-234-g-regular",
      "type": "ParkingGroup",
      "name": "La Farola 1 - Público General",
      "chargeType": ["temporaryPrice"],
      "category": ["offstreet", "shortTerm"],
      "totalSpotNumber": 150,
      "availableSpotNumber": 40,
      "requiredPermit": null,
      "refParkingSite": "parking-example-234",
      "allowedVehicleType": "car",
      "maximumParkingDuration": "PT2H"
      /* Other required fields (Check model) */
    }

2/ Subrogated parking group to denote those parking spots devoted for residents.

    {
      "id": "example-234-g-residents",
      "type": "ParkingGroup",
      "name": "La Farola 1 - Residentes",
      "chargeType": ["annualTax"],   /* Annual payment for residents */
      "category": ["offstreet", "longTerm", "onlyResidents"], /* Group Category. Overwrites parent's */
      "totalSpotNumber": 100,
      "availableSpotNumber": 60,
      "requiredPermit": "residentPermit",
      "refParkingSite": "parking-example-234",
      "allowedVehicleType": "car",
      "maximumParkingDuration": null
      /* Other required fields (Check model) */
    }

Private parking only for employees. A devoted visitor zone.

    {
      "id": "district-telefonica-parking-1",
      "type": "OffStreetParking",
      "name": "Distrito T - Parking Oeste",
      "category": ["private", "underground", "mediumTerm", "forEmployees", "onlyWithPermit", "forVisitors"],
      "requiredPermit": ["employeePermit", "visitorPermit"],
      "chargeType": ["free"],
      "allowedVehicleType": ["car"],
      "maximumParkingDuration": "PT12H",
      "totalSpotNumber": 250,
      "availableSpotNumber": 100,
      "extraSpotNumber": 10,
      "refParkingGroup": ["dt-p1-employee-group", "dt-p1-visitor-group"]
       /* Other required fields (Check model) */
    }

Two different groups are needed:

1/ Subrogated parking group modelling regular employee's spots.

    {
      "id": "dt-p1-employee-group",
      "type": "ParkingGroup",
      "category": ["offstreet", "onlyWithPermit", "shortTerm"],
      "totalSpotNumber": 230,
      "availableSpotNumber": 50,
      "requiredPermit": "employeePermit",
      "chargeType": ["free"],
      "refParkingSite": "district-telefonica-parking-1",
      "allowedVehicleType": "car"
      /* Other required fields (Check model) */
    }

2/ Subrogated parking group modelling visitor's spots.

    {
      "id": "dt-p1-visitor-group",
      "type": "ParkingGroup",
      "category": ["offstreet", "onlyWithPermit", "shortTerm"],
      "totalSpotNumber": 20,
      "availableSpotNumber": 10,
      "requiredPermit": "visitorPermit",
      "chargeType": ["free"],
      "refParkingSite": "district-telefonica-parking-1",
      "allowedVehicleType": "car"
      /* Other required fields (Check model) */
    }

## Test it with a real service

## Open issues

-   How to model tariffs (use DATEX II version 2.3 as possible input)
