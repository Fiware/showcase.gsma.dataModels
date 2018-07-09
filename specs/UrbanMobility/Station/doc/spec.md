# gtfs:Station

## Description

See [https://developers.google.com/transit/gtfs/reference/#stopstxt](https://developers.google.com/transit/gtfs/reference/#stopstxt)

It is a GTFS `stop` which `location_type` is equal to `1`.

## Data Model

+ `id`: Entity Id
    + It shall be `urn:ngsi-ld:gtfs:Station:<station_identifier>` being `station_identifier` a value that can derived from the `stop_id` field. 

+ `type`: Entity Type 
    + It shall be equal to `gtfs:Station`
 
+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.
  
+ `dateModified` : Last update timestamp of this Entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.
    
+ `hasStop` : It shall point to another Entity(ies) of type `gtfs:Stop`  
    + Type: Relationship. List of [gtfs:Stop](../../Stop/doc/spec.md). 
    + Mandatory
  
+ `hasAccessPoint` : It shall point to another Entity(ies) of type `gtfs:AccessPoint`  
    + Type: Relationship. List of [gtfs:AccessPoint](../../AccessPoint/doc/spec.md). 
    + Optional  
 
The specification for the following attributes is the one mandanted by [gtfs:Stop](../../Stop/doc/spec.md):

+ `name`
+ `code`
+ `page`
+ `description`
+ `location`
+ `wheelChairAccessible`
+ `zoneCode` 
+ `address`
+ `hasParentStation` 

### Example

```json
{
  "id": "urn:ngsi-ld:Station:Madrid:est_90_21",
  "type": "gtfs:Station",
  "code": "21",
  "name": "Intercambiador de Plaza de Castilla",
  "location": {
    "type": "Point",
    "coordinates": [-3.6892,40.4669]
  },
  "address": {
    "type": "PostalAddress",
    "streetAddress": "Paseo de la Castellana 189",
    "addressLocality": "Madrid",
    "addressCountry": "ES"
  },
  "hasStop": ["urn:ngsi-ld:gtfs:Stop:Madrid_par_4_1"]
}
```

## Summary of mappings to GTFS

### Properties

Same as [gtfs:Stop](../../Stop/doc/spec.md)

### Relationships

| GTFS Field            | NGSI Attribute      | LinkedGTFS           | Comment                                                       |
|:--------------------- |:--------------------|:---------------------|:--------------------------------------------------------------|
|                       | `hasStop`           |                      | shall point to Entities of type `gtfs:Stop`                   |
|                       | `hasAccessPoint`    |                      | shall point to Entities of type `gtfs:AccessPoint`            |
|                       | `hasParentStation`  |                      | shall point to an Entity of type `gtfs:Station`               |


## Open issues
