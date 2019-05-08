# FIWARE IoT-BigData Instance 

## Table of Contents

-   [Introduction](#introduction)
-   [Public Data sources](#public-data-sources)
-   [Data / IoT Device providers](#data-/-iot-device-providers)
-   [Endpoints](#endpoints)
-   [Harmonized data published](#harmonized-data-published)
-   [Useful links](#useful-links)
-   [Examples](#examples)

### Introduction
This document describes the IoT-BD instance developed under the [GSMA IoT Big Data Project](https://www.gsma.com/iot/connected-living-mobilising-the-internet-of-things/), part of GSMA’s Connected Living Programme.

### Public Data sources
Here there is a description of the original public data sources used to perform data harmonization. 

<table border="0">
<thead>
<tr>
<th>Entity Type</th>
<th>Public Data source(s)</th>
<th>URLs</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2">AirQualityObserved</td>
<td>Generalidad de Catalu&ntilde;a (only Barcelona&rsquo;s data)</td>
<td>http://dtes.gencat.cat/icqa/</td>
</tr>
<tr>
<td>Ayuntamiento de Madridr</td>
<td>http://datos.madrid.es/egob/catalogo/212531-7916318-calidad-aire-tiempo-real.txt</td>
</tr>
<tr>
<td rowspan="2">WeatherObserved WeatherForecast</td>
<td>Agencia Estatal de Meteorolog&iacute;a (AEMET)</td>
<td>http://www.aemet.es</td>
</tr>
<tr>
<td>Instituto portugu&ecirc;s do mar y do atmosfera (IPMA)</td>
<td>https://www.ipma.pt/pt/index.html</td>
</tr>
<tr>
<td>Alert</td>
<td>The Network of European Meteorological Services (EUMETNET)</td>
<td>http://www.meteoalarm.eu/</td>
</tr>
<tr>
<td>PointOfInterest</td>
<td>Ineco</td>
<td>https://www.ineco.com/webineco/</td>
</tr>
<tr>
<td>Vehicle OffStreetParking</td>
<td>Fiware Foundation e.V.</td>
<td>https://fiware.org</td>
</tr>
</tbody>
</table>

The usage of the data offered through this instance is subject to the terms, conditions and licenses expressed by the original data sources. In the table below, for each data source you can find a link to them.

| Data source                                                | Terms and Conditions                                                                   |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Generalidad de Cataluña                                    | <http://web.gencat.cat/ca/menu-ajuda/ajuda/avis_legal/> (Spanish)                      |
| Madrid                                                     | <http://www.mambiente.munimadrid.es/opencms/opencms/calaire/avisoLegal.html> (Spanish) |
| AEMET Agencia Estatal de Meteorología                      | <http://www.aemet.es/es/nota_legal> (Spanish)                                          |
| IPMA Instituto português do mar y do atmosfera             | <https://www.ipma.pt/en/siteinfo/index.html?page=index.xml> (English)                  |
| The Network of European Meteorological Services (EUMETNET) | <http://www.meteoalarm.eu/terms.php?lang=en_UK> (English)                              |
| Ineco                                                      |                                                                                        |
| FIWARE Foundation e.V.                                     |                                                                                        |

### Data / IoT Device providers
Below there is a list of data / IoT Device providers who kindly are publishing a sample of their data to this instance. Such data must not be used for commercial purposes without the consent of their owners. 

| Data Provider  | Data offered                                                          |
| -------------- | --------------------------------------------------------------------- |
| EDP Ingeniería | Air quality data from Málaga (Spain). Sensors mounted on public buses |
| Urban Clouds   | Air quality data from Málaga (Spain). Sensors mounted on bicycles     |
| Kunak          | Air quality data from Pamplona (Spain)                                |
| Turespaña      | A sample of points of interest in Spain                               |

### Endpoints
| Endpoint                          | URL                            |
| --------------------------------- | ------------------------------ |
| Harmonized data endpoint (NGSIv2) | <https://orion.lab.fiware.org> |

### Useful links
| Information                    | URL                                                                   |
| ------------------------------ | --------------------------------------------------------------------- |
| Harmonized data models by GSMA | <https://www.gsma.com/iot/wp-content/uploads/2016/06/CLP.26-v4.0.pdf> |
| Data model by FIWARE           | <https://www.fiware.org/developers/data-models/>                      |

### Harmonized data published
Below there is a description of the harmonized data currently published

<table border="0">
<thead>
<tr>
<th>Entity Type</th>
<th>FIWARE Service</th>
<th>FIWARE Service Path</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2">AirQualityObserved</td>
<td rowspan="2">airquality</td>
<td>/Barcelona</td>
 </tr>
 <tr>
<td>/Madrid </td>
</tr>
<tr>
<td rowspan="2">WeatherObserved</td>
<td rowspan="2">weather</td>
<td>/Spain</td>
 </tr>
 <tr>
<td>/Portugal</td>
</tr>
<tr>
<td rowspan="2">WeatherForecast</td>
<td rowspan="2">weather</td>
<td>/Spain</td>
 </tr>
 <tr>
 <td>/Portugal</td>
</tr>
<tr>
<td>PointOfInterest</td>
<td>poi</td>
<td>/Spain</td>
</tr>
<tr>
<td>Alert</td>
<td>weather</td>
<td>/Spain</td>
</tr>
</tbody>
</table>

### Examples

Some Postman recipes prepared, you can read documents [here](https://documenter.getpostman.com/view/3940441/RznEMKdr).
Be aware, Postman recipes use environment variables, don't forget to change it to "FIWARE Data Streams"
