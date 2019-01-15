overview
========
- redis: REmote DIctionary Server

- in-memory key-value store, a data structures server.

  * A key-value store maps keys to values.

  * Values can be many kinds of data types.

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
* A redis key is a redis string type value. So it can be any binary sequence.

* A key can be empty string.

* creation and removal of keys.

  - When we add an element to an aggregate data type, if the target key does
    not exist, an empty aggregate data type is created before adding the
    element.

  - When we remove elements from an aggregate data type, if the value remains
    empty, the key is automatically destroyed.

  - Calling a read-only command, or a write command removing elements with an
    nonexistent key, 相当于应用该命令在一个类型相符的 empty aggregate value
    上面.

design patterns
---------------
* very long keys is bad, because
  
  1) use more memory.
  
  2) key comparison during lookups becomes expensive.

  When there's need to use a very long key, using its hash as actual key value
  is a better idea.

* 由于 key 没必要是 identifier, 而是任意字符, 对于复杂的应用场景, 需要规范一个
  key schema, 即划分 key 的结构. 例如 ``ns1:ns2:keyname``

  常见分隔符: ``:`` 用于分隔层级, ``.`` or ``-`` 用于层级内 word separation.

data types
==========
string
------
- strings can be any binary sequence. It's not unicode string, but binary
  string.

- A string's max size is 512MB.

- empty string is allowed.

- Some use cases for string values:

  * cache html pages.

bitmap/bit array
^^^^^^^^^^^^^^^^
- Bitmaps are not an actual data type, but a set of bit-oriented operations
  defined on the string type. 因此可以分别使用 GET/SET 去 serialize/deserialize
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

  * Space efficient but high performance boolean information associated with
    object IDs. 前提要求是 object id 是依次递增的. 否则在小数据量时会造成不必要
    的内存浪费.

list
----
- A redis list is a linked list, where elements are strings.
  
- 由于是 linked list, 好处是 push/pop at both sides 操作都是 constant time.
  这对于一个数据库系统来说是很重要的.
  
  但缺点是, access by index is O(N). 若需要对首尾之外的中间部分的快速访问,
  可考虑 sorted set.

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
- A set where every element (a string) is associated with a score, and
  sorted by their scores.

- A score is a floating number.

- elemented are sorted by:

  1) score ascendingly

  2) lexicographically if score equals (by memcmp(3), 因此是纯二进制比较.)

- Because a sorted set has ordering, there are commands acting on ranges.

- a sorted set is implemented by a skip list and a hash table.

- It's useful:
 
  * When fast access to the middle of a large collection of elements is
    important.

hash
----
- a map of strings to strings.

- there's no limit on the number of fields a hash can hold.

- small hashes (i.e., a few elements with small values) are encoded in special
  way in memory that make them very memory efficient.

HyperLogLog (HLL)
-----------------
- a probabilistic data structure which is used in order to estimate the
  cardinality of a set.

- 使用统计学的方法, 可以避免存储已经见过的每个 unique element, 从而大大降低内存
  使用. 然而 tradeoff 是结果的精度. 对于 Redis 的 HLL implementation, 估计结果
  的标准差小于 1%.

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
redis 的 messaging model 是 publish/subscribe messaging model. 因此它只适合
pub/sub 模式适合的应用场景, 而这只是 general messaging 概念的一个子集而已. 除此
之外的使用场景应该用更一般化的 messaging model, 例如 AMQP.

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

注意到, 由于 redis 中相当于 subscriber 总是 declare exclusive queue, 因此在
redis 中一个 subscriber 永远只能收到它 subscribe 一个 channel 之后发到这个
channel 的消息. 而 rabbitmq 等 AMQP 实现, 由于具有独立于 consumer 的队列实体,
只要队列预先存在, consumer 可以收到之前加入队列中 (尚未被消费) 的消息. 因此, 若
需要 message broker 具有相对于 consumer 而言是持久化的队列, 则 redis pub/sub 不
是一个合适的选择. 此时, 可以选择 list or stream (但相当于直接 produce 至队列,
失去了 exchange 的灵活性), 或者直接使用专业的 message broker middleware, 例如
rabbitmq.

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

pipelining
==========
- Pipeline 是用于在一次网络请求中发送多条 commands 至 redis server, 并在一次
  响应中包含多条相应的 command responses.

- pipeline 不是通过一个专门的命令来实现的, 而仅仅是通过一次性地向 socket 中写入
  多条 commands 来实现的. 所以, 一般情况下, pipeline 功能由 client library 提供
  更便于使用的封装层.

- Pipeline 的目的和价值:
  
  * 避免在 request-response cycle 中, 网络 RTT 成为命令执行效率的瓶颈. Pipeline
    将多条命令一次发出, 从而将多次 RTT 带来的延迟减少为一次. 这是 pipeline 的
    主要目的.

  * 由于一次 pipeline 只需进行一组 socket IO, 即调用 ``read()``, ``write()``
    syscalls 各一次, 这样很大程度上减少 context switch 带来的 penalty.

- Redis 需要 pipeline 这种设计, 而 sql 不需要. 这是因为 SQL 是一个比较完备的
  语言 (actually Turing-complete), 可以用 SQL 写一系列处理逻辑, 发给 server
  计算后一次性给出结果. 而 redis commands 只是一系列相对孤立的操作, 没有必要的
  flow control, 变量赋值等 language construct, 所有逻辑需要由 client
  application 来完成. 这样就需要更多的交互. 而 pipeline 可以在一定程度上将
  部分客户端逻辑打包, 一次性执行给出结果.

- Pipelining is a technique widely in use since many decades.

- While the client sends commands using pipelining, the server will be forced
  to queue the replies, using memory. So if you need to send a lot of commands
  with pipelining, it is better to send them as batches having a reasonable
  number, for instance 10k commands, read the replies, and then send another
  10k commands again, and so forth.

