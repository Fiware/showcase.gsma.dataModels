# P2PCarRental

## Description

This entity contains a description of a peer to peer rental car.
It aims to describe basic characteristics of the vehicle and it's owner. In addition to this it has some other details, like price and availability.
We hope that this model receives contributions and will be developed further by the community.

This data model has been created in co-operation with share it blox car.

## Data Model

Please see also the [example.json](../example.json) and
[schema.json](../schema.json). Look at those if the explanations in this
document don't open up the usage.

A JSON Schema corresponding to this data model can be found
[here](../schema.json). All the following entries are mandatory.

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `P2PCarRental`.

-   `vehicle_model` : The model of the vehicle omitting make, for example "159"
    or "Golf".

-   `vehicle_title` : Descriptive and more verbose title intended for human
    readers. For example "Great Alfa Romeo 159 for rental".

-   `manufacture_year` : Year when the vehicle was produced, should match the
    registration papers of the vehicle.

-   `fuel_type` : Like "petrol", "gas" or "electric". At this moment not an
    enum, as this can be sometimes unexpected (like "wood").

-   `timezone` : For example: "Europe/Helsinki". Use
    [IANA](https://www.iana.org/time-zones) spec.

-   `vehicle_maker` : Make of the vehicle, for example "Toyota". Should match
    with the registration papers of the vehicle.

-   `vehicle_location`: Location of the vehicle. If you punch these coordinates
    to the navigator and get there, given the availability, the vehicle should
    be in that location.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://github.com/geojson/schema/blob/master/src/schema/Feature.js](https://github.com/geojson/schema/blob/master/src/schema/Feature.js)
    
-   `availability` : Array of times when vehicle is available for rent. Times in
    [DateTime](https://schema.org/DateTime), which is same as
    [ISO 8601 Datetime format](https://www.iso.org/standard/40874.html).
    Example: 2029-12-31T23:45:00

-   `PostalAddress` : Address of the vehicle, following
    [PostalAddress](https://schema.org/PostalAddress) schema.

-   `seating_capacity`: Integer. How many seats

-   `price_currency` : In free text. For example "euro".

-   `prices` : Entries for hourly, daily and weekly prices.

-   `added`: When the entry was originally added, follows [DateTime](https://schema.org/DateTime)

Following entries are optional:

-   `vehicle_average_rating`: Float, range from 1-5. Peers can give a rating for the renting experience.

-   `details_url`: Url with more information about rentable item in question.

-   `rent_description`: Containing verbose description about the rentable item in question.

-   `image`: Link to an image of the vehicle.

-   `web_url`: A backlink to system hosting the information about vehicles. For example, following this link, user would be guided to P2P rental agency web page.
