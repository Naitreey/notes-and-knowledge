overview
========
- compiles to Java bytecode. executable code runs on JVM. In fact, Scala code
  can be decompiled to readable Java code, with the exception of certain
  constructor operations. To the Java virtual machine (JVM), Scala code and
  Java code are indistinguishable.

- interoperability with Java. libraries written in Java or Scala may be
  referenced in code of either language.

- On JVM runtime, almost all scala code makes heavy use of java libraries.

types
=====
- Scala heavily re-uses Java types. All of Java's primitive types have
  corresponding classes in the ``scala`` package.
    
- When scala source is compiled to Java bytecodes, scala types are converted to
  Java's primitive types where possible to gain performance benefits.
  
- Scala arrays are mapped to Java arrays.
    
- Scala re-uses many of the standard Java library types.

  * ``java.lang`` types are visible with their simple names in Scala program.

scripting
=========
- ``scala`` 解释器支持执行 scala 脚本, 而无需编译.

- A scala script is a sequence of statements in a file that will be executed
  sequentially.

- 运行方式: ``scala script.scala`` 或 Unix shebang 方式.

- ``scala`` 解释器支持 Unix shebang 语法, 并扩展成为 ``#! ... !#`` 语法. 其一般
  形式为::

    #! ...
    [optional shell script ...

    exec scala "$0" "$@"
    !#]

  注意 ``#!`` 必须是 scala script 的第一行. 解释器根据脚本中是否有 ``!#``
  决定执行逻辑:

  * 若没有 ``!#``, 则解释器忽略 ``#!`` line. 从第二行开始作为 scala program 来
    解析.

  * 若有 ``!#``, 则解释器忽略从 ``#! ... !#`` 中间的一切内容. 从下一行开始作为
    scala program 来解析.

  这允许以下两种 scala script executable 的书写方式.
  
  第一种::

    #!/usr/bin/env scala
    scala code ...

  第二种::

    #!/bin/bash
    shell script ...
    exec scala "$0" "$@"
    !#

  在第二种中, 可以在 scala 脚本前面添加任意的 shell 脚本. 最后一行 ``exec``
  line 必须存在.

- command line args are available as global variable ``args``.
