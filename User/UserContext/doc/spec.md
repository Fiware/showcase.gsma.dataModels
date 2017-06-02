# UserContext

## Description

This data model describe the Context of a User. No personal data is encoded in
the model. The actual User data are stored in a different end point, as identified
by the `refUser` property. Within FIWARE, this reference could point to the end of
the FIWARE Identity Manager, where FIWARE user profiles are stored.

## Data Model

A JSON Schema corresponding to this data model can be found [here](https://smartsdk.github.io/dataModels/User/UserContext/schema.json).

+ `id` : Unique identifier.

+ `type` : Entity type. It must be equal to `UserContext`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional    

+ `refUser` : reference to the actual User to which this UserContext is associated. Within FIWARE, this reference could point to the end of
the FIWARE Identity Manager, where FIWARE user profiles are stored.
    + Attribute type: `string`
    + Mandatory

+ `location` : Current location of the User represented by a GeoJSON geometry.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not defined.

+ `address` : Current civic address of the User
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present.

+ `refDevice` : An object representing the current device user by the User. See [Device](../../Device/Device/doc/spec.md) definition.
    + Attribute type: `string`
    + Optional

+ `refActivity` : An object representing the current activity performed by the User. See [UserActivity](../UserActivity/doc/spec.md) definition.
    + Attribute type: `string`
    + Optional

## Examples of use

```
{
  "id": "UserContext1",
  "type": "UserContext",
  "location": {
    "type": "Point",
    "coordinates": [
      -4.754444444,
      41.640833333
    ]
  },
  "refActivity": "http://contextbroker:1026/v2/entities/UserActivity1",
  "refDevice": "http://contextbroker:1026/v2/entities/Device1",
  "refUser": "https://account.lab.fiware.org/users/1"
}
```

## Use it with a real service

The service is currently under development in the context of SmartSDK project.

## Open Issues

- [ ] Evaluate additional properties
