overview
========
- a python implementation of SSHv2 protocol.

Client
======

methods
-------

connect
^^^^^^^
- password. 若 None, 不尝试使用密码方式认证. 若用户密码为空, 需提供
  ``password=""``, 而不是不提供密码.
