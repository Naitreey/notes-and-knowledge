definition
==========
memcached is a distributed memory-caching system.

architecture
============
Memcached's APIs provide a very large hash table distributed
across multiple machines. When the table is full, subsequent inserts cause
older data to be purged in least recently used (LRU) order.

Each client knows all servers; the servers do not communicate with each other.
If a client wishes to set or read the value corresponding to a certain key, the
client's library first computes a hash of the key to determine which server to
use. This gives a simple form of sharding and scalable shared-nothing
architecture across the servers. (也就是说, 缓存的数据没有备份, 每个 memcached
server 保存的数据都是 unique 的. 这样, 最大程度利用了各机器的内存总量.) The
server computes a second hash of the key to determine where to store or read
the corresponding value.
