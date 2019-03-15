# Three-phase alternating current measurement

## Description

A ThreePhaseAcMeasurement entity represents a measurement from an electrical system
that uses three-phase alternating current. It has attributes for various
electrical measurements such as power, frequency, current and voltage. For some
attributes such as current and voltage the value is a structured value with
properties for the three different phases: L1, L2 and L3. For some measurements
such as the different power types (active, reactive and apparent power) there is
an attribute for the total from all phases e.g. `totalActivePower` and an
attribute for values from each phase as a structured value e.g. `activePower`.
There are also attributes for different energy types: active (delivered net
energy), reactive and apparent. They are cumulative values and the start time
for their measurement can be saved to the `dateEnergyMeteringStarted` attribute.

For most of the attributes there are various ways they can be actually measured.
For this purpose the `measurementType` metadata attribute can be used. It can
have the following values:

-   instant: The value is from the specific instant of time
-   average: The value is the average of a time period
-   rms: The value is the root mean square of a time period
-   maximum: The value is the maximum of a time period
-   minimum: The value is the minimum of a time period

When using the average, rms, mininum or maximum values another metadata
attribute called `measurementInterval` should be used to give the length of the
measurement period in seconds. Also the `timestamp` metadata attribute should be
the end time of the measurement period.

## Data Model

A JSON Schema corresponding to this data model can be found
[here](../schema.json).

-   `id` : Entity's unique identifier.

-   `type` : It must be equal to `ThreePhaseAcMeasurement`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `name` : Name given to the measurement location or target.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Optional

-   `description` : A longer description of the measurement.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `location` : location of the measurement target represented by a GeoJSON
    point.

    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
    -   Optional

-   `address` : Civic address where the measurement target is located.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Optional

