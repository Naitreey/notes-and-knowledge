design problems
===============
- 一个大数据分析系统设计面临什么问题:
  
  * 单盘读写速度慢. 解决办法是多个盘并行读写.
  
  * hardware failure. As soon as you start using many pieces of hardware, the
    chance that one will fail is fairly high. 解决办法是 replication. RAID 是
    一种 replication 方法, 分布式存储采用块复制的方法.
  
  * most analysis tasks need to combine data in some way, and combine data read
    from any disks. MapReduce 提供了一种解决 combine 的方法.
  
  那么 hadoop 就是对这些问题的一个解决方案: Hadoop is a reliable, scalable
  platform for storage and analysis.

- 为什么不能用传统 RDBMS 进行大数据分析 (使用大量硬盘来放数据)?

  RDBMS 的设计目的要求能够频繁进行小比例数据 (相对于数据总量) 的随机读写更新.
  也就是说, RDBMS 对硬盘的基本数据访问操作是 seek (寻道). 硬盘的 Seek rate 是数
  据库读写效率的最根本瓶颈. 相应地, 以 B-tree 为基础数据结构的 RDBMS, 其更新速
  度以 seek rate 为上限.
  
  大数据系统的设计目的要求能够进行大比例数据的顺序读写, write once, read many
  times. 也就是说, RDBMS 对硬盘的基本数据访问操作是顺序读写. 硬盘的 Transfer
  rate 是大数据系统读写效率的最根本瓶颈.

  也就是说, RDBMS 和大数据系统的设计目的是不同的. 若使用 RDBMS 的 B-tree 结构来
  进行大数据所需的大量数据顺序读写, 将以 seek rate 为瓶颈来更新 B-tree, 这样就
  远比 transfer rate 慢. 与之相比, 使用 Sort/Merge 来顺序重建数据库的方式在这种
  大比例数据读写的场景下更合适.

  此外, RDBMS is designed to work with structured data that have a defined
  format, which maps to a database schema; While big data system is designed to
  work with semi-structured or unstructured data because it interpret the data
  at processing time.

  In RDBMS, data is normalized to retain its integrity and remove redundancy.
  For big data system, normalization makes reading a record a nonlocal
  operation, thus problematic. Also, big data system is good for processing
  data that are not normalized, e.g., log files.

- 为什么不用并行计算/高性能计算/Grid computing 等技术进行大数据分析? 与大数据分
  析的区别是什么?

  HPC 的基本方法是将 work 分布至集群的每个节点, 每个节点访问一个共享的存储, 即
  shared disk architecture. HPC 的特点是计算密集型, 共享的数据一般是 GB 级别即
  可.

  如果数据量更大, HPC 集群中节点与存储通信带宽将成为瓶颈, 导致计算节点一部分时
  间是闲置的. 而大数据分析就是需要 TB/PB 级别的数据量, 因此一个共享的数据存储
  是不合适的.

  big data system, 例如 hadoop, 通过 data locality, 来避免大量的数据传输, 从而
  数据访问效率非常高, 避免带宽成为瓶颈. 并且, hadoop 中具有根据网络拓扑对存储
  进行优化的机制, 从而更进一步地节省了带宽使用.

  HPC 的编程接口往往是比较底层的, Hadoop 中的编程抽象级别比较高. 省去程序员处理
  底层处理的麻烦, 对于程序员而言, data flow is implicit.

  HPC 中对部分节点计算出错的处理需要程序员自己去做, 在 hadoop 中, 集群自己去管
  理 failure 和重新分配任务等.

overview
========
- Hadoop is a framework for distributed storage and distributed processing of
  big data using the MapReduce programming model. The term "Hadoop" also refers
  to the larger ecosystem of projects, built on top of Hadoop.

- naming: Hadoop the name is meaningless, the yellow elephant is also
  meaningless.  According to Doug Cutting, it's the name his kid given to a
  stuffed yellow elephant. [OriginHadoop]_

- Hadoop was inspired by two Google papers:
 
  * Google File System (October 2003)

  * MapReduce: Simplified Data Processing on Large Clusters (December 2004)

- Hadoop was born out of Apache Nutch project, a web crawler/search engine.

- Some of the now separate Apache projects were born from Hadoop project,
  including HBase, Hive, Pig, Zookeeper, etc.

- originally created by Doug Cutting.

general architecture
====================
All components of Hadoop is designed with a fundamental assumption that
hardware failures is common and should be automatically handled by the
framework itself.

Hadoop splits files into large blocks and distributes them across nodes in a
cluster. It then transfers packaged code into nodes to process the data in
parallel.

components
----------
- Hadoop Common. libraries and utilities used by other Hadoop modules,
  includin FS and OS level abstractions.

- Hadoop Distributed File System (HDFS). A distributed file system that
  stores data for processing. It provides very high aggregate bandwidth
  across the cluster.

- Hadoop YARN. managing computing resources in clusters and scheduling user
  applications. YARN - Yet Another Resource Negotiator.

- Hadoop MapReduce. An implementation of MapReduce programming model for
  big data processing, based on YARN.

- Hadoop Ozone. An object store for Hadoop.

- Hadoop Submarine. A machine learning engine for Hadoop.

services
--------
In general, it is recommended that HDFS and YARN run as separate users. In the
majority of installations, HDFS processes execute as ‘hdfs’. YARN is typically
using the ‘yarn’ account, MapReduce processes use 'mapred'.

HDFS
^^^^
NameNode
""""""""
- Usually running on a dedicated node in the cluster.

- NameNode is a master service.

Secondary NameNode
""""""""""""""""""

DataNode
""""""""
- 对每个需要存储数据的节点都要运行 DataNode (存储节点).

- DataNode is a slave service.

YARN
^^^^
ResourceManager
"""""""""""""""
- Usually running on a dedicated node in the cluster.

- ResourceManager is a master service.

NodeManager
"""""""""""
- 对每个要执行计算任务的节点要运行 NodeManager (计算节点).

- NodeManager is a slave service.

WebAppProxy
"""""""""""

MapReduce
^^^^^^^^^
MapReduce Job History Server
""""""""""""""""""""""""""""

File systems
------------
- At storage layer, hadoop has a general-purpose filesystem abstration. It uses
  a plugin model, different FS implementation can be used. The default is HDFS.

