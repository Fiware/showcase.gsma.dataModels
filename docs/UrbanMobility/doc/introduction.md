# How to represent GTFS feeds using FIWARE NGSI

## Introduction

 The General Transit Feed Specification (GTFS), also known as GTFS static or static transit,
 defines a common format for public transportation schedules and associated geographic information.
 GTFS "feeds" let public transit agencies publish their transit data and developers write applications that consume
 that data in an interoperable way.
 
 This document provides guidelines on how to map GTFS feeds into FIWARE NGSI content.
 This work leverages on [LinkedGTFS specification](https://github.com/OpenTransport/linked-gtfs/blob/master/spec.md).
 Whenever possible the NGSI attributes map directly to GTFS fields. Nonethless for some Entity Types extra attributes are suggested in order
 to better support the data model using the NGSI information model. 
 
 ## General rules
 
 Entity Attributes (Properties or Relationships) are subject to the restrictions defined by the
 [GTFS specification](https://developers.google.com/transit/gtfs/reference/#term-definitions)
 If an Attribute is an enumeration its value shall be provided as per the GTFS specification (not LinkedGTFS). 
