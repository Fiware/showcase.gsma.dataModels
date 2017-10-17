# FIWARE Data Model validator

FIWARE Data Model validator is an utility to help the management of NGSI DataModels. Its code leverage on the [AJV JSON Schema Validator](https://github.com/epoberezkin/ajv).

The FIWARE Data Model validator perform the following checks for each Data Model:
* validity of JSON Schema
* validity of JSON Examples
* adherence of Data Model name to FIWARE Data Models guidelines
* existence of Doc folder
* existence of JSON Schema
* existence of one or more JSON examples
* existence of README file

##  Install the validator
To install the validator on your machine, you need nodejs 7.0.0+. Instructions on how
to install nodejs are available [here](https://nodejs.org/en/download/package-manager/).

Once nodejs installed in your system, you can install the validator with the following command:

```
npm install -g fiware-model-validator
```

## Using the validator
To use the validator, execute it from the root of the DataModel repository:
```
validate -p DataModel -w ignore -i [common-schema.json,geometry-schema.json]
```

Command line available options are:

*  ``-i, --dmv:importSchemas``.  Additional schemas that will be included during validation. Default imported schemas are: common-schema.json, geometry-schema.json   [array]
* ``-w, --dmv:warnings``. How to handle FIWARE Data Models checks warnings.
  * ``true (default)`` - print warnings, but does not fail.
  * `ignore` -  do nothing and do not print warnings.
  * `fail` - print warnings, and fails.         
* ``-p, --dmv:path``. The path of FIWARE Data Model(s) to be validated (if recursion enabled, it will be the starting point of recursion)
* ``-h, --help``. Print the help message

If you want to execute `validate` outside the root directory and you want to import the common schemas, you have to import them using the correct path.

### Default configuration
For a more fine grained configuration you can create a `config.json` file. An example is provided in the repository.

Options available are:
* `dmv:importSchemas`: the list of schemas to be imported as support to validation. Default value: ``['common-schema.json','geometry-schema.json']``
* `dmv:warnings`: how to handle FIWARE Data Models checks warnings.
  * ``true (default)`` - print warnings, but does not fail.
  * `ignore` -  do nothing and do not print warnings.
  * `fail` - print warnings, and fails.
* `dmv:warningChecks`: The list of checks that should be executed:
  * `schemaExist`: existence of JSON Schema
  * `docExist`: existence of Documentation
  * `docFolderExist`: existence of Doc folder
  * `exampleExist`: existence of one or more JSON examples
  * `modelNameValid`: adherence of Data Model name to FIWARE Data Models guidelines
  * `readmeExist`: existence of README file
* `dmv:recursiveScan`: enable or disable the recursive scanning of directory. Default value: `true`
* `dmv:validateExamples`: enable or disable the validation of JSON Examples. Default value: `true`
* `dmv:loadModelCommonSchemas`: automatically include any file named ``*-schema.json`` in data path.
* `dmv:ignoreFolders`: The list of folder names that should be ignored. Default value: `['harvest','auxiliary']`
* `dmv:docFolders`: The list of folder names that are expected to contain Documentation: Default value: `['doc']`
* `ajv:missingRefs`: handling of missing referenced schemas. See [ajv](https://github.com/epoberezkin/ajv) for more details. Option values:
  * `true (default)` - if the reference cannot be resolved during compilation the exception is thrown. The thrown error has properties missingRef (with hash fragment) and missingSchema (without it). Both properties are resolved relative to the current base id (usually schema id, unless it was substituted).
  * `ignore` - to log error during compilation and always pass validation.
  * `fail` - to log error and successfully compile schema but fail validation if this rule is checked.
* `ajv:extendRefs`: validation of other keywords when $ref is present in the schema. See [ajv](https://github.com/epoberezkin/ajv) for more details. Option values:
  * `ignore` - when $ref is used other keywords are ignored (as per JSON Reference standard). A warning will be logged during the schema compilation.
  * `fail (default)` - if other validation keywords are used together with $ref the exception will be thrown when the schema is compiled. This option is recommended to make sure schema has no keywords that are ignored, which can be confusing.
  * `true` - validate all keywords in the schemas with $ref (the default behaviour in versions before ajv 5.0.0).
* `ajv:allErrors`: when `true` check all rules collecting all errors, when `false` return after the first error. See [ajv](https://github.com/epoberezkin/ajv) for more details. Default value: `true`

## Compiling the validator
Should you want to change the code of the validator, to install your modified version, you  simple need compile it with the following command:

``npm install -g``
