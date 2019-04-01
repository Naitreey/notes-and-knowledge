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

Hadoop File systems
===================
overview
--------
- At storage layer, hadoop has a general-purpose filesystem abstration.
  Different FS implementation exists. By default Hadoop uses HDFS
  implementation.

  Abstract client interface to hadoop compatible filesystems:

  .. code:: java

    org.apache.hadoop.fs.FileSystem

- Location awareness of Hadoop compatible file systems.

  For effective scheduling of work, every Hadoop-compatible file system should
  provide location awareness, which is the name of the rack, specifically the
  network switch where a worker node is.
  
  Location-awareness makes the following possible:
  
  * Schedule map and reduce tasks on nodes which the data is located at or near
    (e.g., on the same rack/switch). This is data locality optimization.
  
  * data replication is performed so that data redundancy is ensured across
    multiple racks.

- 注意到 NameNode, DataNode, etc. concepts 是 HDFS 中才存在的实体. When Hadoop
  is used with an alternate file system, architecture of HDFS are replaced by
  the file-system-specific equivalents.

implementations
---------------
Local
^^^^^
- URI scheme: file.

- Java implementation:
 
  with checksum

  .. code:: java

    org.apache.hadoop.fs.LocalFileSystem

  without checksum

  .. code:: java

    org.apache.hadoop.fs.RawLocalFileSystem

- use local disk, with/without client-side checksum, for hadoop's
  standalone mode. 

HDFS
^^^^
- URI scheme: hdfs

- Java implementation:

  .. code:: java

    org.apache.hadoop.hdfs.DistributedFileSystem

- Hadoop's default fs.

WebHDFS
^^^^^^^
- URI scheme: webhdfs

- Java implementation:

  .. code:: java

    org.apache.hadoop.hdfs.web.WebHdfsFileSystem

- A filesystem providing authenticated access to HDFS over http.

Secure WebHDFS
^^^^^^^^^^^^^^
- URI scheme: swebhdfs

- Java implementation:

  .. code:: java

    org.apache.hadoop.hdfs.web.SWebHdfsFileSystem

- An https version of WebHDFS.

HAR
^^^
- URI scheme: har.

- Java implementation:

  .. code:: java

    org.apache.hadoop.fs.HarFileSystem

- A filesystem layered on another filesystem for archiving files. Hadoop
  Archives are used for packing lots of files in HDFS into a single archive
  file to reduce the namenode’s memory usage.

View
^^^^
- URI scheme: viewfs.

- Java implementation:

  .. code:: java

    org.apache.hadoop.viewfs.ViewFileSystem

- A client-side mount table for other hadoop filesystems.

FTP
^^^
- URI scheme: ftp.

- Java implementation:

  .. code:: java

    org.apache.hadoop.fs.ftp.FTPFileSystem

- A filesystem backed by FTP server.

Amazon S3
^^^^^^^^^
- URI scheme: s3a

- Java implementation:

  .. code:: java

    org.apache.hadoop.fs.s3a.S3AFileSystem

- A filesystem backed by Amazon S3.

Microsoft Azure Storage Blobs file system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- URI scheme: azure

- Java implementation:

  .. code:: java

    org.apache.hadoop.fs.azure.NativeAzureFileSystem

- A filesystem backed by Azure.

OpenStack Swift
^^^^^^^^^^^^^^^
- URI scheme: swift

- Java implementation:

  .. code:: java

    org.apache.hadoop.fs.swift.snative.SwiftNativeFileSystem

- A filesystem backed by Swift.

IBM General Parallel File System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

MapRFS
^^^^^^


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

- NameNode automatic failover.
  
  Mechanism. Automatic failover is managed by a failover controller. The
  default implementation uses ZooKeeper and ZooKeeper failover controller
  (ZKFC). ZooKeeper quorum runs in the cluster, which is responsible for:

  * Failure detection - each of the NameNode machines in the cluster maintains
    a persistent session in ZooKeeper. If the machine crashes, the ZooKeeper
    session will expire, notifying the other NameNode(s) that a failover should
    be triggered.

  * Active NameNode election - ZooKeeper provides a simple mechanism to
    exclusively elect a node as active. If the current active NameNode crashes,
    another node may take a special exclusive lock in ZooKeeper indicating that
    it should become the next active.

  ZKFC is a lightweight process runs on each NameNode machine, which is
  responsible for:

  * Health monitoring - ZKFC pings its local NameNode periodically with a
    health-check command. As long as the NameNode responds timely with a
    healthy status, ZKFC considers the node healthy. Otherwise it's unhealthy.
    For a NameNode, it will only responds as healthy when it has read all of
    the edits from the JournalNodes.

  * ZooKeeper session management - when the local NameNode is healthy, the ZKFC
    holds a session open in ZooKeeper. If the local NameNode is active, it also
    holds a special “lock” znode. If it's unhealthy, ZKFC releases the session;
    or in terms of node crash, session will automatically expire. Either way,
    the lock znode will be automatically deleted.

  * ZooKeeper-based election - if the local NameNode is healthy, and the ZKFC
    sees that no other node currently holds the lock znode, it will itself try
    to acquire the lock. If it succeeds, then it has “won the election”, and is
    responsible for running a failover to make its local NameNode active. The
    failover process is similar to the manual failover: first, the previous
    active is fenced if necessary, and then the local NameNode transitions to
    active state.

  Two kinds of failover.

  * graceful failover. A failover that is initiated by intention, e.g., for
    routine maintenance. In this, the failover controller arranges an orderly
    transition for both namenodes to switch roles.

  * ungraceful failover. A failover that is initiated in any event of active
    NameNode failure. In this situation, it's impossible to be sure that the
    failed NameNode has stopped running. Various fencing methods are employed
    to prevent the previously active NameNode from doing any damage and causing
    corruption.

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

  * JournalNode machines. the machines on which you run the JournalNodes. The
    JournalNode daemon is relatively lightweight, so these daemons may
    reasonably be collocated on machines with other Hadoop daemons.

  * ZooKeeper machines. Since ZooKeeper itself has light resource requirements,
    it is acceptable to collocate the ZooKeeper nodes on the same hardware as
    the HDFS NameNode and Standby Node. Many operators choose to deploy the
    third ZooKeeper process on the same node as the YARN ResourceManager. It is
    advisable to configure the ZooKeeper nodes to store their data on separate
    disk drives from the HDFS metadata for best performance and isolation.

