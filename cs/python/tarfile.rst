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

parameters
~~~~~~~~~~

* name. 

* mode: ``r|w|x|a[:[*|gz|bz2|xz]]``
