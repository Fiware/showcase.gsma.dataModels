# Data models guidelines

This is a set of guidelines for defining new data models. 

## Syntax

+ Use English terms, preferably American English.
+ Use camel case syntax for attribute names (`camelCase`). 
+ Entity type names must start with a Capital letter, for instance, `WasteContainer`.
+ Use names and not verbs for attribute names, ex. `name`, qualifying it when necessary, ex. `totalSpotNumber` or `dateCreated`.
+ Avoid plurals in attribute names, but state clearly when a list of items fits. Ex. `category`. 

## Reuse

+ Check for the existence of the same attribute on any of the other models and reuse it, if pertinent. 
+ Have a look at [schema.org](http://schema.org) trying to find a similar term with the same semantics.
+ Try to find common used ontologies or existing standards well accepted by the Community, or by goverments, agencies, etc.
For instance, [Open311](http://www.open311.org/) for civic issue tracking or [Datex II](http://www.datex2.eu/) for transport systems. 

## Data types

+ When possible reuse schema.org data types (`Text`, `Number`, `DateTime`, `StructuredValue`, etc.).

## Attribute definition

+ Enumerate the allowed values for each attribute. Generally speaking it is a good idea to leave it open for applications
to extend the list, provided the new value is not semantically covered by any of the existing ones.

+ State clearly what attributes are mandatory and what are optional. If needed state clearly what is the meaning of a
`null` value. 

## Units

+ Define a default unit for magnitudes. Normally it will be the unit as stated by the international system of units.

+ If a quantity is expressed in a different unit than the default one, use the [unitCode](http://schema.org/unitCode) metadata
attribute.

## Relative values

+ Use values between `0` and `1` for relative quantities, which represent attribute values
such as `relativeHumidity`, `precipitationProbability`, etc. 

## Modelling location

+ Use `address` attribute for civic locations as per [schema.org](http://schema.org/address)

+ Use `location` attribute for geographical coordinates. Ideally use GeoJSON for codifying geospatial properties. That works
from Orion 1.2 on. If not use, old NGSI version 1 type `coords`.

## Modelling linked data

+ When an entity attribute is used as a link to other entities name
it with the prefix `ref` plus the name of the target (linked) entity type. For instance `refStreetlightModel`, represents an attribute
which contains a reference to an entity of type `StreetlightModel`. 

## Date Attributes

+ Attribute type must be `DateTime`.

+ Use the `date` prefix for naming entity attributes representing dates (or complete timestamps). Ex. `dateLastEmptying`. 

+ `dateCreated` must be used to denote the (digital) entity's creation date.

+ `dateModified` must be used to denote the (digital) entity's last update date. 

+ `dateCreated` and `dateModified` are special entity attributes provided off-the-shelf by NGSIv2 implementations.
Be careful because they can be different
than the actual creation or update date of the real world entity represented by its corresponding digital entity.

+ When necessary define additional attributes to capture precisely all the details about dates.
For instance, to denote the date at which a weather forecast was delivered an attribute named `dateIssued` can be used.
In that particular case just reusing `dateCreated` would be incorrect because
the latter would be the creation date of the (digital) entity representing the weather forecast which typically might have a delay. 

## Dynamic attributes

+ Use a metadata attribute named `timestamp` for capturing the last update timestamp of a dynamic attribute. Please note
that this is the actual date at which the measured value was obtained (from a sensor, by visual observation, etc.), and that
date might be different than the date (metadata attribute named `dateModified` as per NGSIv2) at which the attribute
of the digital entity was updated, as typically there might be delay,
specially on IoT networks which deliver data only at specific timeslots. 

## Some of the most used attributes

In case of doubt check other existing models! 

+ `name`
+ `alternateName`
+ `description`
+ `serialNumber`
+ `category`
+ `features`
+ `source`
+ `relativeHumidity`
+ `temperature`
