/* Data Model Validation checkers for structure */

/* eslint no-console: "off" */

const fs = require('fs');
const path = require('path');
const deasync = require('deasync');
const msg = require('./message.js');
const conf = require('./conf.js');
const schema = require('./schema.js');
const NgsiV2 = require('ngsi_v2');
const debug = require('debug')('checks');
let apiEntityClient = null;

//if a path contains folders beyond the doc and ignore ones,
// returns true, otherwise false
const containsModelFolders = function(basePath) {
  const files = fs.readdirSync(basePath);
  let folderCounter = 0;
  files.forEach(function(fileName) {
    try {
      const fullPath = path.join(basePath, fileName);
      debug('*containsModelFolders* - fullPath: ' + fullPath);
      const stat = fs.lstatSync(fullPath);
      if (
        stat &&
        stat.isDirectory() &&
        !conf.nconf
          .get('dmv:ignoreFolders')
          .includes(path.basename(fullPath)) &&
        !conf.nconf.get('dmv:docFolders').includes(path.basename(fullPath)) &&
        !conf.nconf
          .get('dmv:externalSchemaFolders')
          .includes(path.basename(fullPath))
      ) {
        folderCounter++;
      }
      debug('*containsModelFolders* - folders found: ' + folderCounter);
    } catch (err) {
      console.log('***ERROR*** ' + err);
      if (conf.failErrors) {
        throw new Error(err);
      }
    }
  });
  if (folderCounter) {
    return true;
  }
  return false;
};

//if a file matching a given regular expression exists in a given path
// returns true, otherwise false
const fileExists = function(basePath, regex) {
  const files = fs.readdirSync(basePath);
  let counter = 0;
  debug('*fileExists* - regex: ' + regex);
  const regexp = new RegExp(regex);
  files.forEach(function(item) {
    debug('*fileExists* - checked: ' + item);
    if (regexp.test(item)) {
      debug('*fileExists* - regex: match');
      counter++;
    }
  });
  if (counter > 0) {
    return true;
  }
  return false;
};

//returns an EntityClient API for the Orion ContextBroker
const getApiEntityClient = function() {
  if (apiEntityClient == null) {
    const api = NgsiV2.ApiClient.instance;
    api.basePath = conf.nconf.get('dmv:contextBrokerUrl');
    apiEntityClient = new NgsiV2.EntitiesApi();
  }
  return apiEntityClient;
};

