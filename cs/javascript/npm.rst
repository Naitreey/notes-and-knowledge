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
"""""""""""
::

  npm install <name>[@<version>]

- When installing packages, if version is not specified, a ``package.json`` in
  current directory is consulted if present, otherwise the latest version is
  installed.

- When installing new packages, any new packages specified on commandline will
  be saved to package.json.  By default, ``^<ver>`` is used as version number
  specifier.

  * ``--save-prod`` default. save dependencies under ``dependencies`` key.

  * ``--save-dev`` save under ``devDependencies``.

  * ``--save-optional`` save under ``optionalDependencies``.

  * ``--no-save`` prevent saving as dependencies.

  * ``--save-exact`` save exact version number.

  * ``--save-bundle`` also save dependencies as bundled dependencies.

npm uninstall
^^^^^^^^^^^^^
::

  npm uninstall [@<scope>/]<pkg>[@<version>]...

- aliases: remove, rm, r, un, unlink

- uninstall a package, by default also modify package.json and
  package-lock.json accordingly.

  * ``--save`` default. remove the package from ``dependencies`` key.

  * ``--save-dev``. remove the package from ``devDependencies`` key.

  * ``--save-optional``. remove from ``optionalDependencies`` key.

  * ``--no-save``. do not modify package.json and package-lock.json.

- Use ``-g`` to uninstall global package.

npm update
^^^^^^^^^^
::

  npm update [-g] [<pkg>...]

- aliases: up, upgrade

- Update listed packages or all packages to the latest version that satisfying
  version specifier as defined in ``package.json``.

- Use ``-g`` flag to update globally installed packages. If no package is
  specified, all packages are updated.

- Use ``--dev`` flag to update dev dependencies.

npm ls
^^^^^^

npm search
^^^^^^^^^^

npm adduser
^^^^^^^^^^^
- aliases: login, add-user

- create a new user or login a user to the specified registry.

- When logged in, user's credentials are saved to ``.npmrc``.

npm init
^^^^^^^^
- init a project by creating package.json. It operates by calling ``npx``
  or use legacy init behavior.

extensible mode
"""""""""""""""
::

  npm init @<scope> [options]            # npx @<scope>/create
  npm init [@<scope>/]<name> [options]   # npx [@<scope>/]create-<name>

- create and initialize package according the specified initializer.

- additional options are passed to corresponding ``npx`` command.

legacy mode
"""""""""""
::

  npm init [--force|-f|--yes|-y|--scope]

- By default, the following fields are initialized: name, version, description,
  main, scripts, keywords, author, license, bugs, homepage.

- the default value of init fields can be customized by configuration.

- The package.json questionnaire can be customized by ``~/.npm-init.js``

package management
------------------
- npm 只区分 local packages and global packages. 并不存在对 system-wide package
  与 user package 的区分. 对 npm 而言, ``$prefix`` 指向哪里, 哪里就是 global
  packages 的位置.

system-wide packages
^^^^^^^^^^^^^^^^^^^^
- 在 linux 下, global nodejs packages 一般不通过 package manager 安装. 而是通过
  npm 命令的全局模式进行管理.

- 默认的 ``$prefix`` 一般是 ``/usr``.

- system-wide packages 位于 ``$prefix/lib/node_modules``.

user packages
^^^^^^^^^^^^^
- 由于默认不存在 npm user packages 概念, 需要修改 ``$prefix`` 配置. 例如::

    export npm_config_prefix=~/.node_modules

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

- package.json 与 package-lock.json 各自的作用.

  * package.json 指定一个 package/project/etc. 的直接依赖, 它指定的版本依赖
    情况可以是相对灵活的. 也就是说, package.json 用于 package 发布. 用于指定
    一个 package 能够正常工作的依赖版本范围. 它相当于 python 中的 setup.py.

  * package-lock.json 指定一次安装的 snapshot. 它指定完全固定的版本. 也就是说
    package-lock.json 用于项目部署. 用于可重复安装. 它相当于 python 中的
    requirements.txt.

package.json
^^^^^^^^^^^^
- ``package.json`` is a complete specification of a node package.

- It's a json object.

- use ``npm init`` to create a package.json.

contents
""""""""
- ``name``. package's name. required. lowercase, no space, only ``-`` and ``_``
  are allowed as separator between ASCII letters.

- ``version``. package's version. must follow semver.

- ``dependencies``. for production.

- ``devDependencies``. for development and testing.

- ``bundledDependencies``. for dependencies that should be bundled with the
  project source.

  When to use bundled dependencies [SONPMBundledDep]_:

  * packages that doesn't come from a npm registry, that has to be installed
    manually.

  * corporate private modules without a private registry.

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

- 如何使用 package-lock.json.

  * save package-lock.json into VCS in a single commit. 这样可以保证对项目的
    所有部署都是一致的. 这对 CI 和部署是重要的.

  * any npm command that modifies a project/package's dependency in any way,
    will update package-lock.json accordingly by default.

  * the diffs of package-lock.json will inform you of any changes of transitive
    dependencies.

  * When two branches caused merge conflict on package.json and/or
    package-lock.json, manually fix package.json conflicts, then ``npm install``
    will automatically resolve any conflicts for you and write a merged package
    lock that includes all the dependencies from both branches in a reasonable
    tree.

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


references
==========
.. [SONPMBundledDep] `Advantages of bundledDependencies over normal dependencies in NPM <https://stackoverflow.com/a/25044361/1602266>`_
