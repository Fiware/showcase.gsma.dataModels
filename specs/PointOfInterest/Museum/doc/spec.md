# Museum

## Description

<!-- textlint-disable no-dead-link -->

This entity contains a harmonised geographic description of a museum. It is used
in applications that use spatial data and is applicable to Tourism, Cultural,
and Smart City vertical segments and related IoT applications. Special thanks to
[TURESPAÑA](https://www.tourspain.es/en-us) who provided some examples which
inspired the development of this data model.

<!-- textlint-enable no-dead-link -->

## Data Model

A JSON Schema corresponding to this data model can be found
[here](http://fiware.github.io/dataModels/specs/PointOfInterest/Museum/schema.json).
This entity type has been designed as an extension of
[https://schema.org/Museum](https://schema.org/Museum) so that any property
specified by schema.org and which domain is `https://schema.org/Museum` can be
used by applications.

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `Museum`.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.
-   `source` : A sequence of characters giving the source of the entity data.
    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional
-   `name` : Name given to this museum.
    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory
-   `alternateName` : Alternative name given to this museum.

    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional

-   `description` : Description of this museum.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description]
    -   Optional

-   `location` : Location of this museum represented by a GeoJSON geometry,
    usually a `Point` or a `Polygon`.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.
-   `address` : Address of this museum.
    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.
-   `museumType` : Type of museum according to the exhibited content.
    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (`appliedArts`, `scienceAndTechnology`, `fineArts`,
        `music`, `history`, `sacredArt`, `archaeology`, `specials`,
        `decorativeArts`, `literature`, `medicineAndPharmacy`, `maritime`,
        `transports`, `military`, `wax`, `popularArtsAndTraditions`,
        `numismatic`, `unesco`, `ceramics`, `sumptuaryArts`, `naturalScience`,
        `prehistoric`, `ethnology`, `railway`, `mining`, `textile`, `sculpture`,
        `multiDisciplinar`, `painting`, `paleonthology`, `modernArt`,
        `thematic`, `architecture`, `museumHouse`, `cathedralMuseum`,
        `diocesanMuseum`, `universitary`, `contemporaryArt`, `bullfighting`).
        Other possible source for museum types not covered above is
        [Wikipedia](https://en.wikipedia.org/wiki/Category:Types_of_museum).
    -   Optional
-   `owner` : Museum's owner.

    -   Attribute type: [Text](https://schema.org/Text) or a reference to an
        entity of type [Person](https://schema.org/Person) or
        [Organization](https://schema.org/Organization)
    -   Optional

-   `featuredArtist` : Main featured artist(s) at this museum.

    -   Attribute type: List of references to entities of type
        [Person](https://schema.org/Person).
    -   Optional

-   `historicalPeriod` : Corresponds to the historical period(s) of the
    exhibitions made by this museum.
    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values:
        -   A ISO8601 time interval. For example `1920/1940`. The second element
            of the interval can be left empty to denote "till now".
        -   A comma separated list of years, for instance `1620,1625,1718`.
        -   A century, represented by a year pattern, for instance `19xx` would
            correspond to the twentieth century. And `196x` would correspond to
            the sixties decade.
    -   Optional
-   `artPeriod` : Corresponds to the art period(s) of the exhibitions made by
    this museum.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values:
        -   Those defined by
            [Wikipedia](https://en.wikipedia.org/wiki/Art_periods).
        -   Any other extended value needed by an application and not described
            by the above resource.
    -   Optional

-   `buildingType` : Type of building that hosts the museum.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Allowed values: (`prehistoricPlace`, `acropolis`, `alcazaba`,
        `aqueduct`, `alcazar`, `amphitheatre`, `arch`, `polularArchitecture`,
        `basilica`, `road`, `chapel`, `cartuja`, `nobleHouse`, `residence`,
        `castle`, `castro`, `catacombs`, `cathedral`, `cloister`, `convent`,
        `prehistoricCave`, `dolmen`, `officeBuilding`, `houseBuilding`,
        `industrialBuilding`, `militaryBuilding`, `hermitage`, `fortress`,
        `sculpturalGroups`, `church`, `garden`, `fishMarket`, `masia`,
        `masiaFortificada`, `minaret`, `monastery`, `monolith`, `walls`,
        `necropolis`, `menhir`, `mansion`, `palace`, `pantheon`, `pazo`,
        `pyramid`, `bridge`, `gate`, `arcade`, `walledArea`, `sanctuary`,
        `grave`, `synagogue`, `taulasTalayotsNavetas`, `theathre`, `temple`,
        `spring`, `tower`, `archeologicalSite`, `university`, `graveyard`,
        `fortifiedTemple`, `civilEngineering`, `square`, `seminar`,
        `bullfightingRing`, `publicBuilding`, `town`, `cavesAndTouristicMines`,
        `proCathedral`, `mosque`, `circus`, `burialMound`)
    -   Optional

-   `facilities` : Describes different facilities offered by this museum.
    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (`elevator`, `cafeteria`, `shop`, `auditory`,
        `conferenceRoom`, `audioguide`, `cloakRoom`, `forDisabled`, `forBabies`,
        `guidedTour`, `restaurant`, `ramp`, `reservation`) or any other value
        needed by an application.
    -   Optional
-   `openingHoursSpecification` : Opening hours specification for this museum.

    -   Normative References:
        [http://schema.org/openingHoursSpecification](http://schema.org/openingHoursSpecification)
    -   Attribute type: List of
        [OpeningHoursSpecification](https://schema.org/OpeningHoursSpecification)
    -   Optional

-   `touristArea` : Tourist area at which this museum is located. Precise
    semantics might depend on the application or target country or region. For
    instance `Costa del Sol`. + Attribute type:
    [Text](https://schema.org/Text) + Optional
-   `contactPoint` : Contact point for the museum.

    -   Attribute type:
        [https://schema.org/ContactPoint](https://schema.org/ContactPoint)

-   `refSeeAlso` : Reference to one or more related entities.
    -   Attribute type: List of References
    -   Optional

## Examples of use

    {
         "id": "Museum-Barcelona-MACBA-1234",
         "type": "Museum",
         "name": "Museo de Arte Contemporaneo de Barcelona",
         "alternateName": "MACBA",
         "description": "The MACBA was designed by the American architect Richard Meier and inaugurated in 1995.",
         "address": {
            "addressCountry": "ES",
            "addressLocality": "Barcelona",
            "streetAddress": "Plaza Dels Àngels, 1"
         },
         "museumType": ["fineArts"],
         "artPeriod": ["contemporary"],
         "facilities": ["shop", "cloakRoom", "guidedTour"],
         "location": {
            "type": "Point",
            "coordinates": [ 2.1668771521199393, 41.38302235796602]
         },
         "openingHoursSpecification": [
            {
                "opens":  "11:00",
                "closes": "19:30",
                "dayOfWeek": "Mo, Wed, Thu, Fr"
            },
            {
                "opens": "10:00",
                "closes": "21:00",
                "dayOfWeek": "Sat"
            },
            {
                "opens": "10:00",
                "closes": "15:00",
                "dayOfWeek": "Sun"
            }
        ],
        "touristArea": "Barcelona-Capital",
        "source": "http://www.tourspain.es"
    }

## Use it with a real service

Coming soon

## Open Issues
