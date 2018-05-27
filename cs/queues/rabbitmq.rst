Concepts
========

components
----------

virtual host
^^^^^^^^^^^^
A virtual host is a domain that holds a collection of exchanges, queues and
bindings.

在 rabbitmq 中, 一个 user 可操纵整个 virtual host 下的所有实体. 因此
需要 virtual host 进行多应用之间的隔离.

queue
^^^^^
队列用于传递 messages, messages 在队列中排队, 等待消费者 consume 这些信息.
Consumer 监听队列, 接收消息.

一般可能需要创建多个队列, 每个队列具有不同的目的或者功能区分等.

A queue can be configured so that if no consumer is ready to consume
the passed-in messages, the messages will be dropped automatically.

exchange
^^^^^^^^
Exchange 的作用是它决定输入的 messages 该去哪些队列中排队,
并把它们送入这些目的队列中. 它通过匹配 message 的 routing key 与自己
维持的 binding rule list, 选择目标队列.

exchange 具有三种类型: fanout, direct, topic. 对应着不同的匹配灵活度.
具有不同的 CPU 计算量和效率. 设计多种 exchange, 给用户提供了不同
的选择, 由用户去在灵活性和效率之间 tradeoff.

三种 exchange 的具体解释:

* fanout. no routing keys involved. 输入信息会发送给所有绑定的队列.
  相当于 broadcasting.

* direct. message 的 routing key 与 queue binding 使用的值需要
  exact match.

* topic. message routing key 与 queue binding 值进行 pattern matching.
  一个 routing key 由一组 dot separated hierarchy of words 组成.
  匹配时支持以下 metachar:

  - ``*`` matches any single word.

  - ``#`` matches one or more words.

一个 virtual host 中可以创建多个 exchange. 从而满足不同的需求.

可以把 exchange 看成是某种路由器. binding rules 就是它的路由表.

binding
^^^^^^^
Binding 是信息分配至队列的规则. 即满足什么样规则的信息去到哪个队列.
也可理解为, 队列是通过何种方式与该 exchange 进行绑定的.

一个队列通过指定 routing key pattern 与 exchange 进行绑定.

workflow
--------

一条信息包含 routing key 和要发送到的 exchange. exchange 根据
bindings 将信息发送给各个目的队列. Consumer 收到信息后, 给
队列返回 ack 完成该信息的工作流.

persistent messaging
--------------------

- procedure

  * When creating exchange, mark it durable.
  
  * When creating queue, mark it durable.
  
  * set message delivery mode to be 2 (persistent).

- The queue or exchange marked durable will be re-created automatically on
  reboot. Otherwise they won't.

- Persistent messages are written to disk during processing by rabbitmq.
  Note that this will take time therefore slow things down.
