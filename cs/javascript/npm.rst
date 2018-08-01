overview
========
- npm -- nodejs package manager. (But manages browser-based packages as well.)

- written in node.js

- components:

  * npm CLI client

  * npm package registry

  * npm web frontend

Client
======

CLI commands
------------

- trick to get a complete list of help manuals::

    npm help-search ' '

- every command's manual contains a list of related configurations.

npm install
^^^^^^^^^^^
- aliases: i

global mode
""""""""""""
- installs packages into the install prefix at ``$prefix/lib/node_modules``
  and bins are installed in ``$prefix/bin``.

local mode
""""""""""
- installs packages into the current project directory, which defaults to
  the current working directory. Packages are installed to ``./node_modules``,
  and bins are installed to ``./node_modules/.bin``.

- This is the default mode.

npm ls
^^^^^^

npm search
^^^^^^^^^^

npm adduser
^^^^^^^^^^^
- aliases: login, add-user

- create a new user or login a user to the specified registry.

- When logged in, user's credentials are saved to ``.npmrc``.

configuration
-------------

cli options
^^^^^^^^^^^

environment variables
^^^^^^^^^^^^^^^^^^^^^

user configs
^^^^^^^^^^^^

global configs
^^^^^^^^^^^^^^

default configs
^^^^^^^^^^^^^^^

package registry
================
- The registry has no vetting process for submission, which means that packages
  found there can be low quality, insecure, or malicious.

- npm relies on user reports to take down packages if they violate policies by
  being low quality, insecure or malicious.

package format
--------------
- package in CommonJS format and include a metadata file in JSON format.

web frontend
============

package information
-------------------
- readme

- dependencies

- dev dependencies

- dependents

- versions. clicking version tags shows package page based on that version.

npm analyzer
------------

analysis dimensions
^^^^^^^^^^^^^^^^^^^
- popularity. how many times the package has been downloaded.

- quality. considering the presence of a readme file, stability, tests,
  up-to-date dependencies, custom website, and code complexity.

- maintenance. ranks according to the attention given by developers.

- optimal. combines the three other criteria in a meaningful way.
