# Point Of Interest - Weather Stations

This folder contains code to generate a set of POIs which correspond to the
[Weather Stations](https://www.google.com/maps/d/viewer?mid=1Sd5uNFd2um0GPog2EGkyrlzmBnEKzPQw)
owned by the Spanish Meteorological Agency ([AEMET](http://aemet.es)).

Here you can find the following files:

-   [run.py](run.py). Python code to generate and upload the list of stations.

## Public instance

You can read about public instance offering information about weather stations [here](../../gsma.md).

## Example of use

```bash
curl -s -H 'fiware-service:poi' -H 'fiware-servicepath:/Spain'  'http:/streams.lab.fiware.org:1026/v2/entities?type=PointOfInterest&q=category:WeatherStation&options=keyValues&limit=1' | python -m json.tool
```
```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Zaragoza, Valdespartera",
            "addressRegion": [
                "province"
            ]
        },
        "category": "WeatherStation",
        "id": "WeatherStation-ES-9434P",
        "location": {
            "coordinates": [
                -0.935,
                41.620833
            ],
            "type": "Point"
        },
        "source": "https://opendata.aemet.es/",
        "type": "PointOfInterest"
    }
]
```
