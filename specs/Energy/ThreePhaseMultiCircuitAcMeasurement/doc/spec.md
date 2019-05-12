# Three-phase multi-circuit alternating current measurement

## Description

A ThreePhaseMultiCircuitAcMeasurement entity represents a measurement from
an electrical sub-metering system that monitors three-phase alternating
current across multiple circuits. Each circuit is assigned a voltage phase:
L1, L2 or L3; and has attributes for various electrical measurements such
as `current`, `power`, `energy`, `frequency`, and `harmonics`. There are 
cumulative metering values for each circuit (e.g. net energy) and the start
time for their measurement can be saved to the `dateEnergyMeteringStarted`
attribute. There are also attributes for different power and energy types
(`active`, `reactive` and `apparent`).

For most of the attributes there are various ways they can be actually
measured. For this purpose the `measurementType` metadata attribute can be
used. It can have the following values:

-   instant: The value is from the specific instant of time
-   average: The value is the average of a time period
-   rms: The value is the root mean square of a time period
-   maximum: The value is the maximum of a time period
-   minimum: The value is the minimum of a time period

When using the average, rms, mininum or maximum values another metadata
attribute called `measurementInterval` should be used to give the length of
the measurement period in seconds. Also the `timestamp` metadata attribute
should be the end time of the measurement period.



## Data Model

A JSON Schema corresponding to this data model can be found
[here](../schema.json).

-   `id` : Entity's unique identifier.

-   `type` : It must be equal to `ThreePhaseMultiCircuitAcMeasurement`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `areaServed` : Higher level area to which the measurement target belongs to.
    It can be used to group per responsible, district, neighbourhood, etc.

    -   Normative References:
        [https://schema.org/areaServed](https://schema.org/areaServed)
    -   Optional

-   `refDevice` : Device used to obtain the measurement.

    -   Attribute type: List of Reference to entity(ies) of type
        [Device](../../../Device/Device/doc/spec.md)
    -   Optional

-   `voltagePhase` : Information about three voltage phases: L1,L2,L3

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)

    -   `L1`: Information for phase 1

        -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)

            | Property      | Type   | Required |
            | ------------- | ------ | -------- |
            | `crestFactor` | number | Optional |
            | `fft`         | array  | Optional |
            | `thd`         | number | Optional |
            | `voltage`     | number | Optional |

    -   `L2`: Information for phase 2

        -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)

            | Property      | Type   | Required |
            | ------------- | ------ | -------- |
            | `crestFactor` | number | Optional |
            | `fft`         | array  | Optional |
            | `thd`         | number | Optional |
            | `voltage`     | number | Optional |

    -   `L3`: Information for phase 3

        -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)

            | Property      | Type   | Required |
            | ------------- | ------ | -------- |
            | `crestFactor` | number | Optional |
            | `fft`         | array  | Optional |
            | `thd`         | number | Optional |
            | `voltage`     | number | Optional |

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

