Overview
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


Virtual hosts
=============
overview
--------
- Virtual hosts make rabbitmq a multi-tenant system.

- A virtual host is a logical grouping and separation of resources:
  connections, exchanges, queues, bindings, user permissions, policies and some
  other things.

- A client connection is bound to a specific vhost. Connections to a vhost can
  only operate in that vhost. "Interconnection" of e.g. a queue and an exchange
  in different vhosts is only possible when an application connects to two
  vhosts at the same time.

vhost creation
--------------
- Creating vhost is an expensive operation. So when multiple vhosts are created
  in a loop by HTTP or CLI tools, they may experience timeout.

- A newly created vhost will have a default set of exchanges but no other
  entities and no user permissions.

vhost deletion
--------------
- Deleting a virtual host will permanently delete all entities in it.


default vhost
-------------
- name ``/``

vhost limits
------------
Use ``rabbitmqctl set_vhost_limits``.

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

Messaging
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

Exchange
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

Overview
^^^^^^^^
- Clustering connects multiple machines together to form a single logical
  broker.

- A broker is a logical grouping of one or several Erlang nodes, each running
  the RabbitMQ application and sharing users, virtual hosts, queues, exchanges,
  bindings, and runtime parameters.

- When network partitioning is occurred, choose C and P from CAP theorem.

Requirements
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

- 当队列所在节点挂掉时,

  * durable queue become unavailable until the node comes back. All operations
    on a durable queue with unavailable master node will fail. (Consistency 要
    求. 若继续允许操作, 则该队列必须在别的节点上重新声明, 等原节点恢复上线后会
    造成冲突.)

  * non-durable queue is deleted. 因为所有可能具有的数据已经丢了. 此时, 访问
    该队列会报错, 需重新声明.

performance
"""""""""""
- 集群这种水平扩展的方式可以提高一个 broker 整体的 throughput, 例如每秒的消息处
  理数目. 这是因为机器曾多后可以容纳更多的队列.

- 但具体到某个队列, 集群并不能提高单个队列的 throughput. 这是因为, 一个队列默认
  只位于一个节点; 而在 mirrored queue 的情况下, 所有相关节点要做同等的工作, 也
  没有效率提升.

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

Queue mirroring
^^^^^^^^^^^^^^^

mechanism
"""""""""
- 默认情况下, 每个队列只位于一个节点上. 通过一些设置可以得到高可用的队列
  (mirrored queues).

- Queue mirroring 提高单个队列的可用性. 但不能提高单个队列的 throughput, 因为所
  有队列节点都干相同的活.

- Mirrored queues 有一个 master 和多个 mirror. Master queue 所在的节点被称为这
  个队列的 queue master.

- All operations for a given queue are first applied on the queue's master node
  and then propagated to mirrors. This is necessary to guarantee FIFO ordering
  of messages.

- Consumers are connected to the master regardless of which node they connect
  to.

- Mirrors drops messages that have been acknowledged at the master.

