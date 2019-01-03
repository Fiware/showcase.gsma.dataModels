# Aero Allergen Observed

## Description

This entity models aero allergens observed at a given location and related
overall allergen risk.

This data model has been developed based on
[GSMA](http://www.gsma.com/connectedliving/iot-big-data/). Aero allergens
strictly depends on the geographical location. Common Aero allergens in Europe
may be quite different from the ones in US due to the different biological
species. A list of commonly used aero allergens in Europe can be found on
[polleninfo.org](https://www.polleninfo.org/en/allergy/profiles/) a web site
maintained by the European Aeroallergen Network. A World Health Organization
(WHO) Allergen Nomenclature (covering not only aero transported allergens) is
available at [http://www.allergen.org](http://www.allergen.org).

## Data Model

A JSON Schema corresponding to this data model can be found
[here](http://fiware.github.io/dataModels/specs/Environment/AeroAllergenObserved/schema.json).

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `AeroAllergenObserved`.

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `location` : Location of the aero allergens observation represented by a
    GeoJSON geometry.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.
-   `address` : Civic address of the aero allergens observation. Sometimes it
    corresponds to the aero allergens station address.
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.
-   `dateObserved` : The date and time of this observation in ISO8601 UTCformat.
    It can be represented by a specific time instant or by an ISO8601 interval.
    -   Attribute type: [DateTime](https://schema.org/DateTime) or an ISO8601
        interval represented as [Text](https://schema.org/Text).
    -   Mandatory
-   `source` : A sequence of characters giving the source of the entity data.
    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional
-   `allergenRisk` : Overall allergen risk corresponding to the aero allergens
    observed.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Example values defined by the
        [European Aeroallergen Network](https://www.ean-net.org/en/): (`none`,
        `low`, `moderate`, `high`, `veryHigh`). As this can be different between
        countries, regulations or implementations, the set of allowed values
        will depend on the reference specification used. It is recommended that
        implementations use the same naming conventions as exemplified above
        (lower case starting words, camel case when compound terms are used)
    -   Attribute metadata:
        -   `referenceSpecification` : Specification that must be taken as
            reference when interpreting the supplied qualitative value.
        -   Type: [Text](https://schema.org/Text) or
            [URL](https://schema.org/URL)
        -   Mandatory
    -   Optional

-   `refDevice` : A reference to the device(s) which captured this observation.
    -   Attribute type: Reference to an entity of type `Device`
    -   Optional

### Representing aero allergens concentration

To describe the different aero allergens concentrations, _for each_ aero
allergens we use an attribute that _MUST_ refers exactly to the conventional
name of the allergen (usually the latin name of the associated plant) to measure
the concentration (usually in grains per cubic meter `gr/m3`). e.g. `alnus` to
measure the concentration of [alnus](https://en.wikipedia.org/wiki/Alder) pollen
(_Alder_ is the common english name for _Alnus_).

The structure of such an attribute will be as follows:

-   Attribute name: Equal to the name of the allergen, for instance `alnus`. A
    list of commonly used aero allergens in Europe can be found on
    [polleninfo.org](https://www.polleninfo.org/en/allergy/profiles/) a web site
    maintained by the European Aeroallergen Network. A World Health Organization
    (WHO) Allergen Nomenclature (covering not only aero transported allergens)
    is available at [http://www.allergen.org](http://www.allergen.org).

-   Attribute type: [Number](https://schema.org/Number)

-   Attribute value: corresponds to the concentration of the allergen as a
    number.

-   Attribute metadata:
    -   `timestamp` : optional timestamp for the observed value in ISO8601
        format. It can be omitted if the observation time is the same as the one
        captured by the `dateObserved` attribute at entity level.
        -   Type: [DateTime](https://schema.org/DateTime)
    -   `unitCode` : The unit code (text) of measured concentration (usually the
        unit adopted is grains per cubic meter: `gr/m3`).
        -   Type: [Text](https://schema.org/Text)
        -   Optional
    -   `description` : short description of the allergen
        -   Type: [Text](https://schema.org/Text)
        -   Optional

### Representing qualitative levels of aero allergens

To describe the aero allergens qualitative levels, _for each_ aero allergens we
use an attribute that _MUST_ refers exactly to the conventional name of the
allergen (usually the latin name of the associated plant) concatenated with the
string `_Level`, e.g. `alnus_Level` to measure the qualitative level for a given
concentration of [alnus](https://en.wikipedia.org/wiki/Alder) pollen.

-   Attribute name: Equal to the name of the allergen plus the suffix `Level`,
    for instance `alnus_Level`.
-   Attribute type: [Text](https://schema.org/Text)
-   Attribute value: Example values defined by the
    [European Aeroallergen Network](https://www.ean-net.org/en/): (`none`,
    `low`, `moderate`, `high`, `veryHigh`). As this can be different between
    countries, regulations or implementations, the set of allowed values will
    depend on the reference specification used. It is recommended that
    implementations use the same naming conventions as exemplified above (lower
    case starting words, camel case when compound terms are used)
-   Attribute metadata:
    -   `description` : short description of the measurand and its related
        qualitative level
        -   Type: [Text](https://schema.org/Text)
        -   Optional
    -   `referenceSpecification` : Specification that must be taken as reference
        when interpreting the supplied qualitative value.
        -   Type: [Text](https://schema.org/Text) or
            [URL](https://schema.org/URL)
        -   Mandatory

### Representing allergenicity category of aero allergens

To describe the allergenicity category of aero allergens, _for each_ aero
allergens we use an attribute that _MUST_ refers exactly to the conventional
name of the allergen (usually the latin name of the associated plant)
concatenated with the string `_Allergenicity`, e.g. `alnus_Allergenicity` to
describe the allergenicity level of [alnus](https://en.wikipedia.org/wiki/Alder)
pollen.

-   Attribute name: Equal to the name of the allergen plus the suffix
    `_Allergenicity`, for instance `alnus_Allergenicity`.
-   Attribute type: [Text](https://schema.org/Text)
-   Attribute value: Example values defined by the
    [Spanish Network for Aerobiology](https://www.uco.es/rea/infor_rea/interpretacion.html):
    (`1`, `2`, `3`, `4`). As this can be different between countries,
    regulations or implementations, the set of allowed values will depend on the
    reference specification used. It is recommended that implementations use the
    same naming conventions as exemplified above (lower case starting words,
    camel case when compound terms are used)
-   Attribute metadata:
    -   `description` : short description of the measurand and its related
        qualitative level
        -   Type: [Text](https://schema.org/Text)
        -   Optional
    -   `referenceSpecification` : Specification that must be taken as reference
        when interpreting the supplied qualitative value.
        -   Type: [Text](https://schema.org/Text) or
            [URL](https://schema.org/URL)
        -   Mandatory

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

### key-value pairs Example

```json
{
    "id": "AeroAllergenObserved-CDMX-Pollen-Cuajimalpa",
    "type": "AeroAllergenObserved",
    "alnus_Level": "moderate",
    "alnus": 40,
    "alnus_Allergenicity": "3",
    "casuarina_Level": "low",
    "casuarina": 1,
    "casuarina_Allergenicity": "3",
    "allergenRisk": "moderate",
    "address": {
        "addressCountry": "MX",
        "addressLocality": "Ciudad de México",
        "streetAddress": "Colegio Franco-Inglés"
    },
    "dateModified": "2018-02-16T17:24:39.00Z",
    "dateObserved": "2018-02-11T00:00:00.00Z",
    "location": {
        "type": "Point",
        "coordinates": [-99.276977, 19.381877]
    },
    "source": "http://rema.atmosfera.unam.mx/rema/"
}
```

## Use it with a real service

TBD
