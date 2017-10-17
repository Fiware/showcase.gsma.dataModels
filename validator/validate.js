#!/usr/bin/env node
"use strict";

var fs = require("fs");
var nconf = require('nconf');
var util = require('util');
var request = require('request');
var glob = require('glob');
var Ajv  = require('ajv');

const path = require('path');

//
// Setup nconf to use (in-order):
//   1. Command-line arguments
//   2. Environment variables
//   3. 'config.json' file
//   4. defaults
nconf.argv({
  "i": {
    alias: 'dmv:importSchemas',
    describe: 'Additional schemas that will be included during validation. Default imported schemas are: common-schema.json, geometry-schema.json',
    type: 'array'
  },
  "w" : {
    alias: 'dmv:warnings',
    describe: 'How to handle FIWARE Data Models checks warnings.\n true (default) - print warnings, but does not fail. \n ignore -  do nothing and do not print warnings.\n fail - print warnings, and fails.',
    type: 'string'
  },
  "p" : {
    alias: 'dmv:path',
    describe: 'The path of FIWARE Data Model(s) to be validated (if recursion enabled, it will be the starting point of recursion)',
    demand: false,
    type: 'string'
  },
  "h" : {
    alias: 'help',
    describe: 'Print the help message',
    demand: false
  }
},"Usage: validate -p DataModel -w ignore -i [common-schema.json,geometry-schema.json]").file('config.json');