NameNode HA using NFS filer
"""""""""""""""""""""""""""
- QJM is prefered over NFS filer, because the former can ensure that there's
  only one NameNode and only the NameNode with the newer Epoch number to write
  to the EditLog at one time.

Web UI
^^^^^^
- port: 9870

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
overview
^^^^^^^^
- HDFS uses a traditional hierarchical file organization.

- HDFS supports traditional file/directory operations.

- hardlinks and symlinks are not supported.

- Files are write-once except for append and truncate. Strictly one writer at
  any time (per file).

- POSIX-like interface can be presented by client library.

file permissions
^^^^^^^^^^^^^^^^
- similar to the POSIX. with the following exception:

  * For regular file, execution permission (x) is ignored, since files can't
    be executed in HDFS. For directory, it's like POSIX.

- permission checking.

  * can be enabled/disabled by dfs.permissions.enabled property.

  * When permissions checking is enabled, the owner permissions are checked if
    the client’s username matches the owner, and the group permissions are
    checked if the client is a member of the group; otherwise, the other
    permissions are checked.

  * For superuser, permissions are not checked. The NameNode process is the
    superuser.

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

  * For the common case, when the replication factor is three, HDFS’s placement
    policy is to put one replica on the local machine if the writer is on a
    datanode, otherwise on a random datanode in the same rack as that of the
    writer, another replica on a node in a different (remote) rack, and the
    last on a different node in the same remote rack.
  
    If the replication factor is greater than 3, the placement of the 4th and
    following replicas are determined randomly.
  
    NameNode does not allow DataNodes to have multiple replicas of the same
    block, maximum number of replicas created is the total number of DataNodes
    at that time.

  * Overall, this strategy gives a good balance among reliability (blocks are
    stored on two racks), write bandwidth (writes only have to traverse a
    single network switch), read performance (there’s a choice of two racks to
    read from), and block distribution across the cluster (clients only write a
    single block on the local rack).

  * This policy cuts the inter-rack write traffic which generally improves
    write performance (最可靠的方式是将副本全部放在不同的机架上, 但跨机架的带宽
    一般是相对比同一个机架内节点之间慢, 这样 write pipeline 就会慢). The chance
    of rack failure is far less than that of node failure; this policy does not
    impact data reliability and availability guarantees. However, it does
    reduce the aggregate network bandwidth used when reading data since a block
    is placed in only two unique racks rather than three. (对于单个 client 读的
    情况, 无论怎么放, 都不影响读取速度, 因为每次只读一个 DataNode. 但如果有多个
    客户端同时读多个文件. 负载只能分布在两个机架上, 而不是三个机架, 这样总体能
    提供的读带宽就变小了.)

- How does HDFS write file? (See also [hdfsReadAndWrite]_)

  1. The client creates the file by calling ``FileSystem.create()``.

  2. DistributedFileSystem 向 namenode 发起 RPC call, 请求在 filesystem
     namespace 中创建这个文件. 此时没有任何 block.

  3. namenode 做一系列检查, 包括该路径是否已经存在, client 是否有权限创建等.
     若通过, 则创建这个文件, 否则 IOException is thrown. 若通过,
     DistributedFileSystem 返回一个 FSDataOutputStream, 用于写文件数据.

  4. client 写数据时, FSDataOutputStream 将收到的数据封装成一个个 packets, 加入
     data queue. 同时, 它创建一个 ack queue, 对每个写入的 packets 它预期收到
     一个 ack.

  5. DataStreamer 向 namenode 请求 datanodes 以保存数据. namenode 选择并给出 a
     list of datanodes 用于保存 block 副本. The list of datanodes forms a
     pipeline.

  6. DataStreamer 消费 data queue, streaming the packets to the first datanode
     in the pipeline. 第一个 datanode 保存 packets 并转发给第二个 datanode. 如
     此继续直至 pipeline 的最后一个 datanode.

  7. 最后一个节点保存 packet 后, 向前一个节点发送 ack packet, 如此继续直至第一
     个节点给 FSDataOutputStream 返回 ack. 注意只有整个 pipeline 每个节点都保存
     了这个 packet, 才会向 client-side 发送 ack.

     If any datanode fails while data is being written to it, then the
     following actions are taken, which are transparent to the client writing
     the data. First, the pipeline is closed, and any packets in the ack queue
     are added to the front of the data queue so that datanodes that are
     downstream from the failed node will not miss any packets. The current
     block on the good datanodes is given a new identity, which is communicated
     to the namenode, so that the partial block on the failed datanode will be
     deleted if the failed datanode recovers later on. The failed datanode is
     removed from the pipeline, and a new pipeline is constructed from the two
     good datanodes. The remainder of the block’s data is written to the good
     datanodes in the pipeline. The namenode notices that the block is
     under-replicated, and it arranges for a further replica to be created on
     another node. Subsequent blocks are then treated as normal.

     It’s possible, but unlikely, for multiple datanodes to fail while a block
     is being written. As long as dfs.namenode.replication.min replicas (which
     defaults to 1) are written, the write will succeed, and the block will be
     asynchronously replicated across the cluster until its target replication
     factor is reached (dfs.replication, which defaults to 3).

  8. FSDataOutputStream 收到 ack 后, remove the packet from the ack queue.

     注意这个 ack 与 TCP 层的 ack 是不一样的. 这个 ack 的意义是一个 packet 已经
     经过整个 pipeilne 所有 datanode 都接收到了. TCP 的 ack 只是告知 connection
     对端自己接收到了对方的 packet.

  9. client 写完数据后, 调用 ``FSDataOutputStream.close()``. This action
     flushes all the remaining packets to the datanode pipeline and waits for
     acknowledgments. client 接收到所有 packets 的 ack 之后, 访问 namenode to
     signal that the file is complete.

  10. The namenode wait for blocks to be minimally replicated before returning
      successfully.

replica selection (read)
^^^^^^^^^^^^^^^^^^^^^^^^
- When client requested to read a file, NameNode tries to satisfy a read
  request from a replica that is closest to the reader (location proximity).

- how does HDFS read file? (See also [hdfsReadAndWrite]_)

  1. 客户端调用 ``FileSystem.open()`` 读取文件. 对于 HDFS, 这是
     DistributedFileSystem.

  2. DistributedFileSystem 对象向 namenode 发起 RPC, 获取 the locations of the
     first few blocks in the file.

  3. 对于每个 block, namenode 给出一个保存着这个 block 的副本的所有 datanode 地
     址列表. the datanodes are sorted according to their proximity to the
     client (according to the topology of the cluster’s network).

  4. The DistributedFileSystem returns an FSDataInputStream to the client for
     it to read data from.

  5. The client calls ``read()`` on the stream.

  6. FSDataInputStream 根据自身保存的前几个 blocks 与 datanode address 的映射
     关系, connects to the first (closest) datanode for the first block in the
     file.

  7. Data is streamed from the datanode back to the client, which calls
     ``read()`` repeatedly on the stream. When the end of the block is
     reached, FSDataInputStream will close the connection to the datanode,
     then find the best datanode for the next block.

     读的过程中, 若 FSDataInputStream 与 datanode 的交互出错, 它自动尝试下一个
     最近的 datanode. It will also remember datanodes that have failed so that
     it doesn’t needlessly retry them for later blocks.

     FSDataInputStream 读取 block 时还会计算 checksum. 若 checksum 与 checksum
     file 不一致, 则认为 block 损坏. FSDataInputStream 转而从下一个 datanode
     读取这个 block. 它同时还会把坏块上报给 namenode.
     
  8. Blocks are read in order, with the FSDataInputStream opening new connections
     to datanodes as the client reads through the stream. It will also call
     the namenode to retrieve the datanode locations for the next batch of
     blocks as needed. When the client has finished reading, it calls ``close()``
     on the FSDataInputStream.

- 从 HDFS 读取数据有两个重要特征:

  * client 直接与 datanode 交互, namenode 只提供 metadata 和调度的作用. block
    data 不会流经 namenode, 从而 namenode 不会成为集群 throughput 的瓶颈.

  * client 从离他最近的 datanode 读取数据, 从而能更好地利用带宽.

  这两个特性 allows HDFS to scale to a large number of concurrent clients
  because the data traffic is spread across all the datanodes in the cluster.

  注意 HDFS 的这种特性让集群的总 throughput 很大, 然而对单个客户端而言, 并没有
  速度上的提升.

filesystem coherency model
--------------------------
- A coherency model for a filesystem describes the data visibility of reads and
  writes for a file.

- HDFS trades off some POSIX requirements for performance. Hence some aspects
  of behavior differences.

  * After creating a file by ``FileSystem.create()`` (not writing data yet), it
    is visible in the filesystem namespace.

  * When writing data, the current block being written is not visible to other
    readers. To force all buffers to be flushed to the datanodes, use
    ``hflush()``.

  * To force data having been written to datanode's disk, use ``hsync()``.

- With no calls to ``hflush()`` or ``hsync()``, application should be prepared
  to lose up to a block of data in the event of client or system failure. 因为
  当前的 block 可能还在 client-side 的 FSDataOutputStream 的 buffer 中, 尚未写
  入 datanode.

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

Extended file attributes
------------------------
Extended attributes in HDFS are modeled after extended attributes in Linux.
An extended attribute is a name-value pair, with a string name and binary
value. xattrs names must also be prefixed with a namespace. Multiple xattrs can
be associated with a single inode.

- five namespaces in HDFS: user, trusted, system, security, raw.

user
""""
- Commonly used by client applications.
  
