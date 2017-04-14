#!/bin/sh

# Tests the User datamodels

testUserContext()
{
  # Check that running with a short help flag results in a non-error exit code
  ../validate.sh ../User/UserContext/schema.json ../User/UserContext/example.json
  result=$?
  assertEquals "xeno daemon with -h should exit with code 0" 0 ${result}

}