if (nconf.get('dmv:importSchemas') == null) {
  nconf.set('dmv:importSchemas', ['common-schema.json','geometry-schema.json']);
}
if (nconf.get('dmv:warnings') == null) {
  nconf.set('dmv:warnings', 'true');
}
if (nconf.get('dmv:warningChecks') == null) {
  nconf.set('dmv:warningChecks', ['schemaExist','docExist','docFolderExist','exampleExist','modelNameValid','readmeExist']);
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
  nconf.set('dmv:ignoreFolders', ['harvest','auxiliary']);
}
if (nconf.get('dmv:docFolders') == null) {
  nconf.set('dmv:docFolders', ['doc']);
}
if (nconf.get('dmv:externalSchemaFolders') == null) {
  nconf.set('dmv:externalSchemaFolders', ['externalSchema']);
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

/* print help */
if (nconf.get('h')){
  nconf.stores.argv.showHelp();
  return;
}

/* Check configuration */
try {
  nconf.required(['dmv:path']);
} catch (err) {
  process.exitCode = -1;
  console.error("\n Invalid Configuration:"+err.message+"\n");
  nconf.stores.argv.showHelp();
  return;
}

/* Check if path is valid */
try {
  // Query the entry
  var stats = fs.lstatSync(nconf.get('dmv:path'));

  // Is it a directory?
  if (!stats.isDirectory()) {
    throw new Error("The path passed must be a directory");
  }
}
catch (err) {
  process.exitCode = -1;
  console.error("\n Invalid Path: "+err.message+"\n");
  return;
}

/* load configuration */
var warnings = {};
var errors = {};
var validSchemas = {};
var validExamples = {};

var ignoreFolders = nconf.get('dmv:ignoreFolders');
var docFolders = nconf.get('dmv:docFolders');
ignoreFolders = ignoreFolders.concat(['.git','node_modules','validator']);
var warningChecks = nconf.get('dmv:warningChecks');
var externalSchemaFolders = nconf.get('dmv:externalSchemaFolders');
var ignoreWarnings = (nconf.get('dmv:warnings') == 'ignore');
var failWarnings = (nconf.get('dmv:warnings') == 'fail');
var failErrors = !nconf.get('ajv:allErrors');

//load a remote schema
function loadSchema(uri,callback) {
  request(uri,call);

  var call = function(err, res, body) {
    if (err || res.statusCode >= 400)
      callback(err || new Error('Loading error: ' + res.statusCode));
    else {
      callback(null,JSON.parse(body));
    }
  }

};

var ajvOptions = {
  // validation and reporting options:
  allErrors:        nconf.get('ajv:allErrors'),
  schemas:          {},
  // referenced schema options:
  missingRefs:      nconf.get('ajv:missingRefs'),
  extendRefs:       nconf.get('ajv:extendRefs'), // recommended 'fail'
  loadSchema:       loadSchema, // function(uri: string): Promise {}
};


//load additional schemas from filepath
var addSchemas = function(fileList, method, fileType) {
  if (!fileList) return;
  var files = getFiles(fileList);
  files.forEach(function (file) {
    var schema = openFile(file, fileType);
    method(schema);
  });
};

//load  a list of files, supports patterns, e.g. *-schema.json
function getFiles(args) {
  var files = [];
  if (Array.isArray(args)) args.forEach(_getFiles);
  else _getFiles(args);
  return files;

  function _getFiles(fileOrPattern) {
    if (glob.hasMagic(fileOrPattern)) {
      var dataFiles = glob.sync(fileOrPattern, { cwd: process.cwd() });
      files = files.concat(dataFiles);
    } else {
      files.push(fileOrPattern);
    }
  }
};

//load a JSON File
var openFile = function (filename, suffix){
  var json = null;
  var file = path.resolve(process.cwd(), filename);
  try {
    try {
      json = JSON.parse(fs.readFileSync(file).toString());
    } catch(JSONerr) {
      json = require(file);
    }
  } catch(err) {
    console.error('error:  ' + err.message.replace(' module', ' ' + suffix));
    process.exit(2);
  }
  return json;
};

//check if a documentation file exists in a given path
var docExist = function (fullPath){
  if (!fileExists(fullPath, "spec.md") && !fileExists(fullPath, "introduction.md"))
  if (addWarning(fullPath, "does not include a documentation file name spec.md or introduction.md") && failWarnings)
    throw new Error("Fail on Warnings: " +JSON.stringify(warnings,null, '\t'));
};

//check if a documentation folder exists in a given path
var docFolderExist = function (fullPath) {
  var counter = 0;
  docFolders.forEach(function(value){
    try {
      fs.lstatSync(path.join(fullPath, value)).isDirectory();
      counter++;
    } catch (err) {

    }
  });

  if (counter == 0) addWarning(fullPath, "does not include a documentation folder");
  if (warningChecks.includes("docExist") && counter == 0)
  if (addWarning(fullPath, "does not include a documentation file name spec.md or introduction.md") && failWarnings)
    throw new Error("Fail on Warnings: " +JSON.stringify(warnings,null, '\t'));
};

//check if a folder name is valid for a data model
var modelNameValid = function (fullPath) {
  if (fullPath.charAt(0) != fullPath.charAt(0).toUpperCase())
  if (addWarning(fullPath, "Model folder names should start in capital letter") && failWarnings)
    throw new Error("Fail on Warnings: " +JSON.stringify(warnings,null, '\t'));
};

//add message to map
var addMessageToMap = function (modelPath, message, map) {
  var rootModel = getRootModelName(modelPath);
  var fullMessage = modelPath +": "+ message;
  if (map[rootModel]!=null)
    map[rootModel].push(fullMessage);
  else
    map[rootModel]=[fullMessage];
  return true;
};

//add warning to the warnings map for a given model
var addWarning = function (modelPath, message) {
  return addMessageToMap(modelPath, message,warnings);
};

//add error to the errors map for a given model
var addError = function (modelPath, message) {
  return addMessageToMap(modelPath, message,errors);
};

//add valid schema to the valid schemas map for a given model
var addValidSchema = function (modelPath, message) {
  return addMessageToMap(modelPath, message,validSchemas);
};

//add valid example to the valid examples map for a given model
var addValidExample = function (modelPath, message) {
  return addMessageToMap(modelPath, message,validExamples);
};

//given a path, retrieve the name of the root model
var getRootModelName = function (fullPath) {
  var index = fullPath.indexOf(path.sep);
  if (index>0) return fullPath.substring(0,index);
  else return fullPath;
};

//if a path contains folders beyond the doc and ignore ones, returns true, otherwise false
var containsModelFolders = function (basePath) {
  var files = fs.readdirSync(basePath);
  var folderCounter=0;
  files.forEach(function(fileName){
    try {
      var fullPath = path.join(basePath, fileName);
      var stat=fs.lstatSync(fullPath);
      if (stat && stat.isDirectory() && !ignoreFolders.includes(path.basename(fullPath)) && !docFolders.includes(path.basename(fullPath)) && !externalSchemaFolders.includes(path.basename(fullPath)))
        folderCounter++;
    } catch (err) {
      console.log("***ERROR*** "+err );
      if(failErrors) throw new Error(err);
    }
  });
  if(folderCounter) return true;
  else return false;
};

//check if a folder includes a README.md file
var readmeExist = function(fullPath){
  if (!fileExists(fullPath,"README.md"))
  if (addWarning(fullPath, "does not include a Readme file README.md") && failWarnings)
    throw new Error("Fail on Warnings: " +JSON.stringify(warnings,null, '\t'));
};

//check if a folder includes a schema file
var schemaExist = function(fullPath){
  if (!containsModelFolders(fullPath) && !fileExists(fullPath,"schema.json"))
  if (addWarning(fullPath, "does not include a JSON Schema file schema.json") && failWarnings)
    throw new Error("Fail on Warnings: " +JSON.stringify(warnings,null, '\t'));
};

//check if a folder includes one or more example files
var exampleExist = function (fullPath){
  if (!containsModelFolders(fullPath) && !fileExists(fullPath,"example*.json"))
  if (addWarning(fullPath, "does not include a JSON Example file example*.json") && failWarnings)
    throw new Error("Fail on Warnings: " +JSON.stringify(warnings,null, '\t'));
};

//if a file matching a given regular expression exists in a given path returns true, otherwise false
var fileExists = function (basePath,regex) {
  var files = fs.readdirSync(basePath);
  var counter=0;
  var regexp = new RegExp(regex);
  files.forEach( function(item) {
    if(regexp.test(item)){
      counter++;
    }
  });
  if (counter>0) return true;
  else return false;
};

var docValid = function(fullpath){
  console.log("*** docValid: not implemented ***");
};

var docValidLinks = function(fullpath){
  console.log("*** docValidLinks: not implemented ***");
};

var idMatching = function(fullpath){
  console.log("*** idMatching: not implemented ***");
};

var compileSchema = function(fullPath,fileSchema,commonSchemas){
  var file = path.join(fullPath, fileSchema);
  var schema = openFile(file, 'schema');
  var ajv = new Ajv(ajvOptions);
  addSchemas(commonSchemas, ajv.addSchema, 'schema');
  var validate;
  try {
    if(!nconf.get("dmv:resolveRemoteSchemas")){
      validate = ajv.compile(schema);
      /* istanbul ignore else */
      if (typeof validate == 'function') {
        addValidSchema(fullPath, 'Schema '+ file +' is valid');
      } else {
        addError(fullPath, 'Schema '+ file +' failed to compile to a function');
        if(failErrors) throw new Error(validate.errors);
      }
    } else {
      throw new Error("asynch compile is not implemented, don't use yet dmv:resolveRemoteSchemas option");
      console.error("**** asynch compile is not implemented, don't use yet the dmv:resolveRemoteSchemas option ****");
    }
  } catch (err) {
    addError(fullPath, 'Schema '+ file +' is invalid, if one or more schemas cannot be retrieved, try using remote validation (dmv:resolveRemoteSchemas=true), check if "dmv:loadModelCommonSchemas" is enabled (if missing schemas are FIWARE common schemas) or store third party schemas in the "externalSchema" folder: '+err.message);
    if(failErrors) throw new Error(err.message);
  }
  return validate;
};

// load schemas local to FIWARE Data Model (that should be named using *-schema.json pattern
var loadLocalSchemas = function (fullPath) {
  var files;
  if (fullPath != ".")
    files = getFiles(fullPath + path.sep + "*-schema.json");
  else
    files = getFiles("*-schema.json");
  return files;
};

var validateExamples = function (fullPath,validate) {
  var files = getFiles(fullPath + path.sep + "example*.json");
  if (typeof validate != 'function')
  if (addError(fullPath, 'Examples cannot be validated since validation function cannot be computed. Probably not all schemas can be resolved correctly (check schema errors)') && failErrors) throw new Error("Fail on Error:" + JSON.stringify(errors,null, '\t'));

  try{
    files.forEach(function(fileName){
      var data = openFile(fileName, 'example ' + fileName);
      if (typeof validate != 'function') {
        addError(fullPath, 'Example '+ fileName +' is invalid: '+JSON.stringify(validate.errors,null));
        if(failErrors) throw new Error("Fail on Error:" + JSON.stringify(errors,null, '\t'));
      }
      if (validate(data))
      addValidExample(fullPath,fileName +" is valid");
      else {
        addError(fullPath, 'Example '+ fileName +' is invalid: '+JSON.stringify(validate.errors,null));
        if(failErrors) throw new Error("Fail on Error:" + JSON.stringify(errors,null, '\t'));
      }
    });
  } catch (err) {
    if(failErrors) throw new Error("Fail on Error:" + JSON.stringify(errors,null, '\t'));
  }
}

var addUniqueToArray = function (array1, array2){
  var result =  Array.from(array1);
  array2.forEach(function(item2){
    if (!array1.includes(item2))
    result.push(item2);
  });
  return result;
}


// Path Scan function
var commonSchemas = nconf.get("dmv:importSchemas");

var dive = function (basePath,schemas) {

  var relativePath = path.relative(".",basePath);

  var files = fs.readdirSync(basePath);

  var localCommonSchemas=Array.from(schemas);

  if (nconf.get("dmv:loadModelCommonSchemas"))
  localCommonSchemas=addUniqueToArray(localCommonSchemas,loadLocalSchemas(basePath));

  files.forEach(function(fileName){
    try {
      var fullPath;
      if (basePath != ".") fullPath = basePath + path.sep + fileName;
      else fullPath = fileName;
      var stat=fs.lstatSync(fullPath);

      if (stat && stat.isDirectory()) {
        // Dive into the directory
        if (!ignoreFolders.includes(path.basename(fullPath)) && !docFolders.includes(path.basename(fullPath)) && !externalSchemaFolders.includes(path.basename(fullPath))){
          if (warningChecks.includes("modelNameValid") && !ignoreWarnings) modelNameValid(fullPath);
          if (warningChecks.includes("docFolderExist") && !ignoreWarnings) docFolderExist(fullPath);
          if (warningChecks.includes("schemaExist") && !ignoreWarnings) schemaExist(fullPath);
          if (warningChecks.includes("exampleExist") && !ignoreWarnings) exampleExist(fullPath);
          if (warningChecks.includes("readmeExist") && !ignoreWarnings) readmeExist(fullPath);
          if (warningChecks.includes("docValidLinks") && !ignoreWarnings) docValidLinks(fullPath);
          if (warningChecks.includes("docValidLinks") && !ignoreWarnings) docValid(fullPath);
          if (warningChecks.includes("idMatching") && !ignoreWarnings) idMatching(fullPath);

          //dive in again if recursion is enabled
          if (nconf.get("dmv:recursiveScan")) dive(fullPath,localCommonSchemas);

          if (relativePath != "" && docFolders.includes(path.basename(fullPath)) && !ignoreWarnings){
            if (warningChecks.includes("docExist")) docExist(fullPath);
          }
          //schema compilation and example validation
          var validate;
          if (relativePath != "" && fileExists(fullPath,"schema.json")) {
            validate = compileSchema(fullPath,"schema.json",localCommonSchemas);
          }
          if (relativePath != "" && fileExists(fullPath,"example*.json") && nconf.get('dmv:validateExamples')) {
            validateExamples(fullPath,validate);
          }
        }
      }
    } catch (err) {
      console.log(err);
      if(failErrors) throw new Error(err.message);
    }
  });
};

console.log("*** Active Warnings ***:" +warningChecks);
dive(nconf.get('dmv:path'),commonSchemas);
console.log("*** ValidSchemas ***: "+JSON.stringify(validSchemas,null, '\t'));
console.log("*** ValidExamples ***: "+JSON.stringify(validExamples,null, '\t'));
console.log("*** Warnings ***: "+JSON.stringify(warnings,null, '\t'));
console.log("*** Errors ***: "+JSON.stringify(errors,null, '\t'));
if (Object.keys(errors).length != 0) throw new Error(JSON.stringify(errors,null, '\t'));
