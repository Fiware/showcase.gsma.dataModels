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

+ `path` : Itinerary's scheduled path geometry represented by a GeoJSON LineString. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
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
    + Attribute type: [Text](http://schema.org/Text)
    + Optional

+ `refArrival` : Segment's arrival entity's id.
    + Attribute type: [Text](http://schema.org/Text)
    + Optional

+ `scheduledDeparture` : Timestamp which represents when the departure should be made.
    + Attribute Type: [DateTime](http://schema.org/DateTime)

+ `scheduledArrival` : Timestamp which represents when the arrival should be made.
    + Attribute Type: [DateTime](http://schema.org/DateTime)

## Example

    {
      "id" : "itinerarysegment:89237",
      "type" : "ItinerarySegment",
      "refDeparture" : "busstop:3212",
      "refArrival" : "busstop:3213",
      "scheduledDeparture" : "2016-06-29T08:10:00.000Z",
      "scheduledArrival" : "2016-06-29T08:15:00.000Z"
    }
    
## Test it with a real service

T.B.D.
