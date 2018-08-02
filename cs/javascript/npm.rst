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
- This is the default mode.

- installs packages into the current project directory, which defaults to
  the current working directory. Packages are installed to ``./node_modules``,
  and bins are installed to ``./node_modules/.bin``.

invocations
""""""""""""
::

  npm install <name>[@<version>]

- When installing packages, if version is not specified, a ``package.json`` in
  current directory is consulted if present, otherwise the latest version is
  installed.

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

- There are 5 levels of configurations involved with npm:

  * cli options
  
  * environment variables
  
  * user configs
  
  * global configs
  
  * default configs

package file and package locks
------------------------------

package-lock.json
^^^^^^^^^^^^^^^^^
- why does npm need package locks?

  package lock 的作用相当于是对一次 specific installation of dependencies 保存
  快照. 这是为了保证能够在未来的时间、在不同的环境下能够完全重复与此次相同的安
  装结果.

  注意 ``package.json`` 不能保证这种完全的可重复性. 这是因为:

  * ``package.json`` 中对依赖的版本指定可以是一个范围, 而不是确定的版本.

  * ``package.json`` 一般只指定 direct dependencies, 可能出现直接依赖没有改变,
    但间接依赖更新版本的情况.

  因此, 我们需要一种能够明确声明当前安装的所有 packages 的方法.

- ``package-lock.json`` 的作用相当于 python 中 ``pip freeze`` 的输出.

- package lock 的特点在于:

  * exact

  * reproducible.

- Package installation process with the presence of ``package-lock.json``.

  * Once ``package-lock.json`` is present, any future installation will base
    its work off this file, instead of recalculating dependency versions off
    ``package.json``.

  * For installation of certain dependency, the ``resolved`` package file is
    used if available, otherwise falling back to normal package resolution using
    ``version`` key.

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
