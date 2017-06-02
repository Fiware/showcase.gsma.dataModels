# UserActivity

## Description

This entity represents the current activity performed by an user. It can be used in different
scenarios, from modeling social activities on a web site (e.g. Federico shares the a picture of his dog) to real life activities (e.g. Federico drives his car to work). The model is largely inspired by
[https://www.w3.org/TR/activitystreams-core](https://www.w3.org/TR/activitystreams-core).

The model is represents users activities using the following predicate structure: `(Actor, Verb, Object*, Target*)`, where `Object` and `Target` are optional.

The `Actor` is identified by the attribute `refActor`, the `Verb` is identified by `refActivityType`, the `Object` is identified by `refObject`, and the `Target` is identified by `refTarget`. In generally it is assumed that the different part of the predicate are references to other NGSI entities, with the exception of the `Actor`. Within FIWARE, `refActor` could point to the end of the FIWARE Identity Manager, where FIWARE user profiles are stored.

## Data Model

A JSON Schema corresponding to this data model can be found [here](https://smartsdk.github.io/dataModels/User/UserActivity/schema.json).

+ `id` : Unique identifier.

+ `type` : Entity type. It must be equal to `UserActivity`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional  

+ `activityStart` : Activity's start timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Mandatory    

+ `activityEnd` : Activity's end timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `refActor` : Reference to the actor of the activity. Within FIWARE, `refActor` could point to the end of the FIWARE Identity Manager, where FIWARE user profiles are stored.
    + Attribute type: `string`
    + Mandatory

+ `refActivityType` : Reference to the type of activity
    + Attribute type: `string`
    + Mandatory

+ `refObject` : Reference to the object of the action
    + Attribute type: `string`
    + Optional

+ `refTarget` : Reference to the target of the action
    + Attribute type: `string`
    + Optional

## Examples of use

```
{
  "id": "UserActivity1",
  "type": "UserActivity",
  "refActivityType": "http://contextbroker:1026/v2/entities/Drive",
  "description": "User1 drive Car1 to Office1",
  "activityStart": "2016-11-30T07:00:00.00Z",
  "refObject": "http://contextbroker:1026/v2/entities/Car1",
  "refTarget": "http://contextbroker:1026/v2/entities/Office1",
  "refActor": "https://account.lab.fiware.org/users/1"
}
```

## Use it with a real service

The service is currently under development in the context of SmartSDK project.

## Open Issues

- [ ] Discuss if location should be included as part of the model. Consider that the model is referenced in UserContext, where user location is already modeled.
