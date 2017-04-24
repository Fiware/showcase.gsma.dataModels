# SmartSpot

## Description

Smart Spots are devices which provide the the technology which allows users to get access to smart points of interaction so that they can obtain extra information (infotainment, …), provide suggestions (suggestions mailbox, …) or generate new content (co-creation, …). The data model contains resources to configure the interaction service such as the broadcasted URL (typically shortened), the interval between broadcasts (frequency), the availability of the service, transmission power depending on the area to be covered, etc.

In addition to the presented data model, this entity inherits the Device data model. This means that by hierarchy, the `SmartSpot` entity type is a subtype of `[Device](https://github.com/Fiware/dataModels/blob/master/Device/Device/doc/spec.md)` and as a result it can be the subject of any of the properties that an entity of type `[Device](https://github.com/Fiware/dataModels/blob/master/Device/Device/doc/spec.md)` may have.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `SmartSpot`.

+ `announcedUrl` : URL broadcasted by the device.
    + Attribute type: [URL](https://schema.org/URL)
    + Mandatory    

+ `signalStrenght` : Signal strength to adjust the announcement range.
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: "lowest", "medium" or "highest". 
    + Mandatory    

+ `bluetoothChannel` : Bluetooth channels where to transmit the announcement.
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: "37", "38", "39", "37,38", "38,39", "37,39" or "37,38,39".
    + Mandatory  

+ `areaCovered` : Radius of the spot coverage area in meters.
    + Attribute Type: [Number](https://schema.org/Number)
	+ Default unit: Meters.
    + Optional      

+ `announcementPeriod` : Interval between announcements.
    + Attribute Type: [Number](https://schema.org/Number)
	+ Default unit: Milliseconds.
    + Mandatory     

+ `availability`: Specifies the functionality intervals in which the announcements will be sent. The format is an structured value which must contain a subproperty per each required functionality interval, indicating when the functionality is active. If nothing specified (or null) it will mean that the functionality is always on. The syntax must be conformant with schema.org [openingHours specification](https://schema.org/openingHours). For instance, a service which is only active on dayweeks will be encoded as "availability": "Mo,Tu,We,Th,Fr,Sa 09:00-20:00". 
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue)
    + Mandatory. It can be null.

+ `refSmartPointOfInteraction` : Reference to the Smart Point of Interaction which includes this Smart Spot.
    + Attribute type: Reference to an entity of type [SmartPointOfInteraction](https://github.com/Fiware/dataModels/blob/master/SmartPointOfInteraction/SmartPointOfInteraction/doc/spec.md)
    + Optional

## Examples of use

```json
{
  "id": "SSPOT-F94C51A295D9",
  "type": "SmartSpot",
  "announcedUrl" : "https://hpoi.info/325531235437",
  "signalStrenght": "high",
  "bluetoothChannel": "37-38-39",
  "areaCovered": 30,
  "announcementPeriod": 500,
  "availability": "Tu,Th 16:00-20:00",
  "refSmartPointOfInteraction": "SPOI-ES-4326"
}
```
    
## Use it with a real service

T.B.D.

## Open Issues

* Provide JSON Schema

