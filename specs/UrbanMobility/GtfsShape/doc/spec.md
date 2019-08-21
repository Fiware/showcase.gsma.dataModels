# GtfsShape

## Description

See
[https://developers.google.com/transit/gtfs/reference/#shapestxt](https://developers.google.com/transit/gtfs/reference/#shapestxt)

It represents a GTFS `shape`.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:GtfsShape:<shape_identifier>` being
        `shape_identifier` a value that can derived from the GTFS `shape_id`
        field.

-   `type`: Entity Type

    -   It shall be equal to `GtfsShape`

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `location`: The geographical shape associated to this entity encoded as
    GeoJSON `LineString` or `MultiLineString`. The coordinates shall be obtained
    from the `shapes.txt` feed file as per the value of `shape_id`,
    `shape_pt_lat`, `shape_pt_lon`, `shape_pt_sequence`.

    -   Attribute type: GeoProperty. `geo:json`
    -   Optional

-   `distanceTravelled`: An array of the distance travelled when reaching each
    of the points that make the `LineString` or `MultiLineString` that
    represents this shape. It shall match the same number of elements as the
    corresponding `LineString` or `MultiLineString`.

        - Attribute type: List of Number if the Shape is defined by a `LineString`. List of List of Number if the Shape is defined by a `MultiLineString`.
        - Optional

### Example 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:GtfsShape:S234",
    "type": "GtfsShape",
    "location": {
        "type": "geo:json",
        "value": {
            "type": "LineString",
            "coordinates": [
                [-4.421394, 36.73826],
                [-4.421428, 36.73825],
                [-4.421505, 36.738186],
                [-4.421525, 36.738033]
            ]
        }
    },
    "distanceTravelled": {
        "type": "List",
        "value": [
            0,
            6.10,
            9.78
            13.45
        ]
    }
}
```

### Example 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:GtfsShape:S234",
    "type": "GtfsShape",
    "location": {
        "type": "LineString",
        "coordinates": [
            [-4.421394, 36.73826],
            [-4.421428, 36.73825],
            [-4.421505, 36.738186],
            [-4.421525, 36.738033]
        ]
    },
    "distanceTravelled": [
        0,
        6.10,
        9.78
        13.45
    ]
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field            | NGSI Attribute      | LinkedGTFS               | Comment              |
| :-------------------- | :------------------ | :----------------------- | :------------------- |
| `shape_pt_lat`        | `location`          | `geo:lat`                | Latitude of points.  |
| `shape_pt_lon`        | `location`          | `geo:long`               | Longitude of points. |
| `shape_pt_sequence`   | `location`          | `gtfs:pointSequence`     | Sequence of points.  |
| `shape_dist_traveled` | `distanceTravelled` | `gtfs:distanceTravelled` | Distance travelled   |

### Relationships

| GTFS Field | NGSI Attribute | LinkedGTFS | Comment |
| :--------- | :------------- | :--------- | :------ |


## Open issues
