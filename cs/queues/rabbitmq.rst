overview
========
- RabbitMQ is a message broker software.

- It has a plug-in architecture, supporting many protocols.

- Written in Erlang.

Components
==========
- RabbitMQ server

- Gateways for various messaging protocols.

- Client libraries.

- Plugins.

Concepts
========

terms
-----

message
^^^^^^^
A message is a blob of binary data.

Message is produced by producer, queued in queue, consumed by consumer.

producer
^^^^^^^^
Producer produces message, i.e., it sends message.

consumer
^^^^^^^^
Consumer consumes message, i.e., it receives message.

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

A queue can be configured so that if no consumer is ready to consume the
passed-in messages, the messages will be dropped automatically.

A queue is a large message buffer, 队列的容量受限于内存和硬盘容量.

exchange
^^^^^^^^
Exchange routes a message to queues.

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

Server
======
- default port: 5672

Queue
=====
- declaring queue is idempotent operation. 但已声明的队列不能以不同的参数重新声
  明.

- durable queue is stored on disk.

binding
-------
- A queue binds to an exchange with an binding key. A binding key 最大长度是
  255 bytes.

- A queue can bind to an exchange multiple times, each time with a different
  binding key. 效果是这些 binding keys OR-ed, 满足至少一个 binding key 则会给这
  个队列发消息. 

- Multiple queue can bind to the same exchange with the same binding keys.

messaging
=========
- 当一个队列有多个 consumer 时, rabbitmq 会使用 round-robin 的方式将消息分发给
  这些 consumer, 这样在统计上每个 consumer 得到的消息数量是相同的.

- Manual acknowledgement: Consumer 接收消息后, 需要明确发送 ack. If a
  consumer's channel is closed, connection is closed, or TCP connection is lost
  without sending an ack, RabbitMQ will understand that a message wasn't
  processed fully and will re-queue it. 

  Ack must be sent on the same channel where the message delivery is made.

- No timeout is enforced on message by default. Message is only redelivered
  when it's not ack-ed when the worker's connection/channel is lost.

- Forgetting to ack message causes rabbitmq server can not release message from
  server, thus taking more and more memory, like a memory leak.

- message delivery mode.

  * non-persistent (1).

  * persistent (2).

  Marking messages as persistent doesn't fully guarantee that a message won't
  be lost. There is still a short time window when RabbitMQ has accepted a
  message and hasn't saved it yet. Also, RabbitMQ doesn't do fsync(2) for every
  message.

- fair dispatch. basic.qos. 在分发消息时考虑 consumer 当前的 message pressure.

exchange
========
- Exchange is like a router. Producer only sends message to an exchange. It's
  the responsibility of an exchange to route message to the appropriate
  queue(s).

- 当一个 exchange 收到 message 后, 它根据路由条件将消息发给所有符合条件的队列,
  若没有任何符合条件的队列, 则相当于消息直接被抛弃掉了.

- 一个 virtual host 中可以创建多个 exchange. 从而满足不同的需求.

- 可以把 exchange 看成是某种路由器. binding rules 就是它的路由表.

- default exchange 由 empty string 表示.

exchange types
--------------
exchange 类型: fanout, direct, topic, headers.

不同的 exchange type 有不同的匹配灵活度, 适合不同的应用场景, 具有不同的 CPU 计
算量和效率.

fanout
^^^^^^
no routing keys involved. 输入信息会发送给所有绑定的队列.  相当于 broadcasting.

direct
^^^^^^
message 的 routing key 与 queue binding 使用的值需要 exact match.

topic
^^^^^
- topic exchange 的 routing key 和 binding key 必须是 a dot separated hierarchy
  of words.

- 在路由匹配时, message routing key 与 queue binding 值进行 pattern matching.
  当队列指定 binding key 时, topic exchange 对以下 metachar 进行解析:

  * ``*`` is a pattern that matches any single word, when compared with a
    routing key. 例如, ``*.a.*``, ``a.b.*.*``
  
  * ``#`` is a pattern that matches one or more words, when compared with a
    routing key. 例如, ``a.#``.

- A binding key of ``#`` behaves like fanout exchange for this queue.

- A binding key without any metachar behaves like direct exchange for this
  queue.

Protocol Support
================
- AMQP

- STOMP

- MQTT

CLI
===

rabbitmqctl
-----------

list_queues
^^^^^^^^^^^

list_exchanges
^^^^^^^^^^^^^^

list_bindings
^^^^^^^^^^^^^

Client libraries
================

pika
----
- python client

Design Patterns
===============

Client-side programming
-----------------------
- always declaring a queue before using it.

- 根据使用场景决定是否使用 automatic acknowledgement mode. 若使用 manual
  acknowledgement, 设计合理的 ack 位置. 考虑在什么情况下不该 ack, 让消息重新排
  队.

- 一个队列和多个 consumer 的组合构成 task queue 的应用场景. Celery 就是这样.

- 一个 exchange 和多个队列的组合构成 publish/subscribe 的应用场景.

  * Producer declares an exchange of appropriate type, e.g., simple fanout,
    topic match, exact match etc.

  * Every consumer declares a temporary queue that is exclusive to its
    connection.
