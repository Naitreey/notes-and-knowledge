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

task routing
------------
两种方式:

- 静态配置: ``task_routes``

- dispatch 时设置: ``apply_async(queue=...)``

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

  * ``wait()`` is a deprecated alias of ``get()``.

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

Canvas
======
- Canvas 的用处和价值.

  * 如果我们每次请求执行任务时, 只需要异步执行一个单独的任务, 那么 ``Task.delay()``
    即可满足需求. 但很多时候并没有这么简单. 可能需要异步执行多个任务, 且任务之间
    存在依赖关系和执行顺序问题. 也就是说, 我们请求执行的是一个多步骤的任务流.
    
    最简单的解决办法是在上一步任务中同步或异步地调用下一步任务. 这样显然是有很多
    缺陷的. 首先, 强制给任务之间写入关联, 造成了任务之间的强耦合, 各个任务不再能够
    独立执行. 其次, 这种方式有很大的局限性, 对于复杂的关系流, 比如涉及分支和汇聚过程,
    变得难以维护. 显然, 任务之间应该是无显性关联的, 任务之间要保持逻辑独立.

  * Canvas 的意义, 就在于提供一种机制能够将多个独立任务组织起来, 成为一个复杂的异步
    任务流. 一次构建, 一次分发, 分发后任务的依赖关系和执行顺序内部自动解决.

Signature
---------
- A Signature wraps the arguments and execution options of a single task
  invocation. A signature 类似于 partially applied function.

- 与普通的 partially applied function 不同, 初始化 Signature 时, 传入的参数是靠右侧
  填充的. 例如::

    @app.task
    def f(a,b,c):
        pass

    f.s(1,2) # b == 1, c == 2
    f.s(1,2).delay(3) # a == 3

- A Signature supports the Task APIs, such as being asynchronously dispatched,
  invoked directly, etc. 在 call Signature 时, 提供的 kwargs overrides those passed
  in Signature initialization.

methods
^^^^^^^

- ``apply_async()``

- ``delay()``

primitives
----------
- Primitives are special Signature subclasses that serves as job workflow
  orchestration toolset.

- Primitives wraps 一系列的 Signatures, 生成一个新的 Signature, 作为一个 workflow.
  如果其中包含 partial signatures, 在 dispatch workflow Signature 时, 可以一起填充
  缺失的参数.

group
^^^^^
- A group calls an iterable of tasks in parallel.

chain
^^^^^
- A chain links tasks together to be executed sequentially, where the output of
  the previous task's signature is feed as input of the next task's signature.

- A bitwise OR-ed sequence of Signatures is chained automatically.

constructor
""""""""""""
- A bitwise OR-ed sequence of Task Signatures.

chord
^^^^^
- A chord is a group with callback task. In other words, the iterable of tasks
  are executed in parallel, of which the results are feed into the callback task.

- A group chained to another task will be automatically converted to a chord.

map
^^^

starmap
^^^^^^^

chunks
^^^^^^

worker
======
- 使用不同 pool 类型的 workers 适合处理不同类型的任务.

- 可以通过设置不同的队列, 对任务进行分类. 在不同类型的 worker 端,
  监听不同的队列 (``--queues`` option). 不同 worker 处理自己擅长的任务,
  达到更有效的资源利用.

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

- ``--events``. send task events for monitoring.

queue options
""""""""""""""
- ``--queues``, 指定该 worker 监听的队列.

