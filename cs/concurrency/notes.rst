concurrency
===========
- Concurrency means the program is able to initiate another operation without
  waiting the previous operation to finish. In other words, there are more than
  one work is in "running" state.

  并发 (concurrency) 与并行 (parallelism) 是不同的概念. 并行是一种实现并发的机制,
  但并发也可通过其他机制实现. 例如 event loop.

- 单线程 event loop 并发类似于吧台 a bartender serves multiple customer.

synchronization
===============

- 当资源竞争的单位是线程时, 同步适合使用 mutex 等机制.

- 当资源竞争的单位是进程时, 同步适合使用 file lock 例如 ``flock(2)``.

- 当资源竞争的单位是可能涉及多个进程的一个流程时, 同步适合使用数据库字段或文件是否
  存在来加锁.