- Location awareness of Hadoop compatible file systems.

  For effective scheduling of work, every Hadoop-compatible file system should
  provide location awareness, which is the name of the rack, specifically the
  network switch where a worker node is.
  
  Location-awareness makes the following possible:
  
  * Schedule map and reduce tasks on nodes which the data is located at or near
    (e.g., on the same rack/switch).
  
  * data replication is performed so that data redundancy is ensured across
    multiple racks.

- alternatvie file systems. When Hadoop MapReduce is used with an alternate
  file system, the NameNode, standby NameNode, and DataNode architecture of
  HDFS are replaced by the file-system-specific equivalents. The following
  alternative file systems are notable:

  * Amazon S3

  * Windows Azure Storage Blobs file system

  * IBM General Parallel File System

  * MapR's MapRFS.

  * FTP

HDFS
====
design goals
------------
- Highly fault-tolerant, designed to run on commodity hardware. Detection of
  faults and quick, automatic recovery from hardware failures.

- Streaming access to data set. Hadoop applications are not general purpose
  application that runs on general purpose file system. HDFS is designed more
  for batch processing rather than interactive use. The emphasis is on high
  throughput of data access rather than low latency of data access. POSIX
  imposes many hard requirements that are not needed for applications that are
  targeted for HDFS, therefore POSIX semantics in a few key areas has been
  traded to increase data throughput rates.

- Large data set. Tuned to support large files (大文件指的是: 10^3 MB, GB, TB
  量级的文件).  high aggregate data bandwidth and scale to hundreds of nodes in
  a single cluster. It should support tens of millions of files in a single
  instance.

- simple conherency model, write-once-read-many access model. In this access
  model, a file once created, written, and closed need not be changed except
  for appends and truncates. This assumption simplifies data coherency issues
  and enables high throughput data access.

  After a dataset is written to HDFS, various analyses are performed on that
  dataset over time. Each analysis will involve a large proportion of the
  dataset. So the time to read the whole dataset is more important than the
  latency in reading one record.

- It is often better to migrate the computation closer to where the data is
  located rather than moving the data to where the application is running.
  HDFS provides interfaces for applications to move themselves closer to where
  the data is located.

- Portability across heterogeneous hardware and software platforms. (JVM)


non design goals
----------------
- low-latency data access. In the range of 10^1 ms 量级, will not work well
  with HDFS. Use HBase for that.

- Lots of small files. The number of files a HDFS can store is limited by the
  amount of memory of NameNode. Each file, directory, block takes about
  150bytes.

- multiple writers, arbitrary file modifications. HDFS 中, 每个文件同时最多只能
  有一个 writer, 并且是 append-only 的. No support for multiple concurrent
  writes on the same file, or for modifications at arbitrary offsets in the
  file.

concepts
--------
blocks
^^^^^^
- A HDFS block 与硬盘的 block 在概念上是相同的. 即 block 是 HDFS 这个文件系统数
  据读写的单元. Block size 是数据读写的最小单元. File is broken into
  block-sized chunks which are stored as independent units (NameNode 保存每个
  block 的位置).

- Unlike a filesystem for a single disk, a file in HDFS that is smaller than a
  single block does not occupy a full block’s worth of underlying storage. 由于
  HDFS block size 很大, 这样的设计是为了避免大量浪费.

- 当前, HDFS 默认 block size 是 128MB.

- Why HDFS block size is so large? 这是为了尽量降低 seek time 在总的 disk
  access time 中所占的比例. 从而能够让数据读写速度以 transfer speed 为主导.  例
  如, 若希望 seek time 是 transfer time 的 1%, 当 transfer speed 为 128MB/s 且
  硬盘每次 seek 所用时间为 10ms 时, block size 至少要 128MB. (注意到每访问一个
  block 就要 seek 一次.)

- advantages of HDFS's block abstraction.

  * A file can be larger than any single disk in the cluster. 因为存储单元是
    block, 文件只需要通过 blocks 能抽象地重组起来即可.

  * making the unit of abstraction a block rather than a file simplifies the
    storage subsystem. The storage subsystem manages blocks of the fixed size,
    and it does not need to manage file metadata because it does not see files.

  * Blocks fit well with replication for providing fault tolerance and
    availability. 如果由于 disk corruption or node failure 一个一些 block
    replica 不再 available, 只需再次复制相关的 blocks 即可, 无需复制整个文件.
    此外, some applications may choose to set a high replication factor for the
    blocks in a popular file to spread the read load on the cluster

Architecture
------------
- Master-salve architecture. An HDFS cluster consists of
  
  * a single NameNode, a master server that manages the file system namespace
    and regulates access to files by clients.
  
  * a number of DataNodes, usually one per node in the cluster, which manage
    storage attached to the nodes that they run on. 

- File storage.
  
  * HDFS 创建一个 logical filesystem namespace, application data are stored in
    this logical filesystem.

  * a file is split into one or more blocks and these blocks are stored in a
    set of DataNodes.

NameNode
--------
functionalities
^^^^^^^^^^^^^^^
- maintains filesystem tree and metadata for all the files and directories in
  the tree.

- executes file system namespace operations like opening, closing, and
  renaming files and directories.

- Provides DataNode cluster membership by handling registrations, and periodic
  heart beats.

- manage the mapping of blocks to DataNodes.

- Supports block related operations such as create, delete, modify and get
  block location. (user data never flows through the NameNode.)

- Manages replica placement, block replication for under replicated blocks, and
  deletes blocks that are over replicated.

metadata
^^^^^^^^
- EditLog.

  * NameNode uses EditLog to record changes to file system metadata. EditLog is
    a persistent transaction log.
  
  * EditLog is stored as a file in NameNode's local host OS file system.

  * 需要 EditLog 是因为, even though it is efficient to read a FsImage, it is
    not efficient to make incremental edits directly to a FsImage.

- FsImage.

  * A file which stores the entire file system namespace, including the mapping
    of blocks to files and file system properties.

  * FsImage is stored as a file in NameNode's local host OS file system.

  * FsImage is also constantly kept in NameNode's memory for fast access.

- file blockmap.

  * a map from a file to its blocks and where those blocks are located.

  * blockmap is kept in NameNode's memory. It does not persist on NameNode's
    local disk, because this information is reconstructed from DataNode when
    the system starts.

