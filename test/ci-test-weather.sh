#!/bin/sh

# Tests the Weather datamodels

testWeatherObserved(){
   # 1. check that the JSON Schema is a valid JSON Schema
   result=`ajv compile --v5 -s Weather/WeatherObserved/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json`
   assertEquals "schema Weather/WeatherObserved/schema.json is valid" "${result}"

   # 2. check that the JSON example is valid according to the JSON Schema
   result=`ajv test --v5 -s Weather/WeatherObserved/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json -d Weather/WeatherObserved/example.json --valid`
   assertEquals "Weather/WeatherObserved/example.json passed test" "${result}"
}

testWeatherForecast(){
   result=`ajv compile --v5 -s Weather/WeatherForecast/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json`
   assertEquals "schema Weather/WeatherForecast/schema.json is valid" "${result}"
   result=`ajv test --v5 -s Weather/WeatherForecast/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json -d Weather/WeatherForecast/example.json --valid`
   assertEquals "Weather/WeatherForecast/example.json passed test" "${result}"
}

# load shunit2
. shunit2
