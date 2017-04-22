- 3.0+ 默认的 storage engine 是 WiredTiger, 之前是 MMAPv1. 前者的好处是
  支持 document level 的 concurrent read write, 后者支持 concurrent read
  in one collection, 但是在 collection level 对 write 有锁.

- WiredTiger 默认的 internal cache 使用 50% * RAM - 1GB, 但是这意味着什么呢?
  没看出来它占用了很多内存啊??