module.exports = {
  //check if a documentation file exists in a given path
  docExist(fullPath) {
    let check = false;
    conf.nconf.get('dmv:docFolders').forEach(function(value) {
      try {
        fs.lstatSync(path.join(fullPath, value)).isDirectory();
        if (
          fileExists(path.join(fullPath, value), 'spec.md') ||
          fileExists(path.join(fullPath, value), 'introduction.md')
        ) {
          check = true;
        }
      } catch (err) {
        // Deliberately swallow the error.
      }
    });

    if (
      !check &&
      msg.addWarning(
        fullPath,
        'does not include a documentation ' +
          'file named spec.md or introduction.md'
      ) &&
      conf.failWarnings
    ) {
      throw new Error(
        'Fail on Warnings: ' + JSON.stringify(msg.warnings, null, '\t')
      );
    }
    debug('*docExist* - ' + fullPath + ': ' + check);
    return check;
  },

  //check if a documentation folder exists in a given path
  docFolderExist(fullPath) {
    let counter = 0;
    conf.nconf.get('dmv:docFolders').forEach(function(value) {
      try {
        fs.lstatSync(path.join(fullPath, value)).isDirectory();
        counter++;
      } catch (err) {
        // Deliberately swallow the error.
      }
    });
    if (counter === 0) {
      msg.addWarning(fullPath, 'does not include a documentation folder');
    }
    if (
      conf.nconf.get('dmv:warningChecks').includes('docExist') &&
      counter === 0
    ) {
      if (
        msg.addWarning(
          fullPath,
          'does not include a documentation ' +
            'file named spec.md or introduction.md'
        ) &&
        conf.failWarnings
      ) {
        throw new Error(
          'Fail on Warnings: ' + JSON.stringify(msg.warnings, null, '\t')
        );
      }
    }
    debug('*docFolderExist* - ' + fullPath + ': ' + counter);
    if (counter > 0) {
      return true;
    }
    return false;
  },

  //check if a folder name is valid for a data model
  modelNameValid(fullPath) {
    let check = true;
    if (fullPath.charAt(0) !== fullPath.charAt(0).toUpperCase()) {
      check = false;
    }
    if (
      !check &&
      msg.addWarning(
        fullPath,
        'Model folder names should start in capital letter'
      ) &&
      conf.failWarnings
    ) {
      throw new Error(
        'Fail on Warnings: ' + JSON.stringify(msg.warnings, null, '\t')
      );
    }
    debug('*modelNameValid* - ' + fullPath + ': ' + check);
    return check;
  },

  //check if a folder includes a README.md file
  readmeExist(fullPath) {
    let check = true;
    if (!fileExists(fullPath, 'README.md')) {
      check = false;
    }
    if (
      !check &&
      msg.addWarning(fullPath, 'does not include a Readme file README.md') &&
      conf.failWarnings
    ) {
      throw new Error(
        'Fail on Warnings: ' + JSON.stringify(msg.warnings, null, '\t')
      );
    }
    debug('*readmeExist* - ' + fullPath + ': ' + check);
    return check;
  },

  //check if a folder includes a schema file
  schemaExist(fullPath) {
    let check = true;
    if (!fileExists(fullPath, '^schema\\.json')) {
      check = false;
    }
    if (
      !check &&
      !containsModelFolders(fullPath) &&
      msg.addWarning(
        fullPath,
        'does not include a JSON Schema file schema.json'
      ) &&
      conf.failWarnings
    ) {
      throw new Error(
        'Fail on Warnings: ' + JSON.stringify(msg.warnings, null, '\t')
      );
    }
    debug('*schemaExist* - ' + fullPath + ': ' + check);
    return check;
  },

  //check if a folder includes one or more example files
  exampleExist(fullPath) {
    let check = true;
    if (!fileExists(fullPath, '^example(-\\d+)?\\.json')) {
      check = false;
    }
    if (
      !check &&
      !containsModelFolders(fullPath) &&
      msg.addWarning(
        fullPath,
        'does not include a JSON Example file example(-\\d+)?\\.json'
      ) &&
      conf.failWarnings
    ) {
      throw new Error(
        'Fail on Warnings: ' + JSON.stringify(msg.warnings, null, '\t')
      );
    }
    debug('*exampleExist* - ' + fullPath + ': ' + check);
    return check;
  },

  //check if an example is supported by contextBroker
  exampleSupported(fullPath) {
    let check = true;
    const apiInstance = getApiEntityClient();

    let opts = {
      options: 'keyValues',
    };

    const files = schema.getFiles(fullPath + path.sep + 'example*.json');

    const fileName = null;

    try {
      files.forEach(function(fileName) {
        if (fileName.match(/normalized(-\d+)?\.json$/)) {
          opts = {};
        } else {
          opts = {
            options: 'keyValues',
          };
        }

        const body = schema.openFile(fileName, 'example ' + fileName);

        const createEntity = deasync(function(body, cb) {
          // eslint-disable-next-line no-unused-vars
          apiInstance.createEntity(body, opts, function(error, data, response) {
            if (error) {
              check = false;
              cb(error, null);
            } else {
              msg.addSupportedExample(fullPath, fileName + ' is supported');
              debug(
                '*exampleSupported* - API called successfully. Returned data: ' +
                  JSON.stringify(data, null, 2)
              );
              cb(null, data);
            }
          });
        });

        createEntity(body);

        const entityId = body.id; // String | Id of the entity to be deleted

        const deleteEntity = deasync(function(entityId, cb) {
          apiInstance.removeEntity(entityId, null, function(
            error,
            data,
            response /* eslint-disable-line no-unused-vars*/
          ) {
            if (error) {
              debug(
                '*exampleSupported* - remove entity API error: ' +
                  JSON.stringify(error)
              );
              cb(error, null);
            } else {
              debug(
                '*exampleSupported* - remove entity API called successfully.'
              );
              cb(null, data);
            }
          });
        });

        deleteEntity(entityId);
      });
    } catch (err) {
      msg.addError(
        fullPath,
        'JSON Example ' +
          fileName +
          ' is not supported by ' +
          'contextBroker: ' +
          JSON.stringify(err)
      );
      if (conf.failErrors) {
        throw new Error(
          'Fail on Error: JSON Example ' +
            fileName +
            ' is not supported by ' +
            'contextBroker: ' +
            JSON.stringify(err)
        );
      }
    }
    debug('*exampleSupported* - ' + fullPath + ': ' + check);
    return check;
  },

  // eslint-disable-next-line no-unused-vars
  docValid(fullpath) {
    console.log('*** docValid: not implemented ***');
  },

  // eslint-disable-next-line no-unused-vars
  docValidLinks(fullpath) {
    console.log('*** docValidLinks: not implemented ***');
  },

  // eslint-disable-next-line no-unused-vars
  idMatching(fullpath) {
    console.log('*** idMatching: not implemented ***');
  },

  //if a file matching a given regular expression exists in a given path
  // returns true, otherwise false
  fileExists,
};
