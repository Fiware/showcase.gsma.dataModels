# Streetlight group

An entity of type `StreetlightGroup` represents a group of streetlights. They
might be controlled together by the same automated system (cabinet controller).

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier.

-   `type` : It must be equal to `StreetlightGroup`.

-   `location` : Streetlight's group location represented by a GeoJSON
    (multi)geometry.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
    -   Mandatory

-   `areaServed` : Higher level area to which the streetlight group belongs to.
    It can be used to group per responsible, district, neighbourhood, etc. +
    Normative References:
    [https://schema.org/areaServed](https://schema.org/areaServed) + Optional

-   `powerState` : Streetlight group's power state.

    -   Attribute type: [Text](http://schema.org/Text)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Allowed values: one Of (`on`, `off`, `low`, `bootingUp`)
    -   Optional

-   `refStreetlightCabinetController` : Streetlight group's cabinet controller

    -   Attribute type : Reference to a
        [StreetlightCabinetController](../../StreetlightCabinetController/doc/spec.md)
        entity.
    -   Optional

-   `dateLastSwitchingOn` : Timestamp of the last switching on.

    -   Attribute Type: [DateTime](http://schema.org/DateTime)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `dateLastSwitchingOff` : Timestamp of the last switching off.

    -   Attribute Type: [DateTime](http://schema.org/DateTime)
    -   Attribute metadata:
        -   `timestamp` : Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `switchingOnHours` : Switching on hours. It is used normally to set special
    schedules for certain dates.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
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

    -   Attribute Type: [Number](http://schema.org/Number)
    -   Allowed values: A number between 0 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `activeProgramId` : Identifier of the active program for this streetlight
    group.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `dateModified` : Timestamp of the last update made to this entity.

    -   Attribute Type: [DateTime](http://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `description` : Description about the streetlight group.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `annotations` : A field reserved for annotations (incidences, remarks,
    etc.).

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Optional

-   `refStreetlight` : List of streetlight entities belonging to this group.
    -   Attribute type: List of references to entities fo type
        [Streetlight](../../Streetlight/doc/spec.md)
    -   Allowed values: There must topographical integrity between the location
        of the group and of the individual streetlights.
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of Use

    {
      "id": "streetlightgroup:mycity:A12",
      "type": "StreetlightGroup",
      "location": {
        "type": "MultiLineString",
        "coordinates": [
          [ [100.0, 0.0], [101.0, 1.0] ],
          [ [102.0, 2.0], [103.0, 3.0] ]
        ]
      },
      "powerStatus": "on",
      "areaServed": "Calle Comercial Centro",
      "circuitId": "C-456-A467",
      "dateLastSwitchingOn":  "2016-07-07T19:59:06.618Z",
      "dateLastSwitchingOff": "2016-07-07T07:59:06.618Z",
      "refStreetlightCabinetController": "cabinetcontroller:CC45A34",
      "switchingOnHours": [
        {
          "from" :  "--11-30",
          "to" :    "--01-07",
          "hours" : "Mo,Su 16:00-02:00",
          "description": "Christmas"
        }
      ]
    }

## Test it with a real service

## Open Issues

-   Do we really need metering attributes on this entity? Is metering only going
    to be done at Cabinet level?
