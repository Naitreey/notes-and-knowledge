- error logging

  mysqld 根据 ``--log-error`` option 来决定错误日志输出. 若这个选项没有设置,
  日志写到 stderr. 此时 ``log_error`` system variable 为 ``stderr``.

- 处于安全考虑, ``local_infile`` 默认是 OFF, 需要在 mysql client 和 mysqld
  同时开启.

SQL Language Structure
======================

literal values
--------------

String literals
^^^^^^^^^^^^^^^
::

  [_<charset>] <string> [COLLATE <collation>]

- string literal is enclosed in single or double quotes.

  * A ' inside a string quoted with ' may be written as ''.

  * A " inside a string quoted with " may be written as "".

  * Or ' " can be escaped by backslash.

- Quoted strings placed next to each other are concatenated to a single string.

- A string literal can specify its charset (introducer) and/or collation.
  如果两个都没有指定, fallback 至 ``character_set_connection`` and
  ``collation_connection``.

- backslash escapes.
  
  * For unrecognized escape sequences, backslash is ignored.

Numeric literals
^^^^^^^^^^^^^^^^
- exact-value literals. having integer part and/or fractional part,
  may be signed.
  
- approximate-value literals. in scientific notation with a mantissa
  and exponent.

hex literals
^^^^^^^^^^^^
::

  [_<charset>] X'<hex>' [COLLATE <collation>]
  [_<charset>] 0x<hex> [COLLATE <collation>]
    
- ``0x`` can not be written as ``0X``. letter cases does not matter.

- hex literal can be a binary string or number. To ensure numeric treatment of
  a hexadecimal literal, use it in numeric context.

- hex literal as a binary string, has default charset ``_binary``.

- introducer can be useful to prevent hex literal being treated as number.

bit-value literals
^^^^^^^^^^^^^^^^^^
::

  [_<charset>] B'<bin>' [COLLATE <collation>]
  [_<charset>] 0b<bin> [COLLATE <collation>]
  
- By default, a bit-value literal is a binary string. In numeric contexts,
  MySQL treats a bit literal like an integer.

- bit literal as a binary string, has default charset ``_binary``.

boolean literals
^^^^^^^^^^^^^^^^
::

  TRUE
  FALSE

- in any letter case.

null values
^^^^^^^^^^^
::

  NULL

- in any letter case.

- In collation order, NULL precedes any other values.

Date and Time literals
^^^^^^^^^^^^^^^^^^^^^^
::

  [DATE|TIME|TIMESTAMP] 'timestr'
  { d|t|ts 'timestr' }

- format.

  * DATE. 'YYYY-MM-DD', 'YY-MM-DD', YYYYMMDD, YYMMDD or digits as integer. Any
    punctuation character may be used as the delimiter.

  * TIMESTAMP. 'YYYY-MM-DD HH:MM:SS', 'YY-MM-DD HH:MM:SS', 'YYYYMMDDHHMMSS',
    'YYMMDDHHMMSS' or digits as integer. Any punctuation character may be used.
    The date and time parts can be separated by T rather than a space. Value
    can include a trailing fractional seconds part in up to microseconds (6
    digits) precision.

  * TIME. 'D HH:MM:SS', '[H]HH:MM:SS', '[H]HH:MM', 'D HH:MM', 'D HH', 'SS',
    '[H]HHMMSS', or digits as integer. A trailing fractional seconds part is
    recognized. The ``D`` and ``HHH`` part because the TIME type can be used
    not only to represent a time of day (which must be less than 24 hours), but
    also time interval.

- TIMESTAMP produces DATETIME value.

identifiers
-----------
- Common uses of identifiers: variable name, the name of database, table,
  index, column, alias, view, stored procedure, partition, tablespace, resource
  group.

- An identifier may be quoted with backtick or unquoted. If an identifier
  contains special characters or is a reserved word, you must quote it whenever
  you refer to it.

- To escape a backtick in quoted identifier: use double tick.

- Identifiers are converted to Unicode internally. identifier length
  以字符数目计算.

- Valid identifier characters:

  * U+0001 - U+FFFF (unicode point: 1-65535)

  * NULL (U+0000) is not permitted in identifier.

  * Database, table, and column names cannot end with space characters.

- qualified identifiers: consisting of identifiers separated by ``.``
  qualifier, indicating a namespace hierarchy.

- identifier case sensitivity.

  * databases, tables, triggers corresponds to file in file system, therefore
    case sensitivity is determined by its underlying file system.

  * column, column alias, index, stored routine, event, resource group names
    are not case-sensitive.

  * table aliases are case-sensitive on Unix.

- Nonreserved keywords are permitted as identifiers without quoting. Reserved
  words are permitted as identifiers if quoted.

- Special rules for builtin function names.
  
  * To use builtin function's name as a function call in an expression, there
    must be no whitespce between the name and the argument list.

  * To use the function name as an identifier, it must not be followed
    immediately by a parenthesis.

keywords and reserved words
---------------------------
- Keywords are words that have significance in SQL. Keywords may be reserved
  or nonreserved.

- ``information_schema.keywords`` table lists all keywords and their reservation
  state.

user variables
--------------
::

  @<var>

- If var name contains unusual characters, it must be quoted ``@'var'`` ``@"var"``
  ``@`var```.

- user vars are session-specific.

- Var names are case-insensitive.

- variable assignments:

  * SET statement.

  * ``:=`` operator in other statements.

- only limited types of value can be assigned to user variables.

- As a general rule, other than in SET statements, you should never assign a
  value to a user variable and read the value within the same statement.
  Because the order of evaluation is undefined.

comment syntax
--------------
- 三种注释语法

  * ``--``, 后面必须加上一个 whitespace char. line comment.

  * ``#``, line comment.

  * ``/* */``, block comment.
    
- MySQL extension code::

    /*![mysql-version] <code> */
    mysql-version := XYYZZ

  These enable you to write code that includes MySQL extensions, but is still
  portable.  Optional mysql version number specify the minimum version of mysql
  on which the code is executed. 版本号符合上述格式: X, Y, Z 分别是 major,
  minor, patch level. e.g., 5.1.10 == 50110.

- optimizer hints::

    /*+ <hints> */
 
Data types
==========

- general attributes.

  * DEFAULT.
    
    - default should normally be a constant. 但 CURRENT_TIMESTAMP for DATETIME,
      TIMESTAMP 是个例外.

    - 如果一个列在定义时没有指定 DEFAULT attribute. mysql 根据该列是否可以接受
      NULL 来设置 DEFAULT NULL 或者不设置 DEFAULT. 但如果该列是 primary key,
      会设置 NOT NULL.

      因此, 一个列的定义中的默认值只会有三种情况: 明确指定的 non-NULL DEFAULT,
      明确或非明确指定的 NULL DEFAULT, 没有 DEFAULT.

    - 插入时对某列使用默认值的方法:
      
      * 不指定该列的值.

      * 使用 ``DEFAULT[(col)]`` 明确指定插入当前列或指定列的默认值.

      In strict sql mode, 对于没有 DEFAULT 的列, 会报错.

- storage requirements.

  * max row size: 64KB. Excluding BLOB, TEXT, JSON columns, 它们单独存储, 只
    在行内添加必要信息.

Numeric types
-------------
- mysql 支持给 integer types 添加 ``(M)`` attribute 以设置 "display width".
  还有 ZEROFILL attribute. THIS IS CRAZY. DON'T DO THIS. SAVE YOUR FUCKING ASS.

- data type attributes.

  * UNSIGNED.
    
    - integer types: only nonnegative values are allowed. 所有 bytes 用 unsigned
      binary arithmetics 存储, 最大值为 signed 情况的两倍.

    - floating-point and fixed-point types: only nonnegative values are allowed.
      但存储方式不变, 最大值不变.

  * AUTO_INCREMENT. integer types and floating-point types can be
    auto-incremented. AUTO_INCREMENT field 一般同时要求 NOT NULL.

    插入 NULL, 0, DEFAULT 都会自动递增序列值.
    
    Sequence begins with 1. 若插入任何大于当前最大序数的数字,  the column is
    set to that value and the sequence is reset so that the next automatically
    generated value follows sequentially from the inserted value.

    一个表里只能有一个列是 auto-incremented, 并且该列必须有 index.

    You can retrieve the most recent automatically generated ``AUTO_INCREMENT``
    value with the ``LAST_INSERT_ID()`` SQL function.

- In non-strict sql mode, out-of-range values are clipped to the appropriate
  endpoint of the column data type range and the resulting value are stored.

integer types
^^^^^^^^^^^^^

TINYINT
"""""""

- 1 byte.

- BOOL, BOOLEAN are synonyms for TINYINT(1). 所以实际上 BOOL 可以存 0-255
  的数据. FUCKED UP.

- Which data type to use for BOOL, BOOL a.k.a. TINYINT(1) or BIT(1)?

  * BIT(1) 可以严格限制数据.

  * TINYINT(1) 的默认输出就是 1, 0 integer. 无需额外转换, 与 true/false
    一致. BIT(1) 可能需要应用去额外转换.

SMALLINT
""""""""

- 2 byte.

MEDIUMINT
""""""""""

- 3 byte.

INT
""""

- 4 byte.

- synonym: INTEGER.

BIGINT
""""""

- 8 byte.

