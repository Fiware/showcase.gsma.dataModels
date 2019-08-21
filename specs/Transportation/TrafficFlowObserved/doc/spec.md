# Traffic flow observed

**Note: The latest version of this Data Model can be
found at [https://github.com/smart-data-models/dataModel.Transportation](https://github.com/smart-data-models/dataModel.Transportation)**

## Description

An observation of traffic flow conditions at a certain place and time. This
entity is primarily associated with the Automotive and Smart City vertical
segments and related IoT applications.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `TrafficFlowObserved`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    -   Optional

-   `vehicleType` : Type of vehicle from the point of view of its structural
    characteristics.

    -   See definition at [Vehicle](../../Vehicle/Vehicle/doc/spec.md).
    -   Optional

-   `vehicleSubType` : allows to specify a sub type of `vehicleType` , eg if the
    `vehicleType` is set to `Lorry` the `vehicleSubType` may be `OGV1` or `OGV2`
    to convey more information about the exact type of vehicle
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `location` : Location of this traffic flow observation represented by a
    GeoJSON geometry.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `refRoadSegment` is not present.

-   `address` : Civic address of this traffic flow observation.

    -   Attribute type: Property. [Address](https://schema.org/address)
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Optional

-   `refRoadSegment` : Concerned road segment on which the observation has been
    mede.

    -   Attribute type: Relationship. Reference to an entity of type
        [RoadSegment](../../RoadSegment/doc/spec.md).
    -   Mandatory if `location` is not present.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `laneId` : Lane identifier.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Allowed values: Positive integer starting with `1`. Lane identification
        is done using the conventions defined by
        [RoadSegment](../../RoadSegment/doc/spec.md) which are based on
        [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Forward_%26_backward,_left_%26_right).
    -   Mandatory

-   `dateObserved` : The date and time of this observation in ISO8601 UTC
    format. It can be represented by an specific time instant or by an ISO8601
    interval. As a workaround for the lack of support of Orion Context Broker
    for datetime intervals, it can be used two separate attributes:
    `dateObservedFrom`, `dateObservedTo`.
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime) or an ISO8601 interval represented
    as [Text](https://schema.org/Text).
    -   Mandatory

-   `dateObservedFrom` : Observation period start date and time. See
    `dateObserved`.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime).
    -   Optional

-   `dateObservedTo` : Observation period end date and time. See `dateObserved`.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime).
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name` : Name given to this observation.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to [name](https://schema.org/name)
    -   Optional

-   `description` : Description of this observation.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description` equivalent to [description](https://schema.org/description)
    -   Optional

-   `intensity` : Total number of vehicles detected during this observation
    period.

    -   Attribute type: Property. [Number](https://schema.org/Number). Positive integer.
    -   Optional

-   `occupancy` : Fraction of the observation time where a vehicle has been
    occupying the observed laned.

    -   Attribute type: Property. [Number](https://schema.org/Number) between 0 and 1.
    -   Optional

-   `averageVehicleSpeed` : Average speed of the vehicles transiting during the
    observation period.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Kilometer per hour (Km/h).
    -   Optional

-   `averageVehicleLength` : Average length of the vehicles transiting during
    the observation period.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: meter (m)
    -   Optional

-   `congested` : Flags whether there was a traffic congestion during the
    observation period in the referred lane. The absence of this attribute means
    no traffic congestion.

    -   Attribute type: Property. [Boolean](https://schema.org/Boolean)
    -   Optional

-   `averageHeadwayTime` : Average headway time. Headaway time is the time
    ellapsed between two consecutive vehicles.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: second (s)
    -   Optional

-   `averageGapDistance` : Average gap distance between consecutive vehicles.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: meter (m)
    -   Optional

-   `laneDirection` : Usual direction of travel in the lane referred by this
    observation. This attribute is useful when the observation is not
    referencing any road segment, allowing to know the direction of travel of
    the traffic flow observed.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: (`forward`, `backward`). See
        [RoadSegment.laneUsage](../../RoadSegment/doc/spec.md) for a description
        of the semantics of these values.
    -   Optional

-   `reversedLane`: Flags whether traffic in the lane was reversed during the
    observation period. The absence of this attribute means no lane reversion.
    -   Attribute type: Property. [Boolean](https://schema.org/Boolean)
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "TrafficFlowObserved-Valladolid-osm-60821110",
    "type": "TrafficFlowObserved",
    "dateObserved": {
        "value": "2016-12-07T11:10:00/2016-12-07T11:15:00"
    },
    "laneDirection": {
        "value": "forward"
    },
    "dateObservedFrom": {
        "type": "DateTime",
        "value": "2016-12-07T11:10:00"
    },
    "averageVehicleLength": {
        "value": 9.87
    },
    "averageHeadwayTime": {
        "value": 0.5
    },
    "occupancy": {
        "value": 0.76
    },
    "reversedLane": {
        "value": false
    },
    "dateObservedTo": {
        "type": "DateTime",
        "value": "2016-12-07T11:15:00"
    },
    "intensity": {
        "value": 197
    },
    "laneId": {
        "value": 1
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "LineString",
            "coordinates": [
                [-4.73735395519672, 41.6538181849672],
                [-4.73414858659993, 41.6600594193478],
                [-4.73447575302641, 41.659585195093]
            ]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Valladolid",
            "addressCountry": "ES",
            "streetAddress": "Avenida de Salamanca"
        }
    },
    "averageVehicleSpeed": {
        "value": 52.6
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "TrafficFlowObserved-Valladolid-osm-60821110",
    "type": "TrafficFlowObserved",
    "laneId": 1,
    "address": {
        "streetAddress": "Avenida de Salamanca",
        "addressLocality": "Valladolid",
        "addressCountry": "ES"
    },
    "location": {
        "type": "LineString",
        "coordinates": [
            [-4.73735395519672, 41.6538181849672],
            [-4.73414858659993, 41.6600594193478],
            [-4.73447575302641, 41.659585195093]
        ]
    },
    "dateObserved": "2016-12-07T11:10:00/2016-12-07T11:15:00",
    "dateObservedFrom": "2016-12-07T11:10:00Z",
    "dateObservedTo": "2016-12-07T11:15:00Z",
    "averageHeadwayTime": 0.5,
    "intensity": 197,
    "occupancy": 0.76,
    "averageVehicleSpeed": 52.6,
    "averageVehicleLength": 9.87,
    "reversedLane": false,
    "laneDirection": "forward"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:TrafficFlowObserved:TrafficFlowObserved-Valladolid-osm-60821110",
    "type": "TrafficFlowObserved",
    "dateObserved": {
        "type": "Property",
        "value": "2016-12-07T11:10:00/2016-12-07T11:15:00"
    },
    "laneDirection": {
        "type": "Property",
        "value": "forward"
    },
    "dateObservedFrom": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-12-07T11:10:00Z"
        }
    },
    "averageVehicleLength": {
        "type": "Property",
        "value": 9.87
    },
    "averageHeadwayTime": {
        "type": "Property",
        "value": 0.5
    },
    "occupancy": {
        "type": "Property",
        "value": 0.76
    },
    "reversedLane": {
        "type": "Property",
        "value": false
    },
    "dateObservedTo": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-12-07T11:15:00Z"
        }
    },
    "intensity": {
        "type": "Property",
        "value": 197
    },
    "laneId": {
        "type": "Property",
        "value": 1
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "LineString",
            "coordinates": [
                [-4.73735395519672, 41.6538181849672],
                [-4.73414858659993, 41.6600594193478],
                [-4.73447575302641, 41.659585195093]
            ]
        }
    },
    "address": {
        "type": "Property",
        "value": {
            "addressLocality": "Valladolid",
            "addressCountry": "ES",
            "streetAddress": "Avenida de Salamanca",
            "type": "PostalAddress"
        }
    },
    "averageVehicleSpeed": {
        "type": "Property",
        "value": 52.6
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Use it with a real service

T.B.D.

## Open issues
