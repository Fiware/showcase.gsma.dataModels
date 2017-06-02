# Schema library (v 1.0)

This set of schemas represent a mechanism to package sensor data collected from mobile devices worn by a user while performing taking into account medical detail information.

These data models allow to perform health data tracking. They have been designed with a view to enabling trivial interoperability between FIWARE NGSI version 2 and Open mHealth. As a result, property names have not been normalized to the camelCasesyntax, they remain as currently specified by [Open mHealth](http://www.openmhealth.org/). That is the rationale behind naming entity types with omh prefix. However, a few properties are added, so that FIWARE NGSI version 2 implementations can properly store respective data.

oHealth-Context data model defines the following entity:


## Used in general test
* [User](./User/user-1.x.json)
* [Control test](./ClinicalControl/control-test-1.x.json)
* [Physical test](./PhysicalTest/physical-test-1.x.json)
* [Questionnaire](./Questionnaire/questionnaire-1.x.json)
* [Test type](./dataType/test-type-1.x.json)
* [Test identification](./dataType/test-identification-1.x.json)
* [User identification](./dataType/user-identification-1.x.json)
* [Sensor type](./dataType/sensor-type-1.x.json)
* [Sensor speed](./dataType/sensor-speed-1.x.json)
* [Sensor data](./dataType/sensor-data-1.x.json)
* [Sensor resolution](./dataType/sensor-resolution-1.x.json)
* [Sensor power](./dataType/sensor-power-1.x.json)
* [Gender](./dataType/gender-1.x.json)
* [Waist circumference](./dataType/waist-circumference-1.x.json)
* [Question identification](./dataType/question-identification-1.x.json)
* [Question](./dataType/question-1.x.json)
* [Answer to question](./dataType/answer-to-question-1.x.json)

## Specific purpose (Physical test)

Schemas that correspond to the variables of interest for some physical test used as proof of concept.

### Test: Timed Up and Go 
* [Walk speed](./dataType/walk-speed-1.x.json)
* [Distance between steps](./dataType/step-distance-1.x.json)
* [Distance unit value](./dataType/distance-unit-1.x.json)
* [Time between steps](./dataType/latency-1.x.json)

### Test: 30-Second Chair Stand Test
* [Number of repetitions](./dataType/repetitions-1.x.json)
* [Time between repetitions](./dataType/latency-1.x.json)

### Test: 4-Stage Balance Test
* [Interval of time that last the test](http://www.openmhealth.org/schema/omh/duration-unit-value-1.0.json)
* [Balance index](./dataType/balance-index-1.x.json)
* [Balance test](./dataType/balance-test-1.x.json)