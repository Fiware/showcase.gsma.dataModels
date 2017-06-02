# Questionnaire

## Description

Set of questions regarding the physical test performance.

## Data Model

A JSON Schema corresponding to this data model can be found [here](https://github.com/netzahdzc/oHealth-Context/blob/master/schemas/Questionnaire/questionnaire-1.x.json).

+ `id` : Unique identifier. 
    + Mandatory.

+ `type` : Entity type. It must be equal to `Questionnaire`.
    + Mandatory.

+ `user` : User ptofile.
    + Attribute type: [user](https://github.com/netzahdzc/oHealth-Context/blob/master/schemas/User/user-1.x.json).
    + Allowed values: (`Patient`, `Clinician`).
    + Mandatory.

+ `question` : Word or set of words that represent a particular question related to health.
    + Attribute type: [question](https://github.com/netzahdzc/oHealth-Context/blob/master/schemas/dataType/question-1.x.json).
    + Mandatory.  

+ `last_update` : Last entity's update timestamp.
    + Attribute type: [omh:date-time](http://www.openmhealth.org/schema/omh/date-time-1.0.json).
    + Mandatory. 

## Examples of use

```
{
  "id": "ffffffffff9cbbf4465f0ef30033c587-questionnaire-7118",
  "type": "Questionnaire",
  "test": {
    "value": "ffffffffff9cbbf4465f0ef30033c587-test-71108",
    "type": "test-identification"
  },
  "user": {
    "value": "ffffffffff9cbbf4465f0ef30033c587-patient-71108",
    "type": "user-identification"
  },
  "question": {
    "value": "true",
    "type": "answer-to-question"
  },
  "lastUpdate": {
    "value": "2017-01-18T20:45:42.697Z-0800",
    "type": "omh:time-interval"
  }
}
```

    
## Use it with a real service

T.B.D.

## Open Issues

T.B.A.