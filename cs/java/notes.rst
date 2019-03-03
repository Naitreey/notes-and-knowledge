overview
========
- What Java is good for?

  * big interprise software with many people involed in.  This is where Java's
    verbosity becomes useful. It's an enterprise language; a
    boilerplate-oriented language, which lets a larger team of more mediocre
    programmers create something without blowing it up.

- Good and bad about Java and its ecosystem:

  Bad:

  * verbose, repetitive, boilerplate code everywhere.

  * Everything is a class is really stupid.
    
  * Extreme object oriented designs and major design patterns abuse.

  * Class naming convention is insane.

  * Packaging directory is insane.

  * XML configuration is insane.

  * Toolchain is horrible to use.

  * Memory footprint and startup time problem.

  * So many features available in other languages are not there for Java.

  * Too many artificial restrictions put in place by the designers of the
    language to keep programmers "safe" from themselves.

Installation
============
archlinux
---------
overview
^^^^^^^^
- OpenJDK is supported.
  
- Multi-version.  Multiple versions of jdk can be installed simultaneously
  without conflict. jdk version can be switched via ``archlinux-java`` script.

files
^^^^^
* /etc/profile.d/jre.sh -- add /usr/lib/jvm/default/bin to PATH.

CLIs
^^^^
- Most executables of the Java installation are provided by direct links in
  /usr/bin, while others are available in /usr/lib/jvm/default/bin, made available
  by /etc/profile.d/jre.sh.

archlinux-java
""""""""""""""
edit links /usr/lib/jvm/default and /usr/lib/jvm/default-runtime to current
specified java version: ``/usr/lib/jvm/java-${JAVA_MAJOR_VERSION}-${VENDOR_NAME}``
and ``/usr/lib/jvm/java-${JAVA_MAJOR_VERSION}-${VENDOR_NAME}/jre``.

To launch an application with another version of java than the default one,
modify PATH by prepending the desired jdk bin path.

- ``status``. list installed java environments.

  * ``(default)`` meaning now set as default.

  * ``*/jre`` meaning only jre part is installed.

- ``set <JAVA_ENV>``. set installed java version, as output of ``status``

- ``unset``. unset environment.

- ``fix``. fix invalid ``JAVA_ENV``.

packages
^^^^^^^^
- headless jre. minimal java runtime environment, needed for non-GUI java
  programs.

- full jre. full java runtime environment. needed for GUI java programs,
  depending on headless jre.

- jdk. needed for java development, depends on full jre.
CLIs
====
jar
---
- 用于操作 jar package.
