celery
======

Overview
--------
- Definition: Celery is a distributed task queue system.

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

Calling
-------

Result backend
--------------

- 如果任务发送端不需要知道任务状态和任务结果等信息, 则没必要配置 result backend.
  此时, 发送端就只能发送任务, 获取不到结果.

RPC
~~~

- It sends state back as transient messages.

Configuration
-------------

- The configuration can be set on the app instance directly or by using a
  dedicated configuration module.
