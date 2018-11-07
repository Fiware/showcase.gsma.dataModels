# MediaEvent

## Description

Base for all events raised by elements in the media server

## Data Model

-   `id` : Entity's unique identifier.

-   `type` : Entity type. It must be equal to `MediaEvent`

-   `eventType` : Type of event that was raised.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Mandatory

-   `dateCreated` : Time when event raised.

    -   Attribute type: [DateTime](https://schema.org/DateTime) + Mandatory

-   `mediasource` : Object´s technical information that raised the event
    -   Attribute type: [StructuredValue](http://schema.org/StructuredValue)
        See:[MediaSource](https://fiware.github.io/dataModels/specs/Media/mediasource-schema.json#/definitions/MediaSource)
    -   Optional
-   `data`: Any serializable object that is attached to the event. Eg:
    plate-number + Attribute type:
    [StructuredValue](http://schema.org/StructuredValue) + Optional

-   `refSeeAlso` : Reference to one related entities that may provide extra,
    specific information about this Media Event

    -   Attribute type: Reference.
    -   Optional

-   `deviceSource`: The Device entity that has raised the event. + Attribute
    type: [Device](../Device/Device/doc/spec.md) + Optional

-   observedEntities: Entities created updated or just observed by this event.
    Eg: for a plate-number the car associated to it.
    -   Attribute type: List of Orion Entities.
    -   Optional

## Example

    {
      "id": "mediaEvent:1509702324600",
      "type": "MediaEvent",
      "eventType": "plate-detected",
      "mediasource": {
        "name": "03ea110c-0ab2-4b19-8618-57f474721c86_kurento.MediaPipeline/28e4ae84-4e96-43bb-a812-538f7950b75f_platedetector.PlateDetectorFilter",
        "creationTime": "2017-11-03T10:45:19Z",
        "sendTagsInEvents": false,
        "parent": {
          "name": "03ea110c-0ab2-4b19-8618-57f474721c86_kurento.MediaPipeline",
          "creationTime": "2017-11-03T10:45:19Z",
          "sendTagsInEvents": false
        }
      },
      "dateCreated": "2017-11-03T10:45:23Z"
    }

## Test it with a real service

T.B.D.

## Issues