- SERIAL is an alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE.

fixed-point types
^^^^^^^^^^^^^^^^^
- fixed-point data types are used when it is important to preserve exact
  precision.

DECIMAL
""""""""
- fixed-point exact number.

- DECIMAL(M, D). M is precision, D is digits after decimal point.
  M <= 65, D <= 30. default M is 10, D is 0.

- synonyms: DEC, NUMERIC, FIXED.

floating-point types
^^^^^^^^^^^^^^^^^^^^

FLOAT
""""""
- FLOAT(M, D). M is the total number of digits and D is the number of digits
  following the decimal point. default is hardware-dependent.

- 4 bytes.

DOUBLE
""""""

- DOUBLE(M, D). default is hardware-dependent.

- 8 bytes.

- synonym: DOUBLE PRECISION.

bit-value types
^^^^^^^^^^^^^^^

BIT
""""
- BIT(M). M-bit numbers.

- 1 <= M <= 64.

- storage. M bits 所需的整数个 bytes.

String types
------------

- The length in data type definition specifies length in character units.

- In non-strict sql mode, for string exceeding the column's max length, it
  is truncated to fit and warning is produced. In strict sql mode, the
  operation errors out.

- data type attributes.

  * CHARACTER SET, CHARSET.

  * COLLATE

nonbinary and binary strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CHAR
""""
::

  [NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]

- fixed-length string. length fixed to ``M``.
  
- 0 <= M <= 255. default is 1.

- When stored, the string is always right-padded with spaces to the specified length.

- When retrieve, trailing spaces are removed.

- synonym: CHARACTER.

- storage: M×W bytes, where W is bytes required for the maximum-length
  character in the character set. 

VARCHAR
""""""""
::

  [NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]

- variable-length string. Max length is M.

- 0 <= M <= 65535. 注意 row size 限制为 64KB, 所以有效上限还受这个影响.

- string is prefixed by 1-2 byte length in bytes.

- 存储时, string 只占用所需的空间 (+length), 不像 CHAR 那样会 padding 至 M 长度.
  无论有无 trailing spaces, 都会按照实际情况存放.

- CHAR vs VARCHAR. When to use which?[SOCharVarchar]_

  * You *can* use CHAR if all your strings are of *the same length*. 如果满足这个
    前提条件, using CHAR can be more space efficient (no length prefix) and 
    faster (optimization). 

  * 注意 CHAR's whitespace stripping behavior may cause problem.

  * 使用 multi-byte charset 时, VARCHAR 在空间利用率上高效很多. 对于 CHAR 每个字符
    位置都需要占用 charset 单个字符所需最大空间, 所以如果字符串长度不一致, 相对
    VARCHAR 会浪费更多空间. 对于 VARCHAR, 不同长度的字符相邻存放, 不需要给每个
    分配固定的长度.

  * VARCHAR in general is more preferable, because usually strings are not of
    the same length and may vary significantly. Therefore it can be more space
    efficient in general cases.

BINARY
""""""
::

  BINARY(M)

- Similar to CHAR, for binary strings.

- M specifies length in bytes.

- ``binary`` character set and collation, and comparison and sorting are based
  on the numeric values of the bytes in the values.

- The BINARY and VARBINARY data types are distinct from the CHAR BINARY and
  VARCHAR BINARY data types. For the latter types, the BINARY attribute does
  not cause the column to be treated as a binary string column. Instead, it
  causes the binary (_bin) collation for the column character set to be used,
  and the column itself contains nonbinary character strings rather than binary
  byte strings.

- Values are right-padded with 0x00 on insert, and no trailing bytes are
  removed on select.
  
- BINARY vs VARBINARY. If the value retrieved must be the same as the value
  specified for storage with no padding, it might be preferable to use
  VARBINARY or one of the BLOB data types instead.

VARBINARY
""""""""""

- similar to VARCHAR for binary strings. See also BINARY_.

text and binary data
^^^^^^^^^^^^^^^^^^^^

- blob types use binary character set and collation.

- Value exceeding max length is truncated or errored out based on sql mode.

- no whitespace padding or stripping.

- If a ``*TEXT`` column is indexed, index entry comparisons are space-padded at
  the end. ``*BLOB`` columns does not do this.

- Indexes on BLOB and TEXT columns must specify index prefix length.

- BLOB and TEXT columns can not have non-NULL DEFAULT value.

- Only the first ``max_sort_length`` bytes of the column are used when sorting.

- Instances of BLOB or TEXT columns in the result of a query that is processed
  using a temporary table causes the server to use a table on disk rather than
  in memory because the MEMORY storage engine does not support those data types.
  Use of disk incurs a performance penalty, so *include BLOB or TEXT columns in
  the query result only if they are really needed*.

- Each BLOB or TEXT value is represented internally by a separately allocated
  object (因为可能很大, 远大于 row size 64KB). This is in contrast to all other
  data types, for which storage is allocated once per column when the table is
  opened.

- Use TEXT and BLOB types only when necessary, VARCHAR and VARBINARY are more
  preferable if possible. 这主要是因为效率因素. 涉及 TEXT, BLOB 的列不能使用
  内存临时表.

TINYTEXT
""""""""
::

  TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]

- A TEXT column.
 
- storage: limited to 255 bytes.

- stored with 1-byte length prefix.

TEXT
""""
::

  TEXT ...

- text column
 
- storage: limited to 65535 bytes.

- stored with 2-byte length prefix.

MEDIUMTEXT
""""""""""
::

  MEDIUMTEXT ...

- text column
 
- storage: limited to 2^24-1 bytes.

- stored with 3-byte length prefix.

LONGTEXT
""""""""
::

  LONGTEXT ...

- text column
 
- storage: limited to 2^32-1 bytes.

- stored with 4-byte length prefix.

TINYBLOB
""""""""

BLOB
""""

