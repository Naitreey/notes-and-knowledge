system-wide pythons
===================
- variables::

    sys.base_prefix
    sys.prefix

- directories.

  * ``/usr/lib[64]/python2.X/``

  * ``/usr/lib[64]/python3.X/``

  * ``/usr/local/lib[64]/pythonX.Y/``

  * ``site-packages/``

  * ``dist-packages/``

virtual environment
===================

venv
----

usage
^^^^^
- create new virtual environment.

  .. code:: sh
  
      python3 -m venv <dir>
      . .venv/bin/activate

- upgrade an existing virtual environment to new version of python.
  但这不会迁移在旧版本中安装的 modules.

  .. code:: sh

      python3 -m venv --upgrade <dir>

virtualenv
----------
- should be similar to venv

multi-version
=============
pyenv
-----
overview
^^^^^^^^
- 用处: 能够在同一个系统中, 方便地使用多个版本的 python. 这包括多版本的安装,
  版本切换等.

- features:

  * 多个作用域的 python 版本设置: global per-user, per-project, per-shell.
    以及能同时加载多个 python 版本.

  * does not depend on python itself, pure shell script.

  * with pyenv-virtualenv plugin, virtualenv can be managed in a single step.

mechanisms
^^^^^^^^^^
pyenv intercepts Python commands using shim executables, by prepending
``$(pyenv root)/shims`` into PATH. The shims determines which version of the
called command to be used (according to pyenv's scoping rules), and passes
command line to the correct python installation (对于 pyenv install 的版本,
在 ``$(pyenv root)/versions`` 下, 对于系统版本, 则在系统安装目录下.)

what does ``pyenv init -`` do under the hood?

- 添加 shims 进入 PATH, override 平时的 python 相关命令.

- source 自动补全脚本.

- rehash shims.

- install ``pyenv`` shell function, override ``pyenv`` command. 作为 shell
  function, pyenv 才能修改当前 shell 的环境变量 (``pyenv shell`` 需要).

installation
^^^^^^^^^^^^
see https://github.com/pyenv/pyenv#installation, overview:

- Clone pyenv 源代码仓库至 ``$HOME/.pyenv``. pyenv 代码仓库包含它识别和支持
  的全部 python 版本:

  .. code:: sh

    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

- 在 ``~/.bashrc`` 中添加以下内容, 从而让 pyenv 配置 shell 环境:

  .. code:: sh

    declare -x PYENV_ROOT="$HOME/.pyenv"
    [[ ":${PATH}:" == *:$PYENV_ROOT/bin:* ]] || PATH="$PYENV_ROOT/bin${PATH:+:$PATH}"
    command -v pyenv &>/dev/null && eval "$(pyenv init -)"

- 重启当前 shell 以加载新的 bashrc 等配置:

  .. code:: sh

    exec "$SHELL"

upgrade
^^^^^^^
Simply pull the repo, to fetch the latest python versions and other
improvements.

disable
^^^^^^^
- remove ``pyenv init`` line from bashrc.

uninstall
^^^^^^^^^
- disable, then simply remove pyenv repo.

CLI
^^^
- install python version
  
  .. code:: sh

    pyenv install <version>

  Build deps needs to be installed beforehand, e.g.,

  .. code:: sh

    # arch
    pacman -S base-devel openssl zlib xz
    # ubuntu
    sudo apt-get update
    sudo apt-get install -y \
        make build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
        xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

- specify local python version

  .. code:: sh

    pyenv local [--unset | <version> ...]

  writing a ``.python-version`` to current working directory. 当指定多个版本时,
  第一个版本有最高优先级, 即无版本号的 python 相关 command 指向这个版本.

  without args/options, report configured local version.

  with ``--unset``, unset the local version, by deleting the version file from
  current directory. 只有当前目录有 version file 时才能 unset 成功.

- specify global python version

  .. code:: sh

    pyenv global [<version> ...]

  writing ``$(pyenv root)/version``. multi-version 同上.

  without args/options, report the current global version.

- specify shell-specific python version,

  .. code:: sh

    pyenv shell [--unset | <version> ...]

  define ``PYENV_VERSION`` in current shell. multi-version 同上.

  without args/options, report configured shell-specific python version.

  with ``--unset``, unset current shell python version.

- install python version

  .. code:: sh

    pyenv install [options] <version>
    pyenv install [options] <definition-file>
    pyenv install -l|--list

  ``-f``, ``--force``, install even if version appears to be already installed.

  ``-s``, ``--skip-existing``, Skip the installation if the version appears to
  be installed already.

  ``-l``, ``--list`` list available versions.

  pyenv install 调用 python-build plugin 进行安装. 见 plugins for additional
  options.

- uninstall python version:

  .. code:: sh

    pyenv uninstall [-f|--force] <version>

  ``--force``, Attempt to remove the specified version without prompting for
  confirmation.

- list all commands:

  .. code:: sh

    pyenv commands

- refresh shims for python binaries:

  .. code:: sh

    pyenv rehash

  Run this command after you install a new version of Python, or install a
  package that provides binaries. pyenv install/uninstall automatically run
  this command.

- display currently active python version and its origin

  .. code:: sh

    pyenv version

- show all installed versions, show ``*`` next to currently active versions
  (multi-version has multiple ``*``).

  .. code:: sh

    pyenv versions

- display real path of currently active python binaries.

  .. code:: sh

    pyenv which <command>

- Lists all Python versions with the given command installed.

  .. code:: sh

    pyenv whence <command>

python version precedence
^^^^^^^^^^^^^^^^^^^^^^^^^
1. shell: ``PYENV_VERSION`` environ, can be set and unset by ``pyenv shell``.

2. directory-specific local: ``.python-version`` file in the current directory
   or any of its parent directory. can be set and unset by ``pyenv local``.

3. global: ``$(pyenv root)/version`` file. can be set and unset by
   ``pyenv global``.

4. system version

simultaneous multiple versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``pyenv shell|local|global`` 每个 subcommand 都可以指定多个 python 版本.
这样可以同时使用多个版本. 即通过指定 ``pythonX.X`` 来调用所需版本.

recognizable environs
^^^^^^^^^^^^^^^^^^^^^
- ``PYENV_VERSION``. python version to be used for current shell.

- ``PYENV_ROOT``. directory where pyenv repo resides.

- ``PYENV_DEBUG``. output debug info.

- ``PYENV_HOOK_PATH``. where to search for pyenv hooks.

- ``PYENV_DIR``. Directory to start searching for local .python-version files.

- ``PYTHON_BUILD_ARIA2_OPTS``. pass additional parameters to ``aria2``.

debugging
^^^^^^^^^
- enable debug logging by setting ``PYENV_DEBUG=1`` in environment. Then
  execute pyenv commands.

- or ``pyenv --debug ...``.

specify cpython configure options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: sh

  PYTHON_CONFIGURE_OPTS="..."

- for libpython dynamic lib: ``--enable-shared``

- for framework support: ``--enable-framework``

plugins
^^^^^^^
- pyenv 支持安装 plugins, 参考 `Authoring plugins <https://github.com/pyenv/pyenv/wiki/Authoring-plugins>`_ and `Plugins <https://github.com/pyenv/pyenv/wiki/Plugins>`_.

- plugins 只需 clone 至 ``$(pyenv root)/plugins`` 即可.

pyenv-python-build
""""""""""""""""""
- compile and install different versions of Python on UNIX-like systems,
  supporting ``pyenv install`` command.

- CLI::
  
    python-build [options] {<version> | <definition-file>} <destination>

    -k/--keep          Keep source tree in $PYENV_BUILD_ROOT after installation
                       (defaults to $PYENV_ROOT/sources)
    -p/--patch         Apply a patch from stdin before building
    -v/--verbose       Verbose mode: print compilation status to stdout
    --version          Show version of python-build
    -g/--debug         Build a debug version

  * definition file 参考 pyenv 提供的 definition file, 这可用于安装 pyenv 尚不
    支持的 python 版本.

  * apply patch::

      python-build --patch 3.6.7 </path/to/patch

- environment variables.

  * ``TMPDIR`` sets the location where python-build stores temporary files.

  * ``PYTHON_BUILD_BUILD_PATH`` sets the location in which sources are
    downloaded and built. By default, this is a subdirectory of TMPDIR.

  * ``PYTHON_BUILD_CACHE_PATH`` if set, specifies a directory to use for
    caching downloaded package files.

  * ``PYTHON_BUILD_MIRROR_URL`` overrides the default mirror URL root to one of
    your choosing.

  * ``PYTHON_BUILD_SKIP_MIRROR`` if set, forces python-build to download
    packages from their original source URLs instead of using a mirror.

  * ``PYTHON_BUILD_ROOT`` overrides the default location from where build
    definitions in share/python-build/ are looked up.

  * ``PYTHON_BUILD_DEFINITIONS`` can be a list of colon-separated paths that
    get additionally searched when looking up build definitions.

  * ``CC`` sets the path to the C compiler.

  * ``PYTHON_CFLAGS`` lets you pass additional options to the default CFLAGS.
    Use this to override, for instance, the -O3 option.

  * ``CONFIGURE_OPTS`` lets you pass additional options to ./configure.

  * ``MAKE`` lets you override the command to use for make. Useful for
    specifying GNU make (gmake) on some systems.

  * ``MAKE_OPTS`` (or ``MAKEOPTS``) lets you pass additional options to make.

  * ``MAKE_INSTALL_OPTS`` lets you pass additional options to make install.

  * ``PYTHON_CONFIGURE_OPTS`` and ``PYTHON_MAKE_OPTS`` and
    ``PYTHON_MAKE_INSTALL_OPTS`` allow you to specify configure and make
    options for building CPython. These variables will be passed to Python
    only, not any dependent packages (e.g. libyaml).

- python-build will automatically verify the SHA2 checksum of each downloaded
  package before installing it.

pyenv-virtualenv
""""""""""""""""
- useless plugin, 在使用 direnv 的情况下, 并不能简化任何步骤. 而且它让 venv
  在 pyenv 的全局目录下创建, 失去了 local venv 带来的便利性.

- manage virtualenvs and conda environments integrated with pyenv.

- install.

  * clone

  * Add pyenv virtualenv-init to your shell to enable auto-activation of virtualenvs

    .. code:: sh

      eval "$(pyenv virtualenv-init -)"

    在使用 direnv 时, 不该使用这个.

pyenv-update
""""""""""""

deployment with pyenv
^^^^^^^^^^^^^^^^^^^^^
- 设置合适的 global, local, shell-specific python version

- 设置 PATH, 让应用调用 python 相关命令时, 使用的是 shims, 这样才能走 pyenv
  流程加载所需的 python version:

  .. code:: sh

    export PATH=~/.pyenv/shims:~/.pyenv/bin:"$PATH"
