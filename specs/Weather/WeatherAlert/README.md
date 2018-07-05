# Weather Alert

This folder contains all the software artefacts to offer weather alert data in NGSIv2.
The source of this data is the global [European Weather Alarm Service](http://meteoalarm.eu).

* `meteoalarm_harvest.py`. A harvester for weather alarms throughout Europe.

Before using this data please check license at the original data source. 

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## Examples of use

```
curl http://<orion_host:port>/v2/entities?type=Alert&q=category==weather&address.addressCountry==ES
```

```json
{
    "severity": "medium",
    "subCategory": "snow/ice",
    "alertSource": "http://www.meteoalarm.eu",
    "address": {
      "addressCountry": "ES",
      "addressRegion": "Huesca"
    },
    "dateIssued": "2016-03-14T13:54:01",
    "type": "Alert",
    "id": "WeatherAlert-83b872975414bfca10832e564a1bb416-7",
    "validTo": "2016-03-14T23:59:00",
    "validFrom": "2016-03-14T13:00:00"
}
```
