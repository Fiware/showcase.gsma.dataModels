# Point Of interest

This folder contains all the code related to a harmonized NGSI v2 endpoint.

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
[factual_taxonomy.json](https://github.com/Factual/places/blob/master/categories/factual_taxonomy.json))

-   `OffStreetParking: 418`
-   `Restaurant: 347`
-   `Hotel: 436`
-   `Museum: 311`
-   `Beach: 113`
-   `TouristInformationCenter: 439`

## Examples of use

```bash
curl -X GET \
  'https://streams.lab.fiware.org/v2/entities?id=Museum-b24a98d7fd0e4f37947add846d75fc9b&options=keyValues' \
  -H 'fiware-service: poi'| python -m json.tool
```

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressLocality": "Barcelona",
            "addressRegion": "Barcelona"
        },
        "category": [
            "311"
        ],
        "dataProvider": "FIWARE Foundation e.V.",
        "description": "El Museo de lastrong Sagrada Familia /strongofrece multitud de elementos y objetos que permiten comprender el significado y la complejidad de la gran obra de Gaud\u00ed. A trav\u00e9s de planos, dibujos originales, maquetas reconstruidas y distintas piezas, el visitante descubrir\u00e1 m\u00e1s a fondo el proceso de creaci\u00f3n de este impresionante templo, que se ha convertido en el s\u00edmbolo de strongBarcelona/strong. Desde el museo, que se encuentra situado en el interior de la iglesia, tambi\u00e9n se puede admirar la sepultura de Gaud\u00ed.",
        "id": "Museum-b24a98d7fd0e4f37947add846d75fc9b",
        "location": {
            "coordinates": [
                2.174492788,
                41.402942517
            ],
            "type": "Point"
        },
        "name": "Museo del Templo Expiatorio de la Sagrada Familia",
        "source": "http://www.tourspain.es",
        "type": "PointOfInterest"
    }
]
```