MEDIUMBLOB
""""""""""

LONGBLOB
""""""""

ENUM
^^^^
::

  ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

- 从多个选项中选择一个保存. 每个选项值必须是 string literal, 不能是 expression.

- 元素字符串的 trailing whitespaces are stripped.

- 内部以 integer 方式保存. enumeration 中的元素值从 1 开始递增.

- 最多 65535 enumeration, 每个 element 的长度最多 255 chars.

- enum values is cast to its internal number in numeric contexts.

- 若给 enum 列插入 number, 会作为内部 integer 值保存.

- If strict SQL mode is enabled, attempts to insert invalid ENUM values result
  in an error. In non-strict sql mode, invalid value results the empty stirng is
  inserted as a special error value, whose internal integer value is 0.

- ENUM values are sorted based on their internal numbers, with the empty string
  sorting before nonempty strings. 若希望数值与 enum value 值顺序一致, 可以通过
  在定义时保证 ENUM list in alphabetic order, 或者在排序时按照 enum value 来排序
  ORDER BY CAST(col AS CHAR).

- storage. 1-2 bytes.

SET
^^^
::

  SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

- 从多个选项中选择 0 个或多个保存.

- 元素字符串的 trailing whitespaces are stripped.

- 若选择 0 个元素, 则输入值为空字符串 "".

- SET column values that consist of multiple set members are specified as a
  string with members separated by commas. 因此 set member itself should not
  contain commas.

- If strict SQL mode is enabled, attempts to insert invalid SET values result
  in an error.

- 最多 64 个元素. 每个元素最长 255 字符.

- 内部以 integer 方式保存. 每个元素对应 integer 上的一个 bit. 选中则 set bit,
  没选中则 clear bit.

  * 元素的定义顺序对应着 bits 从低位至高位的顺序.
  
  * 最长 64 个元素对应 64 bit 即一个 long int.

  * 若插入整数, 则相应的二进制形式的 bits 对应着选中了哪些元素.

- For a value containing more than one SET element, it does not matter what
  order the elements are listed in when you insert the value. It also does not
  matter how many times a given element is listed in the value. When the value
  is retrieved later, each element in the value appears once, with elements
  listed according to the order in which they were specified at table creation
  time.

- SET values are sorted based on internal numerical value. NULL values sort
  before non-NULL SET values.

- test element in set:
  
  * ``FIND_IN_SET()``.

  * bitwise ``&`` operator with proper numeric value.

- storage. 1,2,3,4,8 bytes.

Date and time types
-------------------

- For input, date and time values can be in any date and time literal format;
  for output, they are outputted in standard format.

- Values are converted to number (integer or decimal as appropriate) in
  numerical context. 别指望能转换回来. Oh fuck.

- zero date or time values are dummy values. Invalid DATE, DATETIME, or
  TIMESTAMP values are converted to the “zero” value of the appropriate type.
  Zero values can not be used in NO_ZERO_DATE sql mode.

- fractional seconds. 定义列时可指定 ``(M)`` 部分, M 为 0-6 位 fractional
  seconds. M default 0.

- conversion between date and time types.

  * DATE -> DATETIME, TIMESTAMP. add '00:00:00'.

  * DATE -> TIME. becomes '00:00:00'.

  * DATETIME, TIMESTAMP -> DATE. keep date part, with rounding effect.

  * DATETIME, TIMESTAMP -> TIME. cut out date part, keep time part.

  * TIME -> DATETIME, TIMESTAMP. CURRENT_DATE is used for date part.
    The TIME is interpreted as time interval.

  * TIME -> DATE. ditto with time part cut off.

- attributes.

  * ``DEFAULT <value>`` . value 可以设置当前时间特殊值
    CURRENT_TIMESTAMP[()]/NOW()/LOCALTIME[()]/LOCALTIMESTAMP[()]. 这个特殊值
    可用于自动设置创建时间.

  * ``ON UPDATE CURRENT_TIMESTAMP|...``. auto-update column value to current
    time when the value of any other column in the row is changed from its
    current value. 如果对该行的修改没有导致任何变化, 时间值不会更新, 此时若要
    更新, 需手动更新.

  以上 attributes 只有 DATETIME and TIMESTAMP 能用.

DATE
^^^^
- date only.

- displayed in YYYY-MM-DD format.

DATETIME
^^^^^^^^

- DATETIME 适合存储一个特定的、可能固定不变的时间.

- date and time.

- display format: ``YYYY-MM-DD HH:MM:SS[.fraction]``

TIMESTAMP
^^^^^^^^^

- TIMESTAMP 适合用于存储具有实时性的、可能经常变动的时间, 这是时间戳的目的.
  例如 created time, modified time 等. 这是与 DATETIME 的区别.

- TIMESTAMP column have no automatic properties unless they are specified
  explicitly. with this exception: If the ``explicit_defaults_for_timestamp``
  system variable is disabled, the first TIMESTAMP column has DEFAULT
  CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP if neither is specified
  explicitly.

- stored as the number of seconds since the epoch.

- MySQL converts TIMESTAMP values from the current time zone (``time_zone``
  system variable) to UTC for storage, and back from UTC to the current time
  zone for retrieval. 这让 TIMESTAMP 具有绝对时间意义, 这是相对于 DATETIME
  更适合做时间戳的另一个性质.

- factional seconds part up to microseconds precision: 6 digits.

- range: 1970 - 2038.

- NULL value. If the ``explicit_defaults_for_timestamp`` system variable is
  disabled (default), TIMESTAMP columns by default are NOT NULL, cannot contain
  NULL values. You can initialize or update any TIMESTAMP (but not DATETIME)
  column to the current date and time by assigning it a NULL value (这并不需要
  设置 ON UPDATE CURRENT_TIMESTAMP). 这保证了 timestamp 一定会更新, 避免了 ON
  UPDATE CURRENT_TIMESTAMP 的问题. 这又是一点比 DATETIME 适合做时间戳的性质.

  To permit a TIMESTAMP column to contain NULL, explicitly declare it with the
  NULL attribute.

TIME
^^^^

- display format: ``[H]HH:MM:SS[.fraction]``

- time 除了可以作为 time of day 使用, 还可以作为 interval 使用. 但是
  这个 interval 比较小, 最多 999 hours. 需要比较大的 interval 最好还是
  使用一系列的 INT 类型.

YEAR
^^^^

- A year in four-digit format.

- display format: YYYY.

- stored in 1 byte. ranging 1901-2155, and 0000.

Geospatial types
-----------------

- geometry types. A geometry-valued SQL column is implemented as a column that
  has a geometry type.

- a geographic/geospatial feature. anything in the world that has a location.

  * An entity.

  * a space.

  * a definable location.

- SPATIAL indexes can be created on NOT NULL spatial columns. But the spatial
  index can be used by optimizer only if the column definition contains SRID
  attribute.

- attributes.

  * SRID. 指定该列 geometry value 所属的 spatial reference system (SRS).

- GEOMETRY types can not have non-NULL DEFAULT.

- storage. 4 bytes for SRID + WKB representation of geometry value.

- OpenGIS Geometry Model.

JSON type
---------

- Automatic JSON data validation.

- Optimized binary storage format and manipulation.

  * quick read access to individual subobjects or values.

  * inplace update of JSON document. 

- JSON column can not have non-NULL DEFAULT value.

- index. JSON column can not be indexed directly. You can create an index on a
  generated column that extracts a scalar value from the JSON column.

- 构建 JSON 的方法.

  * 字符串 JSON literal 在 JSON value context 下解析为 JSON value.

  * 使用 JSON_ARRAY(), JSON_OBJECT() 等构建.

- JSON 字符串形式输入. MySQL parses any string used in a context that
  requires a JSON value, and produces an error if it is not valid as JSON.  In
  JSON value context, string is converted to use ``utf8mb4`` character set and
  ``utf8mb4_bin`` collation.

- Normalization. JSON 输入值在解析时, 需要 normalized. 例如允许输入中包含重复
  的 object keys, 但 normalizing object 时 last duplicate key wins.

- JSON merge. 两种算法.

  * JSON merge preserve. For duplicate keys, retain all values.

  * JSON merge patch. For duplicate keys, retain the last value.

  具体行为.

  * merge arrays. preserve: arrays are concatenated. patch: select only the last
    array.

  * merge objects. preserve: values of dup keys are combined into an array.
    patch: retain the last value.

  * values that is neither array nor object is autowrapped in an array. For patch,
    the array wrapper may be dropped during output.

- JSON path expression. used for extraction and update.

  * ``$`` representing the JSON doc.

  * ``.<key>`` key reference. If key is not valid identifier, must be double-quoted.

  * ``[N]`` index reference.

  * ``[M to N]`` slice, M to N inclusive. ``last`` is rightmost index. relative
    addressing is supported ``{+|-}offset``.

  * ``.*`` gets value of all keys of a json object.

  * ``[*]`` gets all elements of a json array.

  * ``[prefix]**[suffix]`` get values of all matching paths, paths can be multilevel.

  * nonexistent path evaluates to NULL.

- inplace update 要求使用 JSON_SET, JSON_REPLACE, JSON_REMOVE functions. direct
  column assignment does not use inplace update.

  * JSON_SET replace value on existing paths and add new value on nonexisting paths.

  * JSON_INSERT add new but not replace existing.

  * JSON_REPLACE replace but not add.

  * JSON_REPLACE remove paths.

- JSON value comparison and ordering.

- JSON functions.

  * JSON_STORAGE_SIZE()

  * JSON_SET(), JSON_INSERT(), JSON_REPLACE(), JSON_REMOVE()

  * JSON_STORAGE_FREE()

  * JSON_TYPE()

  * JSON_ARRAY(), JSON_OBJECT()
   
  * JSON_MERGE_PRESERVE(), JSON_MERGE_PATCH()

  * JSON_VALID()

- JSON operators.

  * extraction operator: ``->``.

  * unquoting extraction operator: ``->>``.

- storage. 基本相当于 LONGBLOB. 即所需存储空间基本相当于把 JSON stringified
  形式所需存储. 但有一些为了便于更新和查询等的额外 metadata 带来的 overhead.

SQL statements
==============

Data Definition Language (DDL)
------------------------------

CREATE DATABASE
^^^^^^^^^^^^^^^
::

  CREATE DATABASE [IF NOT EXISTS] <name>
      [[DEFAULT] CHARACTER SET [=] charset_name]
      [[DEFAULT] COLLATE [=] collation_name]

- privilege: CREAT for the specified database.

- database definition is recorded in INFORMATION_SCHEMA.SCHEMATA.

ALTER DATABASE
^^^^^^^^^^^^^^
::

  ALTER DATABASE [<name>]
      alter_spec ...

  alter_spec:
      [DEFAULT] CHARACTER SET [=] charset_name
    | [DEFAULT] COLLATE [=] collation_name

- privilege: ALTER privilege on the database.

- If database name is omitted, use current default database.

Data Manipulation Language (DML)
--------------------------------

SELECT
^^^^^^

- Each select expression is evaluated only when sent to the client. This means
  that in a HAVING, GROUP BY, or ORDER BY clause, referring to a variable that
  is assigned a value in the select expression list does not work.

.. -------------------------------

- SQL pattern

  * ``_``: any single character, equivalent to ``?`` in shell.

  * ``%``: any number of any character, equivalent to ``*`` in shell.


.. -------------------------------


  * mysql 不支持 ``SELECT DISTINCT ON (...)``, 聚合时若要根据某列的 distinct 来
    选择行, 可以通过 ``COUNT(DISTINCT <colname>)`` 来迂回处理. 这很 hack.

- 可以给用户分配不存在的数据库的权限. 然后这个用户可以创建这个数据库.

- NULL

  * The result of any arithmetic comparison with NULL is also NULL, 判断是否是 NULL
    只能用 ``IS NULL``, ``IS NOT NULL``.

  * Two NULL values are regarded as equal.

  * When doing an ORDER BY, NULL values are presented first if you do ORDER BY ... ASC
    and last if you do ORDER BY ... DESC.

- In MySQL, 0 or NULL means false and anything else means true. The default truth
  value from a boolean operation is 1.

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

- 一个表必须有一个或者一组 unique key 可以唯一识别不同的资源实例, 否则无法完全
  避免多个 session 同时创建同一个实例时导致的重复 (race condition).

transaction statements
----------------------
- A transaction is an atomic operation that can be committed or rolled back.
  All changes made in a transaction are applied atomically or none applied.

- InnoDB transactions have ACID properties -- atomicity, consistency,
  isolation, and durability.

- autocommit: causes an implicit commit operation after each SQL statement.
  Default on.
 
  enable or disable autocommit for current session.::

    SET autocommit = {0 | 1}

START TRANSACTION, BEGIN
^^^^^^^^^^^^^^^^^^^^^^^^
:: 
  
  START TRANSACTION [WITH CONSISTENT SNAPSHOT | READ WRITE | READ ONLY] ...
  BEGIN

- start a new transaction.

- START TRANSACTION is prefered as it's standarded and accept more options.

- During a transaction, autocommit remains disabled until the end of
  transaction with ``COMMIT`` or ``ROLLBACK``. Then it reverts to its
  previous state.

  注意这并不能从 session variable ``autocommit`` 看出来. 在 transaction
  中, autocommit 变量值不会修改.

- modifiers.

  * 

COMMIT
^^^^^^

ROLLBACK
^^^^^^^^

Character set and collation
===========================

overview
--------

character set
^^^^^^^^^^^^^
- available character sets 保存在 ``INFORMATION_SCHEMA.CHARACTER_SETS`` table.
  Can be queried by SHOW CHARACTER SET.

- mysql stores metadata in ``character_set_system``, which is always UTF-8.

collation
^^^^^^^^^
- available collations 保存在 ``INFORMATION_SCHEMA.COLLATIONS`` table.
  Can be queried by SHOW COLLATION.

- collation naming convention::

    <charset>[_<attr>]...

  attributes:

  * language-specific attribute includes a locale code or language name.

  * ``_ai``, accent insensitive; ``_as``, accent sensitive,
    ``_ci``, case insensitive; ``_cs``, case sensitive; ``_ks``, kana
    sensitive; ``_bin``, binary.

- For the binary collation of the binary character set, comparisons are based
  on numeric byte values. For the _bin collation of a nonbinary character set,
  comparisons are based on numeric character code values, which differ from
  byte values for multibyte characters.

character set repertoire
^^^^^^^^^^^^^^^^^^^^^^^^

- A string expression has repertoire attribute, which can be:

  * ASCII.

  * UNICODE.

- The repertoire for a string constant depends on string content and may differ
  from the repertoire of the string character set. 例如一个 UTF-8 character set
  的 string 如果只有 ASCII 字符, 则 repertoire 是 ASCII. 

settings at different levels of data storage
--------------------------------------------
- Character set and collation can be set at server, database, table, column
  levels.

- 在任何一层, 如果没有明确设置 collation, 将使用 character set 的默认 collation;
  如果明确设置了 collation 但没设置 character set, 将使用该 collation 所属的
  character set.

server level
^^^^^^^^^^^^

- defined by ``character_set_server``, ``collation_server``.

- server level 的 charset, collation 的唯一用途是作为创建数据库时的
  default 值.

database level
^^^^^^^^^^^^^^

- defined by CREATE DATABASE or fallback to server-level settings.

- current default database's values are character_set_database and
  collation_database.

- database level 的 charset, collation 的唯一用途是作为创建表时的
  default 值.

table level
^^^^^^^^^^^

- defined by CREATE/ALTER TABLE or fallback to database-level settings.

- table level 的 charset, collation 的唯一用途是作为 string type columns
  的 default 值.

column level
^^^^^^^^^^^^

- defined by CHAR, VARCHAR, TEXTs, ENUM, SET definition.

- 如果修改某列的 charset & collation 配置, 保存的数据会进行映射至新的
  charset & collation. 若目标 charset 不包含所需全部字符, 可能 data
  corrupt.

settings for connection
-----------------------
- data from client to server: ``character_set_client``

- 服务端接收到数据后, It converts statements sent by the client from
  character_set_client to ``character_set_connection``. 这步转换只对
  string literals 之间的比较有意义.

- string 数据转换成 column 所需 charset 并存储.

- data from server to client: ``character_set_results``

- mysql client programs 对 3 个 connection-related charset 的设置.

  * 用户指定, 通过客户端支持的方式, 例如 ``--default-character-set``
    参数, API 参数, 或者直接执行 SET NAMES.

  * 检测环境变量 LANG, LC_ALL. UTF-8 maps to utf8mb4.

  * default utf8mb4.

SQL statements
--------------

SHOW CHARACTER SET
^^^^^^^^^^^^^^^^^^
::

  SHOW CHARACTER SET [LIKE <pattern> | WHERE <expr>]

- show available character sets.

- ``Maxlen`` column 是单个字符所需最大 bytes.

SHOW COLLATION
^^^^^^^^^^^^^^
::

  SHOW COLLATION [LIKE <pattern> | WHERE <expr>]

- Compiled column indicates whether the character set is compiled into the
  server.

- Sortlen is related to the amount of memory required to sort strings expressed
  in the character set.

SET NAMES
^^^^^^^^^
::

  SET NAMES {<charset> [COLLATE <collation>] | DEFAULT}

- indicates to server what character set the client will use to send SQL
  statements to the server and what character set the server should use for
  sending results back to the client.

- set ``character_set_client``, ``character_set_connection``,
  ``character_set_results`` to the given character set.

- ``collation_connection`` is also set implicitly to the default
  collation of the given charset, or explicitly by COLLATE clause.

- DEFAULT can be used to restore settings to their default.

SET CHARACTER SET
^^^^^^^^^^^^^^^^^
::

  SET CHARACTER SET {<charset> | DEFAULT}

- set character_set_client and character_set_results are set to the given
  character set, and character_set_connection to the value of
  character_set_database.

- SET NAMES vs SET CHARACTER SET. 两者的区别仅在于后者将 string literals 
  之间的比较置于 server charset 之下进行. 前者则置于指定的 charset 下进行.
  一般使用 SET NAMES.

configuration variables
-----------------------

connection
^^^^^^^^^^
- ``character_set_client``. 向服务端声明客户端向服务端发送请求使用的 charset.
  该参数值 一般由 client 在连接上 server 后在 session-scope 进行声明, 目的是让
  server 知道该怎么解析客户端的请求. server 端的 global-scope 配置主要用于 when
  the client-requested value is unknown or not available.

- ``character_set_results``. 告诉服务端向客户端发送结果应使用的 charset.

- ``character_set_connection``. 这个 charset 只对 string literal 之间的比较有
  价值, 对其他情况都用不着.

- ``collation_connection``. collation of ``character_set_connection``.

data
^^^^
- ``--character-set-server``, ``character_set_server``. 服务端的默认 charset.

- ``--collation-server``, ``collation_server``. collation of ``character_set_server``.

- ``character_set_database``. charset of the default database of current
  session. If no default database, use the same value as ``character_set_server``.
  This variable is readonly.

- ``collation_database``. collation of ``character_set_database``.

metadata
^^^^^^^^
- ``character_set_system``. 服务端用于存储 metadata. always utf8.

filesystem
^^^^^^^^^^
- ``character_set_filesystem``. The server's file system character set. Used to
  interpret string literals that refer to file names. Filenames provided by
  client is converted from ``character_set_client`` to ``character_set_filesystem``
  before opening files. Default is ``binary``, no conversion occurs.

Character sets
--------------

utf8mb3
^^^^^^^
- Use max 3-bytes for one char. only support characters in BMP.

utf8mb4
^^^^^^^
- Use max 4-bytes for one char. support complete Unicode character sets. BMP +
  supplementary characters.

- For BMP characters, utf8mb4 and utf8mb3 have identical storage
  characteristics: same code values, same encoding, same length.

- For supplementary characters, utf8mb4 requires 4 bytes.

convert utf8mb3 to utf8mb4
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- mysql 8.0+ 默认的 charset 就是 utf8mb4 了. 省去了麻烦.
  但在此之前的版本, 需要修改.

- 讨论:
  
  * 数据: 对于 string type columns, utf8mb3 -> utf8mb4 对数据不会造成影响, 因为
    BMP 内的字符编码两个 charset 是相同的.

- 表结构方面可能需要调整. 注意检查以下几点, 若存在相应问题, 需要先进行调整:
 
  * 由于 row size 64KB 限制, 在行内保存的字符串类型列 CHAR, VARCHAR 等能保存
    的最大字符数目在 ut8mb4 时减少了. 检查列定义有没有超过行长度上限. 若超过,
    需要修改列定义, 减小长度; 或修改为 TEXT types, 不在行内保存.

  * 对于 TEXT types, 由于最大长度固定, 若要求必须能保存大于某个长度的字符串,
    但在 utf8mb4 下容不下, 则需要修改定义使用更大的 TEXT 类型.

  * 由于索引长度上限是固定的 bytes 值 (根据 row format 不同可能是 767 bytes or
    3072 bytes). 所以可索引的字符数减少了. 检查须索引的列定义有没有超过索引长度
    上限. 若超过, 需要减小列长度定义或 index prefix.

- 配置文件中:
  
  * 保证 client/server 之间发送数据通过 utf8mb4 编码.
    
  * 服务端的 charset 为 utf8mb4, 即新数据库的默认编码.
    
  ::

    [client]
    default-character-set = utf8mb4
    #
    [mysqld]
    #
    # * encoding
    #
    character-set-server = utf8mb4

- 两种修改方式.

  1. 备份所有数据.

     保存一份当前数据库内的所有表定义, 用于修改后进行对比.::

       mysql -B >output-file <<EOF
       SELECT * FROM information_schema.COLUMNS
       WHERE TABLE_SCHEMA = 'enoc' order by TABLE_NAME, ORDINAL_POSITION
       EOF

     直接修改所有需要修改的表 (和所有列) 的 charset, 以及相关数据库的 default
     charset::

       ALTER TABLE <table> CONVERT TO CHARACTER SET utf8mb4; -- every table
       ALTER DATABASE <db> CHARACTER SET utf8mb4; -- every database

     自动执行第一行::

       tables=$(mysql --user root -p<pass> --host <host> -N <<<'SHOW TABLES FROM <db>')
       for tbl in $tables; do
           mysql --user root -p<pass> --host <host> <<EOF
       ALTER TABLE <db>.$tbl CONVERT TO CHARACTER SET utf8mb4
       EOF
       done

     注意 CONVERT TO CHARACTER SET 可能修改列的类型以保证在新的 charset 下,
     该列能保存和原来 charset 下至少一样多的字符数. 如要避免类型修改, 只能对
     每个列单独 MODIFY.

     对比表结构, 看看有什么被修改了.

     修改配置文件如上.

  2. mysqldump 所有数据. 修改以下 charset 定义::

       pass

     重新部署 MySQL. 设置如上配置文件. 以保证所有数据库和表都是 utf8mb4. 恢复数据.

     或者无需修改 mysqldump 文件. 恢复数据后按照 1 中的方式修改所需修改的数据库
     和表中的 charset.

Optimization
============

index
-----
- Create right index to answer the required question. 不要创建不必要的
  索引, 因为:
  
  * 在空间上索引要占用内存和存储;
   
  * 在时间上创建和更新索引需要时间, 每次 insert, update, delete 的过程中,
    都需要完成相关索引的更新.

- index's data structure.

  * B-tree: PRIMARY KEY, UNIQUE, INDEX

  * R-tree: indexes on spatial data types.

  * Inverted index: FULLTEXT.

  * Hash index.

InnoDB storage engine
=====================
InnoDB is fully transactional and supports foreign key references.

options
-------
- ``--innodb-flush-log-at-trx-commit[=#]``, ``innodb_flush_log_at_trx_commit``.

MyISAM storage engine
=====================
MyISAM is shit.

MYISAM doesn't support transactions or enforce foreign-key constraints
(inferential integrity).

Security
========

Account system
--------------

User account
^^^^^^^^^^^^
- User accounts and privileges are stored in ``mysql.user`` table.

- User accounts consist of username and hostname.
  
- Client 连接时, 必须同时 保证 username & hostname 都与服务端 ``mysql.user``
  table 中的记录匹配, 才能认证.

  若创建用户时设置的是 hostname/FQDN 而不是 IP address, 服务端在验证客户端连接
  时, 需要将 client IP address 做 reverse DNS 转换成 hostname, 再和 ``mysql.user``
  中的记录去比较. 因此若要使用 hostname/FQDN 作为 user account's hostname, 必须
  保证 reverse DNS 结果是正确的.

  因此, 一般避免使用非 IP 地址的 user account hostname.

- Max length of username: 32 chars (the byte-length of one char depends on
  character set in use).

- Passwords stored in the user table are encrypted using plugin-specific
  algorithms.

- reserved user accounts.

  * ``'root'@'localhost'``. superuser for administration.

  * ``'mysql.sys'@'localhost'``. DEFINER for sys schema objects. This decouples
    sys database from root account. locked and can not be used by client.

  * ``'mysql.session'@'localhost'``. used by plugins to access the server.
    locked and can not be used by client.

  * ``'mysql.infoschema'@'localhost'``. DEFINER for information_schema views.
    This decouples information_schema database from root account. locked and
    can not be used by client.

User privileges
^^^^^^^^^^^^^^^


Account SQL statements
^^^^^^^^^^^^^^^^^^^^^^
- Account management statements are atomic and crash safe.

CREATE USER
""""""""""""
::

  CREATE USER [IF NOT EXISTS]
    <user> [auth_option] [, <user> [auth_option]] ...
    DEFAULT ROLE <role> [, <role>] ...
    [REQUIRE {NONE | tls_option [[AND] tls_option] ...}]
    [WITH resource_option [resource_option] ...]
    [password_option] ...
    [lock_option] ...

- For each account, CREATE USER creates a new row in the mysql.user system
  table. Its columns corresponds to options specified in CREATE USER statement.

- ``user`` form: ``<user>[@<host>]``. hostname can contain ``%`` wildcard.
  If host is omitted, default is ``%``.

- Type of options that can be specified and their defaults:
  
  * authentication: default authentication plugin 
    (default_authentication_plugin system variable) and empty credentials.

    In other words, if ``auth_option`` is not specified, user is passwordless.
    
  * role: NONE.
    
  * ssl/tls: NONE.

  * resource limits: unlimited.
  
  * password management: PASSWORD EXPIRE DEFAULT PASSWORD HISTORY DEFAULT
    PASSWORD REUSE INTERVAL DEFAULT.
    
  * account locking: ACCOUNT UNLOCK.

- required privileges: CREATE USER, or the INSERT privilege for the mysql
  database.

- multiple users are created as an atomic operation -- all or none is
  succeeded.

SHOW CREATE USER
""""""""""""""""
- default options are filled. Stored password value is shown, avoiding
  disclosing original user password.

