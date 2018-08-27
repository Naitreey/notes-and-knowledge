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

- installation: see https://github.com/pyenv/pyenv#installation

- usage.

  .. code:: sh

    pyenv install <version>
    pyenv global|local|shell <version>
