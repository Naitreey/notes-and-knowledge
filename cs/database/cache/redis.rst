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

redis keys
==========
* A redis key is a redis string type value.

* A key can be empty string.

* Caution: very long keys is bad, because 1) use more memory 2) key
  comparison during lookups becomes expensive.

* 由于 key 没必要是 identifier, 而是任意字符, 对于复杂的应用场景, 需要规范一个
  key schema, 即划分 key 的结构. 例如 ``ns1:ns2:keyname``

  常见分隔符: ``:`` 用于分隔层级, ``.`` or ``-`` 用于层级内 word separation.

* creation and removal of keys.

  - When we add an element to an aggregate data type, if the target key does
    not exist, an empty aggregate data type is created before adding the
    element.

  - When we remove elements from an aggregate data type, if the value remains
    empty, the key is automatically destroyed.

  - Calling a read-only command, or a write command removing elements with an
    nonexistent key, 相当于应用该命令在一个类型相符的 empty aggregate value
    上面.

data types
==========

string
------

- strings can be any binary sequence.

- A string's max size is 512MB.

- empty string is allowed.

- Some use cases for string values:

  * cache html pages.

bitmap/bit array
----------------

- Bitmaps are not an actual data type, but a set of bit-oriented operations
  defined on the String type. 因此可以分别使用 GET/SET 去 serialize/deserialize
  bitmap.

- For max size 512MB string, corresponds to 2**32 bit array.

- During a write operation, bitmap is automatically enlarged if the addressed
  bit is outside the current string length.

- During a read operation, out of range bits are considered zero.

- usage:

  * One of the biggest advantages of bitmaps is that they often provide extreme
    space savings when storing information. 

- 注意到, bitmap 的 offset, 从二进制位的角度看, 是从一个 byte 的高位侧开始数的.
  因此, 作为 string 输出时 (GET), 需要理解它的转换方式.

- example usage:

  * Real time analytics of all kinds.

  * space efficient but high performance boolean information associated with
    object IDs. 前提要求是 object id 是依次递增的. 否则在小数据量时会造成
    不必要的内存浪费.


list
----

- linked list.
  
- string elements.

- sorted according to the order of insertion.

- 由于是 linked list,
  
  * LPUSH & RPUSH 操作都是 constant time.

  * 但对于 access element by index requires an amount of work proportional to
    the index of the accessed element.

- Redis Lists are implemented with linked lists because for a database system
  it is crucial to be able to add elements to a very long list in a very fast
  way.

- example usages:

  * implement message queue, because redis commands are atomic.
    ``(L|R)(PUSH|POP)``, ``B(L|R)POP`` 等命令可实现消息队列.

  * 保存一列 latest entries for quick access. 该列条目可以进一步固定长度, 通过 
    LTRIM 来实现.

set
---

- collection of unique, unsorted strings.

sorted set
----------

- Every element is associated with a score.

- A score is a floating number.

- sorted by score. So it has order, and can talk about ranges.

- It's useful:
 
  * When fast access to the middle of a large collection of elements is
    important.

hash
----

- a map of strings to strings.

HyperLogLog (HLL)
-----------------

- a probabilistic data structure which is used in order to estimate the
  cardinality of a set (like counting unique things).

- 使用统计学的方法, 可以避免存储已经见过的每个 unique element,
  从而大大降低内存使用. 然而 tradeoff 是结果的精度. 对于 Redis 的 HLL
  implementation, 估计结果的标准差小于 1%.

- HLLs in Redis, while technically a different data structure, are encoded as a
  Redis string, so you can call GET to serialize a HLL, and SET to deserialize
  it back to the server.

- HLL data structure only contains a state that does not include actual
  elements.

- HLL is useful:

  * 估计一组非常大量的数据中 unique elements 的数量. 并且这个 unique element
    的数量可能非常大.  

  * 例如, number of unique queries performed by users.

redis expires
=============

- expired key is automatically deleted.

- resolution of key expire time is 1 millisecond.

- Information about expires are replicated and persisted on disk, actual expire
  time is stored in Unix timestamp. Therefore key expires no matter redis
  server is running or not.

