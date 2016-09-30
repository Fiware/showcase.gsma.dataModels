# Air Quality Observed

An observation of air quality conditions at a certain place and time.
This data model has been developed in cooperation with mobile operators and the [GSMA](http://www.gsma.com/connectedliving/iot-big-data/). 

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
    
+ `measurand` : An array of strings containing details (see format below) about each *air quality* measurand observed.
    + Attribute type: List of [Text](https://schema.org/Text).
    + Allowed values: Each element of the array must be a string with the following format (comma separated list of values):
`<measurand>, <observedValue>, <unitcode>, <description>, <timestamp>`, where:
        + `measurand` : corresponds to the chemical formula (or mnemonic) of the measurand, ex. CO.
        + `observedValue` : corresponds to the value for the measurand as a number. 
        + `unitCode` : The unit code (text) of measurement given using the
        [UN/CEFACT Common Code](http://wiki.goodrelations-vocabulary.org/Documentation/UN/CEFACT_Common_Codes) (max. 3 characters)
        + `description` : short description of the measurand.
        + `timestamp` : optional timestamp for the observed value in ISO8601 format.
        It can be ommitted if the observation time is the same as the one captured by the `dateObserved` attribute at entity level. 
        + Examples:
    `"CO,500,M1,Carbon Monoxide"  "NO,45,M1,Nitrogen Monoxide" "NO2,69,M1,Nitrogen Dioxide" "NOx,139,M1,Nitrogen oxides" "SO2,11,M1,Sulfur Dioxide"`
    + Mandatory
    
+ `temperature` : Air's temperature observed.
    + Attribute type: [Number](https://schema.org/(Number)
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional

+ `relativeHumidity` : Air's relative humidity observed.
    + Attribute type: [Number](https://schema.org/(Number)
    + Allowed values: A number between 0 and 1. 
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional

+ `precipitation` : Precipitation level observed.
    + Attribute type: [Number](https://schema.org/(Number)
    + Default unit: Liters per square meter.
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional 

+ `windDirection` : The wind direction expressed in decimal degrees compared to geographic North (measured clockwise), encoded as a Number.
    + Attribute type: [Number](https://schema.org/(Number)
    + Default unit: Decimal degrees
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional 

+ `windSpeed` : The observed wind speed in m/s, encoded as a Number
    + Attribute type: [Number](https://schema.org/(Number)
    + Default unit: meters per second
    + Attribute metadata:
        + `timestamp` : optional timestamp for the observed value. It can be ommitted if the observation time is the same as the one captured
        by the `dateObserved` attribute at entity level.
    + Optional 

+ `source` : A sequence of characters giving the source of the entity data.
    + Attribute type: [Text](https://schema.org/Text) or [URL](https://schema.org/URL)
    + Optional

+ `refDevice` : A reference to the device which captured this observation
    + Attribute type: Reference to an entity of type `Device`
    + Optional

+ `refPointOfInterest` : A reference to a point of interest (usually an air quality station) associated to this observation.
    + Attribute type: Reference to an entity of type `PointOfInterest`
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
        "coordinates": [40.423852777777775, -3.712247222222222]
      },
      "source": "http://datos.madrid.es",
      "measurand": [
         "CO, 500, M1, Carbon Monoxide",
         "NO, 45, M1, Nitrogen Monoxide",
         "NO2, 69, M1, Nitrogen Dioxide",
         "NOx, 139, M1, Nitrogen oxides",
         "SO2, 11, M1, Sulfur Dioxide"
      ],
      "precipitation": 0,
      "relativeHumidity": 54,
      "temperature": 12.2,
      "windDirection": 186,
      "windSpeed": 0.64,
      "refPointOfInterest": "28079004-Pza. de España"
    }