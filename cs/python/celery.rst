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

send task
^^^^^^^^^
- argsrepr

- kwargsrepr

Tasks
=====

task definition
---------------
- A task is a simple callable object wrapped by a task instance.
  Create a task by:

  * ``Celery.task`` decorator

  * ``shared_task`` decorator

  When multiple decorators are applied to a task callable, the task decorator
  must be the outermost wrapper.

design considerations
^^^^^^^^^^^^^^^^^^^^^
- 函数参数注意事项:

  * Don't pass complex objects as task paramters. Only pass JSON/msgpak, etc,
    serializable simple objects.

  * Don't pass database object as parameter. Only pass id, retrieve the object
    from db at the receiving end. The database object you passed might change
    in between the time you place the task and the time it gets executed.

- 等幂性 (idempotence).

  * 理想情况下, 任务的定义应保证等幂性. 即对一个任务多次调用时, 只要维持输入相同,
    任务执行后的结果或者说系统状态就应该是相同的.

  * 但实际中往往不能保证任务的等幂性. 这是一个尽量去满足的要求, 但不强求.

  * 满足等幂性的任务可以配合 ``acks_late`` 来方便地 retry.

- about blocking operations.

  * 如果任务体中需要进行 blocking operation, 例如 IO 操作, 保证这些操作设置了某种
    timeout 机制, 以避免 blocks indefinitely.

  * 另一种避免 task blocks indefinitely 的方式是设置 work 在执行 task 使用的
    soft/hard time limits.

  * 精细的 timeout 与宏观的 time limit 机制应结合使用.

bound task
^^^^^^^^^^
- bind task callable to created task class as a method, rather than static
  method. Therefore, the first paramter must be ``self``. In task body, the
  Task instance is accessible.

- task decorators accepts ``bind`` option to create bound task. It's not a
  option on ``Task`` class, but defined on ``Celery._task_from_fun``.

task inheritance
^^^^^^^^^^^^^^^^
- Create subclass of ``celery.app.task.Task`` to do customizations.

- task decorators accepts ``base`` option to designate base Task class to use.
  It's not a option on ``Task`` class, but defined on ``Celery._task_from_fun``.

task retry
^^^^^^^^^^
- 应用 ``Task.retry()`` 处理 recoverable, expected errors.

- retry 后, 任务进入 RETRY state.

- By default, ``Task.retry()`` will raise an ``Retry`` exception. It isn’t
  handled as an error but rather as a semi-predicate to signify to the worker
  that the task is to be retried. The extra ``raise`` statement is to clearify
  this line is the end of execution, and is not a necessity.

- 若有 exception, can be passed in::

    raise self.retry(exc=exc)

  The original exception 会记录在日志和任务结果中.

- 若 max_retries is configured, task will fail after retries, and current
  exception or original exception will be raised (if there is one).

- task decorators options for convenient retry configuration. 这种 retry
  配置是认为整个 task body 任意位置出现指定错误都可以 retry. 所以精细程度
  低一些.

  * ``autoretry_for``. a list of exception classes, if any of those is raised
    then task is automatically retried.

  * ``retry_kwargs``. a dict of ``Task.retry()`` arguments.

  * ``retry_backoff``. boolean or int. use exponential backoff as countdown.

  * ``retry_backoff_max``. default 600. max backoff interval between retries.

  * ``retry_jitter``. default True. introduce randomness into backoff. The
    actual delay value will be a random number between zero and the expected
    backoff.

