overview
========
- MapReduce is a programming model for processing big data set on a cluster.

- A MapReduce program contains:

  * a map procedure -- filtering and sorting

  * a reduce procedure -- aggregation

- A MapReduce framework orchestrates the MapReduce processing by marshalling
  the distributed servers, running the various tasks in parallel, managing all
  communications and data transfers between the various parts of the system,
  and providing for redundancy and fault tolerance.

  用户程序只需实现 map 和 reduce 两个函数.

operations
==========
map
---
- Each worker node applies the map function to the local data, and writes the
  output to a temporary storage. A master node ensures that only one copy of
  redundant input data is processed.

- 从整体上看, 就是把一个函数在每个节点上应用了一遍, 所以是一个分布式的 map,
  在每个节点上生成一个值域的结果. 传入 reduce 阶段.

shuffle
-------
- worker nodes redistribute data based on the output keys (produced by the map
  function), such that all data belonging to one key is located on the same
  worker node.

- 由于 shuffle 需要在节点之间移动数据, 这是整个 MapReduce 算法效率的决定因素.

- shuffle 需要某种网络机制在 mapper and reducer 之间建立数据连接通信, 这可以是
  一个分布式存储系统, direct streaming from mappers to reducers, or for the
  mapping processors to serve up their results to reducers that query them.

reduce
------
- worker nodes now process each group of output data, per key, in parallel.

performance considerations
==========================
- MapReduce 算法只有在面对极大的数据量时才能体现出价值.
  
  A single-threaded implementation of MapReduce will usually not be faster than
  a traditional (non-MapReduce) implementation.
  
  MapReduce can be applied to significantly larger datasets than a single
  "commodity" server can handle. Any gains are usually only seen with
  multi-threaded implementations on multi-processor hardware. 

- For processes that complete quickly, and where the data fits into main memory
  of a single machine or a small cluster, using a MapReduce framework usually
  is not effective. Since these frameworks are designed to recover from the
  loss of whole nodes during the computation, they write interim results to
  distributed storage. This crash recovery is expensive, and only pays off when
  the computation involves many computers and a long runtime of the
  computation. A task that completes in seconds can just be restarted in the
  case of an error, and the likelihood of at least one machine failing grows
  quickly with the cluster size. On such problems, implementations keeping all
  data in memory and simply restarting a computation on node failures or —when
  the data is small enough— non-distributed solutions will often be faster than
  a MapReduce system.
  
- Optimized and distributed shuffle operation and fault tolerance is key to a
  MapReduce framework.

- When designing a MapReduce algorithm, the author needs to choose a good
  tradeoff between the computation and the communication costs. Communication
  cost often dominates the computation cost, and many MapReduce implementations
  are designed to write all communication to distributed storage for crash
  recovery.

- Reducing includes sorting (grouping of the keys) which has nonlinear
  complexity. Hence, small partition sizes reduce sorting time.

reliability
===========
- Each node is expected to report back periodically with completed work and
  status updates. If a node falls silent for longer than that interval, the
  master node records the node as dead and sends out the node's assigned work
  to other nodes.