Failure handling
""""""""""""""""

* If the node that hosts queue master fails, the oldest mirror will be
  promoted to the new master as long as it synchronised. Unsynchronised
  mirrors can be promoted, too, depending on queue mirroring parameters. If
  there is no mirror that is synchronised with the master, messages that only
  existed on master will be lost.

* The mirror considers all previous consumers to have been abruptly
  disconnected. It requeues all messages that have been delivered to clients
  but are pending acknowledgement.

  This can include messages for which a client has issued acknowledgements,
  say, if an acknowledgement was either lost on the wire before reaching the
  node hosting queue master, or it was lost when broadcast from the master to
  the mirrors. (这是 queue cancellation notification 机制的原因之一. 即客户端
  可能需要处理这种情况: 客户端以为自己已经处理完了消息, 但却由收到了同一个消息.
  但也许更好的方式, 是尽量保证任务的等幂性.)

* Should a mirror fail, there is little to be done other than some
  bookkeeping: the master remains the master and no client need take any
  action or be informed of the failure.

* Messages published to a node that hosts queue mirror are routed to the queue
  master and then replicated to all mirrors. Should the master fail, the
  messages continue to be sent to the mirrors and will be added to the queue
  once the promotion of a mirror to the master completes.

* 当一个原来有 queue mirror 的节点重启后, 若仍成为同一个 queue 的 mirror, 则 it
  throws away any durable local contents it already has and starts empty. 这是
  因为重启后, mirror 无法判断自己是否跟 master 的内容仍然是一致的.

configuration
"""""""""""""
- 通过一系列 policy 参数, 对匹配的队列设置 mirroring:
  ``ha-mode``, ``ha-params``.

- 由于是通过 policy 进行设置, mirroring can be applied and unapplied at any
  time.

- policy:

  * exactly. 指定 repilca 的数目 (master + mirror). ha-params 值为所需数目. If
    a node containing a mirror goes down, then a new mirror will be created on
    another node. If there are fewer than count nodes in the cluster, the
    queue is mirrored to all nodes.
    
    使用这种 policy 时, 建议的 replica 数目为 ``N/2+1``. 当然, 若节点比较多, 并
    且对实时性要求比较高时, 可以在保证可用性的基础上降低 replica 数目.

  * all. Mirrored on all nodes. ha-params 不需要.

  * nodes. ha-params is a list of node names. node name 是 ``cluster_status``
    输出的 node name. If any of those node names are not a part of the cluster,
    this does not constitute an error. If none of the nodes in the list are
    online at the time when the queue is declared then the queue will be
    created on the node that the declaring client is connected to.

performance
"""""""""""
- Queue mirroring 会降低队列的 throughput. 因为与单节点的队列相比, 有更复杂的
  状态机制, 例如跨节点的状态需要同步和保持.

queue master
""""""""""""
- Queue master 的决定方式由 queue-master-locator 配置项决定. 该配置可以在三层
  进行配置:

  * ``x-queue-master-locator`` argument during queue declaration.

  * ``queue-master-locator`` policy key.

  * ``queue_master_locator`` config key.

  配置值:

  * min-masters. node with minimum number of bound masters.

  * client-local. node where client declared the queue.

  * random.

- master migration. 若在应用新的配置后, 导致新的 queue master 与现有 master 不
  同, order to prevent message loss, RabbitMQ will keep the existing master
  around until at least one other mirror has synchronised (even if this is a
  long time). However, once synchronisation has occurred things will proceed
  just as if the node had failed: consumers will be disconnected from the
  master and will need to reconnect.

exclusive queue
"""""""""""""""
- exclusive queue is never mirrored and never durable.

failover and client
"""""""""""""""""""
- For clients wanting to know about failover, they can consume with
  ``x-cancel-on-ha-failover: true`` as argument.

mirror synchronization
""""""""""""""""""""""
- synchronization mode policy, ``ha-sync-mode``:
 
  * manual. When a queue is mirrored on a new node, mirror will receive new
    messages published to the queue, and thus over time will accurately
    represent the tail of the mirrored queue.

    As messages are drained from the mirrored queue, the size of the head of
    the queue for which the new mirror is missing messages, will shrink until
    eventually the mirror's contents precisely match the master's contents.
    Then a queue considered fully synchronized.

  * automatic. synchronize messages enqueued before the queue mirror is
    created, from master to the mirror.

    When automatic synchronization is happening, the queue is blocked.

- Automatic synchronization can be triggered explicitly via
  ``rabbitmqctl sync_queue``.

- Batch synchronization. ``ha-sync-batch-size`` queue argument. If the network
  takes longer than net_ticktime to send one batch of messages, then nodes in
  the cluster could think they are in the presence of a network partition.

  So to tune this value, you need to consider:

  * average message size

  * net_ticktime value

  * network throughput

