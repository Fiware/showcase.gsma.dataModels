# Air quality threshold

This folder contains a NGSIv2 data set which provides the air quality thresholds in Europe.

Air quality thresholds allow to calculate an air quality index (AQI).

For more information, please check [Air Quality Now](http://www.airqualitynow.eu/about_indices_definition.php#parag1)

## Examples of use

```curl http://130.206.83.68:1026/v2/entities?type=AirQualityThreshold```

```json

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

```