# Animal data model: ShareBeef

## Introduction

The next diagram describes the beef chain considered in the ShareBeef project. In this diagram different stakeholders of the meat chain are described like some of their interactions.

![](../resources/diagram1.jpg)

During the execution of the project it will be necessary to define several entities to handle the information generated in the proposed solution. Within all these entities, the animal entity that is the center of the solution stands out in the first place

## Animal data model

### Model definition
The proposed animal data model has been made from a more general point of view, trying to adjust it to the information coming from the devices and sensors used in the UC.

The proposed model for the animal entity has the following properties:

- id: unique identifier
- type: Entity type. It must be equal to “Animal”
- species: Species to which the animal belongs
    - Attribute type: Text
    - Allowed values: (dairy cattle, beef cattle, sheep, goat, horse, pig)
    - Mandatory
- legalID: Legal ID of the animal:
    - Attribute type: Text
    - Mandatory
- birthdate: Animal’s birthdate
    - Attribute type: DateTime
    - Mandatory
- sex: Sex of the animal
    - Attribute type: Text
    - Allowed values: (female, male)
    - Mandatory
- breed: Breed of the animal
    - Attribute type: Text
    - Optional
- calvedBy: Mother of the animal
    - Attribute type: Relationship
    - Optional
- siredBy: Father of the animal
    - Attribute type: Relationship
    - Optional
- location: Location of the animal represented by a GeoJSON geometry.
    - Attribute type: geo:json.
    - Normative References: https://tools.ietf.org/html/rfc7946
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
- weight: The weight of the animal as a number
    - Attribute type: Number
    - Default unit: kg
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
- ownedBy: The owner of the animal:
    - Attribute type: Relationship
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
- locatedAt: AgridataParcel relationship:
    - Attribute type: Relationship
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
- phenologicalCondition: Phenological condition of the animal
    - Attribute type: Text
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
- reproductiveCondition: Reproductive condition of the animal
    - Attribute type: Text
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
 - healthCondition: Health condition of the animal
    - Attribute type: Text
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional
- feedWith: Food used for the animal
    - Attribute type: Relationship
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
        - Type: DateTime
    - Optional
- welfareCondition: Indicator of the animal welfare
    - Attribute type: Text
    - Attribute metadata:
        - timestamp: optional timestamp for the observed value.
            - Type: DateTime
    - Optional

### Example
Below a JSON example of the animal data model is shown:
```json
{
    "id":"8943423481234123",
    "type":"Animal",
    "species":{
        "value":"sheep"
    },
    "legalID":{
        "value":"ES142589652140"
    },
    "birthdate":{
        "type":"DateTime",
        "value":"2016-11-30T07:00:00.00Z"
    },
    "sex":{
        "value":"female"
    },
    "breed":{
        "value":"Meriana"
    },
    "calvedBy":{
        "type":"Relationship",
        "value":"6325415874"
    },
    "siredBy":{
        "type":"Relationship",
        "value":"1478515874"
    },
    "location":{
        "type":"geo:json",
        "value":{
            "type":"Point",
            "coordinates":[-4.754444444,41.640833333]
        },
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2019-02-28T09:23:00.00Z"
            }
        }
    },
    "weight":{
        "value":65.63,
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2019-02-21T09:23:14.00Z"
            }
        }
    },
    "ownedBy":{
        "type":"Relationship",
        "value":"32541789",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2019-01-14T14:23:14.00Z"
            }
        }
    },
    "locatedAt":{
        "type":"Relationship",
        "value":"145879654",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2019-03-22T18:23:31.00Z"
            }
        }
    },
    "phenologicalCondition":{
        "value":"lactacting animal",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2019-03-22T18:23:31.00Z"
            }
        }
    },
    "reproductiveCondition":{
        "value":"nonbreeding animal",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2018-02-22T18:23:31.00Z"
            }
        }
    },
    "healthCondition":{
        "value":"healthy",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2018-12-22T18:23:31.00Z"
            }
        }
    },
    "feedWith":{
        "type":"Relationship",
        "value":"241587",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2019-03-20T17:41:31.00Z"
            }
        }
    },
    "welfareCondition":{
        "value":"adequate",
        "metadata":{
            "timestamp":{
                "type":"DateTime",
                "value":"2018-12-22T18:23:31.00Z"
            }
        }
    }
}
```

### Diagram

![](../resources/diagram2.jpg)
