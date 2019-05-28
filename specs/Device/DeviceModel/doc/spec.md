# Device Model

## Description

This entity captures the static properties of a Device.

## Data Model

The data model is defined as shown below:

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `DeviceModel`.

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `category` : Device's category(ies).

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values, one of the following or any other meaningful to the
        application:
    -   `sensor` : A device that detects and responds to events or changes in
        the physical environment such as light, motion, or temperature changes.
        [https://w3id.org/saref#Sensor](https://w3id.org/saref#Sensor).
    -   `actuator` : A device responsible for moving or controlling a mechanism
        or system.
        [https://w3id.org/saref#Actuator](https://w3id.org/saref#Actuator).
    -   `meter` : A device built to accurately detect and display a quantity in
        a form readable by a human being. Partially defined by
        [SAREF](https://w3id.org/saref#Meter).
    -   `HVAC` : Heating, Ventilation and Air Conditioning (HVAC) device that
        provides indoor environmental comfort.
        [https://w3id.org/saref#HVAC](https://w3id.org/saref#HVAC).
    -   `network` : A device used to connect other devices in a network, such as
        hub, switch or router in a LAN or Sensor network.
        [(https://w3id.org/saref#Network](https://w3id.org/saref#Network).
    -   `multimedia` : A device designed to display, store, record or play
        multimedia content such as audio, images, animation, video.
        [https://w3id.org/saref#Multimedia](https://w3id.org/saref#Multimedia)
    -   Mandatory

-   `deviceClass` : Class of constrained device as specified by RFC 7228. If the
    device is not a constrained device this property can be left as `null` or
    undefined.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Normative References:
        [RFC7228](https://tools.ietf.org/html/rfc7228#section-3)
    -   Allowed values: (`C0`, `C1`, `C2`)
    -   Optional

-   `controlledProperty` : Anything that can be sensed, measured or controlled
    by.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (some of this values are defined as instances of the
        class `Property` in SAREF)
    -   (`temperature`, `humidity`, `light`, `motion`, `fillingLevel`,
        `occupancy`, `power`, `pressure`, `smoke`, `energy`, `airPollution`,
        `noiseLevel`, `weatherConditions`, `precipitation`, `windSpeed`,
        `windDirection`, `atmosphericPressure`, `solarRadiation`, `depth`, `pH`,
        `conductivity`, `conductance`, `tss`, `tds`, `turbidity`, `salinity`,
        `orp`, `cdom`, `waterPollution`, `location`, `speed`, `heading`,
        `weight`, `waterConsumption`, `gasComsumption`,
        `electricityConsumption`, `soilMoisture`, `trafficFlow`)
    -   Mandatory

-   `function` : The functionality necessary to accomplish the task for which a
    Device is designed. A device can be designed to perform more than one
    function. Defined by [SAREF](https://w3id.org/saref#Function).

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (`levelControl`, `sensing`, `onOff`, `openClose`,
        `metering`, `eventNotification`), from SAREF.
    -   Optional

-   `supportedProtocol` : Supported protocol(s) or networks.

    -   Attribute type: List of [Text](https://schema.org/Text).
    -   Allowed values: (`ul20`, `mqtt`, `lwm2m`, `http`, `websocket`, `onem2m`,
        `sigfox`, `lora`, `nb-iot`, `ec-gsm-iot`, `lte-m`, `cat-m`, `3g`,
        `grps`) or any other value meaningful for an application.
    -   Optional

-   `supportedUnits` : Units of measurement supported by the device.

    -   Attribute type: List of [Text](https://schema.org/Text).
    -   Allowed values: The unit code (text) of measurement given using the
        [UN/CEFACT Common Code](http://wiki.goodrelations-vocabulary.org/Documentation/UN/CEFACT_Common_Codes)
        (max. 3 characters).
    -   Optional

-   `energyLimitationClass` : Device's class of energy limitation as per
    RFC 7228.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Normative References:
        [RFC7228](https://tools.ietf.org/html/rfc7228#page-11)
    -   Allowed values: (`E0`, `E1`, `E2`, `E9`)
    -   Optional

-   `brandName` : Device's brand name.

    -   Attribute type: [Text](https://schema.org/Text)
    -   See also: [https://schema.org/brand](https://schema.org/brand)
    -   Mandatory

-   `modelName` : Device's model name.

    -   Attribute type: [Text](https://schema.org/Text)
    -   See also: [https://schema.org/model](https://schema.org/model)
    -   Mandatory

-   `manufacturerName` : Device's manufacturer name.

    -   Attribute type: [Text](https://schema.org/Text)
    -   See also: [https://schema.org/model](https://schema.org/model)
    -   Mandatory

-   `name` : Name given to this device model.

    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory

-   `description` : Device's description

    -   Normative References: [description](https://schema.org/description)
    -   Optional

-   `documentation` : A link to device's documentation.

    -   Attribute type: [URL](https://schema.org/URL)
    -   Optional

-   `image` : A link to an image depicting the concerned device.

    -   Normative References:
        [https://schema.org/image](https://schema.org/image)
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
    "id": "myDevice-wastecontainer-sensor-345",
    "type": "DeviceModel",
    "category": {
        "value": ["sensor"]
    },
    "function": {
        "value": ["sensing"]
    },
    "modelName": {
        "value": "S4Container 345"
    },
    "name": {
        "value": "myDevice Sensor for Containers 345"
    },
    "brandName": {
        "value": "myDevice"
    },
    "manufacturerName": {
        "value": "myDevice Inc."
    },
    "controlledProperty": {
        "value": ["fillingLevel", "temperature"]
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "myDevice-wastecontainer-sensor-345",
    "type": "DeviceModel",
    "name": "myDevice Sensor for Containers 345",
    "brandName": "myDevice",
    "modelName": "S4Container 345",
    "manufacturerName": "myDevice Inc.",
    "category": ["sensor"],
    "function": ["sensing"],
    "controlledProperty": ["fillingLevel", "temperature"]
}
```

## Test it with a real service

## Issues