transactions
============
- A transaction allow the execution of a group of commands in a single step.

transaction properties
----------------------
* All the commands in a transaction are serialized and executed sequentially.
  It can never happen that a request issued by another client is served in
  the middle of the execution of a Redis transaction.

* All the commands in a transaction are executed atomically. Either all or
  none of the commands are executed. When using the append-only file Redis
  makes sure to use a single write(2) syscall to write the transaction on
  disk.

workflow
--------
- A transaction is entered by MULTI.
  
- Then commands can be issued. All commands will reply with the string QUEUED.

- Before EXEC, instead of executing these commands, Redis will queue them.

- To execute the transaction, issue EXEC. Then the transaction is scheduled for
  execution.
  
- To discard the transaction, issue DISCARD, this will flush the command queue.

注意到在 transaction 内部, 并不能进行任何有效的读操作, 也就是说不能根据读取的数
据调整执行逻辑和写操作. 因此看上去 transaction 只有与 pipeline 一起使用才有价值.

optimistic locking with check-and-set (CAS)
-------------------------------------------
- Use WATCH with transaction for optimistic locking.

- WATCHed keys are monitored in order to detect changes against them. If at
  least one watched key is modified before the EXEC command, the whole
  transaction aborts, and EXEC returns a Null reply to notify that the
  transaction failed. Then we can retry the operation.

- When EXEC is called, all keys are UNWATCHed, regardless of whether the
  transaction was aborted or not. When DISCARD is called, all keys are also
  UNWATCHed. Also when a client connection is closed, everything gets
  UNWATCHed.

- It is also possible to use the UNWATCH command (without arguments) in order
  to flush all the watched keys explicitly before EXEC.

error handling
--------------
- If a command fails to be queued, e.g., the command is syntactically wrong,
  there's some critical condition, the server returns an error rather than
  QUEUED. In this case, client should abort the transaction by DISCARDing it.

  The server will remember that there was an error during the accumulation of
  commands. If client enforced a EXEC, the server will refuse to execute the
  transaction, returning another error and discarding the transaction
  automatically.

- If a command fails after EXEC is called, e.g., we performed an operation
  against a key with the wrong value, all the other commands will be executed
  even if some command fails during the transaction.

- Redis does *not* support transaction rollback.

  * Redis commands can fail only if called with a wrong syntax that is not
    detectable during the command queueing, or against keys holding the wrong
    data type. This means a failing command is the result of a programming
    errors and never a data integrity error. Thus it's the kind of fault that
    can be avoided entirely at author time.

  * Redis is internally simplified and faster because it does not need the
    ability to roll back.

usage
-----
- 用于进行具有原子性的多个操作.

- 与 optimistic locking 结合, 实现具有原子性的更复杂操作.

- 与 pipeline 结合, 优化 transaction 的执行效率, 降低延迟.

lua scripting
=============
- 在 Redis 中, 与 SQL 的编程性相对应的是, lua scripting. 使用 lua script, 可以
  完成单个 pipeline 无法实现的逻辑, 同时具有 pipeline 类似的单次
  request-response 带来的低延迟优势.

- A Redis script is transactional by definition, so everything you can do with
  a Redis transaction, you can also do with a script, and usually the script
  will be both simpler and faster.

commands
========
- All redis's commands are atomic. This is simply a consequence of Redis
  using a single-threaded event loop to handle client operations.[SORedisConcurrency]_

generic
-------

EXISTS
^^^^^^
::

  EXISTS key [key]...

- returns the total number of keys existing. if the same existing key is
  mentioned in the arguments multiple times, it will be counted multiple times.

DEL
^^^
::

  DEL key [key ...]

- nonexistent key is ignored.

- returns the number of keys actually removed.

TYPE
^^^^
::

  TYPE key

- returns the type of value or none, in string form. (string, list, set, zset,
  hash and stream, none).

EXPIRE
^^^^^^
::

  EXPIRE key seconds

- Set or reset a key's EXPIRE time countdown. Return 1 if timeout is set, 0 if
  key does not exist.

- A key with an associated timeout is called a volatile key.

- The timeout will only be cleared by commands that delete or overwrite the
  contents of the key, including DEL, SET, GETSET and all the ``*STORE``
  commands. All the operations that conceptually *alter* the value stored at
  the key without replacing it with a new one will leave the timeout untouched.

- Use PERSIST to clear timeout.

- When a key is RENAMEd, timeout is transfered to new key.

- When ``seconds`` is negative, or EXPIREAT specified a time in the past, the
  key is deleted immediately, rather than expired.

- Expire accuracy: the expire error is from 0 to 1 milliseconds.

- Keys expiring information is stored as absolute Unix timestamps in
  milliseconds. This means that the time is flowing even when the Redis
  instance is not active. This also means all nodes in a clustered redis setup
  must have stable, synced time.

- Expire strategies: passive and active expiry.

  * passive expiry. A key is passively expired simply when some client tries to
    access it, and the key is found to be timed out. 然而一些 key 可能不会再被
    访问, 造成内存浪费. 因此 passive expiry 是不够的, 还需要 active expiry.

  * active expiry. Periodically Redis tests a few keys at random among keys
    with an expire set. All the keys that are seen expired are deleted from the
    keyspace.

    Redis does the following expiry checking for 10 times per second:

    - Test 20 random keys from the set of keys with an associated expire.

    - Delete all the keys found expired.

    - If more than 25% of keys were expired, start again from step 1.

    This means that at any given moment the maximum amount of keys already
    expired that are using memory is at max equal to max amount of write
    operations per second divided by 4.

- During replication, the replicas connected to a master will not expire keys
  independently but will wait for the DEL coming from the master.

PERSIST
^^^^^^^
::

  PERSIST key

- remove expiry on key.