- Access to extended attributes in the user namespace is controlled by the
  corresponding file permissions.

trusted
""""""""
- The trusted namespace is available only to HDFS superusers.

system
""""""
- The system namespace is reserved for internal HDFS use.
  
- This namespace is not accessible through userspace methods, and is reserved
  for implementing internal HDFS features.

security
""""""""
- The security namespace is reserved for internal HDFS use.
  
- This namespace is generally not accessible through userspace methods.

- security.hdfs.unreadable.by.superuser.
  
  * can only be set on files, and it will prevent the superuser from reading
    the file’s contents.  The superuser can still read and modify file
    metadata, such as the owner, permissions, etc.
    
  * can be set and accessed by any user, assuming normal filesystem
    permissions.
    
  * write-once, and cannot be removed once set.
    
  * does not allow a value to be set.

raw
""""
- reserved for internal system attributes that sometimes need to be exposed.

- they are not visible to the user except when getfattr is called on a file or
  directory in the ``/.reserved/raw`` HDFS directory hierarchy.

- These attributes can only be accessed by the superuser.

client interfaces
-----------------
Java API
^^^^^^^^
- the hadoop-native API.

- java class: org.apache.hadoop.fs.FileSystem

- also a generic interface to any hadoop compatible filesystem, not only to
  HDFS.

HTTP REST API
^^^^^^^^^^^^^
- The HTTP REST API exposed by the WebHDFS protocol makes it easier for other
  languages to interact with HDFS. Note that the HTTP interface is slower than
  the native Java client, should be avoided for very large data transfers.

- two ways for accessing HDFS over HTTP.

  * directly, where the HDFS daemons serve HTTP requests to clients;

  * via HttpFS proxy, which accesses HDFS on the client’s behalf using the
    usual DistributedFileSystem API. clients speak WebHDFS with proxies.

- There are also two equivalent URI schemes can be used with HTTP REST API.

  * When using hadoop's filesystem tools, webhdfs scheme is recognized::

      [s]webhdfs://<host>:<http_port>/<path>

  * When using generic http tools, http scheme can be used::

      http[s]://<host>:<http_port>/webhdfs/v1/<path>?op=...

  注意到 webhdfs 访问的端口就是 NameNode and DataNode 配置的 http server 端口
  (因为它就是用 http 协议的).

via WebHDFS directly
""""""""""""""""""""
- The embedded web servers in the namenode and datanodes act as WebHDFS
  endpoints.

- File metadata operations are handled by the namenode.
  
- file read and write operations are sent first to the namenode, which sends an
  HTTP redirect to the client indicating the datanode to stream file data from
  or to.

via HttpFS proxy
""""""""""""""""
- The HttpFS proxy is started independently of the namenode and datanode
  daemons.

- clients speak WebHDFS with proxies. Proxies accesses HDFS on the client’s
  behalf using the usual DistributedFileSystem API.

- The proxies are stateless, so they can run behind a standard load balancer.
  All traffic to the cluster passes through the proxy. The client never
  accesses the namenode or datanode directly.

- This allows for stricter firewall and bandwidth-limiting policies to be put
  in place.


C API
^^^^^
- libhdfs C library mirrors the Java FileSystem interface.

- Despite its name, it's a generic interface to any hadoop compatible
  filesystem, not only to HDFS.

- It uses Java Native Interface (JNI) to call a Java filesystem client.

POSIX API via NFS gateway
^^^^^^^^^^^^^^^^^^^^^^^^^
- Using Hadoop's NFSv3 gateway, it's possible to mount HDFS on local client's
  filesystem so that HDFS can be accessed in the POSIX way.

- The following usage patterns are supported:

  * browse HDFS filesystem through local filesystem.

  * download files from HDFS

  * upload files to HDFS.

  * stream data directly to HDFS through mount point. File appending is
    supported, but random write is not supported.

POSIX API via FUSE
^^^^^^^^^^^^^^^^^^
- Fuse-DFS is implemented in C using libhdfs as the interface to HDFS.

- Since it uses libhdfs, it's a generic interface to any hadoop compatible
  filesystem, not only to HDFS.

