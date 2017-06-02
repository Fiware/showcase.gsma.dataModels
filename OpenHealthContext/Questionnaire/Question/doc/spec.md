# Question

## Data Model

A JSON Schema corresponding to this data model can be found [here](../schema.json).

+ `id` : Unique identifier.
    + Mandatory.

+ `type` : Entity type. It must be equal to `Question`.
    + Mandatory.

+ `refQuestionnaire` : Reference to a questionnaire.
    + Attribute type: `string`.
    + Mandatory.

+ `language` : Language in which the questions is written.
    + Attribute type: `string`.
    + Allowed values: (`eng`, `es`, and those included into the ISO: 639-4:2010).
    + Mandatory.

+ `dateModified` : Last entity's update timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime).
    + Mandatory.

## Examples of use

```
{
  "id": "ffffffffff9cbbf4465f0ef30033c587-question-7118",
  "type": "Question",
  "refQuestionnaire": "ffffffffff9cbbf4465f0ef30033c587-questionnaire-7118",
  "language": "en",
  "dateModified": "2017-01-18T20:45:42.697Z"
}
```

## Use it with a real service

T.B.D.

## Open Issues

T.B.A.
