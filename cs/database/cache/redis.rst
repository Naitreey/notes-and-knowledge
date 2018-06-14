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

data types
==========

- Redis keys.

  * A redis key is a redis string type value.

  * A key can be empty string.

  * Caution: very long keys is bad, because 1) use more memory 2) key
    comparison during lookups becomes expensive.

  * 由于 key 没必要是 identifier, 而是任意字符, 对于复杂的应用场景, 需要规范一个
    key schema, 即划分 key 的结构. 例如 ``ns1:ns2:keyname``

    常见分隔符: ``:`` 用于分隔层级, ``.`` or ``-`` 用于层级内 word separation.

- Redis value. Can be string, list, set, sorted set, hash, bitmap, HyperLogLog.

string
------

- strings can be any binary sequence.

- A string's max size is 512MB.

- empty string is allowed.

- Some use cases for string values:

  * cache html pages.

list
----

- linked list.

- string elements.

- sorted according to the order of insertion.

set
---

- collection of unique, unsorted strings.

sorted set
----------

- Every element is associated with a score.

- A score is a floating number.

- sorted by score. So it has order, and can talk about ranges.

hash
----

- a map of strings to strings.

bit array/bitmap
----------------

HyperLogLog (HLL)
-----------------

- a probabilistic data structure which is used in order to estimate the
  cardinality of a set. 

commands
========
- All redis's commands are atomic. This is simply a consequence of Redis
  using a single-threaded event loop to handle client operations.

string
------

GET
^^^

SET
^^^
::

  SET key value [EX seconds] [PX milliseconds] [NX|XX]

- set value to key. By default any existing value is overriden.

- ``NX``. set only if not exist.

- ``XX``. set only if already exist.

DEL
^^^

INCR
^^^^

- Parse the value of key is number, increment by 1. If key does not exist, set
  it to 0 before incrementing. If the value can not be interpreted as integer,
  abort with error.

- limited by 64bit signed integer.

- 解决 race condition. INCR 解决的问题是多个客户端需要递增一个量时, 各自 GET
  then SET 存在信息不同步的问题, 从而导致 race condition. INCR 由 server 控制,
  这样就把控制权集中了, 在多线程 (多客户端的一般化) 情况下避免了 race
  condition. 这是 atomic operation 的意义.

  类似于 database 中的 auto increment field.

INCRBY
^^^^^^

DECR
^^^^

DECRBY
^^^^^^

GETSET
^^^^^^

- GETSET is atomic.

- 解决 race condition. GETSET 解决的问题是一个客户端现在即要 GET 又要 SET, 如果
  GET then SET, 则两个操作之间的时间差允许其他客户端对该 key 值进行修改. 之后的
  SET 就错误 override 了别的客户端的修改. 所以实现一个 atomic 的 GET & SET 操作,
  消除了这个时间差, 也就消除了引发的 race condition.

- usage examples.

  * 一个客户端需要定时获取 counter 值用于统计并重置该 counter. 其他客户端只进行
    INCR.

MGET
^^^^

- useful to reduce latency and atomically get multiple values.

MSET
^^^^

- useful to reduce latency and atomically set multiple values.

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
