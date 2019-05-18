fsc
===
- A fast scala compiler. It's fast because it uses a long-running server to
  compile the sources. 这样 jar packages 加载以及其他初始化操作只需要执行一次.

- The ﬁrst time you run fsc, it will create a local server daemon. On each
  compilation, it send the list of files to compile to the daemon, and the
  daemon will compile the files.

synopsis
--------
- shutdown server::

    fsc -shutdown

scala
=====
- A scala source/bytecode interpreter and REPL.

- It can also interpret scala scripts. When interpreting scala scripts, it
  firstly compile source codes to Java bytecodes, then loads them immediately
  via a class loader, and execute them.

synopsis
--------
::

  scala <options> [<script|class|object|jar> <arguments>]

- script -- scala source code to interpret.

- object -- name of the entry point object of an application.
