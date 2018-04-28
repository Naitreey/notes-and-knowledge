- error logging

  mysqld 根据 ``--log-error`` option 来决定错误日志输出. 若这个选项没有设置,
  日志写到 stderr. 此时 ``log_error`` system variable 为 ``stderr``.

- 处于安全考虑, ``local_infile`` 默认是 OFF, 需要在 mysql client 和 mysqld
  同时开启.

SQL language
============

Language Structure
------------------

literal values
^^^^^^^^^^^^^^

String literals
""""""""""""""""
::

  [_<charset>] <string> [COLLATE <collation>]

- string literal is enclosed in single or double quotes.

  * A ' inside a string quoted with ' may be written as ''.

  * A " inside a string quoted with " may be written as "".

  * Or ' " can be escaped by backslash.

- Quoted strings placed next to each other are concatenated to a single string.

- A string literal can specify its charset and collation.

- backslash escapes.
  
  * For unrecognized escape sequences, backslash is ignored.

Numeric literals
""""""""""""""""
- exact-value literals. having integer part and/or fractional part,
  may be signed.
  
- approximate-value literals. in scientific notation with a mantissa
  and exponent.

hex literals
""""""""""""
::

  [_<charset>] X'<hex>' [COLLATE <collation>]
  [_<charset>] 0x<hex> [COLLATE <collation>]
    
- ``0x`` can not be written as ``0X``. letter cases does not matter.

- hex literal can be a binary string or number. To ensure numeric treatment of
  a hexadecimal literal, use it in numeric context.

bit-value literals
""""""""""""""""""
::

  [_<charset>] B'<bin>' [COLLATE <collation>]
  [_<charset>] 0b<bin> [COLLATE <collation>]
  
- By default, a bit-value literal is a binary string. In numeric contexts,
  MySQL treats a bit literal like an integer.

boolean literals
""""""""""""""""
::

  TRUE
  FALSE

- in any letter case.

null values
""""""""""""
::

  NULL

- in any letter case.

- In collation order, NULL precedes any other values.

Date and Time literals
""""""""""""""""""""""
::

  [DATE|TIME|TIMESTAMP] 'timestr'
  { d|t|ts 'timestr' }

- format.

  * DATE. 'YYYY-MM-DD', 'YY-MM-DD', YYYYMMDD or YYMMDD. Any punctuation
    character may be used as the delimiter.

  * TIMESTAMP. 'YYYY-MM-DD HH:MM:SS', 'YY-MM-DD HH:MM:SS', 'YYYYMMDDHHMMSS' or
    'YYMMDDHHMMSS'. Any punctuation character may be used. The date and time
    parts can be separated by T rather than a space. Value can include a
    trailing fractional seconds part in up to microseconds (6 digits)
    precision.

  * TIME. 'D HH:MM:SS', 'HH:MM:SS', 'HH:MM', 'D HH:MM', 'D HH', or 'SS',
    'HHMMSS'. A trailing fractional seconds part is recognized.

- TIMESTAMP produces DATETIME value.

identifiers
^^^^^^^^^^^
- An identifier may be quoted with backtick or unquoted. If an identifier
  contains special characters or is a reserved word, you must quote it whenever
  you refer to it.

- To escape a backtick in quoted identifier: use double tick.

- Identifiers are converted to Unicode internally. identifier length
  以字符数目计算.

- Valid identifier characters:

  * U+0001 - U+FFFF (unicode point: 1-65535)

  * NULL is not permitted in identifier.

  * Database, table, and column names cannot end with space characters.

- qualified identifiers: consisting of identifiers separated by ``.``
  qualifier, indicating a namespace hierarchy.

Data types
==========

String types
------------

.. -------------------------------

- In general, treat all identifiers (database names, table names, column names,
  etc.) and strings as case sensitive; treat SQL keywords, mysql builtin commands,
  etc. as case insensitive.

- comment syntax: 三种注释语法

  * ``--``, 后面必须加上一个空格, line comment

  * ``#``, line comment

  * ``/* */``, block comment. 还有特殊作用, ``/*! */`` 用于在 sql 中加入 non-portable
    的 mysql extension 语句, 这样注释之外的部分仍然是 portable 的语句.

