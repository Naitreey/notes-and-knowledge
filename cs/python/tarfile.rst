- context manager, fileobj, when file is closed?

overview
========

- format support: plain tar, gzip/bz2/lzma compressed tar.

- tar format support: ustar, gnu tar, pax. default gnu tar.

convenient function
===================

- open().

  参数与 TarFile 相同.

- is_tarfile().

classes
=======

TarFile
-------
- when used as context manager:

  * ``__exit__`` closes tarfile. In the event of an exception an archive opened
    for writing will not be finalized; only the internally used file object
    will be closed (except when ``fileobj`` is used, which is left open).

parameters
~~~~~~~~~~

* name. pathname of the archive. can be omitted if ``fileobj`` is given.

* mode: ``r|w|x|a[:[*|gz|bz2|xz]]``.

* fileobj. If given, used as underlying file object. Mode is overridden by
  fileobj’s mode. fileobj will be used from position 0. fileobj is not closed,
  when TarFile is closed.