- Task.retry vs acks_late.[DocFAQRetry]_

  * acks_late would be used when you need the task to be executed again if the
    worker (for some reason) crashes mid-execution. The worker isn’t known to
    crash, and if it does it’s usually an unrecoverable error that requires
    human intervention.

    此外, 在保证任务等幂性的情况下, 才可以使用 ``acks_late``.

  * When task message is re-queued depends on the message broker being used.
    例如对于 rabbitmq, 当连接中断 (channel closed) 时 message 重新排队. 因此,
    我们说这种延迟 ack 只是为了处理 worker crash 的情况.

  * 注意, 只有当任务导致 worker crash 才会导致 message 不被 ack, 其他情况,
    无论是执行成功、失败、raise exception 等情况 message 都会 ack, 这样
    ``acks_late`` 就起不到作用.

  * 根据上述分析, 我们看到 Task.retry 和 acks_late 解决的实际上是不同的问题.
    Task.retry 解决的是当任务遇到可控的问题时, 可以 gracefully finish 当前
    执行进度并进行重试; acks_late 解决是当任务遇到不可控的问题、并导致突然
    中断时, 可以重新调度.

    两种机制并不矛盾, 完全可以在需要的时候配合使用. 即一个任务, 即在任务体中
    考虑了可能的 retry point, 又设置了 acks_late 保证中断时重新调度.
  
  * 在一般的情况下, Task.retry 相对于 acks_late 是合适的设计. 因为, 只有
    遇到了 uncatchable errors 才需要 acks_late 提供的可靠性 (即在这种情况下还
    可以重新执行任务). 然而, 如果 error 都是 uncatchable 了, 更有可能的原因是
    代码 bug, 而不是重新执行可以解决的.

    因此, 在一般的情况下, 没必要收到任务不 ack. 而是立即 ack, 如果在任务执行中
    出错, 重新排队该任务进行重试.

task options
^^^^^^^^^^^^
- name. must be unique. 默认根据 task module + function name 自动生成.
  生成逻辑由 ``Celery.gen_task_name`` 定义. 子类可自定义.

- typing. whether or not checks task's argument when calling. 若检查, 参数不符
  时在 producer 端就会 raise exception; 否则需要等到 worker 端调用 task callable
  时才能 raise exception. default True.

- max_retries. default 3. set to None will retry indefinitely.

- default_retry_delay. the number of seconds to wait by default when retrying
  task. default: 180s (3min).

- throws. a list of expected error classes that shouldn’t be regarded as an
  actual error.  Errors in this list will be reported as a failure to the
  result backend, but the worker won’t log the event as an error, and no
  traceback will be included. default ().

- rate_limit. limits the number of tasks that can be run in a given time frame.
  This is a per worker instance rate limit, and not a global rate limit. default
  None.

- time_limit. hard time limit in seconds. default to ``task_time_limit``.

- soft_time_limit. default to ``task_soft_time_limit``.

- ignore_result. don't store task state and result. defaults to ``task_ignore_result``.

- store_errors_even_if_ignored. defaults to ``task_store_errors_even_if_ignored``.

- serializer. defaults to ``task_serializer``.

- compression. defaults to ``task_compression``.

- backend. result backend for this task. default to ``app.backend`` defined by
  ``result_backend``.

- acks_late. ack task message after the task has been executed. defaults to
  ``task_acks_late``.

- track_started. track STARTED state. useful for when there are long running
  tasks and there’s a need to report what task is currently running. The host
  name and process id of the worker executing the task will be available in the
  state meta-data. defaults to ``task_track_started``.

task message
------------
- 在 producer 端, Task instance 生成 task message 送入队列, worker processes 读取
  任务消息, 调用指定任务传入指定参数.

message acknowledgement
^^^^^^^^^^^^^^^^^^^^^^^
- A task message is not removed from the queue until that message has been
  acknowledged by a worker.

- By default, worker acknowledges the message in advance, just before it's executed.
  这是保守的做法, 即默认 task is not idempotent. 这样避免消息再次出现在队列中, 被别的
  worker 接收, 如果任务不能保证 idempotent, 这样就会出问题.

- 对于 ``Task.acks_late`` 的任务, message is ack-ed after task is returned.

