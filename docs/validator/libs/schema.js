/* utilities to manage schemas and json */

'use strict';

var glob = require('glob');
var Ajv = require('ajv');
var path = require('path');
var fs = require('fs');
var request = require('request');
var msg = require('./message.js');
var conf = require('./conf.js');
const debug = require('debug')('schema');

var addSchemas = function(fileList, method, fileType) {
  if (!fileList) return;
  var files = getFiles(fileList);
  files.forEach(function(file) {
    var schema = openFile(file, fileType);
    method(schema);
  });
};

//load  a list of files, supports regex
var getFiles = function(args) {
    var files = [];
    if (Array.isArray(args)) args.forEach(_getFiles);
    else _getFiles(args);
    debug("*getFiles* - " +args+ " :" +files);
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
var openFile = function(filename, suffix) {
    var json = null;
    var file = path.resolve(process.cwd(), filename);
    try {
      try {
        json = JSON.parse(fs.readFileSync(file).toString());
        debug("*openFile* - JSON" +file+ " :" +json);
      } catch (JSONerr) {
        json = require(file);
        debug("*openFile* - JSONerr " +file+ " :" +json);
      }
    } catch (err) {
      console.error('error:  ' + err.message.replace(' module', ' ' + suffix));
      process.exit(2);
    }
    return json;
  };

module.exports = {

  //compile schema without remote resolve
  compileSchema: function(fullPath, fileSchema, commonSchemas) {
    var file = path.join(fullPath, fileSchema);
    var schema = openFile(file, 'schema');
    var ajv = new Ajv(conf.ajvOptions);
    addSchemas(commonSchemas, ajv.addSchema, 'schema');
    var validate;
    try {
        validate = ajv.compile(schema);
        /* istanbul ignore else */
        if (typeof validate == 'function') {
          debug("*compileSchema* - valid schema " +file+ " :" +validate);
          msg.addValidSchema(fullPath, 'Schema ' + file + ' is valid');
        } else {
          debug("*compileSchema* - invalid schema " +file+ " :" +validate);
          msg.addError(fullPath, 'Schema ' + file +
            ' failed to compile to a function');
          if (conf.failErrors) throw new Error(validate.errors);
        }
    } catch (err) {
      msg.addError(fullPath, 'Schema ' + file + ' is invalid, ' +
        'if one or more schemas cannot be retrieved, ' +
        'try using remote validation (dmv:resolveRemoteSchemas=true), ' +
        'check if \"dmv:loadModelCommonSchemas\" is enabled ' +
        ' (if missing schemas are FIWARE common schemas) ' +
        'or store third party schemas in the \"externalSchema\" folder: ' +
        err.message);
      if (conf.failErrors) throw new Error(err.message);
    }
    return validate;
  },

  //validate examples agains a compiled schema
  validateExamples: function(fullPath, validate) {
    var files = getFiles(fullPath + path.sep + 'example*.json');
    if (typeof validate != 'function')
    if (msg.addError(fullPath, 'Examples cannot be validated since ' +
         'validation function cannot be computed. Probably not all schemas ' +
         'can be resolved correctly (check schema errors)') && conf.failErrors)
      throw new Error('Fail on Error:' +
        JSON.stringify(msg.errors, null, '\t'));

    try {
      files.forEach(function(fileName) {
        var data = openFile(fileName, 'example ' + fileName);
        if (typeof validate != 'function') {
         debug("*validateExamples* - " + fileName +
           " cannot be validated");
         msg.addError(fullPath, 'Example ' + fileName +
            ' cannot be validated: ' +
            JSON.stringify(validate.errors, null));
          if (conf.failErrors)
            throw new Error('Fail on Error:' +
              JSON.stringify(msg.errors, null, '\t'));
        }
        var validExample = validate(data);
        debug("*validateExamples* - " +fileName+ " validity : " +validExample);
        if (validExample)
          msg.addValidExample(fullPath, fileName + ' is valid');
        else {
          msg.addError(fullPath, 'Example ' + fileName + ' is invalid: ' +
            JSON.stringify(validate.errors, null));
          if (conf.failErrors) throw new Error('Fail on Error:' +
            JSON.stringify(msg.errors, null, '\t'));
        }
      });
    } catch (err) {
      if (conf.failErrors)
        throw new Error('Fail on Error:' +
          JSON.stringify(msg.errors, null, '\t'));
    }
  },

  addUniqueToArray: function(array1, array2) {
    var result = Array.from(array1);
    array2.forEach(function(item2) {
      if (!array1.includes(item2) &&
          !array1.includes(path.basename(item2)))
        result.push(item2);
    });
    return result;
  },

  //load a remote schema
  loadSchema: function loadSchema(uri, callback) {
    request(uri, call);
    debug("*loadSchema* - uri: " + uri);
    var call = function(err, res, body) {
      if (err || res.statusCode >= 400)
      callback(err || new Error('Loading error: ' + res.statusCode));
      else {
        debug("*loadSchema* - body: " + body);
        callback(null, JSON.parse(body));
      }
    };

  },

  addSchemas: addSchemas,
  getFiles: getFiles,
  openFile: openFile,

  // load schemas local to FIWARE Data Model
  // (that should be named using *-schema.json pattern)
  loadLocalSchemas: function(fullPath) {
    var files;
    if (fullPath != '.')
      files = getFiles(fullPath + path.sep + '*-schema.json');
    else
      files = getFiles('*-schema.json');
    debug("*loadLocalSchemas* - files: " + files);
    return files;
  }
};
