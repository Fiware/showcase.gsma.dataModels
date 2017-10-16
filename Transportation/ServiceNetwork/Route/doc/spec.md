# Route

## Description

This entity model a particular transport route model, including all properties which are commom to multiple itinerary instances belonging to such model. A route is a way to identify a journey that is regularly made by a given transport in an agency.

## Data Model

- ```id```: Entity's unique identifier.

- ```type```: Entity type. It must be equal to ```Route```.

- ```shortName```: Short name of a route, often a short and abstract identifier like "7", "34", or "Blue" that riders use to identify a route.
    - Normative References: https://schema.org/name
    - Mandatory 

- ```longName```: Full name of a route, more descriptive than the ```route_short_name``` and often include the route's destination or stop
    - Normative References: https://schema.org/name
    - Mandatory 

- ```description```: Description about this route.
	- Attribute type: https://schema.org/Text
	- Optional 

- ```operatedBy```: Agency this route operated by.
        - Attribute type: Reference to a [Agency](../../Agency/doc/spec.md)
        - Mandatory

- ```color```: Color that corresponds to the route. The color must be provided as a six-character hexadecimal number, for example, 00FFFF.
	- Attribute type: [Text](https://schema.org/Text)
	- Optional

- ```url```: The URL of a web page about that particular route
	- Normative references: https://schema.org/url
	- Optional


## Example

```
{
	"id": "route:194",
        "type": "Route",
	"short_name": "SAUSA",
	"long_name": "Metro Tacubaya - La Valenciana",
	"operatedBy": "CC"
}
```
