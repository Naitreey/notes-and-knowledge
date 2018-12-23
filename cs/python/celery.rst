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

constructor options
-------------------

- broker

- backend

- include.

app config
----------
- ``conf``

- ``config_from_object(<module>)``. 

task registry
-------------
- tasks. The Celery app's task registry.

task creation
-------------
- ``task(*args, **opts)``. This method returns a decorator or a task instance.
  
  当 decorator 应用到 task callable 之后, 创建一个 ``task_cls`` 的子类. 原
  callable object 成为 ``Task.run()`` method or staticmethod (根据 ``bind``
  option 的值). 创建并注册该子类的一个实例, 然后返回, 替换原来的 task callable.

  A task is not instantiated for every message, but is registered in the task
  registry as a global instance.

  ``args`` 一般不存在, 即一般情况下该方法只需指定一系列 task creation options
  即可. 若指定 positionals, 可以将 task callable 作为第一 positional 参数. 此时
  该方法直接返回 task instance. 即::

    @app.task(**opts)
    def func():
      pass
    # equals to
    app.task(**opts)(func)

  options can be:

  * Any Task class attribute.

  * task retry options.

  * base.

  * bind.

  * ...

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
- Task's granularity. 即一个大任务应该如何切分成多个小任务, 即构建一个工作流.

  In general it is better to split the problem up into many small tasks rather
  than have a few long running tasks.

  With smaller tasks you can process more tasks in parallel and the tasks won’t
  run long enough to block the worker from processing other waiting tasks.

  但是过于精细的划分可能会适得其反, 因为每个任务执行的 overhead 带来的影响
  变得显著了.

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

- 任务结果. 如果不需要任务结果, 就别记录. 设置 ``ignore_result``.

- 避免在任务体中再执行同步任务, 使用 canvas 设计更高效、解耦合的异步工作流.
  在任务体中执行同步任务不仅低效 (对 worker 资源不能很好利用), 而且当 worker
  pool exhausted 时会导致 dead lock. 

- 尽量提高 worker 获取执行任务所需数据的效率. 例如, 缓存经常用到的数据至
  cache system.

- Asserting the world is the responsibility of the task, not the caller.

- database transaction 与任务分发. 任务必须在 database transaction 成功
  后才分发. 否则任务中如果需要用到 transaction 中修改的数据, 可能导致
  race condition.

bound task
^^^^^^^^^^
- bind task callable to created task class as a method, rather than static
  method. Therefore, the first paramter must be ``self``. In task body, the
  Task instance is accessible.

- task decorators accepts ``bind`` option to create bound task. It's not a
  option on ``Task`` class, but defined on ``Celery._task_from_fun``.

task inheritance
^^^^^^^^^^^^^^^^
- Create subclass of ``celery.app.task.Task`` (or other appropriate subclasses)
  to do customizations. 在创建 task 时, 使用 ``base`` option to designate base
  Task class to use.  It's not an option on ``Task`` class, but defined on
  ``Celery._task_from_fun``.

- Task inheritance 可用于抽象多个 task 中需要使用的相似的逻辑. 从而达到避免重复
  的意义.

- 注意由于每个 task 只保存一个 global instance 至 Celery app instance. 因此, 任
  务上不能维持状态信息.

retry task
^^^^^^^^^^
- 应用 ``Task.retry()`` 处理 recoverable, expected errors.

- When you call retry it’ll send a new message, using the same task-id, and it’
  ll take care to make sure the message is delivered to the same queue as the
  originating task.

- retry 后, 任务进入 RETRY state.

- By default, ``Task.retry()`` will raise an ``Retry`` exception. It isn’t
  handled as an error but rather as a semi-predicate to signify to the worker
  that the task is to be retried. The extra ``raise`` statement is to clearify
  this line is the end of execution, and is not a necessity.

- 若有 exception, can be passed in::

    raise self.retry(exc=exc)

  ``exc`` 的信息和 traceback 会记录在日志和任务状态中.

- 若 ``max_retries`` is configured, task will fail after retries, and current
  exception or original exception will be raised (if there is one and it's
  passed in ``self.retry()``).

