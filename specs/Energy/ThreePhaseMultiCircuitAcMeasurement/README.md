# Three-phase multi-circuit alternating current measurement

A ThreePhaseMultiCircuitAcMeasurement entity represents a measurement from
an electrical sub-metering system that monitors three-phase alternating
current across multiple circuits. Each circuit is assigned a voltage phase:
L1, L2 or L3; and has attributes for various electrical measurements such
as `current`, `power`, `energy`, `frequency`, and `harmonics`. There are 
cumulative metering values for each circuit (e.g. net energy) and the start
time for their measurement can be saved to the `dateEnergyMeteringStarted`
attribute. There are also attributes for different power and energy types
(`active`, `reactive` and `apparent`).
