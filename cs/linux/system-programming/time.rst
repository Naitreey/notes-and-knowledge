time
====

time data formats
-----------------

* ``time_t``

* ``struct tm``

* ``struct timeval``

* ``struct timespec``

time data retrieval/setting
---------------------------

* ``time_t``: ``time()``, ``stime()``

* ``struct timeval``: ``gettimeofday()``, ``settimeofday()``

* ``struct timespec``: ``clock_gettime()``, ``clock_settime()``

time data conversions
---------------------

- ``time_t`` to/from ``struct tm``

  * to: ``gmtime()``

  * to: ``localtime()``

  * from: ``mktime()``

- ``struct tm`` to/from custom-formatted string

  * to: ``strftime()``

  * from: ``strptime()``

- ``struct tm`` to/from fixed-formatted string

  * to: ``asctime()``

- ``time_t`` to/from fixed-formatted string

  * to: ``ctime()``

timezone
========

timezone definitions
--------------------

format
^^^^^^
- timezone data is defined in a standard format.

- See tzfile(5)

storage
^^^^^^^
- ``/usr/share/zoneinfo``.

- A specified timezone string is actually a relative path to a timezone
  definition file under this directory.

admin tools
^^^^^^^^^^^

- zic(8)

- zdump(8)

specifying timezone
-------------------

- system global timezone:
  
  * defined in ``/etc/localtime``, which is often simply a symlink to one of
    defintions under ``/usr/share/zoneinfo``.

  * For some distributions, ``/etc/timezone`` should also be defined, which
    contains a timezone name, which should be the path to a file relative to
    ``/usr/share/zoneinfo``. [SETimezone]_

- process specific timezone: defined by ``TZ`` environ. two formats are
  accepted. 一种是直接定义时区; 另一种是指向 ``/usr/share/zoneinfo`` 下的定义
  文件. See tzset(3).

determining timezone
--------------------
Timezone is determined by calling tzset(3) function. See tzset(3) for details.

- If TZ is not defined in environ, use system timezone.

- If TZ is defined but not recognized, UTC is used.

- Otherwise, the specified TZ is used.

References
==========
.. [SETimezone] `What is /etc/timezone used for? <https://unix.stackexchange.com/questions/452559/what-is-etc-timezone-used-for>`_
