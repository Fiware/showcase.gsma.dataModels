# Water Quality Observed

## Description

Water Quality data model is intended to represent water quality parameters at a certain water mass (river,  lake, sea, etc.) section

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `WaterQualityObserved`.

+ `location` : Location where measurements have been taken, represented by a GeoJSON Point. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
    + Mandatory if `address` is not present.
    
+ `address`: Civic address where the Water Quality measurement is taken.
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present. 
	
+ `temperature` : Temperature. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: Celsius Degrees.
    + Optional
    
+ `conductivity` : Electrical Conductivity. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: Siemens per meter (S/m).
    + Optional	
	
+ `conductance` : Specific Conductance. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: Siemens per meter at 25 ºC (S/m).
    + Optional	

+ `tss` : Total suspended solids. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional		
	
+ `tds` : Total dissolved solids. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional	

+ `turbidity` : Amount of light scattered by particles in the water column. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: Formazin Turbidity Unit (FTU).
    + Optional	

+ `salinity` : Amount of salts dissolved in water. 
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: Parts per thousand (ppt).
    + Optional		
	
+ `pH` : acidity or basicity of an aqueous solution.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: Negative of the logarithm to base 10 of the activity of the hydrogen ion.
    + Optional

+ `orp` : Oxidation-Reduction potential.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: millivolts (mV).
    + Optional

+ `O2` : Level of free, non-compound oxygen present.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional	

+ `Chla` : Concentration of chlorophyll A.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: micrograms per liter.
    + Optional		
	
+ `PE` : Concentration of pigment phycoerythrin which can be measured to estimate cyanobacteria concentrations specifically.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: micrograms per liter.
    + Optional	
	
+ `PC` : Concentration of pigment phycocyanin which can be measured to estimate cyanobacteria concentrations specifically.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: micrograms per liter.
    + Optional		

+ `NH4` : Concentration of ammonium.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional	

+ `NH3` : Concentration of ammonia.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional	

+ `Cl-` : Concentration of chlorides.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional	

+ `NO3` : Concentration of nitrates.
    + Attribute type: [Number](http://schema.org/Number)
    + Attribute metadata:
        + `dateUpdated`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Default unit: milligrams per liter (mg/L).
    + Optional		
	 
+ `dateUpdated` : Last update timestamp of this entity
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

  
## Examples of use

    {
       "id": "waterqualityobserved:Sevilla:D1",
       "type": "WaterQualityObserved`",
       "location": {
         "type": "Point",
         "coordinates": [  -5.993307, 37.362882 ]
       },
       "temperature" : 24.4,
       "conductivity": 0.005,
       "pH": 7.4
    }


## Test it with real services

## Open issues

* Sensor data probably should be separated to a different entity. 
