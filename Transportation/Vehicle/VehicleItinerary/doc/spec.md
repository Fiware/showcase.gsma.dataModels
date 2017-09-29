# VehicleItinerary

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

+ `stops` : List of ordered stops the itinerary has to do at entities. It will contain its id, entity type and an optional scheduled date.
    + Attribute type: Type [ItemList](https://schema.org/ItemList).
        + Subproperties:
            + `entityType` : List of Entity types
                + Type: [Text](http://schema.org/Text)
            + `id` : Id of the entity
                + Type: [Text](http://schema.org/Text)
            + `scheduledArrival` : DateTime of arrival
                + Type: [DateTime](http://schema.org/DateTime)
            + `scheduledDeparture` : DateTime of departure
                + Type: [DateTime](http://schema.org/DateTime)
    + Mandatory
 
+  `refAssignedVehicle` : Vehicle assigned to this itinerary.
    + Attribute type: Reference to a [Vehicle](../../../Transportation/Vehicle/doc/spec.md) entity.
    + Optional


## Example

    {
      "id": "vehicleitinerary:89237",
      "type": "VehicleItinerary",
      "name": "VehicleItinerary 12",
      "description": "Bus Vehicle Itinerary for 2017-09-22",
      "stops": [
            { "id": "wastecontainer:27" , "type": "WasteContainer" , "dateScheduled" : "2017-09-22T15:05:59.408Z" },
            { "id": "wastecontainer:92" , "type": "WasteContainer" , "dateScheduled" : "2017-09-22T15:09:23.788Z" },
            ],
      "refAssignedVehicle" : "vehicle-512"
    }
    
## Test it with a real service

T.B.D.
