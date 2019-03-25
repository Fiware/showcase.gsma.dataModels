# P2PCarRental

## Description

This entity contains a description of a peer to peer rental car.
It aims to describe basic characteristics of the vehicle and it's owner. In addition to this it has some other details, like price and availability.
We hope that this model receives contributions and will be developed further by the community.

This data model has been created in co-operation with share it blox car.

## Data Model

Please see also the [example.json](../example.json) and [schema.json](../schema.json). Look at those if the explanations in this document don't open up the usage.

A JSON Schema corresponding to this data model can be found
[here](../schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `P2PCarRental`.

-   `vehicle_model` : The model of the vehicle omitting make, for example "159" or "Golf".
	-   Attribute type: String

-   `vehicle_title` : Descriptive and more verbose title intended for human readers. For example "Great Alfa Romeo 159 for rental".
	-   Attribute type: String

-   `manufacture_year` : Year when the vehicle was produced, should match the registration papers of the vehicle.
	-   Attribute type: Integer

-   `fuel_type` : Like "petrol", "gas" or "electric". At this moment not an enum, as this can be sometimes unexpected (like "wood").
	-   Attribute type: String

-   `timezone` : For example: "Europe/Helsinki".
	-   Normative reference: [IANA](https://www.iana.org/time-zones) spec.

-   `vehicle_maker` : Make of the vehicle, for example "Toyota". Should match with the registration papers of the vehicle.
	-   Attribute type: String

-   `vehicle_location`: Location of the vehicle. If you punch these coordinates to the navigator and get there, given the availability, the vehicle should be in that location.

    -   Attribute type: geo:json
    -   Normative Reference: [https://github.com/geojson/schema/blob/master/src/schema/Feature.js](https://github.com/geojson/schema/blob/master/src/schema/Feature.js)
    
-   `availability` : Array of DateTimes (end and begin) when vehicle is available for rent. For example:
`"availability": [
            {
                "end": "2029-12-31T23:45:00",
                "begin": "2019-03-12T08:39:07.211823"
            }
        ],`
	-   Normative reference: [DateTime](https://schema.org/DateTime)
which is same as [ISO 8601 Datetime format](https://www.iso.org/standard/40874.html).
 

-   `seating_capacity`: Integer. How many seats.
	-   Attribute type: Integer

-   `price_currency` : In free text. For example "euro".
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

-   `PostalAddress` : Address of the vehicle.
	-   Normative reference: [PostalAddress](https://schema.org/PostalAddress)
	-   Optional

-   `vehicle_average_rating`: Float, range from 1-5. Peers can give a rating for the renting experience.
	-   Attribute type: Float
	-   Optional

-   `details_url`: Url with more information about rentable item in question.
	-   Normative reference: [URL](https://schema.org/url)
	-   Optional

-   `rent_description`: Containing verbose description about the rentable item in question and the language used. For example: `{
                "content": "Best car for you my friend!",
                "language": "en"
            }`
	-   Attribute type: Object
	-   Optional

-   `image`: Link to an image of the vehicle.
	-   Normative reference: [URL](https://schema.org/url)
	-   Optional

-   `web_url`: A backlink to system hosting the information about vehicles. For example, following this link, user would be guided to P2P rental agency web page.
	-   Normative reference: [URL](https://schema.org/url)
	-   Optional

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

