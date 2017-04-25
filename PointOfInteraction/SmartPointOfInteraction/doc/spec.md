# SmartPointOfInteraction

## Description

A Smart Point of Interaction defines a place with technology to interact with users, for example, through Beacon technology from Apple, Eddystone/Physical-Web from Google or other proximity-based interfaces. Since the interactive area could be composed by more than one device providing the technology, this model encompasses a group of SmartSpot devices.

The data model includes information regarding the area/surface covered by the technology (i.e., the area covered by Bluetooth Low Energy-based Beacon), a way to specify the functionality intervals (i.e. when interactive points are available) and the link to the multimedia resource where users will interact (i.e. Web Apps, etc.). Additionally, the data model may reference to another NGSI entity such as a Parking, a Point of Interest (POI), etc. with enriched interaction provided by this Smart Point of Interest.


This entity is purely virtual, is not a device mapping.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `SmartPointOfInteraction`.

+ `category` : Defines the type of interaction.
    + Attribute type: List of [Text](http://schema.org/Text)
    + Allowed values: `information`, `entertainment`, `infotainment`, `co-creation` or any other extended value defined by the application.
    + Mandatory
    
+ `areaCovered` : Defines the area covered by the Smart Point of Interaction using geoJSON format.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Optional    
    
+ `applicationUrl` : This field specifies the real URL containing the solution or application (information, co-creation, etc) while the SmartSport 'announcedUrl' field specifies the broadcasted URL which could be this same URL or a shortened one.
    + Attribute type: [URL](https://schema.org/URL)
    + Mandatory    

+ `availability`: Specifies the time intervals in which this interactive service is available, but this is a general information while Smart Spots have their own real availability in order to allow advanced configurations. The format is an structured value which must contain a subproperty per each required functionality interval, indicating when the functionality is active. If nothing specified (or null) it will mean that the functionality is always on. The syntax must be conformant with schema.org [openingHours specification](https://schema.org/openingHours). For instance, a service which is only active on dayweeks will be encoded as "availability": "Mo,Tu,We,Th,Fr,Sa 09:00-20:00". 
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue)
    + Mandatory. It can be null.

+ `refRelatedEntity` : List of entities improved with this Smart Point of Interaction. The entity type could be any such as a “Parking”, “Point of Interest”, etc.
    + Attribute type: List of entities.
    + Optional    

+ `refSmartSpot` : References to the “Smart Spot” devices which are part of the Smart Point of Interaction.
    + Attribute type: Reference to one or more entity of type [SmartSpot](https://github.com/Fiware/dataModels/blob/master/SmartPointOfInteraction/SmartSpot/doc/spec.md)
    + Optional    

## Examples of use

```json
{
  "id": "SPOI-ES-4326",
  "type": "SmartPointOfInteraction",
  "category": ["co-creation"],
  "areaCovered": {                           
    "type": "Polygon",
    "coordinates": [[
      [25.774, -80.190],
      [18.466, -66.118], 
      [32.321, -64.757], 
      [25.774, -80.190] 
    ]]
  },
  "applicationUrl": "https://www.fiware.org",
  "availability": "Tu,Th 16:00-20:00",
  "refRelatedEntity": "POI-PlazaCazorla-3123",
  "refSmartSpot": [ "SSPOT-F94C58E29DD5", "SSPOT-F94C53E21DD2", "SSPOT-F94C51A295D9"]
}
```

## Use it with a real service

T.B.D.

## Open Issues

* Provide JSON Schema
