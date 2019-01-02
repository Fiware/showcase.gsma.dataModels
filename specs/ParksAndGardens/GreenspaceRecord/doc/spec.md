# GreenspaceRecord

## Description

This entity contains a harmonised description of the conditions recorded on a
particular area or point inside a greenspace (flower bed, garden, etc.). This
entity type has been inspired by the `AgriParcelRecord` entity type defined by
the GSMA Harmonized Data Models.

## Data Model

A JSON Schema corresponding to this data model can be found
{{add link to JSON Schema}}

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `GreenspaceRecord`.

-   `dataProvider` : Specifies the URL to information about the provider of this information
    -   Attribute type: URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.
-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `location` : Location of the area concerned by this record and represented
    by a GeoJSON geometry.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory
-   `dateObserved` : The date and time of this observation in ISO8601 UTCformat.

    -   Attribute type: [DateTime](https://schema.org/DateTime).
    -   Mandatory

-   `soilTemperature` : The observed soil temperature in Celsius degrees.
    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Celsius degrees.
    -   Attribute metadata: 
        - `timestamp` : optional timestamp for the observed
        value. It can be omitted if the observation time is the same as the one
        captured by the `dateObserved` attribute at entity level.
    -   Optional
-   `soilMoistureVwc` : The observed soil moisture measured as Volumetric Water
    Content, VWC (percentage, expressed in parts per one).

    -   Attribute type: [Number](https://schema.org/Number) between 0 and 1.
    -   Attribute metadata: 
        - `timestamp` : optional timestamp for the observed
        value. It can be omitted if the observation time is the same as the one
        captured by the `dateObserved` attribute at entity level.
    -   Optional

-   `soilMoistureEc` : The observed soild moisture measured as Electrical
    Conductivity, EC in units of Siemens per meter (S/m).

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Siemens per meter (S/m).
    -   Attribute metadata: 
        - `timestamp` : optional timestamp for the observed
        value. It can be omitted if the observation time is the same as the one
        captured by the `dateObserved` attribute at entity level.
    -   Optional

-   `refGreenspace` : The garden or flower bed to which this record refers to.

    -   Attribute type: Reference to an entity of type `Garden` or `FlowerBed`.
    -   Optional

-   `refDevice` : The device or devices used to obtain the data expressed by
    this record.
    -   Attribute type: Reference to an entity of type `Device`
    -   Optional

### Representing related weather conditions

There are two options for representing weather conditions (air temperature,
humidity, etc.) observed at the area:

-   A/ Through a linked entity of type `WeatherObserved` (attribute named
    `refWeatherObserved`).
-   B/ Through a group of weather-related properties already defined by
    [WeatherObserved](../../../Weather/WeatherObserved/doc/spec.md).

Below is the description of the attribute to be used for option A/.

-   `refWeatherObserved` : Weather observed associated to the measurements
    described by this entity.
    -   Attribute type: Reference to a
        [WeatherObserved](../../../Weather/WeatherObserved/doc/spec.md) entity.
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

```json
{
    "id": "Santander-Garden-Piquio-Record-1",
    "type": "GreenspaceRecord",
    "location": {
        "type": "Point",
        "coordinates": [-3.7836974, 43.4741091]
    },
    "temperature": 17,
    "relativeHumidity": 0.87,
    "soilTemperature": 13,
    "refGreenspace": "Santander-Garden-Piquio"
}
```

## Use it with a real service

Soon to be available

## Open Issues
