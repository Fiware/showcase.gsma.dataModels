# UserContext

This data model describe the Context of a User. No personal data is encoded in
the model. The actual User data are stored in a different end point, as identified
by the `refUser` property.

## Examples of use

```
{
  "id": "UserContext1",
  "type": "UserContext",
  "location": {
    "type": "Point",
    "coordinates": [
      -4.754444444,
      41.640833333
    ]
  },
  "refActivity": "UserActivity1",
  "refDevice": "Device1",
  "refUser": "UserId1"
}
```