- FsImage checkpoint. A FsImage checkpoint is triggered at NameNode startup and
  a configured interval. During the checkpoint, NameNode reads EditLog from
  disk, applies all the transactions from the EditLog to the in-memory
  representation of the FsImage, and flushes out this new version into a new
  FsImage on disk.  It can then truncate the old EditLog.

safemode
^^^^^^^^
NameNode 启动后首先进入 safemode, 此时不做 replication. NameNode 此时只接收
DataNode 的 heartbeat and blockreport. NameNode 根据 blockreport 检查 safely
replicated blocks 和 unsafe 的 blocks. After a configurable percentage of
safely replicated data blocks checks in with the NameNode, the NameNode exits
safemode. 开始 replicate 在 safemode 得到的那些尚未安全地复制的 blocks.

fault tolerance
^^^^^^^^^^^^^^^
- metadata fail-safety. Corruption of FsImage and/or EditLog can cause HDFS
  instance non-functional. There are several solutions to fail-safety of
  NameNode: backup metadata on NameNode, secondary NameNode, NameNode HA.

metadata replication on NameNode
""""""""""""""""""""""""""""""""
- NameNode can be configured to write its persistent state to multiple
  filesystems. These writes are synchronous and atomic. The usual configuration
  choice is to write to local disk as well as a remote NFS mount.
 
Run a secondary NameNode
""""""""""""""""""""""""
- Secondary NameNode is not a NameNode, its main role is to periodically merge
  the FsImage with the EditLog to prevent the edit log from becoming too large.

- It keeps a copy (a checkpoint) of the merged FsImage, which can be used in the
  event of NameNode failure. 但是由于这个同步是周期性的, 具有一定延迟, 所以如果
  NameNode 挂掉, 则会丢失最后一次同步至宕机时间内的数据.

- Secondary NameNode runs on a separate physical machine.

NameNode HA using QJM
"""""""""""""""""""""
- With metadata replication on NameNode or secondary NameNode, the NameNode is
  still a single point of failure (SPOF). 这导致以下问题:

  * In the case of an unplanned event such as a machine crash, the cluster
    would be unavailable until an operator restarted the NameNode.

  * Planned maintenance events such as software or hardware upgrades on the
    NameNode machine would result in windows of cluster downtime.
  
  HDFS HA 解决了这个问题.

- active NameNode and standby NameNode architecture.

  * 为了保证 FsImage 的高可用, standby NameNode 仍然要像 secondary NameNode 那
    样, 定期 checkpoint active NameNode's filesystem namespace, 即自己维护一份
    FsImage.

  * 为了保证 active NameNode 与 standby NameNode 的一致性, 两者需要能够访问相同
    的 EditLog 以保证两者都能实时更新 filesystem namespace, standby 不依赖于
    active 来获取 namespace 的变动. 这要求 EditLog 是放在共享的存储上的, 而不是
    放在 active 的本地硬盘.

  * DataNodes 的 blockreport and heartbeat 要发给 active 的同时也发给 standby,
    这样完全消除依赖性.

  * Clients must be configured to handle NameNode failover.

- Hadoop 3.0 以后可以有多个 standby. The minimum number of NameNodes for HA is
  two, but you can configure more. Its suggested to not exceed 5 - with a
  recommended 3 NameNodes - due to communication overheads.

- QJM: quorum journal manager 是一个分布式存储, 专门用于存储 EditLog, 以保证
  EditLog 是高可用的且是唯一的. active 和 standby 访问 QJM 以读写 EditLog, 保证
  了一致性.

  * QJM 本质上是一个专门用于分布式存储 EditLog 的 HDFS implementation. 需要将
    EditLog 的存储设计为分布式的, 是因为如果只是把 EditLog 从 active NN 共享出
    来至某个网络存储, 仍然具有存储本身的单点问题 (只是把单点从 NN 转移到了别处).

  * The QJM only allows one namenode to write to the edit log at one time.
    Otherwise, the namespace state would quickly diverge between the two,
    risking data loss or other incorrect results.
  
- QJM consists of a group of journal nodes (JN). Each edit to EditLog must be
  written to a majority of journal nodes. there can be at least 3 JNs, and
  overall number of JournalNodes must be odd. the system can tolerate at most
  (N - 1) / 2 failures and continue to function normally.

  QJM implementation does not use ZooKeeper. ZooKeeper is used for active
  NameNode election and failover.

- NameNode failover. Failover is managed by a failover controller. The default
  implementation uses ZooKeeper failover controller (ZKFC). Each NameNode runs
  a lightweight failover controller process whose job is to monitor its
  namenode for failures (using a simple heartbeating mechanism) and trigger a
  failover should a namenode fail.

  * graceful failover. A failover that is initiated by intention, e.g., for
    routine maintenance. In this, the failover controller arranges an orderly
    transition for both namenodes to switch roles.

  * ungraceful failover. A failover that is initiated in any event of active
    NameNode failure. In this situation, it's impossible to be sure that the
    failed NameNode has stopped running. Various fencing methods are employed
    to prevent the previously active NameNode from doing any damage and causing
    corruption.

  In the event of a failover, the Standby will ensure that it has read all of
  the edits from the JournalNodes before promoting itself to the Active state.

- Fencing. Fencing methods 是用于在 ungraceful failover 过程中可能需要强制移除
  previously active NameNode, 避免它不知道自己已经不是 active 了, 却仍然在
  serve client 的读操作. 相关的 fencing method 有:

  * ssh fencing.

  * shell fencing.

  * STONITH -- shoot the other node in the head. Use a specialized power
    distribution unit to forcibly power down the host machine.

- HDFS URI with active and standby NameNode. The HDFS URI uses a logical
  hostname that is mapped to a pair of namenode addresses (in the configuration
  file), and the client library tries each namenode address until the operation
  succeeds.

- configuration of NameNode HA using QJM.

  * NameNode machines. the machines on which you run the Active and Standby
    NameNodes should have equivalent hardware to each other.

  * JournalNode machines. the machines on which you run the Active and Standby
    NameNodes should have equivalent hardware to each other.

NameNode HA using NFS filer
"""""""""""""""""""""""""""
- QJM is prefered over NFS filer, because the former can ensure that there's
  only one NameNode and only the NameNode with the newer Epoch number to write
  to the EditLog at one time.

