#!/bin/sh

# Tests the Weather datamodels

testWeatherObserved(){
   result=`ajv compile --v5 -s Weather/WeatherObserved/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json`
   assertEquals "schema Weather/WeatherObserved/schema.json is valid" "${result}"
   result=`ajv test --v5 -s Weather/WeatherObserved/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json -d Weather/WeatherObserved/example.json --valid`
   assertEquals "Weather/WeatherObserved/example.json passed test" "${result}"
}

# load shunit2
. shunit2
