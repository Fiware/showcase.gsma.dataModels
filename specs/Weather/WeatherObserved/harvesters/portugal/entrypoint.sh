#!/bin/sh

ORION_DEFAULT=http://orion:1026
PARAMS=$@
HARVESTER=portugal_weather_observed.py

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --orion)
            ORION="$2"
            shift
        ;;
    esac
    shift
done

if [[ -z ${ORION} ]]; then ORION=${ORION_DEFAULT}; fi

echo "Trying ${ORION}/version .."

while [[ ! "$(curl -s ${ORION}/version)" ]]; do
   echo "sleeping .."
   sleep 5
done

exec /usr/bin/env python3 -u /opt/${HARVESTER} ${PARAMS}