- The host name part of the account name, if omitted, defaults to '%'.

SHOW GRANTS
""""""""""""
::

  SHOW GRANTS [FOR <user-or-role> [USING role [, role] ...]]

- requires the SELECT privilege for the mysql database, except for
  current user.

- ``USING`` clause enables you to examine the privileges associated with roles
  for the user.

Server mechanism
================

Server Configurations
---------------------

server system variables
^^^^^^^^^^^^^^^^^^^^^^^
- storage: ``performance_schema.global_variables|session_variables``.

- global variables and session variables.

  * global variables. 

  * session variables. Session variables are those ultimately in effect
    for current session. They are initialized from global variables.

server SQL mode
^^^^^^^^^^^^^^^

- Server SQL mode affects SQL syntax supported by server, and data validation
  that is performed by server.

- Server SQL mode depends on ``sql_mode`` system variable in current session.
  Its value is a comma separated list of sql modes.

  default on 8.0:
  ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE,
  ERROR_FOR_DIVISION_BY_ZERO, NO_ENGINE_SUBSTITUTION.

- cmdline option: ``--sql-mode``.

- strict sql mode. controls how MySQL handles invalid or missing values in DML.
  
  Invalid value: the value has the wrong data type for the column or might be
  out of range.

  missing value: a new row to be inserted does not contain a value for a NOT
  NULL column that has no explicit DEFAULT.

  Effects of strict sql mode.

  * For invalid or missing values. Non-strict sql mode: MySQL inserts adjusted
    values and produces warnings. Strict sql mode: invalid and missing values
    are errored out.

  * For key exceeding the max key length. Non-strict sql mode: truncation of
    key to max length and produces warning. Strict sql mode: error out.

  * effects on division by zero, zero dates, zeros in dates.

  * Several statements in MySQL support an optional IGNORE keyword.  This
    keyword causes the server to downgrade certain types of errors and generate
    warnings instead.

