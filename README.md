# FIWARE Data Models

[![FIWARE Core Context Management](https://img.shields.io/badge/FIWARE-Core-233c68.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAVCAYAAAC33pUlAAAABHNCSVQICAgIfAhkiAAAA8NJREFUSEuVlUtIFlEUx+eO+j3Uz8wSLLJ3pBiBUljRu1WLCAKXbXpQEUFERSQF0aKVFAUVrSJalNXGgmphFEhQiZEIPQwKLbEUK7VvZrRvbr8zzjfNl4/swplz7rn/8z/33HtmRhn/MWzbXmloHVeG0a+VSmAXorXS+oehVD9+0zDN9mgk8n0sWtYnHo5tT9daH4BsM+THQC8naK02jCZ83/HlKaVSzBey1sm8BP9nnUpdjOfl/Qyzj5ust6cnO5FItJLoJqB6yJ4QuNcjVOohegpihshS4F6S7DTVVlNtFFxzNBa7kcaEwUGcbVnH8xOJD67WG9n1NILuKtOsQG9FngOc+lciic1iQ8uQGhJ1kVAKKXUs60RoQ5km93IfaREvuoFj7PZsy9rGXE9G/NhBsDOJ63Acp1J82eFU7OIVO1OxWGwpSU5hb0GqfMydMHYSdiMVnncNY5Vy3VbwRUEydvEaRxmAOSSqJMlJISTxS9YWTYLcg3B253xsPkc5lXk3XLlwrPLuDPKDqDIutzYaj3eweMkPeCCahO3+fEIF8SfLtg/5oI3Mh0ylKM4YRBaYzuBgPuRnBYD3mmhA1X5Aka8NKl4nNz7BaKTzSgsLCzWbvyo4eK9r15WwLKRAmmCXXDoA1kaG2F4jWFbgkxUnlcrB/xj5iHxFPiBN4JekY4nZ6ccOiQ87hgwhe+TOdogT1nfpgEDTvYAucIwHxBfNyhpGrR+F8x00WD33VCNTOr/Wd+9C51Ben7S0ZJUq3qZJ2OkZz+cL87ZfWuePlwRcHZjeUMxFwTrJZAJfSvyWZc1VgORTY8rBcubetdiOk+CO+jPOcCRTF+oZ0okUIyuQeSNL/lPrulg8flhmJHmE2gBpE9xrJNkwpN4rQIIyujGoELCQz8ggG38iGzjKkXufJ2Klun1iu65bnJub2yut3xbEK3UvsDEInCmvA6YjMeE1bCn8F9JBe1eAnS2JksmkIlEDfi8R46kkEkMWdqOv+AvS9rcp2bvk8OAESvgox7h4aWNMLd32jSMLvuwDAwORSE7Oe3ZRKrFwvYGrPOBJ2nZ20Op/mqKNzgraOTPt6Bnx5citUINIczX/jUw3xGL2+ia8KAvsvp0ePoL5hXkXO5YvQYSFAiqcJX8E/gyX8QUvv8eh9XUq3h7mE9tLJoNKqnhHXmCO+dtJ4ybSkH1jc9XRaHTMz1tATBe2UEkeAdKu/zWIkUbZxD+veLxEQhhUFmbnvOezsJrk+zmqMo6vIL2OXzPvQ8v7dgtpoQnkF/LP8Ruu9zXdJHg4igAAAABJRU5ErkJgggA=)](https://www.fiware.org/developers/catalogue/)
[![License: MIT](https://img.shields.io/github/license/fiware/dataModels.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/readthedocs/fiware-datamodels.svg)](https://fiware-datamodels.rtfd.io)
[![Build badge](https://img.shields.io/travis/Fiware/dataModels.svg "Travis build status")](https://travis-ci.org/Fiware/dataModels/)
[![Support badge](https://img.shields.io/badge/support-askbot-yellowgreen.svg)](http://ask.fiware.org)

This repository contains: 
* [JSON Schemas and documentation](./specs/README.md) on harmonized datamodels for smart cities, developed jointly with [OASC](http://oascities.org), and other domains. 
* code that allows to expose different harmonized datasets useful for different applications.
Such datasets are exposed through the [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API (query).

This work is aligned with the results of the
[GSMA IoT Big Data](http://www.gsma.com/connectedliving/iot-big-data/) Project.
Such project is working on the harmonization of APIs and data models for fueling IoT and Big Data Ecosystems.
In fact the FIWARE datamodels are a superset of the [GSMA Data Models](http://www.gsma.com/connectedliving/wp-content/uploads/2016/11/CLP.26-v1.0.pdf). 

All the code in this repository is licensed under the MIT License. However each original data source may have a different license.
So before using harmonized data please check carefully each data license.

All the datamodels documented here are offered under a [Creative Commons by Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) License.

## JSON Schemas

We intend to provide a [JSON Schema](http://json-schema.org/) for every harmonized data model. In the future all the
documentation could be generated from a JSON Schema, as it is part of our roadmap. The different JSON Schemas usually
depend on common JSON Schema definitions found at the root directory of this repository. 

There are different online JSON Schema Validators, for instance: [http://jsonschemalint.com/](http://jsonschemalint.com/).
For the development of these schemas the [AJV JSON Schema Validator](https://github.com/epoberezkin/ajv) is being used. For
using it just install it through npm: 

```
    npm install ajv
    npm install ajv-cli
```

A `validate.sh` script is provided for convenience.

**Note**: JSON Schemas only capture the NGSI simplified representation, this means that to test the JSON schema examples with
a [FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable) API implementation, you need to use the `keyValues`
mode (`options=keyValues`).

## How to contribute

Contributions should come in the form of pull requests. 

New data models should be added under a folder structured as follows:
- `specs/`
  - `NewModel/`
    - `doc/`
      - `spec.md`: A data model description based on the [data model template](datamodel_template.md), e.g. [spec.md of WeatherObserved](specs/Weather/WeatherObserved/doc/spec.md).
    - `README.md`: A summary file (as an extract from the spec file), e.g. [README.md of WeatherObserved](specs/Weather/WeatherObserved/README.md)
    - `schema.json`: The JSON Schema definition, e.g. [schema.json of WeatherObserved](specs/Weather/WeatherObserved/schema.json)
    - `example.json`: One or more JSON example file, e.g. [example.json of WeatherObserved](specs/Weather/WeatherObserved/example.json)

The name of the folder should match the entity type used in the JSON Schema (e.g. `NewModel`). For data models including more entities, a hierarchical folder should be used. The father folder can include common JSON schemas shared among the entities. e.g.:

- `specs/`
  - `NewModel/`
    - `doc/`
      - `spec.md`
    - `README.md`
    - `newmodel-schema.json`: the common schema for the different entities.
    - `NewModelEntityOne/`
      - `doc/`
        - `spec.md`
      - `README.md`
      - `schema.json`
      - `example.json`
    - `NewModelEntityTwo/`
      - `doc/`
        - `spec.md`
      - `README.md`
      - `schema.json`
      - `example.json`

To facilitate contributions and their validation, we developed a tool that is also used for the Continuous Integration of FIWARE Data Models. The FIWARE IWARE Data Model validator checks the adherence of each data model to the [FIWARE Data Models guidelines](specs/guidelines.md).

For using it just install it through npm: 

```
   npm install -g fiware-model-validator
```

More details are available in the [validator documentation](validator).

[license-image]: https://img.shields.io/badge/license-MIT-blue.svg
[license-url]: LICENSE

## Related Projects 

See:

* [https://github.com/GSMADeveloper/HarmonisedEntityDefinitions](https://github.com/GSMADeveloper/HarmonisedEntityDefinitions)
* [https://github.com/GSMADeveloper/HarmonisedEntityReferences](https://github.com/GSMADeveloper/HarmonisedEntityReferences)
* [schema.org](https://schema.org)
