# gtfs:Frequency

## Description

See [https://developers.google.com/transit/gtfs/reference/#frequenciestxt](https://developers.google.com/transit/gtfs/reference/#frequenciestxt)

## Data Model

+ `id`: Entity id. 
    + It shall be `urn:ngsi-ld:gtfs:Frequency:<frequency_identifier>`. 

+ `type`: Entity type. 
    + It shall be equal to `gtfs:Frequency`.
    
+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated. 
 
+ `dateModified` : Last update timestamp of this Entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.
  
+ `name` : Name given to this frequency.
    + Attribute type: Property. [Text](https://schema.org/Text)
    + Optional

+ `description`: Description given to this frequency.
    + Attribute type: Property. [Text](https://schema.org/Text)
    + Optional
  
+ `hasTrip`: Trip associated to this Entity.
    + Attribute type: Relationship. It shall point to an Entity of Type [gtfs:Trip](../../Trip/doc/spec.md)
    + Mandatory

+ `startTime`: Same as GTFS `start_time`. See [format](https://developers.google.com/transit/gtfs/reference/#frequenciestxt).
    + Attribute type: Property. [Text](https://schema.org/Text).
    + Mandatory
    
+ `endTime`: Same as GTFS `end_time`. See [format](https://developers.google.com/transit/gtfs/reference/#frequenciestxt).
    + Attribute type: Property. [Text](https://schema.org/Text).
    + Mandatory   
    
+ `headwaySeconds`: Same as GTFS `headway_secs`.
    + Attribute type: Property. [Integer](https://schema.org/Integer).
    + Mandatory
    
+ `exactTimes`: Same as GTFS `exact_times` but encoded as a Boolean:
`false`: Frequency-based trips are not exactly scheduled.
`true`: Frequency-based trips are exactly scheduled.
    + Attribute type: Property. [Boolean](https://schema.org/Boolean). 
    + Optional
    
### Example

```json
{
  "id": "urn:ngsi-ld:gtfs:Frequency:Malaga:Linea1",
  "type": "gtfs:Frequency",
  "name": "Laborables",
  "description": "Cada 10 minutos",
  "hasTrip": "urn:ngsi-ld:gtfs:Trip:Spain:Malaga:1",
  "startTime": "07:00",
  "endTime": "10:00",
  "headwaySeconds": 600
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field              | NGSI Attribute      | LinkedGTFS            | Comment                                                      |
|:----------------------- |:--------------------|:--------------------- |:-------------------------------------------------------------|
| `start_time`            | `startTime`         | `gtfs:startTime`      |                                                              |
| `end_time`              | `endTime`           | `gtfs:endTime`        |                                                              |
| `headway_secs`          | `headwaySeconds`    | `gtfs:headwaySeconds` |                                                              |
| `exact_times`           | `exactTimes`        | `gtfs:exactTimes`     |                                                              |
|                         | `name`              | `schema:name`         |                                                              |
|                         | `description`       | `schema:description`  |                                                              |
   

### Relationships

| GTFS Field              | NGSI Attribute        | LinkedGTFS           | Comment                                                |
|:----------------------- |:----------------------|:-------------------- |:-------------------------------------------------------|
| `trip_id`               | `hasTrip`             |                      | It shall point to an Entity of Type `gtfs:Trip`        |


### Open issues

