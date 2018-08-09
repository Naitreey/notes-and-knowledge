overview
========
- libmagic is a file type identification library.

- 似乎所有的 text file types 的 mimetype 都有 ``text/*`` prefix. 这似乎
  可以用来比较完善地检查文本文件.

CLI frontend
============

- ``file`` command

language wrappers
=================

python-magic
------------

module-level utils
^^^^^^^^^^^^^^^^^^
- ``from_file(filepath, mime=False)``. ``mime`` controls whether returns mime
  type.

- ``from_buffer(str_or_bytes, mime=False)``

Magic
^^^^^
- not safe for sharing across multiple threads, will fail throw if this is
  attempted.
