interesting stuffs in `os.path` module

* 一系列基于 ``stat(2)`` 的函数, 例如 ``exists()``, ``getatime()``, ``ismount()``,
  ``samefile()``, etc.

* 一系列 path manipulation functions, 比较容易被忽略的有 ``split()``, ``splitext()``,
  ``commonpath()``, ``commonprefix()``, ``expanduser()``, etc.

* ``expanduser()`` 选择的 home directory 首先根据 environ ``HOME``; 若不存在, 则根据
  real UID 去 passwd 文件里 home directory (根据 pwd module). 注意是 real UID, 因为
  real UID 的概念就是进程的 owner.

* ``exists`` & ``lexists`` 都是检查路径是否存在, 但前者会认为 broken symlink 属于
  路径不存在, 所以还是要根据自己的需求进行选择.