- returns 1 if succuess, 0 if key not exist or no expiry attached.

TTL
^^^
::

  TTL key

- returns: TTL in seconds, or -1 (never expire), -2 (not exist).

PTTL
^^^^
::

  PTTL key

- returns: TTL in milliseconds, or -1 (never expire), -2 (not exist).

SCAN
^^^^
::

  SCAN cursor [MATCH pattern] [COUNT count]

- Incrementally iterate over the set of keys in the currently selected Redis
  database.

- It allow for incremental iteration, returning only a small number of elements
  per call, therefore they can be used in production without risking blocking
  the server when called against big collections of keys.

- The SCAN family of commands only offer limited guarantees about the returned
  elements since the collection that we incrementally iterate can change during
  the iteration process.

- SCAN is a cursor based iterator. This means that at every call of the
  command, the server returns an updated cursor that the user needs to use as
  the cursor argument in the next call.  An iteration starts when the cursor is
  set to 0, and terminates when the cursor returned by the server is 0 (a full
  iteration).

- Guarantees:

  * A full iteration always retrieves all the elements that were present in the collection from the start to the end of a full iteration. This means that if a given element is inside the collection when an iteration is started, and is still there when an iteration terminates, then at some point SCAN returned it to the user.


- Returns an array of two values: the first value is the new cursor to use in
  the next call, the second value is an array of elements.

string
------
GET
^^^
::

  GET key

- If the key does not exist the special value nil is returned.

- Because GET only handles string values, An error is returned if the value
  stored at key is not a string.

SET
^^^
::

  SET key value [EX seconds | PX milliseconds] [NX|XX]

- set value to string value. By default any existing value is overriden.

- Returns OK, or nil if condition not met.

- Any previous TTL associated with the key is discarded on successful SET.

- ``EX``. expire time in seconds.

- ``PX``. expire time in milliseconds.

- ``NX``. set only if not exist.

- ``XX``. set only if already exist.

INCR
^^^^
::

  INCR key

- Parse the value of key as base-10 64 bit signed integer, increment by 1. If
  key does not exist, set it to 0 before incrementing.

- Return the resulted number. Or abort with error, if value can not be
  interpreted as integer or out of range.

- limited by 64bit signed integer.

- Redis stores integers in their integer representation, so for string values
  that actually hold an integer, there is no overhead for storing the string
  representation of the integer.

  但在 GET 这样的整数时, 仍然输出的是正确的 number value, in string form.

- Usage. 当一个 key 作为 counter 使用时, 解决 race condition. INCR 解决的问题是
  多个客户端需要递增一个量时, 各自 GET then SET 存在信息不同步的问题, 从而导致
  race condition. INCR 由 server 控制, 这样就把控制权集中了, 在多线程 (多客户端
  的一般化) 情况下避免了 race condition. 这是 atomic operation 的意义.

  类似于 database 中的 auto increment field.

INCRBY
^^^^^^
::

  INCRBY key increment

- similar to INCR, by an amount. The amount can be negative to actually
  decrement.

INCRBYFLOAT
^^^^^^^^^^^
::

  INCRBYFLOAT key increment

- like INCRYBY, for float.

- Both the value already contained in the string key and the increment argument
  can be optionally provided in exponential notation, however the value
  computed after the increment is stored consistently in the same format, that
  is, an integer number followed (if needed) by a dot, and a variable number of
  digits representing the decimal part of the number. Trailing zeroes are
  always removed.

- The precision of the output is fixed at 17 digits after the decimal point
  regardless of the actual internal precision of the computation.

- The command is always propagated in the replication link and the Append Only
  File as a SET operation, so that differences in the underlying floating point
  math implementation will not be sources of inconsistency.

DECR
^^^^
::

  DECR key

- similar to INCR, negative number is possible.

DECRBY
^^^^^^
::

  DECRBY key decrement

- similar to DECR, by an amount. amount can be negative.

GETSET
^^^^^^
::

  GETSET key value

- Atomically sets key to value and returns the old value.

- Returns nil if key is not string.

- Usage. 解决 race condition. GETSET 解决的问题是一个客户端现在即要 GET 又要
  SET, 如果 GET then SET, 则两个操作之间的时间差允许其他客户端对该 key 值进行修
  改. 之后的 SET 就错误 override 了别的客户端的修改. 所以实现一个 atomic 的 GET
  & SET 操作, 消除了这个时间差, 也就消除了引发的 race condition.

- usage examples.

  * 一个客户端需要定时获取 counter 值用于统计并重置该 counter. 其他客户端只进行
    INCR.

MGET
^^^^
::

  MGET key [key]...

- Returns an Array of values, for every key that does not hold a string value
  or does not exist, the special value nil is returned.

- useful to reduce latency and atomically get multiple values.

MSET
^^^^
::

  MSET key value [key value]...

- Returns OK.

- useful to reduce latency and atomically set multiple values.

MSETNX
^^^^^^

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

LLEN
^^^^

LRANGE
^^^^^^
::

  LRANGE key start stop

- Returns an Array of elements from start to stop, inclusive.

- indexes are 0-based. negative counts from the end of the list, -1 is the
  last.

- Out of range indexes will not produce an error but an empty Array, like
  python slicing. start bigger than stop also produces empty Array.

- accessing small ranges towards the head or the tail of the list is a constant
  time operation.

LTRIM
^^^^^
::

  LTRIM key start stop

- trim a list, leaving the specified range.

- start/stop is the same as LRANGE.

- returns OK.

LREM
^^^^
::

  LREM key count value

- remove the first count occurrences of value from key.

- count:

  * positive, remove first count.

  * negative, remove last ``|count|``.

  * 0, remove all elements.

- Returns the number of removed elements.

LPUSH
^^^^^
::

  LPUSH key value [value]...

