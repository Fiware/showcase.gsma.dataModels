var fs = require("fs");
    nconf = require('nconf');
    util = require('util');
    request = require('request');
    glob = require('glob');
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
      alias: 'fiware:importSchemas',
      describe: 'Additional schemas that will be included during validation. Default imported schemas are: common-schema.json, geometry-schema.json',
      type: 'array'
    },
    "w" : {
      alias: 'fiware:warnings',
      describe: 'How to handle FIWARE Data Models checks warnings.\n true (default) - print warnings, but does not fail. \n ignore -  do nothing and do not pring warnings.\n fail - print warnings, and fails.',
      type: 'string'
    },
    "p" : {
      alias: 'fiware:path',
      describe: 'The path of FIWARE Data Model(s) to be validated (if recursion enabled, it will be the starting point of recursion)',
      demand: false,
      type: 'string'
    },
    "h" : {
      alias: 'help',
      describe: 'Print the help message',
      demand: false
    }
  },"Usage: nodejs test.js -p DataModel -w ignore -i common-schema.json,geometry-schema.json")
   .env()
   .file('config.json')
   .defaults({
     'fiware:importSchemas': ['common-schema.json','geometry-schema.json'],
     'fiware:warnings': 'true',
     'fiware:warningChecks': ['schemaExist','docExist','docFolderExist','exampleExist','modelNameValid','readmeExist'],
     'fiware:recursiveScan': true,
     'fiware:validateExamples': true,
     'fiware:loadModelCommonSchemas': true,
     'fiware:importExternalSchemaFolders': true,
     'fiware:resolveRemoteSchemas': false,
     'fiware:ignoreFolders': ['harvest','auxiliary'],
     'fiware:docFolders': ['doc'],
     'fiware:externalSchemaFolders' : ['externalSchema'],
     'ajv:missingRefs': 'true',
     'ajv:extendRefs': 'fail',
     'ajv:allErrors': true
  });

/* print help */
if (nconf.get('h')){ 
  nconf.stores.argv.showHelp();
  return;
}

/* Check configuration */
try {
  nconf.required(['fiware:path']);
} catch (err) {
  process.exitCode = -1;
  console.error("\n Invalid Configuration:"+err.message+"\n");
  nconf.stores.argv.showHelp();
  return;
}

/* Check if path is valid */
try {
    // Query the entry
    stats = fs.lstatSync(nconf.get('fiware:path'));

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

var ignoreFolders = nconf.get('fiware:ignoreFolders');
var docFolders = nconf.get('fiware:docFolders');
ignoreFolders = ignoreFolders.concat(['.git','node_modules']);
var warningChecks = nconf.get('fiware:warningChecks');
var externalSchemaFolders = nconf.get('fiware:externalSchemaFolders');
var ignoreWarnings = (nconf.get('fiware:warnings') == 'ignore');
var failWarnings = (nconf.get('fiware:warnings') == 'fail');
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
  fullMessage = modelPath +": "+ message;
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
     if(!nconf.get("fiware:resolveRemoteSchemas")){
         validate = ajv.compile(schema);
            /* istanbul ignore else */
            if (typeof validate == 'function') {
                addValidSchema(fullPath, 'Schema '+ file +' is valid');
            } else {
                addError(fullPath, 'Schema '+ file +' failed to compile to a function');
                if(failErrors) throw new Error(validate.errors);
            }
     } else {
        /* 
           function validateAsync (err, result) {
              if (err) {
                addError(fullPath, 'Schema '+ file +' is invalid: '+err.message);
                if(failErrors) throw new Error(err.message);
              } else {
                addValidSchema(fullPath, 'Schema '+ file +' is valid');
              }
              validate = result;
            };
            ajv.compileAsync(schema, validateAsync);
       */
       throw new Error("asynch compile is not implemented, don't use yet fiware:resolveRemoteSchemas option");
       console.error("**** asynch compile is not implemented, don't use yet the fiware:resolveRemoteSchemas option ****");  
     }
   } catch (err) {
     addError(fullPath, 'Schema '+ file +' is invalid, if one or more schemas cannot be retrieved, try using remote validation (fiware:resolveRemoteSchemas=true), check if "fiware:loadModelCommonSchemas" is enabled (if missing schemas are FIWARE common schemas) or store third party schemas in the "externalSchema" folder: '+err.message);
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
       data = openFile(fileName, 'example ' + fileName);
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
var commonSchemas = nconf.get("fiware:importSchemas");

var dive = function (basePath,schemas) {

  var relativePath = path.relative(".",basePath);

  var files = fs.readdirSync(basePath);
   
  var localCommonSchemas=Array.from(schemas);

  if (nconf.get("fiware:loadModelCommonSchemas")) 
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
           if (nconf.get("fiware:recursiveScan")) dive(fullPath,localCommonSchemas);
         
           if (relativePath != "" && docFolders.includes(path.basename(fullPath)) && !ignoreWarnings){
              if (warningChecks.includes("docExist")) docExist(fullPath);
           }         
           //schema compilation and example validation
           var validate;
           if (relativePath != "" && fileExists(fullPath,"schema.json")) {
             validate = compileSchema(fullPath,"schema.json",localCommonSchemas);
           }
           if (relativePath != "" && fileExists(fullPath,"example*.json") && nconf.get('fiware:validateExamples')) {
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
dive(nconf.get('fiware:path'),commonSchemas);
console.log("*** ValidSchemas ***: "+JSON.stringify(validSchemas,null, '\t'));
console.log("*** ValidExamples ***: "+JSON.stringify(validExamples,null, '\t'));
console.log("*** Warnings ***: "+JSON.stringify(warnings,null, '\t'));
console.log("*** Errors ***: "+JSON.stringify(errors,null, '\t'));
