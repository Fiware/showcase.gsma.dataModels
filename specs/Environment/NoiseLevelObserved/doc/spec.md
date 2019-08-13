# Noise Level Observed

## Description

It represents an observation of those acoustic parameters that estimate noise
pressure levels at a certain place and time. This entity is primarily associated
with the Smart City and environment vertical segments and related IoT
applications. In addition it also represents a break down of the frequencies
present in the sound in accordance with the ISO 3741:2010 standard frequencies
of 100 Hz to 10 000 Hz one-third octave band.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `NoiseLevelObserved`.

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

-   `location` : Location of this observation represented by a GeoJSON geometry.

    -   Attribute type: GeoProperty. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not present.

-   `address` : Civic address of this observation.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `name` : Name given to this observation.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Optional

-   `description` : Description given to this observation.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `dateObserved` : The date and time of this observation represented by an
    ISO8601 interval. As a workaround for the lack of support of Orion Context
    Broker for datetime intervals, it can be used two separate attributes:
    `dateObservedFrom`, `dateObservedTo`.

    -   Attribute type: Property. ISO8601 interval represented as
        [Text](https://schema.org/Text).
    -   Optional

-   `dateObservedFrom` : Observation period start date and time. See
    `dateObserved`.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime).
    -   Mandatory

-   `dateObservedTo` : Observation period end date and time. See `dateObserved`.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime).
    -   Mandatory

-   `refDevice` : A reference to the device which captured this observation.

    -   Attribute type: Relationship. Reference to an entity of type `Device`
    -   Optional

-   `sonometerClass` : Class of sonometer (0, 1, 2) according to
    [ANSI](http://soundmetersource.com/ansi-standards.html) used for taking this
    observation. This attribute is useful when no device entity is associated to
    observations. It allows to convey, roughly, information about the precision
    of the measurements.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: one of (`"0"`, `"1"`, `"2"`)
    -   Optional

-   `frequencies` : Specifies the frequencies collected from the sensor
    represented by the ISO 3741:2010 standard frequencies of 100 Hz to 10 000 Hz
    one-third octave band. The value of each frequency is the A-weighted decibel
    value recorded.

    -   `Attribute type` : A StructuredObject of frequency : value pairs as
        defined by the ISO 3741:2010 standard where the values are represented
        as Numbers
    -   Mandatory

-   `refPointOfInterest` : A reference to a point of interest associated to this
    observation.
    -   Attribute type: Relationship. Reference to an entity of type
        `PointOfInterest`
    -   Optional

### Representing acoustic parameters

The number of acoustic parameters measured can vary. _For each_ acoustic
measurand there _MUST_ be an attribute which name _MUST_ be exactly equal to the
acoustic measurand name, as follows:

-   Attribute name: Equal to the name of the measurand, for instance `LAeq`,
    `LAmax`. It must correspond to a term defined at
    [http://www.acoustic-glossary.co.uk/definitions-l.htm](http://www.acoustic-glossary.co.uk/definitions-l.htm),
    with the only exception that those measurands which name contains a `,`
    char, such char shall be substituted by the `_` char. For instance, the
    measurand "LAeq,d" shall be represented by an Attribute which name shall be
    `LAeq_d`.
-   Attribute type: [Number](https://schema.org/Number)
-   Attribute value: corresponds to the value for the measurand as a number
    expressed in decibels.
-   Attribute Metadata:
    -   `description`: short description of the measurand. (optional)
    -   Normative References:
        [https://schema.org/description](https://schema.org/description)

### Representing weather conditions

There are two options for representing them:

-   A/ Through a linked entity of type `WeatherObserved` (attribute named
    `refWeatherObserved`) which will capture the associated weather conditions.
-   B/ Adding weather-related properties defined at
    [WeatherObserved](../../../Weather/WeatherObserved/doc/spec.md).

### Representing Frequency Data

As the number of frequencies collected may vary from the ISO standard it is
suggested that anything outside of this range be omitted and if frequencies
within this range are missing the values are set to 0

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI Response

```json
{
    "id": "Vitoria-NoiseLevelObserved-2016-12-28T11:00:00_2016-12-28T12:00:00",
    "type": "NoiseLevelObserved",
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-2.698, 42.8491]
        }
    },
    "dateObservedFrom": {
        "type": "DateTime",
        "value": "2016-12-28T11:00:00"
    },
    "dateObservedTo": {
        "type": "DateTime",
        "value": "2016-12-28T12:00:00"
    },
    "LAeq": {
        "value": 67.8,
        "metadata": {
            "description": {
                "value": "A-weighted, equivalent, sound level"
            }
        }
    },
    "LAmax": {
        "value": 94.5,
        "metadata": {
            "description": {
                "value": "A-weighted, maximum, sound level"
            }
        }
    },
    "LAS": {
        "value": 91.6,
        "metadata": {
            "description": {
                "value": "A-weighted, Slow, sound level"
            }
        }
    },
    "LAeq_d": {
        "value": 65.4,
        "metadata": {
            "description": {
                "value": "A-weighted, equivalent, day period, sound level"
            }
        }
    },
    "frequencies": {
        "value": {
            "100": 40,
            "125":  40,
            "160": 40,
            "200": 40,
            "250": 40,
            "315": 40,
            "400": 40,
            "500": 40,
            "630": 40,
            "800": 40,
            "1000": 40,
            "1250": 40,
            "1600": 40,
            "2000": 40,
            "2500": 40,
            "3150": 40,
            "4000": 40,
            "8000": 40,
            "10000": 40
        },
        "metadata": {
            "description": {
                "value": "A-weighted, frequency, sound level "
            }
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "Vitoria-NoiseLevelObserved-2016-12-28T11:00:00_2016-12-28T12:00:00",
    "type": "NoiseLevelObserved",
    "LAS": 91.6,
    "LAeq": 67.8,
    "LAeq_d": 65.4,
    "LAmax": 94.5,
    "dateObservedFrom": "2016-12-28T11:00:00.00Z",
    "dateObservedTo": "2016-12-28T12:00:00.00Z",
    "location": {
        "type": "Point",
        "coordinates": [-2.698, 42.8491]
    },
    "frequencies": {
        "100": 40,
        "125": 40,
        "160": 40,
        "200": 40,
        "250": 40,
        "315": 40,
        "400": 40,
        "500": 40,
        "630": 40,
        "800": 40,
        "1000": 40,
        "1250": 40,
        "1600": 40,
        "2000": 40,
        "2500": 40,
        "3150": 40,
        "4000": 40,
        "8000": 40,
        "10000": 40
    }
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:NoiseLevelObserved:Vitoria-NoiseLevelObserved-2016-12-28T11:00:00_2016-12-28T12:00:00",
    "type": "NoiseLevelObserved",
    "dateObservedFrom": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-12-28T11:00:00.00Z"
        }
    },
    "LAmax": {
        "type": "Property",
        "value": 94.5
    },
    "LAeq": {
        "type": "Property",
        "value": 67.8
    },
    "dateObservedTo": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-12-28T12:00:00.00Z"
        }
    },
    "LAeq_d": {
        "type": "Property",
        "value": 65.4
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-2.698, 42.8491]
        }
    },
    "LAS": {
        "type": "Property",
        "value": 91.6
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Open Issues

## References

-   [Wikipedia](https://en.wikipedia.org/wiki/Sound_level_meter)
-   [Acoustic Parameters (Spanish)](http://www.dipucadiz.es/export/sites/default/galeria_de_ficheros/desarrollo_sostenible/docu_cursos_jornadas/acustica_planeamiento_urb/Indices-Acusticos.pdf)
