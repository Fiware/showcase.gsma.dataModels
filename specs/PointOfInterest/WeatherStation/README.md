# Point Of Interest - Weather Stations

This folder contains code to generate a set of POIs which correspond to the
[Weather Stations](https://www.google.com/maps/d/viewer?mid=1Sd5uNFd2um0GPog2EGkyrlzmBnEKzPQw)
owned by the Spanish Meteorological Agency ([AEMET](http://aemet.es)).

Here you can find the following files:

-   [run.py](run.py). Python code to generate and upload the list of stations.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).


You can read about public instance offering information about weather stations [here](../../gsma.md).

## Example of use

```bash
curl -X GET \
  'http://streams.lab.fiware.org:1026/v2/entities?type=PointOfInterest&q=category:WeatherStation&options=keyValues&limit=1' \
  -H 'fiware-service: poi' \
  -H 'fiware-servicepath: /Spain' | python -m json.tool
```

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Calamocha",
            "addressRegion": "Teruel"
        },
        "category": "WeatherStation",
        "id": "WeatherStation-ES-9381I",
        "location": {
            "coordinates": [
                -1.29333,
                40.9261
            ],
            "type": "Point"
        },
        "source": "https://opendata.aemet.es/",
        "type": "PointOfInterest"
    }
]
```