-   `currentCircuit` : Information about multiple circuits

    -   Attribute Type: List of items of type [StructuredValue](http://schema.org/StructuredValue)

        | Property                     | Type                                                 | Required |
        |------------------------------|------------------------------------------------------|----------|
        | `circuitLabel`               | string                                               | Optional |
        | `refVoltagePhase`            | string                                               | Optional |
        | `currentSensorConfiguration` | [StructuredValue](http://schema.org/StructuredValue) | Optional |
        | `current`                    | number                                               | Optional |
        | `activePower`                | number                                               | Optional |
        | `reactivePower`              | number                                               | Optional |
        | `apparentPower`              | number                                               | Optional |
        | `powerFactor`                | number                                               | Optional |
        | `activeEnergy`               | number                                               | Optional |
        | `reactiveEnergy`             | number                                               | Optional |
        | `apparentEnergy`             | number                                               | Optional |
        | `fft`                        | array                                                | Optional |
        | `thd`                        | number                                               | Optional |
        | `crestFactor`                | number                                               | Optional |
        | `dateEnergyMeteringStarted`  | [DateTime](https://schema.org/DateTime)              | Optional |
        | `dateCreated`                | [DateTime](https://schema.org/DateTime)              | Optional |
        | `dateModified`               | [DateTime](https://schema.org/DateTime)              | Optional |

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "ThreePhaseAcMultiCircuitMeasurement:LV3_Ventilation",
    "type": "ThreePhaseAcMultiCircuitMeasurement",
    "currentCircuit": {
        "value": [
            {
                "activePower": 0, 
                "apparentPower": 0, 
                "powerFactor": 0, 
                "activeEnergy": 0, 
                "fft": [], 
                "refVoltagePhase": "L1", 
                "current": 0, 
                "dateEnergyMeteringStarted": "2018-07-07T15:05:59.408Z", 
                "reactiveEnergy": 0, 
                "circuitLabel": "ABC 1", 
                "crestFactor": 0, 
                "reactivePower": 0, 
                "currentSensorConfiguration": {}, 
                "apparentEnergy": 0, 
                "thd": 0
            }, 
            {
                "activePower": 0, 
                "apparentPower": 0, 
                "powerFactor": 0, 
                "activeEnergy": 0, 
                "fft": [], 
                "refVoltagePhase": "L1", 
                "current": 0, 
                "dateEnergyMeteringStarted": "2018-07-07T15:05:59.408Z", 
                "reactiveEnergy": 0, 
                "circuitLabel": "ABC 2", 
                "crestFactor": 0, 
                "reactivePower": 0, 
                "currentSensorConfiguration": {}, 
                "apparentEnergy": 0, 
                "thd": 0
            }
        ]
    }, 
    "name": {
        "value": "HKAPK0200"
    }, 
    "refDevice": {
        "type": "Relationship", 
        "value": "Device:eQL-EDF3GL-2006201705"
    }, 
    "voltagePhase": {
        "value": {
            "frequency": 50, 
            "L2": {
                "voltage": 230.312
            }, 
            "L3": {
                "voltage": 230.312
            }, 
            "L1": {
                "voltage": 230.312
            }
        }
    }, 
    "description": {
        "value": "measurement corresponding to the ventilation machine rooms"
    }
}

```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "ThreePhaseAcMultiCircuitMeasurement:LV3_Ventilation",
    "type": "ThreePhaseAcMultiCircuitMeasurement",
    "description": "measurement corresponding to the ventilation machine rooms",
    "refDevice": "Device:eQL-EDF3GL-2006201705",
    "name": "HKAPK0200",
    "voltagePhase": {
        "L1": {
            "voltage": 230.312
        },
        "L2": {
            "voltage": 230.312
        },
        "L3": {
            "voltage": 230.312
        },
        "frequency": 50
    },
    "currentCircuit": [
        {
            "circuitLabel": "ABC 1",
            "refVoltagePhase": "L1",
            "current": 0,
            "activePower": 0,
            "reactivePower": 0,
            "apparentPower": 0,
            "powerFactor": 0,
            "activeEnergy": 0,
            "reactiveEnergy": 0,
            "apparentEnergy": 0,
            "fft": [],
            "thd": 0,
            "crestFactor": 0,
            "currentSensorConfiguration": {},
            "dateEnergyMeteringStarted": "2018-07-07T15:05:59.408Z"
        },
        {
            "circuitLabel": "ABC 2",
            "refVoltagePhase": "L1",
            "current": 0,
            "activePower": 0,
            "reactivePower": 0,
            "apparentPower": 0,
            "powerFactor": 0,
            "activeEnergy": 0,
            "reactiveEnergy": 0,
            "apparentEnergy": 0,
            "fft": [],
            "thd": 0,
            "crestFactor": 0,
            "currentSensorConfiguration": {},
            "dateEnergyMeteringStarted": "2018-07-07T15:05:59.408Z"
        }
    ]
}

```

## Test it with a real service

## Open Issues