DataNode
--------
functionalities
^^^^^^^^^^^^^^^
- file blocks are stored in DataNodes. DataNode has no knowledge about HDFS
  files.

- serving read and write requests from clients directly.

- block creation, deletion, and replication upon instruction from the NameNode.

- blockreport. DataNode periodically scans through its local file system,
  generates a list of all HDFS data blocks, and sends this report to the
  NameNode. This also happens at DataNode startup time.

local storage scheme
^^^^^^^^^^^^^^^^^^^^
- each block of HDFS data is stored in a separate file in DataNode's local file
  system.

- Datanode uses a heuristic to determine the optimal number of files per
  directory and creates subdirectories appropriately.

fault tolerance
^^^^^^^^^^^^^^^
- heartbeats. Each DataNode sends a heartbeat message to NameNode periodically.
  The NameNode marks DataNodes without recent Heartbeats as dead and does not
  forward any new IO requests to them. DataNode death may cause the replication
  factor of some blocks to fall below their specified value. When this happens,
  NameNode initiates re-replication of those blocks.

- The necessity for re-replication may arise due to many reasons: a DataNode
  may become unavailable, a replica may become corrupted, a hard disk on a
  DataNode may fail, or the replication factor of a file may be increased.

data integrity
^^^^^^^^^^^^^^
- Data integrity. HDFS client software implements checksum checking on the
  contents of HDFS files. When a client creates an HDFS file, it computes a
  checksum of each block of the file and stores these checksums in a separate
  hidden file in the same HDFS namespace. When a client retrieves file contents
  it verifies that the data it received from each DataNode matches the checksum
  stored in the associated checksum file. If not, then the client can opt to
  retrieve that block from another DataNode that has a replica of that block.

block caching
^^^^^^^^^^^^^
- for frequently accessed files the blocks may be explicitly cached in the
  datanode’s memory, in an off-heap block cache.

- By default, a block is cached in one DataNode's memory, but it's configurable
  on a per-file basis.

- Users or applications instruct the namenode which files to cache (and for how
  long) by adding a cache directive to a cache pool. Cache pools are an
  administrative grouping for managing cache permissions and resource usage.

file system namespace
---------------------
- HDFS uses a traditional hierarchical file organization.

- HDFS supports traditional file/directory operations.

- hardlinks and symlinks are not supported.

- Files are write-once except for append and truncate. Strictly one writer at
  any time (per file).

- POSIX-like interface can be presented by client library.

data access
-----------
overview
^^^^^^^^
- Each file is split into blocks. Blocks are basic storage unit in HDFS.

- Blocks are replicated for fault tolerance.

- replication factor: the number of copies of a file. An application can
  specify the number of replicas of a file that should be maintained by HDFS.

- HDFS support file-level block size and replication factor. replication factor
  can be set at file creation time and can be changed later.

- NameNode manages replication. It periodically receives a Heartbeat and a
  Blockreport from each of the DataNodes in the cluster. Receipt of a Heartbeat
  implies that the DataNode is functioning properly. A Blockreport contains a
  list of all blocks on a DataNode.

replica placement (write)
^^^^^^^^^^^^^^^^^^^^^^^^^
- rack-aware replica placement policy.

- improves data reliability, availability, network bandwith utilization.

- For the common case, when the replication factor is three, HDFS’s placement
  policy is to put one replica on the local machine if the writer is on a
  datanode, otherwise on a random datanode in the same rack as that of the
  writer, another replica on a node in a different (remote) rack, and the last
  on a different node in the same remote rack.

- This policy cuts the inter-rack write traffic which generally improves write
  performance (最可靠的方式是将副本全部放在不同的机架上, 但跨机架的带宽一般是相
  对比同一个机架内节点之间慢, 这样 write pipeline 就会慢). The chance of rack
  failure is far less than that of node failure; this policy does not impact
  data reliability and availability guarantees. However, it does reduce the
  aggregate network bandwidth used when reading data since a block is placed in
  only two unique racks rather than three. (对于单个 client 读的情况, 无论怎么
  放, 都不影响读取速度, 因为每次只读一个 DataNode. 但如果有多个客户端同时读多个
  文件. 负载只能分布在两个机架上, 而不是三个机架, 这样总体能提供的读带宽就变小
  了.)

- If the replication factor is greater than 3, the placement of the 4th and
  following replicas are determined randomly.

- NameNode does not allow DataNodes to have multiple replicas of the same
  block, maximum number of replicas created is the total number of DataNodes at
  that time.

- How does HDFS write file? (See also [HDFSReplPaper]_, [hdfsReadAndWrite]_)

  1. HDFS client sends a request to the NameNode to create a new file in the
     filesystem's namespace.

  2. NameNode returns a list of DataNodes (using replication target choosing
     algorithm) to store data block according to replication factor.

  3. File data is first divided into blocks and then splits into packets. The
     list of DataNodes forms a pipeline.

  4. Packets are sent to the DataNode1 in the pipeline, to be stored and
     forwarded to next DataNode in the pipeline, and so forth.

  5. When the client has finished writing data, it calls close() which flushes
     all remaining packets to DataNode pipeline and wait for acknowledgment.

  6. Datanode sends the acknowledgment to client once required replicas are
     created.

  7. Client received acknowledgment and contacting the NameNode to signal that
     file is complete.

replica selection (read)
^^^^^^^^^^^^^^^^^^^^^^^^
- When client requested to read a file, NameNode tries to satisfy a read
  request from a replica that is closest to the reader (location proximity).

- how does HDFS read file? (See also [hdfsReadAndWrite]_)

  1. Client sends a request to the NameNode to open the file.

  2. NameNode provides the locations of the blocks for the first few blocks in
     the file. For each block, the namenode returns the addresses of the
     datanodes that have a copy of that block and datanode are sorted according
     to their proximity to the client.

  3. Client connects to the closest datanode for the first block in the file.
     When the reading of the block ends, it will close the connection to the
     datanode and then finds the best datanode for the next block.

  4. When the client has finished reading the data, it closes the reading
     stream.

HDFS federation
---------------
- HDFS federation 的目的是为了解决单机 NameNode 的内存大小成为 HDFS 可存储文件
  数目的瓶颈.

