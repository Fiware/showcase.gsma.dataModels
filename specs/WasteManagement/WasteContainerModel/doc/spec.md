# Waste Container Model

## Description

A model of waste container which captures the static properties of a class of
containers.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type`: Entity Type. It must be equal to `WasteContainerModel`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `name`. Name given to this container model. It is a "well-known",
    mnemotechnic or codename. This attribute is different than `modelName` which
    conveys the formal model name given by the manufacturer.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `width`. Width of the container.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Default Unit: Meters
    -   See also: [https://schema.org/width](https://schema.org/width)
    -   Optional

-   `height`. Height of the container.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Default Unit: Meters
    -   See also: [https://schema.org/height](https://schema.org/height)
    -   Optional

-   `depth`. Depth of the container.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Default Unit: Meters
    -   See also: [https://schema.org/depth](https://schema.org/depth)
    -   Optional

-   `weight`. Weight of the container.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Default Unit: Kilograms
    -   See also: [https://schema.org/weight](https://schema.org/weight)
    -   Optional

-   `cargoVolume`. Total volume the container can hold.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Normative References:
        [https://schema.org/cargoVolume](https://schema.org/cargoVolume)
    -   Default Unit: liters
    -   Optional

-   `maximumLoad`. Maximum load the container can hold safely.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Default Unit: Kilograms
    -   Optional

-   `recommendedLoad`. Manufacturer recommended load for the container.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Default Unit: Kilograms
    -   Optional

-   `category`. Container’s category.

    -   Attribute type: List of [Text](https://schema.org/Text).
    -   Allowed values (Informative):
        -   `dumpster`. See
            [https://en.wikipedia.org/wiki/Dumpster](https://en.wikipedia.org/wiki/Dumpster)
        -   `trashCan`.
        -   `wheelieBin`.
        -   Any other category relevant for the application.
    -   Optional

-   `insertHolesNumber`. Number of insert holes the container has.

    -   Attribute type: [Number](https://schema.org/Number).
    -   Optional

-   `madeOf`. Material the container is made of.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Allowed values: one Of (`plastic`, `wood` , `metal`, `other`)
    -   Optional

-   `madeOfCode`. Material Code as per standard tables. TBD.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Optional

-   `brandName`. Name of the brand.

    -   Attribute type: [Text](https://schema.org/Text)
    -   See also: [https://schema.org/brand](https://schema.org/brand)
    -   Optional

-   `modelName`. Name of the model as given by the manufacturer. This attribute
    is different than `name` which is just a codename usually given by
    municipalities.

    -   Attribute type: [Text](https://schema.org/Text)
    -   See also: [https://schema.org/model](https://schema.org/model)
    -   Optional

-   `manufacturerName`. Name of the manufacturer.

    -   Attribute type: [Text](https://schema.org/Text)
    -   See also: [https://schema.org/model](https://schema.org/manufacturer)
    -   Optional

-   `description`. Description about the waste container model.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `colors`. Available colors.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed Values:
        -   A color keyword as specified by
            [W3C Color Keywords](https://www.w3.org/TR/SVG/types.html#ColorKeywords)
        -   A color value as specified by
            [W3C Color Data Type](https://www.w3.org/TR/SVG/types.html#BasicDataTypes)
    -   See also: [https://schema.org/color](https://schema.org/color)
    -   Optional

-   `image`. A URL containing a photo of the container model.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `compliantWith`. A list of standards to which the container is compliant
    with (ex. `UNE-EN 840-2:2013`)

    -   AttributeType: List of [Text](https://schema.org/Text).
    -   Optional

-   `features`. A list of container features.
    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed Values:
        -   `wheels`
        -   `lid`
        -   `roundedLid`
        -   `insertHoles`
        -   `lockable`
        -   Any other value meaningful for the application.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "wastecontainermodel:c1",
    "type": "WasteContainerModel",
    "category": {
        "value": ["dumpster"]
    },
    "cargoVolume": {
        "value": 150
    },
    "modelName": {
        "value": "C1"
    },
    "name": {
        "value": "Dumpster_Brute_2009_Plastic_Green"
    },
    "compliantWith": {
        "value": ["UNE-EN 840-2:2013"]
    },
    "madeOf": {
        "value": "plastic"
    },
    "height": {
        "value": 0.8
    },
    "width": {
        "value": 0.5
    },
    "depth": {
        "value": 0.4
    },
    "brandName": {
        "value": "Brute"
    },
    "features": {
        "value": ["wheels", "lid"]
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "wastecontainermodel:c1",
    "type": "WasteContainerModel",
    "name": "Dumpster_Plastic_Brute_2009",
    "width": 0.5,
    "height": 0.8,
    "depth": 0.4,
    "cargoVolume": 150,
    "brandName": "Brute",
    "modelName": "C1",
    "compliantWith": ["UNE-EN 840-2:2013"],
    "madeOf": "plastic",
    "features": ["wheels", "lid"],
    "category": ["dumpster"]
}
```

## Test it with a real service

## Open issues
