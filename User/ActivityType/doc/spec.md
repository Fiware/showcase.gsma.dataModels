# ActivityType

## Description

This data model support the modeling of User's activity in a context aware application. The model definition is to be completed yet.

## Data Model

A JSON Schema corresponding to this data model can be found [here](https://smartsdk.github.io/dataModels/User/ActivityType/schema.json).

+ `id` : Unique identifier.

+ `type` : Entity type. It must be equal to `ActivityType`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

## Examples of use

```
{
  "id": "ActivityType1",
  "type": "ActivityType",
  "description": "ActivityType1 represents the action of driving. A person (the actor of the action) drive a car (the object action) to a destination (the target of the action)",
}

```

## Use it with a real service

The service is currently under development in the context of SmartSDK project.

## Open Issues

- [ ] Complete the model.
