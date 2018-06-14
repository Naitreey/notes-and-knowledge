overview
========

- redis: REmote DIctionary Server

- in-memory key-value store.

  * A key-value store maps keys to values.

- usage: cache, in-memory database, message broker (message queue).

features
--------
- in-memory.

- key-value store.

- distributed.

- support for various data structures as values of keys.

  * string.

  * list of strings.

  * set of strings.

  * ordered set of strings.

  * hash tables.

  * HyperLogLogs.

  * bitmaps.

  * Geospatial data with radius queries.

  * JSON (via module ReJSON)

- transaction.

- pub/sub.

- key with TTL.

- optional persistence (append-only file).

- replication (master-slave).

- clustering.

- HA (redis sentinel).

- Lua scripting.

- LRU eviction.

versioning
----------
- ``major.minor.patchlevel``. An even minor marks a stable release, odd minors
  are used for unstable releases.

comparison: redis vs memcached
------------------------------

- Summary: Redis is more powerful, more popular, and better supported than
  memcached. Memcached can only do a small fraction of the things Redis can
  do. Redis is better even where their features overlap.

- See also [SOMemcachedRedis]_.

commands
========

GET
---

SET
---

DEL
---

INCR
----
- INCR 相比于 GET then SET 的意义在于它是一个操作, 由 server 控制结果.
  这样就把控制权集中了, 在多线程 (多客户端的一般化) 情况下避免了 race
  condition. 这是 atomic operation 的意义.

  类似于 database 中的 auto increment field.

INCRBY
------

SETNX
-----

EXPIRE
------

TTL
---

- SET a key will remove its ttl.

- returns: -1 (never expire), -2 (not exist).

RPUSH
-----

LPUSH
-----

LLEN
----

LRANGE
------

LPOP
----

RPOP
----

SADD
----

SREM
----

SISMEMBER
---------

SMEMBERS
--------

SUNION
------

- combine multiple sets into one and returns it

ZADD
----

ZRANGE
------

HSET
----

HMSET
-----

HGET
----

HGETALL
-------

HINCRBY
-------

persistence
===========

- AOF: append-only file.

replication
===========

- Replication is useful for read (but not write) scalability or data
  redundancy.

clustering
==========

references
==========
.. [SOMemcachedRedis] https://stackoverflow.com/questions/10558465/memcached-vs-redis
