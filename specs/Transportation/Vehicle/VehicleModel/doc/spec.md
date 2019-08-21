# Vehicle Model

**Note: The latest version of this Data Model can be
found at [https://github.com/smart-data-models/dataModel.Transportation](https://github.com/smart-data-models/dataModel.Transportation)**

## Description

This entity models a particular vehicle model, including all properties which
are common to multiple vehicle instances belonging to such model.

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier.

-   `type` : Entity type. It must be equal to `VehicleModel`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: Property. [URL](https://schema.org/URL)
    -   Optional

-   `name` : Name given to this vehicle model.

    -   Attribute type: Property. [Text](https://schema.org/Text).
    -   Normative References: `https://uri.etsi.org/ngsi-ld/name` equivalent to [name](https://schema.org/name)
    -   Mandatory

-   `description` : Vehicle model description.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   Normative References: `https://uri.etsi.org/ngsi-ld/description` equivalent to [description](https://schema.org/description)
    -   Optional

-   `vehicleType` : Type of vehicle from the point of view of its structural
    characteristics.

    -   See definition at [Vehicle](../../Vehicle/doc/spec.md).
    -   Mandatory

-   `brandName` : Vehicle's brand name.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   See also: [https://schema.org/brand](https://schema.org/brand)
    -   Mandatory

-   `modelName` : Vehicle's model name.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   See also: [https://schema.org/model](https://schema.org/model)
    -   Mandatory

-   `manufacturerName` : Vehicle's manufacturer name.

    -   Attribute type: Property. [Text](https://schema.org/Text)
    -   See also: [https://schema.org/model](https://schema.org/model)
    -   Mandatory

-   `vehicleModelDate` : The release date of a vehicle model (often used to
    differentiate versions of the same make and model).

    -   Normative References:
        [https://schema.org/vehicleModelDate](https://schema.org/vehicleModelDate)
    -   Optional

-   `cargoVolume` : The available volume for cargo or luggage. For automobiles,
    this is usually the trunk volume.

    -   Normative References:
        [https://schema.org/cargoVolume](https://schema.org/cargoVolume)
    -   Default Unit: Liters
    -   Optional
    -   Note: If only a single value is provided (type Number) it will refer to
        the maximum volume.

-   `fuelType` : The type of fuel suitable for the engine or engines of the
    vehicle.

    -   Normative References:
        [https://schema.org/fuelType](https://schema.org/fuelType)
    -   Allowed values: one Of (`gasoline`, `petrol(unleaded)`,
        `petrol(leaded)`, `petrol`, `diesel`, `electric`, `hydrogen`, `lpg`,
        `autogas`, `cng`, `biodiesel` `ethanol`, `hybrid electric/petrol`,
        `hybrid electric/diesel`, `other`)
    -   Optional

-   `fuelConsumption` : The amount of fuel consumed for traveling a particular
    distance or temporal duration with the given vehicle (e.g. liters per 100
    km).

    -   Normative References:
        [https://schema.org/fuelConsumption](https://schema.org/fuelConsumption)
    -   Default unit: liters per 100 kilometer.
    -   Optional

-   `height` : Vehicle's height.

    -   Normative References:
        [https://schema.org/height](https://schema.org/height)
    -   Optional

-   `width` : Vehicle's width.

    -   Normative References:
        [https://schema.org/width](https://schema.org/width)
    -   Optional

-   `depth` : Vehicle's depth.

    -   Normative References:
        [https://schema.org/width](https://schema.org/depth)
    -   Optional

-   `weight` : Vehicle's weight.

    -   Normative References:
        [https://schema.org/weight](https://schema.org/weight)
    -   Optional

-   `vehicleEngine` : Information about the engine or engines of the vehicle.

    -   Normative References:
        [https://schema.org/vehicleEngine](https://schema.org/vehicleEngine)
    -   Optional
    -   Note: This property could be at vehicle level as well.

-   `url` : URL which provides a description of this vehicle model.

    -   Normative References: [https://schema.org/URL](https://schema.org/url)
    -   Optional

-   `image`: Image which depicts this vehicle model.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Creation timestamp of this entity.
    -   Attribute type: Property. [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "vehiclemodel:econic",
    "type": "VehicleModel",
    "name": {
        "value": "MBenz-Econic2014"
    },
    "cargoVolume": {
        "value": 1000
    },
    "modelName": {
        "value": "Econic"
    },
    "brandName": {
        "value": "Mercedes Benz"
    },
    "manufacturerName": {
        "value": "Daimler"
    },
    "fuelType": {
        "value": "diesel"
    },
    "vehicleType": {
        "value": "lorry"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "vehiclemodel:econic",
    "type": "VehicleModel",
    "name": "MBenz-Econic2014",
    "brandName": "Mercedes Benz",
    "modelName": "Econic",
    "manufacturerName": "Daimler",
    "vehicleType": "lorry",
    "cargoVolume": 1000,
    "fuelType": "diesel"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:VehicleModel:vehiclemodel:econic",
    "type": "VehicleModel",
    "name": {
        "type": "Property",
        "value": "MBenz-Econic2014"
    },
    "cargoVolume": {
        "type": "Property",
        "value": 1000
    },
    "modelName": {
        "type": "Property",
        "value": "Econic"
    },
    "brandName": {
        "type": "Property",
        "value": "Mercedes Benz"
    },
    "manufacturerName": {
        "type": "Property",
        "value": "Daimler"
    },
    "fuelType": {
        "type": "Property",
        "value": "diesel"
    },
    "vehicleType": {
        "type": "Property",
        "value": "lorry"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with a real service

## Open issues

-   Model fuelConsumption depending on the situation (urban or road)
