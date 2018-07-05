# SmartSpot

## Description

Smart Spots are devices which provide the technology which allows users to get access to smart points of interaction so that they can obtain extra information (infotainment, etc.), provide suggestions (suggestions mailbox, etc.) or generate new content (co-creation, etc.). The data model contains resources to configure the interaction service such as the broadcasted URL (typically shortened), the period between broadcasts, the availability of the service, transmission power depending on the area to be covered, etc.

In addition to the presented data model, this entity type inherits from the [Device](../../../Device/Device/doc/spec.md) entity type. This means that by hierarchy, the `SmartSpot` entity type is a subtype of [Device](../../../Device/Device/doc/spec.md) and as a result it can be the subject of any of the properties that an entity of type [Device](../../../Device/Device/doc/spec.md) may have.

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

+ `coverageRadius` : Radius of the spot coverage area in meters.
    + Attribute Type: [Number](https://schema.org/Number)
	+ Default unit: Meters.
    + Optional      

+ `announcementPeriod` : Period between announcements.
    + Attribute Type: [Number](https://schema.org/Number)
	+ Default unit: Milliseconds.
    + Mandatory     

+ `availability`: Specifies the functionality intervals in which the announcements will be sent. The syntax must be conformant with schema.org [openingHours specification](https://schema.org/openingHours). For instance, a service which is only active on dayweeks will be encoded as "availability": "Mo,Tu,We,Th,Fr,Sa 09:00-20:00". 
    + Attribute type: [Text](https://schema.org/Text)
    + Mandatory. It can be `null`.

+ `refSmartPointOfInteraction` : Reference to the Smart Point of Interaction which includes this Smart Spot.
    + Attribute type: Reference to an entity of type [SmartPointOfInteraction](../../SmartPointOfInteraction/doc/spec.md)
    + Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

```json
{
  "id": "SSPOT-F94C51A295D9",
  "type": "SmartSpot",
  "announcedUrl" : "http://goo.gl/EJ81JP",
  "signalStrenght": "high",
  "bluetoothChannel": "37-38-39",
  "coverageRadius": 30,
  "announcementPeriod": 500,
  "availability": "Tu,Th 16:00-20:00",
  "refSmartPointOfInteraction": "SPOI-ES-4326"
}
```
    
## Use it with a real service

T.B.D.
