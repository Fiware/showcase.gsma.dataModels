# Open 311 Service Type

As per [Open311](http://wiki.open311.org/GeoReport_v2/#get-service-list) an
entity of type `ServiceType` is an acceptable 311 service request type. A
request type can be unique to the city/jurisdiction.

_Please note that this data model has not been harmonized as per FIWARE/OASC
style. We have decided to keep the same property names and structure, although
we strongly believe the Open311 model can be leveraged._

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier.

-   `type` : It must be `Open311ServiceType`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information
    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

The following fields defined by Open 311,
[Service List](http://wiki.open311.org/GeoReport_v2/#get-service-list) are
allowed to be attributes of this entity type:

-   `jurisdiction_id`

-   `type`. To avoid collision with the NGSI entity type it has been renamed to
    `open311:type`.

-   `service_code`

-   `service_name`

-   `description`

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)

-   `keywords`

-   `group`

-   `metadata`. This field is not strictly needed as the proposed entity
    encompasses the attribute definition as well. If defined, its value must be
    `true` if the `attributes` property is defined and its array value is not
    empty. Otherwise it must be equal to `false`.

*   `attributes`. As per the
    [Service Definition](http://wiki.open311.org/GeoReport_v2/#get-service-definition)
    structure defined by Open 311.

FIWARE / OASC recommends the following additional fields as an extension to the
Open 311 model:

-   `location` : Location of the area on which this type of service is provided.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Optional

-   `provider` : Provider of the service.

    -   Attribute Type: Property. [Provider](http://schema.org/provider)
    -   Normative references:
        [https://schema.org/provider](https://schema.org/provider)
    -   Optional

-   `effectiveSince` : The date on which the service type was created. This date
    might be different than the entity creation date.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "o311:servicetype-guadalajara-sidewalks",
    "type": "Open311ServiceType",
    "group": {
        "value": "street"
    },
    "description": {
        "value": "When a sidewalk is broken or dirty allows citizens to request a fix"
    },
    "service_code": {
        "value": 234
    },
    "service_name": {
        "value": "Aceras"
    },
    "open311:type": {
        "value": "realtime"
    },
    "jurisdiction_id": {
        "value": "www.smartguadalajara.com"
    },
    "dateCreated": {
        "type": "DateTime",
        "value": "2007-01-01T12:00:00Z"
    },
    "keywords": {
        "value": "street,sidewalk, cleaning, repair"
    },
    "attributes": {
        "value": [
            {
                "code": "ISSUE_TYPE",
                "description": "What is the identified problem at the sidewalk?",
                "datatype": "singlevaluelist",
                "required": true,
                "values": [
                    {
                        "name": "Bump",
                        "key": 123
                    },
                    {
                        "name": "Dirty",
                        "key": 124
                    }
                ],
                "variable": true,
                "order": 1,
                "datatype_description": ""
            }
        ]
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "o311:servicetype-guadalajara-sidewalks",
    "type": "Open311ServiceType",
    "dateCreated": "2007-01-01T12:00:00Z",
    "jurisdiction_id": "www.smartguadalajara.com",
    "open311:type": "realtime",
    "service_code": 234,
    "service_name": "Aceras",
    "description": "When a sidewalk is broken or dirty allows citizens to request a fix",
    "keywords": "street,sidewalk, cleaning, repair",
    "group": "street",
    "attributes": [
        {
            "variable": true,
            "code": "ISSUE_TYPE",
            "datatype": "singlevaluelist",
            "required": true,
            "datatype_description": "",
            "order": 1,
            "description": "What is the identified problem at the sidewalk?",
            "values": [
                {
                    "key": 123,
                    "name": "Bump"
                },
                {
                    "key": 124,
                    "name": "Dirty"
                }
            ]
        }
    ]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:Open311ServiceType:o311:servicetype-guadalajara-sidewalks",
    "type": "Open311ServiceType",
    "createdAt": "2007-01-01T12:00:00Z",
    "group": {
        "type": "Property",
        "value": "street"
    },
    "description": {
        "type": "Property",
        "value": "When a sidewalk is broken or dirty allows citizens to request a fix"
    },
    "service_code": {
        "type": "Property",
        "value": 234
    },
    "service_name": {
        "type": "Property",
        "value": "Aceras"
    },
    "open311:type": {
        "type": "Property",
        "value": "realtime"
    },
    "jurisdiction_id": {
        "type": "Property",
        "value": "www.smartguadalajara.com"
    },
    "keywords": {
        "type": "Property",
        "value": "street,sidewalk, cleaning, repair"
    },
    "attributes": {
        "type": "Property",
        "value": [
            {
                "code": "ISSUE_TYPE",
                "description": "What is the identified problem at the sidewalk?",
                "datatype": "singlevaluelist",
                "required": true,
                "values": [
                    {
                        "name": "Bump",
                        "key": 123
                    },
                    {
                        "name": "Dirty",
                        "key": 124
                    }
                ],
                "variable": true,
                "order": 1,
                "datatype_description": ""
            }
        ]
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

## Open issues
