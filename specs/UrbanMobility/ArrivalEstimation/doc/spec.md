# ArrivalEstimation

## Description

This Entity Type captures the estimated arrival time of a public transport
vehicle reaching a particular stop, whilst the vehicle is servicing a particular
route.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:gtfs:ArrivalEstimation:<identifier>`.

-   `type`: Entity Type

    -   It shall be equal to `ArrivalEstimation`

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `hasStop` : Stop to which this estimation applies to.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [gtfs:Stop](../../Stop/doc/spec.md)
    -   Mandatory

-   `hasTrip` : The trip to which this estimation applies to.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [gtfs:Trip](../../Trip/doc/spec.md)
    -   Mandatory

-   `remainingTime`: It shall contain the remaining time of arrival for the trip
    heading to the concerned stop.

    -   Attribute type: Property. [Text](https://schema.org/Text). Remaining
        time shall be encoded as a ISO8601 duration. Ex. `"PT8M5S"`.
    -   Attribute Metadata:
        -   `timestamp` (mapped to `observedAt` in NGSI-LD). Timestamp of the
            last attribute update
            -   Type: [DateTime](https://schema.org/DateTime)
            -   Mandatory
    -   Mandatory

-   `remainingDistance`: It shall contain the remaining distance (in meters) of
    arrival for the trip heading to the concerned stop.

    -   Attribute type: Property. Positive Number.
        [https://schema.org/Number](https://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp` (mapped to `observedAt` in NGSI-LD). Timestamp of the
            last attribute update
            -   Type: [DateTime](https://schema.org/DateTime)
            -   Mandatory
    -   Default Unit: Meters
    -   Optional

-   `headSign`: It shall contain the text that appears on a sign that identifies
    the trip's destination to passengers.
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Mandatory

### Examples of use 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:L5C1_Stop74_1",
    "type": "ArrivalEstimation",
    "hasTrip": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:gtfs:Trip:tus:5C1"
    },
    "headSign": {
        "value": "Plaza Italia"
    },
    "remainingTime": {
        "value": "PT8M5S"
    },
    "hasStop": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:gtfs:Stop:tus:74"
    },
    "remainingDistance": {
        "value": 1200
    }
}
```

### Examples of use 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:L5C1_Stop74_1",
    "type": "ArrivalEstimation",
    "hasStop": "urn:ngsi-ld:gtfs:Stop:tus:74",
    "hasTrip": "urn:ngsi-ld:gtfs:Trip:tus:5C1",
    "remainingTime": "PT8M5S",
    "remainingDistance": 1200,
    "headSign": "Plaza Italia"
}
```

## Open issues
