overview
========
- RabbitMQ is a message broker software.

- It has a plug-in architecture, supporting many protocols.

- Written in Erlang.

Installation
============
Ubuntu
------
- setup erlang repo and rabbitmq repo.

- pin erlang packages version by apt/preferences.d

- install:

  * erlang-nox

  * init-system-helpers

  * rabbitmq-server

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

Networking
==========

default ports
-------------
- 4369: epmd. peer discovery service

- 5672, 5671: for AMQP client connections

- 25672: erlang distribution server port, inter-node and CLI tools
  communication (dynamic: AMQP port + 20000)

- 35672-35682: Erlang distribution client ports for communication with nodes
  (dynamic: server distribution port + 10000 through server distribution port +
  10010)

- 15672: HTTP API clients (management plugin)

- 61613, 61614: STOMP clients

- 1883, 8883: MQTT clients

- 15674: STOMP over websocket

- 15675: MQTT over websocket

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



Cluster
=======

Clustering
----------

overview
^^^^^^^^
- Clustering connects multiple machines together to form a single logical
  broker.

- A broker is a logical grouping of one or several Erlang nodes, each running
  the RabbitMQ application and sharing users, virtual hosts, queues, exchanges,
  bindings, and runtime parameters.

- When network partitioning is occurred, choose C and P from CAP theorem.

requirements
^^^^^^^^^^^^
- all nodes in the cluster must have the same Erlang cookie.

- 网络必须可靠, 所有节点的 rabbitmq + erlang 版本必须相同.

- Hostnames or FQDNs of all cluster members must be resolvable from all cluster
  nodes, as well as on hosts where rabbitmq CLIs are invoked.

  * 节点之间默认使用 hostname, 可配置使用 FQDN.

- 一个节点必须在 reset 之后才能加入 new cluster.

Forming a cluster
^^^^^^^^^^^^^^^^^
- blank node: A reset erlang node, without rabbitmq app running.

- 构建集群可通过 CLI 手动的方式, 或多种 peer discovery 的方式. 每种 peer
  discovery 是由一种 backend 来实现的.

- Config file and DNS 是两种 builtin 的 peer discovery backend. 其他后端可由
  plugin 实现.

- Config key for peer discovery backend:
  ``cluster_formation.peer_discovery_backend``.

peer discovery mechanism
""""""""""""""""""""""""
一个节点启动时, 若存在状态数据, 会按保存的状态运行. 若没有状态数据, 它会按照配
置的 peer discovery mechanism 来 discovery and contact peers. 若找到了 peers,
它会尝试加入第一个 reachable peer 所属的集群.

If peer discovery isn't configured, or it fails, or no peers are reachable, a
node that wasn't a cluster member in the past will initialise from scratch and
proceed as a standalone node.

If a node previously was a cluster member, it will try to contact its "last
seen" peer for a period of time. It will not perform peer discovery.

If a node is reset since losing contact with the cluster, it will behave like a
blank node. Note that other cluster members might still consider it to be a
cluster member, in which case there two sides will disagree and the node will
fail to join. Such reset nodes must also be removed from the cluster using
``rabbitmqctl forget_cluster_node`` executed against an existing cluster
member.

A node rejoining after a node name or host name change can start as a blank
node if its data directory path changes as a result. Such nodes will fail to
rejoin the cluster.

via rabbitmqctl
"""""""""""""""
::

  sudo rabbitmqctl stop_app && \
  sudo rabbitmqctl reset && \
  sudo rabbitmqctl join_cluster ... && \
  sudo rabbitmqctl start_app

via config file
"""""""""""""""
- 配置文件::

  cluster_formation.peer_discovery_backend = rabbit_peer_discovery_classic_config
  cluster_formation.classic_config.nodes.<N> = rabbit@<hostname>

- 注意 ``rabbit@`` 部分.

- 配置完成后, 要重置 reset 每个节点, 并停止进程::

    sudo rabbitmqctl stop_app && \
    sudo rabbitmqctl reset && \
    sudo systemctl stop rabbitmq-server.service

- 注意启动服务时, 必须一个一个启动.

- 每个节点必须有相同的 erlang cookie.

- location:

  * server: /var/lib/rabbitmq/.erlang.cookie

  * CLI tools: $HOME/.erlang.cookie

via DNS
"""""""

Mechanisms
^^^^^^^^^^

entities
""""""""
- 以下实体和数据自动复制到各个节点:

  * virtual hosts

  * exchanges

  * users

  * permissions

  queues 默认不复制, 只在一个节点上.

