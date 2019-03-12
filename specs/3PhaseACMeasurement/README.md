# Three-phase alternating current measurement

A 3PhaseACMeasurement entity represents a measurement from an electrical system
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

This model was developed in [Tampere University](http://www.tuni.fi) as a part
of the [CityIoT project](https://www.cityiot.fi/english). Its basis was
electrical measurements included in the
[StreetlightControlCabinet](https://fiware-datamodels.readthedocs.io/en/latest/StreetLighting/StreetlightControlCabinet/doc/spec/index.html)
entity of the
[Street Lighting data model](https://fiware-datamodels.readthedocs.io/en/latest/StreetLighting/doc/introduction/index.html).