architecture
^^^^^^^^^^^^
- With HDFS federation, each NameNode manages a namespace volume, which is
  made up of the metadata for the namespace and a block pool containing all
  the blocks for the files in the namespace.

- Namespace volumes are independent of each other, which means NameNode do not
  communicate with one another, and furthermore the failure of one NameNode
  does not affect the availability of the namespaces managed by other
  namenodes.

- A Namespace Volume is a self-contained unit of management. When a
  Namenode/namespace is deleted, the corresponding block pool at the Datanodes
  is deleted. Each namespace volume is upgraded as a unit, during cluster
  upgrade.

- DataNodes register with each NameNode in the cluster and store blocks from
  multiple block pools. They also send periodic heartbeats and block reports
  to each NameNodes as usual.

benefits
^^^^^^^^
- Namespace horizontal scalability. 大量的文件如单机内存无法承受, 可多台机器
  来存储.

- Performance. File system throughput is not limited by a single Namenode.
  Adding more Namenodes to the cluster scales the file system read/write
  throughput.

- Isolation. By using multiple Namenodes, different categories of applications
  and users can be isolated to different namespaces.

configuration
^^^^^^^^^^^^^

HDFS clients
------------
multiple ways to access hdfs data:

* FileSystem Java API

* C wrapper for the said API

* CLI: FS shell.

* REST API.

* NFS gateway.

YARN
====
- YARN is a cluster resource management system, which allows any distributed
  program, not just MapReduce, to run on data in a Hadoop cluster.

Architecture
------------


NodeManager
-----------
Monitoring health
^^^^^^^^^^^^^^^^^
- NodeManager can periodically run a script to determine if the managed node is
  healthy or not.

- Any check is allowed in the script.

- If the script detects the node to be in an unhealthy state, it must print a
  line to standard output beginning with the string ERROR. The NodeManager
  spawns the script and checks its output. If ERROR, the node’s status is
  reported as unhealthy and the node is black-listed by the ResourceManager.
  No further tasks will be assigned to this node. When a subsequent health
  check does not contain ERROR in output, the node is healthy again and removed
  from blacklist.

MapReduce
=========
overview
--------
- MapReduce is a batch processing system, which is like a brute-force approach.
  MapReduce provides capability that the entire dataset can be processed for
  each query. Questions that took too long to get answered before can now be
  answered.

- MapReduce 的适用场景:

  * suitable for batch processing, offline analysis, problems that need to
    analyze the whole dataset in a batch fashion.

  * suitable for applications where data is written once and read many times.

  * not suitable for interactive analysis.

- MapReduce vs RDBMS.

  * RDBMS 适合 point queries or updates, where dataset has been indexed to
    deliver low-latency retrieval and update times for a small portion of data.

  * RDBMS 适合 dataset that are continually updated.

  * MapReduce 适合 problems that need to analyze the whole or large portion of
    data set in a batch fashion.

  * MapReduce 适合 dataset that is written once and read many times.

  * Data size. RDBMS: GB level. MapReduce: PB level.

  * Access. RDBMS: interactive and batch. MapReduce: batch.

  * Transaction. RDBMS: ACID. MapReduce: None.

  * Structure. RDBMS: schema on write. MapReduce: schema on read, it's designed
    to interpret the data at processing time.

  * Integrity. RDBMS: High. MapReduce: Low.

  * Scaling. RDBMS: nonlinear. MapReduce: linear. If cluster size is doubled,
    it's capable of processing a double size of data at the same speed as does
    previously.

Mechanism
---------
job and task
^^^^^^^^^^^^
Job. A MapReduce job is a unit of work that a client wants to be performed.  It
consists of input data, the MapReduce program, and configuration.

Task. Hadoop runs a job by dividing it into tasks. There are map tasks and
reduce tasks. Tasks are scheduled using YARN. If a task fails, it's rescheduled
automatically on a different node in the cluster.

split and record
^^^^^^^^^^^^^^^^
Hadoop divides the input to a MapReduce job into fixed-size pieces called input
splits or splits. Hadoop create one map task for each split, which runs the
user defined map function for each record in the split.  注意到, 在一个 map
task 中, map function is normally called many times, one time for each record
of a split. (Java API 还支持 pull API, 此时, 由 map function 决定要如何处理
input.)

The size of a split shouldn't be too big or too small.

* When the splits are small, the processing is better load balanced, since a
  faster machine will be able to process more splits over the course of the job
  than a slower machine. Also, if a task failed, the impact is more limited, we
  can restart the same small portion of job on another node. Overall, the
  quality of load balancing increases as the splits become more fine grained.

* WHen the splits are too small, the overhead of managing splits and map task
  creation begins to dominate the total job execution time.

For most jobs, a good split size tends to be the size of an HDFS block or
smaller, which is 128MB by default. split 不该比 block 大的原因是, 若是这样,
一个 map 的输入 split 必然会跨越 2 个以上的 blocks, 这样有很大可能需要从另一个
节点获取至少一个 block.

注意一个 split 的实际 size 还取决于文件的 size. 如果文件本身比配置的 split max
size 小, 则 split 只能达到文件那么大. 这也是为什么推荐尽量使用大文件的原因. 即
太多小文件会创建更多的 map tasks, overhead of map task creation 对执行时间的影
响逐渐增大.

data locality optimization
^^^^^^^^^^^^^^^^^^^^^^^^^^
Data locality optimization. Hadoop 尽量保证在一个 map task 所需数据所在的节点上
运行 map task. 这样可以尽量节省带宽. 若这一点不能保证 (因为一个 split 的所有
blocks 所在的节点都在运行 map task), 则会 fallback 至同一个 rack 上的其他空闲节
点 (inter-node transfer). 若这样的机器也不能找到, 则 fallback 至不同 rack 上的
空闲节点 (inter-rack transfer).

map output handling
^^^^^^^^^^^^^^^^^^^
Map tasks write their output to the local disk, not to HDFS. Map output is
intermediate output: it’s processed by reduce tasks to produce the final
output, and once the job is complete, the map output can be thrown away. So,
storing it in HDFS with replication would be overkill. All outputs of a map
task (multiple key value pairs) are sorted, partitioned then transferred to the
reduce tasks.