YARN
====
- YARN is a cluster resource management system, which allows any distributed
  program, not just MapReduce, to run on a Hadoop cluster.

- Why do we need YARN?
  
  YARN 在 hadoop 这样的分布式计算系统中的地位, 就相当于操作系统在单个计算机中的
  地位. YARN 上层的各种应用程序与 YARN 的关系, 就相当于进程与操作系统 (或更具体
  地讲, 调度器) 的关系.

  集群的资源, 包括 CPU 资源, 内存资源, 存储资源, 带宽资源等. 这些资源需要一个一
  般化的统筹管理者. 这样的价值是很多的. 上层应用的逻辑专注于自身应用逻辑, 只需
  调用 API 申请资源即可. 集群资源可控, 不会允许应用程序滥用. 此外, hadoop 中还
  存在 data locality 优化的问题. YARN 可以自动选择最近的节点运行应用, 节省带宽
  资源. 这对应用是透明的. 总之, 只要想让 hadoop 的资源使用能够一般化到各个应用
  程序, 而不是仅仅能跑 MapReduce, 需要 YARN 这样的资源调度层是很自然的设计.

- YARN provides APIs for requesting and working with cluster resources, but
  these APIs are not typically used directly by user code. Instead, users write
  to higher-level APIs provided by distributed computing frameworks, which
  themselves are built on YARN and hide the resource management details from
  the user.

Architecture
------------
- Resource Manager (RM) -- one per cluster. Managing and allocating resources
  across the cluster, and scheduling applications. RM has two components:

  * Applications Manager (AsM) -- accept job submissions from clients, select
    node with sufficient resources to start AM for job/application, and also
    provide service to relaunch AM in case of failure.

  * Scheduler -- schedule the submitted and accepted applications for
    execution.

- Node Manager (NM) -- one per computing nodes. RM is master and NMs are
  workers/slaves. NM has following functionalities:

  * Track the total available resources to the local node, and their
    utilization status. NM sends these information as report periodically to
    RM.

  * Responsible for launching the containers on the local node, monitor their
    resource usage (CPU, memory, storage and network), and report these status
    to the RM.

  * NM 从节点的角度把控该节点内运行的所有容器的资源使用和运行状态.

- Application Master (AM) -- one per application. Executing applications and
  providing failover.

  * AM is run in a dedicated container. AsM negotiates for the container in
    which an application's AM runs when the application is scheduled by the
    YARN's scheduler.

  * Each application provides its dedicated AM that knows what to do next when
    being spawned up (do some computing works, request more containers,
    communicate with clients, etc.). An application's AM can be written in any
    language, since it's just an process run in a container, and it
    communicates with RM and NMs via networking.

  * responsibility of an application's AM
    
    1) manage the application's lifecycle;

    2) dynamically adjust application's resource consumption;

    3) manage application's execution flow;

    4) handle faults during application task's run

    5) monitor task processes and provide their status; 

  * AM 从一个 application 的角度整体把控它手下所有容器 (和里面的进程) 的运行情
    况.

- container. A container executes an application-specific process with a
  constrained set of resources including CPU, memory, etc. A job/application is
  split in tasks and each task gets executed in one container.

  * A container may be a process on generic Unix or a cgroup on Linux.

  * There can be one or more containers on given computing node (slave node)
    depending upon the available resources and the task's requested resources.

- How is a YARN application run? See also [QuoraAppMaster]_ and [MapRAM]_.

  * Client submits a new application/job request to RM.

  * RM (AsM part) accepts the job request. The job/application is queued in
    scheduler.
    
  * When the application is scheduled, AsM finds a slave node and instructs the
    NM on this node to launch a container and run AM process of this
    application inside of it. The AM process commandline is provided by client.

  * After AM is spawned up, it sends request to RM, asking for resources
    required to run the application. In the request, AM includes resource's
    locality preferences and attributes of the containers.

  * RM considers the locality preferences and resource requirements, responds
    with a list of containers along with a list of slave nodes that containers
    can be spawned on. RM 尽量满足 AM 的 locality 需求, 在所需的节点上分配容器,
    或者在同一个机架上其他节点分配容器, 实在不行才在其他机架上分配容器.
    
    The allocated resources is provided in the form of a lease. AM pulls the
    lease on subsequent heartbeats. 生成 lease 的同时, 还生成了一个 security
    token, 它用于 NM 校验 AM 的资源请求是否合法.

  * AM contacts NMs of the node where the container has been allocated, present
    to them the lease, thereby gaining access to the resources. AM needs to
    provide to NMs a container launch context (CLC) that includes the following
    information:

    - Environment variables

    - Dependencies (local resources such as data files or shared objects needed
      prior to launch)

    - security token

    - commandline of process to run
    
  * NMs grant the requested resources by spawning up containers, running the
    specified commands. In the meantime, AM might report progress status to
    client.

- 几点需要注意的:

  * AM 与 NM 都是从某个整体上对运行进行监控和负责. 但两者的角度是不同的, AM 是
    对应用的所有容器 (和里面的进程) 进行监控和管理, NM 是对这个节点上的所有容器
    进行监控和管理.

  * 一个 YARN application 由三部分构成: client, application master (AM), task
    processes. 一个应用的这几个部分之间如何交互, 由程序本身去定义. YARN 不提供
    应用组件之间的交流机制.

YARN application
----------------
- Application lifespan.

  * one application per user job.
    
    e.g., MapReduce.

  * one application per workflow or user session of possibly unrelated jobs.
    Containers can be reused between jobs, data can also be potentially cached
    between jobs.
    
    e.g., Spark.

  * a long-running application that is shared by different users. Often acts in
    some kind of coordination role. The “always on” application master means
    that users have very low latency responses to their queries since the
    overhead of starting a new application master is avoided.
    
    e.g., Impala (providing a proxy application that the Impala daemons
    communicate with to request cluster resources.).

ResourceManager
---------------
- port: 8088

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

History server
--------------
- port: 19888

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

network topology
================
network topology structure
--------------------------
- network is represented as a tree, leaf 为 nodes, parent node 为交换机和路由器
  等网络设备.

- By default, Hadoop assumes that the network is flat -- a single level
  hierarchy that all nodes are on a single rack in a single data center.

distance of nodes
-----------------
- In the context of high-volume data processing, the limiting factor is the
  rate at which we can transfer data between nodes. Therefore, bandwidth is
  used as a measure of distance between two nodes.

- When the network is represented as a tree, the distance between two nodes is
  the sum of their distances to their closest common ancestor.

- The levels in the tree are commonly defined as data centers, racks, and
  nodes.

