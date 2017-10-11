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

- `refRoute`: Route this itinerary belongs to.
    + Attribute type: Reference to a [Route](../../Route/doc/spec.md)
    + Mandatory

+ `startDate` : When the itinerary weeekdays start.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `endDate` : When the itinerary weekdays end.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `weekdays` : The weekdays that this trip refers to.
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
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

+ `performedPath` : Performed path of the vehicle, to be updated while vehicle is travelling. A geometry represented by a GeoJSON LineString. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

## Example

    {
      "id": "itinerary:89237",
      "type": "Itinerary",
      "name": "Itinerary 12",
      "description": "Bus Itinerary for 2017-09-22",
      "segeemnts": [
            { "id": "wastecontainer:27" , "type": "WasteContainer" , "dateScheduled" : "2017-09-22T15:05:59.408Z" },
            { "id": "wastecontainer:92" , "type": "WasteContainer" , "dateScheduled" : "2017-09-22T15:09:23.788Z" },
            ],
      "refAssignedVehicle" : "vehicle-512"
    }
    
## Test it with a real service

T.B.D.
