# Noise level observed

## Description

It represents an observation of those acoustic parameters that estimate noise pressure levels at a certain place and time.
This entity is primarily associated with the Smart City and environment vertical segments and related IoT applications.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `NoiseLevelObserved`.

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.

+ `location` : Location of this observation represented by a GeoJSON geometry. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not present.

+ `address` : Civic address of this observation.
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present.
    
+ `name` : Name given to this observation.
    + Normative References: [https://schema.org/name]
    + Optional

+ `description` : Description given to this observation.
    + Normative References: [https://schema.org/description]
    + Optional
    
+ `dateObserved` : The date and time of this observation in ISO8601 UTC format.
It can be represented by an specific time instant or by an ISO8601 interval. As a workaround for
the lack of support of Orion Context Broker for datetime intervals, it can be used two separate attributes: `dateObservedFrom`, `dateObservedTo`. 
    + Attribute type: [DateTime](https://schema.org/DateTime) or an ISO8601 interval represented as [Text](https://schema.org/Text). 
    + Mandatory
        
+ `dateObservedFrom` : Observation period start date and time. See `dateObserved`. 
    + Attribute type: [DateTime](https://schema.org/DateTime). 
    + Optional
    
+ `dateObservedTo` : Observation period end date and time. See `dateObserved`. 
    + Attribute type: [DateTime](https://schema.org/DateTime). 
    + Optional
    
+ `refDevice` : A reference to the device which captured this observation.
    + Attribute type: Reference to an entity of type `Device`
    + Optional

+ `sonometerClass` : Class of sonometer (0, 1, 2) according to [ANSI](http://soundmetersource.com/ansi-standards.html)
used for taking this observation. This attribute is useful when no device entity is associated to observations.
It allows to convey, roughly, information about the precision of the measurements. 
    + Attribute type: [Text](https://schema.org/Text)
    + Allowed values: one of (`"0"`, `"1"`, `"2"`)
    + Optional

### Representing acoustic parameters

The number of acoustic parameters measured can vary.
As a result this model prescribes the following attributes to convey the referred parameters: 

+ `measurand` : An array of strings containing details (see format below) about *each acoustic parameter* observed.
    + Attribute type: List of [Text](https://schema.org/Text).
    + Allowed values: Each element of the array must be a string with the following format
    (a list of values separated by the `|` character):
`<measurand>| <observedValue>| <description>`, where:
        + `measurand` : corresponds to a term defined at
        [http://www.acoustic-glossary.co.uk/definitions-l.htm](http://www.acoustic-glossary.co.uk/definitions-l.htm).
        + `observedValue` : corresponds to the value for the measurand as a number expressed in decibels. 
        + `description` : short description of the measurand.
        + Examples:
    `"LAeq | 93.6 | A-weighted, equivalent, sound level"  "LAS | 91.6 | A-weighted, Slow, sound level"
     "LAeq,d | 65.4 | A-weighted, equivalent, day period, sound level"`
    + Mandatory
    
+ In order to enable a proper management of the *historical evolution* of the different acoustic parameters,
*for each* element described by the `measurand` array list there *MAY* be an attribute which name *MUST* be exactly equal to the
measurand name described on the `measurand` array. The structure of such an attribute will be as follows:
    + Attribute name: Equal to the name of the measurand, for instance `LAeq`.
    + Attribute type: [Number](https://schema.org/Number)
    + Attribute value: Exactly equal (same unit of measurement) to the value provided in the `measurand` array.
    
### Representing weather conditions

There are two options for representing them:

+ A/ Through a linked entity of type `WeatherObserved` (attribute named `refWeatherObserved`)
which will capture the associated weather conditions.
+ B/ Adding weather-related properties defined at [WeatherObserved](../../../Weather/WeatherObserved/doc/spec.md).

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

```
    {
      "id": "Vitoria-NoiseLevelObserved-2016-12-28T11:00:00_2016-12-28T12:00:00",
      "type": "NoiseLevelObserved",
      "location": {
        "type": "Point",
        "coordinates": [-2.6980, 42.8491]
      },
      "dateObserved": "2016-12-28T11:00:00/2016-12-28T12:00:00",
      "measurand": [
        "LAeq  | 67.8 | A-weighted, equivalent, sound level",
        "LAmax | 94.5 | A-weighted, maximum, sound level",
      ],
      "LAeq": 67.8,
      "LAmax": 94.5,
      "sonometerClass": "2"
    }
```

## Open Issues

Standard dictionary for acoustic parameters.

## References

* [Wikipedia](https://en.wikipedia.org/wiki/Sound_level_meter)
* [Acoustic Parameters (Spanish)](http://www.dipucadiz.es/export/sites/default/galeria_de_ficheros/desarrollo_sostenible/docu_cursos_jornadas/acustica_planeamiento_urb/Indices-Acusticos.pdf)
