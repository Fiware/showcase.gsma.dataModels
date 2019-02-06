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

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `refUser` : reference to the (anonymised) User to which this UserContext is
    associated.

    -   Attribute type: [https://schema.org/URL](https://schema.org/URL)
    -   Normative References:
        [https://tools.ietf.org/html/rfc3986](https://tools.ietf.org/html/rfc3986)
    -   Mandatory

-   `location` : Current location of the User represented by a GeoJSON geometry.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Current civic address of the User

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `refUserDevice` : An object representing the current device used by the
    User. See [Device](../../Device/Device/doc/spec.md) definition.

    -   Attribute type: A references to a
        [Device](../../Device/Device/doc/spec.md) entity.
    -   Optional

-   `refActivity` : An object representing the current activity performed by the
    User. See [UserActivity](../UserActivity/doc/spec.md) definition.
    -   Attribute type: A references to a
        [UserActivity](../UserActivity/doc/spec.md) entity.
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

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

## Use it with a real service

T.B.D.

## Open Issues

-   [ ] Evaluate additional properties
