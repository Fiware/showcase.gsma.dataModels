# {{Data Model Name}}

## Description

{{Data Model Description}}

## Data Model

A JSON Schema corresponding to this data model can be found
{{add link to JSON Schema}}

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to {{EntityType}}.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `owner` : Entity's owners.
    -   Attribute type: List of references to [Person](http://schema.org/Person)
        or [Organization](https://schema.org/Organization).
    -   Optional

{{Location and address are two typical attributes that are added here for convenience}}

-   `location` : Location of {{entity type}} represented by a GeoJSON geometry.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.
-   `address` : Civic address of {{entity type}}
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

{{Below there is a description of a typical attribute}}

-   `{{attributeName}}` : {{Description of the attribute}}
    -   Normative References: {{Add a normative reference}}
    -   Attribute type: {{Add here the attribute type}}
    -   Attribute metadata:
        -   `{{metadata name}}` : {{Metadata Description}}
    -   {{Optional/Mandatory}}

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

{{Provide a JSON example}}

## Use it with a real service

{{Provide a link to a real service providing data following the harmonized data format}}

## Open Issues

{{Describe here any open issue}}
