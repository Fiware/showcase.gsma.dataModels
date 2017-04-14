# Notification

This data model presents user generated notifications. This model can be used
in different scenarios. For example in Smart Mobility scenarios to provide a Traffic Alert,
or in Smart Security scenarios to report suspicious activities.

## Examples of use

```
{
  "id": "Notification:1",
  "type": "Notification",
  "eventType": "TrafficJam",
  "location": {
    "type": "Point",
    "coordinates": [-3.712247222222222, 40.423852777777775]
  },
  "eventObserved": "2017-01-02T09:25:55.00Z",
  "severity": 3,
  "description": "Traffic Jam in Malibu street",
  "refUser": "https://account.lab.fiware.org/users/1"
}  
```
