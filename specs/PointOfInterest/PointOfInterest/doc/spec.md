# Point of interest

## Description

This entity contains a harmonised geographic description of a Point of Interest. This entity is
used in applications that use spatial data and is applicable to Automotive, Environment,
Industry and Smart City vertical segments and related IoT applications. This data model
has been created in cooperation with the GSMA and the members of the [IoT Big Data Project](http://www.gsma.com/iot/iot-big-data/). 

## Data Model

A JSON Schema corresponding to this data model can be found [here](http://fiware.github.io/dataModels/specs/PointOfInterest/PointOfInterest/schema.json)

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `PointOfInterest`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Read-Only. Automatically generated.
    
+ `source` : A sequence of characters giving the source of the entity data.
    + Attribute type: [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    + Optional    
    
+ `name` : Name of this point of interest.
    + Normative References: [https://schema.org/name](https://schema.org/name)
    + Mandatory
    
+ `alternateName` : Alternative name for this point of interest.
    + Normative References: [https://schema.org/alternateName](https://schema.org/alternateName)
    + Optional

+ `description` : Description of this point of interest.
    + Normative References: [https://schema.org/description](https://schema.org/description)
    + Optional

+ `location` : Location of the point of interest represented by a GeoJSON geometry, usually a `Point`. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not defined. 
    
+ `address` : Civic address of this point of interest.
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present.
    
+ `category` : Category of this point of interest. 
    + Attribute type: List of [Text](https://schema.org/Text)
    + Allowed values: Those defined by the [Factual taxonomy](https://github.com/Factual/places/blob/master/categories/factual_taxonomy.json).
    For instance the value `113` corresponds to beaches, and the value `311` corresponds to museums. 
    + Mandatory
    
+ `contactPoint` :  Contact point of this point of interest.
    + Normative references: [https://schema.org/contactPoint](https://schema.org/contactPoint)
    + Optional    
    
+ `refSeeAlso` : Reference to one or more related entities that may provide extra,
specific information about this point of interest.
    + Attribute type: List of References
    + Optional
    
## Examples of use

    {
        "id": "PointOfInterest-A-Concha-123456",
        "type": "PointOfInterest",
        "name": "Playa de a Concha",
        "description": "La Playa de A Concha se presenta como una continuación de la Playa de Compostela, una de las más frecuentadas de Vilagarcía.",
        "address": {
          "addressCountry": "ES",
          "addressLocality": "Vilagarcía de Arousa"
        },
        "category": ["113"],
        "location": {
          "type": "Point",
          "coordinates": [
            -8.768460000000001,
            42.60214472222222
          ]
        },
        "source": "http://www.tourspain.es",
        "refSeeAlso": ["Beach-A-Concha-123456"]
    }

    
## Use it with a real service

The instance described [here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing) has been set up by the FIWARE Community.

Get POIs around Fira Montjuic (2 Kms around)

```curl -S --header 'fiware-service:poi' --header 'fiware-servicepath:/Spain' --header 'x-auth-token:dd3a796995294dc5b6d7bf2cdb36e15f' “http://130.206.118.244:1027/v2/entities?type=PointOfInterest&attrs=location,name&orderBy=geo:distance&georel=near;maxDistance:2000&geometry=point&coords=41.3730751,2.1482742&options=keyValues”```


## Open Issues

