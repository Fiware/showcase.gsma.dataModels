# PerformedItinerarySegment

## Description

The performance of a piece of an itinerary.

## Data Model

+ `id` : Unique identifier.

+ `type` : Entity type. It must be equal to `PerformedItinerarySegment`. 

+ `refItinerarySegment` : The scheduled ItinerarySegment the vehicle has performed. 
    + Attribute type: Reference to a [ItinerarySegment](../../../Transportation/ServiceNetwork/ItinerarySegment/doc/spec.md) entity.
    + Mandatory

+ `performedPath` : Performed path of the vehicle, to be updated while vehicle is travelling. A geometry represented by a GeoJSON LineString. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Optional
 
+ `refVehicle` : Vehicle which performed to this itinerary segment.
    + Attribute type: Reference to a [Vehicle](../../../Transportation/Vehicle/doc/spec.md) entity.
    + Mandatory

+ `dateDeparted`: Timestamp which captures when the vehicle started the trip segment.
    + Attribute type: [DateTime](https://schema.org/DateTime).
    + Mandatory

+ `dateArrived`: Timestamp which captures when the vehicle finished the trip segment.
    + Attribute type: [DateTime](https://schema.org/DateTime).
    + Mandatory

## Example

    {
      "id": "performeditinerarysegment:89237",
      "type": "PerformedItinerarySegment",
      "refItinerarySegment" : "itinerarysegment:89237",
      "refVehicle" : "vehicle:512",
      "dateDeparted" : "2016-06-29T08:10:00.000Z",
      "dateArrived" : "2016-06-29T08:26:09.224Z"
    }
    
## Test it with a real service

T.B.D.
