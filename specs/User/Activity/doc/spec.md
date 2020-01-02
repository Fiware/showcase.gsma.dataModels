# Activity

## Description

This entity represents the current activity performed by a User. It can be used
in different scenarios, from modeling social activities on a site (e.g. Federico
shares a picture of his dog) to real life activities (e.g. Federico drives his
car to work). The model is largely inspired by
[https://www.w3.org/TR/activitystreams-core](https://www.w3.org/TR/activitystreams-core).

The model represents user activities using the following predicate structure:
`(Agent, Verb, Object*, Target*)`, where `Object` and `Target` are optional.

The `Agent` is identified by the attribute `refAgent`, the `Verb` is identified
by `activityType`, the `Object` is identified by `refObject`, and the `Target`
is identified by `refTarget`.

## Data Model

A JSON Schema corresponding to this data model can be found
[here](https://fiware.github.io/data-models/specs/User/Activity/schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `UserActivity`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateActivityStarted` : Activity's start timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Mandatory

-   `dateActivityEnded` : Activity's end timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional

-   `refAgent` : Reference to the agent (i.e. a person) performing the activity.
    It may be another NGSI Entity or any `Agent` identified by an URI.

    -   Attribute type: Relationship. Reference to an Entity or
        [https://schema.org/URL](https://schema.org/URL).
    -   Mandatory

-   `activityType` : The action performed (e.g. Drive).

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References:
        [https://schema.org/Action](https://schema.org/Action),
        [https://www.w3.org/TR/activitystreams-vocabulary/#activity-types](https://www.w3.org/TR/activitystreams-vocabulary/#activity-types),
        [https://health-lifesci.schema.org/PhysicalActivityCategory](https://health-lifesci.schema.org/PhysicalActivityCategory)
    -   Mandatory

-   `refObject` : Reference to the object of the action (e.g. Car1). It may be
    another NGSI Entity or any `Object` identified by an URI.

    -   Attribute type: Relationship. Reference to an Entity or
        [https://schema.org/URL](https://schema.org/URL).
    -   Optional

-   `refTarget` : Reference to the target of the action (e.g. Office1).
    -   Attribute type: Relationship. Reference to an Entity or
        [https://schema.org/URL](https://schema.org/URL).
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "UserActivity1",
    "type": "UserActivity",
    "description": {
        "value": "User1 drive Car1 to Office1"
    },
    "refTarget": {
        "type": "Relationship",
        "value": "Office1"
    },
    "activityType": {
        "value": "Drive"
    },
    "dateActivityStarted": {
        "type": "DateTime",
        "value": "2016-11-30T07:00:00.00Z"
    },
    "refAgent": {
        "type": "Relationship",
        "value": "User1"
    },
    "refObject": {
        "type": "Relationship",
        "value": "Car1"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "UserActivity1",
    "type": "UserActivity",
    "activityType": "Drive",
    "description": "User1 drive Car1 to Office1",
    "dateActivityStarted": "2016-11-30T07:00:00.00Z",
    "refObject": "Car1",
    "refTarget": "Office1",
    "refAgent": "User1"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:UserActivity:UserActivity1",
    "type": "UserActivity",
    "description": {
        "type": "Property",
        "value": "User1 drive Car1 to Office1"
    },
    "refTarget": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Target:Office1"
    },
    "activityType": {
        "type": "Property",
        "value": "Drive"
    },
    "dateActivityStarted": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-11-30T07:00:00.00Z"
        }
    },
    "refAgent": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Agent:User1"
    },
    "refObject": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Object:Car1"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Use it with a real service

T.B.D.

## Open Issues

-   [ ] Discuss if location should be included as part of the model. Consider
        that the model is referenced in UserContext, where user location is
        already modelled.