- push values at head of list. 对于一次 push 多个元素的情况, elements are
  inserted one after the other to the head of the list, from the leftmost
  element to the rightmost element. 这导致, list 中元素的顺序是 LPUSH 参数
  列表的逆序.

- Returns the length of list after push. an error is returned when key is not
  list.

RPUSH
^^^^^
::

  RPUSH key value [value]...

- push values at tail of list. 对于多个元素的情况, 结果顺序与参数顺序一致, 这与
  LPUSH 正好相反.

- Returns the length of list after push. an error is returned when key is not
  list.

LPOP
^^^^
::

  LPOP key

- pop first element off key.

- returns the value, or nil if key not exist.

RPOP
^^^^
::

  RPOP key

- pop last element off key. otherwise like LPOP.

BLPOP
^^^^^
::

  BLPOP key [key]... timeout

- An element is popped from the head of the first list that is non-empty, with
  the given keys being checked in the order that they are given. Block the
  connection when there are no elements to pop from any of the given lists
  (i.e., none of the keys exists).

- timeout is the max seconds to wait, can be 0 to wait forever.

- Returns an Array, the first is the name of the key where element is popped,
  the second is the value of the popped element. Or nil if no element is
  available and timeout is expired.

- serving order.
  
  * If multiple clients are blocked for the same key, the first client to be
    served is the one that was waiting for more time (the first that blocked
    for the key). Once a client is unblocked it does not retain any priority.

  * When a client is blocking for *multiple keys* at the same time, and
    elements are available at *the same time* in multiple keys (because of a
    transaction or lua script), the client will be unblocked using the first
    key that received an element.

  * After the execution of every command/transaction/script, Redis will run a
    list of all the keys that received data AND that have at least a client
    blocked. The list is ordered by new element arrival time, from the first
    key that received data to the last. For every key processed, Redis will
    serve all the clients waiting for that key in a FIFO fashion, as long as
    there are elements in this key. When the key is empty or there are no
    longer clients waiting for this key, the next key that received new data in
    the previous command / transaction / script is processed, and so forth.

- BLPOP inside a transaction never blocks, it either pops an element immediately
  or returns nil. Otherwise the operation will block the server.

BRPOP
^^^^^
::

  BRPOP key [key]... timeout

- similar to BLPOP, but for tail.

RPOPLPUSH
^^^^^^^^^
::

  RPOPLPUSH source destination

- atomically RPOP from source and LPUSH to destination.

- returns the popped element, or nil if source does not exist.

- If source and destination is the same list, equivalent to list rotation.

BRPOPLPUSH
^^^^^^^^^^
::

  BRPOPLPUSH source destination timeout

- block variant of RPOPLPUSH.

set
---
SADD
^^^^
::

  SADD key member [member]...

- add members to key.

- returns the number of elements actually added.

SREM
^^^^
::

  SREM key member [member]...

- remove members from key.

- returns the number of elements actually removed.

SPOP
^^^^
::

  SPOP key [count]

- pop random count (default 1) number of elements from set.

- return the popped element, or an Array of popped elements or nil if set not
  exist.

- If count is bigger than the number of elements inside the Set, the command
  will only return the whole set without additional elements.

SRANDMEMBER
^^^^^^^^^^^
::

  SRANDMEMBER key [count]

- returns a random element from set, or an Array of count random elements,
  or nil if set does not exist.

- For positive count, returned elements must be unique. If count is bigger than
  the number of elements inside the Set, the command will only return the whole
  set without additional elements.

- For negative count, returned elements can be duplicates.

SMEMBERS
^^^^^^^^
::

  SMEMBERS key

- returns an Array of members.

SINTER
^^^^^^
::

  SINTER key [key]...

- returns the intersection of given sets, as an Array.

- Keys that do not exist are considered to be empty sets. With one of the keys
  being an empty set, the resulting set is also empty.

SINTERSTORE
^^^^^^^^^^^
::

  SINTERSTORE destination key [key]...

- SINTER keys then store result at destination (overriden if exists).

- returns the number of elements in the resulting set.

- ``SINTERSTORE`` with one source key can be used to duplicate the set.

SUNION
^^^^^^
::

  SUNION key [key]...

- returns the union of given sets, as an Array.

SUNIONSTORE
^^^^^^^^^^^
::

  SUNIONSTORE destination key [key]...

- SUNION then store result at destination.

- returns the number of elements in resulting set.

- ``SUNIONSTORE`` with one source key can be used to duplicate the set.

SDIFF
^^^^^
::

  SDIFF key [key]...

- returns the members by computing ``key1 - key2 - key3 ...``.

SDIFFSTORE
^^^^^^^^^^
::

  SDIFFSTORE destination key [key ...]

- SDIFF then store at destination.

- Returns the number of elements in the resulting set.

SCARD
^^^^^
::

  SCARD key

- Returns a set's cardinality, i.e., its length. 0 if key not exist.

SISMEMBER
^^^^^^^^^
::

  SISMEMBER key member

- returns 1 if key has member, 0 otherwise.

SSCAN
^^^^^
sorted set
----------
ZADD
^^^^
::

  ZADD key [NX|XX] [CH] [INCR] score member [score member]...

- adds members with scores to the sorted set.

- If a specified member is already a member of the sorted set, the score is
  updated and the element reinserted at the correct position to ensure correct
  ordering.

- score value: the string representation of a double precision floating point
  number (IEEE 754). +inf and -inf are valid.

- NX. only add nonexisting (new) elements, don't update existing elements.

- XX. only update existing elements, don't add new elements.

- CH. return value represents the number of elements changed. Changed elements
  include new elements and existing elements for which score was changed.

- INCR. make ZADD act like ZINCRBY. only one score-member pair is allowed.
  This mode can be affected by NX/XX, in which case only non-existing or
  existing element's score can be INCR-ed.

