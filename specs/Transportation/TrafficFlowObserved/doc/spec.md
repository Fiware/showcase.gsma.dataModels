# Traffic flow observed

## Description

An observation of traffic flow conditions at a certain place and time. This
entity is primarily associated with the Automotive and Smart City vertical
segments and related IoT applications.

## Data Model

The data model is defined as shown below:

- `id` : Unique identifier.

- `type` : Entity type. It must be equal to `TrafficFlowObserved`.

- `source` : A sequence of characters giving the source of the entity data.
  - Attribute type: Text or URL
  - Optional

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

- `location` : Location of this traffic flow observation represented by a
    GeoJSON geometry.

  - Attribute type: `geo:json`.
  - Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
  - Mandatory if `refRoadSegment` is not present.

- `address` : Civic address of this traffic flow observation.

  - Normative References:
        [https://schema.org/address](https://schema.org/address)
  - Optional

- `refRoadSegment` : Concerned road segment on which the observation has been
    mede.

  - Attribute type: Reference to an entity of type
        [RoadSegment](../../RoadSegment/doc/spec.md).
  - Mandatory if `location` is not present.

- `dateModified` : Last update timestamp of this entity.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `laneId` : Lane identifier.

  - Attribute type: [Number](https://schema.org/Number)
  - Allowed values: Positive integer starting with `1`. Lane identification
        is done using the conventions defined by
        [RoadSegment](../../RoadSegment/doc/spec.md) which are based on
        [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Forward_%26_backward,_left_%26_right).
  - Mandatory

- `dateObserved` : The date and time of this observation in ISO8601 UTC
    format. It can be represented by an specific time instant or by an ISO8601
    interval. As a workaround for the lack of support of Orion Context Broker
    for datetime intervals, it can be used two separate attributes:
    `dateObservedFrom`, `dateObservedTo`. + Attribute type:
    [DateTime](https://schema.org/DateTime) or an ISO8601 interval represented
    as [Text](https://schema.org/Text). + Mandatory

- `dateObservedFrom` : Observation period start date and time. See
    `dateObserved`.

  - Attribute type: [DateTime](https://schema.org/DateTime).
  - Optional

- `dateObservedTo` : Observation period end date and time. See `dateObserved`.

  - Attribute type: [DateTime](https://schema.org/DateTime).
  - Optional

- `dateCreated` : Entity's creation timestamp.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `name` : Name given to this observation.

  - Normative References: [https://schema.org/name](https://schema.org/name)
  - Optional

- `description` : Description of this observation.

  - Normative References:
        [https://schema.org/description](https://schema.org/description)
  - Optional

- `intensity` : Total number of vehicles detected during this observation
    period.

  - Attribute type: [Number](https://schema.org/Number). Positive integer.
  - Optional

- `occupancy` : Fraction of the observation time where a vehicle has been
    occupying the observed laned.

  - Attribute type: [Number](https://schema.org/Number) between 0 and 1.
  - Optional

- `averageVehicleSpeed` : Average speed of the vehicles transiting during the
    observation period.

  - Attribute type: [Number](https://schema.org/Number)
  - Default unit: Kilometer per hour (Km/h).
  - Optional

- `averageVehicleLength` : Average length of the vehicles transiting during
    the observation period.

  - Attribute type: [Number](https://schema.org/Number)
  - Default unit: meter (m)
  - Optional

- `congested` : Flags whether there was a traffic congestion during the
    observation period in the referred lane. The absence of this attribute means
    no traffic congestion. + Attribute type:
    [Boolean](https://schema.org/Boolean) + Optional

- `averageHeadwayTime` : Average headway time. Headaway time is the time
    ellapsed between two consecutive vehicles.

  - Attribute type: [Number](https://schema.org/Number)
  - Default unit: second (s)
  - Optional

- `averageGapDistance` : Average gap distance between consecutive vehicles.

  - Attribute type: [Number](https://schema.org/Number)
  - Default unit: meter (m)
  - Optional

- `laneDirection` : Usual direction of travel in the lane referred by this
    observation. This attribute is useful when the observation is not
    referencing any road segment, allowing to know the direction of travel of
    the traffic flow observed. 
    - Attribute type:
    [Text](https://schema.org/Text) 
    - Allowed values: (`forward`, `backward`).
    See [RoadSegment.laneUsage](../../RoadSegment/doc/spec.md) for a description
    of the semantics of these values. 
    - Optional

- `reversedLane`: Flags whether traffic in the lane was reversed during the
    observation period. The absence of this attribute means no lane reversion. 
    - Attribute type: [Boolean](https://schema.org/Boolean) 
    - Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use (Normalized Format)

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

## Examples of use 2 (?options=keyValues simplified representation for data consumers)

```
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
           [
             -4.73735395519672, 41.6538181849672
           ],
           [
             -4.73414858659993, 41.6600594193478
           ],
           [
             -4.73447575302641, 41.659585195093
           ]
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

## Use it with a real service

T.B.D.

## Open issues
