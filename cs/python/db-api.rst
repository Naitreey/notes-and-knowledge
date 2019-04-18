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
instance methods
----------------
- ``close()``. close the connection. After this, the Connection object is
  unusable. an Error (or subclass) exception will be raised if any operation is
  further attempted with the connection. Note that closing a connection without
  committing the changes first will cause an implicit rollback to be performed.

- 
