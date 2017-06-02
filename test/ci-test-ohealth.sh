#!/bin/sh

# Test OpenHealthContext models

testClinicalControl(){
   result=`ajv compile --v5 -s OpenHealthContext/ClinicalControl/schema.json -r common-schema.json -r geometry-schema.json -r OpenHealthContext/body-height-1.0.json -r OpenHealthContext/body-weight-1.0.json -r OpenHealthContext/diastolic-blood-pressure-1.0.json -r OpenHealthContext/heart-rate-1.0.json -r OpenHealthContext/length-unit-value-1.0.json -r OpenHealthContext/systolic-blood-pressure-1.0.json -r OpenHealthContext/unit-value-1.x.json -r OpenHealthContext/mass-unit-value-1.x.json -r OpenHealthContext/time-frame-1.x.json -r OpenHealthContext/time-interval-1.x.json -r OpenHealthContext/duration-unit-value-1.x.json -r OpenHealthContext/date-time-1.x.json -r OpenHealthContext/descriptive-statistic-1.x.json -r OpenHealthContext/part-of-day-1.x.json -r OpenHealthContext/temporal-relationship-to-physical-activity-1.x.json`
   assertEquals "schema OpenHealthContext/ClinicalControl/schema.json is valid" "${result}"
   result=`ajv test --v5 -s OpenHealthContext/ClinicalControl/schema.json -r common-schema.json -r geometry-schema.json -r OpenHealthContext/body-height-1.0.json -r OpenHealthContext/body-weight-1.0.json -r OpenHealthContext/diastolic-blood-pressure-1.0.json -r OpenHealthContext/heart-rate-1.0.json -r OpenHealthContext/length-unit-value-1.0.json -r OpenHealthContext/systolic-blood-pressure-1.0.json -r OpenHealthContext/unit-value-1.x.json -r OpenHealthContext/mass-unit-value-1.x.json -r OpenHealthContext/time-frame-1.x.json -r OpenHealthContext/time-interval-1.x.json -r OpenHealthContext/duration-unit-value-1.x.json -r OpenHealthContext/date-time-1.x.json -r OpenHealthContext/descriptive-statistic-1.x.json -r OpenHealthContext/part-of-day-1.x.json -r OpenHealthContext/temporal-relationship-to-physical-activity-1.x.json -d OpenHealthContext/ClinicalControl/example.json --valid`
   assertEquals "OpenHealthContext/ClinicalControl/example.json passed test" "${result}"
}

testPhysicalTest()
{
  result=`ajv compile --v5 -s OpenHealthContext/PhysicalTest/schema.json -r common-schema.json -r geometry-schema.json`
  assertEquals "schema OpenHealthContext/PhysicalTest/schema.json is valid" "${result}"
  result=`ajv test --v5 -s OpenHealthContext/PhysicalTest/schema.json -r common-schema.json -r geometry-schema.json -d OpenHealthContext/PhysicalTest/example.json --valid`
  assertEquals "OpenHealthContext/PhysicalTest/example.json passed test" "${result}"
}

testQuestionnaire()
{
  result=`ajv compile --v5 -s OpenHealthContext/Questionnaire/schema.json -r common-schema.json -r geometry-schema.json`
  assertEquals "schema OpenHealthContext/Questionnaire/schema.json is valid" "${result}"
  result=`ajv test --v5 -s OpenHealthContext/Questionnaire/schema.json -r common-schema.json -r geometry-schema.json -d OpenHealthContext/Questionnaire/example.json --valid`
  assertEquals "OpenHealthContext/Questionnaire/example.json passed test" "${result}"
}

testQuestionnaireQuestion()
{
  result=`ajv compile --v5 -s OpenHealthContext/Questionnaire/Question/schema.json -r common-schema.json -r geometry-schema.json`
  assertEquals "schema OpenHealthContext/Questionnaire/Question/schema.json is valid" "${result}"
  result=`ajv test --v5 -s OpenHealthContext/Questionnaire/Question/schema.json -r common-schema.json -r geometry-schema.json -d OpenHealthContext/Questionnaire/Question/example.json --valid`
  assertEquals "OpenHealthContext/Questionnaire/Question/example.json passed test" "${result}"
}

testQuestionnaireAnswer()
{
  result=`ajv compile --v5 -s OpenHealthContext/Questionnaire/Answer/schema.json -r common-schema.json -r geometry-schema.json`
  assertEquals "schema OpenHealthContext/Questionnaire/Answer/schema.json is valid" "${result}"
  result=`ajv test --v5 -s OpenHealthContext/Questionnaire/Answer/schema.json -r common-schema.json -r geometry-schema.json -d OpenHealthContext/Questionnaire/Answer/example.json --valid`
  assertEquals "OpenHealthContext/Questionnaire/Answer/example.json passed test" "${result}"
}


# load shunit2
. shunit2