- task decorators options for convenient retry configuration. 这种 retry
  配置是认为整个 task body 任意位置出现指定错误都可以 retry. 所以精细程度
  低一些.

  * ``autoretry_for``. a list of exception classes, if any of those is raised
    then task is automatically retried.

  * ``retry_kwargs``. a dict of ``Task.retry()`` arguments provided for
    autoretry.

  * ``retry_backoff``. boolean or int. If False, use fixed delay when retrying
    (``default_retry_delay``). If True, use exponential backoff as countdown.
    开启时, 默认的 retry backoff factor 是 1 (retry wait: 1*2**N).  若设置 int
    值, 则成为 factor, 即 (try wait: f*2**N).

  * ``retry_backoff_max``. default 600. max exponential backoff interval
    between retries, a cap value of exponential backoff wait interval.

  * ``retry_jitter``. default True. introduce randomness into exponential
    backoff. The actual delay value will be a random number between zero and
    the expected backoff.

- Task.retry vs acks_late.[DocFAQRetry]_

  Task.retry 和 acks_late 解决的实际上是不同的问题.
 
  * Task.retry 解决的是当任务遇到可控的问题时, 可以 gracefully finish 当前执行
    进度并再次排队该任务进行重试.
  
  * acks_late 解决当 worker 遇到不可控的问题, 导致突然中断时, 可以重新调度. 例
    如, worker (而不是 child) process is terminated, 所在机器断电、重启等.

  两种机制并不矛盾, 完全可以在需要的时候配合使用. 即一个任务, 即在任务体中
  考虑了可能的 retry point, 又设置了 acks_late 保证中断时重新调度.
  
revoke task
^^^^^^^^^^^
revoke task 是不需要 task body 实现进行配合的 task abortion. 它的原理是
producer 发起 revoke, 广播 revoke event, 让所有 worker 知道这个任务要
revoke.

worker 会把要 revoke 的任务记在一个 set 中. 当 worker 收到相符的任务消息,
会发送 task-revoked event, 记录该任务的状态 REVOKED 以及相关信息至 backend,
ack 任务消息.

注意几点:

- 如果 worker 在收到 revoke 广播之前已经执行完了该任务, 就不会再收到这个
  任务 id. 从而 revoke 已经执行的任务没有效果, 不会修改任务状态.

- 如果任务正在执行, 一般情况下已经无法 revoke. 除非强制 ``terminate=True``,
  此时 the worker child process processing the task will be terminated.
  该操作只应该作为 last resort 使用. 用于手动清除卡住的任务, 释放 worker.
  若 used programmatically, 必须十分谨慎. 因为这里存在 race condition.
  如果发送 signal 时任务已经执行完, worker 开始执行下一个任务, 就会错误地
  杀掉其他任务.

- worker 将 to-be-revoked 和 revoked tasks 放在自身内存中. 默认不是持久的.
  若 worker restart, 这些记录会消失. 该 revoke 的任务就不会被 revoke 了.
  需要使用 ``--statedb`` option 保持 revoked task 至持久性存储.

revoke and abort.

- revoke 不适合去可靠地常规性地 revoke 正在执行的任务. 它只适合 revoke
  尚未执行的任务.

- revoke 到底有什么用呢? 它只能 revoke 尚未执行的任务. 可能就是用在大量
  任务堆积时, 清除某些特定的任务、或者批量 revoke 吧.

- abort 相对而言, 更合适实现 graceful abort 正在执行的任务. 它需要 task
  body 去配合. 如果无论是处于什么情况下的任务, 都希望能够可靠地清除, 应该
  使用 abortable task.

abort task
^^^^^^^^^^
- ``celery.contrib.abortable`` 提供了 AbortableTask 和 AbortableAsyncResult.

- 原理是, producer 调用 ``AbortableAsyncResult.abort()`` 在 result backend
  中置 ABORTED 状态. task body 中, 设置多处 ``AbortableTask.is_aborted()``
  检查. 若发现 aborted, 相应处理和退出.

- abortable task 需要保存任务状态, 且能够反复获取, 因此需要使用基于 database or
  cache 的 result backend. 而不能是 RPC backend.

- 对于 producer 而言, 它唯一能做的就是 signal task body the task has been
  aborted. 到底怎么处理完全由 task 执行逻辑来控制, 并且也只能由 task 执行逻辑
  来可靠地控制. producer 做不了其他的任何事. Producer 尝试做任何其他努力, 例如
  terminate worker process, 都可能造成 race condition.