embedded beat options
""""""""""""""""""""""
- ``--beat``. embed celery beat scheduler in this worker. 这导致该
  worker 只能运行一个实例.

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

Routing and Messaging
=====================

- 一些 routing 设计考虑的方面:

  * 考虑 worker 的类型: prefork, eventlet, gevent. 接受不同类型
    的任务.

  * 任务的优先级.

  * 常规任务或周期性任务.

routing configs
---------------

exchange, queue, bindings setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- define queues: ``task_queues``. A list of ``kombu.Queue``. The default is a
  queue/exchange/binding key of ``celery``, with exchange type ``direct``.

  Celery automatically create entities necessary for these queue configuration
  to work. For example, in rabbitmq, creating necessary exchanges, queues,
  bindings.

- define ``task_default_queue`` used for tasks that don't have explicit routing
  key.

- define ``task_default_delivery_mode`` used for tasks that don't have explicit
  delivery mode.

- define ``task_default_exchange``, ``task_default_exchange_type``,
  ``task_default_routing_key``, 作为 ``task_queues``
  中各个 Queue 的参数的默认值.

task routing setup
^^^^^^^^^^^^^^^^^^
- define task routers. ``task_routes`` 集中定义了各个 task 在 dispatch 时生成的
  message 的路由参数是什么样的. 从而能够到达预期的队列, 被预期的 worker 接受.

  ``task_routes`` is a single router or a list of routers. When sending tasks,
  the routers are consulted in order. The first router that doesn’t return None
  is the route to use. A router is one of the following:

  * A router function.

  * import path string to a router function.

  * A dict containing router specification.

  * A list of key-value pairs equivalent to a router specification dict. This
    is useful if the order of matching keys in router spec dict is significant.

  In a router specification dict (or its list equivalent),
  
  * key can be:
    
    - task's import path string
     
    - glob pattern matching task's import path string

    - regex object matching task's import path string

  * value is a routing config dict containing any combination of following
    keys:

    - ``queue``

    - ``exchange``

    - ``routing_key``

  A router function has
  
  * signature::

      (name, args, kwargs, options, task=None, **kwargs)

  * return value: if the router does not know the route of the task to take, it
    returns None; otherwise it returns the name of a queue defined in
    ``task_queues`` or a dict of custom routwrouting configs.
  

routing determination
---------------------
A task's final routing config fields are determined in the following order,
with the same parameter values in the former override those in the latter:

- Config values returned by routers defined in ``task_routes``.

- The routing arguments to ``Task.apply_async()``.

- Routing configs related attributes defined on the Task itself.

message protocol
----------------

message format
^^^^^^^^^^^^^^
- headers.

  * content type. the serialization format of message.

  * encoding

- body.

  * task name

  * task uuid

  * task args

  * task kwargs

  * metadata

AMQP API
--------
basic.publish

queue.declare

basic.ack

exchange.declare

queue.delete

basic.get

exchange.delete

queue.bind

queue.purge

AMQP CLI
--------

celery amqp
^^^^^^^^^^^
- used for low-level message broker administration.

- support tab completion.

- commands are direct counterparts to AMQP APIs.

Monitoring
==========

- Worker can send task-related events.

- Remote control and inspection of worker at runtime can be done if
  message broker is rabbitmq, redis, qpid etc.

CLI
---

celery inspect
^^^^^^^^^^^^^^
- inspect worker.

celery control
^^^^^^^^^^^^^^
- control worker

- operations.

  * enable_events

  * disable_events

celery events
^^^^^^^^^^^^^
- show events sent by workers.

celery status
^^^^^^^^^^^^^
- shows online workers.

Periodic tasks
==============
- Periodic tasks are registered from the ``beat_schedule`` settings or
  other configured sources (like SQL database).

- Periodic tasks are executed by the ``celery beat`` process.
  Only one beat process can be run at a time.

- The tasks may overlap if the first task doesn’t complete before the next. If
  undesirable, use some locking strategy to prevent this.

scheduler classes
-----------------

PersistentScheduler
^^^^^^^^^^^^^^^^^^^

- This is the default scheduler.
 
- It automatically detects timezone changes, and reset the schedule.

- It uses a local shelve database file to keep track of task run times
  (``--schedule`` option).

task entries
------------

- ``app.on_after_configure.connect``. 添加 task 至 ``beat_schedule``.

- manually add tasks in ``beat_schedule``, which is a dict of schedule
  names to schedule configs.

  * task. import path string of task.

  * schedule. the number of seconds, a timedelta, a crontab, or other
    custom schedule values.

  * args. list or tuple.

  * kwargs. dict.

  * options. options for ``apply_async``

  * relative.

schedule types
--------------


crontab
^^^^^^^

solar
^^^^^
- Schedule events according to solar events at a specific location on earth.

CLI
---

celery beat
^^^^^^^^^^^
::

  celery -A proj beat

- For development, celery beat can be embedded in celery worker.

- ``--schedule``. path of schedule database.

timezone
========
- All times and dates, internally and in messages uses the UTC timezone.

- UTC time from/to local time conversion is based on ``timezone`` setting.
  (For django, ``TIME_ZONE`` setting.)

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

routing
-------

- ``task_routes``

- ``task_create_missing_queues``

- ``task_queues``

- ``task_default_queue``

- ``task_default_exchange``

- ``task_default_routing_key``

monitoring
----------

- ``worker_send_task_events``

periodic tasks
--------------

- ``beat_schedule``

django integration
==================
- Celery has builtin support for Django. 通过一些设置, celery 可以加载
  django project 中所有 installed apps 中的 tasks. Optionally, celery
  can also load configs from Django's settings module.

setup
-----
- main celery module in global app: ``proj/proj/celery.py``.
  
  * 设置独立加载 django project 所需配置
    
  * 初始化 celery app

  * 从 django settings 中加载 celery 配置.

  * 自动从 ``<app_name>/tasks.py`` 加载 tasks.

  ::

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "enoc.settings")

    app = Celery("enoc")
    app.config_from_object("django.conf:settings", namespace="CELERY")
    app.autodiscover_tasks()

- global app's init file: ``proj/proj/__init__.py``.

  * 加载 celery app instance. 对于 celery worker, 这一步并不需要. 这是
    为了能够在 django project 中使用 shared celery tasks. 因为 django 不会自动
    加载 ``celery.py``, 会自动加载 app package. 从而加载了初始化的 celery app.
    从而, 加载 shared tasks 时, 会给已经加载的这个 app 添加各个 tasks.

  ::

    from .celery import app as celery_app

    __all__.append(celery_app)

- each app's tasks file: ``proj/app_name/tasks.py``

  * 使用 ``shared_task`` decorator 定义所需任务实例. 使用 ``shared_task``
    是为了避免 explicitly depends on global app, 提高 app 的可重用性.

  ::
  
    @shared_task
    def f...

- celery settings. 在 ``proj/proj/settings.py`` 中设置. 根据预设的规则前缀
  进行设置.

  * 对于 timezone, ``TIME_ZONE`` setting will be used if a celery-specific
    ``timezone`` is not defined.

- start worker::

  celery -A proj worker ...

extensions
----------

django-celery-results
^^^^^^^^^^^^^^^^^^^^^
使用 django ORM 保存 celery task results.

看上去并没有什么必要. celery 使用自己的 result backend 存储方式
就挺好, 何必添加 (与 django project 之间) 不必要的耦合.

django-celery-beat
^^^^^^^^^^^^^^^^^^
将 periodic tasks 保存在 database 中. 并可以通过 django admin
进行管理.

这是有价值的, 因为提高了任务配置的灵活性, 不需要在 settings 中
写死.

使用::

  celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

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

- status

- inspect

- control

- events

- beat

- amqp

References
==========
.. [CeleryPip] http://docs.celeryproject.org/en/latest/getting-started/introduction.html#installation
