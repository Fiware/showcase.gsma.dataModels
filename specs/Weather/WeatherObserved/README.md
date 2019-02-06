# Weather Observed

The Weather observed in Spain is provided by
[Spanish National Meteorology Agency](http://aemet.es), from Portugal by
[Instituto Português do Mar e da Atmosfera](http://www.ipma.pt/pt).
[Harvesters](./harvest) transform this data to NGSIv2.

[Harvester for Spain](./harvest/spain) requires the
[list](../../PointOfInterest/WeatherStation) of stations.

This folder contains the following scripts:

-   `weather_observed.py` .- Contains all the logic to expose the weather
    observed as an NGSIv2 data model (outdated).
-   `spain/harvester.py` .- Performs data harvesting using AEMET's data site as
    the origin and Orion Context Broker as the destination.
-   `portugal/harvester.py` .- Performs data harvesting using IPMA's data site
    as the origin and Orion Context Broker as the destination.

Please check data licenses at the original data sources before using this data
in an application.

## Public instance

To get access to a public instance offering weather observed data please have a
look at the
[GSMA's API Directory](http://apidirectory.connectedliving.gsma.com).

The instance described
[here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing)
has been set up by the FIWARE Community.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

What was the weather observed today in Valladolid (Spain)?

`curl -H 'fiware-service:weather' -H 'fiware-servicepath:/Spain' "https://orion.lab.fiware.org/v2/entities?type=WeatherObserved&q=address.addressLocality:Valladolid&options=keyValues"`

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Valladolid"
        },
        "atmosphericPressure": 937.7,
        "dataProvider": "FIWARE",
        "dateObserved": "2019-01-10T19:00:00.00Z",
        "id": "Spain-WeatherObserved-2422-latest",
        "location": {
            "coordinates": [-4.754444444, 41.640833333],
            "type": "Point"
        },
        "precipitation": 0,
        "pressureTendency": 0.7,
        "relativeHumidity": 0.65,
        "source": "http://www.aemet.es",
        "stationCode": "2422",
        "stationName": "Valladolid",
        "temperature": 1.9,
        "type": "WeatherObserved",
        "windDirection": -135,
        "windSpeed": 2.8
    }
]
```
