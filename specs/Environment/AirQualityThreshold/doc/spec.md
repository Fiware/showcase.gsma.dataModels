# Air quality threshold

The formal documentation of this model is currently under development. In the
meantime please check the examples of use

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

    {
      "id": "EU-AirQualityThreshold-O3-Background-VeryLow",
      "type": "AirQualityThreshold",
      "category": [ "Background" ],
      "frequency": "Hourly",
      "indexClass": "VeryLow",
      "maxConcentration": 60,
      "minConcentration": "0",
      "pollutant": "O3",
      "source": "http://www.airqualitynow.eu/"
    }
