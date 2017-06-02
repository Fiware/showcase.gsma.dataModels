# Schema library (v 1.0)

This set of schemas represent a mechanism to package sensor data collected from mobile devices worn by a user while performing taking into account medical detail information.

These data models allow to perform health data tracking. They have been designed with a view to enabling trivial interoperability between FIWARE NGSI version 2 and Open mHealth. As a result, property names have not been normalized to the camelCasesyntax, they remain as currently specified by [Open mHealth](http://www.openmhealth.org/). That is the rationale behind naming entity types with omh prefix. However, a few properties are added, so that FIWARE NGSI version 2 implementations can properly store respective data.

oHealth-Context data model defines the following entity:

* [Control test](./ClinicalControl/)
* [Physical test](./PhysicalTest/)
* [Questionnaire](./Questionnaire/)
* [Question](./Questionnaire/Question/)
* [Answer](./Questionnaire/Answer/)
