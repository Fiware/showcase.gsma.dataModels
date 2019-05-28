#!/bin/sh

ajv validate --v5 -s $1 -r common-schema.json -r geometry-schema.json -d $2
