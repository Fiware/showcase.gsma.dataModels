# Device

## Description

An apparatus (hardware + software + firmware) intended to accomplish a particular task (sensing the environment, actuating, etc.).
A Device is a tangible object which contains some logic and is producer and/or consumer of data.
A Device is always assumed to be capable of communicating electronically via a network.

This data model has been partially developed in cooperation with mobile operators and the [GSMA](http://www.gsma.com/connectedliving/iot-big-data/).

This data model reuses concepts coming from the [SAREF Ontology](http://www.etsi.org/deliver/etsi_ts/103200_103299/103264/01.01.01_60/ts_103264v010101p.pdf)
part of [ETSI](http://www.etsi.org) standards.

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `Device`.

+ `category` : See attribute `category` from [DeviceModel](../../DeviceModel/doc/spec.md). Optional but recommended to optimize queries.
        
+ `controlledProperty` : See attribute `controlledProperty` from [DeviceModel](../../DeviceModel/doc/spec.md). Optional but recommended to optimize queries.

+ `controlledAsset` : The asset(s) (building, object, etc.) controlled by the device.
    + Attribute type: List of [Text](https://schema.org) or Reference(s) to another entity.
    + Optional

+ `mnc` : This property identifies the Mobile Network Code (MNC) of the network the device is attached to.
The MNC is used in combination with a Mobile Country Code (MCC) (also known as a "MCC / MNC tuple")
to uniquely identify a mobile phone operator/carrier using the GSM, CDMA, iDEN, TETRA
and 3G / 4G public land mobile networks and some satellite mobile networks.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional

+ `mcc` : Mobile Country Code - This property identifies univoquely the country of the mobile network the device is attached to.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional
    
+ `macAddress` : The MAC address of the device.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional
    
+ `ipAddress` : The IP address of the device. It can be a comma separated list of values if the device has more than one IP address. 
    + Attribute type: [Text](https://schema.org/Text)
    + Optional

+ `supportedProtocol` : See attribute `supportedProtocol` from [DeviceModel](../../DeviceModel/doc/spec.md). Needed if due to a software update
new protocols are supported. Otherwise it is better to convey it at `DeviceModel` level. 

+ `configuration` : Device's technical configuration. This attribute is intended to be a dictionary of properties which capture
parameters which have to do with the configuration of a device (timeouts, reporting periods, etc.)
and which are not currently covered by the standard attributes defined by this model. 
    + Attribute type: [StructuredValue](https://schema.org/StructuredValue)
    + Attribute metadata:
        + `dateModified` :  It captures the last modification timestamp of this attribute.
            + Type: [DateTime](https://schema.org/DateTime) 
    + Optional
    
+ `location` : Location of this device represented by a GeoJSON geometry of type point. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Optional.
    
+ `name` : A mnemonic name given to the device.
    + Normative References: [name](https://schema.org/name)
    + Optional

+ `description` : Device's description.
    + Normative References: [description](https://schema.org/description)
    + Optional

+ `dateInstalled` : A timestamp which denotes when the device was installed (if it requires installation).
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateFirstUsed` : A timestamp which denotes when the device was first used.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateManufactured` : A timestamp which denotes when the device was manufactured.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `hardwareVersion` : The hardware version of this device.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional

+ `softwareVersion` : The software version of this device.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional

+ `firmwareVersion` : The firmware version of this device.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional

+ `osVersion` : The version of the host operating system device.
    + Attribute type: [Text](https://schema.org/Text)
    + Optional

+ `dateLastCalibration` : A timestamp which denotes when the last calibration of the device happened.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional
    
+ `serialNumber` : The serial number assigned by the manufacturer.
    + Normative References: [https://schema.org/serialNumber](https://schema.org/serialNumber)
    + Mandatory
    
+ `provider` : The provider of the device.
    + Normative References: [https://schema.org/provider](https://schema.org/provider)
    + Optional

+ `refDeviceModel` : The device's model.
    + Attribute type: Reference to an entity of type [DeviceModel](../../DeviceModel/doc/spec.md).
    + Optional

+ `batteryLevel` : Device's battery level. It must be equal to `1.0` when battery is full. `0.0` when battery ìs empty.
`null` when cannot be determined. 
    + Type: [Number](https://schema.org/Number)
    + Allowed values: Interval [0,1]
    + Attribute metadata:
        + `timestamp`: Timestamp when the last update of the attribute happened.
        This value can also appear as a FIWARE [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib#TimeInstant)
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional
    
+ `deviceState` : State of this device from an operational point of view. Its value can be vendor dependent.  
    + Type: [Text](https://schema.org/Text)
    + Attribute metadata:
        + `timestamp`: Timestamp when the last update of the attribute happened.
        This value can also appear as a FIWARE [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib#TimeInstant)
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional

+ `dateLastValueReported` : A timestamp which denotes the last time when the device successfully reported data to the cloud.
    + Attribute type: [DateTime](https://schema.org/)
    + Optional

+ `value` : A observed or reported value. For actuator devices, it is an attribute that allows
a controlling application to change the actuation setting. For instance, a switch device which is currently *on* can report a value `"on"`of type `Text`.
Obviously, in order to toggle the referred switch, this attribute value will have to be changed to `"off"`.
    + Attribute type: Any type, depending on the device. Usually [Text](https://schema.org/Text) or [QuantitativeValue](https://schema.org/QuantitativeValue).
    + Attribute metadata:
        + `timestamp`: Timestamp when the last update of the attribute happened.
        This value can also appear as a FIWARE [TimeInstant](https://github.com/telefonicaid/iotagent-node-lib#TimeInstant)
            + Type: [DateTime](http://schema.org/DateTime)
    + Optional
    
+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional    

+ `owner` : Entity's owners: an array of entities that represents the owners of an Thing.
    + Attribute type: List of [Person]( http://schema.org/Person) or [Organization](https://schema.org/Organization).
    + Optional

## Examples

    {
      "id": "device-9845A",
      "type": "Device",
      "category": ["sensor"],
      "controlledProperty": ["fillingLevel","temperature"],
      "controlledAsset": ["wastecontainer-Osuna-100"],
      "ipAddress": "192.14.56.78",
      "mcc": "214",
      "mnc": "07",
      "batteryLevel": 0.75,
      "serialNumer": "9845A",
      "refDeviceModel": "myDevice-wastecontainer-sensor-345",
      "value": "l=0.22;t=21.2",
      "deviceState": "ok",
      "dateFirstUsed": "2014-09-11",
      "owner": ["http://person.org/leon"]
    }


## Test it with a real service

T.B.D.

## Issues

+ Is `function` really needed?
+ Do we need a `state` attribute as it happens in SAREF?
+ Check consistency with oneM2M and SAREF ontologies. 
