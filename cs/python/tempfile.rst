high level
==========

全部可以用作 context manager, 用完自动清理.

file
----
- Returns: file-like object.

- file is destroyed when it's closed.

- when using as context manager:

  * ``__enter__`` returns file-like object itself.

  * ``__exit__`` closes the file, which in turns destroys it.

- default mode is ``w+b``

种类.

- TemporaryFile

  the directory entry for the file is either not created at all or is removed
  immediately after the file is created.

  File is created using ``os.O_TMPFILE`` flag.

- NamedTemporaryFile

  file has a named directory entry ``file.name``.

- SpooledTemporaryFile

  Like TemporaryFile, but data is spooled in memory until it exceeds ``max_size``
  or until the file’s fileno() method is called, at which point the contents
  are written to disk.

  additional method:

  - ``.rollover()``. roll over to disk regardless of its size.

directory
---------

- TemporaryDirectory

  * returns: an object.

  * On completion of the context or destruction of the temporary directory
    object the newly created temporary directory and all its contents are
    removed from the filesystem. 注意没有 close method, 不是 file-like object.

  * when used as context manager:

    - ``__enter__`` returns directory name

    - ``__exit__`` remove directory recursively

  * attributes, methods

    - name

    - cleanup().


low level
=========

file
----

- mkstemp

directory
---------

- mkdtemp