- 由于实际中难以测量节点之间的带宽, Hadoop 以集群的网络拓扑结构为依据来建立
  节点之间的距离关系. 这是基于以下带宽关系假定 (由大至小):
  
  * Processes are on the same node
  
  * Different nodes on the same rack
  
  * Nodes on different racks in the same data center
  
  * Nodes in different data centers

Security
========
user authentication
-------------------
- By default, Hadoop runs with security disabled, which means that a client’s
  identity is not authenticated. Because clients are remote, it is possible for
  a client to become an arbitrary user simply by creating an account of that
  name on the remote system.

Setup
=====
standalone mode
---------------
- no daemon running and everything runs in a single JVM.

- the local filesystem and the local MapReduce job runner are used.

- suitable for running MapReduce programs during development.

minimal configurations
^^^^^^^^^^^^^^^^^^^^^^
- core-site.xml

  * fs.defaultFS: ``file:///``

- mapred-site.xml

  * mapreduce.framework.name: ``local``

Pseudo-distributed mode
-----------------------
- daemons run on the local machine. simulating a cluster.

- HDFS and YARN daemons are used, MapReduce is configured to use YARN.

- Hadoop doesn’t actually distinguish between pseudo-distributed and fully
  distributed modes; it merely starts daemons on the set of hosts in the
  cluster (defined by the ``workers`` file) by SSHing to each host and starting
  a daemon process. Pseudodistributed mode is just a special case of fully
  distributed mode in which the (single) host is ``localhost``.

minimal configurations
^^^^^^^^^^^^^^^^^^^^^^
- core-site.xml

  * fs.defaultFS: ``hdfs://localhost/``

- hdfs-site.xml

  * dfs.replication: ``1``

- mapred-site.xml

  * mapreduce.framework.name: ``yarn``

- yarn-site.xml

  * yarn.resourcemanager.hostname: ``localhost``

  * yarn.nodemanager.aux-services: ``mapreduce_shuffle``

setup
^^^^^
See `setup`_ in `Fully distributed mode`_, with hostname substituted
by localhost.

Fully distributed mode
----------------------
- daemons run on a cluster of machines.

- HDFS and YARN daemons are used, MapReduce is configured to use YARN.

minial configurations
^^^^^^^^^^^^^^^^^^^^^
- core-site.xml

  * fs.defaultFS: ``hdfs://<namenode>/``

- hdfs-site.xml

  * dfs.replication: ``3``

- mapred-site.xml

  * mapreduce.framework.name: ``yarn``

- yarn-site.xml

  * yarn.resourcemanager.hostname: ``<resourcemanager>``

  * yarn.nodemanager.aux-services: ``mapreduce_shuffle``

setup
^^^^^
- configure passwordless ssh to each ``workers`` node, for each of Hadoop users:
  hadoop, hdfs, yarn, mapred. hadoop 的各种启动、停止脚本需要使用 ssh 访问各个
  节点, 从而在整个集群各个节点上一起操作.

- formatting the HDFS filesystem:

  .. code:: sh

    hdfs namenode -format

- start HDFS, YARN, MapReduce daemons:

  .. code:: sh

    start-dfs.sh
    start-yarn.sh
    mapred --daemon start historyserver

- stop MapReduce, YARN, HDFS daemons:

  .. code:: sh

    mapred --daemon stop historyserver
    stop-yarn.sh
    stop-dfs.sh

configuration
=============
shell-specific configuration
----------------------------
- Add hadoop binaries to PATH (in bashrc):

  .. code:: sh

    [[ -d "$HADOOP_HOME" ]] && {
        [[ ":${PATH}:" == *:$HADOOP_HOME/bin:* ]] || PATH="${PATH:+$PATH:}$HADOOP_HOME/bin"
        [[ ":${PATH}:" == *:$HADOOP_HOME/sbin:* ]] || PATH="${PATH:+$PATH:}$HADOOP_HOME/sbin"
    }

- Add java home environ (in bashrc):

  .. code:: sh

    declare -x JAVA_HOME=/usr/lib/jvm/default

- specify ``HADOOP_HOME`` and ``HADOOP_CONF_DIR`` (in /etc/profile.d/hadoop.sh)

  .. code:: sh

    export HADOOP_HOME=/usr/lib/hadoop
    export HADOOP_CONF_DIR=/etc/hadoop

environment configuration
-------------------------
- setting site-specific customization of the Hadoop daemons' process environment.

  * /etc/hadoop/hadoop-env.sh

  * /etc/hadoop/yarn-env.sh

  * /etc/hadoop/mapred-env.sh

  * /etc/hadoop/httpfs-env.sh
   
  * /etc/hadoop/kms-env.sh
   
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
- read-only default configurations for all properties, under various
  subdirectories of ``$HADOOP_HOME/share/doc/hadoop``:

  * core-default.xml

  * hdfs-default.xml

  * yarn-default.xml

  * mapred-default.xml

  * httpfs-default.html

- site-specific configuration:

  * /etc/hadoop/core-site.xml, common properties.
   
  * /etc/hadoop/hdfs-site.xml, HDFS properties.
   
  * /etc/hadoop/yarn-site.xml, YARN properties.
    
  * /etc/hadoop/mapred-site.xml, MapReduce properties.

  * /etc/hadoop/httpfs-site.xml, HttpFS properties.

core-site.xml
^^^^^^^^^^^^^
- fs.defaultFS. default: ``file:///``. The name of the default file system. A
  URI whose scheme and authority determine the FileSystem implementation. The
  uri's scheme determines the config property (fs.SCHEME.impl) naming the
  FileSystem implementation class. The uri's authority is used to determine the
  host, port, etc. for a filesystem. 注意这个属性决定 hadoop 使用哪个文件系统
  implementation.

- io.file.buffer.size

