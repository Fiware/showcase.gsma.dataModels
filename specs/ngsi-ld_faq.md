# NGSI-LD FAQ

This FAQ compilation is intended to clarify the NGSI-LD specification by
providing answers to common questions.

### Q: What are the main (essential) differences between NGSI v2 and NGSI-LD?

In summary, the main differences are the following:

-   The underlying Data Model is the
    [Property Graph Data Model](https://github.com/Fiware/NGSI-LD_Wrapper/blob/master/doc/instantiation.png).
-   Entity IDs shall be URIs (URLs or URNs).
-   The `metadata` dictionary disappears. Metadata are represented by nested
    Properties of Properties.
-   There is some "metadata" standardised (`unitCode`, `observedAt`, ...)
-   There is a new type of Attribute `Relationship` intended to link one Entity
    to another Entity. That is done through the `object` member.
-   Geospatial properties are represented using the Attribute type
    `GeoProperty`.
-   The `type` of Attributes can only be `Property`, `Relationship` or
    `GeoProperty`.
-   A JSON-LD `@context` (a hash used to map member names to URIs) can be added
    to Entities to provide Fully Qualified Names (URIs) associated to terms.
    That is somewhat "similar" to XML namespaces.
-   Overall the REST API is quite similar (even simpler) than the NGSI v2,
    although subscription payloads change a bit (but they are the same in
    essence).

### Q: Could you give me some examples of NGSI-LD payloads?

```json
{
    "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
    "type": "AirQualityObserved",
    "dateObserved": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2018-08-07T12:00:00Z"
        }
    },
    "NO2": {
        "type": "Property",
        "value": 22,
        "unitCode": "GP",
        "accuracy": {
            "type": "Property",
            "value": 0.95
        }
    },
    "refPointOfInterest": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/jsonldcontext.jsonld",
        "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

Additional examples can be found
[here](https://github.com/Fiware/NGSI-LD_Tests/blob/master/contextProvision/create_entity_with_ldcontext_test.js#L16)

### Q: Could you give me some examples of a JSON-LD `@context`?

You can find an example
[here](https://schema.lab.fiware.org/ld/jsonldcontext.jsonld).

### Q: What is a Property of a Property / Relationship and all the combinations?

It is similar to NGSI v2 metadata. In NGSIv2, in the example above, the Property
`accuracy` would have been represented as a member of the `metadata` dictionary.

### Q: But, Property and Relationship can be arbitrarily nested?

Yes, but only one or two nesting levels could make sense in a real world
scenario.

### Q: What is `observedAt`?

It is a "timestamp" associated to a Property or Relationship. See the example
below. In NGSI v2 it is usually specified using the `timestamp` metadata
attribute.

```json
{
    "id": "urn:ngsi-ld:WasteContainer:RZ:Obsv4567",
    "type": "WasteContainer",
    "fillingLevel": {
        "type": "Property",
        "value": 0.85,
        "observedAt": "2017-02-07T16:00:00Z"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-2, 35]
        }
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/jsonldcontext.jsonld",
        "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

### Q: How geo-location is represented?

See the example above. In essence an Attribute of type `GeoProperty` plus a
[GeoJSON Geometry](https://tools.ietf.org/html/rfc7946#page-7) value.

### Q: How DateTime is represented (e.g. timestamps, dates, time)?

```json
{
    "id": "urn:ngsi-ld:WeatherObserved:RZ:Obsv4567",
    "type": "WeatherObserved",
    "dateObserved": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2018-08-07T12:00:00Z"
        }
    },
    "temperature": {
        "type": "Property",
        "value": 22
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/jsonldcontext.jsonld",
        "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

### Q: Is `application/json` a supported MIME type?

Yes, indeed. However, the `@context` has to be externally provided, or no
`@context` at all. In the latter case Entities will be under the Default
`@context`. You can see an example
[here](https://github.com/Fiware/NGSI-LD_Tests/blob/master/contextProvision/create_entity_with_ldcontext_test.js#L18)

### Q: What happens if I only use `application/json` content without worrying about the `@context` member?

Nothing, i.e. if you are working in your own application and your data model is
somewhat "private" that is perfectly OK. It is somewhat similar as using XML
content without namespaces.

### Q: What is the JSON-LD Link header?

It is a standard HTTP Link Header intended to provide a `@context` in two
scenarios: 1. when `application/json` is used as MIME type. 2. in GET and DELETE
operations to specify what is the `@context to be used for mapping types or
attribute names to Fully Qualified Names (URIs).

### Q: Could you put an example of a JSON-LD HTTP Link Header?

You can see an example
[here](https://github.com/Fiware/NGSI-LD_Tests/blob/master/contextConsumption/query_entities_with_ld_context_test.js#L13)

### Q: Is the `@context` mandatory?

For JSON-LD content, yes. (`application/ld+json`). For JSON content it can
**only** be specified through the JSON-LD HTTP Link header.

### Q: What happens if an Entity ID is a URL and I use it in a resource `/entities/{entityId}`?

Nothing. Entity IDs have to be percent encoded as mandated by IETF
specifications.

### Q: Where I can find the Default `@context`?

[Here](https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/defaultContext/defaultContext.jsonld)

### Q: What is the Core `@context`?

It is the JSON-LD `@context` where all the NGSI-LD Core terms are defined. It
can be found at
[http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld](http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld)
