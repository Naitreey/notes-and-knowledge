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

messaging
=========
architecture
------------
redis 的 messaging model 是 publish/subscribe messaging model.

从 AMQP 的角度来看, redis 的 messaging model 可以描述为:

* A topic exchange.

* A subscriber (consumer) always declares a exclusive queue.

  Use SUBSCRIBE/PSUBSCRIBE to bind it to the topic exchange, the binding key is
  the channel name or pattern. SUBSCRIBE/PSUBSCRIBE to multiple
  channels/patterns equals to binding to the exchange multiple times, with a
  different binding key each time.

  This is equivalent to saying that a subscriber always receives messages
  published to the matching channel.

* Channel 不留存信息. A subscriber receives a message from a channel, only if
  it SUBSCRIBEd to the channel at the time the publisher PUBLISHed the message.
  也就是说, 如果 PUBLISH 时没有可接受的 subscriber, 则该条消息直接消失.

  这与 AMQP exchange 的机制是相同的.

* A client may receive a single message multiple times if it's subscribed to
  multiple channels/patterns matching a published message.

  这与 AMQP exchange 的机制是相同的.

* Once the client enters the subscribed state it is not supposed to issue any
  other commands, although it can subscribe and unsubscribe to and from other
  channels.

* The commands that are allowed in the context of a subscribed client are
  SUBSCRIBE, PSUBSCRIBE, UNSUBSCRIBE, PUNSUBSCRIBE, PING and QUIT.

Pub/Sub has no relation to the key space. It was made to not interfere with it
on any level, including database numbers. In other words, channels are global
objects.

message format
--------------
The message format is used for

- SUBSCRIBE/UNSUBSCRIBE response message.

- PSUBSCRIBE/PUNSUBSCRIBE response message.

- messages received by client SUBSCRIBEing to channels (direct exchange).

A message is a RESP Array with three elements.

1. the type of message.

   - subscribe/psubscribe. means that we successfully subscribed to a
     channel/pattern.

   - unsubscribe/punsubscribe. means that we successfully unsubscribed from a
     channel/pattern.

   - message. a message received as result of a PUBLISH command issued by
     another client.

2. channel name/pattern.

   - For subscribe/psubscribe, this is the channel/pattern that is subscribed.

   - For unsubscribe/punsubscribe, this is the channel/pattern that is
     unsubscribed.

   - For message, this is the channel where the message is originated.

3. data.

   - For subscribe/psubscribe, this is the number of channel/pattern the
     subscriber is currently subscribed to, after the SUBSCRIBE/PSUBSCRIBE
     operation.

   - For unsubscribe/punsubscribe, this is the number of channel/pattern the
     subscriber is currently subscribed to, after the UNSUBSCRIBE/PUNSUBSCRIBE
     operation. When it's 0, the client is out of the pub/sub state.

   - For message, this is the message payload.

pmessage format
---------------
The pmessage format is used for messages received by client PSUBSCRIBEing to
patterns (topic exchange), A pmessage is a RESP Array with four elements.

1. the type of message: pmessage. means a message received, as a result of
   matching a pattern-matching subscription.

2. pattern. the matched pattern.

3. channel name. the channel where the message is originated.

4. data. the message payload.

Related commands
----------------
SUBSCRIBE, UNSUBSCRIBE, PSUBSCRIBE, PUNSUBSCRIBE, PUBLISH, PUBSUB.

commands
========
- All redis's commands are atomic. This is simply a consequence of Redis
  using a single-threaded event loop to handle client operations.[SORedisConcurrency]_

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

SCAN
^^^^

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

hyperloglog
------------
PFADD
^^^^^

PFCOUNT
^^^^^^^


connection
----------
CONNECT
^^^^^^^

AUTH
^^^^

QUIT
^^^^
pubsub
------
SUBSCRIBE
^^^^^^^^^
::

  SUBSCRIBE channel [channel ...]

- Returns the subscription information, in the form of a message of
  ``subscribe`` type.

UNSUBSCRIBE
^^^^^^^^^^^
::

  UNSUBSCRIBE [channel ...]

- unsubscribe from given channels, or all channels.

- Returns the ``unsubscribe`` type information for each unsubscribed channel.

PSUBSCRIBE
^^^^^^^^^^
::

  PSUBSCRIBE pattern [pattern ...]

- patterns are file globs. supporting:

  * ``?`` one char

  * ``*`` 0 or more char

  * ``[]`` char class
   
  use \ to escape metachars.

PUNSUBSCRIBE
^^^^^^^^^^^^
::

  PUNSUBSCRIBE [pattern ...]

- similar to UNSUBSCRIBE

PUBLISH
^^^^^^^
::

  PUBLISH channel message

- publish a message.

- returns an integer, the number of clients that received the message.

PUBSUB
^^^^^^
introspect pub/sub system state.

::

  PUBSUB CHANNELS [pattern]

- list active channels. An active channel is a Pub/Sub channel with one or more
  subscribers, *not including clients subscribed to patterns*.

