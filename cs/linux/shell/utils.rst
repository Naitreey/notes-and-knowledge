environment management
======================
direnv
------

usage
^^^^^
- load or unload environment variables depending on the current directory. This
  allows project-specific environment variables without cluttering user's
  profile file.

- Before each prompt, direnv checks for the existence of a ".envrc" file in the
  current and parent directories.

- the contents of the .envrc file must be valid bash syntax, regardless of the
  shell you are using. This is because direnv always executes the .envrc with
  bash.

- Before loading a new envrc, you must firstly allow it. This is a security
  measure.

- 当给一个项目设置 envrc 时, 应该避免过分 clutter .envrc file, 即不要凡是参数
  就都放到这里面, export 至整个项目可见.
  
  A rule of thumb: 当项目包含很多组件、程序时, 需要在不止一个组件、程序等使用的
  参数, 才有必要考虑放到环境变量中.

  如果目录本身的目的比较单一, 则不需要考虑这么多, 按方便地来就行.

install
^^^^^^^
- bash::

    eval "$(direnv hook bash)"

configuration
^^^^^^^^^^^^^

- config path: ``/home/naitree/.config/direnv``

CLI
^^^

- ::
    
    direnv allow

- ::

    direnv edit

utility functions
^^^^^^^^^^^^^^^^^
see also: direnv-stdlib(1), and https://github.com/direnv/direnv/blob/master/stdlib.sh

- ``PATH_add <path>``

- ``source_env <envfile>``

- ``source_up``

- ``dotenv`` load .env

- ``layout go``

- ``layout node``

- ``layout perl``

- ``layout python <version>``

- ``layout python3``

- ``layout ruby``

- ``use node``

- ``watch_file``

custom utilities
""""""""""""""""
- create your own extensions by creating a bash file at
  ``~/.config/direnv/direnvrc`` or ``~/.direnvrc``
