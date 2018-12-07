# Waste Container Isle

## Description

A geographical area which keeps one or more waste containers.

## Data Model

The data model is defined as shown below:

- `id` : Unique identifier.

- `type` : Entity type. It must be equal to `WasteContainerIsle`.

- `source` : A sequence of characters giving the source of the entity data.
  - Attribute type: Text or URL
  - Optional

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

- `location` : Location of the isle represented by a GeoJSON Polygon.

  - Attribute type: `geo:json`.
  - Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
  - Mandatory

- `address` : Civic address where the isle is located.

  - Normative References:
        [https://schema.org/address](https://schema.org/address)
  - Optional

- `name` : Name given to the isle

  - Normative References: [https://schema.org/name](https://schema.org/name)
  - Optional

- `description` : Description about the isle.

  - Normative References:
        [https://schema.org/description](https://schema.org/description)
  - Optional

- `insertHolesNumber` : Number of insert holes the isle has.

  - Attribute type: [Number](https://schema.org/Number).
  - Optional

- `features` : A list of features provided by the isle.

  - Attribute type: List of [Text](http://schema.org/Text).
  - Allowed values:
        -   `containerFix`. Allows to fix containers to a permanent position.
        -   `fenced`. The isle is properly fenced.
        -   `underground`. The isle allows to hold buried containers.
        -   Any other value meaningful to the application.
  - Optional

- `refWasteContainer` : List of containers present in the isle.

  - Attribute type: List of references to
        [WasteContainer](../../WasteContainer/doc/spec.md) entities.
  - Allowed values. Container's ID.
  - Optional

- `areaServed` : Higher level area to which the isle belongs to. It can be
    used to group isles per responsible, district, neighbourhood, etc. 
  - Attribute type: [Text](https://schema.org/Text) 
  - Optional

- `dateModified` : Last update timestamp of this entity

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `dateCreated` : Entity's creation timestamp.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `availableSince` : Creation timestamp of the isle (This might different than
    the entity creation time)
  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Example

    {
      "id": "wastecontainerisle:Fleming:12",
      "type": "WasteContainerIsle",
      "location": {
         "type": "Polygon",
         "coordinates": [
          [
            [ -3.164485591715449, 40.62785133667262 ],
            [ -3.164445130316209, 40.627871567372239 ],
            [ -3.164394553567159, 40.627772099765778 ],
            [ -3.164424899616589, 40.62775018317452 ],
            [ -3.164485591715449, 40.62785133667262 ]
          ]
         ]
      },
      "address": {
         "streetAddress" : "Calle Dr. Fleming, 12",
         "addressLocality": "Guadalajara",
         "addressCountry": "ES"
      },
      "features": ["underground"],
      "name": "Dr. Fleming 12, Esquina Manuel Paez Xaramillo",
      "description": "Container isle located downtown",
      "containers": ["wastecontainer:Fleming:12a", "wastecontainer:Fleming:12b"]
    }

## Test it with a real service

T.B.D.
