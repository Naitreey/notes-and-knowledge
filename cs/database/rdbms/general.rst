Cursor
======
- Database cursor is a control structure that enables traversal over the
  records in a result set.

- 名为 cursor, 是因为它可以看作是 a pointer to one row in a set of rows. A
  cursor only reference one row at a time, but can move to other rows of the
  result set as needed.

- 一个 session 内, 同时可以维持多个 cursor. 即维持多个 result set fetch
  context.

- Cursor 的价值.
  
  * Cursor 的作用类似于 programming language 中的 iterator 概念. In stead of
    fetching the entire big result set at once, cursor enables a row-by-row
    streaming access pattern.

  * 因此, cursor can save time -- 因为无需等待完整的 result set 传输完成, 要
    多少取多少.

  * cursor can save memory -- 因为无需留出一大块内存用于保存 result set. 处理程
    序只需 stream through the result set.

- Cursor 的一些注意事项.

  * Consistency concerns. Cursor fetch through a result set. 然而, 根据 RDBMS
    所处的 isolation level, result set 很可能不是一个 snapshot of a set of
    rows. Consistency therefore is only guaranteed for the current row being
    fetched. 同一个 session 或不同 session 中, 对相关 rows 的修改操作, 会对
    这个 cursor 的 result set 可见.

  * Transmitting every row by itself can be very inefficient, since every
    packet has negotiation overhead that you might avoid by sending big, maybe
    compressed, chunks of data per packet. ( No DB server or client library is
    stupid enough to transmit every row individually, there's caching and
    chunking on both ends, still, it is relevant.)

  * 包含聚合操作的 sql 不适合使用 cursor, 因为 GROUP BY and aggregate 不是
    sequential operation. server 必须一次性在内存中根据完整的 result set 计算出
    所需聚合结果.

- 何时使用 cursor 何时不使用 cursor?

  * If you work on small, quickly created resultsets, don't use cursors.

  * Cursors excell on ad hoc, complex (referentially), queries of sequential
    nature with big resultsets and low consistency requirements. (Like an
    iterator.)

See also [SOCursorBenefits]_, [WikiCursor]_.

References
==========
.. [SOCursorBenefits] `What are the benefits of using database cursor? <https://stackoverflow.com/questions/3861558/what-are-the-benefits-of-using-database-cursor>`_
.. [WikiCursor] `Cursor (databases) <https://en.wikipedia.org/wiki/Cursor_(databases)>`_
