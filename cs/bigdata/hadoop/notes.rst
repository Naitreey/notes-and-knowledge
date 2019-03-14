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
- At storage layer, hadoop uses a plugin model, different FS implementation can
  be used. The default is HDFS.

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
Architecture
------------
design goals
^^^^^^^^^^^^
- Highly fault-tolerant, designed to run on commodity hardware. Detection of
  faults and quick, automatic recovery from hardware failures.

- Streaming access to data set. Hadoop applications are not general purpose
  application that runs on general purpose file system. HDFS is designed more
  for batch processing rather than interactive use. The emphasis is on high
  throughput of data access rather than low latency of data access. POSIX
  imposes many hard requirements that are not needed for applications that are
  targeted for HDFS, therefore POSIX semantics in a few key areas has been
  traded to increase data throughput rates.

- Large data set. Tuned to support large files. high aggregate data bandwidth
  and scale to hundreds of nodes in a single cluster. It should support tens of
  millions of files in a single instance.

- simple conherency model, write-once-read-many access model. A file once
  created, written, and closed need not be changed except for appends and
  truncates. This assumption simplifies data coherency issues and enables high
  throughput data access.

- It is often better to migrate the computation closer to where the data is
  located rather than moving the data to where the application is running.
  HDFS provides interfaces for applications to move themselves closer to where
  the data is located.

- Portability across heterogeneous hardware and software platforms. (JVM)

services
^^^^^^^^
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

- NameNode

  * executes file system namespace operations like opening, closing, and
    renaming files and directories.

  * manage the mapping of blocks to DataNodes.

  * the arbitrator and repository for all HDFS metadata. user data never flows
    through the NameNode.

- DataNode

  * file blocks are stored in DataNodes.

  * serving read and write requests from clients directly.

  * block creation, deletion, and replication upon instruction from the
    NameNode.

file system namespace
^^^^^^^^^^^^^^^^^^^^^
- traditional hierarchical file organization.

- traditional file/directory operations are supported.

- hardlinks and symlinks are not supported.

- Files are write-once except for append and truncate. Strictly one writer at
  any time (per file).

data replication
^^^^^^^^^^^^^^^^
overview
""""""""
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
""""""""""""""""""""""""""
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
""""""""""""""""""""""""
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

NameNode safemode
""""""""""""""""""
NameNode 启动后首先进入 safemode, 此时不做 replication. NameNode 此时只接收
DataNode 的 heartbeat and blockreport. NameNode 根据 blockreport 检查 safely
replicated blocks 和 unsafe 的 blocks. After a configurable percentage of
safely replicated data blocks checks in with the NameNode, the NameNode exits
safemode. 开始 replicate 在 safemode 得到的那些尚未安全地复制的 blocks.


metadata persistence
^^^^^^^^^^^^^^^^^^^^
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

- NameNode keeps an image of the entire file system namespace and file Blockmap
  in memory. A FsImage checkpoint is triggered at NameNode startup and a
  configured interval. During the checkpoint, NameNode reads EditLog from disk,
  applies all the transactions from the EditLog to the in-memory representation
  of the FsImage, and flushes out this new version into a new FsImage on disk.
  It can then truncate the old EditLog.

data persistence
^^^^^^^^^^^^^^^^
- DataNode has no knowledge about HDFS files.

- each block of HDFS data is stored in a separate file in DataNode's local file
  system.

- Datanode uses a heuristic to determine the optimal number of files per
  directory and creates subdirectories appropriately.

- blockreport. When a DataNode starts up, it scans through its local file
  system, generates a list of all HDFS data blocks, and sends this report to
  the NameNode.

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

- Data integrity. HDFS client software implements checksum checking on the
  contents of HDFS files. When a client creates an HDFS file, it computes a
  checksum of each block of the file and stores these checksums in a separate
  hidden file in the same HDFS namespace. When a client retrieves file contents
  it verifies that the data it received from each DataNode matches the checksum
  stored in the associated checksum file. If not, then the client can opt to
  retrieve that block from another DataNode that has a replica of that block.

