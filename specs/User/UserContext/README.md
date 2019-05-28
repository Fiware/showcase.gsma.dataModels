# UserContext

This data model describe the Context of a User. No personal data is encoded in
the model. The actual User data are stored in a different end point, as
identified by the `refUser` property.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

```json
{
    "id": "UserContext1",
    "type": "UserContext",
    "location": {
        "type": "Point",
        "coordinates": [-4.754444444, 41.640833333]
    },
    "refActivity": "UserActivity1",
    "refUserDevice": "Device1",
    "refUser": "User1"
}
```