hdfs-site.xml
^^^^^^^^^^^^^
HDFS
""""
- dfs.hosts

- dfs.hosts.exclude

- dfs.blocksize

- dfs.replication. default: 3. default block replication. Per-file replication
  factor overrides this.

- dfs.permissions.enabled. default true. enable permission checking in HDFS.
  Switching between true/false does not change the mode, owner or group of
  files or directories.

xattrs
""""""
- dfs.namenode.xattrs.enabled. 是否开启 extended attributes. by default, true.

- dfs.namenode.fs-limits.max-xattrs-per-inode. 每个 inode 最多的 xattrs 数目,
  默认 32.

- dfs.namenode.fs-limits.max-xattr-size. combined size of the name and value
  of an xattr in bytes. by default, 16384 bytes (16KB).

NameNode
""""""""
- dfs.namenode.rpc-address. RPC address that handles all client requsts.
  default RPC port is 8020.

- dfs.namenode.http-address. default: 0.0.0.0:9870. namenode web UI.

- dfs.namenode.name.dir

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

httpfs-site.xml
^^^^^^^^^^^^^^^
- httpfs.http.port. default 14000. http port for rest api.

workers flie
------------
- /etc/hadoop/workers

- worker's hostname/ip address, one per line.

- SSH trusts must be established for accounts used to run hadoop.

CLI
===
hadoop
------
client commands
^^^^^^^^^^^^^^^
fs
""
- This the hadoop's generic file system shell. It implements the client
  interface to any hadoop compatible filesystems.

help
~~~~
::

  hadoop fs -help [cmd ...]

- display help for each specified command or all commands if none given.

- this is much more verbose than ``-usage``.

put
~~~
::

  hadoop fs -put [-f] [-p] [-l] [-d] <localsrc> ... <dst>

- copy files from local file system to a hadoop filesystem. by default fails if dst exists.

- dst can be:
 
  * a fully qualified hadoop filesystem uri, e.g. ``hdfs://<namenode>/path/to/file``
   
  * absolute path, omitting scheme part (in which case the fs.defaultFS is
    assumed), e.g. ``/path/to/file``

  * relative path, relative to user's home directory in a hadoop filesystem, e.g.,
    ``path/to/file``.

- options.

  * ``-f``. overwrites the destination if exists.

copyFromLocal
~~~~~~~~~~~~~
::

  hadoop fs -copyFromLocal [-f] [-p] [-l] [-d] [-t <thread-count>] <localsrc> ... <dst>

- same as -put. except for thread option.

- options.

  * ``-t <thread count>``. number of threads to be used, default 1.

get
~~~
::

  hadoop fs -get [-f] [-p] [-ignoreCrc] [-crc] <src> ... <localdst>

- src can be a file glob pattern.

- When copying multiple files, dst must be a directory.

copyToLocal
~~~~~~~~~~~
- identical to -get.

mkdir
~~~~~
::

  hadoop fs -mkdir [-p] <path> ...

- create paths as directories.

- options:

  * ``-p``. do not fail if directory already exists, making parent directories
    as necessary.

rmdir
~~~~~
::

  hadoop fs -rmdir [--ignore-fail-on-non-empty] <dir> ...

- remove empty directories.

- won't remove non empty ones.

ls
~~
::

  hadoop fs -ls [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [-e] [<path> ...]

- ls paths matching file glob patterns. If none given, list the content of
  ``/user/<current user>``.

- output columns:

  1. same as ls -l

  2. replication factor of the file. For directory, this is empty, because
     directory is implemented as metadata and stored by NameNode. (assuming
     HDFS)

  3. same as ls -l

  4. same as ls -l

  5. file size in bytes. for directory, this is 0. (assuming HDFS)

  6. same as ls -l

  7. same as ls -l

cp
~~
::

  hadoop fs -cp [-f] [-p | -p[topax]] URI [URI ...] <dest>

- cp 的 source URI 和 dest 必须是 hadoop compatible filesystem 中的路径/URI. 不
  能是本地文件. 似乎不能复制目录.

- raw xattrs. ‘raw.*’ namespace extended attributes are preserved if (1) the
  source and destination filesystems support them (HDFS only), and (2) all
  source and destination pathnames are in the /.reserved/raw hierarchy.
  Determination of whether ``raw.*`` namespace xattrs are preserved is
  independent of the -p (preserve) flag.

- options.

  * ``-f``. overwrite the destination.

  * ``-p``. preserve file attributes (timestamps, ownership, permission, acl,
    xattr). Without arg, it's equivalent to ``top``.

getfattr
~~~~~~~~
::

  hadoop fs -getfattr [-R] {-n name | -d} [-e en] <path>

- display xattr names and values for a file or directory.

- options.

  * ``-R``. like getfattr(1)

  * ``-n``. like getfattr(1)

  * ``-d``. like getfattr(1)

  * ``-e <encoding>``. like getfattr(1)

setfattr
~~~~~~~~
::

  hadoop fs -setattr {-n name [-v value] | -x name} <path>

- set or remove xattr for path.

- options.

  * ``-n``. like setfattr(1)

  * ``-v``. like setfattr(1)

  * ``-x``. like setfattr(1)

distcp
""""""
::

  hadoop distcp [options] [<source> ...] <dest>

overview
~~~~~~~~
- distcp -- distributed copy, is a tool used for large inter/intra-cluster
  copying. It uses MapReduce to effect its distribution, error handling and
  recovery, and reporting.

- distcp can be unreliable. After a copy, it is recommended that one generates
  and cross-checks a listing of the source and destination to verify that the
  copy was truly successful. Since DistCp employs both Map/Reduce and the
  FileSystem API, issues in or between any of the three could adversely and
  silently affect the copy. Some have had success running with ``-update``
  enabled to perform a second pass.

- If another client is still writing to a source file, the copy will likely
  fail. Attempting to overwrite a file being written at the destination should
  also fail on HDFS. If a source file is (re)moved before it is copied, the
  copy will fail with a FileNotFoundException.

- ``hadoop distcp`` is preferred over ``hadoop fs -cp`` even for single file
  copy because ``hadoop fs -cp`` copies the file via the client running the
  command.

mechanism
~~~~~~~~~
- The files/directories in source are expanded into a list of files under that
  namespace, and saved into a temporary file. It partitions the temporary
  file's contents among a set of map tasks. 默认情况下, 每个 map task 输入一组
  要 copy 的文件列表. There's no reduce task.

- At present, the smallest unit of work for DistCp is a file. i.e., a file is
  processed by only one map. 在一个 map 中, ``-blocksperchunk`` 可以对很大的
  文件进行多线程传输.

- Each NodeManager must be able to reach and communicate with both the source
  and destination file systems. For HDFS, both the source and destination must
  be running *the same version of the protocol or use a backwards-compatible
  protocol*.

behaviors
~~~~~~~~~
- When copying from multiple sources, distcp will abort the copy with an error
  message if two sources collide (指的是两个 source 中存在同名的文件, 这样复制
  到 dest 时路径冲突.)

- By default, files already existing at the destination are skipped. A count of
  skipped files is reported at the end of each job.

- without ``-update`` or ``-overwrite``, source directories are copied into the
  target directory. With one of either options, it's different.

- raw xattr namespace. If the target and all of the source pathnames are in the
  ``/.reserved/raw`` hierarchy, then ‘raw’ namespace extended attributes will
  be preserved.  raw xattrs are preserved based solely on whether
  ``/.reserved/raw`` prefixes are supplied. The -p (preserve, see below) flag
  does not impact preservation of raw xattrs.

sources and destination
~~~~~~~~~~~~~~~~~~~~~~~
- Sources and destination are hadoop compatible filesystem URIs, typically
  hdfs:// namespace URIs.

- To copy between different major versions of HDFS, use WebHdfsFileSystem,
  i.e., webhdfs:// URIs.

- If dest does not exist, it will be created.

options
~~~~~~~
- ``-update``. Overwrite if source and destination differ in size, blocksize,
  or checksum.

  * when this option is specified, the *contents* of the source-directories are
    copied to target, and not the source directories themselves.

- ``-append``. If the source file is greater in length than the destination
  file, the checksum of the common length part is compared. If the checksum
  matches, only the difference is copied using read and append functionalities.
  The ``-append`` option only works with ``-update`` without ``-skipcrccheck``.

- ``-overwrite``. overwrite destination. If a map fails and -i is not
  specified, all the files in the split, not only those that failed, will be
  recopied.

  * when this option is specified, the *contents* of the source-directories are
    copied to target, and not the source directories themselves.

- ``-delete``. Delete the files existing in the dst but not in src. Delete is
  applicable only with -update or -overwrite options.

- ``-strategy <strategy>``. Choose the copy-strategy. Can be dynamic,
  uniformsize. By default, uniformsize is used.

- ``-p[rbugpcaxt]``. preserve: replication number, block size, user, group,
  permission, checksum-type, acl, xattrs, timestamp. By default, block size
  is preserved. When ``-update`` is specified, status updates will not be
  synchronized unless the file sizes also differ (i.e. unless the file is
  re-created).

- ``-i``. ignore failures.

- ``-log <logdir>``. write log to this directory. Logs are actually generated
  as map's output. Therefore one log is generated for each file it attempts to
  copy.

- ``-v``. verbose logging. only be used with -log option.

- ``-m <num>``. maximum number of simultaneous copies, i.e., the number of
  map tasks. default 20.

  Number of map tasks should be specified so that file blocks are balanced,
  i.e., they are evenly spread across the cluster. If you specified -m 1, a
  single map would do the copy, which—apart from being slow and not using the
  cluster resources efficientlywould mean that the first replica of each block
  would reside on the node running the map (until the disk filled up).

- ``-f <urilist_uri>``. use an uri to a file containing a list of file uris as
  source list.

- ``-filters <file_uri>``. The path to a file containing a list of pattern
  strings, one string per line, such that paths matching the pattern will be
  excluded from the copy.

- ``-bandwidth``. bandwidth per map, in MB/second. Each map will be restricted
  to consume only the specified bandwidth.

- ``-atomic``. copy the source data to a temporary target location, and then
  move the temporary target to the final-location atomically. Data will either
  be available at final target in a complete and consistent form, or not at
  all.

- ``-tmp <tmp_dir>``. only used with -atomic. used to specify the location of
  the tmp-target. If not specified, a default is chosen. ``tmp_dir`` must be on
  the final target cluster.

- ``-async``. Run DistCp asynchronously. Quits as soon as the Hadoop Job is
  launched. The Hadoop Job-id is logged, for tracking.

- ``-diff <oldSnapshot> <newSnapshot>``. Use snapshot diff report between given
  two snapshots to identify the difference between source and target, and apply
  the diff to the target to make it in sync with source. This option is valid
  only with -update option and the following conditions should be satisfied.

  This option is valid only with -update option and the following conditions
  should be satisfied:

  * Both the source and the target FileSystem must be DistributedFileSystem.

  * Two snapshots <oldSnapshot> and <newSnapshot> have been created on the
    source FS, and <oldSnapshot> is older than <newSnapshot>.

  * The current state of the target has the same content as <oldSnapshot>.

- ``-rdiff <newSnapshot> <oldSnapshot>``. Use snapshot diff report between
  given two snapshots to identify what has been changed on the target since the
  snapshot <oldSnapshot> was created on the target, and apply the diff
  reversely to the target, and copy modified files from the source’s
  <oldSnapshot>, to make the target the same as <oldSnapshot>.   

  This option is valid only with -update option and the following conditions
  should be satisfied.

- ``-numListstatusThreads <num>``. Number of threads to use for building file
  listing. at most 40.

- ``-skipcrccheck``. skip CRC checks between source and target paths.

- ``-blocksperchunk <blocks>``. If set to a positive value, files with more
  blocks than this value will be split into chunks of <blocks> blocks to be
  transferred in parallel, and reassembled on the destination. By default,
  <blocks> is 0 and the files will be transmitted in their entirety without
  splitting. 这有助于更好地处理很大的文件, 将它分块并行传输.
  
  This switch is only applicable when the source file system implements
  getBlockLocations method and the target file system implements concat method.

- ``-copybuffersize <size>``. size of copy buffer to use.

copy strategies
~~~~~~~~~~~~~~~
- uniformsize. make each map copy roughly the same number of bytes. The listing
  file is split into groups of paths, such that the sum of file-sizes in each
  InputSplit is nearly equal to every map.

- dynamic. The listing-file is split into several “chunk-files”, the exact
  number of chunk-files being a multiple of the number of maps requested for in
  the Hadoop Job. Each map task is “assigned” one of the chunk-files, before
  the Job is launched. After all the paths in a chunk are processed, the
  current chunk is deleted and a new chunk is acquired. The process continues
  until no more chunks are available. This “dynamic” approach allows faster
  map-tasks to consume more paths than slower ones, thus speeding up the DistCp
  job overall. Dynamic strategy provides superior performance under most
  conditions.

usage
~~~~~
- A very common use case for distcp is for transferring data between two HDFS
  clusters.

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
- this an alias of ``hadoop fs`` filesystem shell, specific to HDFS client
  interface.

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

httpfs
""""""
::

  hdfs [--daemon (start|status|stop)] httpfs

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

Java API
========
org.apache.hadoop.fs
--------------------
public class FileSystem
^^^^^^^^^^^^^^^^^^^^^^^
- An abstract base class for a fairly generic hadoop compatible filesystem.

static methods
""""""""""""""
- ``public static FileSystem get(Configuration conf)``. get the default FileSystem
  matching the configuration.

- ``public static FileSystem get(URI uri, Configuration conf)``. get a FileSystem
  for uri's scheme and authority. Fallback to the default filesystem if no scheme
  is specified in the uri.

- ``public static FileSystem get(URI uri, Configuration conf, String user)``. get
  a FileSystem for uri's scheme and authority, perform the get as user. Useful if
  security is enabled.

- ``public static LocalFileSystem getLocal(Configuration conf)``. get the local
  FileSystem.

instance methods
""""""""""""""""
- ``public FSDataInputStream open(Path f)``. Opens an FSDataInputStream at the
  indicated Path. Use 4K buffer.

