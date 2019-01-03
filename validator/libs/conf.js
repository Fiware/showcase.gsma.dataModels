/* provide functions to support the  the data model validator */

const nconf = require('nconf');
const fs = require('fs');
const schema = require('./schema.js');
const pjson = require('../package.json');

let ignoreWarnings = false;
let failWarnings = false;
let failErrors = true;
let ajvOptions = {};

module.exports = {
  /* export variables */
  nconf,
  ignoreWarnings,
  failWarnings,
  failErrors,
  ajvOptions,

  /* load configuration from arg and config.json file (if any)*/
  load() {
    nconf
      .argv(
        {
          i: {
            alias: 'dmv:importSchemas',
            describe:
              'Additional schemas that will be included' +
              ' during validation. Default imported schemas are: ' +
              ' common-schema.json, geometry-schema.json',
            type: 'array',
          },
          iF: {
            alias: 'dmv:ignoreFolders',
            describe:
              "The list of folder names that should be ignored. Default value: ['harvest','auxiliary','img']",
            type: 'array',
          },
          w: {
            alias: 'dmv:warnings',
            describe:
              'How to handle FIWARE Data Models checks warnings.\n' +
              'true (default) - print warnings, but does not fail. \n' +
              'ignore -  do nothing and do not print warnings.\n' +
              ' fail - print warnings, and fails.',
            type: 'string',
          },
          p: {
            alias: 'dmv:path',
            describe:
              'The path of FIWARE Data Model(s) to be validated ' +
              '(if recursion enabled, it will be the starting point of recursion)',
            demand: false,
            type: 'string',
          },
          c: {
            alias: 'dmv:contextBroker',
            describe: 'Enable JSON example testing with Orion Context Broker',
            type: 'boolean',
            demand: false,
          },
          u: {
            alias: 'dmv:contextBrokerUrl',
            describe: 'Orion Context Broker Url for example testing',
            type: 'string',
            demand: false,
          },
          v: {
            alias: 'version',
            describe: 'Print the current version',
            demand: false,
          },
          h: {
            alias: 'help',
            describe: 'Print the help message',
            demand: false,
          },
        },
        'Usage: validate -p DataModel -w ignore ' +
          '-i [common-schema.json,geometry-schema.json]' +
          '-iF [harvest,auxiliary,img]'
      )
      .file('config.json');
  },

  /* load default values
  TODO: fix issues with nconf.default */
  defaults() {
    if (nconf.get('dmv:importSchemas') == null) {
      nconf.set('dmv:importSchemas', [
        'common-schema.json',
        'geometry-schema.json',
      ]);
    }
    if (nconf.get('dmv:warnings') == null) {
      nconf.set('dmv:warnings', 'true');
    }
    if (nconf.get('dmv:warningChecks') == null) {
      nconf.set('dmv:warningChecks', [
        'schemaExist',
        'docExist',
        'docFolderExist',
        'exampleExist',
        'modelNameValid',
        'readmeExist',
      ]);
    }
    if (nconf.get('dmv:recursiveScan') == null) {
      nconf.set('dmv:recursiveScan', true);
    }
    if (nconf.get('dmv:validateExamples') == null) {
      nconf.set('dmv:validateExamples', true);
    }
    if (nconf.get('dmv:loadModelCommonSchemas') == null) {
      nconf.set('dmv:loadModelCommonSchemas', true);
    }
    if (nconf.get('dmv:importExternalSchemaFolders') == null) {
      nconf.set('dmv:importExternalSchemaFolders', true);
    }
    if (nconf.get('dmv:resolveRemoteSchemas') == null) {
      nconf.set('dmv:resolveRemoteSchemas', false);
    }
    if (nconf.get('dmv:ignoreFolders') == null) {
      nconf.set('dmv:ignoreFolders', ['harvest', 'auxiliary', 'img']);
    }
    if (nconf.get('dmv:docFolders') == null) {
      nconf.set('dmv:docFolders', ['doc']);
    }
    if (nconf.get('dmv:externalSchemaFolders') == null) {
      nconf.set('dmv:externalSchemaFolders', ['externalSchema']);
    }
    if (nconf.get('dmv:contextBroker') == null) {
      nconf.set('dmv:contextBroker', false);
    }
    if (nconf.get('dmv:contextBrokerUrl') == null) {
      nconf.set('dmv:contextBrokerUrl', 'http://localhost:1026/v2');
    }
    if (nconf.get('ajv:missingRefs') == null) {
      nconf.set('ajv:missingRefs', 'true');
    }
    if (nconf.get('ajv:extendRefs') == null) {
      nconf.set('ajv:extendRefs', 'fail');
    }
    if (nconf.get('ajv:allErrors') == null) {
      nconf.set('ajv:allErrors', true);
    }
    nconf.set(
      'dmv:ignoreFolders',
      nconf
        .get('dmv:ignoreFolders')
        .concat(['.git', 'node_modules', 'validator'])
    );

    /* error and warnings management configuration */
    ignoreWarnings = nconf.get('dmv:warnings') === 'ignore';
    failWarnings = nconf.get('dmv:warnings') === 'fail';
    failErrors = !nconf.get('ajv:allErrors');
    /* set ajv options */
    ajvOptions = {
      // validation and reporting options:
      allErrors: nconf.get('ajv:allErrors'),
      schemas: {},
      // referenced schema options:
      missingRefs: nconf.get('ajv:missingRefs'),
      extendRefs: nconf.get('ajv:extendRefs'),
      loadSchema: schema.loadSchema,
    };
    return true;
  },

  help() {
    if (nconf.get('h')) {
      nconf.stores.argv.showHelp();
      return true;
    }
    return false;
  },

  showHelp() {
    nconf.stores.argv.showHelp();
  },

  version() {
    if (nconf.get('v')) {
      // eslint-disable-next-line no-console
      console.log('data model validator version: ' + pjson.version);
      return true;
    }
    return false;
  },
  /* Check configuration validity */
  validate() {
    nconf.required(['dmv:path']);
    return true;
  },

  /* Check path validity */
  validatePath() {
    const stats = fs.lstatSync(nconf.get('dmv:path'));
    // Is it a directory?
    if (!stats.isDirectory()) {
      throw new Error('The path passed must be a directory');
    }
    return true;
  },
};
