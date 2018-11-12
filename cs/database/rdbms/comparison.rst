mysql vs postgresql
===================
- default isolation level.

  mysql 使用 repeatable read. postgresql 使用 read committed.

  后者才是一般预期的行为, 是除了 mysql 之外所有其他数据库的默认行为.
  这两个 isolation level 的差异, 会导致应用程序的一些 subtle bugs.

- mysql does not support DDLs in transaction. DDL statements are
  non-transactional and break transactions (cause implicit commit etc.).
