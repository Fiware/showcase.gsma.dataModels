# UserActivity

This entity represents the current activity performed by an user. It can be used in different
scenarios, from modeling social activities on a web site (e.g. Federico shares the a picture of his dog) to real life activities (e.g. Federico drives his car to work). The model is largely inspired by
[https://www.w3.org/TR/activitystreams-core](https://www.w3.org/TR/activitystreams-core).

The model is represents users activities using the following predicate structure: `(Actor, Verb, Object*, Target*)`, where `Object` and `Target` are optional.

The `Actor` is identified by the attribute `refActor`, the `Verb` is identified by `refActivityType`, the `Object` is identified by `refObject`, and the `Target` is identified by `refTarget`. In generally it is assumed that the different part of the predicate are references to other NGSI entities, with the exception of the `Actor`. Within FIWARE, `refActor` could point to the end of the FIWARE Identity Manager, where FIWARE user profiles are stored.

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
