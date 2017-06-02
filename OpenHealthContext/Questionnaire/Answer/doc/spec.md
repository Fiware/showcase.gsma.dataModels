# Answer

## Data Model

A JSON Schema corresponding to this data model can be found [here](../schema.json).

+ `id` : Unique identifier.
    + Mandatory.

+ `type` : Entity type. It must be equal to `Answer`.
    + Mandatory.

+ `refQuestion` : Reference to a Question.
    + Attribute type: `string`.
    + Mandatory.

+ `refUser` : Reference to the actual User sheltered by an independent service.
    + Attribute type: `string`.
    + Mandatory.

+ `answer` : Information given to answer respective question.
    + Attribute type: `string`.
    + Mandatory.

+ `dateModified` : Last entity's update timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime).
    + Mandatory.

## Examples of use

```
{
  "id": "ffffffffff9cbbf4465f0ef30033c587-question-7118",
  "type": "Answer",
  "refQuestion": "ffffffffff9cbbf4465f0ef30033c587-question-7118",
  "refUser": "http://207.249.127.162:1234/users/1",
  "answer": "true",
  "dateModified": "2017-01-18T20:45:42.697Z"
}
```

## Use it with a real service

T.B.D.

## Open Issues

T.B.A.
