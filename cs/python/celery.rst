Overview
========
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

features
--------

* HA:
  automatically retry in the event of connection loss or failure,
  and some brokers support HA in way of primary/primary or primary/replica
  replication.

* Fast: millions of tasks a minute with RabbitMQ.

* Major components have many different implementations as plugins, suitable for
  different needs.

* available integration solutions for many web frameworks: django, flask,
  tornado, pyramid, pylons, web2py.

functionalities
---------------
- event monitoring

- composing workflows

- task execution time limit

- task rate limit

- task scheduling

- resource leak protection

components
----------
- celery 的各个部分有提供了很多实现方式, 并与现有系统集成:

  * message transport: rabbitmq, redis, amazon SQS, zookeeper, pyro, slmq,
    consul.

  * concurrency: prefork, eventlet, gevent, single threaded

  * result backend: AMQP, redis, memcached (memcache, pymemcache), couchbase,
    sqlalchemy, django ORM, apache cassandra, IronCache, elasticsearch, riak,
    consul.

  * serialization: pickle, json, yaml, msgpack, zlib, bzip2,
    cryptographic message signing (auth).

  注意 librabbitmq 目前不支持 python3.

- RabbitMQ 是默认的 message broker, 并且应该是首选的 message broker.
  
  RabbitMQ 和 Redis 作为 message transport 都有很好的支持. 但似乎综合
  来看, rabbitmq 有更好的性能. (ref?)

language support
----------------

- native python

- client: node.js, php.

installation
============
- See [CeleryPip]_ for a list of available bundles for pip install.

Celery app
==========
- A ``Celery`` app instance is the entrypoint for everything. It must be
  possible for other modules to import it.

APIs
----

constructor options
^^^^^^^^^^^^^^^^^^^

- broker

- backend

- include.

app config
^^^^^^^^^^
- ``conf``

- ``config_from_object(<module>)``. 

Tasks
=====

task definition
---------------
- A task is a simple callable object wrapped by a task instance.

- 函数参数注意事项:

  * Don't pass complex objects as task paramters. Only pass JSON/msgpak, etc,
    serializable simple objects.

  * Don't pass database object as parameter. Only pass id, retrieve the object
    from db at the receiving end. The database object you passed might change
    in between the time you place the task and the time it gets executed.

states
------
- states transition: PENDING -> STARTED -> [RETRY -> STARTED]... -> SUCCESS|FAILURE

- STARTED state is available only if ``task_track_started`` is enabled
  or in a per-task setting.

- PENDING state is not a recorded state, but rather the default state for any
  task id that’s unknown.

methods
-------

delay
^^^^^
- Returns a ``AsyncResult``.

apply_async
^^^^^^^^^^^

Results
=======

attributes
----------

- traceback.

- backend.

- state.

methods
-------

- ``ready()``

- ``get()``.

  * If the task raised an exception, it is re-raised inside of the get call.

- ``failed()``

- ``successful()``

Result backend
--------------
- Result backend is required to keep track of tasks' states.
  默认不启用 result backend, 即默认配置下, 不可获取任务的状态和结果.

  如果任务发送端不需要知道任务状态和任务结果等信息, 则没必要配置 result backend.
  此时, 发送端就只能发送任务, 获取不到结果. 或者配置简单的 RPC backend.

- Result backends aren’t used for monitoring tasks and workers, for that Celery
  uses dedicated event messages.

RPC
---

- It sends state back as transient messages.

- 它对于每个 client 开一个队列.

AMQP
----
- 与 RPC result backend 同理, 但相比于 rpc 非常低效, 它对于每个任务都单独
  开一个队列.

worker
======

CLIs
----

celery worker
^^^^^^^^^^^^^
- Ctrl-c to stop foreground worker.

worker pool options
""""""""""""""""""""
- ``--pool``. worker pool to use. default prefork.

- ``--concurrency``. the number of worker processes. default is the
  number of logical CPUs on current system. 对每个 worker process,
  实施 ``--pool`` 指定的 worker pool 处理任务.

celery multi
^^^^^^^^^^^^

Serialization
=============
- 不要使用 pickle 作为 serializer, because of security vulnerability. By
  allowing complex objects, you are increasing the chances of getting exposed.

Concurrency
===========

number of processes
-------------------
- If tasks are mostly I/O-bound, try increase it bigger than the number of
  logical CPUs.

- Experimentation has shown that adding more than twice the number of CPU’s is
  rarely effective, and likely to degrade performance instead.

worker pools
------------

prefork
^^^^^^^

- prefork a number of worker processes to concurrently execute received tasks.

- 同时处理的最大任务数即 prefork 进程数.

- prefork is the default worker pool solution.

eventlet, gevent
^^^^^^^^^^^^^^^^
- eventlet, gevent workers 适合进行 async IO 相关的任务处理.
  一个重点是在这些 worker 中不要处理需要 blocking 操作的任务.

Routing
=======

- 不同 pool 类型的 workers 适合处理不同类型的任务.

- 可以通过设置不同的队列, 对任务进行分类. 在不同类型的 worker
  端, 监听不同的队列. 不同 worker 处理自己擅长的任务, 达到更有效
  的资源利用.

- 任务还可以分优先级, 并设置相应不同优先级的队列.

Monitoring
==========

- Worker can send task-related events.

Configuration
=============

- The configuration can be set by two means:
 
  * modifying attributes of the app instance: ``Celery.conf.<key>``.
    
  * using a dedicated configuration module: ``Celery.config_from_object()``.

message broker
--------------
- ``broker_url``

result backend
--------------
- ``result_backend``

celery CLI
==========

global options
--------------

- ``--app`` path of a celery app instance or a package that contains it.

  * format of celery app instance::

      module.name:attribute

  * searching in the following order for a Celery app instance if a package
    ``name`` is specified:

    - ``name.app``

    - ``name.celery``

    - Any attribute of ``name`` package that is an Celery instance.

    - Search in ``name.celery`` module again in the aforementioned order.

- ``--broker`` broker that overrides config file.

subcommands
-----------

- worker

- multi

References
==========
.. [CeleryPip] http://docs.celeryproject.org/en/latest/getting-started/introduction.html#installation
