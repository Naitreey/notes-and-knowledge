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

  [_<charset>] b'<bin>' [COLLATE <collation>]
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

- Keywords are case-insensitive.

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
 
statement syntax
----------------
- Statement is terminated by semicolon.

- Statements can be in free-format.

Data types
==========
general attributes
------------------

NULL, NOT NULL
^^^^^^^^^^^^^^
- If unspecified, default is NULL.

- The result of any arithmetic comparison with NULL is also NULL, 判断是否是
  NULL 只能用 ``IS NULL``, ``IS NOT NULL``.

- When doing an ORDER BY, NULL values are presented first if you do ORDER BY
  ... ASC and last if you do ORDER BY ... DESC.

DEFAULT
^^^^^^^
explicit default value
""""""""""""""""""""""
- definition format::

    DEFAULT literal | DEFAULT (expr)

  也就是说, 默认值可以是一个 literal value, or an expression enclosed in
  parentheses.

- rules for default expression, see [DocDefaultValue]_.

- for TIMESTAMP and DATETIME columns, you can specify the CURRENT_TIMESTAMP
  function as the default, without enclosing parentheses.

- The BLOB, TEXT, GEOMETRY, and JSON data types can be assigned a default value
  only if the value is written as an expression, even if the expression value
  is a literal.

- 若指定的默认值与列数据类型不符, implicit coercion occurs.

implicit default value
""""""""""""""""""""""
- 如果一个列在定义时没有指定 DEFAULT attribute,
  
  * 若该列接受 NULL 值, 自动设置 DEFAULT NULL.

  * 若该列不接受 NULL 值, 不设置 DEFAULT clause.
    
specify default in DML
""""""""""""""""""""""
* 在 INSERT 时在 VALUES list 中不指定该列. 例如::

    INSERT INTO tbl (/* omit col1 */ col2, col3) VALUES (val2, val3);

* 使用 ``DEFAULT`` 明确指定插入当前列的默认值::

    INSERT INTO tbl (col1, col2, col3) VALUES (DEFAULT, val2, val3);

* 使用 ``DEFAULT(col)`` function to get a column's default value, and use it
  anywhere. 注意这与第二个方式是不同的, 不是同一个用法.

storage requirements
--------------------

* max row size: 64KB. Excluding BLOB, TEXT, JSON columns, 它们单独存储, 只
  在行内添加必要信息.

Numeric types
-------------
data type attributes
^^^^^^^^^^^^^^^^^^^^
* UNSIGNED.
    
  - integer types: only nonnegative values are allowed. 所有 bytes 用 unsigned
    binary arithmetics 存储, 最大值为 signed 情况的两倍.

  - floating-point and fixed-point types: only nonnegative values are allowed.
    但存储方式不变, 最大值不变.

* AUTO_INCREMENT.
  
  * integer types and floating-point types can be auto-incremented.

  * AUTO_INCREMENT field 应该设置 NOT NULL, 因为一般通过插入 NULL 来自动递增序
    列值.
  
  * 列值只能为正值. Sequence begins with 1.
    
  * 若插入任何大于当前最大序数的数字,  the column is set to that value and the
    sequence is reset so that the next automatically generated value follows
    sequentially from the inserted value.

  * 若插入负值, 相当于插入 unsigned 等价正值.

  * 一个表里只能有一个列是 auto-incremented, 必须有 index, 不能有 DEFAULT.
    
  * 当一个表里有 AUTO_INCREMENT field 时, 一般就应该作为主键使用吧. 但也许另有
    更适合的主键 (例如多列的组合是更自然的主键的情况).

  * You can retrieve the most recent automatically generated ``AUTO_INCREMENT``
    value with the ``LAST_INSERT_ID()`` SQL function.

  * 在插入时, 递增 AUTO_INCREMENT field 的方法:

    - 插入 NULL.

    - 插入 DEFAULT key 值, 或者使用等价形式, 将该列直接从 VALUES 部分忽略.

- mysql 支持给 integer types 添加 ``(M)`` attribute 以设置 "display width".
  还有 ZEROFILL attribute. THIS IS CRAZY. DON'T DO THIS. SAVE YOUR FUCKING ASS.

- In non-strict sql mode, out-of-range values are clipped to the appropriate
  endpoint of the column data type range and the resulting value are stored.

integer types
^^^^^^^^^^^^^
BOOL
""""
- BOOL, BOOLEAN are synonyms for TINYINT(1). 所以实际上 BOOL 可以存 0-255
  的数据. FUCKED UP.

- TRUE, FALSE 实际上是 1, 0 数值.

- Which data type to use for BOOL, BOOL a.k.a. TINYINT(1) or BIT(1)?

  * BIT(1) 可以严格限制数据.

  * TINYINT(1) 的默认输出就是 1, 0 integer. 无需额外转换, 与 true/false
    一致. BIT(1) 可能需要应用去额外转换.

- falsy values: 0, FALSE, NULL.

- truthy values: anything else.

TINYINT
"""""""

- 1 byte.

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

  * The precision represents the number of significant digits that are stored
    for values, and the scale represents the number of digits that can be
    stored following the decimal point.

  * 注意到, M 必须 >= D.

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

- BLOB and TEXT columns can be assigned a default value only if the value is
  written as an expression, even if the expression value is a literal

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

- Changing ENUM definition:

  * ALTER TABLE 修改列数据类型定义.

  * It is possible to append new members to a ENUM column.

  * Editing or removing existing members will error if MySQL Strict Mode is on.

- storage. 1-2 bytes.

- ENUM field type 的意义: 提高 enumeration 性质的数据的存储效率.

  这是因为: 与 enum integer 对应的 enum literal string 只存储一次. 在各个行中只
  保存一个至多 2 bytes 的整数. 整体的存储是: 一系列的 1-2 bytes 的数字加上一个
  integer-to-string 的映射. 相比之下, 纯粹保存字符串显然需要多很多的存储空间.

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

- GEOMETRY types can be assigned a default value only if the value is written
  as an expression, even if the expression value is a literal.

- storage. 4 bytes for SRID + WKB representation of geometry value.

- OpenGIS Geometry Model.

JSON type
---------

- Automatic JSON data validation.

- Optimized binary storage format and manipulation.

  * quick read access to individual subobjects or values.

  * inplace update of JSON document. 

- JSON column can be assigned a default value only if the value is written as
  an expression, even if the expression value is a literal.

- index. JSON column can not be indexed directly.
  
  * Workaround: create an index on a virtual generated column that extracts a
    scalar value from the JSON column.

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

Database
========
SQL statements
--------------
CREATE DATABASE
^^^^^^^^^^^^^^^
::

  CREATE {DATABASE|SCHEMA} [IF NOT EXISTS] <name>
      [[DEFAULT] CHARACTER SET [=] charset_name]
      [[DEFAULT] COLLATE [=] collation_name]

- privilege: CREAT for the specified database.

- database definition is recorded in INFORMATION_SCHEMA.SCHEMATA.

- 一个数据库就是 mysql 数据目录下的一个子目录. 该语句就是创建了一个目录.
  If a database name contains special characters, the name for the database
  directory contains encoded versions of those characters.

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

SHOW CREATE DATABASE
^^^^^^^^^^^^^^^^^^^^
::

  SHOW CREATE DATABASE [IF NOT EXISTS] <db_name>

- 输出创建该数据库使用的 CREATE DATABASE statement.

- default charset and collation 也会输出. 如果 collation 部分
  没有显示, 说明使用的是相应 charset 默认的 collation.

SHOW DATABASES
^^^^^^^^^^^^^^
::

  SHOW {DATABASES | SCHEMAS} [LIKE <pattern> | WHERE <expr>]

- You see only those databases for which you have some kind of privilege,
  unless you have the global ``SHOW DATABASES`` privilege. 如果
  ``--skip-show-database`` option is specified by server, 则必须要有这个
  global 权限才能 show databases.

- The output corresponds to INFORMATION_SCHEMA.SCHEMATA table.

Table
=====
SQL statements
--------------
CREATE TABLE
^^^^^^^^^^^^
- CREATE privilege for the table is required.

formats
"""""""
- normal "CREATE TABLE"::

    CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
        (create_definition, ...)
        [table_options]
        [partition_options]

    create_definition:
        col_name column_definition
      | [CONSTRAINT [symbol]] PRIMARY KEY (key_part,...)
          [index_option] ...
      | {INDEX|KEY} [index_name] (key_part,...)
          [index_option] ...
      | [CONSTRAINT [symbol]] UNIQUE [INDEX|KEY]
          [index_name] (key_part,...)
          [index_option] ...
      | {FULLTEXT|SPATIAL} [INDEX|KEY] [index_name] (key_part,...)
          [index_option] ...
      | [CONSTRAINT [symbol]] FOREIGN KEY
          [index_name] (col_name,...) reference_definition
      | check_constraint_definition

    column_definition:
        data_type [NOT NULL | NULL] [DEFAULT {literal | (expr)} ]
          [AUTO_INCREMENT] [UNIQUE [KEY]] [[PRIMARY] KEY]
          [COMMENT 'string']
          [COLUMN_FORMAT {FIXED|DYNAMIC|DEFAULT}]
          [STORAGE {DISK|MEMORY|DEFAULT}]
          [reference_definition]
      | generated_column

    key_part, index_option, index_type: See CREATE INDEX

    reference_definition:
        REFERENCES tbl_name (key_part,...)
          [MATCH FULL | MATCH PARTIAL | MATCH SIMPLE]
          [ON DELETE reference_option]
          [ON UPDATE reference_option]
    
    reference_option:
        RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT

- "CREATE TABLE" by queried data::

    CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
        [(create_definition, ...)]
        [table_options]
        [partition_options]
        [IGNORE | REPLACE]
        [AS] query_expression

- "CREATE TABLE" like existing table::

    CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
        LIKE old_tbl_name

table name
""""""""""
::

  [db_name.]tbl_name

- Unqualified table name is created in default database.

- If you use quoted identifiers, quote the database and table names separately.

CREATE TABLE ... query
"""""""""""""""""""""""
- 最终创建的表的列是 ``create_definition`` 部分与 query 语句中包含的列的并集.

  In the resulting table, columns named only in the CREATE TABLE part come
  first. Columns named in both parts or only in the query part come after
  that. The data type of query columns can be overridden by also specifying
  the column in the CREATE TABLE part.

- 查询出来的数据填入新表的对应列, 对于新创建的列, 使用默认值.

- IGNORE and REPLACE 指定如何处理 rows with duplicate PK values. IGNORE
  discards all rows duplicating an existing row. REPLACE replaces the original
  row.  If neither is specified, rows with duplicate PKs result in error.

- 注意对于根据 query 列定义创建的列, 原索引并没有复制, 需在 CREATE TABLE 部分
  单独指定. Retained attributes are NULL (or NOT NULL) and, for those columns
  that have them, CHARACTER SET, COLLATION, COMMENT, and the DEFAULT clause.
  The AUTO_INCREMENT attribute is not preserved.

- 任何 query statement 都可以使用, 不仅仅是 SELECT statement, 例如 UNION.

- About generated column: Destination table does not preserve information about
  whether columns in the selected-from table are generated columns. query part
  cannot assign values to generated columns in the destination table.

- If ``IF NOT EXISTS`` is given and the target table exists, nothing is
  inserted into the destination table, and the statement is not logged.

CREATE TABLE ... LIKE
"""""""""""""""""""""
- create an empty table based on definition of another table.

- SELECT privilege on original table is required.

- Only base tables can be used as original table, not views.

- DATA/INDEX DIRECTORY table option is not preserved.

- Foreign key definitions are not preserved.

- About generated column: Generated column information from the original table
  is preserved.

column definitions
""""""""""""""""""
- hard limit for column numbers: 4096 per table.

- each data types accepts additional data type attributes as defined in
  respective sections of `Data types`_.

- COMMENT. up to 1024 chars.

generated column
""""""""""""""""
::

  generated_column:
      data_type [GENERATED ALWAYS] AS (expression)
          [VIRTUAL | STORED] [NOT NULL | NULL]
          [UNIQUE [KEY]] [[PRIMARY] KEY]
          [COMMENT 'string']
          [reference_definition]

- Column value is generated by expression.

- Rules for expression, see [DocGenColumn]_.

- GENERATED ALWAYS. an optional keyword to make the generated nature of the
  column more explicit.

- A generated column can be VIRTUAL or STORED. default is VIRTUAL.

  * VIRTUAL: 列数据不保存, 在读取相关行时才临时计算, 不需要存储空间.

  * STORED: 列数据与普通列相同方式保存, 所以需要存储空间. 在对该行的 insert 和
    各次 update 时自动计算和更新.

- 若表达式值与列类型不一致, implicit coercion occurs.

- if a generated column is inserted into, replaced, or updated explicitly, the
  only permitted value is DEFAULT.

- generated column and index.

  * Primary and secondary indexes can be defined on stored generated columns.

  * Only secondary index can be defined on virtual generated columns. primary
    key index can not reference a virtual generated column.

  * When secondary index is defined on virtual generated columns, column values
    are materialized in the index. For covering index query, values are
    retrieved directly from index, as usual, without computation on-the-fly.

  * Values of an indexed generated column are MVCC-logged to avoid unnecessary
    recomputation of generated column values during rollback or during a purge
    operation.

- 若 generated column 有索引, 在查询时, 优化器会适时根据 query expression 使用
  该列的索引, 而并不是说只有直接 query against generated column 时才使用索引.

- Use cases.

  * Virtual generated column 可用于替代可重用的复杂 query expression. 这样降低
    重复, 并保证了查询表达式的一致性.

  * Stored generated column 可作为复杂计算结果的缓存.

  * Virtual generated column 配合索引使用, 比 functional index 使用起来稍方便一
    些, 因查询时无需写明复杂的表达式.

