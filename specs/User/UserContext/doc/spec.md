# UserContext

## Description

This data model describe the Context of a User. No personal data is encoded in
the model. The actual User data are stored in a different end point, as
identified by the `refUser` property.

## Data Model

A JSON Schema corresponding to this data model can be found
[here](../schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `UserContext`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `refUser` : reference to the (anonymised) User to which this UserContext is
    associated.

    -   Attribute type: Relationship. [https://schema.org/URL](https://schema.org/URL)
    -   Normative References:
        [https://tools.ietf.org/html/rfc3986](https://tools.ietf.org/html/rfc3986)
    -   Mandatory

-   `location` : Current location of the User represented by a GeoJSON geometry.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Current civic address of the User

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `refUserDevice` : An object representing the current device used by the
    User. See [Device](../../../Device/Device/doc/spec.md) definition.

    -   Attribute type: Property. A references to a
        [Device](../../../Device/Device/doc/spec.md) entity.
    -   Optional

-   `refActivity` : An object representing the current activity performed by the
    User. See [UserActivity](../../Activity/doc/spec.md) definition.
    -   Attribute type: Relationship. A references to a
        [UserActivity](../../Activity/doc/spec.md) entity.
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "UserContext1",
    "type": "UserContext",
    "refActivity": {
        "type": "Relationship",
        "value": "UserActivity1"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-4.754444444, 41.640833333]
        }
    },
    "refUser": {
        "type": "Relationship",
        "value": "User1"
    },
    "refUserDevice": {
        "type": "Relationship",
        "value": "Device1"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "UserContext1",
    "type": "UserContext",
    "location": {
        "type": "Point",
        "coordinates": [-4.754444444, 41.640833333]
    },
    "refActivity": "UserActivity1",
    "refUserDevice": "Device1",
    "refUser": "User1"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:UserContext:UserContext1",
    "type": "UserContext",
    "refActivity": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Activity:UserActivity1"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-4.754444444, 41.640833333]
        }
    },
    "refUser": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:User:User1"
    },
    "refUserDevice": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:UserDevice:Device1"
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

-   [ ] Evaluate additional properties
