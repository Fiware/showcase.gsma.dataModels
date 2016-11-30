# Weather Forecast

## Description

This entity contains a harmonised description of a Weather Forecast. This entity is primarily
associated with the vertical segments of the environment and agriculture but is applicable to
many different applications

This data model has been developed in cooperation with mobile operators and the [GSMA](http://www.gsma.com/connectedliving/iot-big-data/). 

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `WeatherForecast`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional
    
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
    
+ `validity` : Includes the validity period for this forecast as a ISO8601 time interval.
    + Attribute type: [Text](https://schema.org/Text)
    + Mandatory
    
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
      
## Examples of use

```

```
    
## Use it with a real service

To get access to a public instance offering weather observed data please have a look at the [GSMA's API Directory](http://apidirectory.connectedliving.gsma.com/api/weather-spain). 

The instance described [here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing) has been set up by the FIWARE Community.

What is the weather forecast today in Valladolid (Spain)?

```curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' -H 'x-auth-token:<my_token>' "http://130.206.118.244:1027/v2/entities?type=WeatherObserved&q=dateObserved:2016-11-30T07:00;address.addressLocality:Valladolid&options=keyValues"```

## Open Issues
