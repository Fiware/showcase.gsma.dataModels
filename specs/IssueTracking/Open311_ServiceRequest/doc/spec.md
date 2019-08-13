# Open 311 Service Request

An entity of type `ServiceRequest` is an acceptable Open 311 service request.
Such entity encompasses all the properties defined by Open 311 at
[POST Service Request](http://wiki.open311.org/GeoReport_v2/#post-service-request)
and
[GET Service Request](http://wiki.open311.org/GeoReport_v2/#get-service-request).

Using this data model and a FIWARE NGSI version 2 implementation it is
straightforward to implement a service compliant with the Open 311
specifications.

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier. It might be equal to a string
    representation of `service_request_id`.

-   `type` : It must be `Open311ServiceRequest`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Property. Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information
    -   Attribute type: Property. URL
    -   Optional

The following fields defined by Open 311 are allowed to be attributes of this
entity type:

-   `service_request_id`

-   `jurisdiction_id`

-   `service_code`

-   `service_name`

-   `description`

-   `agency_responsible`. Please note that this is semantically equivalent to
    the [provider](http://schema.org/provider) property (name subproperty) of
    schema.org.

-   `service_notice`

-   `address_string`

-   `address_id`

-   `zipcode`

-   `status`

-   `status_notes`

-   `requested_datetime`

-   `updated_datetime`

-   `expected_datetime`

-   `lat`

-   `long`

-   `media_url`

-   `email`

-   `first_name`

-   `last_name`

-   `phone`

-   `device_id`

-   `account_id`

-   `address`. If used it must be renamed to `open311:address`.

_All attribute types must be coherent with the Open 311 definitions.
Applications must use the types `Text`, `Number` and `DateTime` accordingly._

To support FIWARE NGSI v2 geoqueries concerning Open311 Service Requests the
following property must be added:

-   `location` : Location of the area on which this service request is
    concerned.
    -   Attribute type: Property. GeoJSON geometry.
    -   Mandatory if the service request is geolocated.

Additionally, applications might use the following standard schema.org
structured properties:

-   [address](http://schema.org/address).
-   [contactPoint](http://schema.org/contactPoint)

_Note 1: Applications are responsible of keeping consistency between the
`location` field and the Open 311 `lat` and `long` fields_. _The same can be
said about_:

-   `address` property and the Open 311 fields related to it (`zipcode`,
    `address_string`, etc.).
-   `contactPoint` property and fields like (first_name, last_name, etc.)\*

_Note 2: This NGSI data model does not allow the use of `address` property
defined by Open 311. This has been done on purpose as we want to keep the
`address` property consistent with
[http://schema.org/address](http://schema.org/address). Applications are
encouraged to use `address_string` instead and do the corresponding mapping at
the adaptation layer._

To support the `attribute` parameter of Open 311 service requests this NGSI data
model adds the following property (please note it has been pluralized, to keep
consistency with `ServiceType`):

-   `attributes` : It is a dictionary with a key per attribute defined by the
    corresponding `ServiceType`. The key-value is always an array of strings. If
    an attribute is singled valued then such array will only contain one
    element.
    -   Attribute type: Property. [StructuredValue](https://schema.org/StructuredValue).
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "service-request:638344",
    "type": "Open311ServiceRequest",
    "status": {
        "value": "closed"
    },
    "description": {
        "value": "Acera en mal estado con bordillo partido en dos"
    },
    "service_code": {
        "value": 234
    },
    "status_notes": {
        "value": "Duplicate request."
    },
    "service_name": {
        "value": "Aceras"
    },
    "service_request_id": {
        "value": 638344
    },
    "updated_datetime": {
        "type": "DateTime",
        "value": "2010-04-14T06:37:38-08:00"
    },
    "address_string": {
        "value": "Calle San Juan Bautista, 2"
    },
    "requested_datetime": {
        "type": "DateTime",
        "value": "2010-04-14T06:37:38-08:00"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.164485591715449, 40.62785133667262]
        }
    },
    "attributes": {
        "value": {
            "ISSUE_TYPE": ["Bordillo"]
        }
    },
    "expected_datetime": {
        "type": "DateTime",
        "value": "2010-04-15T06:37:38-08:00"
    },
    "agency_responsible": {
        "value": "Ayuntamiento de Ciudad"
    },
    "media_url": {
        "value": "http://exaple.org/media/638344.jpg"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "service-request:638344",
    "type": "Open311ServiceRequest",
    "service_request_id": 638344,
    "status": "closed",
    "status_notes": "Duplicate request.",
    "service_name": "Aceras",
    "service_code": 234,
    "description": "Acera en mal estado con bordillo partido en dos",
    "agency_responsible": "Ayuntamiento de Ciudad",
    "requested_datetime": "2010-04-14T06:37:38-08:00",
    "updated_datetime": "2010-04-14T06:37:38-08:00",
    "expected_datetime": "2010-04-15T06:37:38-08:00",
    "address_string": "Calle San Juan Bautista, 2",
    "attributes": {
        "ISSUE_TYPE": ["Bordillo"]
    },
    "location": {
        "type": "Point",
        "coordinates": [-3.164485591715449, 40.62785133667262]
    },
    "media_url": "http://exaple.org/media/638344.jpg"
}
```

### LD Example

Sample uses the NGSI-LD representation

```json
{
    "id": "urn:ngsi-ld:Open311ServiceRequest:service-request:638344",
    "type": "Open311ServiceRequest",
    "status": {
        "type": "Property",
        "value": "closed"
    },
    "description": {
        "type": "Property",
        "value": "Acera en mal estado con bordillo partido en dos"
    },
    "service_code": {
        "type": "Property",
        "value": 234
    },
    "status_notes": {
        "type": "Property",
        "value": "Duplicate request."
    },
    "service_name": {
        "type": "Property",
        "value": "Aceras"
    },
    "service_request_id": {
        "type": "Property",
        "value": 638344
    },
    "updated_datetime": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2010-04-14T06:37:38-08:00"
        }
    },
    "address_string": {
        "type": "Property",
        "value": "Calle San Juan Bautista, 2"
    },
    "requested_datetime": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2010-04-14T06:37:38-08:00"
        }
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-3.164485591715449, 40.62785133667262]
        }
    },
    "attributes": {
        "type": "Property",
        "value": {
            "ISSUE_TYPE": ["Bordillo"]
        }
    },
    "expected_datetime": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2010-04-15T06:37:38-08:00Z"
        }
    },
    "agency_responsible": {
        "type": "Property",
        "value": "Ayuntamiento de Ciudad"
    },
    "media_url": {
        "type": "Property",
        "value": "http://exaple.org/media/638344.jpg"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

## Test it with real services

## Open issues
