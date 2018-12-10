# Point Of interest

This folder contains all the code related to a harmonized NGSIv2 endpoint.

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
http://iotbd-v2.lab.fiware.org/v2/entities?type=PointOfInterest&q=category=='311'&limit=1
```

```json
[
    {
        "id": "Museum-b24a98d7fd0e4f37947add846d75fc9b",
        "type": "PointOfInterest",
        "address": {
            "type": "PostalAddress",
            "value": {
                "addressLocality": "Barcelona",
                "addressRegion": "Barcelona",
                "addressCountry": "ES"
            },
            "metadata": {}
        },
        "category": {
            "type": "List",
            "value": ["311"],
            "metadata": {}
        },
        "dataProvider": {
            "type": "Text",
            "value": "FIWARE Foundation e.V.",
            "metadata": {}
        },
        "description": {
            "type": "Text",
            "value": "El Museo de la Sagrada Familia ofrece multitud de elementos y objetos que permiten comprender el significado y la complejidad de la gran obra de Gaudí. A través de planos, dibujos originales, maquetas reconstruidas y distintas piezas, el visitante descubrirá más a fondo el proceso de creación de este impresionante templo, que se ha convertido en el símbolo de Barcelona. Desde el museo, que se encuentra situado en el interior de la iglesia, también se puede admirar la sepultura de Gaudí.",
            "metadata": {}
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [2.174492788, 41.402942517]
            },
            "metadata": {}
        },
        "name": {
            "type": "Text",
            "value": "Museo del Templo Expiatorio de la Sagrada Familia",
            "metadata": {}
        },
        "source": {
            "type": "URL",
            "value": "http://www.tourspain.es",
            "metadata": {}
        }
    }
]
```
