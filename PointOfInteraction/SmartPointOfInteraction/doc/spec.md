# SmartPointOfInteraction

## Description

A Smart Point of Interaction defines a place with technology to interact with the citizens, for example, through Beacon technology from Apple, Eddystone/Physical-Web from Google or other proximity-based interfaces. Since the interactive area could be composed by more than one device providing the technology, this model represents a group of Smart Spot devices.

In details, the data model resources include information regarding the area/surface covered by the technology (i.e., the area covered by Bluetooth Low Energy-based Beacon or Eddystone), the schedule of the broadcasted information, links to the multimedia resources / Web Apps etc. In addition, the data model may have a reference to another OMA NGSI entity such as a Parking, a Point of Interest (POI), ... which will be improved with this technology to interact.

This entity is purely virtual, is not a device mapping.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `SmartPointOfInteraction`.

+ `category` : Defines the type of interaction.
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: "Information", "Entertainment", "Infotainment" or "Co-creation".
    + Mandatory
    
+ `area` : Define the area covered by the Smart Point of Interaction using geoJSON format.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Optional    
    
+ `url` : Final URL announced by the spots. This is the real URL containing the solution/application.
    + Attribute type: [Text](https://schema.org/Text)
    + Mandatory    

+ `refLocationNGSIEntity` : List of entities improved with this Smart Point of Interaction. They could be any entity type such as a “Parking”, “Point of Interest”, ...
    + Attribute type: List of entities.
    + Optional    

+ `refSmartSpot` : References to the “Smart Spot” devices which are part of the Smart Point of Interaction.
    + Attribute type: Reference to an entity of type [SmartSpot](https://github.com/HOP-Ubiquitous/dataModels/blob/feature/smartpoi/PointOfInteraction/SmartSpot/doc/spec.md)
    + Mandatory    

## Examples of use

```json
{
"id": "SPOI-ES-4326",
"category": "SmartPointOfInteraction",
"type": "Co-creation",
"area": {                           
  "type": "Polygon",
  "coordinates": [[
    [25.774, -80.190],
    [18.466, -66.118], 
    [32.321, -64.757], 
    [25.774, -80.190] 
  ]]
},
"url": "www.siidi.eu",
"refSmartSpot": [ "SSPOT-F94C58E29DD5", "SSPOT-F94C53E21DD2", "SSPOT-F94C51A295D9"]
}
```

## Use it with a real service

T.B.D.

## Open Issues

* Provide JSON Schema

* It's interesting define the "availability" field where to set the intervals where the announcements will be sent, but this should be studied and defined carefully. 

  * ISO8601 contemplates recurring time intervals but seems it is not enought to represent "each monday from 10:00 to 11:00".
    * An "ugly" solution could be introduce several fields such as "MondayAvailability", "TuesdayAvailability" where to set simple time intervals: ``` "MondayAvailability": [ "T09:00:00Z/T14:00:00Z", "T15:00:00Z/T19:00:00Z" ], ```

  * RFC2445 could be a solution but introduce or write a parser is maybe too heavy for embedded programming.
