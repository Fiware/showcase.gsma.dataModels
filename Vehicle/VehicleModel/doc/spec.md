# Vehicle Model

## Description

This entity models a particular vehicle model, including all properties which are common to multiple vehicle instances belonging to such model. 

## Data Model

+ `id` : Entity's unique identifier. 

+ `type` : Entity type. It must be equal to `VehicleModel`.

+ `name` : Name given to this vehicle model. 
    + Normative References: [https://schema.org/name](https://schema.org/name)
    + Mandatory

+ `description` : Vehicle model description. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional
    
+ `vehicleType` : Type of vehicle.
    + Attribute type: [Text](https://schema.org/Text)
   + Allowed Values: The following values defined by *VehicleTypeEnum*,
    [DATEX 2 version 2.3](http://www.datex2.eu/sites/www.datex2.eu/files/DATEXIISchema_2_2_2_1.zip):
        + (`agriculturalVehicle`, `bicycle`, `bus`, `car`, `caravan`,
           `carWithCaravan`, `carWithTrailer`, `lorry`, `moped`,
           `motorcycle`, `motorcycleWithSideCar`, `motorscooter`, `tanker`, `trailer`, `van`)
    + Mandatory

+ `brandName` : Vehicle's brand name.
    + Attribute type: [Text](https://schema.org/Text)
    + See also: [https://schema.org/brand](https://schema.org/brand)
    + Mandatory

+ `modelName` : Vehicle's model name.
    + Attribute type: [Text](https://schema.org/Text)
    + See also: [https://schema.org/model](https://schema.org/model)
    + Mandatory

+ `manufacturerName` : Vehicle's manufacturer name.
    + Attribute type: [Text](https://schema.org/Text)
    + See also: [https://schema.org/model](https://schema.org/model)
    + Mandatory

+ `vehicleModelDate` : The release date of a vehicle model (often used to differentiate versions of the same make and model).
    + Normative References: [https://schema.org/vehicleModelDate](https://schema.org/vehicleModelDate)
    + Optional

+ `cargoVolume` : The available volume for cargo or luggage. For automobiles, this is usually the trunk volume.
    + Normative References: [https://schema.org/cargoVolume](https://schema.org/cargoVolume)
    + Default Unit: Liters
    + Optional
    + Note: If only a single value is provided (type Number) it will refer to the maximum volume.
    
+ `fuelType` : The type of fuel suitable for the engine or engines of the vehicle.
    + Normative References: [https://schema.org/fuelType](https://schema.org/fuelType)
    + Allowed values: one Of (`gasoline`, `petrol(unleaded)`, `petrol(leaded)`, `petrol`, `diesel`, `electric`,
    `hydrogen`, `lpg`, `autogas`, `cng`, `biodiesel` `ethanol`, `hybrid electric/petrol`, `hybrid electric/diesel`, `other`)
    + Optional

+ `fuelConsumption` : The amount of fuel consumed for traveling a particular distance or temporal
duration with the given vehicle (e.g. liters per 100 km).
    + Normative References: [https://schema.org/fuelConsumption](https://schema.org/fuelConsumption)
    + Default unit: liters per 100 kilometer. 
    + Optional

+ `height` : Vehicle's height.
    + Normative References: [https://schema.org/height](https://schema.org/height)
    + Optional

+ `width` : Vehicle's width.
    + Normative References: [https://schema.org/width](https://schema.org/width)
    + Optional

+ `depth` : Vehicle's depth.
    + Normative References: [https://schema.org/width](https://schema.org/depth)
    + Optional

+ `weight` : Vehicle's weight.
    + Normative References: [https://schema.org/weight](https://schema.org/weight)
    + Optional

+ `vehicleEngine` : Information about the engine or engines of the vehicle.
    + Normative References: [https://schema.org/vehicleEngine](https://schema.org/vehicleEngine)
    + Optional
    + Note: This property could be at vehicle level as well.
    
+ `url` : URL which provides a description of this vehicle model.
    + Normative References: [https://schema.org/url](https://schema.org/url)
    + Optional
    
+ `image`: Image which depicts this vehicle model.
    + Normative References: [https://schema.org/image](https://schema.org/image)
    + Optional

+ `dateModified` : Last update timestamp of this entity
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Creation timestamp of this entity
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional
    
## Examples

    {
      "id": "vehiclemodel:econic",
      "type": "VehicleModel",
      "brandName": "Mercedes Benz",
      "modelName": "Econic",
      "vehicleType": "lorry",
      "cargoVolume": 1000,
      "fuelType": "diesel"
    }


## Test it with a real service


## Open issues

* Model fuelConsumption depending on the situation (urban or road)
