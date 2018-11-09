free
====

overview
--------
show memory info, by parsing ``/proc/meminfo``.

fields
------

* total.

* used. 除去 buffer/cache 之外实际使用的内存. total - free - buffers - cache

* free. unused memory.

* shared.

* buffers. kernel buffers.

* cache. page cache and slabs.

* buff/cache.

* available. 这个值表示 how much memory is available for starting new
  applications, without swapping. this field takes into account page cache and
  also that not all reclaimable memory slabs will be reclaimed due to items
  being in use. 这个值可能会比 total - used 小一点.

references
==========
- free(1)
