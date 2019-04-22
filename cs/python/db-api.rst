overview
========
- Python Database API specification (DB API) is the general relational database
  API specification for python db connector modules.

- DB API 规范的作用类似于 Java 中的 JDBC.

module-level functions
======================
- ``connect(...)``. ``Connection`` object factory. It returns a connection to
  the database. Its parameters are db-dependent.

module-level constants
======================
- ``apilevel``. string constant stating the supported DB API level. possible
  values: "1.0", "2.0". If not given, "1.0" should be assumed.

- ``threadsafety``. Integer constant stating the level of thread safety the
  interface supports. Possible values:

  * 0. threads may not share the module.

  * 1. threads may share the module, but not the connections.

  * 2. threads may share the module and the connections but not the cursors.

  * 3. threads may share the module, connections and cursors.

  Sharing in the above context means that two threads may use a resource
  without wrapping it *using a mutex semaphore to implement resource locking*.

  很多情况下, 通过 resource locking (mutex) 即可让多个线程共同使用一个本身不具
  有 thread safety 的对象. 但是并不是总可以这样 -- the resource may rely on
  global variables or other external sources that are beyond your control.

- ``paramstyle``. string constant stating the type of parameter marker
  formatting expected by the interface. Possible values:

  * qmark. question mark style: ``name=?``

  * numeric. numeric, positional style: ``name=:1``

  * named. named style: ``name=:name``

  * format: C printf(3) format code: ``name=%s``

  * pyformat: python extended format code: ``name=%(name)s``

exception hierarchy
===================
::

  Exception
  |__Warning
  |__Error
     |__InterfaceError
     |__DatabaseError
        |__DataError
        |__OperationalError
        |__IntegrityError
        |__InternalError
        |__ProgrammingError
        |__NotSupportedError

- Warning. Exception raised for important warnings like data truncations while
  inserting, etc. 

- Error. Exception that is the base class of all other error exceptions.
  Warnings are not considered errors and thus should not use this class as
  base.

- InterfaceError. Exception raised for errors that are related to the database
  interface rather than the database itself.

- DatabaseError. Exception raised for errors that are related to the database.

- DataError. Exception raised for errors that are due to problems with the
  processed data like division by zero, numeric value out of range, etc.

- OperationalError. Exception raised for errors that are related to the
  database's operation and not necessarily under the control of the programmer.

- IntegrityError. Exception raised when the relational integrity of the
  database is affected, e.g. a foreign key check fails.

- InternalError. Exception raised when the database encounters an internal
  error, e.g. the cursor is not valid anymore, the transaction is out of sync,
  etc.

- ProgrammingError. Exception raised for programming errors, e.g. table not
  found or already exists, syntax error in the SQL statement, wrong number of
  parameters specified, etc.

- NotSupportedError. Exception raised in case a method or database API was used
  which is not supported by the database, e.g. requesting a .rollback() on a
  connection that does not support transaction or has transactions turned off. 

Connection
==========
class attributes
----------------
- Warning, Error, etc. All exception classes defined by the DB API standard
  should be exposed on the Connection objects as attributes.

instance attributes
-------------------
- ``messages``. same as ``Cursor.messages``. the messages in the list are
  connection oriented.  The list is cleared automatically by all standard
  connection methods calls (prior to executing the call) to avoid excessive
  memory usage.

- ``errorhandler``. Read/write attribute which references an error handler to
  call in case an error condition is met. Signature::

    errorhandler(connection, cursor, errorclass, errorvalue)

instance methods
----------------
- ``close()``. close the connection. After this, the Connection object is
  unusable. an Error (or subclass) exception will be raised if any operation is
  further attempted with the connection. Note that closing a connection without
  committing the changes first will cause an implicit rollback to be performed.

- ``commit()``. Commit pending transaction to the database. If the database
  supports an auto-commit feature, it must be initially off. An interface
  method may be provided to turn it back on.

  Database modules that do not support transactions should implement this
  method with void functionality.

  注意 commit/rollback 等 transaction control methods 应该在 Connection 上面,
  而不是 cursor 上面. Cursor 的价值在于方便地 fetch result set. Cursor 并不进行
  状态控制.

- ``rollback()``. optional since not all databases provide transaction support.
  In case a database does provide transactions this method causes the database
  to roll back to the start of any pending transaction. Closing a connection
  without committing the changes first will cause an implicit rollback to be
  performed.

- ``cursor()``. Returns a Cursor object using this Connection.

Cursor
======
- Cursor represents a database cursor, which is used to manage the context of
  a fetch operation.

- 一个线程内, 同时能维持的 cursor instances 的数目, 是由 threadsafety 等级决定
  的.  也就是能维持的 fetch context 数目由 threadsafety 等级决定.

- Cursors created from the same connection are not isolated, i.e., any changes
  done to the database by a cursor are immediately visible by the other
  cursors. 

instance attributes
-------------------
- ``description``. Readonly. A sequence of 7-item sequences. Each of these
  sequences contains information describing one result column. None if
  operations that do not return rows or if the cursor has not had an operation
  invoked.  Each sequence contains the following elements:

  * ``name``. column name.

  * ``type_code``. 列的类型 code, 由具体的 db-api implementation 给出列类型与
    type code 的映射关系.

  * ``display_size``.

  * ``internal_size``

  * ``precision``

  * ``scale``

  * ``null_ok``. 该列是否 NULL-able.

