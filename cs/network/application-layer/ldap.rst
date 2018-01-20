overview
========

- A application layer protocol for accessing and maintaining distributed directory
  information services.

- LDAP 是一种 directory service.

- X.500 directory services were traditionally accessed via the X.500 Directory
  Access Protocol (DAP), which required the Open Systems Interconnection (OSI)
  protocol stack. LDAP was originally intended to be a lightweight alternative
  protocol for accessing X.500 directory services through the simpler (and now
  widespread) TCP/IP protocol stack.

usage
=====
- A common use of LDAP is to provide a central place to store usernames and
  passwords. This allows many different applications and services to connect to
  the LDAP server to validate users.

- 注意 username/password 类型的认证只是 LDAP 的 directory services 功能之一.
  实际上, 是 LDAP 最基础的功能. 因为它实际上可以承载各个 DN 的任何信息 (attributes),
  这才是 directory service 的价值. 认证只是访问这些信息的第一步.

- Unix user and group information can be stored in LDAP and accessed via PAM
  and NSS modules.

architecture
============

- client & server architecture.

  * LDAP server, listening TCP/UDP port 389.
   
  * client make request operation to server.

- 协议没有定义 server 如何实现这些功能. For example, data storage in the server
  is not specified - the server may use flat files, databases, or just be a
  gateway to some other server.

directory structure
===================

- An entry consists of a set of attributes.

- An attribute has an attribute type and one or more values.

- Each entry has a unqiue identifier -- Distinguished Name (DN).

- DN consists of Relative Distinguished Name (RDN) and parent entry's DN.

- RDN is constructed from some of its attributes.

Common attributes.

- cn: common name.

- dc: domain component.

- mail: email.

- sn: surname.

operations
==========

Add
---
Add an entry.

Bind
----
Authenticate a client session.

这是使用 LDAP 进行统一用户认证需要使用的操作.

Delete
------
Delete an entry.

Search and Compare
------------------
Search for an entry.

Check a attributes of DN in request with its stored values.

filter syntax
~~~~~~~~~~~~~
syntax::
    (<operator>[<filter>]+)
    <filter>=(<attribute><operator><value>)

operators::
    =, ~=, <=, >=
    &, |, !

wildcard: ``*``

Special characters can be escaped by ``\``.

Modify
------
Make changes to existing entries.

Modify DN
---------
rename entry.

Abandon
-------
Inform server to abandon an operation.

Unbind
------
Abandon operations and closes connection.

Extended operations
-------------------

StartTLS
~~~~~~~~
Establish TLS on connection.

URI scheme
==========

schema
======

