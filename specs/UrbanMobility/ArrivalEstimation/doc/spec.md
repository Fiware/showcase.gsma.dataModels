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

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `hasStop` : Stop to which this estimation applies to.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsStop](../../GtfsStop/doc/spec.md)
    -   Mandatory

-   `hasTrip` : The trip to which this estimation applies to.

    -   Attribute type: Relationship. It shall point to an Entity of Type
        [GtfsTrip](../../GtfsTrip/doc/spec.md)
    -   Mandatory

-   `remainingTime`: It shall contain the remaining time of arrival for the trip
    heading to the concerned stop.

    -   Attribute type: Property. [Text](https://schema.org/Text). Remaining
        time shall be encoded as a ISO8601 duration. Ex. `"PT8M5S"`.
    -   Attribute Metadata:
        -   `timestamp` (mapped to `observedAt` in NGSI-LD). Timestamp of the
            last attribute update
            -   Type: [DateTime](https://schema.org/DateTime) - Mandatory
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

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:L5C1_Stop74_1",
    "type": "ArrivalEstimation",
    "hasTrip": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsTrip:tus:5C1"
    },
    "headSign": {
        "value": "Plaza Italia"
    },
    "remainingTime": {
        "value": "PT8M5S"
    },
    "hasStop": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:GtfsStop:tus:74"
    },
    "remainingDistance": {
        "value": 1200
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:L5C1_Stop74_1",
    "type": "ArrivalEstimation",
    "hasStop": "urn:ngsi-ld:GtfsStop:tus:74",
    "hasTrip": "urn:ngsi-ld:GtfsTrip:tus:5C1",
    "remainingTime": "PT8M5S",
    "remainingDistance": 1200,
    "headSign": "Plaza Italia"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:ArrivalEstimation:L5C1_Stop74_1",
    "type": "ArrivalEstimation",
    "hasTrip": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsTrip:tus:5C1"
    },
    "headSign": {
        "type": "Property",
        "value": "Plaza Italia"
    },
    "remainingTime": {
        "type": "Property",
        "value": "PT8M5S"
    },
    "hasStop": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:GtfsStop:tus:74"
    },
    "remainingDistance": {
        "type": "Property",
        "value": 1200
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Open issues
