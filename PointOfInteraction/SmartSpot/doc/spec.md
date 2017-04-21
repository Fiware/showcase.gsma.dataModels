# SmartSpot

## Description

Smart Spots are devices which provide the technology to allow users to interact (suggestions mailbox, co-creation, …) or to obtain extra information (tourism, infotainment, …). The data model contains resources to configure the interaction service such as the broadcasted URL (probably will be a shortened url), the interval between broadcasts (frequency), the availability of the service, transmission power in function of the area to cover, etc.

These resources (except the references to other entities) are mapped from a real device. For that reason, the changes in any of the values of this entity will modify the value in the real device.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `SmartSpot`.

+ `physicalURL` : Physical URL broadcasted by the device.
    + Attribute type: [URL](https://schema.org/URL)
    + Mandatory    

+ `signalStrenght` : Signal strength to adjust the announcement range.
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: "lowest", "medium" or "highest". 
    + Optional    

+ `bluetoothChannel` : Bluetooth channels where to transmit the announcement.
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: "37", "38", "39", "37-38", "38-39", "37-39" or "37-38-39".
    + Optional  

+ `areaRadius` : Spot coverage area in meters.
    + Attribute Type: [Number](https://schema.org/Number)
    + Mandatory      

+ `announcementInterval` : Interval in milliseconds between announcements.
    + Attribute Type: [Number](https://schema.org/Number)
    + Optional      

+ `refSmartPointOfInteraction` : Reference to the Smart Point of Interaction which includes this Smart Spot.
    + Attribute type: Reference to an entity of type [SmartPointOfInteraction](https://github.com/Fiware/dataModels/blob/master/SmartPointOfInteraction/SmartPointOfInteraction/doc/spec.md)
    + Optional

+ `refDevice` : A reference to the device(s) which is providing this interative area.
    + Attribute type: Reference to an entity of type `Device`
    + Optional    

## Examples of use

```json
{
  "id": "SSPOT-F94C51A295D9",
  "type": "SmartSpot",
  "physicalUrl" : "https://hpoi.info/325531235437",
  "signalStrenght": "high",
  "bluetoothChannel": "37-38-39",
  "areaRadius": 30,
  "announcementInterval": 500,
  "refSmartPointOfInteraction": "SPOI-ES-4326",
  "refDevice": "Device-ES-09aab934a8"
}
```
    
## Use it with a real service

T.B.D.

## Open Issues

* Include "location" field? Currently not inserted since it could be obtained from "Device" data model.

* Provide JSON Schema

* It could be interesting define the "availability" field where to set the intervals where the announcements will be sent, but this should be studied and defined carefully. 

  * ISO8601 contemplates recurring time intervals but seems it is not enought to represent "each monday from 10:00 to 11:00".
    * An "ugly" solution could be introduce several fields such as "MondayAvailability", "TuesdayAvailability" where to set simple time intervals: ``` "MondayAvailability": [ "T09:00:00Z/T14:00:00Z", "T15:00:00Z/T19:00:00Z" ], ```

  * RFC2445 could be a solution but introduce or write a parser is maybe too heavy for embedded programming.
