Row-oriented and Column-oriented DBMS
=====================================
Row-oriented
------------
- Row-based systems are designed to efficiently return data for an entire row,
  or record, in as few operations as possible.
 
  This matches the common use-case where the system is attempting to retrieve
  information about a particular object.

- Row-based systems are not efficient at performing set-wide operations on the
  whole table, as opposed to a small number of specific records.
  
  To improve the performance of these sorts of operations (which are very
  common, and generally the point of using a DBMS), most DBMSs support the use
  of secondary indexes.

  As they store only single pieces of data, rather than entire rows, indexes
  are generally much smaller than the main table stores. Scanning this smaller
  set of data reduces the number of disk operations. If the index is heavily
  used, it can dramatically reduce the time for common operations. However,
  maintaining indexes adds overhead to the system, especially when new data is
  written to the database. Records not only need to be stored in the main
  table, but any attached indexes have to be updated as well.

- Row-oriented databases are well-suited for OLTP-like workloads which are more
  heavily loaded with interactive transactions. For example, retrieving all
  data from a single row is more efficient when that data is located in a
  single location (minimizing disk seeks), as in row-oriented architectures.

Column-oriented
---------------
- A DBMS that stores data tables by column rather than by row.

- By storing data in columns rather than rows, the database can more precisely
  access the data it needs to answer a query rather than scanning and
  discarding unwanted data in rows.

- In a row-oriented indexed system, the primary key is the rowid that is mapped
  from indexed data. In the column-oriented system, the primary key is the
  data, which is mapped from rowids.

- Whether or not a column-oriented system will be more efficient in operation
  depends heavily on the workload being automated.
  
  Operations that retrieve all the data for a given object (the entire row) are
  slower. A row-based system can retrieve the row in a single disk read,
  whereas numerous disk operations to collect data from multiple columns are
  required from a columnar database.

  However, in the majority of cases, only a limited subset of data is needed to
  be retrieved.

- When writing data into the database, column-oriented database is especially
  more efficient if the data to be written tend to be sparse with many optional
  columns. For this reason, column stores have demonstrated excellent
  real-world performance in spite of many theoretical disadvantages.

- columnar databases are well-suited for OLAP-like workloads (e.g., data
  warehouses) which typically involve highly complex queries over all data
  (possibly petabytes). Transactions (INSERTs) must be separated into columns
  and compressed as they are stored, making it less suited for OLTP workloads.

- Compression. Column data is of uniform type; therefore, there are some
  opportunities for storage size optimizations available in column-oriented
  data that are not available in row-oriented data. 

  To improve compression, sorting rows can also help. For example, using bitmap
  indexes, sorting can improve compression by an order of magnitude.

  Columnar compression achieves a reduction in disk space at the expense of
  efficiency of retrieval. The greater adjacent compression achieved, the more
  difficult random-access may become, as data might need to be uncompressed to
  be read. Therefore, column-oriented architectures are sometimes enriched by
  additional mechanisms aimed at minimizing the need for access to compressed
  data.
