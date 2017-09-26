- error logging

  mysqld 根据 ``--log-error`` option 来决定错误日志输出. 若这个选项没有设置,
  日志写到 stderr. 此时 ``log_error`` system variable 为 ``stderr``.

- 处于安全考虑, ``local_infile`` 默认是 OFF, 需要在 mysql client 和 mysqld
  同时开启.

mysql client
------------

- ``\g`` ``\G`` 可以执行语句, 相当于 ``;``. 后者将结果列以竖排的形式输出, 比较方便.

- ctrl-c 和 ``\c`` 都可以终止当前语句.

- mysql client 会给出执行时间, 这个时间是在客户端算出的从发出请求到收到结果的 wall
  clock time.

- 支持输入 mutiline 的 string 和 identifier. 直接加回车即可.

- mysql client 对不同的 multiline 模式给出不同的 prompt string, 甚至包含 string,
  identifier 和 block comment 的多行输入模式. ``">``, ``'>``, ``\`>``, ``/*>``.

- 可以在连接时指定要使用的数据库, 或者用 ``USE`` 切换.

- cmdline 参数 ``-p`` 指定密码时不能有空格, 否则会被认为后面的参数是数据库名.

- In non-interactive mode, read input sql from stdin, print results to stdout.
  For processing convenience, such output is tab-delimited for each column.

Language driver
---------------
- python driver 需要根据应用场景和需求来选择.

  目前主要的 python driver 以及各自的特点:

  * MySQL for Python (``MySQLdb``)

    - popular, mature and stable

    - not developed since 2013-06-28 (latest update date on sourceforge),
      essentially dead.
      https://github.com/PyMySQL/mysqlclient-python/issues/44

    - no python3 support

    - c extension, very fast
      https://gist.github.com/methane/90ec97dda7fa9c7c4ef1
      https://github.com/PyMySQL/PyMySQL/issues/342
      https://wiki.openstack.org/wiki/PyMySQL_evaluation#Architecture_and_Performance

  * mysqlclient

    - popular (700+ stars on github), mature and stable

    - a fork of MySQLdb, adding python3 support, new features and bugfixes.

    - drop-in replacement of MySQLdb, 100% API compatiblity, even module names
      are the same.

    - recommended by django
      https://docs.djangoproject.com/en/1.11/ref/databases/#mysql-db-api-drivers

    - python3 support

    - c extension, very fast (see reference above)

    - developed and maintained by the same group of people behind PyMySQL.

  * PyMySQL

    - popular (~3000 stars on github), mature and stable

    - pure python

    - python3 support

    - suitable for asynchronous applications (async, eventlet, gevent, etc.)

    - recommended by openstack
      https://wiki.openstack.org/wiki/PyMySQL_evaluation

    - much slow than those written as C extension. (see reference above)

      (Though MySQL Connector is a pure Python library, while MySQLdb is largely
      written in C, and we could expect that the new module is a bit slower than
      the current one, performance may actually be improved. This is because the
      new module is eventlet aware, meaning threads will be able to switch while
      waiting for I/O from a database server.
      http://specs.openstack.org/openstack/oslo-specs/specs/juno/enable-mysql-connector.html
      )

  * MySQL Connector/Python (``mysql.connector``)

    - officially supported and actively developed by Oracle

    - pure python

    - python3 support

    - suitable for asynchronous applications (async, eventlet, gevent, etc.)

    - much slower than those written as C extension, also slower than PyMySQL.
      (see references above)

  根据以上分析, 我会选择 mysqlclient 和 PyMySQL, 在同步和异步的情况下使用.

SQL language
------------
- In general, treat all identifiers (database names, table names, column names,
  etc.) and strings as case sensitive; treat SQL keywords, mysql builtin commands,
  etc. as case insensitive.

- ``SELECT`` statement

  * mysql 不支持 ``SELECT DISTINCT ON (...)``, 聚合时若要根据某列的 distinct 来
    选择行, 可以通过 ``COUNT(DISTINCT <colname>)`` 来迂回处理. 这很 hack.

- 注意 ``SELECT`` 后面的部分是 case insensitive 的.

- comment syntax: 三种注释语法

  * ``--``, 后面必须加上一个空格, line comment

  * ``#``, line comment

  * ``/* */``, block comment. 还有特殊作用, ``/*! */`` 用于在 sql 中加入 non-portable
    的 mysql extension 语句, 这样注释之外的部分仍然是 portable 的语句.

- column header 是 ``SELECT`` 的项, 它可以是表的列名字, 也可能是表达式.

- backtick (``\```) wrap 的是 identifier, 当 identifier 中不包含特殊字符时, 可以省去.

- 可以给用户分配不存在的数据库的权限. 然后这个用户可以创建这个数据库.

- ``DATE`` data type 要求的输入格式是 ``YYYY-MM-DD``.

- Comparisons on character type columns are case-insensitive. 并且这直接影响按照 char
  type 类型排序时是 case-insensitive 的. 用 ``BINARY`` 来避免这种效果. ``BINARY``
  还可以转换 regexp 的匹配成为 case-sensitive 的.

- NULL

  * The result of any arithmetic comparison with NULL is also NULL, 判断是否是 NULL
    只能用 ``IS NULL``, ``IS NOT NULL``.

  * Two NULL values are regarded as equal.

  * When doing an ORDER BY, NULL values are presented first if you do ORDER BY ... ASC
    and last if you do ORDER BY ... DESC.

- In MySQL, 0 or NULL means false and anything else means true. The default truth
  value from a boolean operation is 1.

- SQL pattern

  * ``_``: any single character, equivalent to ``?`` in shell.

  * ``%``: any number of any character, equivalent to ``*`` in shell.

- ``LIKE`` 后面的 SQL pattern 必须匹配整个字符串, 才算匹配.
  ``RLIKE`` ``REGEXP`` 后面的正则 pattern 只需字符串的任何地方匹配即可, 类似 python
  中的 ``re.search``.

- ``COUNT()`` does not count NULL values. 因此若某个列中有 NULL, ``count(<col>)``
  不等于 ``count(*)``.

- group

  * If you name columns to select in addition to the ``COUNT()`` value, a ``GROUP BY``
    clause should be present that names those same columns. This can be enforced by
    the ``ONLY_FULL_GROUP_BY`` SQL mode.

  * ``select`` 时, 原始数据集本身构成一个 group, 所以可以在这个组上直接使用聚合函数,
    生成一行结果.

- Joining tables

  * When combining (joining) information from multiple tables, you need to specify
    how records in one table can be matched to records in the other.

  * Sometimes it is useful to join a table to itself, if you want to compare records
    in a table to other records in that same table.

- ``AUTO_INCREMENT`` field

  对于 auto increment field, 插入 0 或 NULL 时写入自增的值. 若设置了
  ``NO_AUTO_VALUE_ON_ZERO``, 则插入 0 就是插入 0.

  When you insert any other value into an ``AUTO_INCREMENT`` column, the column is
  set to that value and the sequence is reset so that the next automatically
  generated value follows sequentially from the largest column value.

  You can retrieve the most recent automatically generated ``AUTO_INCREMENT``
  value with the ``LAST_INSERT_ID()`` SQL function.

- 一个表必须有一个或者一组 unique key 可以唯一识别不同的资源实例, 否则无法完全
  避免多个 session 同时创建同一个实例时导致的重复 (race condition).
