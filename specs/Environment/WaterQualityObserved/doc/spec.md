# Water Quality

## Description

Water Quality data model is intended to represent water quality parameters at a
certain water mass (river, lake, sea, etc.) section

## Data Model

A JSON Schema corresponding to this data model can be found
[here](http://fiware.github.io/dataModels/specs/Environment/WaterQualityObserved/schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `WaterQualityObserved`.

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

-   `location` : Location where measurements have been taken, represented by a
    GeoJSON Point.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
    -   Mandatory if `address` is not present.
-   `address`: Civic address where the Water Quality measurement is taken.
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.
-   `refPointOfInterest` : A reference to a point of interest associated to this
    observation.

    -   Attribute type: Reference to an entity of type `PointOfInterest`
    -   Optional

-   `dateObserved` : The date and time of this observation in ISO8601 UTCformat.
    It can be represented by an specific time instant or by an ISO8601 interval.
    -   Attribute type: [DateTime](https://schema.org/DateTime) or an ISO8601
        interval represented as [Text](https://schema.org/Text).
    -   Mandatory
-   `source` : A sequence of characters giving the source of the entity data.
    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

### Common water quality parameters

-   `temperature` : Temperature.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: Celsius Degrees.
    -   Optional
-   `conductivity` : Electrical Conductivity.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: Siemens per meter (S/m).
    -   Optional
-   `conductance` : Specific Conductance.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: Siemens per meter at 25 ºC (S/m).
    -   Optional

-   `tss` : Total suspended solids.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
    -   Optional
-   `tds` : Total dissolved solids.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
    -   Optional

-   `turbidity` : Amount of light scattered by particles in the water column.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: Formazin Turbidity Unit (FTU).
    -   Optional

-   `salinity` : Amount of salts dissolved in water.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: Parts per thousand (ppt).
    -   Optional
-   `pH` : Acidity or basicity of an aqueous solution.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: Negative of the logarithm to base 10 of the activity of
        the hydrogen ion.
    -   Optional

-   `orp` : Oxidation-Reduction potential.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: millivolts (mV).
    -   Optional

### Concentrations of chemical agents

This data model is flexible enough to accommodate different chemical agents
present in water and which can be measured. Applications MUST declare the list
of chemical agents which concentration is being measured. The `measurand`
attribute must be used for such purpose.

-   `measurand` : An array of strings containing details (see format below)
    about extra measurands provided by this observation.
    -   Attribute type: List of [Text](https://schema.org/Text).
    -   Allowed values: Each element of the array must be a string with the
        following format (comma separated list of values):
        `<measurand>, <observedValue>, <unitcode>, <description>`, where:
        -   `measurand` : corresponds to the chemical formula (or mnemonic) of
            the measurand, ex. CO.
        -   `observedValue` : corresponds to the value for the measurand as a
            number.
        -   `unitCode` : The unit code (text) of measurement given using the
            [UN/CEFACT Common Code](http://wiki.goodrelations-vocabulary.org/Documentation/UN/CEFACT_Common_Codes)
            (max. 3 characters). For instance, `M1` represents milligrams per
            liter.
        -   `description` : short description of the measurand.
        -   Examples: `"NO3,0.01, M1, Nitrates"`
    -   Optional

Below there is a list of typical chemical agents measured when analysing water
quality. If such chemical agents are measured data providers MUST use the
property names expressed by the following list. Nonetheless, the `measurand`
attribute MUST be used to declare them, so that applications can discover what
extra measurands are available as part of an observation.

-   `O2` : Level of free, non-compound oxygen present.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
    -   Optional

-   `Chla` : Concentration of chlorophyll A.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: micrograms per liter.
    -   Optional
-   `PE` : Concentration of pigment phycoerythrin which can be measured to
    estimate cyanobacteria concentrations specifically.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: micrograms per liter.
    -   Optional
-   `PC` : Concentration of pigment phycocyanin which can be measured to
    estimate cyanobacteria concentrations specifically.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: micrograms per liter.
    -   Optional

-   `NH4` : Concentration of ammonium.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
    -   Optional

-   `NH3` : Concentration of ammonia.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
    -   Optional

-   `Cl-` : Concentration of chlorides.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
    -   Optional

-   `NO3` : Concentration of nitrates.
    -   Attribute type: [Number](http://schema.org/Number)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Default unit: milligrams per liter (mg/L).
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
    "id": "waterqualityobserved:Sevilla:D1",
    "type": "WaterQualityObserved",
    "dateObserved": {
        "type": "DateTime", 
        "value": "2017-01-31T06:45:00Z"
    }, 
    "temperature": {
        "value": 24.4
    }, 
    "NO3": {
        "value": 0.01
    }, 
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [
                -5.993307,
                37.362882
            ]
        }
    }, 
    "pH": {
        "value": 7.4
    },
    "measurand": {
        "value": [
            "NO3, 0.01, M1, Concentration of Nitrates"
        ]
    },
    "conductivity": {
        "value": 0.005
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "waterqualityobserved:Sevilla:D1",
    "type": "WaterQualityObserved",
    "dateObserved": "2017-01-31T06:45:00Z",
    "measurand": ["NO3, 0.01, M1, Concentration of Nitrates"],
    "location": {
        "type": "Point",
        "coordinates": [-5.993307, 37.362882]
    },
    "temperature": 24.4,
    "conductivity": 0.005,
    "pH": 7.4,
    "NO3": 0.01
}
```

## Test it with real services

## Open issues
