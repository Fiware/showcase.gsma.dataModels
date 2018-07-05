# Weather Observed

Weather observed from the [Spanish National Meteorology Agency](http://aemet.es) (AEMET) is exposed through NGSIv2.
The Weather observed is provided by [weather stations](../../PointOfInterest/WeatherStation) owned by AEMET and by the IPMA (Portuguese Institute for Sea and Atmosphere). 

This folder contains the following scripts:

+ `weather_observed.py` .- Contains all the logic to expose the weather observed as an NGSIv2 data model (outdated).
+ `spain_weather_observed_harvest.py` .- Performs data harvesting using AEMET's data site as origin and Orion Context Broker as destination. 
+ `portugal_weather_observed_harvest.py` .- Performs data harvesting using IPMA's data site as origin and Orion Context Broker as destination. 

Please check data licenses at the original data sources before using this data in an application.

## Public instance

To get access to a public instance offering weather observed data please have a look at the [GSMA's API Directory](http://apidirectory.connectedliving.gsma.com). 

The instance described [here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing) has been set up by the FIWARE Community.

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

What was the weather observed today at 07:00 UTC in Valladolid (Spain)?

```curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' -H 'x-auth-token:<my_token>' "http://130.206.118.244:1027/v2/entities?type=WeatherObserved&q=dateObserved:2016-11-30T07:00;address.addressLocality:Valladolid&options=keyValues"```

```json

    [
        {
            "id": "Spain-WeatherObserved-2422-2016-11-30T08:00:00",
            "type": "WeatherObserved",
            "address":
            {
                "addressLocality": "Valladolid",
                "addressCountry": "ES"
            },
            "atmosfericPressure": 938.9,
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
            "windSpeed": 2
        }
    ]

```


