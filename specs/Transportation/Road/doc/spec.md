# Road

**Note: The latest version of this Data Model can be 
found at [https://github.com/smart-data-models/dataModel.Transportation](https://github.com/smart-data-models/dataModel.Transportation)**

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
[GSMA](https://www.gsma.com/iot/iot-big-data/).

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `Road`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `name` : Name given to this road, for instance `M-30`.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `alternateName` : An alias for this road.

    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional

-   `description` : Description or long name given to this road.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `roadClass` : The classification of this road.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: Those described by
        [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Key:highway).
    -   Mandatory

-   `refRoadSegment` : Road segments which define this road.

    -   Attribute type: Relationship. List of references to entities of type
        [RoadSegment](../../RoadSegment/doc/spec.md).
    -   Mandatory if `location` is not defined

-   `location` : A GeoJSON (multi)line string which defines this road.

    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Attribute type: GeoProperty. `geo:json`
    -   Mandatory if `refRoadSegment` is not defined

-   `length` : Total length of this road in kilometers.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   See also [https://schema.org/length](https://schema.org/length)
    -   Default unit: Kilometer (Km)
    -   Optional

-   `responsible` : Responsible for the raod i.e. the organism or company in
    charge of its maintenance.
    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "Spain-Road-A62",
    "type": "Road",
    "refRoadSegment": {
        "type": "Relationship",
        "value": [
            "Spain-RoadSegment-A62-0-355-forwards",
            "Spain-RoadSegment-A62-0-355-backwards"
        ]
    },
    "roadClass": {
        "value": "motorway"
    },
    "description": {
        "value": "Autov\u00eda de Castilla"
    },
    "responsible": {
        "value": "Ministerio de Fomento - Gobierno de Espa\u00f1a"
    },
    "length": {
        "value": 355
    },
    "alternateName": {
        "value": "E-80"
    },
    "name": {
        "value": "A-62"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "Spain-Road-A62",
    "type": "Road",
    "name": "A-62",
    "alternateName": "E-80",
    "description": "Autovía de Castilla",
    "roadClass": "motorway",
    "length": 355,
    "refRoadSegment": [
        "Spain-RoadSegment-A62-0-355-forwards",
        "Spain-RoadSegment-A62-0-355-backwards"
    ],
    "responsible": "Ministerio de Fomento - Gobierno de España"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:Road:Spain-Road-A62",
    "type": "Road",
    "refRoadSegment": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:RoadSegment:Spain-RoadSegment-A62-0-355-forwards",
            "urn:ngsi-ld:RoadSegment:Spain-RoadSegment-A62-0-355-backwards"
        ]
    },
    "roadClass": {
        "type": "Property",
        "value": "motorway"
    },
    "description": {
        "type": "Property",
        "value": "Autov\u00eda de Castilla"
    },
    "responsible": {
        "type": "Property",
        "value": "Ministerio de Fomento - Gobierno de Espa\u00f1a"
    },
    "length": {
        "type": "Property",
        "value": 355
    },
    "alternateName": {
        "type": "Property",
        "value": "E-80"
    },
    "name": {
        "type": "Property",
        "value": "A-62"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Use it with a real service

T.B.D.

## Open issues