reject task
^^^^^^^^^^^
reject task 是需要配合 AMQP 的 basic.reject method 来使用的, 即是对这个方法
的封装. 相应地, reject task 有两种用途:

- reject task message and requeue. worker reserved task message, 但随后
  rejected the message. 消息重回队列. 继续可以被任何 worker 接收执行.::

    raise Reject(requeue=True)

  这种用法并不推荐. 因为可能造成无限循环. 不如使用 Task.retry + max_retries.

- reject task message and send to Dead Letter Exchange (DLE). 用于进行特殊
  处理.::

    raise Reject(requeue=False)

注意无论哪种用法, 在 task body 中进行 reject 的前提是任务消息没有被预先 ack.
因此, 必须配合 ``acks_late`` 使用才有效果.

Rejected task 在没有后续 worker 处理之前, 状态停留在 PENDING (or STARTED if
recorded). 

ignore task
^^^^^^^^^^^
ignore task 的效果是该任务没有任何自动的状态记录 (或只有 STARTED 记录, if
recorded). 注意到任务消息在 raise Ignore 之前就 ack 了.::

    raise Ignore()

这可用于手动状态记录, 或就是 ignore.

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

新状态的 metadata 会覆盖旧状态的 metadata.

标准状态
^^^^^^^^
- PENDING. Task is waiting for execution or unknown. Not a recorded state, but
  rather the default state for any task id that’s unknown. Unknown 指的是
  result backend 还没有关于该任务的任何记录. 所以说, 任务状态不会查询消息队列,
  无论是还在排队还是根本没这个任务, 对于 celery 而言都一样, 就是未知的.

- STARTED. Task execution is started for real. Available only if
  ``task_track_started`` is enabled or in per-task ``Task.track_started``.

  Meta data: ``pid`` and ``hostname`` of worker process.

- RETRY: task is being retried.

  Meta data: ``result`` is the exception that caused the retry,
  ``traceback`` is exception's traceback.

- SUCCESS. task execution has finished and is successful.

  Meta data: ``result`` is task's return value.

- FAILURE: task execution has finished and is unsuccessful.

  Meta data: ``result`` is raised exception instance, ``traceback``
  is exception's traceback.

- REVOKED. Task has been revoked.

其他状态
^^^^^^^^
这些状态一般不会出现, 但可以手动设置.

- RECEIVED. task is received by a worker, 但可能还没有执行. This state is
  not normally available. Only used in events.

- REJECTED.

- IGNORED.

States transition
^^^^^^^^^^^^^^^^^
::

  PENDING -> [STARTED] -> [RETRY -> [STARTED]]... -> SUCCESS|FAILURE
                                                  -> REVOKED

classification
^^^^^^^^^^^^^^
- ready states, meaning the task is finished, its result is ready.
  无论成败. 当任务进入 ready states, AsyncResult 会 cache task data
  on the instance.

  * SUCCESS

  * FAILURE

  * REVOKED

- unready states.

  * PENDING

  * RECEIVED

  * STARTED

  * RETRY

- propagate states. The exception can be propagated to caller-side
  if task is in these states.

  * FAILURE

  * REVOKED

custom state
^^^^^^^^^^^^
- simply define a unique state name and associate with this state whatever
  metadata you want. Then call ``Task.update_state()``.

task class
----------

class attributes
^^^^^^^^^^^^^^^^
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

- ignore_result. don't store task state and result. defaults to
  ``task_ignore_result``. 如果任务结果确实没用, 应该设置这个选项.

- store_errors_even_if_ignored. defaults to ``task_store_errors_even_if_ignored``.

- serializer. defaults to ``task_serializer``.

- compression. defaults to ``task_compression``.

- backend. result backend for this task. default to ``app.backend`` defined by
  ``result_backend``.