mirror promotion policies
"""""""""""""""""""""""""
- ``ha-promote-on-failure``, policy during an uncontrolled master shutdown
  (i.e. server or node crash, or network outage):

  * when-synced. unsynchronised mirrors are not promoted. This avoids data loss
    due to promotion of an unsynchronised mirror but makes queue availability
    依赖于同步性和 master 的状态.  In the event of queue master node failure,
    若 master/slave 仍是同步的 (例如没有新消息), 只要 master/mirror 有一点点不
    同步 (例如因为刚来的尚未同步的新消息), the queue will become unavailable
    until queue master recovers. In case of a permanent loss of queue master
    the queue won't be available unless it is deleted and redeclared.

  * always (default). unsync queue can be promoted. This ensures max
    availability.

- ``ha-promote-on-shutdown``, policy during a controlled master shutdown (i.e.
  explicit stop of the RabbitMQ service or shutdown of the OS):

  * when-synced (default). Refuse to promote an unsynchronised mirror on in
    order to avoid message loss.

  * always.

Client connection
^^^^^^^^^^^^^^^^^
- 在客户端连接至任意节点时, 可访问整个集群中的所有实体.

  * 对于 queue 相关操作, nodes will route operations to the queue master node
    transparently.

- In case of a node failure, clients should be able to reconnect to a different
  node, recover their topology and continue operation. 这可由以下方式实现:

  * 客户端配置 a list of node's hostname/ip 等以供选择连接.

  * 客户端只配置一个 hostname, 由其他机制保证多态切换和负载均衡. 例如 DNS 或
    TCP load balancer.

Use case
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

Parameters and Policies
=======================

overview
--------
- Parameters and policies are used for configs that have the following
  properties:

  * needs to be applied at cluster-level, rather than node specific.

  * likely to change at run time.
 
  Therefore they are not suitable in static node configuration file.

- 2 kinds of parameters: vhost-scoped parameters and global parameters.

- Policies are a special case of parameters. Policies are vhost-scoped.

parameters
----------
- Set vhost-specific parameters via ``rabbitmqctl set_parameter``

- Set global parameters via ``rabbitmqctl set_global_parameter``

policies
--------
- Policies is used to solve the following problems:

  * Setting exchanges/queues' x-arguments in client applications are
    inflexible, which requires modifying client applications. We want flexible
    settings from server-side.

  * to control the extra arguments for groups of queues and exchanges.

- How policy works:
  
  * A policy matches one or more entities by name and appends its definition to
    the x-arguments of the matching entities.

  * Each exchange/queue has at most one (combined) policy in effect.

  * A policy can match exchanges, queues, or both. This is defined by
    ``apply-to`` option.

  * When policy is changed, its effect on matching exchanges and queues will be
    reapplied.

  * When new entities are created, matching policy is applied.

- Policy definition:

  * name: any unicode

  * pattern: an regex matching any entity names.

  * definition: JSON object.

  * priority. The policy with highest priority is applied.

operator policies
-----------------
- Operator policies, don't just overwrite regular policy values. They enforce
  limits but try to not override user-provided policies where possible.


Authentication and Authorization
================================

default user
------------
- name: guest, pass: guest. full access to default ``/`` vhost.

- default vhost, user/pass are created when the database is uninitialized.

- By default, guest user is prohibited from connecting to the broker remotely.

ACL mechanism
-------------

vhost level
^^^^^^^^^^^
该层 ACL 在客户端连接时校验. 当一个用户向 vhost 连接时, 只有当该用户在这个
vhost 中具有权限条目时才允许连接. 然而注意只要有权限即可, 即使全部都是 ``^$``
也可以.

entity level
^^^^^^^^^^^^
该层 ACL 在客户端对相应实体进行操作时校验. 对一个资源实体, 存在 configure,
write and read 三类权限.

- configure. create or destroy resources, or alter their behavior.

- write. inject messages into a resource.

- read. retrieve messages from a resource.

一个 AMQP 操作可能涉及多个实体的权限. See [ACLDoc]_ for details.

