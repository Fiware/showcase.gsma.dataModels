# Route

## Description

This entity model a particular transport route model, including all properties which are commom to multiple itinerary instances belonging to such model. This data model is based on the the [General Transit Feed Specification (GTFS)](https://developers.google.com/transit/gtfs/) that defines a common format for transportation schedules and associated geographic information. A route is a way to identify a journey that is regularly made by a given transport in an agency.

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

- ```refAgency```: Agency this route operated by.
        - Attribute type: Reference to a [Agency](../../Agency/doc/spec.md)
        - Mandatory
	
- ```vehicleType```: Describes the type of transportation used on a route
	- Attribute type: [Number](https://github.com/schema.org/Number)
	- Allowed values:
                - `tram` : Any light rail or street level system within a metropolitan area
                - `subway` : Any underground rail system within a metropolitan area
                - `rail` : Used for intercity or long-distance travel
                - `bus` : Used for short- and long-distance bus routes
                - `ferry` : Used for short- and long-distance boat service
                - `cablecar` : Used for street-level cable cars where the cable runs beneath the car
                - `gondola` : Suspended cable car. Typically used for aerial cable cars where the car is suspended from the cable
                - `funicular` : Any rail system designed for steep inclines
                - `car` : Particular vehicle
                - `van` : 
                - `truck` : 
                - `electriccar` :
                - Any other value meaningfull for the scenario

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
	"id": "routeID",
        "type": "Route",
	"short_name": "SAUSA"
	"long_name": "Metro Tacubaya - La Valenciana"
	"vehicleType": "rail"
}
```