constraints
"""""""""""
- CONSTRAINT clause is used for naming a constraint explicitly. 这里,
  constraint 指的是 PRIMARY KEY, UNIQUE INDEX, FOREIGN KEY 三种具有限制性的
  索引.

  所有 constraint 都具有以下特点: They prevent data from being inserted or
  updated if data would become inconsistent.

- CONSTRAINT 若使用, 其后命名的 symbol name 必须是在整个数据库中唯一的.

- CONSTRAINT clause 基本上是多余的, 除了具有一定的 semantic value 之外, 没有任
  何实际作用.

primary key
"""""""""""
- A special unique index.

- all key parts of a PRIMARY KEY index must be NOT NULL, either explicitly
  by programmer or implicitly by MySQL parser.

- A table can have only one PRIMARY KEY.

- The index/constraint name is PRIMARY.

foreign key
"""""""""""
- FOREIGN KEY constraint 主要有两个作用:
  
  * Referential integrity (表之间的数据交叉引用时).  Specifically, MySQL
    rejects any INSERT or UPDATE operation that attempts to create a foreign
    key value in a child table if there is no a matching candidate key value in
    the parent table.

  * Referential action. When an UPDATE or DELETE operation affects a key value
    in the parent table that has *matching rows* in the child table, the action
    depends on ON UPDATE and ON DELETE clauses. 注意 *matching rows* 是根据
    referencing and referenced columns 的值是否相同来决定的 (通过 scan index).
    并不存在想象中的 pointer connection.

    - ON DELETE CASCADE, ON UPDATE CASCADE. 当两个表各自设置了指向对方的 FK
      constraints 时, 若其一指定了 CASCADE referential action, 另一个也必须
      指定相同的 CASCADE action.

    - ON DELETE SET NULL, ON UPDATE SET NULL.

    - RESTRICT (default), NO ACTION. Rejects the delete or update operation for
      the parent table.

    - SET DEFAULT. (并不可用.)

- schema design considerations:

  * For self-referencing FK, ON DELETE RESTRICT will cause only the most leaf
    row (lowest child) can be deleted. Any bulk delete (more than one row) is
    forbidden. If bulk delete is desired, referential integrity must be
    relaxed, and use SET NULL or CASCADE as appropriate.

  * When two tables must be cross-referenced with 2 FKs, any one of them using
    RESTRICT may cause dead lock. In that case, at least one of the FKs can use
    SET NULL or CASCADE as appropriate.

- implementation:

  - FK constraint 依赖于相关列之上的一个 index 来实现.
  
    * 若表中已经存在以 FK 各列起始的 index, 则创建 FK constraint 时不会再重复创
      建索引, 而是重用这个索引. 此时, ``index_name`` 若指定则忽略.
  
    * 若表中没有这样可重用的索引, 则会新建一个 index 以实现 FK constraint.

    * 若后续明确创建了可重用于 FK constraint 的索引, 且初始创建 FK index 时
      没有指定 index name, 则原来的 FK index 会被 drop 掉.

  - 在 referenced table 中, 对 referenced columns 上面也必须有与 REFERENCES
    clause 中顺序相符的索引或索引前缀.

  - FK columns 以及 referenced columns 上的两个索引, 是为了提高正向和反向的
    FK check 速度, 避免 full table scan.

- naming of foreign key constraint:

  * use the specified ``CONSTRAINT`` name

  * use the specified ``FOREIGN KEY`` name

  * use an autogenerated name.

  注意 FK 的名字不代表一定创建相应的同名索引, 索引是可以看情况重用的.

- parent table and child table 的关联限制.
  
  * Child FK columns 中填入所引用的 parent table 中相关列的完全相同的列值.

  * Parent and child tables must use the same storage engine.

  * Parent and child tables must not be TEMPORARY tables.

  * Parent and child tables 中的相关列的数据类型限制:

    - 对于 integer types: The size and sign must be the same

    - 对于 string/binary types: length need not be the same. For nonbinary
      string columns, the character set and collation must be the same.

    - TEXT/BLOB 等类型列不能用于 FK constraints, 因 FK 的索引不能包含 prefix.

  * Parent table 中的 referenced columns 不必构成 unique index.

- 设置了 partitioning 的表, 不能用于 FK 关系中.

- generated column.

  * Stored generated column 上设置 FK constraint 时, referential action 只能使
    用 ON DELETE CASCADE.

  * Virtual generated column can not be referenced by a FK.

- constraints on altering schema.

  * the server prohibits changes to foreign key columns with the potential to
    cause loss of referential integrity.

  * DROP TABLE for a table that is referenced by a FOREIGN KEY constraint is
    disallowed.

temporary table
"""""""""""""""
::

  CREATE TEMPORARY TABLE

- 当一个 session 中需要对同样的查询结果数据进行多次处理时, 可以通过创建临时表来
  提高效率. 尤其是当这个查询结果的构造成本比较高时.

- require privilege: CREATE TEMPORARY TABLES.

- A temporary table is visible only within the current session, and is dropped
  automatically when the session is closed.

- two different sessions can use the same temporary table name without
  conflicting with each other. The existing non-TEMPORARY table of the same
  name is hidden until the temporary table is dropped.

- CREATE TEMPORARY TABLE does NOT cause an implicit commit.

- Drop a database does not automatically drop any TEMPORARY tables in that
  database. A TEMPORARY table can be created in a nonexistent database.

CHECK constraints
"""""""""""""""""
::

  check_constraint_definition:
      [CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]

implicit column specification
"""""""""""""""""""""""""""""
- PRIMARY KEY columns are made NOT NULL, if unspecified.

- Certain data types used by other RDBMS are mapped to mysql types.

- If the specified USING index type is not available for the given storage
  engine, but there's another type available without affecting query results,
  the available type is used.

- CHAR/VARCHAR/TEXT with CHARACTER SET binary is converted to
  BINARY/VARBINARY/BLOB.

table options
"""""""""""""
::

  table_options:
      table_option [[,] table_option] ...

  table_option:
      AUTO_INCREMENT [=] value
    | AVG_ROW_LENGTH [=] value
    | [DEFAULT] CHARACTER SET [=] charset_name
    | CHECKSUM [=] {0 | 1}
    | [DEFAULT] COLLATE [=] collation_name
    | COMMENT [=] 'string'
    | COMPRESSION [=] {'ZLIB'|'LZ4'|'NONE'}
    | CONNECTION [=] 'connect_string'
    | {DATA|INDEX} DIRECTORY [=] 'absolute path to directory'
    | DELAY_KEY_WRITE [=] {0 | 1}
    | ENCRYPTION [=] {'Y' | 'N'}
    | ENGINE [=] engine_name
    | INSERT_METHOD [=] { NO | FIRST | LAST }
    | KEY_BLOCK_SIZE [=] value
    | MAX_ROWS [=] value
    | MIN_ROWS [=] value
    | PACK_KEYS [=] {0 | 1 | DEFAULT}
    | PASSWORD [=] 'string'
    | ROW_FORMAT [=] {DEFAULT|DYNAMIC|FIXED|COMPRESSED|REDUNDANT|COMPACT}
    | STATS_AUTO_RECALC [=] {DEFAULT|0|1}
    | STATS_PERSISTENT [=] {DEFAULT|0|1}
    | STATS_SAMPLE_PAGES [=] value
    | TABLESPACE tablespace_name [STORAGE {DISK|MEMORY|DEFAULT}]
    | UNION [=] (tbl_name[,tbl_name]...)

Table options apply to all storage engines unless otherwise indicated.

- ENGINE. Unquoted or string-quoted engine name. Default is InnoDB.  INNODB,
  MYISAM, MEMORY, CSV, ARCHIVE, EXAMPLE, FEDERATED, MERGE, NDB.

- AUTO_INCREMENT. initial auto increment value for the table. (There can be
  only one AUTO_INCREMENT column in a table.) default is 1.

- [DEFAULT] CHARACTER SET. the default character set for the table. This is the
  default charset for textual columns in the table. ``charset_name`` by default
  is DEFAULT, in which case it falls back to database default charset.

- [DEFAULT] COLLATE. ditto for collation.

- COMMENT. max 2048 字符. default empty.

- COMPRESSION. specify page-level compression for InnoDB tables. Zlib, LZ4, None.
  default is None.

- {DATA|INDEX} DIRECTORY. For InnoDB, only DATA DIRECTORY can be used (Because
  InnoDB file-per-table tablespace file contains both data and index). This
  permits creating a file-per-table tablespace outside of the data directory.
  The tablespace data file is created in the specified directory, inside a
  subdirectory with the same name as the schema. Default is specified by
  ``datadir`` system variable.

- TABLESPACE. specify a general tablespace, a file-per-table tablespace, or
  system tablespace. 如果是 general tablespace, 必须预先存在; ``innodb_system``
  is system tablespace, specify ``innodb_file_per_table`` to create explicitly
  a file-per-table tablespace, as will do by default ``innodb_file_per_table``
  system variable. 这个 table option 用于明确指定所属的 tablespace, override by
  system defaults.

  Only when specifying ``innodb_file_per_table`` TABLESPACE, DATA DIRECTORY
  can be specified.

- ENCRYPTION. InnoDB page-level data encryption for file-per-table tablespace.
  default is N.

- KEY_BLOCK_SIZE. the page size in kilobytes to use for compressed InnoDB
  tables. the default compressed page size, which is half of the
  ``innodb_page_size`` value.

- MAX_ROWS. The maximum number of rows you plan to store in the table. This is
  not a hard limit, but rather a hint to the storage engine that the table must
  be able to store at least this many rows. max value is 2**32-1.

- MIN_ROWS. The minimum number of rows you plan to store in the table. The
  MEMORY storage engine uses this option as a hint about memory use.

- ROW_FORMAT. The physical format of rows. default is DEFAULT, which is defined
  by ``innodb_default_row_format``. See `Row formats`_ for detail.

- STATS_PERSISTENT. whether to enable persistent statistics for an InnoDB
  table. default is DEFAULT, which is defined by ``innodb_stats_persistent``.

- STATS_AUTO_RECALC. whether to automatically recalculate persistent statistics
  for an InnoDB table. default is DEFAULT, defined by ``innodb_stats_auto_recalc``.

- STATS_SAMPLE_PAGES. The number of index pages to sample when calculating
  table statistics.

- AVG_ROW_LENGTH.

- CHECKSUM.

- CONNECTION.

- DELAY_KEY_WRITE.

- INSERT_METHOD.

- PACK_KEYS.

- UNION.

table partitioning
""""""""""""""""""
::

  partition_options:
      PARTITION BY
          { [LINEAR] HASH(expr)
          | [LINEAR] KEY [ALGORITHM={1|2}] (column_list)
          | RANGE{(expr) | COLUMNS(column_list)}
          | LIST{(expr) | COLUMNS(column_list)} }
      [PARTITIONS num]
      [SUBPARTITION BY
          { [LINEAR] HASH(expr)
          | [LINEAR] KEY [ALGORITHM={1|2}] (column_list) }
        [SUBPARTITIONS num]
      ]
      [(partition_definition [, partition_definition] ...)]
  
  partition_definition:
      PARTITION partition_name
          [VALUES
              {LESS THAN {(expr | value_list) | MAXVALUE}
              |
              IN (value_list)}]
          [[STORAGE] ENGINE [=] engine_name]
          [COMMENT [=] 'string' ]
          [DATA DIRECTORY [=] 'data_dir']
          [INDEX DIRECTORY [=] 'index_dir']
          [MAX_ROWS [=] max_number_of_rows]
          [MIN_ROWS [=] min_number_of_rows]
          [TABLESPACE [=] tablespace_name]
          [(subpartition_definition [, subpartition_definition] ...)]
  
  subpartition_definition:
      SUBPARTITION logical_name
          [[STORAGE] ENGINE [=] engine_name]
          [COMMENT [=] 'string' ]
          [DATA DIRECTORY [=] 'data_dir']
          [INDEX DIRECTORY [=] 'index_dir']
          [MAX_ROWS [=] max_number_of_rows]
          [MIN_ROWS [=] min_number_of_rows]
          [TABLESPACE [=] tablespace_name]

See `Partitioning`_.