- 不同的节点上可以有不同的队列, 也可以进行 mirroring.

node relation
"""""""""""""
- A standalone node is equivalent to a cluster with one node. Any other node
  can join it to form a larger cluster.

- All nodes in a cluster are equal peers. queue mirroring will complicate this
  a little bit.

- CLI tools can be executed against any node.

node authentication
"""""""""""""""""""
- For two nodes to be able to communicate they must have the same shared Erlang
  cookie. 

- Erlang cookie is a string of alphanumeric characters up to 255 characters.

- Erlang cookie must be only readable to the rabbitmq user (0600).

- If the file does not exist, Erlang VM will try to create one with a randomly
  generated value when the RabbitMQ server starts up.

node failure handling
"""""""""""""""""""""
- Nodes can be started and stopped at will, as long as they can contact a
  cluster member node known at the time of shutdown.

node stop and start
"""""""""""""""""""
- When new node joined a cluster, it automatically sync from other nodes.

- A stopping node picks an online cluster member (only disc nodes will be
  considered) to sync with after restart. Upon restart the node will try to
  contact that peer 10 times by default, with 30 second response timeouts. In
  case the peer becomes available in that time interval, the node successfully
  starts, syncs what it needs from the peer and keeps going. If the peer does
  not become available, the restarted node will give up and voluntarily stop.

- When a node has no online peers during shutdown, it will start without
  attempts to sync with any known peers. It does not start as a standalone
  node, however, and peers will be able to rejoin it.

- When the entire cluster is brought down therefore, the last node to go down
  is the only one that didn't have any running peers at the time of shutdown.
  That node can start without contacting any peers first. Since nodes will try
  to contact a known peer for up to 5 minutes (by default), nodes can be
  restarted in any order in that period of time.

- In some cases the last node to go offline cannot be brought back up. It can
  be removed from the cluster using the ``rabbitmqctl forget_cluster_node`` 
  command.

- ``rabbitmqctl force_boot`` command can be used on a node to make it boot
  without trying to sync with any peers (as if they were last to shut down).
  This is usually only necessary if the last node to shut down or a set of
  nodes will never be brought back online.

node leaving cluster
""""""""""""""""""""
- reset a node for it to leave voluntarily from a cluster.

- ``rabbitmqctl forget_cluster_node`` to tell cluster to remove a node. But
  the node itself does not know it. For itself to forget the membership, it
  must be reset as well.

- The last node in a cluster need not be reset.

node storage
""""""""""""
- A node can be a disk node or a RAM node.

- 集群必须有至少一个 disk node. It's not possible to manually remove the last
  remaining disk node in a cluster.

  A cluster containing only RAM nodes is fragile; if the cluster stops you will
  not be able to start it again and will lose all data. RabbitMQ will prevent
  the creation of a RAM-node-only cluster in many situations, but it can't
  absolutely prevent it.

- disk nodes store internal database tables on disk and RAM. RAM node 只保存这
  些信息在内存中. 这不包含 messages, message store indices, queue indices and
  other node state. Therefore, the performance improvements will affect only
  resource management (e.g. adding/removing queues, exchanges, or vhosts), but
  not publishing or consuming speed.

- RAM nodes are a special case that can be used to improve the performance
  clusters with high queue, exchange, or binding churn.

  注意 RAM node do not provide higher message rates.

- For RAM node, on startup they must sync database from a peer node on startup.

client connection
^^^^^^^^^^^^^^^^^
- 在客户端连接至任意节点时, 可访问整个集群中的所有实体.

  * 对于 queue 相关操作, nodes will route operations to the queue master node
    transparently.

- In case of a node failure, clients should be able to reconnect to a different
  node, recover their topology and continue operation. 这可由以下方式实现:

  * 客户端配置 a list of node's hostname/ip 等以供选择连接.

  * 客户端只配置一个 hostname, 由其他机制保证多态切换和负载均衡. 例如 DNS 或
    TCP load balancer.

use case
^^^^^^^^
* HA

* increase throughput

* 机器在同一机房.

Federation
----------
- Federation allows an exchange or queue on one broker to receive messages
  published to an exchange or queue on another. 注意这里 broker 指的是 logical
  broker.

- When network partitioning is occurred, choose A and P from CAP theorem.

- 网络可以不可靠, Exchanges and queues are connected via AMQP. 各 broker 可以
  运行不同版本的 rabbitmq and erlang.

- Consumer 连接任何 broker 只能看见该 broker 中的队列.

- use case:

  * link brokers across the internet.

Shovel
------
- Similar to federation, but at a lower level.

- Whereas federation aims to provide opinionated distribution of exchanges and
  queues, the shovel simply consumes messages from a queue on one broker, and
  forwards them to an exchange on another.

- use case:

  * link brokers across the internet, with more control than federation.

Dynamic Shovel
--------------
- use case:

  * moving messages around in an ad-hoc manner on a single broker

Protocol Support
================
- AMQP

- STOMP

- MQTT

Server
======

hostname consideration
----------------------
- by default RabbitMQ names the database directory using the current hostname
  of the system. If the hostname changes, a new empty database is created. To
  avoid data loss it's crucial to set up a fixed and resolvable hostname.

- Whenever the hostname changes RabbitMQ node must be restarted.

process properties
------------------
- run as rabbitmq user.

logging
-------
- systemd journal.

System Configuration
====================
- file descriptor limit: 65536 (recommended). via:

  * kernel parameter: ``fs.file-max`` (global max)

  * systemd service limit::

      [Service]
      LimitNOFILE=65536

Configuration
=============

means of configuration
----------------------
- configuration files

- environment variables

- runtime parameters and policies

configuration file
------------------

main config
^^^^^^^^^^^
- format: sysctl::

    key = value

  Line starting with # is comment.

- location: /etc/rabbitmq/rabbitmq.conf

advanced config
^^^^^^^^^^^^^^^
- format: erlang term.

- location: /etc/rabbitmq/advanced.config.

check config
^^^^^^^^^^^^
- check configuration: rabbitmqctl environment

config items
^^^^^^^^^^^^

environment variables
---------------------

env file
^^^^^^^^
- location: /etc/rabbitmq/rabbitmq-env.conf

CLI
===

rabbitmqctl
-----------
- cluster mode.
 
  * 在 cluster 中, 一部分子命令是 "cluster-wide" 的, 另一些是 "node-local" 的.

  * "cluster-wide" commands will often contact one node first, discover cluster
    members and contact them all to retrieve and combine their respective
    state.

list_queues
^^^^^^^^^^^

list_exchanges
^^^^^^^^^^^^^^
- output formatting:
 
  .. code:: sh

     rabbitmqctl list_exchanges | column -s $'\t' -t

list_bindings
^^^^^^^^^^^^^

environment
^^^^^^^^^^^
- check application environment, i.e., its configuration.

forget_cluster_node
^^^^^^^^^^^^^^^^^^^

set_cluster_name
^^^^^^^^^^^^^^^^

cluster_status
^^^^^^^^^^^^^^

start_app
^^^^^^^^^

stop_app
^^^^^^^^

reset
^^^^^

Client libraries
================

pika
----
- python client



Architecture
============
- smart broker, dumb consumer model.

- Decoupling producers from queues via exchanges ensures that producers aren't
  burdened with hardcoded routing decisions. 

Use case
========
- Your application needs to work with any combination of existing protocols
  like AMQP 0-9-1, STOMP, MQTT, AMQP 1.0.

- Needs complex routing scheme, to integrate multiple apps with message queue.

- Your application needs variety in point to point, request / reply, and
  publish/subscribe messaging

- Traditional message queue application like rabbitmq is often used in web
  architecture.

- When messaging throughput does not need to be extremely high, like those in
  kafka.

- RabbitMQ 的设计就让它适合做一般性服务之间的消息传递. 而不适合做大数据类型的消
  息传递.

Client-side programming
=======================
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

- 使用消息队列实现 (同步) RPC model.

  * request side 声明一个 reply queue. 发送消息至 request queue, 消息属性中附上
    ``reply_to`` and ``correlation_id``.

  * response side 收到消息后, 执行操作, 将结果返回至 ``reply_to`` queue, 附上
    ``correlation_id``.

  * request side 监听 ``reply_to`` queue, 注意要检查收到的消息的
    ``correlation_id`` 是否与原消息相符.

References
==========
.. [Kafka-vs-RabbitMQ] `Understanding When to use RabbitMQ or Apache Kafka <https://content.pivotal.io/blog/understanding-when-to-use-rabbitmq-or-apache-kafka>`_
.. [SOKafka-vs-RabbitMQ] `Is there any reason to use RabbitMQ over Kafka? <https://stackoverflow.com/questions/42151544/is-there-any-reason-to-use-rabbitmq-over-kafka>`_
