# Civic Issue Tracking data models

These data models allow to perform civic issue tracking. They have been designed with a view to enabling trivial
interoperability between FIWARE NGSI version 2 and [Open311](http://www.open311.org/). As a result, property names have not been
normalized to the `camelCase`syntax, they remain as currently specified by Open311. That is the rationale behind naming entity
types with `Open311` as prefix. However, a few properties are added, so that FIWARE NGSI version 2
implementations can properly store and serve Open 311 data.

FIWARE and OASC, in the medium term, might propose to the Open311 Community
a harmonized data model aligned with the rest of FIWARE data models and schema.org. In fact, 
using these data models and a FIWARE NGSI version 2 implementation it is trivial
to implement the APIs proposed by Open311. Another option would be the use of [JSON-LD](http://json-ld.org) to
define equivalencies and mappings between a FIWARE / Schema.org data model and Open 311. 

The FIWARE NGSI civic issue tracking data model defines the following entity types:

+ [Open311:ServiceType](../Open311_ServiceType/doc/spec.md). A type of service a citizen can request. It encompasses data from
the Open 311 GET Service List and GET Service Definition. 
+ [Open311:ServiceRequest](../Open311_ServiceRequest/doc/spec.md). A specific service request (of a service type) made by a citizen. 
