# Point Of Interest - Weather Stations

This folder contains code to generate a set of POIs which correspond to the
[Weather Stations](https://jmcanterafonseca.cartodb.com/viz/e7ccc6c6-9e5b-11e5-a595-0ef7f98ade21/map)
owned by the Spanish Meteorological Agency ([AEMET](http://aemet.es)).

Here you can find the following files:

  - [stations.json](stations.json). This is a list of weather stations owned by AEMET and a list of municipalities which provide automated readings.
  - [generate.py](generate.py). This is the Python code that was used to generate the [stations.json](stations.json).
  - [info.xls](info.xls). This is a list of Spain provinces and communities with codes that needed for [generate.py](generate.py).
  - [upload.py](upload.py). This is the Python code that upload [stations.json](stations.json) to the Orion Context Broker.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).

## Example of use

```bash
curl -s -H 'fiware-service:poi' -H 'fiware-servicepath:/Spain'  'https://orion.lab.fiware.org/v2/entities?type=PointOfInterest&q=category:WeatherStation&options=keyValues&limit=1' | python -m json.tool
```

```json
[
    {
        "address": {
            "addressCommunity": "Navarra",
            "addressCountry": "ES",
            "addressLocality": "Baztan",
            "addressProvince": "Navarra"
        },
        "category": "WeatherStation",
        "id": "Spain-WeatherStations-1002Y",
        "location": {
            "coordinates": [
                -1.543055556,
                43.135833333
            ],
            "type": "Point"
        },
        "type": "PointOfInterest"
    }
]
```