partition
^^^^^^^^^
每个 map task 将所有输出的 key value pairs 分成多组 (partition), 组的数目与
reduce task 的数目相同. Partition 时, 保证对于每个 key 的所有 key value pairs
都位于一个 partition 中 (从而 reduce 时才能是正确的结果). Partition function
可以由用户指定, 默认的 partition function 将 key hash 至 hash buckets, 对每个
bucket 作为一个 partition.

reduce task
^^^^^^^^^^^
Reduce tasks normally don't have the property of data locality. The input to a
single reduce task often comes from all map tasks' output. 来自各个 map task 的
sorted key value pairs are merged into pairs of key and a list of values, then
passed to the user defined reduce function. The output of reduce is normally
stored in HDFS for reliability. For each HDFS block of the reduce output, the
first replica is stored on the local node, with other replicas being stored on
off-rack nodes for reliability.

一个 MapReduce job 可以没有 reduce 阶段. 这样的任务具有完全并行执行的特点.
即不存在聚合步骤, 完全是并行 map 处理 (filter, extract, transform, etc.).

shuffle
^^^^^^^
The shuffle. map task 对输出进行 partition, 传输至 reduce tasks, 以及 reduce
task 对输入进行 merge 这些流程总称为 shuffle.

combiner function
^^^^^^^^^^^^^^^^^
Combiner function 的意义在于, 对 map task 的输出预先 locally aggregate 一次, 从
而降低 shuffle 阶段的网络传输量, 从而避免带宽成为 MapReduce job 的执行效率瓶颈.
Combiner function runs on the map output, its output forms the final output of
mapper node, feeded to reduce task.

Hadoop does not provide a guarantee of how many times it will call it for a
particular map output record. In other words, calling the combiner function
zero, one, or many times should produce the same output from the reducer.
因此, combiner function 作为一个算符必须具有 commutativity and associativity.

map and reduce input/output
^^^^^^^^^^^^^^^^^^^^^^^^^^^
map and reduce phases have key-value pairs as input and output. Programmer
defines what the input/output is for each phase, and defines the map and reduce
function to operate on the input and produce the output.

- map phase: 由用户提供.

  * 输入: 原始数据. key: offset. value: 数据

  * 输出: 关键信息 key value pairs.

  * 操作: 对原始数据进行过滤和关键信息提取等操作.

- shuffle phase: 由 Hadoop 完成.

  * 输入: map phase 输出的关键信息 key value pairs.

  * 输出: key 是一组 unique keys, 对应于 map phase 输出的 keys. 对于每个 key,
    其值是 map phase 输出的这个 key 对应的所有可能 value 值的列表.

  * 操作: 对 key 进行排序, 对 values 按 key 进行分组 (grouping).

- reduce phase: 由用户提供.

  * 输入: shuffle phase 输出的 key value pairs. 其中 value 为 a list of values
    corresponding to the key.

  * 输出: key 是一组 unique keys, 对于每个 key, 其值是对 value list 的聚合结果.
    结果最终写入 HDFS, 对于每个 reducer, 生成一个 ``part-r-NNNN`` 文件.

  * 操作: 对于每个 key, 对它的 a list of values 进行所需的分析和聚合操作.

Debugging
---------
- mapreduce job's log output provides many useful information.

  * job id

  * Counters section 有助于确认 mapreduce job 的执行情况是否与预期一致.

Java API
--------
- packages.
 
  * org.apache.hadoop.io package 提供了一些 Hadoop 定义的 basic types,
    optimized for network serialization.

  * org.apache.hadoop.mapreduce 即 Apache Hadoop MapReduce Core, 是 mapreduce
    的 client library.

- ``Job`` is the specification for a mapreduce job.

  methods:

  * ``setJarByClass()``

  * ``setJobName()``

  * ``setMapperClass()``

  * ``setReducerClass()``

  * ``setOutputKeyClass()``

  * ``setOutputValueClass()``

  * ``waitForCompletion()``

- ``Mapper`` generic type. four type parameters:

  * type of input key
  
  * type of input value
  
  * type of output key
  
  * type of output value
  
  methods:
  
  * ``map(LongWritable key, Text value, Context context)`` abstract method.

- ``Reducer`` generic type.

  * type of input key, matching type of Mapper output key
  
  * type of input value, matching type of Mapper output value
  
  * type of output key
  
  * type of output value

Tools
=====
Hadoop Streaming
----------------
- tool path: ``$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar``

- Hadoop streaming is a utility that allows MapReduce jobs to be created and
  run with any executables/scripts as mapper or reducer.

- 称这种处理为 streaming, 是因为以 Unix standard streams (stdin/stdout) 作为
  hadoop 与 mapper/reducer 程序的交互界面. 就像数据了用户提供的 mapper 和
  reducer 程序. 注意与实时的流处理区分开来.

- Hadoop streaming 由于是通过 standard stream 传输输入输出, it's naturally
  suited for text processing.

Mechanism
^^^^^^^^^
- mapper.
 
  * Each mapper task will launch the executable as a separate process when the
    mapper is initialized. As the mapper task runs, it converts its inputs into
    lines and feed the lines to the stdin of the process. In the meantime, the
    mapper collects the line oriented outputs from the stdout of the process
    and converts each line into a key/value pair, which is collected as the
    output of the mapper.

  * Input for the mapper. By default, use TextInputFormat. the offset from the
    beginning of the file is key and the line will be the value. But key is
    discarded for some *unknown* reason.

  * Output from the mapper. By default, the prefix of a line up to the first tab
    character is the key and the rest of the line will be the value. If there
    is no tab character in the line, then entire line is considered as key and
    the value is null.

- reducer.

  * When an executable is specified for reducers, each reducer task will launch
    the executable as a separate process then the reducer is initialized. As
    the reducer task runs, it converts its input key/values pairs into lines
    and feeds the lines to the stdin of the process. In the meantime, the
    reducer collects the line oriented outputs from the stdout of the process,
    converts each line into a key/value pair, which is collected as the output
    of the reducer.

  * Input for the reducer. By default, the prefix of a line up to the first tab
    character is the key and the rest of the line is the value. 注意这与 Java
    API 的 reduce method 的输入是不同的. 在这里, 并没有一次输入一个 Iterable of
    values of a key. 对于一个 key 的多个 values, 是一行一行输入的, 即需要通过前
    后 key 值的异同, 来判断何时对一组 key 的 values 值的聚合结束. (Shuffle 保证
    keys are ordered.)

  * Output from the reducer. ditto.

