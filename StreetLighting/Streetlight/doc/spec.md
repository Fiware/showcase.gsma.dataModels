# Streetlight

An entity of type `Streetlight` represents a urban streetlight. Actually, there will be an entity of type `Streetlight` per lamp. Thus,
if a particular pole holds more than one lantern there will be as many streetlight entites as installed lamps. As a result there might be more than
one streetlight entity per location. 
A `Steeetlight` entity does not contain any attribute corresponding to structural characteristics.
Such data is captured by entities of type `StreetlightModel`.

## Data Model

+ `id` : Entity's unique identifier. 

+ `type` : It must be equal to `Streetlight`.

+ `location` : Streetlight's location represented by a GeoJSON Point. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
    + Mandatory if `address` is not present.
    
+ `address` : Civic address where the streetlight is located. 
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present.
    
+ `areaServed` : Higher level area to which this streetlight belongs to. It can be used to group streetlights per
responsible, district, neighbourhood, etc.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional 

+ `circuit` : The circuit to which this streetlight connects to and gets power from.
Typically it will contain an identifier that will allow to obtain more information about such circuit. 
    + Attribute type: [Text](http://schema.org/Text)
    + Optional

+ `refStreetlightModel` : Streetlight's model. 
    + Attribute type : Reference to a [StreetlightModel](../../StreetlightModel/doc/spec.md) entity.
    + Optional
    
+ `refStreetlightControlCabinet` : If this streetlight is individually controlled, reference to the control cabinet in charge of.
    + Attribute type : Reference to a [StreetlightControlCabinet](../../StreetlightControlCabinet/doc/spec.md) entity.
    + Optional

+ `status` : The overall status of this street light. 
    + Attribute type: [Text](http://schema.org/Text)
    + Allowed values: one Of (`ok`, `defectiveLamp`, `columnIssue`, `brokenLantern`)
        + Or any other value meaningful to the application and not covered by the values above. 
    + Attribute metadata:
        + `timestamp`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Mandatory

+ `powerState` : Streetlight's power state.
    + Attribute type: [Text](http://schema.org/Text)
    + Attribute metadata:
        + `timestamp` : Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Allowed values: one Of (`on`, `off`, `low`, `bootingUp`)
    + Optional
    
+ `refStreetlightGroup` : Streetlight's group, if this streetlight belongs to any group. 
    + Attribute type : Reference to a [StreetlightGroup](../../StreetlightGroup/doc/spec.md) entity.
    + Optional

+ `dateLastLampChange` : Timestamp of the last change of lamp made. If `null` it will mean that the lamp has never been changed. 
    + Attribute Type: [DateTime](http://schema.org/DateTime)
    + Attribute metadata:
        + `timestamp` : Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional
    
+ `dateLastSwitchingOn` : Timestamp of the last switching on.
    + Attribute Type: [DateTime](http://schema.org/DateTime)
    + Attribute metadata:
        + `timestamp` : Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional

+ `dateLastSwitchingOff` : Timestamp of the last switching off.
    + Attribute Type: [DateTime](http://schema.org/DateTime)
    + Attribute metadata:
        + `timestamp` : Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional

+ `controllingMethod` : The method used to control this streetlight.
    + Attribute type: [Text](http://schema.org/Text)
    + Allowed values: one Of (`group`, `individual`)
    + Optional
    
+ `dateModified` : Timestamp of the last update made to this entity
    + Attribute Type: [DateTime](http://schema.org/DateTime)
    + Optional
    
+ `dateServiceStarted` : Date at which the streetlight started giving service.
    + Attribute Type: [Date](http://schema.org/Date)
    + Optional
       
+ `image` : A URL containing a photo of the streetlight.
    + Normative References: [https://schema.org/image](https://schema.org/image)
    + Optional
    
+ `description` : Description about the streetlight. 
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

+ `annotations` : A field reserved for annotations (incidences, remarks, etc.).
    + Attribute type: List of [Text](https://schema.org/Text)
    + Optional

+ `locationCategory` : Category of the location where the streetlight is placed.
    + Attribute type:
    + Allowed values: oneOf (`façade`, `sidewalk`, `pedestrianPath`, `road`, `playground`,
    `park`, `garden`, `bridge`, `tunnel`, `parking`, `centralIsland`)
        + Or any other value with semantics not covered by the above list. 

+ `lanternHeight` : Lantern's height. In columns with many arms this can vary between streetlights. Another variation source
of this property are wall-mounted streetlights. 
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Meters. 
    + Optional

+ `illuminanceLevel` : Relative illuminance level setting.
    + Attribute Type: [Number](http://schema.org/Number)
    + Allowed values: A number between 0 and 1.
    + Attribute metadata:
        + `timestamp`: Timestamp when the last update of the attribute happened.
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional
    
        
## Examples of Use

    {
      "id": "streetlight:guadalajara:4567",
      "type": "Streetlight",
      "location": {
        "type": "Point",
        "coordinates": [  -3.164485591715449, 40.62785133667262 ]
      },
      "areaServed": "Roundabouts city entrance",
      "status": "ok",
      "refStreetlightGroup": "streetlightgroup:G345",
      "refStreetlightModel": "streetlightmodel:STEEL_Tubular_10m",
      "circuit": "C-456-A467",
      "lanternHeight": 10,
      "locationCategory" : "centralIsland",
      "powerState": "off",
      "controllingMethod": "individual",
      "dateLastLampChange": "2016-07-08T08:02:21.753Z"
    }

## Test it with a real service


## Open Issues

+ Initially is not considered practical to monitor individual power consumptions