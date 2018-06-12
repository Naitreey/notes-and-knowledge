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
.. code:: sh

    python3 -m venv <dir>
    . .venv/bin/activate

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
