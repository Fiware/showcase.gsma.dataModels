# FlowerBed

## Description

 A garden plot in which flowers (or other plants) are grown.
 Usually you will find flower beds in parks, gardens, pedestrian areas or at big highway interchanges.
 
## Data Model

A JSON Schema corresponding to this data model can be found {{add link to JSON Schema}}

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `FlowerBed`. 

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.

+ `taxon` : Used to indicate the biological [taxon](http://en.wikipedia.org/wiki/en:taxon)
to which the trees, or plants in the flower bed belong.
    + Attribute type: List of [Text](https://schema.org/Text)
    + Optional
    
+ `category` : Category of this flower bed. 
    + Attribute type: List of [Text](https://schema.org/Text)
    + Allowed values: (`hedge`, `lawnArea`, `portable`, `urbanTreeSpot`) or any extended value needed by the application.
    + Optional
    
+ `width`. Width of this flower bed.
    + Attribute type: [Number](https://schema.org/Number).
    + Default Unit: Meters
    + See also: [https://schema.org/width](https://schema.org/width)
    + Optional 

+ `height`. Height of this flower bed. 
    + Attribute type: [Number](https://schema.org/Number).
    + Default Unit: Meters
    + See also: [https://schema.org/height](https://schema.org/height)
    + Optional 

+ `depth`. Depth of this flower bed.
    + Attribute type: [Number](https://schema.org/Number).
    + Default Unit: Meters
    + See also: [https://schema.org/depth](https://schema.org/depth)
    + Optional

+ `shape`. Shape of this flower bed.
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: One Of (`rectangular`, `square`, `elliptic`, `polygonal`, `circular`) or any other required by an application.
    + Optional

+ `location` : Location of the flower bed represented by a GeoJSON geometry. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not defined
    
+ `address` : Civic address of this flower bed.
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present.     

+ `dateLastWatering` : Timestamp which corresponds to the last watering of the flower bed.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `nextWateringDeadline` : Deadline for next watering operation.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional
    
+ `refGarden` : Flower bed's garden (if it belongs to any). 
    + Attribute type: Reference to an entity of type `Garden`
    + Optional
    
### Representing measurements related to a flower bed

 There are two options for representing measurements observed:

+ A/ Through a linked entity of type `GreenspaceRecord` (attribute named `refRecord`).
+ B/ Through a group of measurement properties already defined by [GreenspaceRecord](../../GreenspaceRecord/doc/spec.md). 

Below is the description of the attribute to be used for option A/. 
    
+ `refRecord` : List of records which contain measurements related to this flower bed.
    + Attribute type: List of references to entities of type `GreenspaceRecord`
    + Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).
    
## Examples of use

```json
{
  "id": "FlowerBed-345",
  "type": "FlowerBed",
  "category": ["urbanTreeSpot"],
  "dateLastWatering": "2017-03-31T08:00",
  "address": {
    "streetAddress": "Paseo Zorrilla, 122",
    "adressLocality": "Valladolid",
    "addressCountry": "Spain"
  },
  "soilTemperature": 17,
  "soilMoistureVwc": 0.85
}
```
    
## Use it with a real service


## Open Issues

