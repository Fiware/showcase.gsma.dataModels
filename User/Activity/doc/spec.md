# Activity

## Description

This entity represents the current activity performed by an user. It can be used in different
scenarios, from modeling social activities on a web site (e.g. Federico shares a picture of his dog) to real life activities (e.g. Federico drives his car to work). The model is largely inspired by
[https://www.w3.org/TR/activitystreams-core](https://www.w3.org/TR/activitystreams-core).

The model is represents users activities using the following predicate structure: `(Actor, Verb, Object*, Target*)`, where `Object` and `Target` are optional.

The `Actor` is identified by the attribute `refActor`, the `Verb` is identified by `activityType`, the `Object` is identified by `refObject`, and the `Target` is identified by `refTarget`. In generally it is assumed that the different part of the predicate are references to other NGSI entities, with the exception of the `Actor`.

## Data Model

A JSON Schema corresponding to this data model can be found [here](https://fiware.github.io/dataModels/User/UserActivity/schema.json).

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

+ `refActor` : Reference to the actor of the activity.
    + Attribute type: [https://schema.org/URL](https://schema.org/URL)
    + Normative References: [https://tools.ietf.org/html/rfc3986](https://tools.ietf.org/html/rfc3986)
    + Mandatory

+ `activityType` : The action performed (e.g. Drive)
    + Attribute type: `string`
    + Normative References: [https://schema.org/Action](https://schema.org/Action), [https://www.w3.org/TR/activitystreams-vocabulary/#activity-types](https://www.w3.org/TR/activitystreams-vocabulary/#activity-types), [https://health-lifesci.schema.org/PhysicalActivity](https://health-lifesci.schema.org/PhysicalActivity)
    + Mandatory

+ `refObject` : Reference to the object of the action
    + Attribute type: `string` or [https://schema.org/URL](https://schema.org/URL)
    + Normative References: [http://schema.org/Thing](http://schema.org/Thing)
    + Optional

+ `refTarget` : Reference to the target of the action.
    + Attribute type: `string` or [https://schema.org/URL](https://schema.org/URL)
    + Normative References: [http://schema.org/Thing](http://schema.org/Thing)
    + Optional

## Examples of use

```
{
  "id": "UserActivity1",
  "type": "UserActivity",
  "activityType": "Drive",
  "description": "User1 drive Car1 to Office1",
  "activityStart": "2016-11-30T07:00:00.00Z",
  "refObject": "Car1",
  "refTarget": "Office1",
  "refActor": "UserId1"
}
```

## Use it with a real service

T.B.D.

## Open Issues

- [ ] Discuss if location should be included as part of the model. Consider that the model is referenced in UserContext, where user location is already modelled.
