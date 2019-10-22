# NGSI-LD FAQ

This FAQ compilation is intended to clarify the NGSI-LD specification by
providing answers to common questions.

A tutorial that can complement this FAQ can be found at 
[https://github.com/FIWARE/tutorials.Linked-Data](https://github.com/FIWARE/tutorials.Linked-Data).

### Q: What implementations of NGSI-LD are available?

-   Orion-LD: [https://github.com/Fiware/context.Orion-LD](https://github.com/Fiware/context.Orion-LD)
-   Scorpio:  [https://github.com/ScorpioBroker/ScorpioBroker](https://github.com/ScorpioBroker/ScorpioBroker)
-   Djane:    [https://github.com/sensinov/djane/](https://github.com/sensinov/djane/)

### Q: What are the main (essential) differences between NGSI v2 and NGSI-LD?

In summary, the main differences are the following:

-   The underlying Data Model is the
    [Property Graph Data Model](https://github.com/Fiware/NGSI-LD_Wrapper/blob/master/doc/instantiation.png).
-   Entity IDs shall be **URIs** (URLs or URNs).
-   The `metadata` dictionary disappears. Metadata are represented by nested
    Properties of Properties.
-   There is some "metadata" standardised (`unitCode` for expressing units,
    `observedAt` for expressing timestamps, ...)
-   There is a new type of Attribute `Relationship` intended to link one Entity
    to another Entity. That is done through the `object` member.
-   Geospatial properties are represented using the Attribute type
    `GeoProperty`.
-   The `type` of Attributes can only be `Property`, `Relationship` or
    `GeoProperty`.
-   A JSON-LD `@context` (a hash map used to map member names to URIs) can be
    added to Entities to provide Fully Qualified Names (URIs) associated to
    terms. That is somewhat "similar" to the concept of XML namespaces.
-   Overall the REST API is quite similar (even simpler) than NGSI v2, although
    subscription and registration payloads change a bit (but they are the same
    in essence).

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
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

For each FIWARE Data Model there is an example Entity encoding it in NGSI-LD.
For instance,
[here](https://github.com/FIWARE/data-models/blob/master/specs/PointOfInterest/Museum/example-normalized-ld.jsonld)

### Q: Could you give me some examples of a JSON-LD `@context`?

You can find an example [here](https://schema.lab.fiware.org/ld/context).

### Q: What URI should I use to reference the FIWARE Data Models `@context`?

The sources of truth for the FIWARE Data Models `@context` are [https://fiware.github.io/data-models/context.jsonld](https://fiware.github.io/data-models/context.jsonld) and [https://fiware.github.io/data-models/full-context.jsonld](https://fiware.github.io/data-models/full-context.jsonld). 
The latter includes both the FIWARE Data Models `@context` and the Core `@context`. 

The full `@context` is also available at 
[https://schema.lab.fiware.org/ld/context](https://schema.lab.fiware.org/ld/context)

When it comes to referencing the FIWARE Data Models `@context` 
in your NGSI-LD Entities, there are three different options: 

*   Use the FIWARE Lab URI [https://schema.lab.fiware.org/ld/context](https://schema.lab.fiware.org/ld/context).
*   Use the GitHub URI [https://fiware.github.io/data-models/full-context.jsonld](https://fiware.github.io/data-models/full-context.jsonld).
*   Host a copy of the Data Models `@context` file within your own premises and use a URI referencing a local server

The main advantage of the first method, is that the FIWARE Lab URI is convenient, as it is shorter and cleaner,
however it does depend on a redirection made by the FIWARE Lab Infrastructure,  which does not have 100% 
availability guaranteed. The GitHub URI is longer, but in general GitHub has higher guaranteed availability 
than FIWARE Lab. The self-hosting method, ensures that the `@context` will only be updated when you chose to do and
an on-premise URI can help to solve issues faced by applications that are deployed behind firewalls, however your
local copy of the `@context` file will not include recent changes made to the standard models defined by the `@context`.

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

Remember that in NGSI-LD timestamps **must** always be expressed using UTC i.e.
a trailing 'Z' **must** always be present.

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
        "https://schema.lab.fiware.org/ld/context",
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
        "https://schema.lab.fiware.org/ld/context",
        "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

### Q: Is `application/json` a supported MIME type?

Yes. However, when using it the LD `@context` has to be externally
provided, or no JSON-LD `@context` at all. In the latter case Entities will be
under the Default `@context`. You can see an example
[here](https://github.com/Fiware/NGSI-LD_Tests/blob/master/contextProvision/create_entity_with_ldcontext_test.js#L18)

### Q: What happens if I only use `application/json` content without worrying about the `@context` member?

Nothing, i.e. if you are working in your own application and your data model is
somewhat "private" that is perfectly OK. It is somewhat similar as using XML
content without namespaces.

However, we recommend to use JSON-LD `@context` and that can be easily
abstracted out by a convenience library.

### Q: What is the JSON-LD Link header?

It is a standard HTTP Link Header intended to provide a `@context` in two
scenarios:

-   when `application/json` is used as MIME type.
-   in GET and DELETE operations to specify what is the `@context` to be used
    for mapping types or attribute names to Fully Qualified Names (URIs).

### Q: Could you put an example of a JSON-LD HTTP Link Header?

For instance, the Link header to address the FIWARE Data Models would be:

```
Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"
```

**Please note that only one JSON-LD Link header is allowed per HTTP Request**

### Q: Is the `@context` mandatory?

For JSON-LD content (`application/ld+json`), yes it shall accompany each Entity
payload as a `@context` member. For JSON content (`application/json`) it can
**only** be specified through the JSON-LD HTTP Link header.

**Please note that only one JSON-LD Link header is allowed per HTTP Request**

### Q: If I have a `@context` which references multiple URIs how can I reference it through the HTTP `Link` header?

As the `Link` header can only reference one JSON-LD `@context` it is necessary
to create a **wrapper** `@context`.

Below you can see an example of JSON-LD `@context` wrapping, in which FIWARE
Data Models and schema.org `@context` are put together.

```
{
   "@context": [
      "http://schema.lab.fiware.org/ld/context",
      "http://schema.org"
   ]
}
```

If you set up an endpoint URI to serve the content above (serving it with MIME
type `application/ld+json`) then you can reference it from a HTTP `Link` header.
Please note that in many cases that would not be necessary as , for instance,
the FIWARE Data Models `@context` already contains the proper references to
schema.org.

### Q: What happens if an Entity ID is a URL and I use it in a resource like `/entities/{entityId}`?

Nothing. Entity IDs have to be percent encoded as mandated by IETF
specifications.

### Q: What is the Core `@context`?

It is the JSON-LD `@context` where all the NGSI-LD API Core terms are defined.
It can be found at
[https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld](https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld)

**The Core `@context` terms cannot be overwritten by applications**

### Q: What is the Default `@context`?

Actually, the role of Default `@context`is played by the Core `@context` itself, which does include a default `@vocab` rule to map unknown terms (i.e. those for which no correspondance is found in the user `@context`) to a default URI.

### Q: Do I always need to provide the Core `@context` when invoking API operations?

It **is not** necessary. The Core `@context` is always implicit when processing
API requests. However, when generating API responses the Core `@context` is
always included to facilitate the work of JSON-LD processors that might be
upstream.