- A key's expiry will be cleared by commands that delete or overwrite the
  contents of the key, including DEL, SET, GETSET, ``*STORE`` commands.

- A key's expiry will not be touched by any operation that conceptually alters
  the value stored at the key without replacing it with a new one.

- If a key is renamed, new key will inherit all the characteristics of the
  original key.

- If a negative timeout or an expiry time in the past is specified to a key,
  the key is deleted.

commands
========
- All redis's commands are atomic. This is simply a consequence of Redis
  using a single-threaded event loop to handle client operations.

generic
-------

EXISTS
^^^^^^

DEL
^^^
::

  DEL key [key ...]

- nonexistent key is ignored.

- returns the number of keys actually removed.

TYPE
^^^^

- returns the type of value or none.

EXPIRE
^^^^^^

- 

PERSIST
^^^^^^^

TTL
^^^

- returns: -1 (never expire), -2 (not exist).

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
^^^^^

bitmap
------

GETBIT
^^^^^^

SETBIT
^^^^^^

BITOP
^^^^^

- bitwise operation between keys.

BITCOUNT
^^^^^^^^

- Count the number of set bits (population counting) in a string.

BITPOS
^^^^^^

- Find first position of first bit having the specified value.

list
----

RPUSH
^^^^^

LPUSH
^^^^^

LLEN
^^^^

LRANGE
^^^^^^

- time complexity: O(N). accessing small ranges towards the head or the tail of
  the list is a constant time operation.

LPOP
^^^^

RPOP
^^^^

BLPOP
^^^^^
::

  BLPOP key [key ...] timeout

- timeout can be 0 to wait forever.

BRPOP
^^^^^

RPOPLPUSH
^^^^^^^^^

BRPOPLPUSH
^^^^^^^^^^

LTRIM
^^^^^

set
---

- unordered collection of strings.

SADD
^^^^

SREM
^^^^

SISMEMBER
^^^^^^^^^

SMEMBERS
^^^^^^^^

SUNION
^^^^^^

- combine multiple sets into one and returns it

SUNIONSTORE
^^^^^^^^^^^

SINTER
^^^^^^

SPOP
^^^^

SCARD
^^^^^

- get a set's cardinality, the same thing as LLEN.

SRANDMEMBER
^^^^^^^^^^^

sorted set
----------

- elements are unique, non-repeating string elements.

- every element in a sorted set is associated with a floating point value,
  called the score. This is like mapping elements to scores.

- Elements in a sorted sets are sorted in internal data structure. In other
  words, order is stored with data.

- elemented are sorted by:

  1) score

  2) lexicographically if score equals (by memcmp(3), 因此是纯二进制比较.)

ZADD
^^^^

- calling ZADD against an element already included in the sorted set will
  update its score (and position) with O(log(N)) time complexity.

ZREM
^^^^

ZREMRANGEBYSCORE
^^^^^^^^^^^^^^^^

ZRANGE
^^^^^^

ZREVRANGE
^^^^^^^^^

ZRANGEBYSCORE
^^^^^^^^^^^^^
::

  ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]

- min, max can be -inf, +inf. 默认是闭区间, prefixing the score with ``(``
  to specify an open interval.

ZRANGEBYLEX
^^^^^^^^^^^

ZREVRANGEBYLEX
^^^^^^^^^^^^^^

ZREMRANGEBYLEX
^^^^^^^^^^^^^^

ZLEXCOUNT
^^^^^^^^^

- Count the number of members in a sorted set between a given lexicographical
  range.

ZRANK
^^^^^

ZREVRANK
^^^^^^^^

hash
----
- there's no limit on the number of fields a hash can hold.

- small hashes (i.e., a few elements with small values) are encoded in special
  way in memory that make them very memory efficient.


HSET
^^^^

HMSET
^^^^^

HGET
^^^^

HGETALL
^^^^^^^

HINCRBY
^^^^^^^

HyperLogLog
------------

PFADD
^^^^^

PFCOUNT
^^^^^^^

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