SQL modes
"""""""""
only those useful are noted.

- ERROR_FOR_DIVISION_BY_ZERO. If not enabled, division by zero inserts NULL and
  produces no warning. If enabled, division by zero inserts NULL and produces a
  warning. If enabled with strict mode, division by zero produces an error.

  This mode deprecated and will be merged into strict mode.

- NO_AUTO_VALUE_ON_ZERO. This mode can be useful if 0 has been unfortunately
  stored in a table's AUTO_INCREMENT column.

- NO_ENGINE_SUBSTITUTION. When enabled, an error occurs and the table is not
  created or altered if the desired engine is unavailable.

- NO_ZERO_DATE. If this mode and strict mode are enabled, '0000-00-00' is not
  permitted and inserts produce an error.

  This mode deprecated and will be merged into strict mode.

- NO_ZERO_IN_DATE. whether the server permits dates in which the year part is
  nonzero but the month or day part is 0. If this mode and strict mode are
  enabled, dates with zero parts are not permitted and inserts produce an
  error.

  This mode deprecated and will be merged into strict mode.

- ONLY_FULL_GROUP_BY. rejects queries for which the select list, HAVING
  condition, or ORDER BY list refer to nonaggregated columns that are neither
  named in the GROUP BY clause nor are functionally dependent on (uniquely
  determined by) GROUP BY columns.

  Disabling ONLY_FULL_GROUP_BY is useful primarily when you know that, due to
  some property of the data, all values in each nonaggregated column not named
  in the GROUP BY are the same for each group.

- PAD_CHAR_TO_FULL_LENGTH. For CHAR columns, During retrieval, trimming does
  not occur and retrieved CHAR values are padded to their full length.

- PIPES_AS_CONCAT.

- STRICT_TRANS_TABLES. Enable strict SQL mode for transactional storage
  engines, and when possible for nontransactional storage engines.

- STRICT_ALL_TABLES. Enable strict SQL mode for all storage engines.

- TRADITIONAL. Basic principle is to give an error instead of a warning when
  inserting an incorrect value into a column. equivalent to
  STRICT_TRANS_TABLES, STRICT_ALL_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE,
  ERROR_FOR_DIVISION_BY_ZERO, and NO_ENGINE_SUBSTITUTION

management SQL statements
^^^^^^^^^^^^^^^^^^^^^^^^^

SHOW VARIABLES
""""""""""""""
::

  SHOW [GLOBAL | SESSION] VARIABLES
     [LIKE 'pattern' | WHERE expr] 

- no privileges are required.

- variables can be filtered via two clauses:

  * simple ``LIKE`` pattern filtering on variable name. Strictly speaking,
    because ``_`` is a wildcard that matches any single character, you should
    escape it as ``\_`` to match it literally.

  * ``WHERE`` clause general filtering on resulting table's column names.

- ``GLOBAL`` and ``SESSION`` modifiers.

  * default is ``SESSION``.

server logs
-----------

binary log
^^^^^^^^^^
overview
""""""""
- what is:
  contains events for database changes, including structure changes and
  data changes. Also contains time used for each changes.

- usage:

  * replication.

  * additional data recovery. After a backup has been restored, the events in
    the binary log that were recorded after the backup was made are
    re-executed.

- server performance slightly slower. But its benefits generally outweight
  the introduced minor performance decrement.

- binlog filename: ``log_bin_basename`` + numeric extension. The extension
  increases for each new log file.

- binlog size: no bigger than ``max_binlog_size`` except for during logging
  a transaction, as a transaction is written to the file in one piece,
  never split between files.

- binlog index file: contains a list of used binlog files.

- verification: the server logs the length or checksum of the event as well as
  the event itself and uses this to verify that the event was written
  correctly.

logic
""""""
- Binary logging is done immediately after a statement or transaction completes
  but before any locks are released or any commit is done. This ensures that
  the log is logged in commit order.

  For transactions: Within an uncommitted transaction, all updates (UPDATE,
  DELETE, or INSERT) that change transactional tables such as InnoDB tables are
  cached until a COMMIT statement is received by the server. At that point,
  mysqld writes the entire transaction to the binary log before the COMMIT is
  executed. Note: server handles binlog writing and commit together on receiving
  COMMIT statement. Thus ensures binlog in commit order for several concurrent
  transactions.

- For a transactional storage engine, a binary log buffer (of
  ``binlog_cache_size``) is allocated for each client to buffer statements
  (from server point of view, a new thread is opened for each client
  connection).  If a statement is bigger than this, the thread opens a
  temporary file to store the transaction. The temporary file is deleted when
  the thread ends.

  The ``Binlog_cache_use`` and ``Binlog_cache_disk_use`` status variables can
  be useful for tuning.

- data safety. By default, the binary log is synchronized to disk at each write
  (``sync_binlog=1``).
 
  At restart after a crash, after doing a rollback of transactions, the MySQL
  server scans the latest binary log file to collect transaction xid values and
  calculate the last valid position in the binary log file. The MySQL server
  then tells InnoDB to complete any prepared transactions that were
  successfully written to the to the binary log, and truncates the binary log
  to the last valid position.

  If the MySQL server discovers at crash recovery that the binary log is
  shorter than it should have been, it lacks at least one successfully
  committed InnoDB transaction (``sync_binlog!=1``). In this case, this binary
  log is not correct and replication should be restarted from a fresh snapshot
  of the master's data.

operations
""""""""""
- reset binlog::

    RESET MASTER;

