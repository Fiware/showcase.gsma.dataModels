# Weather Observed

**Note: The latest version of this Data Model can be 
found at [https://github.com/smart-data-models/dataModel.Weather](https://github.com/smart-data-models/dataModel.Weather)**

## Description

An observation of weather conditions at a certain place and time. This data
model has been developed in cooperation with mobile operators and the
[GSMA](https://www.gsma.com/iot/iot-big-data/).

## Data Model

A JSON Schema corresponding to this data model can be found
[here](https://fiware.github.io/dataModels/specs/Weather/WeatherObserved/schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `WeatherObserved`.

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.
-   `name` : Name given to the weather observed location.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Optional

-   `location` : Location of the weather observation represented by a GeoJSON
    geometry.

    -   Attribute type: Property. `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.

-   `address` : Civic address of the weather observation. Sometimes it
    corresponds to a weather station address.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `dateObserved` : The date and time of this observation in ISO8601 UTCformat.
    It can be represented by an specific time instant or by an ISO8601 interval.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime) or an ISO8601
        interval represented as [Text](https://schema.org/Text).
    -   Mandatory

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `refDevice` : A reference to the device(s) which captured this observation.

    -   Attribute type: Relationship. Reference to an entity of type `Device`
    -   Optional

-   `refPointOfInterest` : A reference to a point of interest (usually a weather
    station) associated to this observation.

    -   Attribute type: Relationship. Reference to an entity of type `PointOfInterest`
    -   Optional

-   `weatherType` : The observed weather type. It is represented by a comma
    separated list of weather statuses, for instance `overcast, lightRain`.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: A combination of (`clearNight`,`sunnyDay`,
        `slightlyCloudy`, `partlyCloudy`, `mist`, `fog`, `highClouds`, `cloudy`,
        `veryCloudy`, `overcast`, `lightRainShower`, `drizzle`, `lightRain`,
        `heavyRainShower`, `heavyRain`, `sleetShower`, `sleet`, `hailShower`,
        `hail`, `shower`, `lightSnow`, `snow`, `heavySnowShower`, `heavySnow`,
        `thunderShower`, `thunder`) or any other extended value.
    -   Optional

-   `dewPoint` : The dew point encoded as a number.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Celsius degrees.
    -   See also:
        [https://en.wikipedia.org/wiki/Dew_point](https://en.wikipedia.org/wiki/Dew_point)
    -   Optional

-   `visibility` : Visibility reported.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Allowed values: One of (`veryPoor`, `poor`, `moderate`, `good`,
        `veryGood`, `excellent`)
    -   Optional

-   `temperature` : Air's temperature observed.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Degrees centigrades.
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `relativeHumidity` : Air's relative humidity observed (percentage, expressed
    in parts per one).

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Allowed values: A number between `0` and `1`.
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `precipitation` : Precipitation level observed.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Liters per square meter.
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `windDirection` : The wind direction expressed in decimal degrees compared
    to geographic North (measured clockwise), encoded as a Number.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Decimal degrees
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `windSpeed` : The observed wind speed in m/s, encoded as a Number.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: meters per second
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `atmosphericPressure` : The atmospheric pressure observed measured in Hecto
    Pascals.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Hecto Pascals
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `pressureTendency` : Is the pressure rising or falling? It can be expressed
    in quantitative terms or qualitative terms.

    -   Attribute type: Property. [Text](https://schema.org/Text) or
        [Number](https://schema.org/Number)
    -   Allowed values, if expressed in quantitative terms: one Of (`raising`,
        `falling`, `steady`)
    -   Optional

-   `solarRadiation` : The solar radiation observed measured in Watts per square
    meter.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Watts per square meter
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
            -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `illuminance` : The
    [illumninance](https://en.wikipedia.org/wiki/Illuminance) observed measured
    in lux (lx) or lumens per square metre (cd·sr·m−2).

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Lux
    -   Attribute metadata:
    -   `timestamp` : optional timestamp for the observed value. It can be
        omitted if the observation time is the same as the one captured by the
        `dateObserved` attribute at entity level.
        -   Type: [DateTime](https://schema.org/DateTime)
    -   Optional

-   `streamGauge`: The water level surface elevation observed by Hydrometric
    measurement sensors, namely a
    [Stream Gauge](https://en.wikipedia.org/wiki/Stream_gauge), expressed in
    centimeters.

    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Centimeters (cm)
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `snowHeight`: The snow height observed by generic snow depth measurement
    sensors, expressed in centimeters.
    -   Attribute type: Property. [Number](https://schema.org/Number)
    -   Default unit: Centimeters (cm)
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00.00Z",
    "type": "WeatherObserved",
    "dateObserved": {
        "type": "DateTime",
        "value": "2016-11-30T07:00:00.00Z"
    },
    "illuminance": {
        "value": 1000
    },
    "temperature": {
        "value": 3.3
    },
    "precipitation": {
        "value": 0
    },
    "atmosphericPressure": {
        "value": 938.9
    },
    "pressureTendency": {
        "value": 0.5
    },
    "refDevice": {
        "type": "Relationship",
        "value": "device-0A3478"
    },
    "source": {
        "value": "http://www.aemet.es"
    },
    "windSpeed": {
        "value": 2
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-4.754444444, 41.640833333]
        }
    },
    "stationName": {
        "value": "Valladolid"
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "Valladolid",
            "addressCountry": "ES"
        }
    },
    "stationCode": {
        "value": "2422"
    },
    "dataProvider": {
        "value": "TEF"
    },
    "windDirection": {
        "value": -45
    },
    "relativeHumidity": {
        "value": 1
    },
    "streamGauge": {
        "value": 50
    },
    "snowHeight": {
        "value": 20
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "Spain-WeatherObserved-2422-2016-11-30T08:00:00",
    "type": "WeatherObserved",
    "address": {
        "addressLocality": "Valladolid",
        "addressCountry": "ES"
    },
    "atmosphericPressure": 938.9,
    "dataProvider": "TEF",
    "dateObserved": "2016-11-30T07:00:00.00Z",
    "location": {
        "type": "Point",
        "coordinates": [-4.754444444, 41.640833333]
    },
    "precipitation": 0,
    "pressureTendency": 0.5,
    "relativeHumidity": 1,
    "source": "http://www.aemet.es",
    "stationCode": "2422",
    "stationName": "Valladolid",
    "temperature": 3.3,
    "windDirection": -45,
    "windSpeed": 2,
    "illuminance": 1000
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:WeatherObserved:Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00.00Z",
    "type": "WeatherObserved",
    "dateObserved": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2016-11-30T07:00:00.00Z"
        }
    },
    "illuminance": {
        "type": "Property",
        "value": 1000
    },
    "temperature": {
        "type": "Property",
        "value": 3.3
    },
    "precipitation": {
        "type": "Property",
        "value": 0
    },
    "atmosphericPressure": {
        "type": "Property",
        "value": 938.9
    },
    "pressureTendency": {
        "type": "Property",
        "value": 0.5
    },
    "refDevice": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:device-0A3478"
    },
    "source": {
        "type": "Property",
        "value": "http://www.aemet.es"
    },
    "windSpeed": {
        "type": "Property",
        "value": 2
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-4.754444444, 41.640833333]
        }
    },
    "stationName": {
        "type": "Property",
        "value": "Valladolid"
    },
    "address": {
        "type": "Property",
        "value": {
            "addressLocality": "Valladolid",
            "addressCountry": "ES",
            "type": "PostalAddress"
        }
    },
    "stationCode": {
        "type": "Property",
        "value": "2422"
    },
    "dataProvider": {
        "type": "Property",
        "value": "TEF"
    },
    "windDirection": {
        "type": "Property",
        "value": -45
    },
    "relativeHumidity": {
        "type": "Property",
        "value": 1
    },
    "streamGauge": {
        "type": "Property",
        "value": 50
    },
    "snowHeight": {
        "type": "Property",
        "value": 20
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Public instance

You can read about public instance offering information about observed weather
[here](../../../gsma.md).

## Open Issues