- Returns
  
  * normally: number of elements added, not including existing updated
    elements.

  * with CH: number of elements changed.

  * with INCR. the new score, like ZINCRBY. If NX/XX condition is invalidated,
    return nil.

ZREM
^^^^
::

  ZREM key member [member]...

- Remove members. returns the number of elements actually removed from sorted
  set.

ZREMRANGEBYSCORE
^^^^^^^^^^^^^^^^
::

  ZREMRANGEBYSCORE key min max

- Removes all elements in the sorted set stored at key with a score between min
  and max.

- min, max syntax is the same as ZRANGEBYSCORE.

- returns the number of elements actually removed.

ZREMRANGEBYLEX
^^^^^^^^^^^^^^
::

  ZREMRANGEBYLEX key min max

- having the same requirements as ZRANGEBYLEX.

- min, max syntax is the same as ZRANGEBYLEX.

- returns the number of elements actually removed.

ZINCRBY
^^^^^^^
::

  ZINCRBY key increment member

- increment member of key, by increment.

- The increment should be the string representation of a numeric value, and can
  be double precision floating point numbers. Can be negative to decrement.

- Returns the new score of member.

ZSCORE
^^^^^^
::

  ZSCORE key member

- return the score of member at key.

ZRANGE
^^^^^^
::

  ZRANGE key start stop [WITHSCORES]

- Returns the range of elements of sorted set, from start to stop.

- Ranges are computed by elements' ordering.

- start/stop is the same as LRANGE.

- WITHSCORES, return the scores of the elements together with the elements.
  The returned list is of form: value1,score1,...

ZRANGEBYSCORE
^^^^^^^^^^^^^
::

  ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]

- Returns the range of elements with scores between min and max. The elements
  having the same score are returned in lexicographical order.