- ``public abstract FSDataInputStream open(Path f, int bufferSize)``. Open an
  FSDataInputStream at the Path f, using a buffer of bufferSize.

- ``public FSDataOutputStream create(Path f) throws IOException``. Create an
  FSDataOutputStream at the indicated Path. Files are overwritten by default.

- ``public FSDataOutputStream create(Path f, Progressable progress) throws IOException``.
  Create an FSDataOutputStream at the indicated Path with write-progress
  reporting. Files are overwritten by default.

- ``public FSDataOutputStream append(Path f) throws IOException``. append to an
  existing file.

- ``public boolean exists(Path f) throws IOException``. Check if a path exists.

- ``public boolean mkdirs(Path f) throws IOException``. Create directory and
  all necessary parent directories with default permissions. Reutrns true if
  directories are successfully created.

- ``public abstract FileStatus getFileStatus(Path f) throws IOException``.
  Return a FileStatus object that represents the path. Throws
  FileNotFoundException when path does not exist.

- ``public abstract FileStatus[] listStatus(Path f) throws FileNotFoundException, IOException``.
  List the statuses of the files/directories in the given path if the path is a
  directory.

- ``public FileStatus[] listStatus(Path f, PathFilter filter) throws FileNotFoundException, IOException``.
  List files/directories using filter.

