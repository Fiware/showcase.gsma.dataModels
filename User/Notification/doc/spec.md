# Notification

## Description

This data model represents user generated notifications. This model can be used
in different scenarios. For example in Smart Mobility scenarios to provide a Traffic Alert,
or in Smart Security scenarios to report suspicious activities.

## Data Model

A JSON Schema corresponding to this data model can be found [here](https://smartsdk.github.io/dataModels/User/Notification/schema.json).

+ `id` : Unique identifier.

+ `type` : Entity type. It must be equal to  `Notification`.

+ `description` : Describe the occurred event.
    + Attribute type: `string`
    + Optional

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `eventObserved` : The date and time of this user event in ISO8601 UTC format. It can be represented by an specific time instant or by an ISO8601 interval.
	+ Attribute type: DateTime or an ISO8601 interval represented as Text.
	+ Mandatory    

+ `location` : Location of `Notification` represented by a GeoJSON geometry.
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not defined.

+ `address` : Civic address of `Notification`
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present.

+ `severity` : Describe the severity of `Notification` (0 = None, 1 = Low, 2 = Medium, 3 = High)
    + Attribute type: `integer`
    + Optional

+ `eventType` : Define the type of event described in the `Notification` (e.g. TrafficJam, DiseaseEpisode, CarAccident, ObservedWeather)
    + Attribute type: `string`
    + Mandatory

+ `refEvent` : Provide an external reference to the event providing more details.
    + Attribute type: `string`
    + Optional

+ `refUser` : reference to the actual User to which this UserContext is associated. Within FIWARE, this reference could point to the end of
the FIWARE Identity Manager, where FIWARE user profiles are stored.
    + Attribute type: `string`
    + Mandatory

## Examples of use

```
{
  "id": "Notification:1",
  "type": "Notification",
  "eventType": "TrafficJam",
  "location": {
    "type": "Point",
    "coordinates": [-3.712247222222222, 40.423852777777775]
  },
  "eventObserved": "2017-01-02T09:25:55.00Z",
  "severity": 3,
  "description": "Traffic Jam in Malibu street",
  "refUser": "https://account.lab.fiware.org/users/1"
}  
```

## Use it with a real service

The service is currently under development in the context of SmartSDK project.

## Open Issues

- [ ] Validate the model
- [ ] Look for related references (e.g. Waze APIs)