- By default, the worker will acknowledge the message if the child process
  executing the task is terminated (either by the task calling sys.exit(), or
  by signal) even when ``acks_late`` is enabled.
  
  这是因为如果一个任务导致 worker's child process get terminated,
  这更可能是某种人为行为或者十分异常的 malfunction (因为 python 级别的
  exception 全部被 catch 掉了, 避免 child 退出). 如果要避免这种 ack, 设置
  ``Task.reject_on_worker_lost``.

task states
-----------
- 

- states transition: PENDING -> STARTED -> [RETRY -> STARTED]... -> SUCCESS|FAILURE

- STARTED state is available only if ``task_track_started`` is enabled
  or in a per-task setting.

- PENDING state is not a recorded state, but rather the default state for any
  task id that’s unknown.

meta informations
-----------------

- ``request`` property. Information and state related to the currently
  executing task.

task class
----------
- celery 读取应用中定义的 task callable, 对于每个 task callable, 定义一个
  ``celery.app.task.Task`` subclass, 包裹 task callable, 并实例化后返回, 替换
  原来的 task callable.

methods
-------

delay
^^^^^
- Returns a ``AsyncResult``.

apply_async
^^^^^^^^^^^
- options.

  * argsrepr. Hide sensitive information in arguments.

  * kwargsrepr. Hide sensitive information in arguments.

retry
^^^^^

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

Logging
=======
- 默认配置 ``worker_hijack_root_logger=True``, 此时 root, celery, celery.task,
  celery.redirected loggers 全部被 celery 重新配置 (其他 logger 维持原样).
  例如, django 的 ``LOGGINGS`` 配置中相关的 logger 会被重新配置.

- 因此, 设置必要的 celery logging settings, 并使用 ``celery.utils.log`` 获取
  loggers, 能最佳地与 celery logging 封装协作.

- By default, stdout/stderr streams will be redirected to ``celery.redirected``
  logger, with WARNING level.

task logging
------------

- use ``get_task_logger`` to retrieve ``ceelry.task`` logger children.
  享受 ``worker_task_log_format`` 自动提供的额外信息.::

    from celery.utils.log impor get_task_logger

    logger = get_task_logger(__name__)

settings
--------
- ``worker_hijack_root_logger``. default True. To configure logging manually,
  set this to False.

- ``worker_log_color``. by default use color if logging to terminal.

- ``worker_log_format``. format used by all loggers except for celery.task.
  default::

    [%(asctime)s: %(levelname)s/%(processName)s] %(message)s

- ``worker_task_log_format``. format for celery.task. 默认就多了 ``task_name``
  和 ``task_id`` 的自动输出. default::

    %(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s

- ``worker_redirect_stdouts``. default True. redirect stdout/stderr streams
  to logger.

- ``worker_redirect_stdouts_level``. default WARNING. stdout/stderr output's
  level.

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

    注意, 符合 AMQP 协议需要至少提供 ``exchange`` and ``routing_key``. 否则
    可能产生非预期路由结果.

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

schedule
^^^^^^^^

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

models
""""""
- IntervalSchedule. define interval schedules.

- CrontabSchedule. define crontab schedules.

- SolarSchedule. define solar schedules.

- PeriodicTask. define periodic tasks.

  * name 是 unique key. 从而可唯一确定一个任务.
  
  * 与某个 schedule entry 关联.

  * 可设置任务参数.

  * 可设置各种 apply 参数, 例如 queue, exchange, routing_key.

- PeriodicTasks. keep track of when the schedule is last updated.

  * ``update_changed()``. classmethod. 更新上次更新时间.

signals
""""""""
增加、修改、删除 ``PeriodicTask`` 和 ``*Schedule`` 时会自动更新上次
更新时间. 从而应用新配置.

由于 bulk create/update/delete 操作时不会触发 signal, 此时需要手动
更新时间.

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
.. [DocFAQRetry] http://docs.celeryproject.org/en/latest/faq.html#should-i-use-retry-or-acks-late