- if pattern is specified only channels matching the specified glob-style
  pattern are listed.

- Returns an Array of channel names.

::

  PUBSUB NUMSUB [channel ...]

- Returns the number of subscribers (not counting clients subscribed to
  patterns) for the specified channels.

- Returns an Array. The format is channel, count, channel, count, ..., so the
  list is flat, according to the order specified in command.

::

  PUBSUB NUMPAT

- returns the number of subscriptions to patterns.

scripting
---------
EVAL
^^^^

misc
----
HELP
^^^^
::

  help @<category>
  help <command>

- categories: generic, list, set, sorted_set, hash, pubsub, transactions,
  connection, server, scripting.

CLEAR
^^^^^
- clear screen.

persistence
===========
- AOF: append-only file.

replication
===========
- Replication is useful for read (but not write) scalability or data
  redundancy.

clustering
==========

CLI
===
redis-cli
---------
::

  redis-cli [options] [cmd [arg]...]

- A CLI client of redis.

interactive mode
^^^^^^^^^^^^^^^^
- redis-cli without any positional args enters REPL

- prompt format::

    host:port[n]>

- When redis-cli failed to connect to server, it enters REPL with
  prompt::

    not connected>

  Typing any command makes it try to reconnect.
  
  Generally after a disconnection is detected, the CLI always attempts to
  reconnect transparently: if the attempt fails, it shows the error and enters
  the disconnected state. When a reconnection is performed, redis-cli
  automatically re-select the last database number selected. 

- commandline editting is enabled by linenoise library.

  * history is preserved in ``$REDISCLI_HISTFILE``, which defaults to
    ``$HOME/.rediscli_history``.

  * command completion: Tab key.

- Repeat command by N times::

    N cmd [arg...]

non-interactive mode
^^^^^^^^^^^^^^^^^^^^
several ways of passing commands:

- a command and args are passed as arguments of redis-cli command.

- read commands from stdin.
  
  * one command per line.

  * arg with spaces/newlines can be quoted.

- ``-x``. read stdin as value of the last argument.

- ``-r <count>``. repeat command. To run forever, use -1 as count.

- ``-i <delay>``. delay between repeat, use decimal for fractional seconds.

stats mode
^^^^^^^^^^
- ``--stat`` option.

- ``-i <delay>`` specify delay between stats output.

- monitor stats of Redis instances in real time.

- a new line is printed every delayed seconds with useful information and the
  difference between the old data point.

key space analyzer mode
^^^^^^^^^^^^^^^^^^^^^^^
- ``--bigkeys`` option.

- ``-i <delay>`` throttles the scanning process by the specified fraction of
  second for each 100 keys requested.

- The outpout is separated in two parts:

  * In the first part of the output, each new key larger than the previous
    larger key (of the same type) encountered is reported.

  * The summary section provides general stats about the data inside the Redis
    instance.

key scanning mode
^^^^^^^^^^^^^^^^^
- ``--scan`` option.

- ``--pattern <pattern>``. filter by pattern.

- This scans key space with SCAN.

pub/sub mode
^^^^^^^^^^^^
- The subscriber mode is entered automatically when SUBSCRIBE or PSUBSCRIBE
  command is issued.

- The "reading messages message" shows that we entered Pub/Sub mode.

- Unlike other client, redis-cli will not accept any commands once in
  subscribed mode and can only quit the mode with Ctrl-C.

command monitoring mode
^^^^^^^^^^^^^^^^^^^^^^^
- Use MONITOR command.

latency monitoring mode
^^^^^^^^^^^^^^^^^^^^^^^

simple latency
""""""""""""""
- ``--latency`` option.

- Using this option the CLI runs a loop where the PING command is sent to the
  Redis instance, and the time to get a reply is measured. The min, max and
  avg of latency is printed.

- This happens 100 times per second, and stats are updated in a real time in
  the console.

- Latency are provided in milliseconds.

- The average latency of a very fast instance tends to be overestimated a bit
  because of the latency due to the kernel scheduler of the system

latency history
"""""""""""""""
- ``--latency-history`` option.
  
- shows the stats evolution through time. It works like ``--latency``, but
  every delay seconds a new sampling session is started from scratch.

- ``-i <delay>`` specify the length of sampling session, by default it's 15
  seconds.

latency distribution
""""""""""""""""""""
- ``--latency-dist``.

- use color terminals to show a spectrum of latencies.

- You'll see a colored output that indicate the different percentages of
  samples, and different ASCII characters that indicate different latency
  figures.

intrinsic latency
"""""""""""""""""
- ``--intrinsic-latency <test-time>`` option.
  
- The test's time is in seconds, and specifies how many seconds redis-cli
  should check the latency of the system it's currently running on.

- The latency that's intrinsic to the kernel scheduler

- this command must be executed on the computer you want to run Redis server
  on, not on a different host. It does not even connect to a Redis instance and
  performs the test only locally.