-   `areaServed` : Higher level area to which the measurement target belongs to. It can
    be used to group per responsible, district, neighbourhood, etc.

    -   Normative References:
        [https://schema.org/areaServed](https://schema.org/areaServed)
    -   Optional

-   `refDevice` : Device(s) used to obtain the measurement.

    -   Attribute type: List of Reference to entity(ies) of type
        [Device](../../Device/Device/doc/spec.md)
    -   Optional

-   `refTargetDevice` : Device(s) for which the measurement was taken.

    -   Attribute type: List of Reference to entity(ies) of type
        [Device](../../Device/Device/doc/spec.md)
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `totalActiveEnergyImport` : Total energy imported i.e. consumed since
    metering started (since `dateEnergyMeteringStarted`).

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: kilowatt hour (kWh).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `totalReactiveEnergyImport` : Total energy imported i.e. consumed (with
    regards to fundamental frequency reactive power) since the metering start
    date (`dateEnergyMeteringStarted`).

    -   Attribute type: [Number](https://schema.org/Number)
        -   Default unit: kilovolt-ampere-reactive-hour (kVArh).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `totalApparentEnergyImport` : Total energy imported i.e. consumed (with
    regards to apparent power) since the metering start date
    (`dateEnergyMeteringStarted`).

    -   Attribute type: [Number](https://schema.org/Number)
        -   Default unit: kilovolt-ampere-hour (kVAh).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime
    -   Optional

-   `totalActiveEnergyExport` : Total energy exported since metering started
    (since `dateEnergyMeteringStarted`).

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: kilowatt hour (kWh).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `totalReactiveEnergyExport` : Total fundamental frequency reactive energy
    exported since metering started (since `dateEnergyMeteringStarted`).

    -   Attribute type: [Number](https://schema.org/Number)
    -   Default unit: kilovolt-ampere-reactive-hour (kVArh).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `totalApparentEnergyExport` : Total energy exported (with regards to
    apparent power) since the metering start date (`dateEnergyMeteringStarted`).

    -   Attribute type: [Number](https://schema.org/Number)
        -   Default unit: kilovolt-ampere-hour (kVAh).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `activeEnergyImport` : Active energy imported i.e. consumed per phase since
    the metering start date. The actual values will be conveyed by subproperties
    which names will be equal to the name of each of the alternating current
    phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: kilowatt hour (kWh)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `reactiveEnergyImport` : Fundamental frequency reactive energy imported i.e.
    consumed per phase since the metering start date. The actual values will be
    conveyed by subproperties which names will be equal to the name of each of
    the alternating current phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: kilovolt-ampere-reactive-hour (kVArh)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `apparentEnergyImport` : Apparent energy imported i.e. consumed per phase
    since the metering start date. The actual values will be conveyed by
    subproperties which names will be equal to the name of each of the
    alternating current phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: kilovolt-ampere-hour (kVAh)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `activeEnergyExport` : Active energy exported per phase since the metering
    start date. The actual values will be conveyed by subproperties which names
    will be equal to the name of each of the alternating current phases: L1, L2,
    L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: kilowatt hour (kWh)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `reactiveEnergyExport` : Fundamental frequency reactive energy exported per
    phase since the metering start date. The actual values will be conveyed by
    subproperties which names will be equal to the name of each of the
    alternating current phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: kilovolt-ampere-reactive-hour (kVArh)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `apparentEnergyExport` : Apparent energy exported per phase since the
    metering start date. The actual values will be conveyed by subproperties
    which names will be equal to the name of each of the alternating current
    phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: kilovolt-ampere-hour (kVAh)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `dateEnergyMeteringStarted` : The starting date for metering energy.

    -   Attribute Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `frequency` : The frequency of the circuit.

    -   Attribute type: [Number](http://schema.org/Number)
    -   Default unit: Hertz (Hz)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `totalActivePower` : Active power consumed (counting all phases)

    -   Attribute Type: [Number](http://schema.org/Number)
    -   Default unit: watt (W).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `totalReactivePower` : Reactive power consumed (counting all phases).

    -   Attribute Type: [Number](http://schema.org/Number)
    -   Default unit: volt-ampere-reactive (VAr).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `totalApparentPower` : Apparent power consumed (counting all phases).

    -   Attribute Type: [Number](http://schema.org/Number)
    -   Default unit: volt-ampere (VA).
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `activePower` : Active power consumed per phase. The actual values will be
    conveyed by subproperties which names will be equal to the name of each of
    the alternating current phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: watt (W)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `apparentPower` : Apparent power consumed per phase. The actual values will
    be conveyed by subproperties which names will be equal to the name of each
    of the alternating current phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: volt-ampere (VA)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `reactivePower` : Fundamental frequency reactive power. The actual values
    will be conveyed by subproperties whose names will be equal to the name of
    each of the alternating current phases: L1, L2, L3.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: volts-ampere-reactive (VAr)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `totalPowerFactor` : Power factor including all phases.

    -   Attribute Type: [Number](http://schema.org/Number)
    -   Allowed values: A number between -1 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
        -   `onlyPositive`: Is the value always greater than zero or can it also
            be negative. If not present this is assumed to be false.
            -   Type: [Boolean](https://schema.org/Boolean)
    -   Optional

-   `powerFactor` : Power factor for each phase. The actual values will be
    conveyed by one subproperty per alternating current phase: L1, L2 and L3

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Allowed values: A number between -1 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
        -   `onlyPositive`: Is the value always greater than zero or can it also
            be negative. If not present this is assumed to be false.
            -   Type: [Boolean](https://schema.org/Boolean)
    -   Optional

-   `totalDisplacementPowerFactor` : Displacement power factor including all
    phases. The quantity is based on the fundamental frequency of the system

    -   Attribute Type: [Number](http://schema.org/Number)
    -   Allowed values: A number between -1 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
        -   `onlyPositive`: Is the value always greater than zero or can it also
            be negative. If not present this is assumed to be false.
            -   Type: [Boolean](https://schema.org/Boolean)
    -   Optional

-   `displacementPowerFactor` : Displacement power factor for each phase. The
    quantity is based on the fundamental frequency of the system. The actual
    values will be conveyed by one subproperty per alternating current phase:
    L1, L2 and L3

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Allowed values: A number between -1 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
        -   `onlyPositive`: Is the value always greater than zero or can it also
            be negative. If not present this is assumed to be false.
            -   Type: [Boolean](https://schema.org/Boolean)
    -   Optional

-   `current` : Electrical current. The actual values will be conveyed by one
    subproperty per alternating current phase and the neutral wire: L1, L2, L3
    and N.

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: Ampers (A)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `phaseVoltage` : The voltage between each phase and neutral conductor. The
    actual values will be conveyed by one subproperty per alternating current
    phase: L1, L2 and L3

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: Volts (V)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `phaseToPhaseVoltage` : Voltage between phases. A value for each phase pair:
    phases 1 and 2 (L12), phases 2 and 3 (L32), phases 3 and 1 (L31).

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Default unit: Volts (V)
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `thdVoltage` : Total harmonic distortion of voltage for each phase. The
    actual values will be conveyed by one subproperty per alternating current
    phase: L1, L2 and L3

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Allowed values: A number between 0 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

-   `thdCurrent` : Total harmonic distortion of electrical current. The actual
    values will be conveyed by one subproperty per alternating current phase:
    L1, L2 and L3

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Allowed values: A number between 0 and 1.
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
        -   `measurementType`: How the measurement was made. (see beginning of
            document for details)
            -   type: Text
        -   `measurementInterval`: For certain measurement types the measurement
            period. (See beginning of document for details)
            -   type: [Number](http://schema.org/Number)
    -   Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "ThreePhaseAcMeasurement:LV3_Ventilation",
    "type": "ThreePhaseAcMeasurement",
    "dateEnergyMeteringStarted": {
        "type": "DateTime",
        "value": "2018-07-07T15:05:59.408Z"
    },
    "refDevice": {
        "type": "Relationship",
        "value": ["Device:eQL-EDF3GL-2006201705"]
    },
    "name": {
        "value": "HKAPK0200"
    },
    "description": {
        "value": "measurement corresponding to the ventilation machine rooms"
    },
    "totalActiveEnergyImport": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            }
        },
        "value": 150781.96448
    },
    "totalReactiveEnergyImport": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            }
        },
        "value": 20490.3392
    },
    "totalActiveEnergyExport": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            }
        },
        "value": 1059.80176
    },
    "totalReactiveEnergyExport": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            }
        },
        "value": 93275.02176
    },
    "totalActivePower": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "value": 31700.269531
    },
    "activePower": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 11996.416016,
            "L2": 9461.501953,
            "L3": 10242.351562
        }
    },
    "totalReactivePower": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "value": -7830.332031
    },
    "reactivePower": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": -2612.606934,
            "L2": -2209.906006,
            "L3": -3007.81958
        }
    },
    "totalApparentPower": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "value": 36019.089844
    },
    "apparentPower": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 13201.412109,
            "L2": 10755.304688,
            "L3": 11941.094727
        }
    },
    "powerFactor": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            },
            "onlyPositive": {
                "value": true
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 0.908817,
            "L2": 0.879906,
            "L3": 0.859293
        }
    },
    "displacementPowerFactor": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            },
            "onlyPositive": {
                "value": true
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 0.978013,
            "L2": 0.973317,
            "L3": 0.960382
        }
    },
    "frequency": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "value": 50.020672
    },
    "current": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "rms"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 56.126038,
            "L2": 45.894356,
            "L3": 50.872452,
            "N": 0.0
        }
    },
    "phaseVoltage": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "rms"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 234.961304,
            "L2": 234.563477,
            "L3": 235.354034
        }
    },
    "phaseToPhaseVoltage": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "rms"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L12": 406.769196,
            "L23": 407.081238,
            "L31": 407.734558
        }
    },
    "thdVoltage": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 0.01471114,
            "L2": 0.01600046,
            "L3": 0.01541459
        }
    },
    "thdCurrent": {
        "metadata": {
            "timestamp": {
                "type": "DateTime",
                "value": "2019-01-24T22:00:00.173Z"
            },
            "measurementType": {
                "value": "average"
            },
            "measurementInterval": {
                "value": 1
            }
        },
        "type": "StructuredValue",
        "value": {
            "L1": 0.38497337,
            "L2": 0.45807529,
            "L3": 0.4938652
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "ThreePhaseAcMeasurement:LV3_Ventilation",
    "type": "ThreePhaseAcMeasurement",
    "dateEnergyMeteringStarted": "2018-07-07T15:05:59.408Z",
    "refDevice": ["Device:eQL-EDF3GL-2006201705"],
    "name": "HKAPK0200",
    "description": "measurement corresponding to the ventilation machine rooms",
    "totalActiveEnergyImport": 150781.96448,
    "totalReactiveEnergyImport": 20490.3392,
    "totalActiveEnergyExport": 1059.80176,
    "totalReactiveEnergyExport": 93275.02176,
    "totalActivePower": 31700.269531,
    "activePower": {
        "L1": 11996.416016,
        "L2": 9461.501953,
        "L3": 10242.351562
    },
    "totalReactivePower": -7830.332031,
    "reactivePower": {
        "L1": -2612.606934,
        "L2": -2209.906006,
        "L3": -3007.81958
    },
    "totalApparentPower": 36019.089844,
    "apparentPower": {
        "L1": 13201.412109,
        "L2": 10755.304688,
        "L3": 11941.094727
    },
    "powerFactor": {
        "L1": 0.908817,
        "L2": 0.879906,
        "L3": 0.859293
    },
    "displacementPowerFactor": {
        "L1": 0.978013,
        "L2": 0.973317,
        "L3": 0.960382
    },
    "frequency": 50.020672,
    "current": {
        "L1": 56.126038,
        "L2": 45.894356,
        "L3": 50.872452,
        "N": 0.0
    },
    "phaseVoltage": {
        "L1": 234.961304,
        "L2": 234.563477,
        "L3": 235.354034
    },
    "phaseToPhaseVoltage": {
        "L12": 406.769196,
        "L23": 407.081238,
        "L31": 407.734558
    },
    "thdVoltage": {
        "L1": 0.01471114,
        "L2": 0.01600046,
        "L3": 0.01541459
    },
    "thdCurrent": {
        "L1": 0.38497337,
        "L2": 0.45807529,
        "L3": 0.4938652
    }
}
```

## Test it with a real service

## Open Issues
