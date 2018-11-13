# Weather Observed

## Description

An observation of weather conditions at a certain place and time. This data
model has been developed in cooperation with mobile operators and the
[GSMA](http://www.gsma.com/connectedliving/iot-big-data/).

## Data Model

A JSON Schema corresponding to this data model can be found
[here](https://fiware.github.io/dataModels/specs/Weather/WeatherObserved/schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `WeatherObserved`.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.
-   `name` : Name given to the weather observed location.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Optional

-   `location` : Location of the weather observation represented by a GeoJSON
    geometry.
    -   Attribute type: `geo:json`.
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
    -   Attribute type: [DateTime](https://schema.org/DateTime) or an ISO8601
        interval represented as [Text](https://schema.org/Text).
    -   Mandatory
-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional

-   `refDevice` : A reference to the device(s) which captured this observation.

    -   Attribute type: Reference to an entity of type `Device`
    -   Optional

-   `refPointOfInterest` : A reference to a point of interest (usually a weather
    station) associated to this observation.
    -   Attribute type: Reference to an entity of type `PointOfInterest`
    -   Optional
-   `weatherType` : The observed weather type. It is represented by a comma
    separated list of weather statuses, for instance `overcast, lightRain`. A
    proposed mapping for Spanish terms can be found
    [here](https://github.com/Fiware/dataModels/blob/master/specs/Weather/WeatherForecast/harvest/spain_weather_forecast_harvest.py#L135). +
    Attribute type: [Text](https://schema.org/Text) + Allowed values: A
    combination of (`clearNight`,`sunnyDay`, `slightlyCloudy`, `partlyCloudy`,
    `mist`, `fog`, `highClouds`, `cloudy`, `veryCloudy`, `overcast`,
    `lightRainShower`, `drizzle`, `lightRain`, `heavyRainShower`, `heavyRain`,
    `sleetShower`, `sleet`, `hailShower`, `hail`, `shower`, `lightSnow`, `snow`,
    `heavySnowShower`, `heavySnow`, `thunderShower`, `thunder`) or any other
    extended value. + Optional
-   `dewPoint` : The dew point encoded as a number.
    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Celsius degrees.
    -   See also:
        [https://en.wikipedia.org/wiki/Dew_point](https://en.wikipedia.org/wiki/Dew_point)
    -   Optional
-   `visibility` : Visibility reported.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Allowed values: One of (`veryPoor`, `poor`, `moderate`, `good`,
        `veryGood`, `excellent`)
    -   Optional

-   `temperature` : Air's temperature observed.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Degrees centigrades.
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `relativeHumidity` : Air's relative humidity observed (percentage, expressed
    in parts per one).

    -   Attribute type: [Number](https://schema.org/Number)
    -   Allowed values: A number between `0` and `1`.
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `precipitation` : Precipitation level observed.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Liters per square meter.
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `windDirection` : The wind direction expressed in decimal degrees compared
    to geographic North (measured clockwise), encoded as a Number.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Decimal degrees
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `windSpeed` : The observed wind speed in m/s, encoded as a Number.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: meters per second
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `atmosphericPressure` : The atmospheric pressure observed measured in Hecto
    Pascals.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Hecto Pascals
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `pressureTendency` : Is the pressure rising or falling? It can be expressed
    in quantitative terms or qualitative terms.

    -   Attribute type: [Text](https://schema.org/Text) or
        [Number](https://schema.org/Number)
    -   Allowed values, if expressed in quantitative terms: one Of (`raising`,
        `falling`, `steady`)
    -   Optional

-   `solarRadiation` : The solar radiation observed measured in Watts per square
    meter.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Watts per square meter
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

-   `illuminance` : The
    [illumninance](https://en.wikipedia.org/wiki/Illuminance) observed measured
    in lux (lx) or lumens per square metre (cd·sr·m−2).
    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Lux
    -   Attribute metadata:
        -   `timestamp` : optional timestamp for the observed value. It can be
            omitted if the observation time is the same as the one captured by
            the `dateObserved` attribute at entity level.
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use 1 (Normalized Format)

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
    }
}
```

## Examples of use 2 (?options=keyValues simplified representation for data consumers)

```
{
            "id": "Spain-WeatherObserved-2422-2016-11-30T08:00:00",
            "type": "WeatherObserved",
            "address":
            {
                "addressLocality": "Valladolid",
                "addressCountry": "ES"
            },
            "atmosphericPressure": 938.9,
            "dataProvider": "TEF",
            "dateObserved": "2016-11-30T07:00:00.00Z",
            "location":
            {
                "type": "Point",
                "coordinates":
                [
                    -4.754444444,
                    41.640833333
                ]
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

## Use it with a real service

To get access to a public instance offering weather observed data please have a
look at the
[GSMA's API Directory](http://apidirectory.connectedliving.gsma.com/api/weather-spain).

The instance described
[here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing)
has been set up by the FIWARE Community.

## Open Issues
