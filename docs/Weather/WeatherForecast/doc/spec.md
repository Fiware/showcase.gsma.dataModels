# Weather Forecast

## Description

This entity contains a harmonised description of a Weather Forecast. This entity is primarily
associated with the vertical segments of the environment and agriculture but is applicable to
many different applications.

This data model has been developed in cooperation with mobile operators and the [GSMA](http://www.gsma.com/connectedliving/iot-big-data/).

You can see a description of weather forecast parameters provided by AEMET (in Spanish) [here](http://www.aemet.es/es/eltiempo/prediccion/municipios/ayuda). 

## Data Model

A JSON Schema corresponding to this data model can be found [here](http://fiware.github.io/dataModels/Weather/WeatherForecast/schema.json).

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `WeatherForecast`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.
    
+ `name` : Name given to the weather forecast location.
    + Normative References: [https://schema.org/name](https://schema.org/name)
    + Optional

+ `location` : Location of the weather observation represented by a GeoJSON geometry. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not defined. 
    
+ `address` : Civic address of the weather forecast. 
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present. 
    
+ `dateRetrieved` : The date and time the forecast was retrieved in ISO8601 UTC format.
    + Attribute type: [DateTime](https://schema.org/DateTime). 
    + Mandatory
    
+ `dateIssued` : The date and time the forecast was issued by the meteorological bureau in ISO8601 UTC format.
    + Attribute type: [DateTime](https://schema.org/DateTime).
    + Mandatory
    
+ `validity` : Includes the validity period for this forecast as a ISO8601 time interval. As a workaround for
the lack of support of Orion Context Broker for datetime intervals, it can be used two separate attributes: `validFrom`, `validTo`. 
    + Attribute type: [Text](https://schema.org/Text)
    + Mandatory
    
+ `validFrom` : Validity period start date and time.
    + Attribute type: [DateTime](https://schema.org/DateTime). 
    + Optional
    
+ `validTo` : Validity period end date and time.
    + Attribute type: [DateTime](https://schema.org/DateTime). 
    + Optional
    
+ `source` : A sequence of characters giving the source of the entity data.
    + Attribute type: [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    + Optional

+ `refPointOfInterest` : A reference to a point of interest associated to this forecast.
    + Attribute type: Reference to an entity of type `PointOfInterest`
    + Optional
    
+ `weatherType` : The forecasted weather type.
    + See [WeatherObserved.weatherType](../../WeatherObserved/doc/spec.md) for description and allowed values.
    + Optional
        
+ `visibility` : Visibility forecasted. 
    + See [WeatherObserved.visibility](../../WeatherObserved/doc/spec.md) for description and allowed values.
    + Optional

+ `temperature` : Air's temperature forecasted.
    + See [WeatherObserved.temperature](../../WeatherObserved/doc/spec.md) for description and units.
    + Optional
    
+ `feelsLikeTemperature` : Feels like temperature forecasted.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Degrees centigrades.
    + Optional

+ `relativeHumidity` : Air's relative humidity forecasted (percentage, expressed in parts per one).
    + See [WeatherObserved.relativeHumidity](../../WeatherObserved/doc/spec.md) for description and units.
    + Optional

+ `precipitationProbability` : The probability of precipitation, expressed as a number between 0 ≤ precipitationProbability ≤ 1.
    + Attribute type: [Number](https://schema.org/Number)
    + Optional 

+ `windDirection` : Wind direction forecasted
    + See [WeatherObserved.windDirection](../../WeatherObserved/doc/spec.md) for description and units.
    + Optional 

+ `windSpeed` : Wind speed forecasted.
    + See [WeatherObserved.windSpeed](../../WeatherObserved/doc/spec.md) for description and units.
    + Optional
 
+ `dayMinimum` : Minimum values forecasted for the reported period.
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue)
    + Subattributes:
        + `temperature` : Minimum temperature. Same semantics and units as `WeatherForecast.temperature`.
        + `feelLikesTemperature`. Minimum feels like temperature. Same semantics and units as `WeatherForecast.feelsLikeTemperature`.
        + `relativeHumidity`. Minimum relative humidity. Same semantics and units as `WeatherForecast.relativeHumidity`.
    + Optional
 
+ `dayMaximum` : Maximum values for the reported period.
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue)
    + Subattributes:
        + `temperature` : Maximum temperature. See `WeatherForecast.temperature` for description and units.
        + `feelLikesTemperature`. Maximum feels like temperature. Same semantics and units as `WeatherForecast.feelsLikeTemperature`.
        + `relativeHumidity`. Maximum relative humidity. Same semantics and units as `WeatherForecast.relativeHumidity`.
 
+ `uVIndexMax` : The maximum UV index for the period, based on the World Health Organization's UV Index measure.
    + Normative references: [http://www.who.int/uv/intersunprogramme/activities/uv_index/en/](http://www.who.int/uv/intersunprogramme/activities/uv_index/en/)
    + Attribute type: [Number](https://schema.org/Number)
    + Optional


**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

```

{
        "id": "Spain-WeatherForecast-46005_2016-12-01T18:00:00_2016-12-02T00:00:00",
        "type": "WeatherForecast",
        "address":
        {
            "addressCountry": "Spain",
            "postalCode": "46005",
            "addressLocality": "Valencia"
        },
        "dataProvider": "TEF",
        "dateIssued": "2016-12-01T10:40:01.00Z",
        "dateRetrieved": "2016-12-01T12:57:24.00Z",
        "dayMaximum":
        {
            "feelsLikeTemperature": 15,
            "temperature": 15,
            "relativeHumidity": 0.9
        },
        "dayMinimum":
        {
            "feelsLikeTemperature": 11,
            "temperature": 11,
            "relativeHumidity": 0.7
        },
        "feelsLikeTemperature": 12,
        "precipitationProbability": 0.15,
        "relativeHumidity": 0.85,
        "source": "http://www.aemet.es/xml/municipios/localidad_46250.xml",
        "temperature": 12,
        "validFrom": "2016-12-01T17:00:00.00Z",
        "validTo": "2016-12-01T23:00:00.00Z",
        "validity": "2016-12-01T18:00:00+01:00/2016-12-02T00:00:00+01:00",
        "weatherType": "overcast",
        "windDirection": null,
        "windSpeed": 0
    }

```
    
## Use it with a real service

To get access to a public instance offering weather forecast data please have a look at the [GSMA's API Directory](http://apidirectory.connectedliving.gsma.com/api/weather-spain). 

The instance described [here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing)
has been set up by the FIWARE Community.

What is the weather forecast today in Valencia (Spain) from 17:00 UTC on?

```curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' -H 'x-auth-token:<my_token>'
http://130.206.118.244:1027/v2/entities?type=WeatherForecast&options=keyValues&q=address.addressLocality:Valencia;validFrom:2016-12-01T17
```

## Open Issues
