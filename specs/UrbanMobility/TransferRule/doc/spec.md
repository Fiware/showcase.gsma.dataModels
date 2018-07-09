# gtfs:TransferRule

## Description

See [https://developers.google.com/transit/gtfs/reference/#transferstxt](https://developers.google.com/transit/gtfs/reference/#transferstxt)

## Data Model

+ `id`: Entity id. 
    + It shall be `urn:ngsi-ld:gtfs:TransferRule:<transfer_rule_identifier>`. 

+ `type`: Entity type. 
    + It shall be equal to `gtfs:Transfer`.
    
+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated. 
 
+ `dateModified` : Last update timestamp of this Entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.
  
+ `name` : Name given to this transfer rule.
    + Attribute type: Property. [Text](https://schema.org/Text)
    + Optional

+ `description`: Description given to this transfer rule.
    + Attribute type: Property. [Text](https://schema.org/Text)
    + Optional
  
+ `hasOrigin`: Trip associated to this Entity.
    + Attribute type: Relationship. It shall point to an Entity of Type [gtfs:Stop](../../Stop/spec.md) or [gtfs:Station](../../Station/spec.md)
    + Mandatory
  
+ `hasDestination`: Trip associated to this Entity.
    + Attribute type: Relationship. It shall point to an Entity of Type [gtfs:Stop](../../Stop/spec.md) or [gtfs:Station](../../Station/spec.md)
    + Mandatory
  
+ `transferType`: Same as GTFS `transfer_type`.
    + Attribute type: Property. [Text](https://schema.org/Text).
    + Allowed values: (`"0"`,`"1"`,`"2"`,`"3"`)
    + Mandatory
    
+ `minimumTransferTime`: Same as GTFS `min_transfer_time`. 
    + Attribute type: Property. [Integer](https://schema.org/Integer).
    + Default unit: seconds
    + Optional   
        
### Example

```json
{
  "id": "urn:ngsi-ld:gtfs:TransferRule:Malaga:Linea1_Linea5",
  "type": "gtfs:TransferRule",
  "name": "L1_L5",
  "hasOrigin": "urn:ngsi-ld:gtfs:Stop:Malaga_101",
  "hasDestination": "urn:ngsi-ld:gtfs:Stop:Malaga_508",
  "transferType": "0",
  "minimumTransferTime": 10
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field              | NGSI Attribute      | LinkedGTFS                 | Comment                                                      |
|:----------------------- |:--------------------|:-------------------------- |:-------------------------------------------------------------|
| `transfer_type`         | `transferType`      | `gtfs:transferType`        |                                                              |
| `minimumTransferTime`   | `min_tranfer_time`  | `gtfs:minimumTransferTime` |                                                              |
|                         | `name`              | `schema:name`              |                                                              |
|                         | `description`       | `schema:description`       |                                                              |
   

### Relationships

| GTFS Field              | NGSI Attribute        | LinkedGTFS              | Comment                                                           |
|:----------------------- |:----------------------|:----------------------- |:------------------------------------------------------------------|
| `from_stop_id`          | `hasOrigin`           | `gtfs:originStop`       | It shall point to an Entity of Type `gtfs:Stop` or `gtfs:Station` |
| `to_stop_id`            | `hasDestination`      | `gtfs:destinationStop`  | It shall point to an Entity of Type `gtfs:Stop` or `gtfs:Station` |


### Open issues

