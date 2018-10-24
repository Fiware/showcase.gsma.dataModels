# Aero Allergen Observed

## Description

This entity models aero allergens observed at a given location and related
overall allergen risk.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of Use

```json
{
    "id": "AeroAllergenObserved-CDMX-Pollen-Cuajimalpa",
    "type": "AeroAllergenObserved",
    "alnus_Level": "moderate",
    "alnus": 40,
    "alnus_Allergenicity": "3",
    "casuarina_Level": "low",
    "casuarina": 1,
    "casuarina_Allergenicity": "3",
    "allergenRisk": "moderate",
    "address": {
        "addressCountry": "MX",
        "addressLocality": "Ciudad de México",
        "streetAddress": "Colegio Franco-Inglés"
    },
    "dateModified": "2018-02-16T17:24:39.00Z",
    "dateObserved": "2018-02-11T00:00:00.00Z",
    "location": {
        "type": "Point",
        "coordinates": [-99.276977, 19.381877]
    },
    "source": "http://rema.atmosfera.unam.mx/rema/"
}
```
