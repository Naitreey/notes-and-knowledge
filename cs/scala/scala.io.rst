source data
===========
class Source
------------
concrete value members
^^^^^^^^^^^^^^^^^^^^^^
- ``getLines(): Iterator[String]``. Returns an iterator who returns lines (NOT
  including newline character(s)). It will treat any of ``\r\n``, ``\r``, or
  ``\n`` as a line separator (longest match).

object Source
-------------
- provides many factory methods to create an iterable representation of some
  kind of source.

value members
^^^^^^^^^^^^^
- ``fromFile(name: String)(implicit codec: Codec): BufferedSource``. Create a
  Source from file name.

BufferedSource
--------------
