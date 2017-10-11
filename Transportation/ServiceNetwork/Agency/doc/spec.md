# Agency

## Description

This entity model a particular a transport agency model, including all properties which are common to multiple itinerary instances belonging to such model. An agency refers to a company or entity which provides a transportation service.

## Data Model

- ```id```: Entity's unique identifier.

- ```type```: Entity type. It must be equal to ```Agency```.

- ```name```: Name given to this agency.
    - Normative References: https://schema.org/name
    - Mandatory 

- ```url```: URL which provides information about this agency.
    - Normative references: https://schema.org/url 
    - Optional 

- ```timezone```: Timezone where this agency belongs to.
    - Attribute type: [Text](https://schema.org/Text)
    - Optional

## Example

```
{
    "id": "CC",
    "type": "Agency",
    "name": "Corredores Concesionados"
}
```
 
