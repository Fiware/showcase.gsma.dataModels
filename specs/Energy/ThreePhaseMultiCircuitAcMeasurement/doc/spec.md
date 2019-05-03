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

-   `fftVoltage` : Voltage values at N multiples of the fundamental frequency. Where N=1
    is the measured fundamental `frequency` (e.g. 50Hz), N=2 is 100Hz, etc..

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

-   `crestFactorVoltage` : Ratio of voltage waveform peaks to RMS value. Expressed
    as a number (eg: for a pure sine wave, crestFactorVoltage = 1.414) 

    -   Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
    -   Allowed values: A number between 0 and 10.
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

-   `circuitLabel` : Descriptive text (eg: basement AC, kitchen lights, oven…) 

    -   Attribute Type: List of items of type [Text](https://schema.org/Text)
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

-   `refVoltagePhase` : Phase on which a circuit is connected to.

    -   Attribute Type: List of items of type [Text](http://schema.org/Text)
    -   Allowed values, one of the following : "L1","L2","L3"
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

-   `currentSensorConfiguration` : Configuration for the current sensor.

    -   Attribute Type: List of items of type Object
    -   Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `current` : Electrical current.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
    -   Default unit: Amperes (A)
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

-   `activePower` : Active power consumed per circuit.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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

-   `reactivePower` : Fundamental frequency reactive power.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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

-   `apparentPower` : Apparent power consumed per circuit.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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

-   `powerFactor` : Power factor for each circuit.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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
    -   Optional

-   `dateEnergyMeteringStarted` : The starting date for metering energy.

    -   Attribute Type: [DateTime](http://schema.org/DateTime)
    -   Optional

-   `activeEnergy` : Active energy metered in circuit since the metering start date.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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

-   `reactiveEnergy` : Reactive energy metered in circuit since the metering start date.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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

-   `apparentEnergy` : Apparent energy metered in circuit since the metering start date.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
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

-   `fftCurrent` : Current readings at N multiples of the fundamental frequency. Where
    N=1 is the measured fundamental `frequency` (e.g. 50Hz), then N=2 is 100Hz, etc.

    -   Attribute Type: List of Lists of items of type [Number](http://schema.org/Number)
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

-   `thdCurrent` : Total harmonic distortion of electrical current.

    -   Attribute Type: List of Lists of items of type [Number](http://schema.org/Number)
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

-   `crestFactorCurrent` : Apparent energy metered in circuit since the metering start date.

    -   Attribute Type: List of items of type [Number](http://schema.org/Number)
    -   Allowed values: A number between 0 and 10.
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
    "current": {
        "value": [
            33.55, 
            34.77, 
            31.32, 
            32.4, 
            34.08, 
            13.33, 
            10.86, 
            11.11, 
            23.31, 
            11.31, 
            14.16, 
            40.19, 
            29.6, 
            13.36, 
            33.99, 
            24.28
        ]
    }, 
    "description": {
        "value": "measurement corresponding to the ventilation machine rooms"
    }, 
    "refVoltagePhase": {
        "type": "Relationship", 
        "value": [
            "L1", 
            "L2", 
            "L3", 
            "L1", 
            "L2", 
            "L3", 
            "L1", 
            "L2", 
            "L3", 
            "L1", 
            "L2", 
            "L3", 
            "L1", 
            "L2", 
            "L3", 
            "L1"
        ]
    }, 
    "refDevice": {
        "type": "Relationship", 
        "value": [
            "Device:eQL-EDF3GL-2006201705"
        ]
    }, 
    "phaseVoltage": {
        "value": {
            "L2": 234.563477, 
            "L3": 235.354034, 
            "L1": 234.961304
        }
    }, 
    "dateEnergyMeteringStarted": {
        "type": "DateTime", 
        "value": "2018-07-07T15:05:59.408Z"
    }, 
    "frequency": {
        "value": 50.020672
    }, 
    "circuitLabel": {
        "value": [
            "Circuit 1", 
            "Circuit 2", 
            "Circuit 3", 
            "Circuit 4", 
            "Circuit 5", 
            "Circuit 6", 
            "Circuit 7", 
            "Circuit 8", 
            "Circuit 9", 
            "Circuit 10", 
            "Circuit 11", 
            "Circuit 12", 
            "Circuit 13", 
            "Circuit 14", 
            "Circuit 15", 
            "Circuit 16"
        ]
    }, 
    "phaseToPhaseVoltage": {
        "value": {
            "L23": 407.081238, 
            "L12": 406.769196, 
            "L31": 407.734558
        }
    }, 
    "name": {
        "value": "HKAPK0200"
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "ThreePhaseAcMultiCircuitMeasurement:LV3_Ventilation",
    "type": "ThreePhaseAcMultiCircuitMeasurement",
    "dateEnergyMeteringStarted": "2018-07-07T15:05:59.408Z",
    "refDevice": [
        "Device:eQL-EDF3GL-2006201705"
    ],
    "name": "HKAPK0200",
    "description": "measurement corresponding to the ventilation machine rooms",
    "frequency": 50.020672,
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
    "circuitLabel": [
        "Circuit 1",
        "Circuit 2",
        "Circuit 3",
        "Circuit 4",
        "Circuit 5",
        "Circuit 6",
        "Circuit 7",
        "Circuit 8",
        "Circuit 9",
        "Circuit 10",
        "Circuit 11",
        "Circuit 12",
        "Circuit 13",
        "Circuit 14",
        "Circuit 15",
        "Circuit 16"
    ],
    "refVoltagePhase": [
        "L1",
        "L2",
        "L3",
        "L1",
        "L2",
        "L3",
        "L1",
        "L2",
        "L3",
        "L1",
        "L2",
        "L3",
        "L1",
        "L2",
        "L3",
        "L1"
    ],
    "current": [
        33.55,
        34.77,
        31.32,
        32.40,
        34.08,
        13.33,
        10.86,
        11.11,
        23.31,
        11.31,
        14.16,
        40.19,
        29.60,
        13.36,
        33.99,
        24.28
    ]
}
```

## Test it with a real service

## Open Issues
