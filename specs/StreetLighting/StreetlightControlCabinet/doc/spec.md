# Streetlight control cabinet

It represents equipment, usually on street, used to the automated control of a
group(s) of streetlights, i.e. one or more circuits.

## Data Model

The data model is defined as shown below:

- `id` : Entity's unique identifier.

- `type` : It must be equal to `StreetlightControlCabinet`.

- `source` : A sequence of characters giving the source of the entity data.
  - Attribute type: Text or URL
  - Optional

- `dataProvider` : Specifies the URL to information about the provider of this information
  - Attribute type: URL
  - Optional

- `location` : Control cabinet's location represented by a GeoJSON point.

  - Attribute type: `geo:json`.
  - Normative References:
        [https://tools.ietf.org/html/draft-ietf-geojson-03](https://tools.ietf.org/html/draft-ietf-geojson-03)
  - Mandatory

- `address` : Civic address where the control cabinet is located.

  - Normative References:
        [https://schema.org/address](https://schema.org/address)
  - Mandatory if `location` is not present.

- `areaServed` : Higher level area to which the cabinet belongs to. It can be
    used to group per responsible, district, neighbourhood, etc.

  - Normative References:
        [https://schema.org/areaServed](https://schema.org/areaServed)
  - Optional

- `serialNumber` : Serial number of the control cabinet.

  - Normative References:
        [https://schema.org/serialNumber](https://schema.org/serialNumber)
  - Optional

- `refStreetlightGroup` : Streetlight group(s) controlled.

  - Attribute type: List of references to entities of type
        [StreetlightGroup](../../StreetlightGroup/doc/spec.md).
  - Mandatory

- `brandName` : Name of the cabinet's brand.

  - Attribute type: [Text](https://schema.org/Text)
  - See also: [https://schema.org/brand](https://schema.org/brand)
  - Optional

- `modelName` : Name of the cabinet's model.

  - Attribute type: [Text](https://schema.org/Text)
  - See also: [https://schema.org/model](https://schema.org/model)
  - Optional

- `manufacturerName` : Name of the cabinet's manufacturer.

  - Attribute type: [Text](https://schema.org/Text)
  - See also: [https://schema.org/model](https://schema.org/manufacturer)
  - Optional

- `cupboardMadeOf` : Material the cabinet's cupboard is made of.

  - Attribute type: [Text](https://schema.org/Text)
  - Allowed values: one Of (`plastic`, `metal`, `concrete`, `other`)
  - Optional

- `features` : A list of cabinet controller features.

  - Attribute type: List of [Text](https://schema.org/Text)
  - Allowed Values: Those technical values considered meaningful by
        applications.
        -   `astronomicalClock` .- The control cabinet includes an astronomical
            clock to deal with switching hours.
        -   `individualControl` .- The control cabinet allows to control street
            lights individually.

- `compliantWith`. A list of standards to which the cabinet controller is
    compliant with (ex. `IP54`)

  - AttributeType: List of [Text](https://schema.org/Text).
  - Optional

- `annotations` : A field reserved for annotations (incidences, remarks,
    etc.).

  - Attribute type: List of [Text](https://schema.org/Text)
  - Optional

- `refDevice` : Reference to the device(s) used to monitor this control cabinet.

  - Attribute type: List of Reference to entity(ies) of type [Device](../../../Device/Device/doc/spec.md)
  - Optional

- `dateModified` : Last update timestamp of this entity.

  - Attribute type: [DateTime](https://schema.org/DateTime)
  - Read-Only. Automatically generated.

- `dateServiceStarted` : Date at which the cabinet controller started giving
    service.

  - Attribute Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `dateLastProgramming` : Date at which there was a programming operation over
    the cabinet.

  - Attribute Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `nextActuationDeadline` : Deadline for next actuation to be performed
    (programming, testing, etc.).

  - Attribute Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `responsible` : Responsible for the cabinet controller, i.e. entity in
    charge of actuating (programming, etc.).

  - Attribute type: [Text](http://schema.org/Text)
  - Optional

- `workingMode` : Working mode for this cabinet controller.

  - Attribute type: [Text](http://schema.org/Text)
  - Allowed values:
        -   `automatic` : The cabinet controller decides automatically when
            light groups are switched on and off. Manual operation is not
            allowed.
        -   `manual` : Human intervention is required for switching on and off.
        -   `semiautomatic` : The same as `automatic` but in this case manual
            intervention is allowed.
  - Mandatory

- `maximumPowerAvailable` : The maximum power available (by contract) for the
    circuits controlled by this cabinet.

  - Attribute type: [Number](http://schema.org/Number)
  - Default unit: Kilowatts (kW)
  - Optional

- `energyConsumed` : Energy consumed by the circuits controlled since metering
    started (since `dateMeteringStarted`).

  - Attribute type: [Number](https://schema.org/Number)
  - Default unit: Kilowatts per hour (kWh).
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `energyCost` : Cost of the energy consumed by the circuits controlled since
    the metering start date (`dateMeteringStarted`).

  - Attribute type: [Number](https://schema.org/Number)
  - Default currency: Euros. (Other currencies might be expressed using a
        metadata attribute)
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `reactiveEnergyConsumed` : Energy consumed (with regards to reactive power)
    by circuits since the metering start date (`dateMeteringStarted`). +
    Attribute type: [Number](https://schema.org/Number) + Default unit:
    KiloVolts-Ampere-Reactive per hour (kVArh). + Attribute metadata: +
    `timestamp`: Timestamp when the last update of the attribute happened. +
    Type: [DateTime](http://schema.org/DateTime) + Optional

- `dateMeteringStarted` : The starting date for metering energy consumed.

  - Attribute Type: [DateTime](http://schema.org/DateTime)
  - Mandatory if `energyConsumed` is present.

- `lastMeterReading` : Value of the last reading obtained from the energy
    consumed metering system.

  - Attribute type: [Number](https://schema.org/Number)
  - Default unit: Kilowatts per hour (kWh).
  - Attribute metadata:
        -   `timestamp`: Timestamp which reflects the date and time at which the
            referred reading was obtained.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `meterReadingPeriod` : The periodicity of energy consumed meter readings in
    days.

  - Attribute Type: [Number](http://schema.org/Number)
  - Optional

- `frequency` : The working frequency of the circuit.

  - Attribute type: [Number](http://schema.org/Number)
  - Default unit: Hertz (Hz)
  - Optional

- `totalActivePower` : Active power currently consumed (counting all phases).

  - Attribute Type: [Number](http://schema.org/Number)
  - Default unit: KiloWatts (kW).
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `totalReactivePower` : Reactive power currently consumed (counting all
    phases).

  - Attribute Type: [Number](http://schema.org/Number)
  - Default unit: KiloVolts-Ampere-Reactive (kVArh).
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `activePower` : Active power consumed per phase. The actual values will be
    conveyed by subproperties which name will be equal to the name of each of
    the alternating current phases, typically R, S, T.

  - Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
  - Default unit: Kilowatts (kW)
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `reactivePower` : Reactive power. The actual values will be conveyed by
    subproperties which name will be equal to the name of each of the
    alternating current phases, typically R, S, T.

  - Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
  - Default unit: KiloVolts-Ampere-Reactive (kVArh)
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `powerFactor` : Power factor.

  - Attribute Type: [Number](http://schema.org/Number)
  - Allowed values: A number between -1 and 1.
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `cosPhi` : "Cosin of phi" parameter.

  - Attribute Type: [Number](http://schema.org/Number)
  - Allowed values: A number between -1 and 1.
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `intensity` : Electric intensity. The actual values will be conveyed by one
    subproperty per alternating current phase. The name of each subproperty will
    be equal to a phase mnemonic. The mnemonic used for denoting phases can vary
    depending on world regions. In Europe they are typically named as `R`, `S`,
    `T`.

  - Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
  - Default unit: Ampers (A)
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `voltage` : Electric tension. The actual values will be conveyed by one
    subproperty alternating current phase. The name of each subproperty will be
    equal to a phase mnemonic. The mnemonic used for denoting phases can vary
    depending on world regions. In Europe they are typically named as `R`, `S`,
    `T`.

  - Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
  - Default unit: Volts (V)
  - Attribute metadata:
        -   `timestamp`: Timestamp when the last update of the attribute
            happened.
            -   Type: [DateTime](http://schema.org/DateTime)
  - Optional

- `thdrVoltage` : Total harmonic distortion (R) of The name of each
    subproperty will be equal to a phase mnemonic. The mnemonic used for
    denoting phases can vary depending on world regions. In Europe they are
    typically named as `R`, `S`, `T`.

  - Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
  - Allowed values: A number between 0 and 1.
  - Optional

- `thdrIntensity` : Total harmonic distortion (R) of intensity. The name of
    each subproperty will be equal to a phase mnemonic. The mnemonic used for
    denoting phases can vary depending on world regions. In Europe they are
    typically named as `R`, `S`, `T`.

  - Attribute Type: [StructuredValue](http://schema.org/StructuredValue)
  - Allowed values: A number between 0 and 1.
  - Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of Use

    {
      "id": "streetlightcontrolcabinet:A45HGJK",
      "type": "StreetlightControlCabinet",
      "location": {
        "type": "Point",
        "coordinates": [  -3.164485591715449, 40.62785133667262 ]
      },
      "cupboardMadeOf": "plastic",
      "brandName": "Siemens",
      "modelName": "Simatic S7 1200",
      "refStreetlightGroup": ["streetlightgroup:BG678", "streetlightgroup:789"],
      "compliantWith": ["IP54"],
      "dateLastProgramming": "2016-07-08T16:04:30.201Z",
      "maximumPowerAvailable": 10,
      "energyConsumed": 162456,
      "dateMeteringStarted": "2013-07-07T15:05:59.408Z",
      "lastMeterReading": 161237,
      "meterReadingPeriod": 60,
      "intensity": {
         "R": 20.1,
         "S": 14.4,
         "T": 22
      },
      "reactivePower": {
        "R": 45,
        "S": 43.5,
        "T": 42
      },
      "workingMode": "automatic"
    }

## Test it with a real service

## Open Issues

-   Should we create a `StreetlightControlCabinetModel` entity type?
-   Should we have the programming parameters as attribute of this entity?
    Advantage is that if programming is the same for all the controlled cicuits
    then there is no need to repeat the same parameters over multiple entities.
