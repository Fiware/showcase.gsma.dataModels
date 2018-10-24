# Point Of interest

This folder contains all the code related to a harmonized NGSIv2 end point.

Such endpoint serves entities of type `PointOfInterest`. Data comes from
different sources:

-   from the city of Porto (Portugal)

The scripts present in this folder are:

-   `poi-server.js`. Main entry point of the endpoint.
-   `oporto-ost.js`. Contains all the logic needed to interact with
    [OST Platform](https://www.ost.pt/)

Please check the original datasource licenses before using this data in a
commercial application.

Currently the following categories are supported: (For a more extended list of
categories please check
https://github.com/Factual/places/blob/master/categories/factual_taxonomy.json)

-   `OffStreetParking: 418`
-   `Restaurant: 347`
-   `Hotel: 436`
-   `Museum: 311`
-   `Beach: 113`
-   `TouristInformationCenter: 439`

## Examples of use

```
http://130.206.118.244:1050/v2/entities?type=PointOfInterest&q=category:436
```

```json
{
    "id": "porto-poi-22897",
    "type": "PointOfInterest",
    "source": "http://fiware-porto.citibrain.com/docs",
    "name": "Belver Beta Porto Hotel",
    "category": ["436"],
    "dateCreated": "1970-01-01T00:00:00.000Z",
    "dateUpdated": "2015-11-12T20:39:58.336Z",
    "location": {
        "type": "Point",
        "coordinates": [-8.614206, 41.178103]
    },
    "description": "The Belver Beta Porto Hotel is ..."
}
```
