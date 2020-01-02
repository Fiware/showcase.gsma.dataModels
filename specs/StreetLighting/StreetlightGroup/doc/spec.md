# Streetlight group

**Note: The latest version of this Data Model can be found at
[https://github.com/smart-data-models/dataModel.Streetlighting](https://github.com/smart-data-models/dataModel.Streetlighting)**

An entity of type `StreetlightGroup` represents a group of streetlights. They
might be controlled together by the same automated system (cabinet controller).

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier.

-   `type` : It must be equal to `StreetlightGroup`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `location` : Streetlight's group location represented by a GeoJSON
    (multi)geometry.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
    -   Mandatory

-   `areaServed` : Higher level area to which the streetlight group belongs to.
    It can be used to group per responsible, district, neighbourhood, etc.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References:
        [https://schema.org/areaServed](https://schema.org/areaServed)
    -   Optional

-   `powerState` : Streetlight group's power state.

    -   Attribute type: Property. [Text](http://schema.org/Text)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Allowed values: one Of (`on`, `off`, `low`, `bootingUp`)
    -   Optional

-   `refStreetlightControlCabinet` : Streetlight group's control cabinet

    -   Attribute type : Reference to a
        [StreetlightControlCabinet](../../StreetlightControlCabinet/doc/spec.md)
        entity.
    -   Optional

-   `dateLastSwitchingOn` : Timestamp of the last switching on.

    -   Attribute type: Property. [DateTime](http://schema.org/DateTime)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `dateLastSwitchingOff` : Timestamp of the last switching off.

    -   Attribute type: Property. [DateTime](http://schema.org/DateTime)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `switchingOnHours` : Switching on hours. It is used normally to set special
    schedules for certain dates.

    -   Attribute Type: List of
        [StructuredValue](http://schema.org/StructuredValue)
    -   Subproperties:
        -   `from` : Starting date (it can be yearless).
            -   Type: [Date](https://schema.org/Date)
        -   `to` : Ending date (it can be yearless)
            -   Type: [Date](https://schema.org/Date)
        -   `hours` : Hours.
            -   Normative References: Value must be compliant with
                [https://schema.org/openingHours](https://schema.org/openingHours)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `switchingMode` : Switching mode.

    -   Attribute Type: List of [Text](http://schema.org/Text)
    -   Allowed values: (`night-ON`, `night-OFF`, `night-LOW`, `always-ON`,
        `day-ON`, `day-OFF`, `day-LOW`)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `illuminanceLevel` : Relative illuminance level setting for the group.

    -   Attribute type: Property. [Number](http://schema.org/Number)
    -   Allowed values: A number between 0 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `activeProgramId` : Identifier of the active program for this streetlight
    group.

    -   Attribute type: Relationship. [Text](https://schema.org/Text)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `dateModified` : Timestamp of the last update made to this entity.

    -   Attribute type: Property. [DateTime](http://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `description` : Description about the streetlight group.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description`
        equivalent to [description](https://schema.org/description)
    -   Optional

-   `annotations` : A field reserved for annotations (incidences, remarks,
    etc.).

    -   Attribute type: Property. List of [Text](https://schema.org/Text)
    -   Optional

-   `refStreetlight` : List of streetlight entities belonging to this group.
    -   Attribute type: Relationship. List of references to entities fo type
        [Streetlight](../../Streetlight/doc/spec.md)
    -   Allowed values: There must topographical integrity between the location
        of the group and of the individual streetlights.
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "streetlightgroup:mycity:A12",
    "type": "StreetlightGroup",
    "circuitId": {
        "value": "C-456-A467"
    },
    "powerState": {
        "value": "on"
    },
    "dateLastSwitchingOn": {
        "type": "DateTime",
        "value": "2016-07-07T19:59:06.618Z"
    },
    "refStreetlightCabinetController": {
        "type": "Relationship",
        "value": "cabinetcontroller:CC45A34"
    },
    "dateLastSwitchingOff": {
        "type": "DateTime",
        "value": "2016-07-07T07:59:06.618Z"
    },
    "switchingOnHours": {
        "value": [
            {
                "hours": "Mo,Su 16:00-02:00",
                "to": "--01-07",
                "from": "--11-30",
                "description": "Christmas"
            }
        ]
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "MultiLineString",
            "coordinates": [
                [[100.0, 0.0], [101.0, 1.0]],
                [[102.0, 2.0], [103.0, 3.0]]
            ]
        }
    },
    "areaServed": {
        "value": "Calle Comercial Centro"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "streetlightgroup:mycity:A12",
    "type": "StreetlightGroup",
    "location": {
        "type": "MultiLineString",
        "coordinates": [
            [[100.0, 0.0], [101.0, 1.0]],
            [[102.0, 2.0], [103.0, 3.0]]
        ]
    },
    "powerState": "on",
    "areaServed": "Calle Comercial Centro",
    "circuitId": "C-456-A467",
    "dateLastSwitchingOn": "2016-07-07T19:59:06.618Z",
    "dateLastSwitchingOff": "2016-07-07T07:59:06.618Z",
    "refStreetlightCabinetController": "cabinetcontroller:CC45A34",
    "switchingOnHours": [
        {
            "from": "--11-30",
            "to": "--01-07",
            "hours": "Mo,Su 16:00-02:00",
            "description": "Christmas"
        }
    ]
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:StreetlightGroup:streetlightgroup:mycity:A12",
    "type": "StreetlightGroup",
    "circuitId": {
        "type": "Property",
        "value": "C-456-A467"
    },
    "powerState": {
        "type": "Property",
        "value": "on"
    },
    "dateLastSwitchingOn": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-07-07T19:59:06.618Z"
        }
    },
    "refStreetlightCabinetController": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:StreetlightCabinetController:cabinetcontroller:CC45A34"
    },
    "dateLastSwitchingOff": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-07-07T07:59:06.618Z"
        }
    },
    "switchingOnHours": {
        "type": "Property",
        "value": [
            {
                "hours": "Mo,Su 16:00-02:00",
                "to": "--01-07",
                "from": "--11-30",
                "description": "Christmas"
            }
        ]
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "MultiLineString",
            "coordinates": [
                [[100.0, 0.0], [101.0, 1.0]],
                [[102.0, 2.0], [103.0, 3.0]]
            ]
        }
    },
    "areaServed": {
        "type": "Property",
        "value": "Calle Comercial Centro"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

## Open Issues

-   Do we really need metering attributes on this entity? Is metering only going
    to be done at Cabinet level?
