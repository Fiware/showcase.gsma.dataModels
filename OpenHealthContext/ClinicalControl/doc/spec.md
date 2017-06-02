# ClinicalControl

## Data Model

A JSON Schema corresponding to this data model can be found [here](../schema.json).

+ `id` : Unique identifier.
   + Mandatory.

+ `type` : Entity type. It must be equal to `ControlTest`.
   + Mandatory

+ `refUser` : Reference to the actual User sheltered by an independent service.
    + Attribute type: `string`.
    + Mandatory.

+ `omh:body_weight` : Represents body weight.
    + Attribute type: [body-weight](http://www.openmhealth.org/schema/omh/body-weight-1.0.json).
    + Allowed values: (`kg`, `g`, `lbs`, `oz`).
    + Mandatory.

+ `omh:body_height` : Represents body height.
    + Attribute type: [body-height](http://www.openmhealth.org/schema/omh/body-height-1.0.json).
    + Allowed values: (`m`, `cm`, `ft`, `in`).
    + Mandatory.

+ `waistCircumference` : This schema represents a person's waist circumference, either a single body weight measurement, or for the result of aggregating several measurements made over time (see Numeric descriptor schema for a list of aggregate measures).
    + Attribute type: [waist-circumference](https://github.com/netzahdzc/oHealth-Context/blob/master/schemas/dataType/waist-circumference-1.x.json).
    + Mandatory.

+ `omh:heart_rate` : Represents a person’s heart rate.
    + Attribute type: [heart-rate](http://www.openmhealth.org/schema/omh/heart-rate-1.0.json).
    + Allowed values: (`beats/min`).
    + Mandatory.

+ `omh:systolic_blood_pressure` : It should be combined with diastolic blood pressure schema to create the full schema.
    + Attribute type: [systolic-blood-pressure](http://www.openmhealth.org/schema/omh/systolic-blood-pressure-1.0.json).
    + Allowed values: (`mmHg`).
    + Mandatory.

+ `omh:diastolic_blood_pressure` : It should be combined with systolic blood pressure schema to create the full schema.
    + Attribute type: [diastolic-blood-pressure](http://www.openmhealth.org/schema/omh/diastolic-blood-pressure-1.0.json).
    + Allowed values: (`mmHg`).
    + Mandatory.

+ `dateModified` : Date and time measurements are taken.
    + Attribute type: [DateTime](https://schema.org/DateTime).
    + Mandatory.


## Examples of use

```
{  
   "id": "ffffffffff9cbbf4465f0ef30033c587-control-4",
   "type": "ControlTest",
   "refUser": "http://207.249.127.162:1234/users/1",
   "omh:body_weight": {  
      "value": 89,
      "unit": "kg"
   },
   "omh:body_height": {  
      "value": 180,
      "unit": "cm"
   },
   "waistCircumference": {  
      "value": 100,
      "unit": "cm"
   },
   "omh:heart_rate": {  
      "value": 70,
      "unit": "beats/min"
   },
   "omh:systolic_blood_pressure": {  
      "value": 120,
      "unit": "mmHg"
   },
   "omh:diastolic_blood_pressure": {  
      "value": 120,
      "unit": "mmHg"
   },
   "dateModified": "2017-01-18T20:45:42.697Z"
}
```

## Use it with a real service

T.B.D.

## Open Issues

T.B.A.
