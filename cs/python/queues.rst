General
=======

- Asynchronous task queues 经常用在 web 后端架构中, 用于 delegrate
  long-running tasks to a separate execution unit. 从而作为服务
  响应主体的 web server 可以迅速返回响应给客户端, 完成 request-response
  cycle.

- 交给任务队列去执行的任务, 一般具有以下特征:

  * long-running task.

  * Calling external API, whose execution time is not under control of the
    calling program.

  一些例子:

  * email user.

  * spread really large bulk database operations over time.

celery
======

Overview
--------
- Definition: Celery is a distributed task queue system.

- 注意 celery 的定义, 它是 task queue, 不是 message queue.
  Message queue 实现了一个功能: It receives and delivers messages.
  Task queue uses MQ as message broker to receive tasks (from user)
  and deliver results (to user).

  Celery 是 task queue, 它是以任务为核心的. 它所有的功能都是 task-oriented.
  It's not generic message receiving/delivery kind of stuff.

  常见的 web app 中的 out-of-cycle 任务处理方式: 从 request/response
  cycle 中发送某个信息至 MQ, 某个长期运行的 (worker) 进程接受该信息,
  处理后给出结果. Celery 做的事情就是将这各个环节封装起来, 成为易于
  使用的一系列 API, 从而省去手工构建上述流程的麻烦.
  
  We no longer need to learn or worry about the details of AMQP or RabbitMQ. We
  can use Redis or even a database (MySQL for example) as a message broker.
  Celery allows us to define "Tasks" with our worker codes. When we need to do
  something in the background (or even foreground), we can just call this task
  (for instant execution) or schedule this task for delayed processing.

- version: next version of celery (5.x) works only on python3.5+.

- features:

  * HA:
    automatically retry in the event of connection loss or failure,
    and some brokers support HA in way of primary/primary or primary/replica
    replication.

  * Fast: millions of tasks a minute with RabbitMQ.

  * integration for many web frameworks: django, flask, tornado, pyramid, pylons,
    web2py.

- celery 的各个部分有提供了很多实现方式, 并与现有系统集成:

  * message transport: rabbitmq, redis, amazon SQS, zookeeper, pyro, slmq, consul.

  * concurrency: prefork, eventlet, gevent, single threaded

  * result backend: AMQP, redis, memcached (memcache, pymemcache), couchbase,
    sqlalchemy, django ORM, apache cassandra, IronCache, elasticsearch, riak, consul.

  * serialization: pickle, json, yaml, msgpack, zlib, bzip2,
    cryptographic message signing (auth).

  注意 librabbitmq 目前不支持 python3.

- RabbitMQ 和 Redis 作为 message transport 是支持得最好的.

Tasks
-----

- Task states: PENDING -> STARTED -> SUCCESS|FAILURE

- task 参数注意事项:

  * Don't pass complex objects as task paramters. Only pass JSON/msgpak, etc,
    serializable simple objects.

  * Don't pass database object as parameter. Only pass id, retrieve the object
    from db at the receiving end. The database object you passed might change
    in between the time you place the task and the time it gets executed.

Calling
-------

Serialization
-------------
- 不要使用 pickle 作为 serializer, because of security vulnerability. By
  allowing complex objects, you are increasing the chances of getting exposed.

Result backend
--------------

- 如果任务发送端不需要知道任务状态和任务结果等信息, 则没必要配置 result backend.
  此时, 发送端就只能发送任务, 获取不到结果. 或者配置简单的 RPC backend.

RPC
~~~

- It sends state back as transient messages.

- 它对于每个 client 开一个队列.

AMQP
~~~~

- amqp result backend 相比于 rpc 非常低效, 它对于每个任务都单独开一个队列.

Configuration
-------------

- The configuration can be set on the app instance directly or by using a
  dedicated configuration module.