- delete binlog::

    PURGE BINARY LOGS;

  During replication, old binlogs can be deleted as soon as no slaves will use
  them any longer.

- show binlog content: ``mysqlbinlog``.

formats
""""""""
- statement-based logging. actual SQL statement is logged.

  With statement-based replication, there may be issues with replicating
  nondeterministic statements.

  * advantages:

    - less data written to log. taking and restoring from backups, make
      replications can be accomplished more quickly.

    - can be used to audit database.

  * disadvantages:

    - nondeterministic statements are unsafe for statement-based logging.
      including:
      
      * A statement that depends on a UDF or stored program;

      * DELETE and UPDATE statements that use a LIMIT clause without an ORDER BY.

    - more row locks than row-based logging.

    - ...

- row-based logging. writes events to the binary log that indicate how
  individual table rows are affected.

  If you are using InnoDB tables and the transaction isolation level is
  ``READ COMMITTED`` or ``READ UNCOMMITTED``, only row-based logging can be
  used.

  With the binary log format set to ROW, many changes are written to the binary
  log using the row-based format. Some changes, however, still use the
  statement-based format. Examples include all DDL statements such as
  ``CREATE TABLE``, ``ALTER TABLE``, or ``DROP TABLE``.

  * advantages:

    - all changes can be logged, thus backup and replication. This is the 
      safest form of replication.

    - Fewer row locks are required, which thus achieves higher concurrency.

  * disadvantages:

    - more data. takes more time to log. longer backup, recover, replication
      time.

- mixed logging. statement-based logging is used by default, but the logging
  mode switches automatically to row-based in certain cases.

options
"""""""
basic binlog options.

- ``--log-bin[=pathname]``, ``log_bin``, ``log_bin_basename``.
  enable binary log. optionally with a pathname, default is ``<hostname>-bin``.
  ``pathname`` can be absolute path or a basename. For the latter, binlog is
  stored in data directory.

  If you supply an extension in the log name, the extension is silently removed
  and ignored.

- ``--log-bin-index[=filename]``, ``log_bin_index``.
  default to ``<log_bin_basename>.index``.

- ``--binlog-format={ROW|STATEMENT|MIXED}``, ``binlog_format``.
  default ROW.

- ``--sync-binlog=#``, ``sync_binlog``.
  the number of binary log commit groups to collect before synchronizing the
  binary log to disk. default 1.

  For 0, never synchronized to disk. the server relies on the operating system
  to flush the binary log's contents from time to time as for any other file. 

  For 1, all transactions are synchronized to the binary log before they are
  committed. This guarantees that no transaction is lost from the binary log,
  and is the safest option.  

  When 0 or N>1, transactions are committed without having been synchronized to
  disk. Therefore, in the event of a power failure or operating system crash,
  it is possible that the server has committed some transactions that have not
  been synchronized to the binary log. Therefore it is impossible for the
  recovery routine to recover these transactions and they will be lost from the
  binary log.

- ``--max-binlog-size=#``, ``max_binlog_size``.
  default 1G. A transaction is written in one chunk to the binary log, so it is
  never split between several binary logs.

binlog checksum.

- ``--binlog-checksum={NONE|CRC32}``
  default CRC32. causes the master to write checksums for events written to the
  binary log.

- ``--master-verify-checksum={0|1}``, ``master_verify_checksum``.
  master uses checksum to verify binlog when reading.

binlog buffer.

- ``--binlog-cache-size=#``, ``binlog_cache_size``.
  default 32768. The size of the in-memory buffer to hold changes to the binary
  log during a transaction.

- ``--max-binlog-cache-size=#``, ``max_binlog_cache_size``.
  max size of buffer for a transaction. including in-memory buffer and on-disk
  temporary file.

HA and scalability
==================
- MySQL 提供了多种 HA 方案.

  * replication.

  * group replication.

  * NDB cluster.

  * InnoDB cluster
  
Replication
-----------
- Replication 是最简单的 HA 方案.

- 模式:
  
  * one master, multiple slaves.
    
  * one-way replication: data is replicated from master to slaves.
    
  * master is write-only, slaves are read-only.

  * 同步类型:

    - asynchronous. 默认.

    - semi-synchronous.

- 特点:

  * spread read access on multiple servers for scalability, while all write
    must be performed on master. master 只用于写, 相对于同时又读又写的情况
    写的效率肯定是提高了, 但由于仍然是单机写, 所以上限明显.

  * failover.

- 两种实现.

  * binary log file position based replication.

  * global transaction identifiers (GTIDs) based replication.

- replication format.

  * Statement Based Replication (SBR).

  * Row Based Replication (RBR).

  * Mixed Based Replication (MBR).

- 注意事项.

  * master, slave 应该设置相同的 sql mode.

