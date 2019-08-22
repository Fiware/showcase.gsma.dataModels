# ArrivalEstimation

## Description

This entity Type is intended to provide arrival estimation information that can
be used either in a standalone manner or to generate GTFS-RT feeds that
complement a GTFS static file.

## Data Model

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:ArrivalEstimation:<identifier>`

-   `type`: Entity Type

    -   It shall be equal to `ArrivalEstimation`

-   `refGtfsTransitFeedFile` : Reference to the entity pointing to the external
    GTFS file.

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional. Necessary to create GTFS-RT feeds

-   `routeId` : Identifier of the bus route (or bus line)

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory

-   `stopId` : Identifier of the stop

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory if `stopSequence` is not defined

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `lastUpdatedAt` : Last update of the entity set by the data provider. It is
    not automatically generated.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional.

-   `arrivalEstimationUpdate` : Current updates of the trips referred to the
    route/stop pair
    -   Attribute type: Property. Array of
        [StructuredValue](https://schema.org/StructuredValue)
    -   Subproperties (items):
        -   `arrivalDelay`: Delay in seconds (positive or negative). 0 means
            that the vehicle is on time
            -   Type: [Integer](https://schema.org/Integer)
            -   Optional. Necessary to create GTFS-RT feeds
        -   `arrivalTime`: Estimated arrival time in absolute time value
            (timestamp ISO 8601)
            -   Type: [DateTime](https://schema.org/DateTime)
            -   Optional. Mandatory if arrivalDelay is not defined
        -   `tripId`: Identifier of the trip as defined in the associated GTFS
            -   Type: [Text](https://schema.org/Text)
            -   Optional. Mandatory if neither `vehicleId` or `vehicleLabel` are defined. Necessary to create GTFS-RT feeds
        -   `vehicleId`: Vehicle identifier corresponding to the estimate
            -   Type: [Text](https://schema.org/Text)
            -   Optional. Mandatory if neither `tripId` or `vehicleLabel` are defined
        -   `vehicleLabel`: Human readable label to identify the vehicle
            -   Type: [Text](https://schema.org/Text)
            -   Optional. Mandatory if neither `tripId` or `vehicleId` are defined


### Examples of use 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:Santander:1",
    "type": "ArrivalEstimation",
    "refGtfsTransitFeedFile": {
        "value": "urn:ngsi-ld:GtfsTransitFeedFile:Santander:bus"
    },
    "routeId": {
        "value": "route1"
    },
    "stopId": {
        "value": "stop1"
    },
    "lastUpdatedAt": {
        "value": "2018-12-19T10:14:00.238Z",
        "type": "DateTime"
    },
    "arrivalEstimationUpdate": {
        "value": [
            {
                "tripId": "1",
                "arrivalDelay": -2
            },
            {
                "tripId": "2",
                "arrivalDelay": -2
            },
            {
                "tripId": "3",
                "arrivalDelay": -2
            }
        ]
    }
}
```

### Examples of use 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:Santander:1",
    "type": "ArrivalEstimation",
    "refGtfsTransitFeedFile": "urn:ngsi-ld:GtfsTransitFeedFile:Santander:bus",
    "routeId": "route1",
    "stopId": "stop1",
    "lastUpdatedAt": "2018-12-19T10:14:00.238Z",
    "arrivalEstimationUpdate": [
        {
            "tripId": "1",
            "arrivalDelay": -2
        },
        {
            "tripId": "2",
            "arrivalDelay": -2
        },
        {
            "tripId": "3",
            "arrivalDelay": -2
        }
    ]
}
```

## Open issues
