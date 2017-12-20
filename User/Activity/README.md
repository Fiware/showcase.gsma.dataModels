# UserActivity

This entity represents the current activity performed by an user. It can be used in different
scenarios, from modelling social activities on a web site (e.g. Federico shares the a picture of his dog) to real life activities (e.g. Federico drives his car to work). The model is largely inspired by
[https://www.w3.org/TR/activitystreams-core](https://www.w3.org/TR/activitystreams-core).

The model is represents users activities using the following predicate structure: `(Actor, Verb, Object*, Target*)`, where `Object` and `Target` are optional.

The `Actor` is identified by the attribute `refActor`, the `Verb` is identified by `refActivityType`, the `Object` is identified by `refObject`, and the `Target` is identified by `refTarget`. In generally it is assumed that the different part of the predicate are references to other NGSI entities, with the exception of the `Actor`.

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
