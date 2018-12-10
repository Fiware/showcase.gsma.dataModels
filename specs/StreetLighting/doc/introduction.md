# Street Lighting Data Models

Streetlights, commonly known as 'lamp-posts', are designed to make the streets
safer for pedestrians and drivers. These data models are intended to model
streetlights and all their controlling equipment towards energy-efficient and
effective urban illuminance.

It encompasses the following entity types:

-   [Streetlight](../Streetlight/doc/spec.md). It represents a particular
    instance of a streetlight. A streetlight is composed by a lantern and a
    lamp. Such elements are mounted on a column (pole), wall or other structure.
-   [StreetlightGroup](../StreetlightGroup/doc/spec.md). It represents a group
    of streetlights being part of the same circuit and controlled together by an
    automated system.
-   [StreetlightModel](../StreetlightModel/doc/spec.md). It represents a model
    of streetlight composed by a specific supporting structure model, a lantern
    model and a lamp model. A streetlight instance will be based on a certain
    streetlight model.
-   [StreetlightControlCabinet](../StreetlightControlCabinet/doc/spec.md). It
    represents automated equipment, usually on street, typically used to control
    a group(s) of streetlights, i.e. one or more circuits.
