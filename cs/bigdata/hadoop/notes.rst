overview
========
- Hadoop is a framework for distributed storage and distributed processing
  of big data using the MapReduce programming model.

- naming: Hadoop the name is meaningless, the yellow elephant is also
  meaningless.  According to Doug Cutting, it's the name his kid given to a
  stuffed yellow elephant. [OriginHadoop]_

- Hadoop was inspired by two Google papers:
 
  * Google File System (October 2003)

  * MapReduce: Simplified Data Processing on Large Clusters (December 2004)

- Hadoop was born out of Apache Nutch project, a web crawler/search engine.

- Some of the now separate Apache projects were born from Hadoop project,
  including HBase, Hive, Pig, Zookeeper, etc.

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
