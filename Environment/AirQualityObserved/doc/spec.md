# Air Quality Observed

## Description

An observation of air quality conditions at a certain place and time.
This data model has been developed in cooperation with mobile operators and the [GSMA](http://www.gsma.com/connectedliving/iot-big-data/). 

## Data Model

+ `id` : Unique identifier. 

+ `type` : Entity type. It must be equal to `AirQualityObserved`.

+ `dateModified` : Last update timestamp of this entity.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional

+ `dateCreated` : Entity's creation timestamp.
    + Attribute type: [DateTime](https://schema.org/DateTime)
    + Optional    

+ `location` : Location of the air quality observation represented by a GeoJSON geometry. 
    + Attribute type: `geo:json`.
    + Normative References: [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    + Mandatory if `address` is not defined. 
    
+ `address` : Civic address of the air quality observation. Sometimes it corresponds to the air quality station address.
    + Normative References: [https://schema.org/address](https://schema.org/address)
    + Mandatory if `location` is not present. 
    
+ `dateObserved` : The date and time of this observation in ISO8601 UTCformat. It can be represented by an specific time instant or by an ISO8601 interval. 
    + Attribute type: [DateTime](https://schema.org/DateTime) or an ISO8601 interval represented as [Text](https://schema.org/Text). 
    + Mandatory
    
+ `source` : A sequence of characters giving the source of the entity data.
    + Attribute type: [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    + Optional

+ `refDevice` : A reference to the device(s) which captured this observation.
    + Attribute type: Reference to an entity of type `Device`
    + Optional

+ `refPointOfInterest` : A reference to a point of interest (usually an air quality station) associated to this observation.
    + Attribute type: Reference to an entity of type `PointOfInterest`
    + Optional    

### Representing air pollutants

The number of air pollutants represented can vary. As a result the model prescribes the following attributes to convey those parameters: 

+ `measurand` : An array of strings containing details (see format below) about *each air quality measurand* observed.
    + Attribute type: List of [Text](https://schema.org/Text).
    + Allowed values: Each element of the array must be a string with the following format (comma separated list of values):
`<measurand>, <observedValue>, <unitcode>, <description>`, where:
        + `measurand` : corresponds to the chemical formula (or mnemonic) of the measurand, ex. CO.
        + `observedValue` : corresponds to the value for the measurand as a number. 
        + `unitCode` : The unit code (text) of measurement given using the
        [UN/CEFACT Common Code](http://wiki.goodrelations-vocabulary.org/Documentation/UN/CEFACT_Common_Codes) (max. 3 characters).
        For instance, `GP` represents milligrams per cubic meter and `GQ` represents micrograms per cubic meter.
        + `description` : short description of the measurand.
        + Examples:
    `"CO,500,GP,Carbon Monoxide"  "NO,45,GQ,Nitrogen Monoxide" "NO2,69,GQ,Nitrogen Dioxide" "NOx,139,GQ,Nitrogen oxides" "SO2,11,GQ,Sulfur Dioxide"`
    + Mandatory

+ In order to enable a proper management of the *historical evolution* of the concentrations of the different pollutants,
*for each* element described by the `measurand` array list there *MAY* be an attribute which name *MUST* be exactly equal to the
measurand name described on the `measurand` array. The structure of such an attribute will be as follows:
    + Attribute name: Equal to the name of the measurand, for instance `CO`.
    + Attribute type: [Number](https://schema.org/Number)
    + Attribute value: Exactly equal (same unit of measurement) to the value provided in the `measurand` array. 
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value in ISO8601 format.
        It can be ommitted if the observation time is the same as the one captured by the `dateObserved` attribute at entity level.
            + Type: [DateTime](https://schema.org/DateTime)

    
### Representing airquality-related weather conditions

Certain weather conditions have an influence over the observed air quality. There are two options for representing them:

+ A/ Through a linked entity of type `WeatherObserved` (attribute named `refWeatherObserved`) which will capture the associated weather conditions.
+ B/ Through a set of attributes which denote the different meteorological conditions under which the air quality data was captured. 

Below is the description of the attribute to be used for option A/. 

+ `refWeatherObserved` : Weather observed associated to the air quality conditions described by this entity.
    + Attribute type: Reference to a `WeatherObserved` entity.
    + Optional
    
Below is a list of typical weather observed parameters which may be included inline (option B/) by this entity type: 
    
+ `temperature` : Air's temperature observed.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Degrees centigrades.
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional

+ `relativeHumidity` : Air's relative humidity observed (percentage, expressed in parts per one).
    + Attribute type: [Number](https://schema.org/Number)
    + Allowed values: A number between `0` and `1`. 
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional

+ `precipitation` : Precipitation level observed.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Liters per square meter.
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional 

+ `windDirection` : The wind direction expressed in decimal degrees compared to geographic North (measured clockwise), encoded as a Number.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Decimal degrees
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional 

+ `windSpeed` : The observed wind speed in m/s, encoded as a Number.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: meters per second
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional
    
+ `barometricPressure` : The barometric pressure observed measured in Hecto Pascals.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Hecto Pascals
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional 

+ `solarRadiation` : The solar radiation observed measured in Watts per square meter.
    + Attribute type: [Number](https://schema.org/Number)
    + Default unit: Watts per square meter
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional

    
## Examples of use

    {
      "id": "Madrid-AmbientObserved-28079004-2016-03-15T11:00:00",
      "type": "AirQualityObserved",
      "address": {
        "addressCountry": "ES",
        "addressLocality": "Madrid",
        "streetAddress": "Plaza de España"
      },
      "dateObserved": "2016-03-15T11:00:00/2016-03-15T12:00:00",
      "location": {
        "type": "Point",
        "coordinates": [-3.712247222222222, 40.423852777777775]
      },
      "source": "http://datos.madrid.es",
      "precipitation": 0,
      "relativeHumidity": 0.54,
      "temperature": 12.2,
      "windDirection": 186,
      "windSpeed": 0.64,
      "measurand": [
         "CO, 500, GP, Carbon Monoxide",
         "NO, 45, GQ, Nitrogen Monoxide",
         "NO2, 69, GQ, Nitrogen Dioxide",
         "NOx, 139, GQ, Nitrogen oxides",
         "SO2, 11, GQ, Sulfur Dioxide"
      ],
      "CO": 500,
      "NO": 45,
      "NO2": 69,
      "NOx": 139,
      "SO2": 11,
      "refPointOfInterest": "28079004-Pza. de España"
    }
    
## Use it with a real service

To get access to a public instance offering air quality observed data please have a look at the [GSMA's API Directory](http://apidirectory.connectedliving.gsma.com/api/air-quality-spain). 

The instance described [here](https://docs.google.com/document/d/1lHP7XS-7TNzsxLa0bNFb-96JnJXh0ecIHS3-H0qMREg/edit?usp=sharing) has been set up by the FIWARE Community.


```curl -S -H 'fiware-service:airquality' -H 'fiware-servicepath:/Spain_Madrid' -H 'x-auth-token:<my_token>' "http://130.206.118.244:1027/v2/entities?options=keyValues&q=dateObserved:2016-11-28T12:00;stationCode:'28079004'"```

## Open Issues

* Should `measurand` be an `StructuredValue` instead of an array? 