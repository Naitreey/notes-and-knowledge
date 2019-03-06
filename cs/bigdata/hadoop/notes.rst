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

- Some of the now separate Apache projects were born from Hadoop project,
  including HBase, Hive, Pig, Zookeeper, etc.

architecture
============
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
  applications.

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

YARN
====

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
namenode
^^^^^^^^
::

  hdfs namenode -format <cluster_name>
  hdfs [--daemon (start|status|stop)] namenode

datanode
^^^^^^^^
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

questions
=========
- what's WebAppProxy?

- content of each configuration file

- content of ``*-env.sh``

- To configure the Hadoop cluster you will need to configure the environment in
  which the Hadoop daemons execute as well as the configuration parameters for
  the Hadoop daemons?

- starting historyserver, hdfs user, permission?