Permission definition
---------------------
- format::

    <configure> <write> <read>

  每项为一个正则, 匹配该 vhost 中的一系列实体. 对用户授予所有匹配到的实体的相应
  权限.

  * For convenience, default blank exchange is aliased to amq.default for
    matching.

  * ``^$`` and ``''`` means to grant no permissions.

Permission caching
------------------
- RabbitMQ may cache the results of access control checks on a per-connection
  or per-channel basis. Hence changes to user permissions may only take effect
  when the user reconnects.


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

Production Checklist
====================
vhost
-----
- single-tenant: use default / vhost is fine.

- multi-tenant: use a separate vhost for each tenant.

users
-----
- delete default guest user.

- Use a separate user per application.

- generate strong password.

- Credentials roll-over (e.g. periodically or in case of a breach).

- If needed, set up fine-grained permissions.

memory
------
- ``vm_memory_high_watermark``. RabbitMQ will not accept any new messages when
  it detects that it's using more than this amount of the available memory.

  Leave enough memory for kernel, processes and caching. Otherwise swapping and
  OOM might happen.  recommended 0.40 to 0.66. The OS and file system must be
  left with at least 30% of the memory, otherwise performance may degrade
  severely due to paging.

- node's available memory (``free`` output) should always be at least 128MB.

storage
-------
- Insufficient disk space will lead to node failures and may result in data
  loss as all disk writes will fail.

- ``disk_free_limit.relative``.

  * 1.0. minimum recommended.

  * 1.5. safer. If RabbitMQ needs to flush to disk memory worth of data, there
    will be sufficient disk space available for RabbitMQ to start again. 

  * 2.0. most conservative. full confidence in RabbitMQ having all the disk
    space that it needs, at all times.

file descriptor
---------------
- Make sure your environment allows for at least 50K open file descriptors for
  effective RabbitMQ user

  65536 (recommended). via:

  * kernel parameter: ``fs.file-max`` (global max)

  * systemd service limit::

      [Service]
      LimitNOFILE=65536

Erlang cookie
-------------
- should be cryptographically generated.

cluster
-------
- Try making consumers and producers connect to the same node, if possible:
  this will reduce inter-node traffic.

- Equally helpful would be making consumers connect to the node that currently
  hosts queue master.

Time synchronization
--------------------
- Node time should be synced. It does not affect cluster operation, but it does
  affect plugins such as management statistics.

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
- prefer long-lived TCP connection to rabbitmq server.

  * open connection is expensive.

  * Under continuous short-lived connection, server might experience connection
    churn. Then node must be tuned to release TCP connections much quicker than
    kernel defaults, otherwise they will eventually run out of file handles or
    memory and will stop accepting new connections.

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

- 客户端程序必须实现可靠的 connection recovery 机制 (或者由客户端库来实现).  这
  是用于解决以下几种情况:

  * 网络问题, 导致连接断开.

  * 集群中节点挂掉, 导致连接断开.

- clients that consume from the queue must be aware that they are likely to
  subsequently receive messages that they have already received. 这种消息重复可
  能源于多种情况:

  * 客户端本身的问题, 例如处理中断等.

  * 在 rabbitmq 集群中, 客户端发送 ack 表示自己处理完成后, queue master 节点可
    能挂掉而没收到 ack. 这样在有 mirrored queue 时, 集群会再次发送该信息.

- Channels are meant to be long-lived. Applications should minimize the number
  of channels they use when possible and close channels that are no longer
  necessary.

References
==========
.. [Kafka-vs-RabbitMQ] `Understanding When to use RabbitMQ or Apache Kafka <https://content.pivotal.io/blog/understanding-when-to-use-rabbitmq-or-apache-kafka>`_
.. [SOKafka-vs-RabbitMQ] `Is there any reason to use RabbitMQ over Kafka? <https://stackoverflow.com/questions/42151544/is-there-any-reason-to-use-rabbitmq-over-kafka>`_
.. [ACLDoc] `Access Control (Authentication, Authorisation) in RabbitMQ <https://www.rabbitmq.com/access-control.html>`_