- backtick (``\```) wrap 的是 identifier, 当 identifier 中不包含特殊字符时, 可以省去.

- SQL pattern

  * ``_``: any single character, equivalent to ``?`` in shell.

  * ``%``: any number of any character, equivalent to ``*`` in shell.


.. -------------------------------


- ``SELECT`` statement

  * mysql 不支持 ``SELECT DISTINCT ON (...)``, 聚合时若要根据某列的 distinct 来
    选择行, 可以通过 ``COUNT(DISTINCT <colname>)`` 来迂回处理. 这很 hack.

- 注意 ``SELECT`` 后面的部分是 case insensitive 的.

- column header 是 ``SELECT`` 的项, 它可以是表的列名字, 也可能是表达式.

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

transaction
-----------
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


Programming Designs
===================

- 在 RDBMS 里保存 JSON 合适么?
  
  这取决于你想以 json 形式保存的数据到底是做什么用的.
  
  如果这个 json 数据虽然结构可能复杂, 但是从概念上实际上是一个完整的数据单元,
  也就是说, 你自己的业务逻辑并不需要 (频繁) 对这些数据内部的字段进行单独访问和
  操作, 而只是整块取出、整块写入时, 就可以使用 JSON 保存. 常见的场景有: 保存
  历史信息, 保存日志信息, 保存不需后端 manipulate 的复杂信息.

  如果你需要对 JSON 中的字段单独访问, 进行数据库操作, 例如 join, filter, index 等,
  则不适合作为整块 JSON 保存.

  A rule of thumb: 一般情况下尽量把数据 normalized 化. 尽量避免存储 json, 而是
  扩展成 fields 或者 foreign key 连接的 extension table 等形式. 这样可能长期看,
  对于 MVC 和减少重复是有好处的 (因为格式在 model 中都建立好了, 不需要手动解析
  数据构建 json 等).

- 对于具有少数几个确定字符串值的 enum 类型量, 应该在数据库里存储字符串本身还是
  integer flags?

  存储字符串, 或者使用 RDBMS 本身支持的 enum 类型, 这样存储时是数字、读写时是
  字符串. 理由:

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

- 是否应该利用数据库提供的 binary field type 去保存文件?

  不该. 原因:

  1. 在数据库中保存文件将导致数据库体积迅速增长, 这些二进制数据将占用数据库体积
     的绝大部分. 这导致的问题是: 不必要的内存占用量大大增加; 而且体积大的数据库
     更难以维护, 例如备份更慢, 甚至实际难以备份.

  2. 加重数据库的读写负担. 文件比数据需要更长时间的读写, 所以应用和数据库的连接
     需要维持更长时间, 整体上加重了并发连接数和负载. 而这些文件很多时候可以由
     前端服务器如 nginx 去提供. 此外, 由前端服务器去 serve 静态文件也更高效, 因为
     可以并发.

  3. 使用文件系统保存文件, 也很容器迁移存储架构, 例如从硬盘存储迁移至分布式存储.
     

mysql vs postgresql
===================

- encoding.

  mysql 5.7 仍然不是默认 utf-8 编码. 而且要在 mysql 中使用真正的 utf-8
  编码需要使用奇葩的 utf8mb4.
 
  postgresql 默认是 utf-8.

- select ... for update.

  mysql 不支持 ``NOWAIT``, ``SKIP LOCKED``, which is VERY IMPORTANT features!

  postgresql 支持得很好.

- default isolation level.

  mysql 使用 repeatable read. postgresql 使用 read committed.

  后者才是一般预期的行为, 是除了 mysql 之外所有其他数据库的默认行为.
  这两个 isolation level 的差异, 会导致应用程序的一些 subtle bugs.

References
==========
.. [DOMysqlSlave] `How To Set Up Master Slave Replication in MySQL <https://www.digitalocean.com/community/tutorials/how-to-set-up-master-slave-replication-in-mysql>`_
.. [PerconaAcce] `Accelerating the backup process <https://www.percona.com/doc/percona-xtrabackup/LATEST/innobackupex/parallel_copy_ibk.html>`_
.. [PerconaXbstream] `The xbstream binary <https://www.percona.com/doc/percona-xtrabackup/LATEST/xbstream/xbstream.html>`_
