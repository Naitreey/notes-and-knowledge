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

- what is synchronous and what is asynchronous?

  当我们讨论同步和异步时, 必须涉及至少两个操作 A 和 B, 且 A 操作触发 B 操作.
  我们说这两个操作的关系是同步的或者异步的. 如果 A 触发 B 后, 等待 B 操作
  结束返回, 然后才继续自己的逻辑, 则 A, B 是同步的. 如果 A 触发 B 后, 自己
  继续自己的逻辑干别的去了, 不等 B 操作, 则 A, B 是异步的.

  AB 同步时, A 等待 B 的方式可能是 blocking, 或者 periodic polling. 此时, 对
  B 结果的处理逻辑在 A 中按照自然顺序执行即可.

  AB 异步时, 对 B 结果的处理逻辑以 callback 形式注册到 B 结果返回事件中. 即
  事件驱动的结果处理.

- How to ensure synchronization.

  - 当资源竞争的单位是线程时, 同步适合使用 mutex 等机制.
  
  - 当资源竞争的单位是进程时, 同步适合使用 file lock 例如 ``flock(2)``.
  
  - 当资源竞争的单位是可能涉及多个进程的一个流程时, 同步适合使用数据库字段或文件是否
    存在来加锁.

actor model
===========
- Actor model is a mathematical model of concurrent computation that treats
  "actors" as the universal primitives of concurrent computation.

- In response to a message that it receives, an actor can: make local
  decisions, create more actors, send more messages, and determine how to
  respond to the next message received.

- Actors may modify their own private state, but can only affect each other
  through messages, avoiding the need for any locks.

- Actor model has been used both as a framework for a theoretical understanding
  of computation and as the theoretical basis for several practical
  implementations of concurrent systems.

- Decoupling the sender from communications sent was a fundamental advance of
  the Actor model enabling asynchronous communication and control structures as
  patterns of passing messages.

- Recipients of messages are identified by address, sometimes called "mailing
  address". Thus an actor can only communicate with actors whose addresses it
  has. It can obtain those from a message it receives, or if the address is for
  an actor it has itself created.
