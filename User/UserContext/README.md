# UserContext

This data model describe the Context of a User. No personal data is encoded in
the model. The actual User data are stored in a different end point, as identified
by the `refUser` property. Within FIWARE, this reference could point to the end of
the FIWARE Identity Manager, where FIWARE user profiles are stored.

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
  "refActivity": "http://contextbroker:1026/v2/entities/UserActivity1",
  "refDevice": "http://contextbroker:1026/v2/entities/Device1",
  "refUser": "https://account.lab.fiware.org/users/1"
}
```
