# ItinerarySegment

## Description

A piece of an itinerary. Itineraries always have a purpose. An itinerary is not just traveling to a certain point, there is some intention of interacting there with some entity:

+ Gathering passengers at bus stops.
+ Delivering packages at houses, business, depots.
+ Collecting waste containers.
+ ...

Therefore it is more meaningful and explicit to keep a reference to the entities that are going to be visited. Having to move to that entity, means consequently travelling to its 
location which will be contained in that entity's instance.

## Data Model

+ `id` : Unique identifier.

+ `type` : Entity type. It must be equal to `ItinerarySegment`. 

+ `name` : Name given to the itinerary
    + Normative References: [https://schema.org/name](https://schema.org/name)
    + Optional

+ `description` : Description about the itinerary. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

+ `scheduledPath` : Itinerary's scheduled path geometry represented by a GeoJSON LineString. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

+ `performedPath` : Performed path of the vehicle, to be updated while vehicle is travelling. A geometry represented by a GeoJSON LineString. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional
 
+  `refAssignedVehicle` : Vehicle assigned to this itinerary segment.
    + Attribute type: Reference to a [Vehicle](../../../Transportation/Vehicle/doc/spec.md) entity.
    + Optional

+ `departurePoint` : Departure location represented by a GeoJSON Point.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `refDeparture is not present.

+ `arrivalPoint` : Departure location represented by a GeoJSON Point.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `refArrival is not present.

+ `refDeparture` : Segment's departure entity's id.
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue).
        + Subproperties:
            + `entityType` : Entity type which is the departuring point.
                + Type: [Text](http://schema.org/Text)
            + `id` : Entities id.
                + Type: List of [Text](http://schema.org/Text)
    + Optional

+ `refArrival` : Segment's arrival entity's id.
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue).
        + Subproperties:
            + `entityType` : Entity type which the arrival point.
                + Type: [Text](http://schema.org/Text)
            + `id` : Entities id.
                + Type: List of [Text](http://schema.org/Text)
    + Optional

+ `scheduledDeparture` : Timestamp which represents when the departure should be made.
    + Attribute Type: [DateTime](http://schema.org/DateTime)

+ `scheduledArrival` : Timestamp which represents when the arrival should be made.
    + Attribute Type: [DateTime](http://schema.org/DateTime)

+ `departureTimestamp`: Timestamp which captures when the user started the trip segment. This value can also appear as a FIWARE [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/develop/README.md#TimeInstant)
    + Attribute type: [Time](http://schema.org/Time) or ```ISO8601``` (legacy).
    + Mandatory

+ `arrivalTimestamp`:	Timestamp which captures when the user finished the trip segment. This value can also appear as a FIWARE [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib/blob/develop/README.md#TimeInstant)
    + Attribute type: [Time](http://schema.org/Time) or ```ISO8601``` (legacy).
    + Optional

## Example

    {
      "id": "itinerarysegment:89237",
      "type": "ItinerarySegment",
      "refAssignedVehicle" : "vehicle-512"
    }
    
## Test it with a real service

T.B.D.