lua scripting mode
^^^^^^^^^^^^^^^^^^
- ``--eval <file>``. evaluate lua script file. 此时, args 格式为::

    key1 key2 ... , val1 val2 ...

  number of keys and values should match.

RDB dump mode
^^^^^^^^^^^^^
- ``--rdb <file>``.

- a remote backup facility, that allows to transfer an RDB file from any Redis
  instance to the local computer, by pretending to be slave connecting to a
  master.

slave mode
^^^^^^^^^^
- ``--slave``.

- useful for Redis developers and for debugging operations. It allows to
  inspect what a master sends to its slaves in the replication stream.

- The command begins by discarding the RDB file of the first synchronization
  (because we are not actually slave, we only need what is to send) and then
  logs each command received as in CSV format.

LRU simulation mode
^^^^^^^^^^^^^^^^^^^
- ``--lru-test <num-keys>``.

- performs a simulation of GET and SET operations, using an 80-20% power law
  distribution in the requests pattern. This means that 20% of keys will be
  requested 80% of times, which is a common distribution in caching scenarios.

- its main motivation was for testing the quality of Redis' LRU implementation,
  but now is also useful in for testing how a given version behaves with the
  settings you had in mind for your deployment.

- 测试 maxmemory setting and maxmemory policy 与应用场景中需要使用的 keys 的数
  目两者的结合, key hits/misses 的比例.

output formatting
^^^^^^^^^^^^^^^^^
* human-readable format: When redis-cli detects the stdout is a tty, or when
  ``--no-raw`` is enforced, it uses pretty human-readable format.

* raw format: When stdout is not a tty, or when ``--raw`` is enforced, use raw
  output format.

- csv format: Use ``--csv``.

connection options
^^^^^^^^^^^^^^^^^^
- ``-h <host>``. host. default 127.0.0.1

- ``-p <port>``. port. default 6379

- ``-a <password>``. password.

- ``-n <dbnum>``. database number.

- ``-s <socket>``. server socket.

- ``-u <uri>``. a uri specifying connection parameters.::

    redis://[password@]host[:port][/db]

Client libraries
================
redis-py
--------
installation
^^^^^^^^^^^^
- redis package

- deps:

  * hiredis, C client library, a prefered high performance parser library.

overview
^^^^^^^^
- By default, all responses are returned as bytes in Python 3 and str in Python 2.

- redis-py attempts to adhere to the official command syntax. with following
  exceptions:

  * SELECT, not implemented.

  * DEL. del is a python keyword, rename to delete.

  * MULTI/EXEC. part of Pipeline class.

  * SUBSCRIBE, etc. part of PubSub class, as it places the underlying
    connection in a state where it can't execute non-pubsub commands.

  * SCAN, etc. Besides the samely named methods, there're are also iterator
    equivalent method.

Redis
^^^^^

response callbacks
""""""""""""""""""
- The client class uses a set of callbacks to cast Redis responses to the
  appropriate Python type. These are defined in ``response_callbacks``.

- Custom callbacks can be added on a per-instance basis using the
  ``set_response_callback`` method. Callbacks added in this manner are only
  valid on the instance the callback is added to.
  
- To define callbacks globally, make a subclass of the Redis client and modify
  RESPONSE_CALLBACKS class dictionary.

- callback signature::

    callback(response[, opt1, ...])

  * resopnse is server response for this command.

  * optional parameters can be defined, they are passed as kwargs during call,
    from ``execute_command()`` method.

thread safety
"""""""""""""
- Redis client instances can safely be shared between threads. Internally,
  connection instances are only retrieved from the connection pool during
  command execution, and returned to the pool directly after.

- Command execution never modifies state on the client instance.

ConnectionPool
^^^^^^^^^^^^^^
- Connections to redis server is actually managed by a connection pool. A Redis
  client does not make connections directly.

- 由于一个 redis connection instance 本身不具有 thread safety, Connection pool
  维持一组连接, 记录空闲的连接与正在使用的连接, 每次只提供空闲的连接, 从而避免
  了 thread safety 的问题.

  这样, Redis client 等上层封装通过 connection pool 使用连接时, 本身具有了
  thread safety.

Connection
^^^^^^^^^^
- A connection to redis server, by TCP.

UnixDomainSocketConnection
^^^^^^^^^^^^^^^^^^^^^^^^^^
- A connection to redis server, by unix domain socket.

PythonParser
^^^^^^^^^^^^
- parse response from redis server using pure python implementation.

- This is a fallback parser when HiredisParser is not usable.

HiredisParser
^^^^^^^^^^^^^
- High performance response parser using C client library hiredis.

- depends on hiredis module.

references
==========
.. [SOMemcachedRedis] https://stackoverflow.com/questions/10558465/memcached-vs-redis
.. [SORedisConcurrency] `Redis is single-threaded, then how does it do concurrent I/O? <https://stackoverflow.com/questions/10489298/redis-is-single-threaded-then-how-does-it-do-concurrent-i-o>`
