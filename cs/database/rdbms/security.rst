SQL injection
=============
- SQL injection is a type of attack that tries to perform actions on a database
  used by the target web site.

- 各种 sql injection 其实都是类似的, 本质上都可以通过 ORM + prepared statement +
  escaping 去解决.

  ORM: 杜绝手写 SQL statement, 自动地强制了使用参数化的 SQL statement;
  prepared statement: 固定 sql 代码, 传入的都认为是参数, 避免了 sql 代码插入问题;
  escaping: 避免 sql 代码插入.
