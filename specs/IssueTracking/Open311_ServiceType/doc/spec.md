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

-   `type` : It must be `Open311:ServiceType`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information
    -   Attribute type: URL
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

    -   Attribute type: GeoJSON geometry.
    -   Optional

-   `provider` : Provider of the service.

    -   Normative references:
        [https://schema.org/provider](https://schema.org/provider)
    -   Optional

-   `effectiveSince` : The date on which the service type was created. This date
    might be different than the entity creation date.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

    {
      "id": "o311:servicetype-guadalajara-sidewalks",
      "type": "Open311:ServiceType",
      "dateCreated": "2007-01-01",
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
          "datatype_description": null,
          "order": 1,
          "description": "What is the identified problem at the sidewalk?",
          "values": [
            {
              "key": 123,
              "name": "Bump"
            },
            {
              "key": 124,
              "name":"Dirty"
            }
          ]
        }
      ]
    }

## Test it with a real service

## Open issues
