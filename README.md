# FIWARE Data Models

[![FIWARE Core Context Management](https://nexus.lab.fiware.org/repository/raw/public/badges/chapters/core.svg)](https://www.fiware.org/developers/catalogue/)
[![License: MIT](https://img.shields.io/github/license/fiware/dataModels.svg)](https://opensource.org/licenses/MIT)
[![Support badge](https://img.shields.io/badge/support-askbot-yellowgreen.svg)](http://ask.fiware.org)
<br/>
[![Documentation](https://img.shields.io/readthedocs/fiware-datamodels.svg)](https://fiware-datamodels.rtfd.io)
[![Build badge](https://img.shields.io/travis/Fiware/dataModels.svg "Travis build status")](https://travis-ci.org/Fiware/dataModels/)


This repository contains:

-   [JSON Schemas and documentation](./specs/README.md) on harmonized datamodels
    for smart cities, developed jointly with [OASC](http://oascities.org), and
    other domains.
-   code that allows to expose different harmonized datasets useful for
    different applications. Such datasets are exposed through the
    [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
    API (query).

This work is aligned with the results of the
[GSMA IoT Big Data](http://www.gsma.com/connectedliving/iot-big-data/) Project.
Such project is working on the harmonization of APIs and data models for fueling
IoT and Big Data Ecosystems. In fact the FIWARE data models are a superset of
the
[GSMA Data Models](http://www.gsma.com/connectedliving/wp-content/uploads/2016/11/CLP.26-v1.0.pdf).




| :books: [Documentation](https://fiware-datamodels.rtfd.io) |
| ---|


## Data Models adoption

To support the adoption, we created a short [guideline](specs/howto.md) for the
usage of data models.

## JSON Schemas

We intend to provide a [JSON Schema](http://json-schema.org/) for every
harmonized data model. In the future all the documentation could be generated
from a JSON Schema, as it is part of our roadmap. The different JSON Schemas
usually depend on common JSON Schema definitions found at the root directory of
this repository.

There are different online JSON Schema Validators, for instance:
[http://jsonschemalint.com/](http://jsonschemalint.com/). For the development of
these schemas the
[AJV JSON Schema Validator](https://github.com/epoberezkin/ajv) is being used.
For using it just install it through npm:

```
    npm install ajv
    npm install ajv-cli
```

A `validate.sh` script is provided for convenience.

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## How to contribute

Contributions should come in the form of pull requests.

New data models should be added under a folder structured as follows:

-   `specs/`
    -   `NewModel/`
        -   `doc/`
            -   `spec.md`: A data model description based on the
                [data model template](datamodel_template.md), e.g.
                [spec.md of WeatherObserved](specs/Weather/WeatherObserved/doc/spec.md).
        -   `README.md`: A summary file (as an extract from the spec file), e.g.
            [README.md of WeatherObserved](specs/Weather/WeatherObserved/README.md)
        -   `schema.json`: The JSON Schema definition, e.g.
            [schema.json of WeatherObserved](specs/Weather/WeatherObserved/schema.json)
        -   `example.json`: One or more JSON example file, e.g.
            [example.json of WeatherObserved](specs/Weather/WeatherObserved/example.json)

The name of the folder should match the entity type used in the JSON Schema
(e.g. `NewModel`). For data models including more entities, a hierarchical
folder should be used. The father folder can include common JSON schemas shared
among the entities. e.g.:

-   `specs/`
    -   `NewModel/`
        -   `doc/`
            -   `spec.md`
        -   `README.md`
        -   `newmodel-schema.json`: the common schema for the different
            entities.
        -   `NewModelEntityOne/`
            -   `doc/`
                -   `spec.md`
            -   `README.md`
            -   `schema.json`
            -   `example.json`
        -   `NewModelEntityTwo/`
            -   `doc/`
                -   `spec.md`
            -   `README.md`
            -   `schema.json`
            -   `example.json`

To facilitate contributions and their validation, we developed a tool that is
also used for the Continuous Integration of FIWARE Data Models. The FIWARE Data
Model validator checks the adherence of each data model to the
[FIWARE Data Models guidelines](specs/guidelines.md).

For using it just install it through npm:

```console
npm install -g fiware-model-validator
```

More details are available in the [validator documentation](validator).

### Formatting and Text Correction

When creating a Pull Request, please ensure the files are properly formatted,
the [Husky](https://github.com/typicode/husky) should do this automatically on
`git commit`, but the files can be manually formatted at any time using the
`prettier` and `prettier:text` commands:

```console
cd validator
npm i

# To format JavaScript files:
npm run prettier

# To format Markdown files:
npm run prettier:text
```

To check for spelling mistakes and dead links in the text within the Data 
Model, run the text linter as shown:

```console
npm test
```

```console
npm run lint:text
```

[license-image]: https://img.shields.io/badge/license-MIT-blue.svg
[license-url]: LICENSE

## Related Projects

See:

-   [https://github.com/GSMADeveloper/HarmonisedEntityDefinitions](https://github.com/GSMADeveloper/HarmonisedEntityDefinitions)
-   [https://github.com/GSMADeveloper/HarmonisedEntityReferences](https://github.com/GSMADeveloper/HarmonisedEntityReferences)
-   [schema.org](https://schema.org)
-   [https://github.com/GSMADeveloper/NGSI-LD-Entities](https://github.com/GSMADeveloper/NGSI-LD-Entities)


---

## License

### Code

[MIT](LICENSE) © 2019 FIWARE Foundation e.V.

[![License: MIT](https://img.shields.io/github/license/fiware/dataModels.svg)](https://opensource.org/licenses/MIT)

All the code in this repository is licensed under the MIT License. However each
original data source may have a different license. So before using harmonized
data please check carefully each data license.

### Models

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

All the data models documented here are offered under a
[Creative Commons by Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
License.
