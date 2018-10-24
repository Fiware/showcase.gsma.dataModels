# Point Of Interest - Weather Stations

This folder contains code to generate a set of POIs which correspond to the
[Weather Stations](https://jmcanterafonseca.cartodb.com/viz/e7ccc6c6-9e5b-11e5-a595-0ef7f98ade21/map)
owned by the Spanish Meteorological Agency ([AEMET](http://aemet.es)).

Here you can find the following files:

-   `stations-normalized-wgs84.csv`. This is a list of weather stations owned by
    AEMET which provide automated readings.
-   `stations.py` This is the Python code that was used to generate the former
    file from an
    [Excel Sheet](http://datosclima.es/Aemet2013/Archivos/ListadoEstaciones2016-02.xlsx)
    downloaded.
-   `aemet-st.js`. This script loads all the weather stations to Orion Context
    Broker.

```
curl http://130.206.83.68:1027/v2/entities?type=PointOfInterest&q=category:WeatherStation
```

```json
{
    "category": "WeatherStation",
    "location": {
        "type": "Point",
        "coordinates": [-7.684722222222222, 43.78611111111111]
    },
    "name": "Estaca de Bares",
    "postalAddress": {
        "addressCountry": "ES",
        "addressLocality": "Mañón",
        "addressRegion": "A Coruña"
    },
    "source": "http://aemet.es",
    "type": "PointOfInterest",
    "id": "WeatherStation-ES-1351"
}
```

If you want to know the Weather Stations close to a certain location, for
instance Santander (Spain), you can issue a GET request like

```
http://130.206.83.68:1027/v2/entities?type=PointOfInterest&q=category:WeatherStation&georel=near;maxDistance=10000&coords=43.4275,-3.8224
```