- 注意 mapper and reducer program 应该在从 stdin 遍历读取多个数据. 这与 Java
  API 中一条一条操作是不同的. 这是 pull API. 对于每个 map task 和 reduce task,
  启动一个 mapper/reducer process.

- By default, streaming tasks exiting with non-zero status are considered to be
  failed tasks. Can be customized by ``stream.non.zero.exit.is.failure``.

packaging files during job submission
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- any executable can be mapper, reducer, or other components. 但是它们必须提供
  给集群, 通过 ``-files`` generic option.

specify number of reducers
^^^^^^^^^^^^^^^^^^^^^^^^^^
Use ``-D mapreduce.job.reduces=N``. for map-only jobs, use N=0.

customize how lines are split into key/value pairs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
customize field separators and nth separator char as the separator between
key and value:

- ``-D stream.map.input.field.separator=SEP``

- ``-D stream.map.output.field.separator=SEP``

- ``-D stream.num.map.output.key.fields=NUM``

- ``-D stream.reduce.input.field.separator=SEP``

- ``-D stream.reduce.output.field.separator=SEP``

- ``-D stream.num.reduce.output.fields=NUM``

CLI
^^^
两种调用方式

.. code:: sh

  yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-X.X.X.jar \
    [genericOptions] [commandOptions]
  $HADOOP_HOME/bin/mapred streaming \
    [genericOptions] [commandOptions]

- generic options

  * ``-conf <config-file>``

  * ``-D property=value``. specify/override configs of mapred-site.xml.

  * ``-fs host:port or local``. namenode to connect to.

  * ``-files file1,fil2,...``. comma-separated files to be made available to
    jobs. Each file is a path to the local file or archive.

  * ``-libjars file1,file2,...``. comma-separated jar files to include in the
    classpath. Each jar is URI to the file or archive that you have already
    uploaded to HDFS.

  * ``-archives archive1,...``. archives to be unarchived on the compute
    machines.

- streaming options

  * ``-input <file-or-directory>``. input for mapper.

  * ``-output <directory>``. output location for reducer.

  * ``-mapper <executable-path-or-java-class-name>``. mapper used for map
    stage. default is org.apache.hadoop.mapred.lib.IdentityMapper. 对于
    executable path, 直接使用 ``-files`` 中文件的 filename (不包含 parent
    directory).

  * ``-reducer <executable-path-or-java-class-name>``. reducer used for reduce
    stage. default is org.apache.hadoop.mapred.lib.IdentityMapper. 路径同上.

  * ``-inputformat <java-class-name>``. Input format class to parse input to
    mapper. The class you supply for the input format should return key/value
    pairs of Text class. the TextInputFormat is used as the default. Since the
    TextInputFormat returns keys of LongWritable class, which are actually not
    part of the input data, the keys will be discarded; only the values will be
    piped to the streaming mapper.

  * ``-outputformat <java-class-name>``. Output format class to parse output
    from reducer. The class you supply for the output format is expected to
    take key/value pairs of Text class. the TextOutputFormat is used as the
    default.

  * ``-partitioner <java-class-name>``. java class for partition function.

  * ``-combiner <executable-path-or-java-class-name>``. combiner function can
    be a java class or executable program. 路径同上.

  * ``-cmdenv key=val`` environ to be passed to streaming cmds.

  * ``-verbose``

  * ``-lazyOutput``

  * ``-numReduceTasks <n>``. the number of reduce tasks.

  * ``-mapdebug <executable-path>``. script to call when map task failed.

  * ``-reducedebug <executable-path>``. script to call when reduce task failed.


Dumbo
-----
- A more pythonic API to code MapReduce in Python.

configuration
=============
environment configuration
-------------------------
- setting site-specific customization of the Hadoop daemons' process environment.

  * /etc/hadoop/hadoop-env.sh

  * /etc/hadoop/yarn-env.sh

  * /etc/hadoop/httpfs-env.sh
   
  * /etc/hadoop/kms-env.sh
   
  * /etc/hadoop/mapred-env.sh

hadoop-env
^^^^^^^^^^
generic
""""""""
- JAVA_HOME. required.

- HADOOP_HOME. 建议在 system-wide shell environment configuration 中设置, 例如
  /etc/profile.d/hadoop.sh. hadoop 的安装路径, 例如 /usr/lib/hadoop.

JVM options
""""""""""""
- HADOOP_OPTS. Java runtime options for all Hadoop commands.

- HDFS_NAMENODE_OPTS

- HDFS_SECONDARYNAMENODE_OPTS

- HDFS_DATANODE_OPTS

memory
""""""
- HADOOP_HEAPSIZE_MIN

- HADOOP_HEAPSIZE_MAX

file path
""""""""""
- HADOOP_CONF_DIR. 建议在 system-wide shell environment configuration 中设置,
  例如 /etc/profile.d/hadoop.sh.

- HADOOP_LOG_DIR

- HADOOP_PID_DIR

yarn-env
^^^^^^^^
JVM options
""""""""""""
- YARN_RESOURCEMANAGER_OPTS

- YARN_NODEMANAGER_OPTS

- YARN_PROXYSERVER_OPTS

- YARN_TIMELINESERVER_OPTS

- YARN_TIMELINEREADER_OPTS

memory
""""""
- YARN_RESOURCEMANAGER_HEAPSIZE

- YARN_NODEMANAGER_HEAPSIZE

- YARN_PROXYSERVER_HEAPSIZE

- YARN_TIMELINE_HEAPSIZE

mapred-env
^^^^^^^^^^
JVM options
""""""""""""
- MAPRED_HISTORYSERVER_OPTS

memory
""""""
- HADOOP_JOB_HISTORYSERVER_HEAPSIZE

daemon configuration
--------------------
- read-only default configuration:

  * core-default.xml

  * hdfs-default.xml

  * yarn-default.xml

  * mapred-default.xml

- site-specific configuration:

  * /etc/hadoop/core-site.xml
   
  * /etc/hadoop/hdfs-site.xml
   
  * /etc/hadoop/yarn-site.xml
    
  * /etc/hadoop/mapred-site.xml

core-site.xml
^^^^^^^^^^^^^
- fs.defaultFS

- io.file.buffer.size

hdfs-site.xml
^^^^^^^^^^^^^
NameNode
""""""""
- dfs.namenode.name.dir

- dfs.hosts

- dfs.hosts.exclude

- dfs.blocksize

- dfs.namenode.handler.count

- dfs.namenode.checkpoint.period.

- dfs.namenode.checkpoint.txns.

DataNode
""""""""
- dfs.datanode.data.dir

yarn-site.xml
^^^^^^^^^^^^^
ResourceManager
""""""""""""""""
- yarn.acl.enable