SELECT
^^^^^^
::

  SELECT
    [ALL | DISTINCT]
    select_expr [, select_expr ...]
    [FROM table_references
      [PARTITION partition_list]
      [WHERE where_condition]
      [GROUP BY {col_name | expr}, ... [WITH ROLLUP]]
      [HAVING where_condition]
      [WINDOW window_name as (window_spec) [, window_name as (window_spec)] ...]
      [ORDER BY {col_name | expr} [ASC | DESC], ... [WITH ROLLUP]]
      [LIMIT {[offset,] row_count | row_count OFFSET offset}]
      [INTO OUTFILE 'file_name' [CHARACTER SET charset_name] export_options
        | INTO DUMPFILE 'file_name'
        | INTO var_name [, var_name]]
      [FOR {UPDATE | SHARE} [OF tbl_name [, tbl_name] ...] [NOWAIT | SKIP LOCKED]]

select list
"""""""""""
- Select list specifies which columns to retrieve.

- Each ``select_expr`` can be:

  * A column name. The name can be unqualified, or fully qualified as
    ``[db_name.]tbl_name.col_name`` for necessary disambiguation. But whatever
    form is used, only columns made available by FROM clause can be referenced.

  * An arbitrary expression that contains column references or not.

  * ``[db_name.]tbl_name.*`` is a qualified shorthand, selecting all columns
    from the named table.

  * A single unqualified ``*`` shorthand, selecting all columns from all
    tables. Use an unqualified ``*`` with other items in the select list may
    produce a parse error. To avoid this problem, use a qualified
    ``tbl_name.*`` reference.

- Alias. ``select_expr`` can be given an alias ``[AS] alias``, which is used as
  expression's column name. Alias can be used in GROUP BY, HAVING, ORDER BY;
  but can not be used in WHERE, because when the WHERE clause is evaluated, the
  column value may not yet have been determined (for example column is an
  aggregate expression).

  Note that ``AS`` is technically optional.

table references
""""""""""""""""
Complete table reference syntax::

  table_references:
    table_reference [, table_reference] ...

  table_reference:
    table_factor | joined_table

  table_factor:
      tbl_name [PARTITION (partition_names)] [[AS] alias] [index_hint_list]
    | table_subquery [AS] alias [(col_list)]

  joined_table:
      table_reference {[INNER | CROSS] JOIN | STRAIGHT_JOIN} table_factor [join_specification]
    | table_reference {LEFT|RIGHT} [OUTER] JOIN table_reference join_specification
    | table_reference NATURAL [INNER | {LEFT|RIGHT} [OUTER]] JOIN table_factor

  join_specification:
      ON search_condition | USING (join_column_list)

  join_column_list:
      column_name [, column_name] ...

  index_hint_list:
      index_hint [, index_hint] ...

  index_hint:
      USE {INDEX|KEY} [FOR {JOIN|ORDER BY|GROUP BY}] ([index_list])
    | {IGNORE|FORCE} {INDEX|KEY} [FOR {JOIN|ORDER BY|GROUP BY}] (index_list)

  index_list:
      index_name [, index_name] ...

- FROM clause indicates tables to select rows from.
  
- If no FROM clause, only arbitrary expressions (not referencing columns) can
  be selected. This is equivalent to specifying ``FROM DUAL`` dummy table.

- Table name can be fully qualified as ``db_name.tbl_name``, for tables in
  default database, unqualified table name is sufficient.

- Table name can be aliased in table reference, including in join expressions.
  When a table is aliased, the original name can not be used anymore, only
  alias can be used.

- A subquery must be assigned an alias, and may optionally include a list of
  table column names in parentheses.

  * The subquery must be a table subquery.

  * By default, column names are defined by SELECT list of subquery. This can
    be overriden by providing a list of table column names in parentheses.

- Different JOINs.

  * CROSS JOIN. Modeled after cross product, or Cartesian product. Each and
    every row in the first table is joined to each and every row in the second
    table.

  * INNER JOIN. Conceptually, CROSS JOIN two tables then returning only rows
    matching the join predicates. 由于 mysql 里 CROSS JOIN 和 INNER JOIN 都可以
    指定 join predicates, 所以是等价的.

  * LEFT [OUTER] JOIN. Outer JOINs can be LEFT JOIN and RIGHT JOIN, OUTER is
    optional. Conceptually, the union of INNER JOIN and left/right table. It's
    *outer*, because it returns all rows from the left/right side table, even
    if a row has no matching rows on the other side; whereas for INNER JOIN,
    only matching rows are included.
    
    In the case that no matching row is found, the row at the left/right table
    is included in the result for once, with NULL values for columns at the
    other side.

  * RIGHT [OUTER] JOIN. See above.

  * FULL [OUTER] JOIN. not supported by mysql. The union of LEFT OUTER JOIN and
    RIGHT OUTER JOIN.

  * NATURAL [INNER] JOIN. equivalent to INNER JOIN with a USING clause that
    automatically use all common columns in both tables.

  * NATURAL {LEFT|RIGHT} [OUTER] JOIN. equivalent to the corresponding normal
    JOINs with the aforementioned USING clause.

  * STRAIGHT_JOIN. similar to INNER JOIN or CROSS JOIN, except that the left
    table is always read before the right table. Used to manually enforce a
    join order to optimizer.

- In MySQL, JOIN, CROSS JOIN, INNER JOIN are syntactic equivalents, 注意这不包
  含 OUTER JOINs. Implicit cross join ``,``, CROSS JOIN and INNER JOIN, are
  equivalent in the absence of a join condition.
  
  From BNF grammar, we can see that all JOIN operators have higher precedence
  than the comma operator (,).

- ON clause specifies join predicates. It can be any conditional expression as
  the same form of a WHERE clause.

  对于 MySQL, join predicates 还可以放在 WHERE clause 中. [SOJoinWhere]_
  [SOCommaJoinDiff]_ 例如::

    SELECT * FROM a JOIN b ON (a.id = b.id)
    -- equivalent to
    SELECT * FROM a JOIN b WHERE a.id = b.id

  两者生成的 query plan 是完全相同的. 然而注意, 两种写法的 semantics 是有区别的.
  前者是通过条件来筛选要 join 的行, 生成一个表. 后者是先生成一个表, 然后过滤满
  足条件的行. 前者是更可读、意义更清晰的形式.

- USING clause is a shortcut predicate, matching rows where the specified
  columns in both tables must be equal. 此时, result table 中只包含一组
  matching columns, 不像 ON clause 中如果 ``a.col == b.col``, result table 中包
  含来自两个 table 的同名的列.

  The order of columns in result table:

  * coalesced USING columns of the two joined tables, in the order in which
    they occur in the first table.

  * columns unique to the first table, in appearing order.

  * columns unique to the second table, in appearing order.

filtering conditions
""""""""""""""""""""
- WHERE clause indicates the conditions that rows must satisfy to be selected
  from referenced tables. Omitting WHERE clause equals to constant true.  WHERE
  clause can not contain aggregate functions.

grouping
""""""""
- Each GROUP BY field can be: the same as ORDER BY.

- WITH ROLLUP. Causes aggregate result to include extra rows that represent
  higher-level (that is, super-aggregate) summary.

HAVING clause
"""""""""""""
- HAVING is used to conveniently filtering aggregated rows, i.e., filtering
  based on aggregated result.
  
- HAVING clause filters data on the group rows, rather than on individual
  source rows. Whereas WHERE clause filters on source rows.  HAVING is added
  just because WHERE can not filter on aggregate results. HAVING 和 WHERE 执行
  的阶段是不同的.

- HAVING 并不是必须的, 相同的结果可通过 filter on subquery 来实现, 即::

    SELECT ... WHERE where_condition GROUP BY ... HAVING having_condition;
    -- equivalent to
    SELECT * FROM (
      SELECT ... WHERE where_condition GROUP BY ...
    ) as grouped WHERE having_condition;

- In MySQL, the HAVING clause is applied nearly last, just before items are
  sent to the client, with no optimization. (LIMIT is applied after HAVING.)

- HAVING should reference only columns in the GROUP BY clause or columns used
  in aggregate functions. In mysql, HAVING can also refer to normal columns in
  select list and columns in outer subqueries.

WINDOW clause
"""""""""""""
- Defines named windows that can be referred to by window functions.

ordering
""""""""
- Each ORDER BY field can be:

  * a column name or its alias name. All columns and aliases in select list
    and FROM clause can be used.

  * an arbitrary expression, which can contain reference to any column name or
    its alias.

- Ordering direction. ascending or descending order. ASC is default.

- Actually when sorting, only first ``max_sort_length`` bytes of column values
  are used.

LIMIT clause
""""""""""""
- constrain the rows returned by SELECT statement.

- To retrieve all rows from a certain offset up to the end of the result set,
  row count can be some extremely large number.

- If LIMIT occurs within a subquery and also is applied in the outer query, the
  outermost LIMIT takes precedence.

locking read
""""""""""""
- FOR UPDATE and FOR SHARE are locking read clauses.

- FOR UPDATE. Rows selected by the query are write-locked until the end of the
  current transaction. Another transaction is forbidden from locking read of
  the same row. Non-locking reads can still read that row. It's useful when
  update must be considered an atomic operation.

- FOR SHARE. The shared lock permits other transactions to read the selected
  rows but not to update or delete them. It's useful when multiple sessions
  need readonly share of row values.

- By default, when the matching row is locked, other transactions are blocked.
  This can be changed with modifiers.

- Modifiers.

  * NOWAIT. Query execute immediately, returning an error if a row lock cannot
    be obtained due to a lock held by another transaction.

  * SKIP LOCKED. Query execute immediately, excluding rows from the result set
    that are locked by another transaction.

- ``OF tbl_name``. Specifying the table to be locked. Omitting this clause
  causes that all tables referenced by the query block are locked (for matching
  rows).

SELECT modifiers
""""""""""""""""
- ALL and DISTINCT specify whether duplicate rows should be returned. default
  is ALL.

SELECT ... INFO
"""""""""""""""
::

  SELECT ... INTO var_list

- select column values and stores them into variables.

- The number of variables must match the number of columns. The query should
  return a single row.

::

  SELECT ... INTO OUTFILE

- write selected rows into a file.

- intended primarily to let you very quickly dump a table to a text file on the
  server machine.

- This is the opposite of LOAD DATA. See LOAD DATA for formatting options.

::

  SELECT ... INTO DUMPFILE

- writes a single row to a file without any formatting.

UNION
"""""
::

  (SELECT ...)
  UNION [ALL | DISTINCT]
  (SELECT ...)
  [UNION [ALL | DISTINCT]
  (SELECT ...)]
  [ORDER BY {col_name | expr} [ASC | DESC], ...]
  [LIMIT {[offset,] row_count | row_count OFFSET offset}]

- The column names from the first SELECT statement are used as the column names
  for the results returned.

- Corresponding columns of each SELECT statement should have the same type. If
  data types do not match, the values retrieved by all of the SELECT statements
  are taken into consideration.

- The last SELECT can be SELECT ... INTO OUTFILE, then the UNION result is
  written to the file.

- Modifiers. ALL and DISINTCT specify whether duplicate rows are included. By
  default is DISTINCT.

- a DISTINCT union overrides any ALL union to its left.

- To apply ORDER BY or LIMIT to an individual SELECT, place the clause inside
  the parentheses that enclose the SELECT. Use of ORDER BY for individual
  SELECT statements implies nothing about the order in which the rows appear in
  the final result because UNION by default produces an unordered set of rows.
  Therefore, the use of ORDER BY in this context is typically in conjunction
  with LIMIT, so that it is used to determine the subset of the selected rows
  to retrieve for the SELECT. If ORDER BY appears without LIMIT in a SELECT, it
  is optimized away because it will have no effect anyway.

LOAD DATA
^^^^^^^^^
::

  LOAD DATA
    [LOW_PRIORITY | CONCURRENT] [LOCAL]
    INFILE 'file_name'
    [REPLACE | IGNORE]
    INTO TABLE tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [CHARACTER SET charset_name]
    [{FIELDS | COLUMNS}
        [TERMINATED BY 'string']
        [[OPTIONALLY] ENCLOSED BY 'char']
        [ESCAPED BY 'char']
    ]
    [LINES
        [STARTING BY 'string']
        [TERMINATED BY 'string']
    ]
    [IGNORE number {LINES | ROWS}]
    [(col_name_or_user_var
        [, col_name_or_user_var] ...)]
    [SET col_name={expr | DEFAULT},
        [, col_name={expr | DEFAULT}] ...]

- LOAD DATA 与 SELECT ... INTO 互逆.

file encoding
"""""""""""""
- File name is a string literal, interpreted based on ``character_set_filesystem``.
  
- ``CHARACTER SET`` clause specifies the encoding used by file content. By
  default, use ``character_set_database``.

concurrency
"""""""""""
- For engines that uses only table-level locking, ``LOW PRIORITY`` cause the
  statement's execution delayed until no other clients are reading from the
  table.

- ``CONCURRENT`` is useful with MyISAM engine.

local file
""""""""""
- ``LOCAL`` affects where the file is expected to be found:

  * With LOCAL, the file is read by the client program on the client host and
    sent to the server. A copy of the file is created in the directory where
    the MySQL server stores temporary files. 

  * Without LOCAL, the file must be located on the server host and is read
    directly by the server.

- Non-LOCAL load operations read text files located on the server. For security
  reasons, such operations require that you have the FILE privilege.

- 出于安全考虑, ``local_infile`` 默认是 OFF, 需要在 mysql client 和 mysqld
  同时开启.

duplicate handling
""""""""""""""""""
- The REPLACE and IGNORE modifiers control handling of input rows that
  duplicate existing rows on unique key values.

- If you do not specify either modifier, the behavior depends on whether the
  LOCAL modifier is specified. Without LOCAL, an error occurs when a duplicate
  key value is found, and the rest of the text file is ignored. With LOCAL, the
  default behavior is IGNORE.

field and line handling
"""""""""""""""""""""""
- Without FIELDS, LINES clauses, the default is the following::

    FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
    LINES TERMINATED BY '\n' STARTING BY ''

- Anything *after* line terminator and *before* the next line's start prefix is
  ignored.

- The IGNORE number LINES option can be used to ignore lines at the start of
  the file.

- When you use SELECT ... INTO OUTFILE in tandem with LOAD DATA to write data
  from a database into a file and then read the file back into the database
  later, the field- and line-handling options for both statements must match.

- If not empty, the FIELDS [OPTIONALLY] ENCLOSED BY and FIELDS ESCAPED BY
  values must be a single character.

column list specification
"""""""""""""""""""""""""
- By default, input lines are expected to contain a field for each table
  column, in the table column's defining order. Specify a column list to define
  explicitly the mapping between table columns and file fields.

- Column list can contain user variables, useful as
 
  * preprocessing variables.

  * dummy fields to consume redundant fields.

- In SET list, the LHS must be column name, RHS can contain:

  * user variables assigned by column list specs.

  * scalar subqueries.

  * Any functions, constants, etc.

- If an input line has too many fields, the extra fields are ignored and the
  number of warnings is incremented.

- If an input line has too few fields, the table columns for which input fields
  are missing are set to their default values.

- Note an empty field is different from a missing field. With empty field, it's
  equivalent to inserting an empty string to the corresponding column.

usage
""""""
- importing data written out by SELECT ... INTO OUTFILE

- importing data from an formatted external source, such as a CSV file.

INSERT
^^^^^^
INSERT ... VALUES
""""""""""""""""""
::

  INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
      [INTO] tbl_name
      [PARTITION (partition_name [, partition_name] ...)]
      [(col_name [, col_name] ...)]
      {VALUES | VALUE} (value_list) [, (value_list)] ...
      [ON DUPLICATE KEY UPDATE assignment_list]

- the parentheses-wrapped column list defines the corresponding columns to
  insert value lists. If column list is not provided, values for every column
  in the table must be provided by the VALUES list, in the defining order.

INSERT ... SET
""""""""""""""
::

  INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
      [INTO] tbl_name
      [PARTITION (partition_name [, partition_name] ...)]
      SET assignment_list
      [ON DUPLICATE KEY UPDATE assignment_list]

- The assignment list indicates the columns to be assigned, and their values.

- INSERT ... SET can only insert one row into the table.

INSERT ... query
""""""""""""""""
::

  INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
      [INTO] tbl_name
      [PARTITION (partition_name [, partition_name] ...)]
      [(col_name [, col_name] ...)]
      SELECT ...
      [ON DUPLICATE KEY UPDATE assignment_list]

- insert rows extracted by query.

- The column list acts like those in INSERT ... VALUES.

- The order in which a SELECT statement with no ORDER BY clause returns rows is
  nondeterministic.

- The target table of the INSERT statement may appear in the FROM clause of the
  SELECT part of the query. However, you cannot insert into a table and select
  from the same table in a subquery.

  To avoid ambiguous column reference problems when the SELECT and the INSERT
  refer to the same table, provide a unique alias for each table used in the
  SELECT part, and qualify column names in that part with the appropriate
  alias.

ON DUPLICATE KEY UPDATE
"""""""""""""""""""""""
- enables existing rows to be updated if a row to be inserted would cause a
  duplicate value in an unique index.

- 对于每个本来要 INSERT 的 row, 最多进行一次 UPDATE. 也就是说, 对于一次插入
  多行的情况, 可能会 UPDATE 多次, 但不会多于行数.

- With ON DUPLICATE KEY UPDATE, the affected-rows value per row is 1 if the row
  is inserted as a new row, 2 if an existing row is updated, and 0 if an
  existing row is set to its current values. 

- For INSERT ... VALUES, RHS of assignment list in the ON DUPLICATE KEY UPDATE
  clause can use the ``VALUES(col_name)`` function to refer to column values
  from the INSERT portion.

- For INSERT ... query, RHS of assignment list in the ON DUPLICATE KEY UPDATE
  clause can reference columns from the query. Restrictions:

  * Columns of a single table or a join over multiple tables can be referenced.

  * To refer to columns of a UNION or GROUP BY's resulting table, a derived
    table must be used::

      SELECT * FROM (... UNION ...) AS t

- privilege: requires UPDATE privilege for the columns to be updated.

privileges
""""""""""
- require INSERT privilege for the table.

about values
""""""""""""
- For any column value of a row, it's either provided by INSERT statement or
  using the column's default value.

- If strict SQL mode is enabled, an INSERT statement generates an error if it
  does not specify an explicit value for every column that has no default
  value.

- Use the keyword DEFAULT to set a column explicitly to its default value.

- A value expression can refer to any column that was set earlier in a value
  list.

modifiers
"""""""""
- LOW_PRIORITY, HIGH_PRIORITY. affects only storage engines that use only
  table-level locking.

- IGNORE. errors that occur while executing the INSERT statement are ignored.
  The offending row is discarded and operation continues.

UPDATE
^^^^^^
::

  UPDATE [LOW_PRIORITY] [IGNORE] table_references
    SET assignment_list
    [WHERE where_condition]
    [ORDER BY ...]
    [LIMIT row_count]

  assignment_list:
    assignment [, assignment] ...

  assignment:
    col_name = value

  value:
    {expr | DEFAULT}

- UPDATE can be for single-table or for multiple tables.

- If ``expr`` contains column names from the table to updated, UPDATE uses the
  current value of the column, 此外注意 assignments are evaluated from left to
  right. 例如, ``UPDATE t1 SET col1 = col1 + 1, col2 = col1`` 中, 第二个赋值使
  用第一个赋值更新的值.
  
- For multiple tables, ``table_references`` is a table join expression. 即使一
  个 row 在 joined table 中出现多次 (例如 join 导致 FK 指向的行出现多次), 它也
  会只更新一次.

- The WHERE clause, if given, specifies the conditions that identify which rows
  to update. With no WHERE clause, all rows are updated.

- If the ORDER BY clause is specified, the rows are updated in the order that
  is specified.

- The LIMIT clause is a rows-matched restriction. The statement stops as soon
  as it has found ``row_count`` rows that satisfy the WHERE clause, whether or
  not they actually were changed.

- For multiple table update, ORDER BY and LIMIT can not be used.

- Privileges: need UPDATE privilege only for columns referenced in an UPDATE
  that are actually updated. need only the SELECT privilege for any columns
  that are read but not modified.

- UPDATE returns the number of rows that were actually changed.

DELETE
^^^^^^
- A DML that removes rows from a table(s).

single table syntax
"""""""""""""""""""
::

  DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name [[AS] tbl_alias]
    [PARTITION (partition_name [, partition_name] ...)]
    [WHERE where_condition]
    [ORDER BY ...]
    [LIMIT row_count]

- delete rows from ``tbl_name`` and returns the number of deleted rows.

multiple table syntax
"""""""""""""""""""""
::

  DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
      tbl_name [, tbl_name] ...
      FROM table_references
      [WHERE where_condition]

  DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
      FROM tbl_name [, tbl_name] ...
      USING table_references
      [WHERE where_condition]

- delete rows from one or more tables depending WHERE conditions.
  ``table_references`` constructs the rows to be filtered by WHERE clause.
  根据筛选出来的 joined rows, 推出来自各个表的原始行, 进行删除.

- Syntax of ``table_references`` aligns with the SELECT statement.

- 对于第一种格式, FROM 前面列出的表中的匹配行被删除; 对于第二种格式, FROM 后面
  USING 前面的列出的表中的匹配行被删除. The effect is that you can delete rows
  from many tables at the same time and have additional tables that are used
  only for searching.

WHERE clause
""""""""""""
- WHERE clause identifies which rows to delete. Without WHERE clause, all rows
  from ``tbl_name`` for single table syntax, or all rows from
  ``table_references`` for multiple table syntax are deleted.

ORDER BY and LIMIT
""""""""""""""""""
- If the ORDER BY clause is specified, the rows are deleted in the order that
  is specified. The LIMIT clause places a limit on the number of rows that can
  be deleted.

- ORDER BY and LIMIT can only be used in single table syntax.

privileges
""""""""""
- the DELETE privilege on a table to delete rows from it.
  
- the SELECT privilege for any columns that are only read.

performance
"""""""""""
- TRUNCATE TABLE is faster than a DELETE without WHERE.

auto-increment column behavior
""""""""""""""""""""""""""""""
- deleting the row containing the maximum value for an ``AUTO_INCREMENT``
  column, the value is not reused for a MyISAM or InnoDB table. 

- deleting all rows in the table (by DELETE without a WHERE clause) in
  autocommit mode, the sequence starts over for all storage engines except
  InnoDB and MyISAM.

REPLACE
^^^^^^^
::

  REPLACE [LOW_PRIORITY]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    VALUES (value_list) [, (value_list)] ...

  REPLACE [LOW_PRIORITY]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    SET assignment_list

  REPLACE [LOW_PRIORITY]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...

- Similar to INSERT, except that if an old row in the table has the same value
  as a new row for a PRIMARY KEY or a UNIQUE index, the old row is deleted
  before the new row is inserted.

  * 对于 REPLACE ... SET, ``assignment_list`` 对 unique index 列设置的值决定
    去替换哪些行.

- A REPLACE statement either inserts or deletes and inserts.

- REPLACE makes sense only if a table has a PRIMARY KEY or UNIQUE index.
  Otherwise, it becomes equivalent to INSERT, because there is no index to be
  used to determine whether a new row duplicates another.

- Values for all columns are taken from the values specified in the REPLACE
  statement. Any missing columns are set to their default values

- When setting values for new row, the original row's values can not be
  referred. If original value of a column is referred, it's replaced by the
  column's default value.

- privileges: INSERT and DELETE.

- If a generated column is replaced explicitly, the only permitted value is
  DEFAULT.

- The REPLACE statement returns a count to indicate the number of rows
  affected. This is the sum of the rows deleted *and* inserted. 

- Procedure performed for REPLACE.

  1. Try to insert the new row into the table

  2. If the insertion fails because of a duplicate-key error for a primary key
     or unique index:
     
     a. Delete from the table the conflicting row that has the duplicate key
        value.

     b. Try again to insert the new row into the table

WITH
^^^^
::

  WITH [RECURSIVE]
      cte_name [(col_name [, col_name] ...)] AS (subquery)
      [, cte_name [(col_name [, col_name] ...)] AS (subquery)] ...

- WITH is used to build common table expression (CTE), which is a named
  temporary result set that exists within the scope of a single statement and
  that can be referred to later within that statement, possibly multiple times.

- A CTE name defined earlier can be referenced in CTEs defined later, enabling
  CTEs to be defined based on other CTEs.

- A CTE in a given query block can refer to CTEs defined in query blocks at a
  more outer level, but not CTEs defined in query blocks at a more inner level.

- A CTE can refer to itself to define a recursive CTE. The RECURSIVE keyword
  must be included if any CTE in the WITH clause is recursive.

  The structure of a cursive CTE:

  * The recursive CTE subquery has two parts, separated by UNION [ALL] or UNION
    DISTINCT. The first SELECT produces the initial row or rows for the CTE and
    does not refer to the CTE name. The second SELECT produces additional rows
    and recurses by referring to the CTE name in its FROM clause. Recursion
    ends when this part produces no new rows.

  * The types of the CTE result columns are inferred from the column types of
    the nonrecursive SELECT part only, and the columns are all nullable.

  * Each iteration of the recursive part operates only on the rows produced by
    the previous iteration.

  * If the recursive part of a CTE produces wider values for a column than the
    nonrecursive part, it may be necessary to widen the column in the
    nonrecursive part to avoid data truncation.

  * The recursive SELECT part must reference the CTE only once and only in its
    FROM clause, not in any subquery. It can reference tables other than the
    CTE and join them with the CTE. If used in a join like this, the CTE must
    not be on the right side of a LEFT JOIN.

  Recursive CTE examples:

  .. code:: sql

    WITH RECURSIVE dates (date) AS
    (
      SELECT MIN(date) FROM sales
      UNION ALL
      SELECT date + INTERVAL 1 DAY FROM dates
      WHERE date + INTERVAL 1 DAY <= (SELECT MAX(date) FROM sales)
    )
    SELECT dates.date, COALESCE(SUM(price), 0) AS sum_price
    FROM dates LEFT JOIN sales ON dates.date = sales.date
    GROUP BY dates.date
    ORDER BY dates.date;

- Column names of a CTE can be specified after ``cte_name`` or provided by
  subquery.

- WITH clause can be used with SELECT, UPDATE, DELETE statements. For SELECT
  statement, it can be associated with any kind of SELECT, including subquery,
  statements that include a SELECT (e.g., INSERT ... query).

- CTE and derived tables often can be used interchangeably. However, CTEs have
  some advantages over derived tables:

  * A derived table can be referenced only a single time within a query. A CTE
    can be referenced multiple times. To use multiple instances of a derived
    table result, you must derive the result multiple times.

  * A CTE can be self-referencing (recursive).

  * One CTE can refer to another.

  * A CTE may be easier to read because its definition appears at the beginning
    of the statement rather than embedded within it.

SHOW CREATE TABLE
^^^^^^^^^^^^^^^^^
::

  SHOW CREATE TABLE tbl_name

- 显示的 CREATE TABLE statement 是与当前 table definition 一致的, 而不一定是最
  初创建 table 时使用的 statement.

SHOW TABLES
^^^^^^^^^^^
::

  SHOW [EXTENDED] [FULL] TABLES
    [{FROM|IN} <db_name>] [LIKE <pattern> | WHERE <expr>]

- base tables and views are listed. temporary tables are not listed.

- EXTENDED shows also hidden tables created by failed ALTER TABLE statements.

- FULL displays tables' type: BASE TABLE for a table, VIEW for a view, or
  SYSTEM VIEW for an INFORMATION_SCHEMA table. 这样可以区分 table 和 view.

- Only tables you have some privileges are shown.

- table infos are stored in INFORMATION_SCHEMA.TABLES table.

SHOW COLUMNS
^^^^^^^^^^^^
::

  SHOW [EXTENDED] [FULL] {COLUMNS | FIELDS}
    {FROM | IN} tbl_name
    [{FROM | IN} db_name]
    [LIKE 'pattern' | WHERE expr]

- normal output fields: Field, Type, Null, Key, Default, Extra.

- ``tbl_name`` can be fully-qualified, thus eliminate the need for the ``{FROM
  | IN} db_name`` clause.

- When showing table in current default database, the second ``FROM`` clause
  can also be omitted.

- EXTENDED include information about hidden columns that MySQL uses internally
  and are not accessible by users.

- FULL include the column collation and comments, as well as the privileges you
  have for each column. (Collation, Privileges, Comment fields.)

- LIKE, filter output by column name using patterns.

- WHERE, filter output by general conditions.

- output field explanations:

  * Field. column name.

  * Type. column data type.

  * Collation. For nonbinary string columns, otherwise NULL.

  * Null. yes if nullable, no otherwise.

  * Key.

    - Empty, when the column is not indexed or is indexed only as a secondary
      column in a multiple-column, nonunique index.

    - PRI, one of the columns in a PRIMARY KEY.

    - UNI. the first column in a UNIQUE index.

    - MUL. the first column in a nonunique index.

    If more than one of the Key values applies to a given column of a table,
    Key displays the one with the highest priority, in the order PRI, UNI, MUL.

    A UNIQUE index may be displayed as PRI if it cannot contain NULL values and
    there is no PRIMARY KEY in the table. A UNIQUE index may display as MUL if
    several columns form a composite UNIQUE index; although the combination of
    the columns is unique, each column can still hold multiple occurrences of a
    given value.

  * Default. default value of the column. This is NULL if the column has an
    explicit default of NULL, or if the column definition includes no DEFAULT
    clause, 即使该列定义为 NOT NULL.

  * Extra. additional information about a column.

    - ``AUTO_INCREMENT``

    - ``ON UPDATE CURRENT_TIMESTAMP``

    - ``VIRTUAL GENERATED`` virtual generated column

    - ``VIRTUAL STORED`` stored generated column

    - ``DEFAULT_GENERATED`` expression default value

  * Privileges. a comma separated list of privileges.

  * Comment. column's comment.

EXPLAIN
^^^^^^^
For table structure
"""""""""""""""""""
::

  EXPLAIN tbl_name [col_name | wild]

- A simplified version of SHOW COLUMNS.
  
- output in the same format as does SHOW COLUMNS.

- If ``col_name`` or ``wild`` pattern is specified, only show information about
  this column or matching columns.

- ``wild`` uses the same pattern as does ``LIKE`` operator.

For execution plan
""""""""""""""""""
See `Query Execution Plan`_ for detail.

DESCRIBE
^^^^^^^^
- synonymous to EXPLAIN. But usually used for obtain information about table
  structure.

subquery syntax
^^^^^^^^^^^^^^^
- A subquery is a query statement within another statement.

- It's possible to nest subqueries within other subqueries to a considerable
  depth.

- A subquery is always surrounded by parentheses.

- scalar, column, row, table subquery: A subquery that returns a scalar, a
  column of values, a single row, or a table.

- A subquery's outer statement can be any of: SELECT, INSERT, UPDATE, DELETE,
  SET or DO.

- In general, tables containing NULL values and empty tables are “edge cases.”
  *When writing subqueries, always consider whether you have taken those two
  possibilities into account.*

- correlated subquery. A subquery that contains a reference to a table that
  also appears in the outer query.

  * For subqueries in HAVING or ORDER BY clauses, MySQL also looks for column
    names in the outer select list.

- In MySQL, you cannot modify a table and select from the same table in a
  subquery.

scalar subquery
""""""""""""""""
- A scalar subquery can be used almost anywhere a single column value or
  literal is legal. But if a statement permits only a literal value, you cannot
  use a subquery.

- The result of a scalar query has characteristics that all operands have: a
  data type, a length, an indication that it can be NULL, and so on.

- If the subquery result is empty, the result is NULL.

- A scalar subquery can be part of an expression, but remember the parentheses,
  even if the subquery is an operand that provides an argument for a function.::

    SELECT UPPER((SELECT c FROM t));

- scalar subquery in comparison::

    non_subquery_operand comparison_operator (subquery)

- Some of the subquery comparisons can be achieved using table joins. But not
  all of them can.

row subqueries
""""""""""""""
- A row subquery returns a single row that contains any number of columns.
  Can be used in row subquery comparison.

- A row constructor is either of the two::

    (col1, col2, ...)
    ROW(col1, col2, ...)

- In a row subquery comparison, a row constructor is compared against the
  result of a row subquery.::

    row_constructor comparison_operator (subquery)

  * When the subquery produces no rows, the expression is NULL.

  * For a comparison of the subquery to a row constructor, the subquery must be
    a row subquery that returns the same number of columns.

  * In a row subquery comparison, the row subquery must returns at least two
    columns.

column subqueries
""""""""""""""""""
- subquery that returns multiple rows of single column values.
  Can be used in ANY, IN, SOME, ALL comparisons.

table subqueries
""""""""""""""""
- subqueries that returns a table of data. can be used in

  * FROM clause of SELECT.

  * IN comparison where the LHS is a row constructor.

subqueries with ANY, IN, SOME, ALL comparison
""""""""""""""""""""""""""""""""""""""""""""""
- format::

  operand comparison_operator {ANY | SOME} (subquery)
  operand IN (subquery)
  operand comparison_operator ALL (subquery)

- ANY/SOME. return TRUE if the comparison is TRUE for ANY of the values in the
  column that the subquery returns. 注意 subquery must be a column subquery.

  * SOME is alias to ANY. SOME is useful when comparison operator is negated::

      SELECT s1 FROM t1 WHERE s1 != SOME (SELECT s1 FROM t2);
      SELECT s1 FROM t1 WHERE s1 != ANY (SELECT s1 FROM t2);

    注意到第二句的字面意思与它的实际 semantics 是不同的, 所以 SOME 更合适.

  * the comparison is NULL if the column values of all rows from subquery are
    NULL.

- IN. IN is alias for ``= ANY``. NOT IN is an alias for ``!= ALL``.

- ALL. return TRUE if the comparison is TRUE for ALL of the values in the
  column that the subquery returns.

  * the comparison is NULL if the column values from subquery contains NULL and
    all other non-NULL column values satisfying the comparison.::

      SELECT 1 > ALL (SELECT 0 UNION ALL SELECT NULL); -- returns NULL.

  * the comparison is True if subquery is empty.

subqueries with EXISTS or NOT EXISTS
""""""""""""""""""""""""""""""""""""
::

  EXISTS (subquery)
  NOT EXISTS (subquery)

- Tests whether subquery returns any rows at all. Even rows with NULL values.

- MySQL ignores select list in a subquery that tests whether there's any rows,
  because it's the conditional clauses that are important.

subquery optimization
""""""""""""""""""""""
- MySQL executes uncorrelated subqueries only once. Use EXPLAIN to make sure
  that a given subquery really is uncorrelated.

- MySQL rewrites IN, ALL, ANY, and SOME subqueries in an attempt to take
  advantage of the possibility that the select-list columns in the subquery are
  indexed.

- Sometimes rewriting subqueries as joins can make query more efficient.

Transaction
===========
- A transaction is an atomic operation that can be committed or rolled back.
  All changes made in a transaction are applied atomically or none applied.

- InnoDB transactions have ACID properties -- atomicity, consistency,
  isolation, and durability.

- autocommit: causes an implicit commit operation after each SQL statement.
  Default on.
 
  enable or disable autocommit for current session.::

    SET autocommit = {0 | 1}

statements causing implicit commit
----------------------------------
Some statements are handled in its own special transaction, such that they
implicitly end any transaction active in the current session (as if with
``COMMIT``) and also cause an implicit commit after executing (除了 transaction
control and locking statements).

- DDL statements that define or modify database objects (with some additional
  details).

- Statements that implicitly use or modify tables in the ``mysql`` database.
  E.g., account system admin statements.

- Transaction-control and locking statements (with some additional details).
  这些语句不会在执行后再 commit 一次.

- Some admin statements: ANALYZE TABLE, CACHE INDEX, CHECK TABLE, FLUSH, LOAD
  INDEX INTO CACHE, OPTIMIZE TABLE, REPAIR TABLE, RESET.

- Replication control statements.

SQL statements
--------------
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

- 输出内容包括:

  * ``Maxlen`` column 是单个字符所需最大 bytes.

  * ``Default collation`` of the charset.

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

collations
""""""""""
- Never use ``utf8mb4_general_ci``, use ``utf8mb4_unicode_ci`` or better
  ``utf8mb4_unicode_520_ci``, or even better ``utf8mb4_0900_ai_ci``.
  See also [SOUTF8Difference]_.

- For 8.0+, ``utf8mb4_0900_ai_ci`` is the default collation for utf8mb4.

- 如何修改成更好的 collation?
 
  * 考虑到不同 mysql 版本, utf8mb4 的 collation 总是变 (不断变得更好), 最简单
    的办法是不在任何层设置明确的 collation, 依赖数据库升级后自动升级默认的
    collation. 然后重新创建数据库, 导入数据. 这个前提是数据不太庞大.

  * 如果数据太多, 则只能挨个 ``ALTER DATABASE``, ``ALTER TABLE``.

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

  1. 只修改指定表和数据库的 charset.
       
     备份所有数据.

     保存一份当前数据库内的所有表定义, 用于修改后进行对比.::

       mysql -B >output-file <<EOF
       SELECT * FROM information_schema.COLUMNS
       WHERE TABLE_SCHEMA = 'enoc' order by TABLE_NAME, ORDINAL_POSITION
       EOF

     修改需要转换的表 (包含所有列) 和数据库的 default charset::

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

  2. 修改服务器上所有表和数据库的 charset 默认使用 utf8mb4 charset. 这需要重新
     部署 mysql 服务器, 再恢复数据.
       
     mysqldump 所需备份数据.

     重新部署 MySQL. 设置如上配置文件. 以保证所有数据库和表都是 utf8mb4. 恢复数据.

     恢复数据后按照 1 中的方式修改恢复的数据库和表中的 charset.


Functions and Operators
=======================
String Functions and Operations
-------------------------------
String Comparison Functions and Operatiors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
LIKE
""""
- SQL pattern

  * ``_``: any single character, equivalent to ``?`` in shell.

  * ``%``: any number of any character, equivalent to ``*`` in shell.

- ``LIKE`` 后面的 SQL pattern 必须匹配整个字符串, 才算匹配.

Regular Expressions
^^^^^^^^^^^^^^^^^^^
- ``RLIKE`` ``REGEXP`` 后面的正则 pattern 只需字符串的任何地方匹配即可, 类似
  python 中的 ``re.search``.

Aggregate Functions
-------------------
- ``COUNT()`` does not count NULL values. 因此若某个列中有 NULL, ``count(<col>)``
  不等于 ``count(*)``.

Date and Time Functions
-----------------------
- ``CURDATE()``, ``CURRENT_DATE()``. format: ``YYYY-MM-DD``.

Information Functions
---------------------
- ``VERSION()``. mysql server version, in utf-8 encoding. see also ``version``
  system variable.

- ``DATABASE()``. name of the default database, in utf-8. If no default,
  returns NULL.

- ``DEFAULT(col)``. default value for a table column. Column name can be
  qualified. This function is permitted only for columns that have a literal
  default value, not for columns that have an expression default value.

Stored Programs and Views
=========================

view
----
- 对于定义的 view, 只保存了创建这个 view 的 SQL 语句. 在每次查询 view 时, 执行
  SQL, 生成相应的数据. 所以本质上, view 只是将复杂的 SQL 保存了下来, 以方便重用
  而已.

Optimization
============
order by
--------
.. XXX 确认以下说法

- 当 order by 的列组合不能充分确定行的顺序时, 对于每个欠排序的部分中的多行, 其
  输出顺序貌似是 undefined. 对于实体表, 似乎可以保证这个输出顺序在跨 session 多
  次查询时的一致性 (也许是对应于 index 或 file sort 给出的顺序); 对于 UNION 等
  涉及临时生成的表, 无法保证跨 session 多次查询时的一致性 (也许因为 UNION 本身
  给出 an unordered set of rows), 只能保证一个 session 内部多次查询的一致性.

index
-----

See also [SOIndexWorking]_.

terms
^^^^^
- cardinality. The number of unique values in a table column.

- selectivity. A data's selectivity by a column is the number of distinct
  values in a column (i.e., its cardinality) divided by the number of records
  in the table. High selectivity means that the column values are relatively
  unique, and can retrieved efficiently through an index.

- clustered index. the primary key index in innodb. 由于在 innodb 中, 行数据
  完全是在 primary key index 这个 b-tree 结构中, 所以称为 "cluster".

- secondary index. All indexes except clustered index. A secondary index can be
  used to satisfy covering index queries.  For more complex queries, it can be
  used to identify the relevant rows in the table, which are then retrieved
  through lookups using the clustered index.

- Covering index. 这是一种查询语句优化操作. 当查询语句可通过走索引完全满足时,
  MySQL 会直接从索引获取结果, 无需访问 clustered index, 从而提高查询速度.

What is index
^^^^^^^^^^^^^
索引是一个数据结构, 它将一个或多个列的数据按照一定顺序 (升序或降序) 排列, 以
达到快速查询所需数据行的目的. 在索引中的每个项, 保存了指向相应数据行的指针,
这样可以根据确定的列值直接 seek 到对应的数据行.

索引抽象结构::

  ^
  |
  -----------------------------
  column value | pointer to row
  -----------------------------
  |
  V

Why need index
^^^^^^^^^^^^^^
在没有索引的情况下, 基于一个列的值对表数据进行搜索, 必须使用 linear search, 这
样时间复杂度是 O(n), 其中 n 是表中的数据行数. 当对一个列建立索引后, 由于索引
中的列值是 sorted, 可以使用数搜索, 搜索的时间复杂度是 O(log n), 对于 B-tree 索
引. 因此, 使用索引能极大地提高数据查询性能.

Advantages and disadvantages of index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
advantages:

- 大大提高查询效率.

索引的两方面代价:

- 维护索引的时间成本. 在每次数据修改时 (插入、更新、删除等), 相关的索引都
  必须更新.

- 索引数据的空间占用. 索引占用的体积相对与原数据表而言是可观的. 当数据量大时,
  索引占用空间也会非常大.

When index is used
^^^^^^^^^^^^^^^^^^
- Matching a WHERE clause.

- To retrieve rows from other tables when performing joins.

- To find ``MIN()``, ``MAX()`` for a column.

- To sort or group a table if the sorting or grouping is done on a leftmost
  prefix of a usable index.

- 当查询语句可通过 covering index 优化完成时.

index types and data structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

B-tree
""""""
- used for: PRIMARY KEY, UNIQUE, INDEX

- B-tree 适合 lookup for exact matches (equals operator) and ranges.

- B-tree index 是有序的, 升序或降序.

Inverted index
""""""""""""""
used for: FULLTEXT index.

R-tree
"""""""
used for: indexes on spatial data types.

Hash index
""""""""""
- used for: default index type for MEMORY table.

- hash index 适合 lookup for exact matches, rather than ranges.

- hash index is only available for MEMORY storage engine.

- hash index 是无序的, 不支持排序.

- The MEMORY storage engine can also use B-tree indexes, and you should choose
  B-tree indexes for MEMORY tables if some queries use range operators.

Composite Index
^^^^^^^^^^^^^^^
- Composite index (复合索引) is multi-column index.

- 一个包含多列的索引自动即成为所谓复合索引. 一个索引最多可以包含 16 个列.

- 一个复合索引可以用在对所有 index prefix 部分的列的查询条件上, 只要查询条件
  对列的顺序要求与 index prefix 部分一致即可.

- 复合索引中的每个索引值可理解为是各个列的值的 concatenation. 因此索引的构建顺
  序是按照列的优先级顺序进行排序的. 例如::

    column 1 | column 2 | column 3
    ABC
    ABD
    ACD
    ADE
    BAB
    BAC
    BBA
    BBB
    ...


Index name
^^^^^^^^^^
- PRIMARY KEY's name is PRIMARY.

- secondary index's name is specified by programmer, or assigned the same name
  as the first indexed column, with an optional suffix (``_2``, ``_3``, ...) to
  make it unique.

SQL statements
^^^^^^^^^^^^^^
CREATE INDEX
""""""""""""
::

  CREATE [UNIQUE | FULLTEXT | SPATIAL] INDEX index_name
      ON tbl_name (key_part, ...)
      [index_option]
      [algorithm_option | lock_option]

  key_part: {col_name [(length)] | (expr)} [ASC | DESC]

  index_option:
      KEY_BLOCK_SIZE [=] value
    | index_type
    | WITH PARSER parser_name
    | COMMENT 'string'
    | {VISIBLE | INVISIBLE}

  index_type:
      USING {BTREE | HASH}

  algorithm_option:
      ALGORITHM [=] {DEFAULT | INPLACE | COPY}

  lock_option:
      LOCK [=] {DEFAULT | NONE | SHARED | EXCLUSIVE}
    
- CREATE INDEX is mapped to ALTER TABLE. It can not create primary key or
  foreign key, but ALTER TABLE can.

- Index prefix length:

  * can be specified for CHAR, VARCHAR, BINARY, VARBINARY, TEXT-related,
    BLOB-related columns.
 
  * required for TEXT and BLOB related columns.

  * prefix length is measured in bytes for binary string types, and in
    characters for text string types.

  * Permissible prefix length is determined by InnoDB row format.

- Functional key parts: ``(expr)``

  * Functional key part 相当于单独创建 virtual generated column 并配合创建包含
    这列的索引. 当创建包含 functional key part 的索引时, 同时会创建一个 hidden
    virtual generated column, 对应于这个 key part. 这样, 仍然保证了每个 key
    part 对应一个 column.

  * A functional key part indexes expression value rather than column or
    column prefix value.

  * column values can be referenced in the expression.

  * A functional key part must be enclosed in parentheses, even if it's a
    single literal.

  * A functional key part cannot consist solely of a column name, even enclosed
    in parentheses.

  * A composite index can have functional and normal key parts.

  * UNIQUE index can have functional key parts.

  * FULLTEXT, SPATIAL index can not have functional key parts, 因为 doesn't
    make sense.

  * primary key index can not have functional key parts, 因为 primary key 要尽
    量不变且没有依赖, 而 functional key parts 的意义就是依赖其他列与变化.

  * 在查询时, mysql 会根据 query condition 适时使用 functional index.

- Index order: ASC or DESC specify index values are stored in ascending or
  descending order. Default is ASC. Index order is not permitted for HASH
  indexes.

- Unique index. Requires every value in the index to be unique. 也就是说, 对于
  表中的每行, 所有 key parts 的组合必须是唯一的.

  * 若 column 本身允许 NULL, 则 index 中允许多个 NULL 值, 不算违反 UNIQUE.

  * When only the prefix of a column is indexed, it's the uniqueness of the
    prefix that is considered.

  * When a PRIMARY KEY or a UNIQUE NOT NULL index contains a single column that
    is of integer type, ``_rowid`` can be used to refer to the column in SELECT
    statements.

- Full-text index.

  * For full-text searches.

  * can include only CHAR, VARCHAR, TEXT-related columns.

  * index prefix length unsupported.

  * can include NULL.

- Spatial index.

  * can include only spatial data types.

  * indexed columns must be NOT NULL.

- index options.

  * USING type.
    
    * 只有 MEMORY table 的普通索引才可能需要指定 index type, 即在 HASH, BTREE
    中选择, 其他 engine 的普通索引只有 BTREE.
    
    * 对于 FULLTEXT, SPATIAL index, 不能选择, 因它们使用的数据结构是确定的.

  * WITH PARSER is used for FULLTEXT index.

  * COMMENT can be up to 1024 chars.

  * VISIBLE, INVISIBLE. Index is visible by default.

design pattern
^^^^^^^^^^^^^^
- primary key index 的设计.

  * 一个表应该有明确定义的 primary key. 这有助于依据关键信息进行高效检索.  (即
    使建表人不创建 primary key, innodb 也会自动创建一个隐藏的 cluster index 来
    组织表结构).

  * 选择几乎或完全不需要修改的列 (组合) 作为 primary key index. 因修改
    clustered index is expensive.

  * primary key index 应该尽量短. 因为所有 secondary index 中都要存一份 primary
    index value.

- Create right index to answer the required question. 不要创建不必要的
  索引, 因为:

  * 在空间上索引要占用内存和存储;

  * 在时间上创建和更新索引需要时间, 每次 insert, update, delete 的过程中,
    都需要完成相关索引的更新.

- 若索引相关的列并没有查询需要, 而只是输出, 则没有必要创建索引.

- 如果能够满足需求的话, 查询语句应利用 mysql 的 covering index 操作, 来优化
  查询速度.

- 若数据行数比较小, 则索引并没有那么重要, 因全表扫描也不会慢多少.

- 若查询语句需要返回一个表的绝大部分或全部行, 全表顺序遍历比使用索引更快.
  Because sequential reads minimize disk seeks, even if not all the rows are
  needed for the query.

- An index with low selectivity is useless. MySQL processes the query
  differently depending on the selectivity of the index. 当 selectivity 比较低
  时, 不会使用相应的 index, 这个 index 就变成了只会增加负担, 但没有用处的废物.

- 当列值的分布非常不均匀时, 对于某些列值 (对应的行数比较少时) 的查询可能使用索
  引比较高效, 而对于另一些列值 (对应的行比较多时) 的查询使用索引比较低效. In
  such a case, you might need to use index hints to pass along advice about
  which lookup method is more efficient for a particular query.

- Hashed column as alternative to wide index spanning multiple columns.
  如果索引涉及的列比较多, 可能查询起来更快的方式是添加一个 indexed hash column,
  其值是这些需要索引的列的 concatenation 的 hash. 查询方式::

    SELECT * FROM tbl_name
      WHERE hash_col=MD5(CONCAT(val1,val2))
      AND col1=val1 AND col2=val2;

Query Execution Plan
--------------------
SQL statements
^^^^^^^^^^^^^^
EXPLAIN
""""""""
::

  EXPLAIN [explain_type] {explainable_stmt | FOR CONNECTION connection_id}

  explain_type: {
      FORMAT = format_name
  }
  
  format_name: {
      TRADITIONAL
    | JSON
  }
  
  explainable_stmt: {
      SELECT statement
    | DELETE statement
    | INSERT statement
    | REPLACE statement
    | UPDATE statement
  }

- Can explain execution of INSERT, UPDATE, DELETE, REPLACE, SELECT statements.

- When used with FOR CONNECTION connection_id rather than an explainable
  statement, it displays the execution plan for the statement executing in the
  named connection.

- MySQL displays information from the optimizer about the statement execution
  plan, i.e., how it would process the statement.

- output format:

  * TRADITIONAL. output in tabular format.

  * JSON. output in JSON format. containing more detailed info than
    traditional.


InnoDB storage engine
=====================
features
--------
InnoDB is fully transactional and supports foreign key references.

On-Disk Structures
------------------
- For file-per-table tablespace or general tablespace, a table's data and
  indexes are stored in ``.ibd`` file, under its belonging database's
  directory.

- In the created table, the clustered index (PRIMARY KEY) is placed first,
  followed by all UNIQUE indexes, and then the nonunique indexes.

- For system tablespace, table's data and indexes are stored in ``ibdata*``
  file.

Row formats
-----------

options
-------
- ``--innodb-flush-log-at-trx-commit[=#]``, ``innodb_flush_log_at_trx_commit``.

- ``--innodb-file-per-table``, ``innodb_file_per_table``.

- ``foreign_key_checks``. whether to check foreign key constraints during
  various DML operations. default ON.

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


Access Privilege System
-----------------------

Privilege types
^^^^^^^^^^^^^^^
Static privileges
"""""""""""""""""
Administrative privileges can only be granted at global level, other static
privileges can be granted at all level.

- ALL PRIVILEGES. Grant all privileges at specified access level, except
  GRANT OPTION and PROXY.

  * ALL PRIVILEGES at the global level grants all static global privileges and
    all currently registered dynamic privileges. A dynamic privilege registered
    subsequent to execution of the GRANT statement is not granted retroactively
    to any account.

- USAGE. synonym to "no privileges". useful for grant ``WITH GRANT OPTION``.

- GRANT OPTION. enable privileges to be granted to or removed from other
  accounts.

  * When you grant a user the GRANT OPTION privilege at a particular privilege
    level, any privileges the user possesses at that level can also be granted
    by that user to other users.

  * 由于该权限不是一个权限 per se, 而是关于授予其他权限. 所以它的语法是
    ``WITH GRANT OPTION``, 与其他权限不同.

Dynamic privileges
""""""""""""""""""
Dynamic privileges are all global and can only be granted globally.

Privilege levels
^^^^^^^^^^^^^^^^
- global level.

  * MySQL stores global privileges in the ``mysql.user`` system table.

  * When granting, use ``*.*``.

- database level.

  * MySQL stores database privileges in the ``mysql.db`` system table.

  * When granting, ``*`` represents the current default database, rather than
    global level.

- table level.

  * MySQL stores table privileges in the ``mysql.tables_priv`` system table.

  * When granting, a unqualified ``tablename`` represents a table in the
    current default database.

  * They can be granted to tables and views.

- column level.

  * MySQL stores column privileges in the ``mysql.columns_priv`` system table.

- routine level.

  * MySQL stores routine-level privileges in the ``mysql.procs_priv`` system
    table.

- proxy user privilege.

  * MySQL stores proxy privileges in the ``mysql.proxies_priv`` system table.

SQL statements
^^^^^^^^^^^^^^
GRANT
"""""
- grant privileges::

    GRANT
      <priv_type> [(<column_list>)] [, <priv_type> [(<column_list>)]]...
      ON [<object_type>] <priv_level>
      TO <user_or_role> [, <user_or_role>]
      [WITH GRANT OPTION]

    object_type: TABLE | FUNCTION | PROCEDURE

- grant roles::

    GRANT <role> [, <role>] ...
      TO <user_or_role> [, <user_or_role>] ...
      [WITH ADMIN OPTION]

- To grant a privilege, you must have the GRANT OPTION privilege, and you must
  have the privileges that you are granting.

- GRANT is atomic -- it either succeeds for all named users and roles or rolls
  back and has no effect if any error occurs. The statement is written to the
  binary log only if it succeeds for all named users and roles.

- In GRANT statements, the ``ALL [PRIVILEGES]`` or ``PROXY`` privilege must be
  named by itself and cannot be specified along with other privileges.

- Account name:
 
  * account name 可以是 ``username@hostname`` 形式. The host name part of the
    account or role name, if omitted, defaults to '%'. 注意 ``@`` 不能 quote 起
    来. 它是识别两个部分的分隔符.

  * You can specify wildcards in the host name, but NOT in username.

  * If host is omitted, it fallback to ``%``.

  * Anonymous user is specified by ``''``. Does NOT exist by default.

- Quoting:

  * Quote the user name and host name separately.

  * If a username or hostname value in an account name is legal as an unquoted
    identifier, you need not quote it.

  * quotation marks are necessary to specify a username/hostname string
    containing chars that is not part of legal identifier.

  * Quote database, table, column, and routine names as identifiers.

  * Quote user names and host names as identifiers or as strings.

  * 当授予关于 database-level objects 的权限时, metacharacters are permitted,
    所以在授予单个数据库权限时, 数据库名若包含 ``_``, ``%`` 字符, 应该 escape.

  * When a database name not is used to grant privileges at the database level,
    but as a qualifier for granting privileges to some other object such as a
    table or routine, wildcard characters are treated as normal characters.

- You can grant privileges on databases or tables that do not exist. For
  tables, the privileges to be granted must include the CREATE privilege.
  这是为了便于管理员预先分配权限, 而后再创建数据库等 objects.

- The WITH GRANT OPTION clause gives the user the ability to give to other
  users any privileges the user has at the specified privilege level.

- Granting roles:
  
  * You can grant a role to another role.

  * If the GRANT statement includes the WITH ADMIN OPTION clause, each named
    user becomes able to grant the named roles to other users or roles, or
    revoke them from other users or roles. This includes the ability to use
    WITH ADMIN OPTION itself.

Performance implication
^^^^^^^^^^^^^^^^^^^^^^^
- If you are using table, column, or routine privileges for even one user, the
  server examines table, column, and routine privileges for all users and this
  slows down MySQL a bit. Similarly, if you limit the number of queries,
  updates, or connections for any users, the server must monitor these values.

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
三种 binlog format 设置: row, statement, mixed.

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

具体细节说明.

- 关于 ``mysql`` database 的 replication.[SEMysqlRepl]_

  * 对 ``mysql`` database 的直接修改, 会按照 ``binlog_format`` 设置的格式
    进行记录和复制.

  * 如果是因为执行一些 statements, 导致了修改 ``mysql`` database 的 side
    effect, 即间接的修改. 这些修改会按照 statement format 进行记录和复制.
    这些语句包含: GRANT, REVOKE, SET PASSWORD, RENAME USER, CREATE (all forms
    except CREATE TABLE ... SELECT), ALTER (all forms), and DROP (all forms).

    这导致一些麻烦的问题. 由于执行这些语句时, 一般不会先 ``use mysql;``, 所以
    slave 的 database-level 的 replication filter 可能不能起作用 (注意它们是
    statement format 进行记录的).

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

binlog filters.

- ``--binlog-do-db``
  
- ``--binlog-ignore-db``

  注意这些选项是控制哪些数据库需要记录 binlog. 这不同于哪些数据库需要
  replication. 因为 binlog 除了用于 replication, 还用于数据恢复. 对于
  replication 相关的控制和过滤, 应该只在 slave 上进行.

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
    
  * master is write-only, slaves are read-only. 只有 master 上没有向 slave
    replicate 的数据库和/或表, 或者只有 slave 上存在的数据库和表,  slave 上
    才能安全地进行写操作. 否则, slave 必须保持只读.

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

Configuring replication
""""""""""""""""""""""""
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

- manully backup master mysql data, or for the better, use xtrabackup. See
  `Percona XtraBackup`_.

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
  
    * apply master data snapshot to slave.

- Configure the slave with settings for connecting to the master.

  * set unique server id, relay log::

      [mysqld]
      server-id=2
      relay-log=relay-bin
      master-info-repository=TABLE
      relay-log-info-repository=TABLE
      relay-log-purge=1
      relay-log-recovery=1

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

Remove a slave
""""""""""""""

- stop slave threads::

    STOP SLAVE;

- clear replication status and saved configs on slave::

    RESET SLAVE ALL;

- remove replication related configurations.

- restart slave mysqld.

replication filtering
^^^^^^^^^^^^^^^^^^^^^
- Decisions about whether to execute or ignore statements received from the
  master are made according to the ``--replicate-*`` options that the slave was
  started with.

  * Database-level options are checked first. If no database-level options are
    used, option checking proceeds to any table-level options that may be in
    use.

- To make it easier to determine what effect an option set will have, it is
  recommended that you avoid mixing “do” and “ignore” options, or wildcard and
  nonwildcard options.

- procedure.

  * 根据该条 log 的格式确定要检查的数据库.
    
    每条 relay log 可以是不同格式的 (statement or row format). 各个 replication
    filters 对不同格式的 relay log 解析方式不同.

    - 对于 row format log, 要检查的数据库是修改所涉及的数据库.

    - 对于 statement format log, 要检查的数据库是 current default database.

  * 剩下的 See https://dev.mysql.com/doc/refman/8.0/en/replication-rules-db-options.html
    and https://dev.mysql.com/doc/refman/8.0/en/replication-rules-table-options.html

  * 根据上述步骤, 可以看出如果要稳定可靠的 cross-database replication filtering,
    只使用 database-level 的 filtering rule 是不够的, 还需要使用 table-level 的.
    例如, ``--replicate-ignore-table``, ``--replicate-wild-ignore-table``.

replication options
^^^^^^^^^^^^^^^^^^^

essentials
""""""""""
- ``--server-id``, ``server_id``.
  default: 0. If the server ID is set to 0, binary logging takes place (if
  ``log_bin`` is set), but a master with a server ID of 0 refuses any
  connections from slaves, and a slave with a server ID of 0 refuses to connect
  to a master.

master info log and relay log options
"""""""""""""""""""""""""""""""""""""

- ``--master-info-file=<filename>``.
  default: master.info.

- ``--master-info-repository={FILE|TABLE}``, ``master_info_repository``.
  default: TABLE.
  whether the slave logs master status and connection information to a FILE or
  TABLE (``mysql.slave_master_info``).

- ``--relay-log=pathname``, ``relay_log``.
  default: ``<hostname>-relay-bin`` for default channel, or
  ``<hostname>-relay-bin-<channel>`` for the named channel.

  It's recommended to set this option independent of hostname to avoid
  issues casued by changed hostname or to ease cloning slave.

- ``--relay-log-info-file=<filename>``, ``relay_log_info_file``.
  default: relay-log.info.

- ``--relay-log-info-repository={FILE|TABLE}``, ``relay_log_info_repository``.
  default: TABLE.
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

binlog checksum
""""""""""""""""

- ``--slave-sql-verify-checksum={0|1}``, ``slave_sql_verify_checksum``.
  let slave use checksum to verify binlog.

replication filter options
""""""""""""""""""""""""""

- ``--replicate-ignore-db``.

  To specify more than one database to ignore, use this option multiple times.

- ``--replicate-wild-ignore-table``

  Ignore replicating a statement in which any table matches the given wildcard
  pattern. Works for cross-database updates.

  This option applies to tables, views, and triggers. It does not apply to
  stored procedures and functions, or events. To filter statements operating on
  the latter objects, use one or more of the --replicate-*-db options.

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

STOP SLAVE
""""""""""
::

  STOP SLAVE [thread_type [, thread_type] ... ] [FOR CHANNEL channel]

  thread_type: IO_THREAD | SQL_THREAD

- requires the REPLICATION_SLAVE_ADMIN or SUPER privilege.

- STOP SLAVE causes an implicit commit of an ongoing transaction.

- If no tread_type is provided, all types of threads are stopped.

- Providing a FOR CHANNEL clause applies the STOP SLAVE statement to a
  specific replication channel. If a STOP SLAVE statement does not name a
  channel when using multiple channels, this statement stops the specified
  threads for all channels.

RESET SLAVE
"""""""""""
::

  RESET SLAVE [ALL] [FOR CHANNEL channel]

- reset slave's some or all configs and data about replication.

- Use RESET SLAVE to reset slave's replication to its initial state and
  ready to perform a clean start. Maybe for the specified channel.

- Without ALL, It clears the master info and relay log info repositories,
  deletes all the relay log files, and starts a new relay log file. It also
  resets to 0 the replication delay. Connection parameters are not reset.
 
- With ALL, connection parameters and other configs are further reset. So
  basically nothing about replication is preserved. All replication channels
  or the specified channel is deleted.

- Providing a FOR CHANNEL channel clause operation affecting a specific
  replication channel.

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


test database
=============
- The test database often is available as a workspace for users to try things
  out.


Utility Statements
==================

USE
---
::

  USE <database>

- use the specified database as the default (current) database for subsequent
  statements.

- This statement is special in that it does not require a semicolon.

- It must be given on a single line.

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
::

  mysql [options] [db_name]

- ``db_name`` will be the initial default database for queries. If ``db_name``
  is not specified, no default db is selected.

options
"""""""
- ``-p`` 指定密码时不能有空格. 或者使用 ``--password=<pass>``.

- 可以在连接时指定要使用的数据库, 或者用 ``USE`` 切换.

interactive mode
""""""""""""""""
- 语句执行:
  
  * ``;``, ``\g``, ``\G`` 标识一个 statement 的结束.  mysql collects input
    lines but does not send them to server until it sees the terminating token.
    
  * ctrl-c 和 ``\c`` 可以终止当前语句.

  * ``;``, ``\g`` 以 tabular form 输出结果.

  * ``\G`` 将结果列以竖排的形式输出.

- 结果显示:
  
  * 显示形式:
    
    - tabular form: 第一行是表的列名或表达式. 下面的是 query results.

  * 最后显示:
    
    - 结果行数.
      
    - 执行时间, 这个时间是在客户端算出的, 所以并不精确. 它大致等于从发出请求到
      收到结果的全程 wall clock time. 若需要精确的执行实现, 使用 ``SHOW PROFILES``.

- prompts:

  * ``mysql>``. ready for new input.

  * ``">``. waiting for completion of a string that began with a double quote
    ("). 

  * ``'>``. waiting for completion of a string that began with a single quote
    (').

  * ``\`>``. waiting for completion of a backtick-quoted identifier.

  * ``/*>``. waiting for completion of a multiline comment.

  如需输入 mutiline 的 string 和 identifier, 直接加回车即可.

- ``QUIT``, ``\q`` or ctrl-d to quit.

non-interactive mode
""""""""""""""""""""
- In non-interactive mode, read input sql from stdin, print results to stdout.
  For processing convenience, such output is tab-delimited for each column.

mysqldump
^^^^^^^^^
- To make it easier to reload dump files for tables that have foreign key
  relationships, mysqldump automatically includes a statement in the dump
  output to set ``foreign_key_checks`` to 0. This avoids problems with tables
  having to be reloaded in a particular order when the dump is reloaded.

mysqlimport
^^^^^^^^^^^
- essentially a CLI wrapper for LOAD DATA statement.

mysqladmin
^^^^^^^^^^

Utility Programs
----------------

mysqlshow
^^^^^^^^^
::

  mysqlshow [options] [db_name [tbl_name [col_name]]]

a CLI interface to the following SHOW statements:

* ``SHOW DATABASES``

* ``SHOW TABLES FROM db_name``

* ``SHOW TABLE STATUS FROM db_name``

options.

- ``--status``, ``-i``. 直接从 INFORMATION_SCHEMA 中获取最全的信息.

mysqlbinlog
^^^^^^^^^^^

Language drivers
================
- python drivers 列表和选择 -- 需要根据应用场景和需求来选择.

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

      (Though MySQL Connector is a pure Python library, while MySQLdb is
      largely written in C, and we could expect that the new module is a bit
      slower than the current one, performance may actually be improved. This
      is because the new module is eventlet aware, meaning threads will be able
      to switch while waiting for I/O from a database server.
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
- ``_mysql`` 提供 mysql C-API 的面向对象形式. MySQLdb 其他 python modules 是
  thin python wrapper around ``_mysql``, which makes the driver interface
  compatible with DB API.

- mysqlclient 在连接时, socket object 会设置 ``SO_KEEPALIVE`` option.

package structure
^^^^^^^^^^^^^^^^^
- MySQLdb.connections -- implements Connection API.

- MySQLdb.cursors -- implements Cursors of various types for Connection.

- MySQLdb.converters -- handles all the type conversions for MySQL. If the
  default type conversions aren’t what you need, you can make your own. Two
  kinds of conversions are defined here:

  * from mysql types (``MySQLdb.constants.FIELD_TYPE.*``) to python types.

    - key is a field type enumeration value.

    - conversion function signature: input: sql value as string; output:
      corresponding python object.

  * from python types to mysql types.

    - key is a python type object

    - conversion function signature: input: python object of the indicated
      type, conversion dictionary; output: sql literal value.

- ``MySQLdb.constants.CLIENT.*`` mapped from ``CLIENT_*``. Client constants
  used to create the connection. Use bitwise-OR to combine options together,
  and pass them as the ``client_flags`` parameter to ``MySQLdb.Connection``.

- ``MySQLdb.constants.CR.*`` mapped from ``CR_*``. client errors.

- ``MySQLdb.constants.ER.*`` mapped from ``ER_*``. server errors.

- ``MySQLdb.constants.FIELD_TYPE.*`` mapped from ``FIELD_TYPE_*``. 包含 column
  types supported by MySQL, as an enumeration.

- ``MySQLdb.contants.FLAG.*`` mapped from ``FLAG_*``. column property flags in
  a result set. Can be OR-ed to attach multiple properties to a column.

_mysql C extension module
^^^^^^^^^^^^^^^^^^^^^^^^^
- 实现了 ``_mysql.connection`` class, and ``_mysql.result`` class.

- In general,
  
  * any function which takes ``MYSQL *mysql`` as an argument is now a method of
    the connection object, 
 
  * any function which takes ``MYSQL_RES *result`` as an argument is a method
    of the result object.
  
  * Functions requiring none of the MySQL data structures are implemented as
    functions in the module. Functions requiring none of the MySQL data
    structures are implemented as functions in the module.

module-level functions
""""""""""""""""""""""
- ``connect(*args, **kwargs)``

  * ``host``. When specifying ``localhost``, UNIX domain socket will be used,
    otherwise TCP will be used. default is localhost. To connect to the
    localhost with TCP, specifying the machine's hostname, FQDN, or IP address
    of localhost.

  * ``port``. default 3306.

  * ``user``. default is current effective user.

  * ``passwd``. default does not use password.

  * ``db``. default do not USE a default database.

  * ``conv``. a dict for automatic column value conversion. For format of key
    value pairs, see ``MySQLdb.converters.conversions`` and that module's
    documentation. Any column type that can’t be found in conv is returned as a
    string.

  * ``read_default_file``.

connection object
"""""""""""""""""
instance methods
~~~~~~~~~~~~~~~~
- ``query(sql)``. make a query with the passed-in complete sql string.

- ``store_result()``. returns the entire result set to the client immediately.
  Returns a ``result`` object. Use ``store_result()`` unless your result set
  is really huge and you can’t use LIMIT for some reason, and in that case,
  use ``use_result()``.


- ``use_result()``. keeps the result set in the server and sends it row-by-row
  when you fetch. You cannot do any more queries until you have fetched all the
  rows.  Returns a ``result`` object.

result object
"""""""""""""
instance methods
~~~~~~~~~~~~~~~~
- ``fetch_row(maxrows=1, how=0)``. returns a tuple of rows. It may return
  fewer rows than ``maxrows``, but never more. If ``maxrows=0``, all rows of
  the result set are returned. Returns an empty tuple when no more rows to
  fetch.

  When ``how=0``, each row is returned as a tuple. When ``how=1``, each row
  is returned as a dict, where the keys are the column names, or
  ``<table>.<column>`` if there are two columns with the same name. When
  ``how=2``, each row is returned as a dict, and keys are always
  ``<table>.<column>``.

  Each column value is returned as strings, and conversion to actual data type
  should be handled by user or by ``conv`` connect parameter.

exceptions
""""""""""
- MySQLError. top level exception.

- Other exceptions conform to python DB API, and are subclasses of MySQLError.

module-level functions
^^^^^^^^^^^^^^^^^^^^^^
- ``connect(*args, **kwargs)``. create a connection to database. Returns a
  Connection object. parameters:

  * ``_mysql.connect()`` parameters.

  * ``password``. alias of ``passwd``.

  * ``database``. alias of ``db``.

  * ``unix_socket``. default ``/run/mysqld/mysqld.sock``.

  * ``conv``. same as ``_mysql.connect()`` parameter, but default to
    ``MySQLdb.converters.conversions``.

  * ``compress``. enable protocol compression. default no compression.

  * ``connect_timeout``. Abort if connect is not completed within given number
    of seconds. Default: no timeout.

  * ``named_pipe``. Use a named pipe (windows). default: do not use.

  * ``init_command``. initial command to issue to server upon connection.
    default nothing.

  * ``read_default_file``. MySQL configuration file to read. Read options from
    the named option file instead of from my.cnf.

  * ``read_default_group``. default group to read. Read options from the named
    group from ``read_default_file``.

  * ``cursorclass``. cursor class to be used by ``Connection.cursor()``.
    default to ``MySQLdb.cursors.Cursor``.

  * ``use_unicode``. If True, CHAR, VARCHAR, TEXT columns are converted to
    unicode strings. Otherwise they are returned as bytes.

  * ``charset``. Set connection charset (via SET NAMES).

  * ``sql_mode``. set session sql mode.

  * ``ssl``. This parameter takes a dictionary or mapping, where the keys are
    parameter names used by the ``mysql_ssl_set`` MySQL C API call. If this is
    set, it initiates an SSL connection to the server.

  * ``local_infile``. boolean, whether to enable LOAD LOCAL INFILE.

  * ``autocommit``. default False. enable autocommit.

  * ``binary_prefix``. boolean. If set, the '_binary' prefix will be used for
    raw byte query arguments (e.g. Binary). This is disabled by default.

module-level constants
^^^^^^^^^^^^^^^^^^^^^^
- ``apilevel``. 2.0

- ``threadsafety``. 1 -- threads may share the module, but threads may not
  share the connection. 这是因为:

  * Server-side cursor (SSCursor) 在 server 端维持 fetch context, 这是在
    connection 级别的. 一个 connection 同时只能维持一个 server-side cursor.
    跨线程使用更不可能.

  * transaction 状态是 connection 级别的. Two threads simply cannot share a
    connection while a transaction is in progress, in addition to not being
    able to share it during query execution.

- ``paramstyle``. "format". 由于 ``cursor.execute()`` 支持传入 mapping 作为
  formatting argument, 所以实际上也支持 "pyformat".

Connection
^^^^^^^^^^
- ``begin()``. start a transaction. only useful when autocommit mode is on.

- ``commit()``. see db-api.

- ``rollback()``. see db-api.

- ``cursor(cursorclass=None)``. see db-api. If ``cursorclass`` is not given, it
  defaults to the value given when creating the connection object.

- ``autocommit(on)``. turn on/off autocommit mode.

- ``warning_count()``. Return the number of warnings generated from the last
  query.

- ``show_warnings()``. Return detailed information about warnings as a sequence
  of tuples of ``(Level, Code, Message)``.

- ``set_character_set(charset)``. Set the connection character set to charset.

- ``set_sql_mode(sql_mode)``. set session sql mode.

cursors
^^^^^^^
BaseCursor
""""""""""
instance attributes
~~~~~~~~~~~~~~~~~~~
- ``description_flags``. Tuple of column flags for last query, one entry per
  column in the result set.

instance methods
~~~~~~~~~~~~~~~~
- ``execute(query, args=None)``. args is a sequence or mapping. Note that any
  literal percent signs in the ``query`` string passed to must be escaped.
  Parameter placeholders in ``query`` can only be used to insert column values.
  They can not be used for other parts of SQL, such as table names, statements,
  etc.

  Parameter placeholders in ``query`` can be ``%s`` or ``%(name)s``. 注意全部使
  用 ``%s`` 字符串 formatting. 这是因为, ``args`` 传入的参数首先会经过
  ``MySQLdb.converters.conversions`` 进行转换. 转换为 SQL literal 形式 (在
  python 中以字符串形式出现) 后才与 ``query`` template 合并.

- ``executemany(query, args)``. ``args`` is a sequence of sequences or
  mappings. Returns the number of rows affected. This method improves
  performance on multiple-row INSERT and REPLACE. Otherwise it is equivalent to
  looping over args with ``execute()``.


- ``fetchone()``. see db-api.

- ``fetchmany(size)``. see db-api.

- ``fetchall()``. see db-api.

- ``callproc(procname, args)``. see db-api.

- ``close()``. Closes the cursor. When using server-side cursors, it is very
  important to close the cursor when you are done with it and before creating a
  new one.

- ``__enter__()``

- ``__exit__(*exc_info)``. close cursor on exiting from context.

- ``nextset()``. Advances the cursor to the next result set, discarding the
  remaining rows in the current result set. If there are no additional result
  sets, it returns None; otherwise it returns a true value.

- ``setinputsizes(*args)``. does nothing.

- ``setoutputsizes(*args)``. does nothing.

CursorStoreResultMixIn
""""""""""""""""""""""
- Causes the Cursor to use the ``connection.store_result()`` to get the query
  result. The entire result set is stored on the client side.

CursorUseResultMixIn
""""""""""""""""""""
- Causes the cursor to use the ``connection.use_result()`` function to get the
  query result. The result set is stored on the server side and is transferred
  row by row using fetch operations.

CursorTupleRowsMixIn
""""""""""""""""""""
- return rows as tuples.

CursorDictRowsMixIn
""""""""""""""""""""
- return rows as dicts.

Cursor
""""""
- the default cursor class. subclass of CursorStoreResultMixIn,
  CursorTupleRowsMixIn, BaseCursor.

DictCursor
""""""""""
- like Cursor, but return rows as dicts.

SSCursor
""""""""
- Server-side Cursor. subclass of CursorUseResultMixIn.

SSDictCursor
""""""""""""
- like SSCursor, but return rows as dicts.

Client Programming Design Patterns
==================================
- 是否应该利用数据库提供的 binary field type 去保存文件?

  不该. 原因:

  1. 在数据库中保存文件将导致数据库体积迅速增长, 这些二进制数据将占用数据库体积
     的绝大部分. 这导致的问题是: 不必要的内存占用量大大增加; 而且体积大的数据库
     更难以维护, 例如备份更慢, 甚至实际难以备份.

  2. 加重数据库的读写负担. 文件比数据需要更长时间的读写, 所以应用和数据库的连接
     需要维持更长时间, 整体上加重了并发连接数和负载. 而这些文件很多时候可以由
     前端服务器如 nginx 去提供. 此外, 由前端服务器去 serve 静态文件也更高效, 因为
     可以并发.

  3. 以 mysql 为例, 一些数据库在涉及到 binary field 类型的语句时, 反而会去硬盘
     上创建临时表, 这样反而降低了执行速度.

  4. 使用文件系统保存文件, 也很容易迁移存储架构, 例如从硬盘存储迁移至分布式存储.

- 对于具有少数几个确定字符串值的 enum 类型量, 应该在数据库里存储字符串本身还是
  integer flags?

  存储字符串, 或者使用 RDBMS 本身支持的 enum 类型 (例如 mysql), 这样存储时是数字、
  读写时是字符串. 理由:

  首先, 在现今的计算能力下, 从字符串至 int flag 的转换是 micro optimization.
  存储字符串 (或 enum) 带来的好处大于它造成的问题. 好处: 数据可读性更高, 不需要
  业务逻辑代码进行翻译, 且部分前端/GUI 可直接使用这些数据, 程序员不需要记忆无聊
  且易错的 enum table. 坏处: 需要更大的存储空间.

  由于硬盘相对于程序员的编程时间和排错时间便宜很多, so anything that trades
  development effort for disk space is also a good thing, from a business
  perspective.

  其次, 对于支持 enum 类型的数据库, 则可以使用这个类型在两方面之间达成一个折中.

  aside: the scripting language Lua, renowned for being direct and
  high-performance, used to write entire game engines, etc. They never bothered
  having a number type at all. Their string handling code is so effective, they
  can add numbers together that are actually strings, in time-sensitive game
  engine code. Like JavaScript, they don't even have objects - just very fancy
  hash tables. The C programmer's view of "a huge array of chars? How
  inefficient!" is outdated.

- 在 RDBMS 里保存 JSON 合适么?
  
  这取决于两方面:
  
  * 准备以 json 形式保存的数据到底是做什么用的.
  
    如果这个 json 数据虽然结构可能复杂, 但是从概念上实际上是一个完整的数据单元,
    也就是说, 你自己的业务逻辑并不需要 (频繁) 对这些数据内部的字段进行单独访问和
    操作, 而只是整块取出、整块写入时, 就可以使用 JSON 保存. 常见的场景有: 保存
    历史信息, 保存日志信息, 保存不需后端 manipulate 的复杂信息.

    如果你需要对 JSON 中的字段单独访问, 进行数据库操作, 例如 join, filter, index 等,
    则一般来讲不适合作为整块 JSON 保存. 但若数据库本身支持 JSON 类型的复杂操作,
    则需具体考虑.

  * 数据是否具有变化比较大的格式差别. 如果是这样, 可以考虑用 JSON 保存. 但
    如果需要对 JSON 中的字段进行单独访问、更新等操作, 见上述.

  A rule of thumb: 一般情况下尽量把数据 normalized 化. 尽量避免存储 json, 而是
  扩展成 fields 或者 foreign key 连接的 extension table 等形式. 这样可能长期看,
  对于 MVC 和减少重复是有好处的 (因为格式在 model 中都建立好了, 不需要手动解析
  数据构建 json 等).

- Increment a column value (counting) in a thread-safe way. 两种方式:

  * Atomic update operation::

      UPDATE table SET counter=counter+1 WHERE ...

  * 若程序逻辑要求无法使用 atomic operation, 必须先取出 column value, 使用
    transaction + SELECT ... FOR UPDATE, 设置 row lock::

      START TRANSACTION;
      SELECT `counter` FROM `table` WHERE ... FOR UPDATE;
      UPDATE `table` SET `counter` = `counter`+1 WHERE ...;
      COMMIT;

- database normalization and denormalization, 该如何权衡.

  数据库设计首先应该尽量去 normalized, 因为这些 normalization forms 具有很多价
  值; 只有当 normalized design 确实成为了性能瓶颈之后才应适当地增加数据的冗余度
  以改善性能.  Denormalization 应当是以 normalized 数据库设计为基础进行的优化.
  而不是空中楼阁. 首先做好 normalized design, 才谈得上 denormalization 优化.
  只有在 profiling 之后发现 denormalization 可以解决性能瓶颈, 才选择进行
  denormalization. Denormalized form is NOT unnormalized form. 

  See also [SENormalization]_, [WikiDenormalization]_.

- 一个表必须有一个或者一组 unique key 可以唯一识别不同的资源实例, 否则无法完全
  避免多个 session 同时创建同一个实例时导致的重复 (race condition).

Installation
=============
- Purge MySQL from the system [SERemoveMySQL]_::

    sudo -i
    service mysql stop
    killall -KILL mysql mysqld_safe mysqld
    apt-get --yes purge mysql-server mysql-client
    apt-get --yes autoremove --purge
    apt-get autoclean
    deluser --remove-home mysql
    delgroup mysql
    rm -rf /etc/apparmor.d/abstractions/mysql /etc/apparmor.d/cache/usr.sbin.mysqld /etc/mysql /var/lib/mysql /var/log/mysql* /var/log/upstart/mysql.log* /var/run/mysqld
    updatedb
    mkdir -p /etc/apparmor.d/abstractions/mysql
    mkdir -p /etc/mysql/conf.d/
    exit

References
==========
.. [DOMysqlSlave] `How To Set Up Master Slave Replication in MySQL <https://www.digitalocean.com/community/tutorials/how-to-set-up-master-slave-replication-in-mysql>`_
.. [PerconaAcce] `Accelerating the backup process <https://www.percona.com/doc/percona-xtrabackup/LATEST/innobackupex/parallel_copy_ibk.html>`_
.. [PerconaXbstream] `The xbstream binary <https://www.percona.com/doc/percona-xtrabackup/LATEST/xbstream/xbstream.html>`_
.. [SOCharVarchar] `What are the use cases for selecting CHAR over VARCHAR in SQL? <https://stackoverflow.com/questions/59667/what-are-the-use-cases-for-selecting-char-over-varchar-in-sql>`_
.. [SEMysqlRepl] `How can you stop MySQL slave from replicating changes to the 'mysql' database? <https://dba.stackexchange.com/questions/584/how-can-you-stop-mysql-slave-from-replicating-changes-to-the-mysql-database>`_
.. [SOUTF8Difference] `What's the difference between utf8_general_ci and utf8_unicode_ci <https://stackoverflow.com/questions/766809/whats-the-difference-between-utf8-general-ci-and-utf8-unicode-ci>`_
.. [SOIndexWorking] `How does database indexing work? [closed] <https://stackoverflow.com/questions/1108/how-does-database-indexing-work>`_
.. [DocDefaultValue] https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html
.. [DocGenColumn] https://dev.mysql.com/doc/refman/8.0/en/create-table-generated-columns.html
.. [SENormalization] `How far should you go with normalization? <https://dba.stackexchange.com/questions/505/how-far-should-you-go-with-normalization>`_
.. [WikiDenormalization] `Denormalization <https://en.wikipedia.org/wiki/Denormalization>`_
.. [SERemoveMySQL] `How do I uninstall MySQL completely? <https://askubuntu.com/q/640899/348299>`_
.. [SOJoinWhere] `MySQL Join clause vs WHERE clause <https://stackoverflow.com/q/4160637/1602266>`_
.. [SOCommaJoinDiff] `What's the difference between comma separated joins and join on syntax in MySQL? <https://stackoverflow.com/q/20138355/1602266>`_
