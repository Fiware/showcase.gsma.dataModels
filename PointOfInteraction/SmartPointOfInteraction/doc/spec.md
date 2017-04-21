# SmartPointOfInteraction

## Description

A Smart Point of Interaction defines a place with technology to interact with citizens, for example, through Beacon technology from Apple, Eddystone/Physical-Web from Google or other proximity-based interfaces. Since the interactive area could be composed by more than one device providing the technology, this model represents a group of Smart Spot devices.

The data model includes information regarding the area/surface covered by the technology (i.e., the area covered by Bluetooth Low Energy-based Beacon or Eddystone), the schedule of the broadcasted information, links to the multimedia resources / Web Apps, etc. In addition, the data model may have a reference to another OMA NGSI entity such as a Parking, a Point of Interest (POI), etc. with enriched interaction provided by this technology.

This entity is purely virtual, is not a device mapping.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `SmartPointOfInteraction`.

+ `category` : Defines the type of interaction.
    + Attribute type: List of [Text](http://schema.org/Text)
    + Allowed values: `information`, `entertainment`, `infotainment` or `co-creation`.
    + Mandatory
    
+ `areaCovered` : Defines the area covered by the Smart Point of Interaction using geoJSON format.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Optional    
    
+ `applicationUrl` : This field specifies the real URL containing the solution or application (information, co-creation, etc) while the SmartSport 'announcedUrl' field specifies the broadcasted URL which could be this same URL or a shortened URL.
    + Attribute type: [URL](https://schema.org/URL)
    + Mandatory    

+ `availability`: Specifies the time intervals in which this service is available. This is a general service information while SmartSpots have their own availability in order to allow advanced configurations.
    + Attribute type: [openingHours](https://schema.org/openingHours)
    + Optional

+ `refRelatedEntity` : List of entities improved with this Smart Point of Interaction. The entity type could be any such as a “Parking”, “Point of Interest”, etc.
    + Attribute type: List of entities.
    + Optional    

+ `refSmartSpot` : References to the “Smart Spot” devices which are part of the Smart Point of Interaction.
    + Attribute type: Reference to one or more entity of type [SmartSpot](https://github.com/Fiware/dataModels/blob/master/SmartPointOfInteraction/SmartSpot/doc/spec.md)
    + Mandatory    

## Examples of use

```json
{
  "id": "SPOI-ES-4326",
  "type": "SmartPointOfInteraction",
  "category": ["Co-creation"],
  "areaCovered": {                           
    "type": "Polygon",
    "coordinates": [[
      [25.774, -80.190],
      [18.466, -66.118], 
      [32.321, -64.757], 
      [25.774, -80.190] 
    ]]
  },
  "applicationUrl": "www.siidi.eu",
  "availability": "Tu,Th 16:00-20:00",
  "refSmartSpot": [ "SSPOT-F94C58E29DD5", "SSPOT-F94C53E21DD2", "SSPOT-F94C51A295D9"]
}
```

## Use it with a real service

T.B.D.

## Open Issues

* Provide JSON Schema