- yarn.admin.acl

- yarn.log-aggregation-enable

- yarn.resourcemanager.address

- yarn.resourcemanager.scheduler.address

- yarn.resourcemanager.resource-tracker.address

- yarn.resourcemanager.admin.address

- yarn.resourcemanager.webapp.address

- yarn.resourcemanager.hostname

- yarn.resourcemanager.scheduler.class

- yarn.scheduler.minimum-allocation-mb

- yarn.scheduler.maximum-allocation-mb

- yarn.resourcemanager.nodes.include-path 
 
- yarn.resourcemanager.nodes.exclude-path

NodeManager
""""""""""""
- yarn.acl.enable

- yarn.admin.acl

- yarn.log-aggregation-enable

- yarn.nodemanager.resource.memory-mb

- yarn.nodemanager.vmem-pmem-ratio

- yarn.nodemanager.local-dirs

- yarn.nodemanager.log-dirs

- yarn.nodemanager.log.retain-seconds

- yarn.nodemanager.remote-app-log-dir

- yarn.nodemanager.remote-app-log-dir-suffix

- yarn.nodemanager.aux-services

- yarn.nodemanager.env-whitelist

- yarn.nodemanager.health-checker.script.path

- yarn.nodemanager.health-checker.script.opts

- yarn.nodemanager.health-checker.interval-ms

- yarn.nodemanager.health-checker.script.timeout-ms

History Server
""""""""""""""
- yarn.log-aggregation.retain-seconds

- yarn.log-aggregation.retain-check-interval-seconds

mapred-site.xml
^^^^^^^^^^^^^^^
MapReduce Applications
""""""""""""""""""""""
- mapreduce.framework.name

- mapreduce.map.memory.mb

- mapreduce.map.java.opts

- mapreduce.reduce.memory.mb

- mapreduce.reduce.java.opts

- mapreduce.task.io.sort.mb

- mapreduce.task.io.sort.factor

- mapreduce.reduce.shuffle.parallelcopies

MapReduce Job History Server
""""""""""""""""""""""""""""
- mapreduce.jobhistory.address

- mapreduce.jobhistory.webapp.address

- mapreduce.jobhistory.intermediate-done-dir

- mapreduce.jobhistory.done-dir

workers flie
------------
- /etc/hadoop/workers

- worker's hostname/ip address, one per line.

- SSH trusts must be established for accounts used to run hadoop.

CLI
===
hdfs
----
admin commands
^^^^^^^^^^^^^^
dfsadmin
""""""""
::

  hdfs dfsadmin -report

client commands
^^^^^^^^^^^^^^^
dfs
""""

daemon commands
^^^^^^^^^^^^^^^
namenode
""""""""
::

  hdfs namenode -format <cluster_name>
  hdfs [--daemon (start|status|stop)] namenode

datanode
""""""""
::

  hdfs [--daemon (start|status|stop)] datanode

yarn
----
client commands
^^^^^^^^^^^^^^^
jar
""""
::

  yarn jar <jar-path> [mainClass] [arg ...]

daemon commands
^^^^^^^^^^^^^^^
resourcemanager
""""""""""""""""
::

  yarn [--daemon (start|status|stop)] resourcemanager

nodemanager
""""""""""""
::

  yarn [--daemon (start|status|stop)] nodemanager

proxyserver
""""""""""""
::

  yarn [--daemon (start|status|stop)] proxyserver

mapred
------
historyserver
^^^^^^^^^^^^^
::

  mapred [--daemon (start|status|stop)] historyserver

processing patterns
===================
- batch processing. i.e., MapReduce.

- interactive SQL. using a distributed query engine, like Impala (daemon), Hive
  on Tez (container reuse).

- iterative processing. hold intermediate working set in memory to improve
  efficiency, like Spark.

- stream processing. like Storm, Spark Streaming, Samza. real-time, distirbuted
  computations on unbound streams of data and emit results to HDFS or external
  systems.

- Search. Solr can run on Hadoop, indexing documents as they are added to HDFS,
  and serving queries from indexes stored in HDFS.

distributors
============
See also [distroToChoose]_.

- Cloudera -- Cloudera Data Hub (CDH)

  * installation is fast

  * Impala

- Hortonworks -- Hortonworks Data Platform (HDP)

  * open source

  * more options

- MapR -- MapR Data Platform (MDP)

  * easier and faster than the other two.

  * MapRFS and MapRDB.

about containerization
======================
- Hadoop 在部署时一般成为一个专用的计算集群, 完全占据集群内所有硬件资源,
  所以没有容器化的需要.

references
==========
.. [OriginHadoop] `Origin of the Name Hadoop <http://www.balasubramanyamlanka.com/origin-of-the-name-hadoop/>`_
.. [distroToChoose] `What distribution should I choose <https://www.quora.com/What-distribution-should-I-choose-Cloudera-Hortonworks-or-MapR-I-will-need-to-do-some-stream-processing-from-social-networks-and-real-time-too-I%E2%80%99m-thinking-of-using-Apache-Storm-rather-than-Spark-with-Hortonworks-Is-that-a-good-approach>`_.
.. [hdfsReadAndWrite] `Hadoop HDFS Data Read and Write Operations <https://data-flair.training/blogs/hadoop-hdfs-data-read-and-write-operations/>`_
.. [HDFSReplPaper] `An Efficient Replication Technique for Hadoop Distributed File System <https://pdfs.semanticscholar.org/dffe/5bfcf3e9300190002aa8456f9b2170507e33.pdf>`_

questions
=========
- what's WebAppProxy?

- content of each configuration file

- content of ``*-env.sh``

- To configure the Hadoop cluster you will need to configure the environment in
  which the Hadoop daemons execute as well as the configuration parameters for
  the Hadoop daemons?

- how does HDFS know where the write is? on datanode or on the same rack?
