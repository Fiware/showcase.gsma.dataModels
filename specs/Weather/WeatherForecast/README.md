# Weather Forecast

This folder contains a set of scripts which allow to expose a NGSIv2 endpoint
intended to provide weather forecasts.

Source of weather forecast are the
[Spanish National Meteorology Agency](http://aemet.es) (AEMET) and the
[Portuguese Institute for Sea and Atmosphere](http://ipma.pt) (IPMA).

The scripts present in this folder are the following:

-   `aemet.py` is the main entry point for providing weather information
    (outdated)
-   `ipma.py` contains the Python code for getting and formatting the IPMA data
    (outdated)
-   `spain_weather_forecast_harvest.py` a script for performing data harvesting
    for weather forecasts in Spain and publishing the data on an instance of
    Orion Context Broker.
-   `portugal_weather_forecast_harvest.py` a script for performing data
    harvesting for weather forecasts in Portugal and publishing the data on an
    instance of Orion Context Broker.

Please check data licenses at the original data sources before using this data
in an application.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

You can use a FIWARE instance described
[here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing)

What is the weather forecast today in Valencia (Spain) from 17:00 UTC on?

````curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' -H 'x-auth-token:<my_token>'
http://130.206.118.244:1027/v2/entities?type=WeatherForecast&options=keyValues&q=address.addressLocality:Valencia;validFrom:2016-12-01T17```
````

{ "id": "Spain-WeatherForecast-46005_2016-12-01T18:00:00_2016-12-02T00:00:00",
"type": "WeatherForecast", "address": { "addressCountry": "Spain", "postalCode":
"46005", "addressLocality": "Valencia" }, "dataProvider": "TEF", "dateIssued":
"2016-12-01T10:40:01.00Z", "dateRetrieved": "2016-12-01T12:57:24.00Z",
"dayMaximum": { "feelsLikeTemperature": 15, "temperature": 15,
"relativeHumidity": 0.9 }, "dayMinimum": { "feelsLikeTemperature": 11,
"temperature": 11, "relativeHumidity": 0.7 }, "feelsLikeTemperature": 12,
"precipitationProbability": 0.15, "relativeHumidity": 0.85, "source":
"http://www.aemet.es/xml/municipios/localidad_46250.xml", "temperature": 12,
"validFrom": "2016-12-01T17:00:00.00Z", "validTo": "2016-12-01T23:00:00.00Z",
"validity": "2016-12-01T18:00:00+01:00/2016-12-02T00:00:00+01:00",
"weatherType": "overcast", "windDirection": null, "windSpeed": 0 }

```

```
