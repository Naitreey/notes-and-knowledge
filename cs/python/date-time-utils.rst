time
====

- time 模块中的内容并不包含 Linux kernel, glibc 提供的全部时间类内容.
  这是为了尽量保持跨平台一致的 API (包含与 POSIX 兼容), 从而进行了
  一定的封装和统一化.

- content overview:

  * wrapper functions akin those C-level functions, for time manipulation.

  * access to different clocks.

  * timer function, sleep function, etc. utilities.

time data format
----------------
- float number. 64bit IEEE double precision.

  * 返回 floating point number 的时间函数, 在 Linux 中具有 nanosecond 精度.
    
  * 注意直接在 REPL 中输出时, string formatting 会显得精度不够, 但实际上不是
    这样.

  * 使用 float 类型作为这类函数的返回值, 有一个潜在的精度问题: 即由于 64bit
    的限制, 当计时超过 104d, 会失去 10E-9 精度. 在 python3.7 中将引入返回值
    为 nanaosecond integer 的一组函数类型.

- ``struct_time``.

  * A namedtuple. equivalent to ``struct tm``.

  * 包含两个时区相关的 additional attributes, 不一定在 tuple 内, 取决于平台的
    ``struct tm`` 实现.

    - ``tm_gmtoff``

    - ``tm_zone``

    这两个属性来源于对程序所属时区的判断, 通过 tzset(3) 实现. 因此,
    ``gmtime()``, ``localtime()`` 等函数的结果不再是 naive 的, 而是全球唯一
    的一个时间点. 具有唯一确定一个时间点的全部信息.

time functions
--------------
For time functions' relation and conversions, see
`this </cs/linux/system-programming/time.rst>`_.

calendar time clock
^^^^^^^^^^^^^^^^^^^

- ``time()``.

  * returns the most accurate time available in floating point, 不局限于
    time(2) syscall 精度.

monotonic clocks
^^^^^^^^^^^^^^^^

- ``monotonic()``. A system-wide clock that doesn't go backwards.

- ``perf_counter()``.  a clock with the highest available resolution to measure
  a short duration. It is system-wide. 在 Linux 中与 monotonic clock 相同.

posix times
^^^^^^^^^^^

- ``clock_gettime(clk_id)``

- ``clock_settime(clk_id, time)``

- ``clock_getres(clk_id)``

- Clock IDs.

  * CLOCK_REALTIME

  * CLOCK_MONOTONIC

  * CLOCK_MONOTONIC_RAW

  * CLOCK_PROCESS_CPUTIME_ID

  * CLOCK_THREAD_CPUTIME_ID

clock informations
------------------

- ``get_clock_info(name)``

seconds <-> struct_time
^^^^^^^^^^^^^^^^^^^^^^^
- ``gmtime([secs])``.

- ``localtime([secs])``