binary log file position based replication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mechanism
"""""""""
- Master writes updates and changes as “events” to the binary log.
  The binary log serves as a written record of all events that modify database
  structure or content (data) from the moment the server was started.

  When a slave connects, master creates a thread to send binlog contents to the
  slave (binlog dump thread is created for each slave connection). The binary
  log dump thread acquires a lock on the master's binary log for reading each
  event that is to be sent to the slave. As soon as the event has been read,
  the lock is released, even before the event is sent to the slave.

- Slaves are configured to get binary logs from the master. When a ``START SLAVE``
  statement is issued on a slave server, the slave creates an I/O thread, which
  connects to the master and asks it to send the updates recorded in its binary
  logs.

  The slave I/O thread reads the updates that the master's Binlog Dump thread
  sends and copies them to local files that comprise the slave's relay log.
  Slaves verify the retrieved binlogs by length or checksum.

  Slave create a SQL thread to read the relay log that is written by the slave
  I/O thread and execute the events contained therein.

- Slave can be configured to process only events that apply to particular
  databases or tables.

- each slave keeps binary log coordinates which represents its replication
  progress:
  
  * the binlog filename.

  * position within the file.

- each slave operates independently. Each can operates on its own pace.

- slave logs.

  * master info log. contains status and current configuration information for
    the slave's connection to the master. It is required for the recovery of
    the slave's I/O thread.

  * relay log. the events read from the binary log of the master and written by
    the slave I/O thread. Events in the relay log are executed on the slave as
    part of the SQL thread. The SQL thread automatically deletes each relay log
    file after it has executed all events in the file and no longer needs it. 

    consists of a set of numbered files containing events that describe
    database changes, and an index file that contains the names of all used
    relay log files.

    Relay log files have the same format as binary log files and can be read
    using mysqlbinlog.

  * relay log info log. status information about the execution point within the
    slave's relay log. It is required for the recovery of the SQL thread.

  master info log and relay log info log can be saved to database, which
  improves resilience to unexpected halts. The updates to the tables are
  committed together with the transaction, meaning that the information in them
  is always consistent with what has been applied to the database, even in the
  event of a server halt.

replication formats
""""""""""""""""""""
- SBR. executing the SQL statements on the slave.

- RBR. copying the events representing the changes to the table rows to the
  slave.

- MBR. 

configuration
""""""""""""""
- On the master, you must enable binary logging and configure a non-zero
  unique server ID::

    [mysqld]
    log-bin=log-bin
    server-id=1
    binlog-format=ROW
    sync-binlog=1
    innodb-flush-log-at-trx-commit=1

- On each slave that you want to connect to the master, you must configure a
  unique server ID.

- On master, use a user who's been granted ``REPLICATION SLAVE`` privilege
  during replication, or create a separate user for your slaves to use during
  authentication with the master when reading the binary log for replication::

    CREATE USER 'replication'@'%' IDENTIFIED BY 'replication';
    GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';
    FLUSH PRIVILEGES;

- Before creating a data snapshot or starting the replication process, on the
  master you should record the current position in the binary log.

  * Start a session and flush all tables and block write statements::

      FLUSH TABLES WITH READ LOCK;

    leave the session open to keep global lock.

  * get current binary log coordinates::

      SHOW MASTER STATUS;

    For a new master, this is empty, then use ``''`` and 4.
  
- If you already have data on the master and want to use it to synchronize the
  slave, you need to create a data snapshot to copy the data to the slave.

  * use mysqldump::
      
      mysqldump --all-databases --master-data >dump.sql

    release read lock::
      
      UNLOCK TABLES;
      QUIT;

  * copy raw data.

- Configure the slave with settings for connecting to the master.

  * set unique server id, relay log::

      [mysqld]
      server-id=2
      relay-log=relay-bin
      master-info-repository=TABLE
      relay-log-info-repository=TABLE
      relay-log-purge=1
      relay-log-recovery=1

  * apply master data snapshot.

  * configure replication::

      CHANGE MASTER TO
          MASTER_HOST='master_host_name',
          MASTER_USER='replication_user_name',
          MASTER_PASSWORD='replication_password',
          MASTER_LOG_FILE='recorded_log_file_name',
          MASTER_LOG_POS=recorded_log_position;
      
  * start slave threads::

      START SLAVE;

  * check slave status::

      SHOW SLAVE STATUS;

    ``Slave_IO_running`` and ``Slave_SQL_Running`` should be yes.

  * show binlog threads::

      SHOW PROCESSLIST;

    on master, ``Binlog Dump`` thread should be running, indicating that
    a slave is connected.

    on slave, I/O thread and SQL thread should be running with correct state.

checking replication status
""""""""""""""""""""""""""""
- on master:
  
  * ``SHOW PROCESSLIST;``

- on slave:
  
  * ``SHOW SLAVE STATUS;``
    重要列: ``Slave_IO_State``, ``Slave_IO_Running``, ``Slave_SQL_Running``,
    ``Last_IO_Error``, ``Last_SQL_Error``.

  * ``performance_schema`` replication tables.

replication options
^^^^^^^^^^^^^^^^^^^
- ``--server-id``, ``server_id``.
  default: 0. If the server ID is set to 0, binary logging takes place (if
  ``log_bin`` is set), but a master with a server ID of 0 refuses any
  connections from slaves, and a slave with a server ID of 0 refuses to connect
  to a master.

master info log and relay log options.

- ``--master-info-file=<filename>``.
  default: master.info.

- ``--master-info-repository={FILE|TABLE}``, ``master_info_repository``.
  default: FILE.
  whether the slave logs master status and connection information to a FILE or
  TABLE.

- ``--relay-log=pathname``, ``relay_log``.
  default: ``<hostname>-relay-bin`` for default channel, or
  ``<hostname>-relay-bin-<channel>`` for the named channel.

  It's recommended to set this option independent of hostname to avoid
  issues casued by changed hostname or to ease cloning slave.

- ``--relay-log-info-file=<filename>``, ``relay_log_info_file``.
  default: relay-log.info.

- ``--relay-log-info-repository={FILE|TABLE}``, ``relay_log_info_repository``.
  default: FILE.
  whether the slave's position in the relay logs is written to a FILE or TABLE.

- ``--relay-log-purge={0|1}``, ``relay_log_purge``.
  default: 1.
  automatic purging of relay logs as soon as they are no longer needed.

- ``--relay-log-recovery={0|1}``, ``relay_log_recovery``.
  default 0.
  Enables automatic relay log recovery immediately following server startup.
  This makes a slave resilient to unexpected halts.

- ``--max-relay-log-size=#``, ``max_relay_log_size``.
  default 0, which falls back to ``max_binlog_size``.

binlog checksum.

- ``--slave-sql-verify-checksum={0|1}``, ``slave_sql_verify_checksum``.
  let slave use checksum to verify binlog.

performance schema replication tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- 这些表是 ``SHOW SLAVE STATUS;`` statement 的数据基础. 并且提供的信息
  更加具体和详细.

- table categories.

  * info related to master-slave connections.
    ``replication_connection_configuration``, ``replication_connection_status``.

  * general info related to transaction applier.
    ``replication_applier_configuration``, ``replication_applier_status``.

  * transaction applier info by threads.
    ``replication_applier_status_by_coordinator``,
    ``replication_applier_status_by_worker``.

  * info related to replication filers.
    ``replication_applier_filters``, ``replication_applier_global_filters``.

  * info related to group replication memebers.
    ``replication_group_members``, ``replication_group_member_stats``.

replication_connection_configuration table
""""""""""""""""""""""""""""""""""""""""""
- configuration parameters used by the slave server for connecting to the
  master server.

- Its content remains constant during the connection.

- columns.

  * CHANNEL_NAME. ``""`` for default channel.

  * HOST.

  * PORT.

  * USER.

  * NETWORK_INTERFACE.

  * AUTO_POSITION. 0 if not using autopositioning.

  * ssl options.

  * CONNECTION_RETRY_INTERVAL.

  * CONNECTION_RETRY_COUNT. max retry times.

  * HEARTBEAT_INTERVAL.

  * TLS_VERSION.

  * PUBLIC_KEY_PATH.

  * GET_PUBLIC_KEY.

replication_connection_status Table
""""""""""""""""""""""""""""""""""""
- the current status of replication connection, including the I/O thread that
  handles the slave server connection to the master server, transactions in
  relay logs, etc.

- columns.

  * CHANNEL_NAME.

  * GROUP_NAME.

  * SOURCE_UUID. master server uuid.

  * THREAD_ID.

  * SERVICE_STATE. values: ON (IO thread running and connected), OFF (IO thread
    not running), CONNECTING (IO thread running and connecting to master).

  * RECEIVED_TRANSACTION_SET.

  * LAST_ERROR_NUMBER, LAST_ERROR_MESSAGE, LAST_ERROR_TIMESTAMP.

  * LAST_HEARTBEAT_TIMESTAMP.

  * COUNT_RECEIVED_HEARTBEATS.

  * LAST_QUEUED_TRANSACTION,
    LAST_QUEUED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    LAST_QUEUED_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP,
    LAST_QUEUED_TRANSACTION_START_QUEUE_TIMESTAMP,
    LAST_QUEUED_TRANSACTION_END_QUEUE_TIMESTAMP.

  * QUEUEING_TRANSACTION,
    QUEUEING_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    QUEUEING_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP,
    QUEUEING_TRANSACTION_START_QUEUE_TIMESTAMP.

replication_applier_status Table
""""""""""""""""""""""""""""""""
- general transaction execution status on the slave server that are not
  specific to any thread involved.

- columns.

  * CHANNEL_NAME

  * SERVICE_STATE

  * REMAINING_DELAY

  * COUNT_TRANSACTIONS_RETRIES

replication_applier_global_filters Table
""""""""""""""""""""""""""""""""""""""""
- global replication filters configured on this slave.

- columns.

  * FILTER_NAME.

  * FILTER_RULE.

  * CONFIGURED_BY.

  * ACTIVE_SINCE.

replication SQL statements
^^^^^^^^^^^^^^^^^^^^^^^^^^

SHOW SLAVE HOSTS
""""""""""""""""
:: 

  SHOW SLAVE HOST

- displays a list of replication slaves currently registered with the master.

- each row corresponds to one slave.

- basic columns: Server_id, Master_id, Slave_UUID.
  extra columns (根据 slave 是否提供): Host, User, Password, Port.

SHOW SLAVE STATUS
""""""""""""""""""
::

  SHOW SLAVE STATUS [FOR CHANNEL <channel>]

- privileges required: REPLICATION CLIENT.

- 显示的信息源于 performance schema replication tables.

