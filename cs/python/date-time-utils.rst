time
====

overview
--------

- time 模块中的内容并不包含 Linux kernel, glibc 提供的全部时间类内容.
  这是为了尽量保持跨平台一致的 API (包含与 POSIX 兼容), 从而进行了
  一定的封装和统一化.


time functions
--------------
For time functions' relation and conversions, see
`this </cs/linux/system-programming/time.rst>`_.

- ``time()``.

  * returns the most accurate time available in floating point, 不局限于
    time(2) syscall 精度.

time-related operations
-----------------------

- ``sleep()``.

  * accept fractional seconds, 不局限于 sleep(3) glibc library call 精度.

time data format
----------------

- ``struct_time``.

  * A namedtuple. equivalent to ``struct tm``.

datetime
========
- time, datetime

  * time.timezone 给出的 offset 是 localtime 和 utc-time 之差的相反数.

  * 对于 datetime.strptime classmethod, ``format`` 中包含 ``%z`` 时, 将生成一个
    timezone-aware 的 datetime object.

dateutil
========

calendar
========