- acks_late. ack task message after the task has been executed. defaults to
  ``task_acks_late``. See also `retry task`_ and `message acknowledgement`_.

  * acks_late would be used when you need the task to be executed again if the
    worker (注意是 worker 而不是 worker's child process) crashes mid-execution.

    ack task message 是 worker 的任务而不是 child process 的任务. 这里导致
    worker crash 的原因例如: worker has bug, worker get killed by SIGKILL,
    twice ctrl-c on terminal (quick shutdown), 服务器关机、重启、断电等.
    
  * 注意 acks_late 不管 child process crash 的情况. 那是由 reject_on_worker_lost
    控制的. 当 ``acks_late=True, reject_on_worker_lost=False`` 时, 如果 worker's
    child crash (导致 worker 中出现 WorkerLostError), 仍然会 ack.

    做这些区分, 是因为 celery 中任务由 worker's childs 执行, worker 本身是
    控制. 如果 worker crash, 是外部原因, 不怪任务, 所以 acks_late 就可以让
    任务重新执行; 如果 worker's child crash, 则更可能是 task 本身导致了
    unrecoverable error (python 层的错误都会被 catch), 或者 admin 明确 kill
    掉执行进程, 总之, 应该是 task 本身存在 bug 或者其他问题, 所以这样的任务
    更保险的处理是不重新执行, 故进行 ack, 而 reject_on_worker_lost 会允许
    这样的任务也再次执行.

  * 在保证任务等幂性的情况下, 才可以使用 ``acks_late``.

  * When task message is re-queued depends on the message broker being used.
    例如对于 rabbitmq, 当连接中断 (channel closed) 时 message 重新排队. 因此,
    我们说这种延迟 ack 只是为了处理 worker crash 的情况.

  * 注意, 只有当任务导致 worker crash 才会导致 message 不被 ack, 其他情况,
    无论是执行成功、失败、raise exception 等情况 message 都会 ack, 这样
    ``acks_late`` 就起不到作用.

- reject_on_worker_lost. 默认 False. 如果一个任务 acks_late, 并且 worker's
  child process is lost during task execution, 决定是要 reject task message
  还是 ack task message. 如果开启, 则 reject task message 并 requeue. 从而
  再次执行. 注意如果一个 task message 已经 redelivered 过了, 则会 reject 而
  不再 requeue. 这样不会再次执行.

- track_started. track STARTED state. useful for when there are long running
  tasks and there’s a need to report what task is currently running. The host
  name and process id of the worker executing the task will be available in the
  state meta-data. defaults to ``task_track_started``.

attributes
^^^^^^^^^^
- ``request`` property. Metadata and state related to the currently executing
  task.

methods
^^^^^^^

- ``delay()``. Returns a ``AsyncResult``.

- ``apply_async(args=None, kwargs=None, task_id=None, producer=None, link=None,
  link_error=None, shadow=None, **options)``.

  * link. A single or a list of signatures to apply as a callback after
    success execution. The return value of this task execution is applied
    to the signature as additional args.

    The task result keeps track of all subtasks called by the original task.

    The callbacks are run in parallel tasks, all of which are passed task
    return value.

  * link_error. A single or a list of signatures to apply as callback after
    execution failure. The callbacks are passed 3 positionals: raw request,
    exception raised, related traceback. The callbacks are called synchronously
    and sequentially, rather than asynchronously, so that the raw request,
    exception and traceback objects can be passed to it.

  * argsrepr. Hide sensitive information in arguments.

  * kwargsrepr. Hide sensitive information in arguments.

- ``retry()``

- ``after_return()``. handler to call after task returns. 无论成功还是失败.
  对于需要忽略的 return reason: IGNORED, REJECTED, RETRY 不会执行.

- ``on_failure()``. handler to run when the task fails.

- ``on_retry()``. handler to run when task is to be retried.

- ``on_success()``. handler to run when task succeeded.

- ``signature(args=None, *starargs, **starkwargs)``. 参数顺序要符合 Signature
  constructor 顺序. kwargs 可用于指定 options.

- ``s(*args, **kwargs)``.::

    .s(*a, **k) -> .signature(a, k)

  所以只能指定 task args and kwargs that need to be partially applied.

  看上去与普通的 partially applied function 不同, 即相当于 partially apply 时,
  传入的参数是靠右侧填充的. 例如::

    @app.task
    def f(a,b,c):
        pass

    f.s(1,2) # b == 1, c == 2
    f.s(1,2).delay(3) # a == 3

- ``si(*args, **kwargs)``. shortcut::

    .si(*a, **k) -> .signature(a, k, immutable=True)

Results
=======

AsyncResult
-----------
attributes
^^^^^^^^^^

- traceback.

- backend.

- state.

- parent. the parent result (the result of parent task).

- graph. dependency graph.

methods
^^^^^^^

- ``ready()``

- ``get()``.

  * If the task raised an exception, it is re-raised inside of the get call.

  * ``wait()`` is a deprecated alias of ``get()``.

- ``failed()``

- ``successful()``

Result backend
==============
- Result backend is required to keep track of tasks' states.
  默认不启用 result backend, 即默认配置下, 不可获取任务的状态和结果.

  如果任务发送端不需要知道任务状态和任务结果等信息, 则没必要配置 result backend.
  此时, 发送端就只能发送任务, 获取不到结果. 或者配置简单的 RPC backend.

- Result backends aren’t used for monitoring tasks and workers, for that Celery
  uses dedicated event messages.

content
-------
- result backend 保存着任务的各种信息, 这些信息是 ``AsyncResult`` 中信息的来源.
  包含:

  * task id ``task_id``.

  * 当前状态 ``status``.

  * 结果 ``result``.

  * ``traceback`` if any.

  * children tasks ``children`` if any.

RPC and AMQP result backends
----------------------------
- When rabbitmq or QPid is used as message broker, RPC and AMQP result backend
  ``rpc://`` and ``amqp://`` are available automatically.

- RPC/AMQP 的命名, 就体现了这种 result backend 本质上是 RPC 操作. 因此, they
  send task state information back as transient messages, rather than actually
  storing result somewhere. 这些任务状态信息可以理解为 RPC 的返回值. Therefore
  result can only be retrieved once, and only by the client that initiated the
  task.

- It's still an excellent choice if you need to receive state changes in
  real-time. Using messaging means the client doesn’t have to poll for new
  states.

- RPC 与 AMQP result backend 的区别.
 
  * RPC 对于每个 client 开一个队列 (In AMQP jargon, a ``reply_to`` queue that
    is ``exclusive`` to this client). 不同的任务结果通过 task id 作为 AMQP 中的
    ``correlation_id`` 来识别.
    
  * AMQP 对于每个任务单独开一个队列. 因此非常低效, deprecated.

database result backends
------------------------
- Polling the database for new states is expensive. 避免过于频繁的状态 polling.

- MySQL transaction isolation level should be READ-COMMITTED. 不然如果在一个
  transaction 中 polling for state change, 会看不到这期间其他数据库线程 commit
  的状态改变.

Canvas
======
- Canvas 的用处和价值.

  * 如果我们每次请求执行任务时, 只需要异步执行一个单独的任务, 那么
    ``Task.delay()`` 即可满足需求. 但很多时候并没有这么简单. 可能需要异步执行多
    个任务, 且任务之间存在依赖关系和执行顺序问题. 也就是说, 我们请求执行的是一
    个多步骤的任务流.
    
    最简单的解决办法是在上一步任务中同步或异步地调用下一步任务. 这样显然是有很
    多缺陷的. 首先, 强制给任务之间写入关联, 造成了任务之间的强耦合, 各个任务不
    再能够独立执行. 其次, 这种方式有很大的局限性, 对于复杂的关系流, 比如涉及分
    支和汇聚过程, 变得难以维护. 显然, 任务之间应该是无显性关联的, 任务之间要保
    持逻辑独立.

  * Canvas 的意义, 就在于提供一种机制能够将多个独立任务组织起来, 成为一个复杂的
    异步任务流. 一次构建, 一次分发, 分发后任务的依赖关系和执行顺序内部自动解决.

Signature
---------
- A Signature wraps the arguments and execution options of a single task
  invocation. A signature 类似于 partially applied function.

- A Signature 本质上只是一个 prettified dict storage (Signature is a dict
  subclass). 它的核心是一系列 key-value pairs, 记录着 signature 的相关信息.
  外加一系列用于执行任务的 methods.

- A Signature supports the Task APIs, such as being asynchronously dispatched,
  invoked directly, etc.

- Signature instantiation & signature call 时, 参数的应用规则见
  ``Signature.apply_async()``.

- Data preserved in a signature.

  * task: task name.

  * args: partially applied positionals.

  * kwargs: partially applied kwargs.

  * options: partially applied task calling options.

  * subtask_type: primitive type (which is a subtask type).

  * immutable: whether the signature is immutable.

  * chord_size: ...

- Creating a signature:

  * celery.canvas.signature function.

  * celery.canvas.Signature class.

  * celery.app.task.Task.signature method.

  * celery.app.task.Task.s method.

- immutable signature.

  * An immutable signature doesn't take additional args, kwargs, when
    being applied, called, cloned, etc.

  * When an immutable signature doesn't have sufficient args, kwargs,
    it's not callable.

  * Only execution options can be set on immutable signature.

  * This is useful when there's need to prevent modification of calling
    signature. For example, in complex canvas workflow, to prevent a task in
    next stage from taking the result from previous stage.

utility functions
^^^^^^^^^^^^^^^^^
- ``signature(varies, *args, **kwargs)``. create a signature.
  varies can be:

  * A task name string, task instance. passed to Signature constructor.

  * A Signature, then it's cloned. args, and kwargs if provided is ignored.

  * A general dict instance. Then it's passed to ``Signature.from_dict`` to
    create a Signature instance. dict should contain the necessary keys to
    form a valid signature.

constructor
^^^^^^^^^^^
- task. Can be:

  * a dict instance. Then signature is simply initialized with this dict's
    content as its data.
 
  * task instance, task name. A signature is initialized with this task and
    all other arguments as its data.

- args. see above.

- kwargs. see above.

- options. see above.

- subtask_type. see above.

- immutable. see above.

- app. the app to which the signature's attached. None for global app.

- ``**ex``. other options as kwargs to be merged into options.

attributes
^^^^^^^^^^
- app. signature attaching to the app.

- ``_app``. explicitly set app.

- type. signature attaching to the task.

- ``_type``. explicitly set task instance.

- name. task name.

- id. task id.

- parent_id. parent task id.

- root_id. root task id.

- all standard keys stored in Signature dict.

methods
^^^^^^^
- ``apply(args=None, kwargs=None, **options)``. sync version of
  ``.apply_async()``

- ``__call__(*args, **kwargs)``. sync version of ``.delay()``

- ``apply_async(args=None, kwargs=None, route_name=None, **options)``

  * args: args are prepended to signature instantiation 时传入的 positionals.

  * kwargs: kwargs overrides those passed in Signature instantiation.

  * options: options overrides those passed in Signature instantiation.

- ``delay(*args, **kwargs)``. a shortcut for ``apply_async(args, kwargs)``, 不
  能传 options.

- ``set(immutable=None, **options)``. Set task execution options. returns
  self, so can be chained.

- ``clone(args=None, kwargs=None, **opts)``. Clone a signature, adding
  additional args, kwargs and options. 这可用于创建衍生的 signature.

- ``link(callback)``. link a callback task's signature. Returns the callback.
  Call this method multiple times to link a list of callbacks. Works like
  ``Task.apply_async(link=)``.

- ``link_error(callback)``. ditto for error.

- ``on_error(callback)``. ditto that returns self, for chaining methods.

Primitives
----------
- Primitives are special Signature subclasses that serves as job workflow
  orchestration toolset.

- Primitives wraps 一系列的 Signatures, 生成一个新的 Signature, 作为一个 workflow.
  如果其中包含 partial signatures, 在 dispatch workflow Signature 时, 可以一起填充
  缺失的参数.

group
^^^^^
- A group calls an iterable of tasks in parallel.

constructor
"""""""""""
- ``*tasks``. can be:
 
  * positional task signatures to be grouped.

  * 只有一个元素, 此时 positional 还可以是一个 an iterable of task signatures to
    be grouped, or another group.

- ``**options``. kwargs execution options.

methods
""""""""
- ``apply_async(args=None, kwargs=None, add_to_parent=True, producer=None, **options)``.
  args, kwargs, options 允许同时给 group 中的所有任务 signature 应用相同的参数. Returns
  a GroupResult.

chain
^^^^^
- A chain links tasks together to be executed sequentially, where the output of
  the previous task's signature is feed as input of the next task's signature.

- A bitwise OR-ed sequence of Signatures is chained automatically.::

    task.s() | task.s() | task.s()

constructor
"""""""""""
- ``*tasks``. positional task signatures to be chained.

- ``**options``. kwargs execution options.

methods
"""""""
- ``__call__(*args, **kwargs)``. equivalent to ``apply_async(args, kwargs)``.
  注意 chain 没有 explicit sync execution 的方法.

- ``apply_async(args=None, kwargs=None, **options)``. args and kwargs are
  applied to the first task signature in the chain. Returns the AsyncResult
  of the last task in chain.

chord
^^^^^
- A chord is a group (called header) with callback task (called body). In other
  words, the iterable of tasks are executed in parallel, of which the results
  are feed into the callback task.

- chord 是 "弦". (大致可以理解为弦是多个半径的终结?)

- A group chained to another task will be automatically converted to a chord.::

    group | task -> chord

constructor
"""""""""""
- header. an iterable of tasks that forms a group.

- body. a signature as callback.

- args. partial args as in signature.

- kwargs. ditto for kwargs.

- options. as in signature.

methods
"""""""
- ``apply_async(args=None, kwargs=None, task_id=None, producer=None,
  publisher=None, connection=None, router=None, result_cls=None, **options)``
  args, kwargs, options are merged with those during initialization, and
  they are applied to the header group.

xmap
^^^^
- Works like python built-in map function. Apply the task to an iterable of
  arguments, sequentially.

- 本质上是异步调用 ``celery.map`` task, 传入要指定的 task 和 iterable 参数.

xstarmap
^^^^^^^^
- works like itertools.starmap function. Apply the task to an iterable of
  argument iterables. Each application is executed sequentially.

- 本质上是异步调用 ``celery.starmap`` task.

chunks
^^^^^^
- When applying the task to an iterable of argument iterables (which are an
  iterable of works), split the work into chunks. Works in each chunk are
  executed sequentially; while chunks are executed in parallel.


Graphs
======

DependencyGraph
---------------

methods
^^^^^^^
- ``to_dot()``

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

  * 考虑 worker 的类型: prefork, eventlet, gevent. 接受不同类型的任务.

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
- All times and dates, internally and in messages uses the UTC timezone
  (``enable_utc=True``).

- UTC time from/to local time conversion is based on ``timezone`` setting.
  (For django, ``TIME_ZONE`` setting is *supposed* to be respected. 但是
  并不管用, 可能是 bug?)

settings
--------
- ``enable_utc``. If enabled dates and times in messages will be converted to
  use the UTC timezone.

- ``timezone``. default UTC if ``enable_utc=True`` otherwise local timezone.

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
    
  * 实例化 celery app

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

而且, 用关系型数据库保存 celery result 多慢啊.

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

timezone
""""""""
- 默认情况下, periodic tasks 在数据库中保存的 ``last_run_at`` 时间是 UTC 时间或
  aware datetime. 修改 django ``TIME_ZONE`` 不影响程序对时间的判断, 并不需要手
  动重置任务执行时间. 这与文档描述不同.

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

design patterns
===============

- 可靠的 long-running task 的中断.

  * 首先, 使用 abortable task. 通过 ABORTED 状态标识需要中断.
   
  * 在任务体中多处进行判断. 最好能够在执行 IO 等长时间操作的
    同时 polling task state (要求异步). 如果需要执行 blocking
    操作, 最好能设置 timeout.

  * 发起任务中断时, 检查任务状态是否 ready (READY_STATES), 
    若已经完成则没必要中断了. 否则发起 abort, 即设置 ABORTED
    状态.
    
  * 以上能解决几乎所有问题. 保证无论当前任务是还在排队还是已经
    开始, 只要任务逻辑正确, 就能保证任务按要求在未来某个时间中断.
    
  * 注意没必要记录 STARTED 状态, 即没必要区分任务是否开始来分别
    处理. 例如, 若记录了 STARTED, 则 PENDING 表示只在排队尚未开始.
    可能想到此时 revoke 即可. 但是这可能存在 race condition.
    即当前以为是还在排队中, 所以 revoke. 但同时可能任务已经开始,
    从而 revoke 失败.

  * 注意, 如果中断的同时需要删除数据库记录, 根据不同需求, 可能在
    中断发起处删除也可能在原任务体中的中断逻辑里面设置删除数据库
    记录. 对于后者, 需要考虑如果 worker 在执行过程中重启或退出,
    会导致数据库记录残留. 这时需要设置 ``acks_late`` 保证任务重新
    执行, 从而再次执行中断清理, 从而还要保证任务等幂性.

References
==========
.. [CeleryPip] http://docs.celeryproject.org/en/latest/getting-started/introduction.html#installation
.. [DocFAQRetry] http://docs.celeryproject.org/en/latest/faq.html#should-i-use-retry-or-acks-late
