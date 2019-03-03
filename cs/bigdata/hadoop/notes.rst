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
NameNode
^^^^^^^^
- Usually running on a dedicated node in the cluster.

Secondary NameNode
^^^^^^^^^^^^^^^^^^

DataNode
^^^^^^^^
- 对每个需要存储数据的节点都要运行 DataNode (存储节点).

ResourceManager
^^^^^^^^^^^^^^^
- Usually running on a dedicated node in the cluster.

NodeManager
^^^^^^^^^^^
- 对每个要执行计算任务的节点要运行 NodeManager (计算节点).

File systems
------------
- At storage layer, hadoop uses a plugin model, different FS implementation can
  be used.

- Location awareness of Hadoop compatible file systems.

  For effective scheduling of work, every Hadoop-compatible file system should
  provide location awareness, which is the name of the rack, specifically the
  network switch where a worker node is.
  
  Location-awareness makes the following possible:
  
  * Schedule map and reduce tasks on nodes which the data is located at or near
    (e.g., on the same rack/switch).
  
  * data replication is performed so that data redundancy is ensured across
    multiple racks.

- alternatvie file systems:

  * Amazon S3

  * Windows Azure Storage Blobs file system

  * IBM General Parallel File System

  * MapR's MapRFS.

  * FTP

HDFS
^^^^
- When Hadoop MapReduce is used with an alternate file system, the NameNode,
  standby NameNode, and DataNode architecture of HDFS are replaced by the
  file-system-specific equivalents.

Distributors
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
