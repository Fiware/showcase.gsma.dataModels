# Itinerary

## Description

An itinerary scheduled for a time period, it can be for just one day (by setting start and end dates) or fixed for the entire life. 

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `VehicleItinerary`. 

+ `name` : Name given to the itinerary
    + Normative References: [https://schema.org/name](https://schema.org/name)
    + Optional

+ `description` : Description about the itinerary. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

+ `refRoute`: Route this itinerary belongs to.
    + Attribute type: Reference to a [Route](../../Route/doc/spec.md)
    + Mandatory

+ `refSegments`: ItinerarySegments that compose to this itinerary
    + Attribute type: List of references to a [ItinerarySegment](../../ItinerarySegment/doc/spec.md)
    + Mandatory

+ `vehicleType`: Type of vehicle from the point of view of its structural characteristics.
    + See definition at [Vehicle](../../Vehicle/doc/spec.md).
    + Mandatory

+ `startDate` : When the itinerary weeekdays start.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `endDate` : When the itinerary weekdays end.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `weekdays` : The weekdays that this trip is scheduled to be performed.
    + Attribute type: List of [Text](http://schema.org/Text)
    + Allowed values (Informative):
        + `monday'
        + `tuesday`
        + `wednesday`
        + `thursday`
        + `friday`
        + `saturday`
        + 'sunday`
    + Optional

+ `scheduledPath` : Itinerary's scheduled path geometry represented by a GeoJSON LineString. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Optional

## Example

    {
      "id": "itinerary:89237",
      "type": "Itinerary",
      "name": "B25-8:10",
      "description": "Bus line 25 from Metro Tacubaya to La Valenciana, itinerary departing at 08:10",
      "refRoute" : "route:194",
      "refSegments": ["itinerarysegment:89237","itinerarysegment:89238","itinerarysegment:89239","itinerarysegment:89240","itinerarysegment:89241"],
    }
    
## Test it with a real service

T.B.D.
