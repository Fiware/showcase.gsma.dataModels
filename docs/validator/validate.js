#!/usr/bin/env node
'use strict';
var fs = require('fs');
var path = require('path');
var conf = require('./libs/conf.js');
var msg = require('./libs/message.js');
var schema = require('./libs/schema.js');
var checks = require('./libs/checks.js');

const debug = require('debug')('validate');

/* load conf from command line and/or config.js */
conf.load();
/* load default values if not provided: as bug fix to nconf bug */
conf.defaults();
/* print help if -h option and exit */
if (conf.help())
  return;
/* print version if -v option and exit */
if (conf.version())
  return;
/* validate command line input */
try {
  conf.validate();
  conf.validatePath();
} catch (err) {
  process.exitCode = -1;
  console.error('\n Invalid Configuration:' + err.message + '\n');
  conf.showHelp();
  return;
}

// Path Scan function

var dive = function(basePath, schemas) {

  debug('*dive* basePath: '+basePath);
  debug('*dive* processPath: '+process.cwd());

  var localCommonSchemas = Array.from(schemas);

  debug('*dive* localSchema: ' + localCommonSchemas);

  debug('*dive* root path: ' + (path.basename(basePath) == 'dataModels'));

  debug('*dive* basename: ' + path.basename(basePath));

  var fullPath = basePath;

  debug('*dive* fullPath: ' + fullPath);

  //Is it a Data Model directory?
  if (!conf.nconf.get('dmv:ignoreFolders')
        .includes(path.basename(fullPath)) &&
      !conf.nconf.get('dmv:docFolders')
        .includes(path.basename(fullPath)) &&
      !conf.nconf.get('dmv:externalSchemaFolders')
        .includes(path.basename(fullPath))) {

    //let's run the configured checkers
    debug('*dive* running checkers');

    //is the modelNameValid?
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('modelNameValid') &&
        !conf.ignoreWarnings)
      checks.modelNameValid(fullPath);

    //does the data model include a documentation folder?
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('docFolderExist') &&
        !conf.ignoreWarnings)
      checks.docFolderExist(fullPath);

    //is there a JSON Schema file?
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('schemaExist') &&
        !conf.ignoreWarnings)
      checks.schemaExist(fullPath);

    //is there one or more JSON Example
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('exampleExist') &&
        !conf.ignoreWarnings)
      checks.exampleExist(fullPath);

    //is there a readme file?
    if (conf.nconf.get('dmv:warningChecks').includes('readmeExist') &&
        !conf.ignoreWarnings)
      checks.readmeExist(fullPath);

    //are links in the documentation valid? TODO
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('docValidLinks') &&
        !conf.ignoreWarnings)
      checks.docValidLinks(fullPath);

    //is the documentation valid? TODO
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('docValid') &&
        !conf.ignoreWarnings)
      checks.docValid(fullPath);

    //is the schema id matching the name of the folder? TODO
    if (path.basename(basePath) != 'dataModels' &&
        conf.nconf.get('dmv:warningChecks').includes('idMatching') &&
        !conf.ignoreWarnings)
      checks.idMatching(fullPath);

    //does it exists the documentation of the data model?
    if (path.basename(basePath) != 'dataModels' &&
        !conf.ignoreWarnings &&
        conf.nconf.get('dmv:warningChecks').includes('docExist'))
      checks.docExist(fullPath);

    try {
      //schema compilation and example validation
      var validate;

      if (conf.nconf.get('dmv:loadModelCommonSchemas') &&
          checks.fileExists(fullPath, '.+-schema\.json')) {

        var schemaFiles = schema.getFiles(fullPath + path.sep + '*-schema.json');
        debug('*dive* validate common schemas :' + files);
        if (!conf.nconf.get('dmv:resolveRemoteSchemas')){
          schemaFiles.forEach(function(fileName) {
            debug('*dive* validate common schema :' + path.basename(fileName));
            schema.compileSchema(
              fullPath,
              path.basename(fileName),
              localCommonSchemas
            );
          });
        } else {
          console.error('**** asynch compile is not implemented, ' +
            "don't use yet the dmv:resolveRemoteSchemas option ****");
          throw new Error('asynch compile is not implemented,  ' +
            "don't use yet dmv:resolveRemoteSchemas option");
        }
      }

      debug('*dive* load common schemas :' +
        conf.nconf.get('dmv:loadModelCommonSchemas'));

      if (conf.nconf.get('dmv:loadModelCommonSchemas'))
        localCommonSchemas =
          schema.addUniqueToArray(
            localCommonSchemas,
            schema.loadLocalSchemas(basePath)
        );


      if (path.basename(basePath) != 'dataModels' &&
          checks.fileExists(fullPath, '^schema\\.json')) {
        debug('*dive* run schema validation');
        if (!conf.nconf.get('dmv:resolveRemoteSchemas')) {
          validate =
            schema.compileSchema(
              fullPath,
              'schema.json',
              localCommonSchemas
            );
        } else {
          console.error('**** asynch compile is not implemented, ' +
            "don't use yet the dmv:resolveRemoteSchemas option ****");
          throw new Error('asynch compile is not implemented,  ' +
            "don't use yet dmv:resolveRemoteSchemas option");
        }
      }

      if (path.basename(basePath) != 'dataModels' &&
          checks.fileExists(fullPath, '^example(-\\d+)?\\.json') &&
          conf.nconf.get('dmv:validateExamples')) {
        debug('*dive* run example validation');
        schema.validateExamples(fullPath, validate);
      }

      if (path.basename(basePath) != 'dataModels' &&
          checks.fileExists(fullPath, '^example(-\\d+)?\\.json') &&
          conf.nconf.get('dmv:contextBroker')) {
        debug('*dive* check example support');
        checks.exampleSupported(fullPath);
      }

      //dive in again if recursion is enabled
      var files = fs.readdirSync(basePath);

      if (conf.nconf.get('dmv:recursiveScan'))
        files.forEach(function(fileName) {
          debug('*dive* recursion on ' + fileName);
          try {
            var fullPath = basePath + path.sep + fileName;
            var stat = fs.lstatSync(fullPath);

            //it's a directory -> run the validator inside
            if (stat && stat.isDirectory())
              dive(fullPath, localCommonSchemas);

          } catch (err) {
            console.log(err);
            if (conf.failErrors) throw new Error(err.message);
          }
        });
    } catch (err) {
      console.log(err);
      if (conf.failErrors) throw new Error(err.message);
    }
  }
};

console.log('*** Active Warnings ***:' + conf.nconf.get('dmv:warningChecks'));

var scanningPath = path.resolve(process.cwd(),conf.nconf.get('dmv:path'));

console.log('scan: ' + scanningPath);

/* absolute schema path */
var schemas = [];

conf.nconf.get('dmv:importSchemas').forEach(function(schema) {
  var schemaFullPath = path.resolve(process.cwd(),schema);
  schemas.push(schemaFullPath);
});

debug('full path common schemas :' + schemas);

dive(scanningPath, schemas);

console.log('*** ValidSchemas ***: ' +
  JSON.stringify(msg.validSchemas, null, '\t'));
console.log('*** ValidExamples ***: ' +
  JSON.stringify(msg.validExamples, null, '\t'));
console.log('*** SupportedExamples ***: ' +
  JSON.stringify(msg.supportedExamples, null, '\t'));
console.log('*** Warnings ***: ' +
  JSON.stringify(msg.warnings, null, '\t'));
console.log('*** Errors ***: ' +
  JSON.stringify(msg.errors, null, '\t'));

if (Object.keys(msg.errors).length != 0)
  throw new Error(JSON.stringify(msg.errors, null, '\t'));