- ``rowcount``. Readonly. the number of rows that the last ``execute*()``
  produced. It's -1 in case no ``.execute*()`` has been performed on the
  cursor.

- ``rownumber``. the current 0-based index of the cursor in the result set or
  None if the index cannot be determined.

- ``arraysize``. read/write. specifies the number of rows to fetch at a time
  with ``.fetchmany()``. It defaults to 1.

- ``lastrowid``. This read-only attribute provides the rowid of the last
  modified row. If the operation does not set a rowid or if the database does
  not support rowids, this attribute should be set to None. The semantics of
  .lastrowid are undefined in case the last executed statement modified more
  than one row.

- ``connection``. a reference to the Connection object on which the cursor was
  created.

- ``messages``. a list to which the interface appends tuples (exception class,
  exception value) for all messages which the interfaces receives from the
  underlying database for this cursor.

  The list is cleared by all standard cursor methods calls (prior to executing
  the call) except for the ``.fetch*()`` calls automatically to avoid excessive
  memory usage.

  All error and warning messages generated by the database are placed into this
  list, so checking the list allows the user to verify correct operation of the
  method calls.

- ``errorhandler``. same as Connection.errorhandler.

instance methods
----------------
- ``callproc(procname[, parameters])``. optional. Call a stored database
  procedure with the given name. The sequence of parameters must contain one
  entry for each argument that the procedure expects.

  The result of the call is returned as modified copy of the input sequence.
  Input parameters are left untouched, output and input/output parameters
  replaced with possibly new values.

  The procedure may also provide a result set as output. This must then be made
  available through the standard ``.fetch*()`` methods.

- ``close()``. Close the cursor. The cursor will be unusable from this point
  forward; an Error (or subclass) exception will be raised if any operation is
  attempted with the cursor.

- ``execute(operation[, parameters])``. prepare and execute an database
  operation. Parameters may be provided as sequence or mapping and will be
  bound to variables in the operation. 

- ``executemany(operation, seq_of_parameters)``. Prepare a database operation
  (query or command) and then execute it against all parameter sequences or
  mappings found in the sequence ``seq_of_parameters``.

  Use of this method for an operation which produces one or more result sets
  constitutes undefined behavior, and the implementation is permitted (but not
  required) to raise an exception when it detects that a result set has been
  created by an invocation of the operation.

  ``execute()`` 适合任何形式的单项操作; ``executemany()`` 适合不返回 result set
  的多项操作的重复, 例如 INSERT 多次. 两者都利用了 prepared statements.

- ``fetchone()``. fetch the next row, return a single sequence of columns, or
  None if result set is exhausted. An Error (or subclass) exception is raised
  if the previous call to ``.execute*()`` did not produce any result set or no
  call was issued yet.

- ``fetchmany([size=cursor.arraysize])``. Fetch the next set of rows of a query
  result, returning a sequence of sequences (e.g. a list of tuples). An empty
  sequence is returned when no more rows are available.

  The number of rows to fetch per call is specified by the parameter. If it is
  not given, the cursor's arraysize determines the number of rows to be
  fetched.

  An Error (or subclass) exception is raised if the previous call to
  ``.execute*()`` did not produce any result set or no call was issued yet.

- ``fetchall()``. Fetch all (remaining) rows of a query result, returning them
  as a sequence of sequences (e.g. a list of tuples).

  An Error (or subclass) exception is raised if the previous call to
  ``.execute*()`` did not produce any result set or no call was issued yet.

- ``nextset()``. optional. This method will make the cursor skip to the next
  available set, discarding any remaining rows from the current set.  If there
  are no more sets, the method returns None. Otherwise, it returns a true value
  and subsequent calls to the ``.fetch*()`` methods will return rows from the
  next result set.

- ``setinputsizes(sizes)``. can be used before a call to ``.execute*()`` to
  predefine memory areas for the operation's parameters. sizes is specified as
  a sequence — one item for each input parameter. The item should be a Type
  Object that corresponds to the input that will be used, or it should be an
  integer specifying the maximum length of a string parameter. If the item is
  None, then no predefined memory area will be reserved for that column.

- ``setoutputsize(size[, column])``. Set a column buffer size for fetches of
  large columns (e.g. LONGs, BLOBs, etc.). The column is specified as an index
  into the result sequence. Not specifying the column will set the default size
  for all large columns in the cursor.

- ``scroll(value[, mode="relative"])``. Scroll the cursor in the result set to
  a new position according to mode.

  If mode is relative (default), value is taken as offset to the current
  position in the result set, if set to absolute, value states an absolute
  target position.

  An IndexError should be raised in case a scroll operation would leave the
  result set. In this case, the cursor position is left undefined (ideal would
  be to not move the cursor at all).

- ``__iter__()``. iterator protocol requirement. return self, so that Cursor
  is an iterator.

- ``__next__()``. iterator next method. Return the next row from the currently
  executing SQL statement using the same semantics as ``fetchone()``.

Two-Phase Commit (TPC) extensions
=================================
