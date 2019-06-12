# Weather Alert

This folder contains all the software artefacts to offer weather alert data in
NGSI v2. The source of this data is the global
[European Weather Alarm Service](http://meteoalarm.eu).

-   `meteoalarm_harvest.py`. A harvester for weather alarms throughout Europe.

Before using this data please check license at the original data source.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

```bash
curl -X GET \
  'https://streams.lab.fiware.org/v2/entities?type=Alert&orderBy=validTo&options=keyValues&limit=1' \
  -H 'fiware-service: weather' | python -m json.tool
```

```json
[
    {
        "address": {
            "addressCountry": "ES",
            "addressRegion": "Costa  Litoral sur de Alicante",
            "type": "PostalAddress"
        },
        "alertSource": "http://www.meteoalarm.eu",
        "category": "weather",
        "dateIssued": "2019-06-13T01:00:00.00Z",
        "id": "WeatherAlert-ac175375a4d9a868d83ddc53e645a27d-3",
        "severity": "medium",
        "subCategory": "coastalEvent",
        "type": "Alert",
        "validFrom": "2019-06-13T11:00:00.00Z",
        "validTo": "2019-06-13T20:59:00.00Z"
    }
]
```
