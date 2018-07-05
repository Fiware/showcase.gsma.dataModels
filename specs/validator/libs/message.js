/* handle warning and error messages */

'use strict';

var path = require('path');

var warnings = {};
var errors = {};
var validSchemas = {};
var validExamples = {};
var supportedExamples = {};

var addMessageToMap = function(modelPath, message, map) {
  var rootModel = getRootModelName(modelPath);
  var fullMessage = modelPath + ': ' + message;
  if (map[rootModel] != null)
  map[rootModel].push(fullMessage);
  else
  map[rootModel] = [fullMessage];
  return true;
};

//given a path, retrieve the name of the root model
var getRootModelName = function(fullPath) {
  var index = fullPath.indexOf(path.sep);
  if (index > 0) return fullPath.substring(0, index);
  else return fullPath;
};

module.exports = {
  warnings: warnings,
  errors: errors,
  validSchemas: validSchemas,
  validExamples: validExamples,
  supportedExamples: supportedExamples,

  //add warning to the warnings map for a given model
  addWarning: function(modelPath, message) {
    return addMessageToMap(modelPath, message, warnings);
  },

  //add error to the errors map for a given model
  addError: function(modelPath, message) {
    return addMessageToMap(modelPath, message, errors);
  },

  //add valid schema to the valid schemas map for a given model
  addValidSchema: function(modelPath, message) {
    return addMessageToMap(modelPath, message, validSchemas);
  },

  //add valid example to the valid examples map for a given model
  addValidExample: function(modelPath, message) {
    return addMessageToMap(modelPath, message, validExamples);
  },
  //add valid example to the valid examples map for a given model
  addSupportedExample: function(modelPath, message) {
    return addMessageToMap(modelPath, message, supportedExamples);
  }
};
