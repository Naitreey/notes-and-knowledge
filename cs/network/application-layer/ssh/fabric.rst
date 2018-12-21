overview
========
- A high-level library to execute shell commands remotely over SSH.

Architecture
============
fabric, invoke, paramiko 三个库的分工.
  
pyinvoke
--------
- CLI parsing, task organization, and shell command execution

- Anything that isn’t specific to remote systems tends to live in Invoke.

paramiko
--------
- low/mid level SSH functionality - SSH and SFTP sessions, key management, etc.

fabric
------
- Subclassing Invoke’s context and command-runner classes, wrapping them around
  Paramiko-level primitives.

- Extending Invoke’s configuration system by using Paramiko’s ssh_config
  parsing machinery.

- Implementing new high-level primitives of its own.

Connections
===========

Connection
----------
- A connection to SSH daemon.

 * Inherit invoke.context.Context, as it is a context within which commands,
   tasks etc can operate.

 * Encapsulate a paramiko.client.SSHClient.

- Lifecycle:

  * Instantiation does not actually initiate the network connection. (lazy
    connection)

  * 进行操作时会 implicitly call ``open()`` method.

  * Connection close need not be explicit handled by programmer, can be left to
    be handled by GC. Or by calling ``close()`` explicitly or via context
    manager.

constructor options
^^^^^^^^^^^^^^^^^^^
- ``host``. Required. The first formal parameter. Can be a compound string::

    [user@]host[:port]

  这样可以省去相关参数和相关配置.

- ``user``. default to config.user.

- ``port``. default to config.port.

- ``config``. A Config instance to use for this connection. default to an
  anonymous Config.

- ``gateway``.

- ``forward_agent``

- ``connect_timeout``. default to config.timeouts.connect.

- ``connect_kwargs``. a dict of kwargs passed to SSHClient.connect. Put
  password/keyfile etc. SSH connection parameters here. Default:
  config.connect_kwargs.

- ``inline_ssh_env``.

attributes
^^^^^^^^^^
- ``is_connected``. 能确实保证当前是否已连接. 因为它是一个 property, 会自动检测
  ssh transport layer 状态.

methods
^^^^^^^
- ``run(command, **kwargs)``. Every run execution is invoked in its own
  distinct shell session. Returns: ``fabric.runners.Result``. See
  ``invoke.Context.run`` for parameters. The difference from
  ``invoke.Context.run``:

  * ``replace_env`` is default True. so that remote commands run with a ‘clean’,
    empty environment instead of inheriting a copy of the current process’
    environment. For security.

- ``sudo(command, **kwargs)``. execute via sudo. otherwise identical to run().

- ``put(*args, **kwargs)``. transfer file to remote host. See Transfer.put.

- ``get()``. transfer file from remote host.

- ``local()``. execute command locally, as invoke.context.Context.run.

- ``__enter__()``, ``__exit__()``. context manager to close connection
  automatically upon exiting context.

- ``close()``. Close connection, if open.

Runners
=======

Result
------
- fabric.runners.Result is a subclass of invoke.runners.Result.

file transfer
=============

Transfer
--------
- A wrapper to connection, responsible for managing file upload/download.

methods
^^^^^^^
- ``put(local, remote=None, preserve_mode=True)``. Upload a local file or
  stream to remote system. returns fabric.Transfer.Result.

  * local: A path to local file (not directory), or a file-like object.

  * remote: remote path to save file. Default None, meaning uploading to home
    dir. Intermediate directories must exist beforehand.

    - When local is file path, remote can be None, a file path or directory path.

    - When local is stream, remote must be a file path.
    
    Most SFTP servers set the remote working directory to the connecting user’s
    home directory and do *not* expand tildes.

  * preserve_mode: whether chmod to match local mode. default True.

Auto-response
=============
- Use pyinvoke's auto-response utilities to feed input as appropriate. Like
  ``expect`` command.

Connection groups
=================

Group
-----

SerialGroup
-----------

ThreadingGroup
--------------

GroupResult
-----------

GroupException
--------------

CLI usage
=========

fab
---
::

  fab [options] task [task-options] [task [task-options]]...

- ``task`` can be: Python functions, methods or entire objects

- Can specify task execution order.

- Tasks are parameterized via regular GNU-style arguments.

task definition
---------------
::

  @task
  def some_task(connection):
    pass

- Use fabric.task decorator to expose the task on the command line.

- The task is called for each host passed as ``connection``.