- output columns from tables.

  * ``sys.processlist``:
    Slave_IO_State,
    Slave_SQL_Running_State

  * ``performance_schema.replication_connection_status``:
    Slave_IO_Running,
    Master_UUID,
    Last_IO_Errno,
    Last_IO_Error,
    Last_IO_Error_Timestamp,
    Channel_name,

  * ``performance_schema.replication_applier_status``:
    Slave_SQL_Running,

  * ``performance_schema.replication_applier_global_filters``:
    Replicate_Do_DB,
    Replicate_Ignore_DB,
    Replicate_Do_Table,
    Replicate_Ignore_Table,
    Replicate_Wild_Do_Table,
    Replicate_Wild_Ignore_Table,
    Replicate_Rewrite_DB

  * ``performance_schema.replication_connection_configuration``:
    Master_Host,
    Master_User, 
    Master_Port, 
    Master_Bind,
    Connect_Retry,
    Master_Retry_Count,
    Master_SSL_Allowed,
    Master_SSL_CA_File,
    Master_SSL_CA_Path,
    Master_SSL_Cert,
    Master_SSL_Cipher,
    Master_SSL_CRL_File,
    Master_SSL_CRL_Path,
    Master_SSL_Key,
    Master_SSL_Verify_Server_Cert,
    Auto_Position,
    Master_TLS_Version,
    Master_public_key_path,
    Get_master_public_key

  * ``mysql.slave_master_info``:
    Master_Log_File, 
    Read_Master_Log_Pos

  * ``mysql.slave_relay_log_info``:
    Relay_Log_File, 
    Relay_Log_Pos, 
    Relay_Master_Log_File,
    SQL_Delay

  * ``performance_schema.replication_applier_status_by_worker``:
    Last_SQL_Errno,
    Last_SQL_Error
    Last_Errno,
    Last_Error,
    Last_SQL_Error_Timestamp,

  * Skip_Counter

  * Exec_Master_Log_Pos

  * Relay_Log_Space

  * Until_Condition, Until_Log_File, Until_Log_Pos

  * Replicate_Ignore_Server_Ids

  * Master_Server_Id

  * Master_Info_File

  * Seconds_Behind_Master

  * SQL_Remaining_Delay

  * Retrieved_Gtid_Set

  * Executed_Gtid_Set

CHANGE MASTER TO
""""""""""""""""
- 配置保存在 ``performance_schema.replication_connection_configuration``.

CHANGE REPLICATION FILTER
"""""""""""""""""""""""""

backup and recovery
===================

Percona XtraBackup
------------------
feature
^^^^^^^

- non-blocking hot backup for InnoDB.

prerequisites
^^^^^^^^^^^^^
* full-backup permissions

  - ``RELOAD``, ``LOCK TABLES``
  
  - ``REPLICATION CLIENT``
  
  - ``PROCESS``

* need access to mysql data dir. thus can only be run locally.

procedure
^^^^^^^^^

- create user with permissions::

    CREATE USER '<user>'@'localhost' IDENTIFIED BY '<pass>';
    GRANT RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT ON *.* TO '<user>'@'localhost';
    FLUSH PRIVILEGES;

- full backup::

    xtrabackup -u <user> -p<pass> --backup --parallel=# --target-dir=<dir>

  它自动访问 mysql data directory, 复制数据. target dir 若已有数据, 会报错退出.
  可以直接 stream 到 slave node, 而不是保存成文件::

    xtrabackup -u <user> \
            -p<pass> \
            --backup \
            --parallel=# \
            --stream=xbstream \
            --compress \
            --compress-threads=# 2> backup-progress.log | \
        ssh <user>@<host> xbstream -x --parallel=# -C <dir>

  When performing a local backup or the streaming backup with xbstream option,
  multiple files can be copied concurrently. ``--parallel`` option specifies
  the number of threads created by xtrabackup to copy data files. [PerconaAcce]_

  Parallel data compression is also performed. Data read by parallel I/O
  threads will be piped to compression threads.

  At receiving end, use ``xbstream`` to decompress and extract streamed data
  into files. Parallel extraction is specified. [PerconaXbstream]_

- prepare a backup::

    xtrabackup --prepare --target-dir=<dir>

  Because xtrabackup performs hot backup, data were copied at different times
  as the program ran, and they might have been changed while this was
  happening. Therefore Data files are not point-in-time consistent until
  they’ve been prepared.

  You can run the prepare operation on any machine; it does not need to be on
  the originating server or the server to which you intend to restore.

- restore backup::

    xtrabackup --move-back && chown -R mysql:mysql /var/lib/mysql

replication info
^^^^^^^^^^^^^^^^

- ``xtrabackup_binlog_info`` file contains coordinate of the exact point in the
  binary log to which the prepared backup corresponds.

CLI
===

Option Files
------------
- option files 是 mysql 相关程序通用的一种配置文件系统.
  本质上是配置了各种 mysql 程序启动时指定的命令行参数.

- ``--help`` 输出一个 mysql 程序识别的配置参数, 读取的配置文件和顺序, 以及
  对每个文件读取的 config group.

- MySQL ignores configuration files that are world-writable.

- option files and read order:

  * /etc/my.cnf

  * /etc/mysql/my.cnf

  * SYSCONFDIR/my.cnf. don't know what it is.

  * $MYSQL_HOME/my.cnf. server only.

  * defaults-extra-file. specified by ``--defaults-extra-file``.

  * ~/.my.cnf.

  * ~/.mylogin.cnf. clients only. encrypted.

  * DATADIR/mysqld-auto.cnf. server only. managed by mysqld.

- 重复的选项最后一个生效, 除非该选项允许指定多次. ``--user`` 只有第一个生效.

- Any long option that may be given on the command line when running a MySQL
  program can be given in an option file as well. 同时, hyphen 也都可以转换
  成 underscore, 符合 system variable 的形式.

file format
^^^^^^^^^^^

- empty lines are ignored.

- #, ; starts line comment.

- ``[<group>]`` a config group. group name can be:

  * mysql program name. the options apply only to the specific program.

  * 对于 mysqld group, 可以附加版本号, 例如: ``[mysqld-8.0]``.

  * ``client``. applies to all client mysql programs. Be sure not to put an
    option in the [client] group unless it is recognized by all client programs
    that you use. 不然的话会导致一些 client program 无法运行.

  * option files 中的 groups 应该从 general 至 specific 的顺序安排. 例如::

    [client]
    # ...
    [mysql]
    # ...
    [mysqld]
    # ...

- ``{opt_name|opt-name} = value``.
  
  * space around = is optional.
  
  * value can be optionally quoted using single or double quotes.

  * On an option line, leading and trailing spaces are stripped.

  * backslash escape sequences are accepted as in string literals.

- ``!include <file>``. read additional file.

- ``!includedir <dir>``. files in dir must ends with ``.cnf``.
  Order of reading of files in dir is unspecified.

Client Programs
---------------

mysql
^^^^^

- ``\g`` ``\G`` 可以执行语句, 相当于 ``;``. 后者将结果列以竖排的形式输出, 比较方便.

- ctrl-c 和 ``\c`` 都可以终止当前语句.

- mysql client 会给出执行时间, 这个时间是在客户端算出的从发出请求到收到结果的 wall
  clock time.

- 支持输入 mutiline 的 string 和 identifier. 直接加回车即可.

- mysql client 对不同的 multiline 模式给出不同的 prompt string, 甚至包含 string,
  identifier 和 block comment 的多行输入模式. ``">``, ``'>``, ``\`>``, ``/*>``.

- 可以在连接时指定要使用的数据库, 或者用 ``USE`` 切换.

- cmdline 参数 ``-p`` 指定密码时不能有空格. 或者使用 ``--password=<pass>``.

- In non-interactive mode, read input sql from stdin, print results to stdout.
  For processing convenience, such output is tab-delimited for each column.

Utility Programs
----------------

mysqlbinlog
^^^^^^^^^^^

Language driver
===============
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

  根据以上分析, 我会选择 mysqlclient 和 PyMySQL, 分别在同步和异步的情况下使用.

mysqlclient
-----------

mysql data types in python
^^^^^^^^^^^^^^^^^^^^^^^^^^

- BIT(N): bytes

mysql vs postgresql
===================

- default isolation level.

  mysql 使用 repeatable read. postgresql 使用 read committed.

  后者才是一般预期的行为, 是除了 mysql 之外所有其他数据库的默认行为.
  这两个 isolation level 的差异, 会导致应用程序的一些 subtle bugs.

- mysql does not support DDLs in transaction. DDL statements are
  non-transactional and break transactions (cause implicit commit etc.).

References
==========
.. [DOMysqlSlave] `How To Set Up Master Slave Replication in MySQL <https://www.digitalocean.com/community/tutorials/how-to-set-up-master-slave-replication-in-mysql>`_
.. [PerconaAcce] `Accelerating the backup process <https://www.percona.com/doc/percona-xtrabackup/LATEST/innobackupex/parallel_copy_ibk.html>`_
.. [PerconaXbstream] `The xbstream binary <https://www.percona.com/doc/percona-xtrabackup/LATEST/xbstream/xbstream.html>`_
.. [SOCharVarchar] `What are the use cases for selecting CHAR over VARCHAR in SQL? <https://stackoverflow.com/questions/59667/what-are-the-use-cases-for-selecting-char-over-varchar-in-sql>`_