- min, max can be any score, -inf, +inf. 默认是闭区间, prefixing the score with
  ``(`` to specify an open interval.

- LIMIT. select by offset and count in the filtered range of elements.

ZRANGEBYLEX
^^^^^^^^^^^
::

  ZRANGEBYLEX key min max [LIMIT offset count]

- Returns an Array of elements in range.

- Can be used only when all scores in a sorted set are equal. When there're
  different scores, return value is unspecified.

- min, max must start with ``(``, ``[``, for exclusive or inclusive. ``+`` and
  ``-`` denotes positively infinite and negatively infinite strings. min, max
  are strings compared with elements by ``memcmp()`` function, to determine
  ranges.

ZREVRANGE
^^^^^^^^^
::

  ZREVRANGE key start stop [WITHSCORES]

- similar to ZRANGE, in descending order.

ZREVRANGEBYSCORE
^^^^^^^^^^^^^^^^
::

  ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]

- Note: max first, min second. Return in descending order. Otherwise similar to
  ZRANGEBYSCORE.

ZREVRANGEBYLEX
^^^^^^^^^^^^^^
::

  ZREVRANGEBYLEX key max min [WITHSCORES] [LIMIT offset count]

- similar to ZRANGEBYLEX, in descending order.

ZPOPMIN
^^^^^^^
::

  ZPOPMIN key [count]

- pop count (default 1) lowest members from key, as ordered by score and lex.

- Returns an Array of popped elements and scores, in order. Or an empty Array.

ZPOPMAX
^^^^^^^
::

  ZPOPMAX key [count]

- Like ZPOPMIN, for highest members.

- In return, the one with the highest score will be the first, followed by the
  elements with lower scores.

BZPOPMIN
^^^^^^^^
::

  BZPOPMIN key [key]... timeout

- a blocking variant of ZPOPMIN.

- The blocking and popping behavior is like BLPOP.

- Returns nil if timeout expired, or an Array with three elements: key, score,
  member.

BZPOPMAX
^^^^^^^^
::

  BZPOPMAX key [key]... timeout

- a blocking variant of ZPOPMAX.

- The blocking and popping behavior is like BRPOP.

- Returns nil if timeout expired, or an Array with three elements: key, score,
  member.

ZLEXCOUNT
^^^^^^^^^

- Count the number of members in a sorted set between a given lexicographical
  range.

ZRANK
^^^^^
::

  ZRANK key member

- the rank (i.e., index) of member in key, in ascending order.

- rank is 0-based.

- Returns the rank integer, or nil if member or key does not exist.

ZREVRANK
^^^^^^^^
::

  ZREVRANK key member

- rank in ascending order. otherwise like ZRANK.

ZCOUNT
^^^^^^
::

  ZCOUNT key min max

- the number of elements in key, between min and max scores.

- min, max has the same syntax as ZRANGEBYSCORE.

- returns the number of elements in range.

ZSCAN
^^^^^
::

  ZSCAN key cursor [MATCH pattern] [COUNT count]

- Work like SCAN. Iterates elements of a sorted set.

hash
----
HSET
^^^^
::

  HSET key field value

- set field of key to value.

- returns 1 if field is created and set; 0 if field is updated.

HGET
^^^^
::

  HGET key field

- get field of key.

- returns the string or nill if field or key not exist.

HMSET
^^^^^
::

  HMSET key field value [field value]...

- set multiple fields.

HMGET
^^^^^
::

  HMGET key field [field]...

- Returns an Array with values of all matching fields.

- A nil is returned for every non-existent field.

HGETALL
^^^^^^^
::

  HGETALL key

- Returns an Array containing all fields and values of a hash. In the array,
  every field name is followed by its value. Or an empty list if key not exist.

HDEL
^^^^
::

  HDEL key field [field]...

- Remove specified fields from key.

- Returns the number of fields actually removed.

HKEYS
^^^^^
::

  HKEYS key

- returns all field names in an Array, or empty Array.

HVALS
^^^^^
::

  HVALS key

- similar to HKEYS for values.

HEXISTS
^^^^^^^
::

  HEXISTS key field

- returns 1 if field exists in key, 0 otherwise.

HLEN
^^^^
::

  HLEN key

- returns the number of fields at key. 0 if not exist.

HINCRBY
^^^^^^^
::

  HINCRBY key field increment

- similar to INCRBY, act on a field of hash.

- returns the value after increment.

HINCRBYFLOAT
^^^^^^^^^^^^
::

  HINCRBYFLOAT key field increment

- like INCRBYFLOAT, for hash field.

- The command is always propagated in the replication link and the Append Only
  File as a HSET operation, so that differences in the underlying floating
  point math implementation will not be sources of inconsistency.

hyperloglog
------------
PFADD
^^^^^

PFCOUNT
^^^^^^^


transactions
------------
WATCH
^^^^^
::

  WATCH key [key ...]

- Mark one or more keys to be watched prior to starting a transaction.  If any
  of those keys change prior EXEC of that transaction, the entire transaction
  will be canceled.

- Non-existent key can be watched. If it's added after WATCH before EXEC, the
  transaction will be canneled.

- WATCH makes EXEC conditional: perform the transaction only if none of the
  WATCHed keys were modified.

- If you WATCH a volatile key and Redis expires the key after you WATCHed it,
  EXEC will still work.

- WATCH can be called multiple times before the EXEC. The keys are watched
  starting from their respective calls, up to the moment EXEC is called.

- Returns OK.

UNWATCH
^^^^^^^
::

  UNWATCH

- unwatch all keys explicitly.

- returns OK.

MULTI
^^^^^
::

  MULTI

- mark start of transaction block.

- returns OK.

EXEC
^^^^
::

  EXEC

- execute transaction, and restore connection state to normal.

- Returns Array of each command's response, or NULL reply if execution is
  aborted because of WATCH lock.

DISCARD
^^^^^^^
::

  DISCARD

- discard transaction, all queued commands and restore connection state to
  normal.

- also unwatch all keys.

- returns OK.

connection
----------
CONNECT
^^^^^^^

SELECT
^^^^^^
::

  SELECT index

- select redis logical database by its 0-based index number.

- new connection use 0 db by default.

- SELECT can not be used in Redis Cluster.

- Returns Simple string "OK".

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

- returns an integer, the number of bindings that received the message.  注意不
  是 number of clients, 因为若一个 client 有多个 bindings matching the
  published channel, 则为多个 bindings, 消息会接收多次.

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


server
------
CLIENT LIST
^^^^^^^^^^^

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

server
======
database
--------
- databases are a form of namespacing: all the databases are anyway persisted
  together in the same RDB / AOF file.
  
- Different databases can have keys having the same name, and there are
  commands available like FLUSHDB, SWAPDB or RANDOMKEY that work on specific
  databases.

- Redis databases should mainly used in order to, if needed, separate different
  keys *belonging to the same application*, and *not* in order to use a single
  Redis instance for multiple unrelated applications.

- Redis Cluster supports only database 0.

persistence
===========
- AOF: append-only file.

replication
===========
- Replication is useful for read (but not write) scalability or data
  redundancy.

clustering
==========
- Redis Cluster supports only database 0.

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

- ``-n <dbnum>``. database number. default 0.

- ``-s <socket>``. server socket.

- ``-u <uri>``. a uri specifying connection parameters.::

    redis://[password@]host[:port][/db]

Client programming
==================
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
  During request, all non-bytes values are encoded into bytes before sending
  to server, using utf-8 by default.

- redis-py attempts to adhere to the official command syntax. with following
  exceptions:

  * SELECT, not implemented. Because SELECT command allows you to switch the
    database currently in use by the connection. This makes connections in
    connection pool stateful. Thus it breaks thread safety guarantee of Redis
    client.

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

- To prevent breaking thread safety, SELECT command is not implemented on
  client instances. To use multiple Redis databases within the same
  application, create a separate client instance (and possibly a separate
  connection pool) for each database.

class attributes
""""""""""""""""
- ``RESPONSE_CALLBACKS``. A dict, mapping command names to its response parsing
  callbacks.

class methods
"""""""""""""
- ``from_url(url, db=None, **kwargs)``. Create a Redis client from url schemes.
  This method calls directly ``ConnectionPool.from_url()`` class method to
  create a connection pool, and create a Redis client using the pool.
  The interpretation of ``url``, ``db``, available ``kwargs`` are all defered
  to ConnectionPool.

methods
"""""""
- ``pipeline(transaction=True, shard_hint=None)``. Create a Pipeline.
  ``transaction`` controls whether to wrap the pipeline with a transaction, so
  that the commands in pipeline are executed atomically.

- ``transaction(func, *watches, shard_hint=None, value_from_callable=False,
  watch_delay=None, **kwargs)``. a convenience method that running a pipeline
  inside a transaction, with optional watches. This handles retry on
  WatchError, using optimistic locking with CAS pattern. See also `client-side
  atomicity enforcement`_.

  * ``func`` 的唯一参数为一个 Pipeline instance. 在 func 中不执行
    ``Pipeline.execute()``. 若指定 ``*watches``, 在 func 中必须适时执行
    ``Pipeline.multi()`` 进入 pipeline execution mode. 否则, 不能使用
    ``Pipeilne.multi()``.

  * 若指定 ``*watches``, 这些 keys 会在执行 func 之前 WATCHed.

  * ``shard_hint`` same as Pipeline constructor.

  * ``value_from_callable`` 是否使用 func 的返回值作为返回值, 默认使用
    ``Pipeline.execute()`` 的返回值.

  * ``watch_delay`` 重试时的等待时间, 默认不等待.

- ``pubsub(**kwargs)``. Create a PubSub. passing client's connection pool.
  ``**kwargs`` are those accepted by PubSub constructor.

ConnectionPool
^^^^^^^^^^^^^^
- Connections to redis server is actually managed by a connection pool. A Redis
  client does not make connections directly.

- 由于一个 redis connection instance 本身不具有 thread safety, Connection pool
  维持一组连接, 记录空闲的连接与正在使用的连接, 每次只提供空闲的连接, 从而避免
  了 thread safety 的问题.

  这样, Redis client 等上层封装通过 connection pool 使用连接时, 本身具有了
  thread safety.

class methods
"""""""""""""
- ``from_url(url, db=None, decode_components=False, **kwargs)``. create a
  ConnectionPool from url.

  url schemes:

  * ``redis://[:password][@host][:6379][/db | ?db=N]``, TCP

  * ``rediss://[:password][@host][:6379][/db | ?db=N]``, SSL over TCP.

  * ``unix://[:password]@/path/to/socket.sock?db=N``, unix domain socket.

  db specified in url take precedence over separate parameter. default to 0.

  ``decode_components`` whether to decode url-encoded urls. This only applies
  to the ``hostname``, ``path``, and ``password`` components.

  urls also accepts any querystring parameters that are valid kwargs for the
  class constructor. They are merged with ``kwargs``, and passed to the class
  constructor. Special handling for the following kwargs when passed as query
  string parameters: ``socket_connect_timeout`` and ``socket_timeout`` are
  parsed as float; ``socket_keepalive`` and ``retry_on_timeout`` are parsed to
  boolean values that accept True/False, Yes/No values to indicate state;
  ``max_connections`` is parsed as int.

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

Pipeline
^^^^^^^^
- a subclass of Redis class, thus inheriting all its methods (e.g., all command
  methods).

thread safety
"""""""""""""
- No thread safety guarantee, each thread should use a separate Pipeline.

method chaining
"""""""""""""""
- For ease of use, all commands methods return the pipeline object itself,
  so that it's possible::

    pipe.set(...).get(...).execute()

reusing a pipeline
""""""""""""""""""
- A pipeline can be reused by:

  * calling ``reset()`` explicitly.

  * after calling ``execute()``, which calls ``reset()``.

  * after exiting from the context manager, which calls ``reset()``.

constructor
"""""""""""
- ``connection_pool``. where to get connection. A connection is retrieved
  from pool when executing pipeline, and released back to the pool after
  execution.

- ``response_callbacks``. how to parse response.

- ``transaction``. Whether to use transaction. If True, all commands executed
  within a pipeline are wrapped with MULTI and EXEC calls. This guarantees all
  commands executed in the pipeline will be executed atomically.

- ``shard_hint``.

methods
"""""""
- ``execute(raise_on_error=True)``. execute all the commands queued in current
  pipeline. Returns a list of responses, one for each command, in order.

- ``execute_command(*args, **kwargs)``. overriding parent class's method,
  queues commands to be executed in the ``self.command_stack``. 这样调用任何
  command methods 都不会立即执行, 而是缓存起来. Returns self, to support method
  chaining.

- ``__enter__()``. as a context manager. return self.

- ``__exit__(exc_type, exc_value, traceback)``. reset pipeline.

- ``multi()``. Mark all following commands in pipeline to be wrapped in a
  transaction explicitly. 注意这并不会立即发送 MULTI 至 server. 而是进入
  pipeline execution mode. 先 cache commands at client-side.

- ``watch(*names)``. WATCH names. mark pipeline in ``watching`` state.  after
  WATCHing, the pipeline is put into immediate execution mode until we tell it
  to start buffering commands again by ``multi()``.

PubSub
^^^^^^

thread safety
"""""""""""""
- No thread safety guarantee, each thread should use a separate PubSub.

message format
""""""""""""""
a dict with following keys:

- type. 'subscribe', 'unsubscribe', 'psubscribe', 'punsubscribe', 'message',
  'pmessage'

- channel. same as `message format`_ and `pmessage format` in `messaging`_.

- pattern. for pmessage, the pattern matched; otherwise None.

- data. same as `message format`_ and `pmessage format` in `messaging`_.

message handler
"""""""""""""""
If for a channel/pattern a callback is specified, the callback is called 
on receiving related messages, and the message itself is not returned.

strategies for reading messages
"""""""""""""""""""""""""""""""
- ``get_message()``. suitable for integrate into an existing event loop inside
  your application

- ``listen()``. If your application doesn't need to do anything else but
  receive and act on messages received from redis.

- ``run_in_thread()``. handle consuming message in a separate thread, and do
  other jobs in main thread.

operations
""""""""""
- PubSub can only receive messages, to publish message use Redis client.

- message consumption occupies a connection, but since Redis client uses
  connection pool internally, while the ``PubSub.connection`` is in pub/sub
  mode, the Redis client can still be used to issue other commands.

connection recovery
"""""""""""""""""""
PubSub objects remember what channels and patterns they are subscribed to. In
the event of a disconnection such as a network error or timeout, the PubSub
object will re-subscribe to all prior channels and patterns when reconnecting.

constructor
""""""""""""
- ``connection_pool``.

- ``shard_hint=None``

- ``ignore_subscribe_messages=False``. ignore subscribe/psubscribe,
  unsubscribe/punsubscribe messages.

methods
"""""""
- ``subscribe(*args, **kwargs)``. subscribe to channels, with optional
  callbacks. channels can be specified as a list, or positionals, or kwargs
  with callback function, for channel name that is invalid identifier, use
  ``**{"channel": callback}``.

  callback is passed with the received message as the only argument.

- ``psubscribe(*args, **kwargs)``. subscribe to patterns, with optional
  callbacks. others similar to ``subscribe()``.

- ``unsubscribe(*args)``. UNSUBSCRIBE from the specified channels or all
  channels.

- ``punsubscribe(*args)``. PUNSUBSCRIBE similar to ``unsubscribe()``.

- ``get_message(ignore_subscribe_messages=False, timeout=0)``. get message, if
  no message after optional timeout seconds, return None. 注意如果采用了
  callback, 即使有 message, 相应的 message 不会输出, 而是 None. 因此, None 不代
  表没有收到消息.
  
- ``listen()``. block and listen for messages forever. Returns a generator that
  yields the received and *unhandled* messages. If a message has already been
  handled by a callback, it's not returned.

- ``run_in_thread(sleep_time=0, daemon=False)``. run the message consuming loop
  in a thread. All channels/patterns must have a callback. Messages are just
  received and handled, but not returned in any way.
  ``sleep_time`` specify how long to wait for the message in the loop.
  ``daemon`` specify whether it's a daemon thread.

  Returns the thread and starts it automatically.

  Call ``Thread.stop()`` to stop the thread.

- ``close()``. When you're finished with a PubSub object, call this method to
  shutdown the connection and resetting all states.

design patterns
---------------
client-side atomicity enforcement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optimistic locking: Use pipeline with WATCH.

- watch the key you wanna modify before making changes.

- start a transactional pipeline to make changes.
  
  * If WatchError is raised, the key's value is changed between setting watch
    and making changes, therefore we has to retry.

  * Otherwise the change must have been successfully made.

.. code:: python

    with r.pipeline() as p:
      while True:
        try:
          p.watch("key")
          p.multi()
          # ... make changes
          p.execute()
        except WatchError:
          continue
        else:
          break

    # or

    r.transaction(func)

atomic counter
^^^^^^^^^^^^^^
- use INCR related commands

counter with atomic reset
^^^^^^^^^^^^^^^^^^^^^^^^^
- use GETSET to make atomic reset and get the old value at the same time,
  for statistics possibly.

rate limiter
^^^^^^^^^^^^
limit rate for every second, every IP

1. ::

    FUNCTION LIMIT_API_CALL(ip)
    ts = CURRENT_UNIX_TIME()
    keyname = ip+":"+ts
    current = GET(keyname)
    IF current != NULL AND current > 10 THEN
        ERROR "too many requests per second"
    ELSE
        MULTI
            INCR(keyname,1)
            EXPIRE(keyname,10)
        EXEC
        PERFORM_API_CALL()
    END

2. ::

    FUNCTION LIMIT_API_CALL(ip)
    current = LLEN(ip)
    IF current > 10 THEN
        ERROR "too many requests per second"
    ELSE
        IF EXISTS(ip) == FALSE
            MULTI
                RPUSH(ip,ip)
                EXPIRE(ip,1)
            EXEC
        ELSE
            RPUSHX(ip,ip)
        END
        PERFORM_API_CALL()
    END

listening to multiple queues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
blocking pop from multiple lists.

reliable message queues
^^^^^^^^^^^^^^^^^^^^^^^
Use list, with RPOPLPUSH/BRPOPLPUSH.

简单的 RPOP/BRPOP 等操作, 虽然能实现基本的 consume message 的操作, 但 not
reliable as messages can be lost, for example in the case there is a network
problem or if the consumer crashes just after the message is received but it is
still to process.

RPOPLPUSH (or BRPOPLPUSH for the blocking variant) offers a way to avoid this
problem: the consumer fetches the message and at the same time pushes it into a
processing list. It will use the LREM command in order to remove the message
from the processing list once the message has been processed.

对于 processing list 的处理, 可以有多种方式.

1. An additional client may monitor the processing list for items that remain
   there for too much time, and will push those timed out items into the queue
   again if needed.

2. On start, client RPOPLPUSH the elements off processing list to the original
   queue.

对于 blocking/non-blocking 操作的选择:

- 对于 dedicated message consumer/worker application, 应使用 blocking operation
  去接收 messages. 而不要使用 polling, 即不要使用以下方式: 使用 nonblocking
  operation 尝试获取消息, 若没有则等待一段时间再重试.
  
  polling 的缺点:
  
  * Redis and client application 需要做更多没有价值的操作.
  
  * Adds a unnecessary delay to the processing of items, when the message arrives
    after the application has just tried to consume any message. To make the
    delay smaller, we could wait less between calls, which amplifies the first
    problem.

- 对于 non-dedicated message consumer, 可以使用 non-blocking operation 与现有操作
  逻辑集成.

event notification
^^^^^^^^^^^^^^^^^^
Use list, with blocking pop for receiving event, and act accordingly.

capped list
^^^^^^^^^^^
- LPUSH/RPUSH + LTRIM.

circular list
^^^^^^^^^^^^^
Use RPOPLPUSH/BRPOPLPUSH with source and destination are the same list, a
client can visit all the elements of an N-elements list, one after the other,
in O(N) without transferring the full list from the server to the client using
a single LRANGE operation.

The above makes it very simple to implement a system where a set of items must
be processed by N workers continuously as fast as possible. An example is a
monitoring system that must check that a set of web sites are reachable, with
the smallest delay possible, using a number of parallel workers.

weighed random choice
^^^^^^^^^^^^^^^^^^^^^
Use sorted set and ZRANGEBYSCORE.

suppose a set of choices with weights::

  {a:1, b:2, c:3}

compute accumulative normalized score and add to a sorted set::

  SUM = ELEMENTS.TOTAL_WEIGHT
  SCORE = 0
  FOREACH ELE in ELEMENTS
      SCORE += ELE.weight / SUM
      ZADD KEY SCORE ELE
  END

select random element by::

  ZRANGEBYSCORE key rand() +inf LIMIT 0 1
  
references
==========
.. [SOMemcachedRedis] https://stackoverflow.com/questions/10558465/memcached-vs-redis
.. [SORedisConcurrency] `Redis is single-threaded, then how does it do concurrent I/O? <https://stackoverflow.com/questions/10489298/redis-is-single-threaded-then-how-does-it-do-concurrent-i-o>`
