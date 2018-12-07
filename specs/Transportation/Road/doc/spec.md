# Road

## Description

This entity contains a harmonised geographic and contextual description of a
road. Roads are made up of one or more
[RoadSegment](../../RoadSegment/doc/spec.md) entities. Road segments are usually
used to model the different carriageways of highways, for instance. The presence
of dedicated bicycle lanes should be modelled using road segments as well. Road
segments also play an important role when modelling roads with heterogeneous
segments, for instance segments on which speed limits are different.

This entity is primarily associated with the Automotive and Smart City vertical
segments and related IoT applications.

This data model has been developed in cooperation with mobile operators and the
[GSMA](http://www.gsma.com/connectedliving/iot-big-data/).

## Data Model

The data model is defined as shown below:

- `id` : Unique identifier.

- `type` : Entity type. It must be equal to `Road`.

- `source` : A sequence of characters giving the source of the entity data.
  - Attribute type: Text or URL
  - Optional

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

- `dateCreated` : Entity's creation timestamp.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `dateModified` : Last update timestamp of this entity.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `name` : Name given to this road, for instance `M-30`.

  - Normative References: [https://schema.org/name](https://schema.org/name)
  - Mandatory

- `alternateName` : An alias for this road.

  - Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
  - Optional

- `description` : Description or long name given to this road.

  - Normative References:
        [https://schema.org/description](https://schema.org/description)
  - Optional

- `roadClass` : The classification of this road.

  - Attribute type: [Text](https://schema.org/Text)
  - Allowed values: Those described by
        [http://wiki.openstreetmap.org/wiki/Key:highway](OpenStreetMap).
  - Mandatory

- `refRoadSegment` : Road segments which define this road.

  - Attribute type: List of references to entities of type
        [RoadSegment](../../RoadSegment/doc/spec.md).
  - MAndatory

- `length` : Total length of this road in kilometers.

  - Attribute type: [Number](https://schema.org/Number)
  - See also [https://schema.org/length](https://schema.org/length)
  - Default unit: Kilometer (Km)
  - Optional

- `responsible` : Responsible for the raod i.e. the organism or company in
    charge of its maintenance.
  - Attribute type: [Text](https://schema.org/Text)
  - Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of Use

```
    {
        "id": "Spain-Road-A62",
        "type": "Road",
        "name": "A-62",
        "alternateName": "E-80",
        "description": "Autovía de Castilla",
        "roadClass": "motorway",
        "length": 355,
        "refRoadSegment": ["Spain-RoadSegment-A62-0-355-forwards",
                           "Spain-RoadSegment-A62-0-355-backwards"],
        "responsible": "Ministerio de Fomento - Gobierno de España"
    }
```

## Use it with a real service

T.B.D.

## Open issues
