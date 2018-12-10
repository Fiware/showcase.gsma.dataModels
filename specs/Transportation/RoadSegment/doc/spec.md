# Road Segment

## Description

This entity contains a harmonised geographic and contextual description of a
road segment. A collection of road segments are used to describe a
[Road](../../Road/doc/spec.md).

Road segments can include several lanes. This data model allows to convey road
segments made up of heterogeneous lanes (different in their usage, speed,
height, etc.).

Lanes are identified by using integer numbers between `1` and `n`, being number
`1` the lane to the right when going forwards. The `forward` direction is the
direction denoted by the vector which goes from the segment's start point to the
segment's endpoint. This is the same convention as the one used by
[OpenStreetMap](http://wiki.openstreetmap.org/wiki/Forward_%26_backward,_left_%26_right).

This entity is primarily associated with the Automotive and Smart City vertical
segments and related IoT applications.

This data model has been developed in cooperation with mobile operators and the
[GSMA](http://www.gsma.com/connectedliving/iot-big-data/).

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `RoadSegment`.

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `source` : The source of this data.

    -   Attribute type: [URL](https://schema.org/URL)
    -   Optional

-   `name` : Name given to this road segment.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `alternateName` : An alias for this road segment.

    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional

-   `refRoad` : Road to which this road segment belongs to.

    -   Attribute type: A reference to an entity of type
        [Road](../../Road/doc/spec.md).
    -   Mandatory

-   `location` : A GeoJSON (multi)line string which defines this road segment.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory

-   `startPoint` : The start point of this road segment encoded as a GeoJSON
    point.

    -   Attribute type: `geo:json`
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory

-   `endPoint` : The endpoint of this road segment encoded as a GeoJSON point.

    -   Attribute type: `geo:json`
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory

-   `startKilometer` : The kilometer number (measured from the road's start
    point) where this road segmnent starts.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Optional

-   `endKilometer` : The kilometer number (measured from the road's start point)
    where this road segment ends.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Optional

-   `allowedVehicleType` : Vehicle type(s) allowed to transit through this road
    segment.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: The following values defined by _VehicleTypeEnum_,
        [DATEX 2 version 2.3](http://d2docs.ndwcloud.nu/): -
        (`agriculturalVehicle`, `bicycle`, `bus`, `car`, `caravan`,
        `carWithCaravan`, `carWithTrailer`, `constructionOrMaintenanceVehicle`,
        `lorry`, `moped`, `motorcycle`, `motorcycleWithSideCar`, `motorscooter`,
        `tanker`, `trailer`, `van`, `anyVehicle`)
    -   Mandatory

-   `totalLaneNumber` : Total number of lanes offered by this road segment.

    -   Attribute type: [Number](https://schema.org/Number). Integer greater
        than 0.
    -   Mandatory

-   `length` : Total length of this road segment in kilometers.

    -   Attribute type: [Number](https://schema.org/Number)
    -   See also [https://schema.org/length](https://schema.org/length)
    -   Default unit: Kilometer (Km)
    -   Optional

-   `maximumAllowedSpeed` : Maximum allowed speed while transiting this road
    segment. More restrictive limits might be applied to specific vehicle types
    (trucks, caravans, etc.). - Attribute type:
    [Number](https://schema.org/Number) - Default unit: Kilometer per hour
    (Km/h). - Optional

-   `minimumAllowedSpeed` : Minimum allowed speed while transiting this road
    segment.

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: Kilometer per hour (Km/h).
    -   Optional

-   `maximumAllowedHeight` : Maximum allowed height for vehicles transiting this
    road segment.

    -   Attribute type: [Number](https://schema.org/Number)
    -   See also: [https://schema.org/height](https://schema.org/height)
    -   Default unit: Meter (m)
    -   Optional

-   `maximumAllowedWeight` : Maximum allowed weight for vehicles transiting this
    road segment.

    -   Attribute type: [Number](https://schema.org/Number)
    -   See also: [https://schema.org/weight](https://schema.org/weight)
    -   Default unit: Kilogram (Kg)
    -   Optional

-   `width` : Road's segmwent width.

    -   Normative References:
        [https://schema.org/width](https://schema.org/width)
    -   Default unit: Meter (m)
    -   Optional

-   `laneUsage` : This attribute can be used to convey specific parameters
    describing each lane.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: It must contain a string per road segment lane. The
        element 0 of the array must contain the information of lane 1, and so
        on. Format of the referred string must be:
        `"<lane_direction>, <lane_minimumAllowedSpeed>, <lane_maximumAllowedSpeed>, <lane_maximumAllowedHeight>, <lane_maximumAllowedWeight>"`
        . `<lane_direction>` is a text string with the following allowed
        values: - `forward`. The lane is currently used in the `forwards`
        direction. - `backward`. The lane is currently used in the `backwards`
        direction. The only mandatory parameter is `lane_direction`. If not
        specified, the rest of parameters can be assumed to be equal to those
        specified at entity level.
    -   Optional

-   `category` : Allows to convey extra characteristics of a road segment.
    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: - `oneway` : Flags whether the road segment can only be
        used in one direction. If not present it means road segment can be used
        in both directions (forwards and backwards). See also
        [http://wiki.openstreetmap.org/wiki/Key:oneway](http://wiki.openstreetmap.org/wiki/Key:oneway) -
        `toll` : Flags whether the road segment is under toll fees. - `link` :
        Flags whether this road segment is an auxiliary link segment for exiting
        or entering a road. See
        [https://wiki.openstreetmap.org/wiki/Tag:highway%3Dmotorway_link](https://wiki.openstreetmap.org/wiki/Tag:highway%3Dmotorway_link) -
        Any other value meaningful to an application.
    -   Optional

The properties `laneUsage` and those which convey the maximum allowed parameters
can be dynamic, for instance, a lane direction can be temporarily changed to
improve traffic conditions.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

Please note that this road segment's line string has been simplified only four
points just to make the example shorter.

```
{
    "id": "Spain-RoadSegment-A62-osm-24702186",
    "type": "RoadSegment",
    "name": "Valladolid-Dueñas",
    "category": ["oneway"],
    "refRoad": "Spain-Road-A62",
    "totalLaneNumber": 2,
    "maximumAllowedSpeed": 120,
    "minimumAllowedSpeed": 60,
    "startPoint": {
      "type": "Point",
      "coordinates": [-4.7299180606009, 41.6844918725019]
    },
    "endPoint": {
      "type": "Point",
      "coordinates": [-4.55167335377909, 41.8570461783071]
    },
    "allowedVehicleType": [
        "car", "bus", "lorry", "trailer",
        "tanker", "van", "caravan"
    ],
    "location": {
       "type": "LineString",
       "coordinates": [
            [
               -4.7299180606009, 41.6844918725019
            ],
            [
              -4.72855890957602, 41.6860596957855
            ],
            [
              -4.5520357341647, 41.8569278186523
            ],
            [
               -4.55167335377909, 41.8570461783071
            ]
       ]
    },
    "laneUsage": ["forward", "forward"],
    "source": "http://wwww.openstreetmap.org"
}
```

## Use it with a real service

T.B.D.

## Open issues