- metadata fail-safety. Corruption of FsImage and/or EditLog can cause HDFS
  instance non-functional. Fail-safety can be achieved via:
 
  * maintaining multiple copies of the FsImage and EditLog at NameNode. Any
    update to either the FsImage or EditLog causes each of the FsImages and
    EditLogs to get updated synchronously.

  * HA with distributed edit log.

- Snapshot. useful to roll back a corrupted HDFS instance to a previously known
  good point in time.

data accessibility
^^^^^^^^^^^^^^^^^^
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

- MapReduce is:

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

- API. Java, C++, Ruby, Python, etc.

Tools
=====
Hadoop Streaming
----------------
- Hadoop streaming is a utility that allows MapReduce jobs to be created and
  run with any executables/scripts as mapper or reducer.

- 称这种处理为 streaming, 只是因为以 executable/script 的输入输出做 map 和
  reduce 各自的输入和输出. 就像流过了用户提供的 mapper 和 reducer 程序. 但
  这并不是实时的流处理那种感觉.

Mechanism
^^^^^^^^^
- mapper.
 
  * Each mapper task will launch the executable as a separate process when the
    mapper is initialized. As the mapper task runs, it converts its inputs into
    lines and feed the lines to the stdin of the process. In the meantime, the
    mapper collects the line oriented outputs from the stdout of the process
    and converts each line into a key/value pair, which is collected as the
    output of the mapper.

  * By default, the prefix of a line up to the first tab character is the key
    and the rest of the line will be the value. If there is no tab character in
    the line, then entire line is considered as key and the value is null.

- reducer.

  * When an executable is specified for reducers, each reducer task will launch
    the executable as a separate process then the reducer is initialized. As
    the reducer task runs, it converts its input key/values pairs into lines
    and feeds the lines to the stdin of the process. In the meantime, the
    reducer collects the line oriented outputs from the stdout of the process,
    converts each line into a key/value pair, which is collected as the output
    of the reducer.

  * By default, the prefix of a line up to the first tab character is the key
    and the rest of the line is the value.

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

  hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-X.X.X.jar \
    [genericOptions] [commandOptions]
  $HADOOP_HOME/bin/mapred streaming \
    [genericOptions] [commandOptions]

- generic options

  * ``-conf <config-file>``

  * ``-D property=value``. specify/override configs of mapred-site.xml.

  * ``-fs host:port or local``. namenode to connect to.

  * ``-files file1,fil2,...``. comma-separated files to be made available to
    jobs. Each file is URI to the file or archive that you have already
    uploaded to HDFS.

  * ``-libjars file1,file2,...``. comma-separated jar files to include in the
    classpath. Each jar is URI to the file or archive that you have already
    uploaded to HDFS.

  * ``-archives archive1,...``. archives to be unarchived on the compute
    machines.

- streaming options

  * ``-input <file-or-directory>``. input for mapper.

  * ``-output <directory>``. output location for reducer.

  * ``-mapper <executable-path-or-java-class-name>``. mapper used for map
    stage. default is org.apache.hadoop.mapred.lib.IdentityMapper.

  * ``-reducer <executable-path-or-java-class-name>``. reducer used for reduce
    stage. default is org.apache.hadoop.mapred.lib.IdentityMapper.

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

  * ``-partitioner <java-class-name>``

  * ``-combiner <executable-path-or-java-class-name>``

  * ``-cmdenv key=val`` environ to be passed to streaming cmds.

  * ``-verbose``

  * ``-lazyOutput``

  * ``-numReduceTasks <n>``. the number of reduce tasks.

  * ``-mapdebug <executable-path>``. script to call when map task failed.

  * ``-reducedebug <executable-path>``. script to call when reduce task failed.

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
resourcemanager
^^^^^^^^^^^^^^^
::

  yarn [--daemon (start|status|stop)] resourcemanager

nodemanager
^^^^^^^^^^^
::

  yarn [--daemon (start|status|stop)] nodemanager

proxyserver
^^^^^^^^^^^
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
