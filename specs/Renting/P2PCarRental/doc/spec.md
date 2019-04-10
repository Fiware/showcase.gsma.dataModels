# P2PCarRental

## Description

This entity contains a description of a peer to peer rental car.
It aims to describe basic characteristics of the vehicle and it's owner. In addition to this it has some other details, like price and availability.
We hope that this model receives contributions and will be developed further by the community.

This data model has been created in co-operation with Share it blox car.

## Data Model

Please see also the [example.json](../example.json) and [schema.json](../schema.json). Look at those if the explanations in this document don't open up the usage.

A JSON Schema corresponding to this data model can be found [here](../schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `P2PCarRental`.

-   `vehicle_average_rating`: Float, range from 1-5. Peers can give a rating for the renting experience.
	-   Attribute type: Float
	-   Optional

-   `timezone` : For example: "Europe/Helsinki".
	-   Normative reference: [IANA](https://www.iana.org/time-zones) spec.

-   `vehicle_information` : Follows [VehicleModel](https://github.com/FIWARE/dataModels/tree/master/specs/Transportation/Vehicle/VehicleModel) more details how to use the model are there. How ever, some of the semantics when using this datamodel are different. Here is a explanation how those are used in this model:

	- `ID`: Unique id of the vehicle, can be autocreated.
	- `name`: Descriptive name of the vehile, like "Alfa Romeo Giulia Quadrifoglio".
	- `URL`: Url containing information about the vehicle.
	- `type`: Mandatory, needs to be "VehicleModel".
	- `vehicleType`: Enum for example "car".
	- `brandName`: Brandname, not necessarily same as manufacturer.
	- `modelName`: For example "Giulia" or "Golf".
	- `manufacturerName`: Manufacturer, for example "Alfa Romeo" or "Folgsfagen".
	- `fuel_type`: enum, for example "petrol" or "other".
	- `image`: Link to an image of the vehicle.
	- `dataProvider`: A backlink to system hosting the information about vehicles. For example, following this link, user would be guided to P2P rental agency web page.


-   `manufacture_year` : Year when the vehicle was produced, should match the registration papers of the vehicle.
	-   Attribute type: Integer

-   `seating_capacity`: Integer. How many people vehicle seats.
	-   Attribute type: Integer

-   `vehicle_location`: Location of the vehicle, including the postal address. If you punch these coordinates to the navigator and get there, given the availability, the vehicle should be in that location.

    -   Attribute type: geo:json
    -   Normative Reference: [https://github.com/geojson/schema/blob/master/src/schema/Feature.js](https://github.com/geojson/schema/blob/master/src/schema/Feature.js)
    
	-   `PostalAddress` : Address of the vehicle.
	-   Normative reference: [PostalAddress](https://schema.org/PostalAddress)
	-   Optional

-   `availability` : Array of DateTimes (end and begin) when vehicle is available for rent. For example:
`"availability": [
            {
                "end": "2029-12-31T23:45:00",
                "begin": "2019-03-12T08:39:07.211823"
            }
        ],`
	-   Normative reference: [DateTime](https://schema.org/DateTime)
which is same as [ISO 8601 Datetime format](https://www.iso.org/standard/40874.html).
 
-   `rent_description`: Containing verbose description about the rentable item in question and the language used. For example: `{
                "content": "Best car for you my friend!",
                "language": "en"
            }`
	-   Attribute type: Object
	-   Optional
-   `contact_details`: Contact details for the person who to ask about the renting of the Vehicle in question, might not always be the owner. For example:
 `  "name": "Zighn Fergusson",
    "phone": "+358 44 723 8734",
    "email": "zin877@gmail.com",
    "additional": "Contact between 9 and six"`

-   `price_currency`: In free text. For example "euro".
	-   Attribute type: String

-   `prices` : Entries for hourly, daily and weekly prices. For example:
` prices": [
            {
                "pricing": "hourly",
                "extra_km_price": 0.099,
                "free_km": 20,
                "price": 6
            },
            {
                "pricing": "daily",
                "extra_km_price": 0.099,
                "free_km": 400,
                "price": 29.7
            },
            {
                "pricing": "weekly",
                "extra_km_price": 0.099,
                "free_km": 650,
                "price": 171
            }
        ]`
	-   Attribute type: [StructuredValue](http://schema.org/StructuredValue)

-   `added`: When the entry was originally added.
	-    Normative reference: [DateTime](https://schema.org/DateTime)


**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

Please see the [example.json](../example.json)

## Use it with a real service

TBD

## Open Issues

None identified at the moment.