- ``mktime(t)``

  * 注意是转换 ``struct_time`` in local time (i.e., in process's timezone) 至
    seconds since epoch.  若要转换 ``struct tm`` in UTC to seconds since epoch,
    use ``calendar.timegm()``.

struct_time <-> fixed formatted string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``asctime([t])``. If t is not provided, use ``localtime()``.

seconds <-> fixed formatted string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``ctime([secs])``. Default use ``time()``.

struct_time <-> formatted string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``strftime(format[, t])``. Default use ``localtime()``.

- ``strptime(string[, format])``. Default format is ``ctime()`` output format.

timezone
--------

- ``tzset()``

- timezone constants.

  * altzone.

  * daylight.

  * timezone. The offset of the local (non-DST) timezone, in seconds west of
    UTC.

  * tzname.

time-related utils
------------------

- ``sleep()``.

  * accept fractional seconds, 不局限于 sleep(3) glibc library call 精度.

  * The function sleeps at least secs even if the sleep is interrupted by a
    signal, except if the signal handler raises an exception.

- ``process_time()``. the sum of the system and user CPU time of the current
  process. implemented by CLOCK_PROCESS_CPUTIME_ID.

datetime
========
- naive datetime and aware datetime. 基本区别就在于是否有时区. 如果有时区,
  它的时间就是在全球时间中一个确定的点. 否则, 则可以理解为属于任何一个时区.

  * An aware object is used to represent a specific moment in time that is not
    open to interpretation.

  * date is always naive.
    
  * time and datetime can be naive or aware. They are naive if
    ``tzinfo is None``.

- date, time, datetime, timedelta, tzinfo, timezone instances are immutable.

- class hierarchy.

  * datetime is subclass of date.

  * timezone is subclass of tzinfo.

timedelta
---------
- Only days, seconds and microseconds are stored internally. And days, seconds
  and microseconds are normalized to ensure the representation is unique.

  Normalization 时, seconds and microseconds 限制在前一属性的范围内. 例如,
  seconds 最多是 1 天的秒数; microseconds 最多是 1 秒的微秒数.

constructor options
^^^^^^^^^^^^^^^^^^^

All default to 0. All can be integers or float, positive or negative.

- days.

- hours.

- minutes.

- seconds.

- milliseconds.

- microseconds.

- weeks.

class attributes
^^^^^^^^^^^^^^^^

- min.

- max

- resolution.

attributes
^^^^^^^^^^

- days.

- seconds.

- microseconds.

methods
^^^^^^^

arithmetics
"""""""""""
- +,- timedelta

- 数乘. integer or float.

- 除数值, 除 timedelta.

- 整除整数, 整除 timedelta.

- modulo timedelta.

- divmod timedelta.

- negate timedelta.

- abs timedelta.

logic comparison
""""""""""""""""
- the timedelta object representing the smaller duration considered to be the
  smaller timedelta.

- mixed type raise TypeError except for equality checking.

truth
""""""
- ``__bool__``. timedelta 0 is falsy, otherwise truthy.

representation
""""""""""""""
- ``__str__``. ``[D day[s], ][H]H:MM:SS[.UUUUUU]``

- ``__repr__``. can be used to generate the same timedelta.

to seconds
""""""""""
- ``total_seconds()``

date
----

constructor options
^^^^^^^^^^^^^^^^^^^

- year

- month

- day

class attributes
^^^^^^^^^^^^^^^^

- min.

- max.

- resolution.

class methods
^^^^^^^^^^^^^

- ``today()``. current local date.

- ``fromtimestamp(ts)``. local date corresponding to ts.

- ``fromordinal(ordinal)``. ordinal 是从 Gregorian calendar 元年 0 天算起
  的序数.

attributes
^^^^^^^^^^

- year.

- month.

- day.

methods
^^^^^^^

- ``replace(year=None, month=None, day=None)``. Replace the specified
  fields and returns a new date.

- ``timetuple()``.

- ``toordinal()``

- ``weekday()``, 0-6. mon to sun.

- ``isoweekday()``, 1-7. mon to sun.

- ``isocalendar()``. (ISO year, ISO week number, ISO weekday).

arithmetics
"""""""""""
- +,- timedelta

- date - date

representation
""""""""""""""
- ``__str__``. isoformat.

- ``__repr__``. valid input.

- ``isoformat()``.

- ``ctime()``

- ``strftime(format)``.

- ``__format__(format)``. date 可以用在 string format 中, 使用 strftime
  支持的 format specifiers.

comparision
"""""""""""
- 根据日期顺序.

datetime
--------
- Note that datetime is subclass of date, all attributes and methods are
  available.

constructor options
^^^^^^^^^^^^^^^^^^^

- year, month, day. required

- hour, minutes, seconds, microseconds. default 0.

- tzinfo. default None. naive.

- fold. default 0.

class attributes
^^^^^^^^^^^^^^^^
see date.

class methods
^^^^^^^^^^^^^

- ``today()``. naive now().

- ``now(tz=None)``. naive or aware local now.

- ``fromtimestamp(ts, tz=None)``. see date.

- ``utcnow()``. naive utc now.

- ``utcfromtimestamp(ts)``. naive utc datetime.

- ``strptime(date_string, format)``

  * ``format`` 中包含 ``%z`` 时, 将生成 一个 timezone-aware 的 datetime object.

- ``fromordinal(ordinal)``. see date. naive.

- ``combine(date, time, tzinfo=None)``. use tzinfo of time if tzinfo is
  unprovided.

attributes
^^^^^^^^^^

See constructor options.

methods
^^^^^^^

- arithmetic see date.

- date(). its date.

- time(). its naive time.

- timetz(). its aware time.

- replace(...). all attributes can be replaced. No conversion is performed
  whatsoever.

- astimezone(tz=None). Return a datetime in new tz, representing the same
  UTC time. If tz is None, use process's timezone.

- utcoffset(). If aware, return ``self.tzinfo.utcoffset(self)``

- dst(). ``self.tzinfo.dst(self)``

- tzname(). ``self.tzinfo.tzname(self)``

- timetuple(). see date.

- utctimetuple(). Firstly convert a datetime to UTC (if aware) then get
  timetuple.

- toordinal(). see date.

- timestamp().

- weekday(). see date.

- isoweekday(). see date.

- isocalendar(). see date.

arithmetics
""""""""""""
- see date.

- Subtraction of a datetime from a datetime is defined only if both operands
  are naive, or if both are aware. If one is aware and the other is naive,
  TypeError is raised.

comparison
^^^^^^^^^^
- If one comparand is naive and the other is aware, TypeError is raised if an
  order comparison is attempted.

representation
""""""""""""""
- isoformat(sep='T', timespec='auto'). timespec 控制时间部分显示到哪个部分
  为止.

- ``__str__``. isoformat with space separator.

- ctime(). see date.

- strftime(). see date.

- ``__format__``. see date.

time
----

- a time independent of day.

- This class is pretty useless. As datetime has more methods (e.g., astimezone)
  than time.

constructor
^^^^^^^^^^^
time part of datetime.

attributes
^^^^^^^^^^
time part of datetime.

methods
^^^^^^^

All available methods look like those of datetime.

timezone
--------

tzinfo
^^^^^^
- a ABC.

- 注意时区的各种信息一般情况下讲依赖于它参考的时间. 这就是
  为什么 tzinfo 的各种 API 要传入 datetime 的原因.

  例如, DST 是否生效, 依赖于参考的日期时间点; 一个时区在
  不同的历史时间上的名称也可能不同; 在一年的不同时间, 时区
  的 offset 可能是不同的.

- datetime.timezone 只是一个很简单的时区实现, 更复杂的应该
  使用 pytz 或 dateutil.

methods
""""""""

- utcoffset(dt). offset east of UTC.

- dst(dt). DST adjustment, east of UTC.

- tzname(dt). timezone's name.

- fromutc(dt). treat dt as in UTC, return equivalent datetime in tzinfo's
  timezone. 

timezone
^^^^^^^^
- A subclass of tzinfo that has fixed offset from UTC.

class attributes
""""""""""""""""
- utc. The UTC timezone.

dateutil
========

calendar
========

- calendar calculations.

- 提供日历相关函数和日历展示函数.

Calendar
--------
- provides several methods that can be used for preparing the calendar data for
  formatting. This class doesn’t do any formatting itself.

TextCalendar
------------
- generate plain text calendar like unix cal.

HTMLCalendar
------------
- generate HTML calendar.

LocaleTextCalendar
------------------

LocaleHTMLCalendar
------------------

utilities
---------
- utilities for convenient operations.

- one unfit ``timegm()`` function.