- ``public FileStatus[] listStatus(Path[] files) throws FileNOtFoundException, IOException``.
  List the statuses of the files/directories in the given list of paths.

- ``public FileStatus[] listStatus(Path[] files, PathFilter filter) throws FileNOtFoundException, IOException``.
  List files/directories using filter.

- ``public FileStatus[] globStatus(Path pathPattern) throws IOException``.
  Return all the files that match filePattern and are not checksum files.
  Results are sorted by their names. Hadoop supports the same set of glob
  characters as the Unix bash shell.

- ``public FileStatus[] globStatus(Path pathPattern, PathFilter filter) throws IOException``.
  Return an array of FileStatus objects whose path names match pathPattern and
  is accepted by the user-supplied path filter.

- ``public abstract boolean delete(Path f, boolean recursive) throws IOException``.
  delete a file or directory. If path is a directory and set to true, the
  directory is deleted. In case of a file the recursive can be set to either
  true or false.

public class FsUrlStreamHandlerFactory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A factory class for handler of hadoop compatible filesystem's url scheme.

public class Path
^^^^^^^^^^^^^^^^^
- Names a file or directory in a FileSystem. Path strings use slash as the
  directory separator.

public class FileStatus
^^^^^^^^^^^^^^^^^^^^^^^
- A class encapsulates filesystem metadata for files and directories.

instance methods
""""""""""""""""
- ``public Path getPath()``.

- ``public boolean isDirectory()``.

- ``public long getLen()`` the length of this file, in bytes.

- ``public long getModificationTime()``. get modification time of the file,
  as milliseconds since Epoch.

- ``public short getReplication()``. get replication factor.

- ``public long getBlockSize()``. block size of the file, in bytes.

- ``public String getOwner()``. owner of the file in string.

- ``public String getGroup()``. group of the file in string.

- ``public FsPermission getPermission()``.


public class FileUtil
^^^^^^^^^^^^^^^^^^^^^
- A collection of file-processing util methods.

static methods
""""""""""""""
- ``public static Path[] stat2Paths(FileStatus[] stats)``. convert an array of
  FileStatus to an array of Path.

public class FSDataInputStream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- a specialization of java.io.DataInputStream with support for random access.

public class FSDataOutputStream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Utility that wraps a OutputStream in a DataOutputStream. does not permit
  seeking. This is because HDFS allows only sequential writes to an open file
  or appends to an already written file.

instance methods
""""""""""""""""
- ``public long getPos()``. get current position in the output stream.

- ``public void hflush() throws IOException``. Flush out the data in client's
  user buffer. After the return of this call, new readers will see the data.

- ``public void hsync() throws IOException``. Similar to posix fsync, flush out
  the data in client's user buffer all the way to the disk device (but the disk
  may have it in its cache).

public interface Seekable
^^^^^^^^^^^^^^^^^^^^^^^^^
- Stream that permits seeking

instance methods
""""""""""""""""
- ``void seek(long pos) throws IOException``. Seek to the pos from the start of
  the file. Calling ``seek()`` with a position that is greater than the length
  of the file will result in an IOException. Calling ``seek()`` is a relatively
  expensive operation and should be done sparingly.

- ``long getPos() throws IOException``. Return the current offset from the
  start of the file.

public interface PositionedReadable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Stream that permits positional reading.

instance methods
""""""""""""""""
- ``int read(long position, byte[] buffer, int offset, int length) throws IOException``.
  Read up to the length number of bytes, from a given position within a file,
  into buffer, starting at offset, and return the number of bytes read. *This
  does not change the current offset of a file.*

- ``void readFully(long position, byte[] buffer, int offset, int length) throws IOException``.
  Read *exact* length number of bytes, from a given position within a file.
  This does not change the current offset of a file. Throws EOFException if the
  end of the data was reached before the read operation completed.

- ``void readFully(long position, byte[] buffer) throws IOException``.
  Read *exact* buffer.length number of bytes, from a given position within a
  file. This does not change the current offset of a file. Throws EOFException
  as above.

public interface PathFilter
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- a filter for file Path.

instance methods
""""""""""""""""
- ``boolean accept(Path path)``. returns true if path should be included in a
  pathname list. false otherwise.

org.apache.hadoop.io
--------------------
class IOUtils
^^^^^^^^^^^^^
- An utility class for I/O related functionality.

static methods
""""""""""""""
- ``public static void copyBytes(InputStream in, OutputStream out, int buffSize, boolean close)``.
  copy from in stream to out stream, using a buffer of buffSize, optionally
  close in and out stream at the end (in finally clause, therefore always
  performed).

- ``public static void closeStream(Closable stream)``. close the stream ignoring Throwable.


org.apache.hadoop.conf
----------------------
public class Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^
- A class representing hadoop's configuration.

org.apache.hadoop.util
----------------------
public interface Progressable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A facility for reporting progress.

instance methods
""""""""""""""""
- ``void progress()``. Report progress.

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
.. [QuoraAppMaster] `What is container and Application Master in Hadoop. Can anyone explain this? <https://www.quora.com/What-is-container-and-Application-Master-in-Hadoop-Can-anyone-explain-this>`_
.. [MapRAM] `ApplicationMaster <https://mapr.com/docs/60/MapROverview/c_application_master.html>`_

questions
=========
- what's WebAppProxy?

- content of ``*-env.sh``

- To configure the Hadoop cluster you will need to configure the environment in
  which the Hadoop daemons execute as well as the configuration parameters for
  the Hadoop daemons?
