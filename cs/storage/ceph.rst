Questions
=========
- reliable and complete installation procedure?

- how to make configuration taking effect immediately? Must reboot?

- what is placement group?? what's the effect of different number of pgs?

- wtf is CRUSH?

- mount cephfs using default tunables requires kernel 4.5+.

- RADOS paper. https://ceph.com/wp-content/uploads/2016/08/weil-rados-pdsw07.pdf

- CRUSH algorithm paper. https://ceph.com/wp-content/uploads/2016/08/weil-crush-sc06.pdf

- Paxos algorithm.

- erasure coding.

- WTF erasure coding has to do with PGs, replicas and anything?
  https://ceph.com/community/new-luminous-erasure-coding-rbd-cephfs/

- PG logs?

- WTF is epoch here?

- data striping.

- cephfs non-root read/write.
  目前知道可以 chown 来让 non-root 读写. 不知是否最优.

Overview
========
- Ceph 以及对象存储的好处.

  * 应用只需和抽象的 object storage 打交道, 很简单. 它背后的整个集群, 以及
    所有复杂的 routing/replication 等等逻辑, 全部封装成简单的接口. 应用无需
    关心存储细节.

  * object/object group 这个抽象层, 让数据可以在集群中漂移, 让 replication
    和 rebalancing 等自稳定操作更方便, 对上层应用是完全透明的.

  * 一个文件可以使用位于不同 PG 的多组 objects 来存储, 类似于 RAID, 多台节点
    同时 serve 读写, 大大提高存储效率.

  * Replication 带来的 HA.

- 分布式存储一般用于存储非常大量的 binary data, 例如虚拟机镜像, 图片, 任意类型的
  文件 (Dropbox). 它与分布式数据库或搜索引擎的用处是不同的.

- Object Storage Device 在 iSCSI 协议中有定义. SCSI command set 中有定义.

Architecture
============

terms
-----
- RADOS. Reliable Autonomic Distributed Object Store.
  The storage system of ceph. 由 monitor + OSD daemon 构成.

- OSD. Object Storage Device. A physical or logical storage unit.

- Ceph OSD Daemon. ceph OSD software that interacts with OSD.

- MDS. The Ceph metadata software.

- RBD. RADOS Block Device.

- Ceph Client. The collection of Ceph components which can access a Ceph
  Storage Cluster. These include the Ceph Object Gateway, the Ceph Block
  Device, the Ceph Filesystem, and their corresponding libraries, kernel
  modules, and FUSEs.

  Note Ceph Client differs from Ceph client node.

functionalities
---------------
- librados. a native interface to the Ceph Storage Cluster.

- radosgw. a RESTful API gateway built on librados.

- RBD. a block device built on librados.

- CephFS. a POSIX-compliant distributed file system.

the ceph storage cluster
------------------------
A RADOS cluster consists of two types of daemons: monitor, OSD daemon.

A Ceph Monitor maintains a master copy of the cluster map. A cluster of
monitors ensures HA. Ceph Clients retrieve cluster map from monitor.

OSD Daemon checks its own state and the state of other OSDs and reports back to
monitors.

Ceph Clients and OSD daemons use the CRUSH algorithm to compute data location.

storing data
~~~~~~~~~~~~
data are stored as objects. each object corresponds to a file in a filesystem.
Ceph OSD Daemons handle the read/write operations on OSD.

Ceph OSD Daemons store all data as objects in a flat namespace.  An object has
an identifier, binary data, and metadata consisting of a set of name/value
pairs. Content of metadata varies by Ceph Clients.

scalability and HA
~~~~~~~~~~~~~~~~~~
In traditional architectures, clients talk to a centralized component (e.g., a
gateway, broker, API, facade, etc.), which acts as a single point of entry to a
complex subsystem. This imposes a limit to both performance and scalability,
while introducing a single point of failure (i.e., if the centralized component
goes down, the whole system goes down, too).

In Ceph, Ceph Clients object locations and talk to OSD daemons directly.
Ceph OSD Daemons create object replicas on other Ceph Nodes to ensure data
safety and high availability.  Ceph also uses a cluster of monitors to ensure
high availability. To eliminate centralization, Ceph uses an algorithm called
CRUSH.

In a cluster of monitors, latency and other faults can cause one or more
monitors to fall behind the current state of the cluster. For this reason, Ceph
must have agreement among various monitor instances regarding the state of the
cluster. Ceph always uses a majority of monitors (e.g., 1, 2:3, 3:5, 4:6, etc.)
and the Paxos algorithm to establish a consensus among the monitors about the
current state of the cluster.

For high availability, a Ceph Storage Cluster should store more than two copies
of an object (e.g., size = 3 and min size = 2) so that it can continue to run
in a degraded state while maintaining data safety.

cluster map
~~~~~~~~~~~
Cluster map is the cluster topology.

Ceph Monitors maintain a master copy of the cluster map including the cluster
members, state, changes, and the overall health of the Ceph Storage Cluster.
Ceph Clients and OSD daemons need to know cluster topology to operate.

- Monitor map. Contains the cluster fsid, the position, name, address and port
  of each monitor. It also indicates the current epoch, when the map was
  created, and the last time it changed.

- OSD map. Constains the cluster fsid, when the map was created and last
  modified, a list of pools, replica sizes, PG numbers, a list of OSDs and
  their status.

- PG map. Contains the PG version, its time stamp, the last OSD map epoch, the
  full ratios, and details on each placement group such as the PG ID, the Up
  Set, the Acting Set, the state of the PG (e.g., active + clean), and data
  usage statistics for each pool.

- CRUSH map. Contains a list of storage devices, the failure domain hierarchy
  (e.g., device, host, rack, row, room, etc.), and rules for traversing the
  hierarchy when storing data.

- MDS map. Contains the current MDS map epoch, when the map was created, and
  the last time it changed.

CRUSH algorithm
~~~~~~~~~~~~~~~
Ceph Clients use CRUSH to compute object location.  Ceph OSD Daemons use CRUSH
to compute where replicas of objects should be stored (and for rebalancing).

In a typical write scenario, a client uses the CRUSH algorithm to compute where
to store an object, maps the object to a pool and placement group, then looks
at the CRUSH map to identify the primary OSD for the placement group.  The
client writes the object to the identified placement group in the primary OSD.
Then, the primary OSD with its own copy of the CRUSH map identifies the
secondary and tertiary OSDs for replication purposes, and replicates the object
to the appropriate placement groups in the secondary and tertiary OSDs (as many
OSDs as additional replicas), and responds to the client once it has confirmed
the object was stored successfully.

Pools are logical partitions for storing objects. Ceph Clients retrieve a
Cluster Map from a Ceph Monitor, and write objects to pools. The pool’s size or
number of replicas, the CRUSH rule and the number of placement groups determine
how Ceph will place the data.

Each pool has a number of placement groups. CRUSH maps PGs to OSDs dynamically.
When a Ceph Client stores objects, CRUSH will map each object to a placement
group.

Mapping objects to placement groups creates a layer of indirection between the
Ceph OSD Daemon and the Ceph Client. The Ceph Storage Cluster must be able to
grow (or shrink) and rebalance where it stores objects dynamically. If the Ceph
Client “knew” which Ceph OSD Daemon had which object, that would create a tight
coupling between the Ceph Client and the Ceph OSD Daemon. Instead, the CRUSH
algorithm maps each object to a placement group and then maps each placement
group to one or more Ceph OSD Daemons. This layer of indirection allows Ceph to
rebalance dynamically when new Ceph OSD Daemons and the underlying OSD devices
come online.

calculating PG ID. The only input required by the client is the object ID and
the pool.

1. Ceph Client takes the object ID and hashes it.

2. Ceph Client calculates the hash modulo the number of PGs to get a PG ID.

3. Ceph Client prepends the pool ID to the PG ID.

Now that we have PG ID, we can use cluster map to find the OSD daemon to
store object.

peering
~~~~~~~
Peering is the process of bringing all of the OSDs that store a Placement Group
(PG) into agreement about the state of all of the objects (and their metadata)
in that PG. Ceph OSD Daemons Report Peering Failure to the Ceph Monitors.

When a series of OSDs are responsible for a placement group, that series of
OSDs, we refer to them as an Acting Set. By convention, the Primary is the
first OSD in the Acting Set, and is responsible for coordinating the peering
process for each placement group where it acts as the Primary, and is the ONLY
OSD that that will accept client-initiated writes to objects for a given
placement group where it acts as the Primary.

The Ceph OSD daemons that are part of an Acting Set may not always be up. When
an OSD in the Acting Set is up, it is part of the Up Set. The Up Set is an
important distinction, because Ceph can remap PGs to other Ceph OSD Daemons
when an OSD fails.

rebalancing
~~~~~~~~~~~
Cluster map is changed when a Ceph OSD Daemon is added to or removed from
cluster. PGs are re-mapped to the new cluster map, and rebalanced.

authentication
~~~~~~~~~~~~~~
Ceph uses cephx authentication system to authenticate users and daemons.

Cephx uses shared secret keys for authentication, meaning both the client and
the monitor cluster have a copy of the client’s secret key.  Both parties are
able to prove to each other they have a copy of the key without actually
revealing it. This provides mutual authentication, which means the cluster is
sure the user possesses the secret key, and the user is sure that the cluster
has a copy of the secret key.

A user/actor invokes a Ceph client to contact a monitor. Each monitor can
authenticate users and distribute keys, so there is no single point of failure
or bottleneck when using cephx. The monitor returns a data structure that
contains a session key for use in obtaining Ceph services. This session key is
itself encrypted with the user’s permanent secret key, so that only the user
can request services from the Ceph Monitor(s). The client then uses the session
key to request its desired services from the monitor, and the monitor provides
the client with a ticket that will authenticate the client to the OSDs that
actually handle data. Ceph Monitors and OSDs share a secret, so the client can
use the ticket provided by the monitor with any OSD or metadata server in the
cluster. cephx tickets expire, so an attacker cannot use an expired ticket or
session key obtained surreptitiously.

To use cephx, an administrator must set up users first. The client.admin user
tell cluster to generate a user and secret key. Ceph’s auth subsystem generates
the username and key, stores a copy with the monitor(s) and transmits the
user’s secret back.

status monitoring
~~~~~~~~~~~~~~~~~
The OSDs periodically send messages to the Ceph Monitor. If the Ceph Monitor
doesn’t see that message after a configurable period of time then it marks the
OSD down. This mechanism is a failsafe, however. Normally, Ceph OSD Daemons
will determine if a neighboring OSD is down and report it to the Ceph
Monitor(s).

data scrubbing
~~~~~~~~~~~~~~
As part of maintaining data consistency and cleanliness, Ceph OSD Daemons can
scrub objects within placement groups. That is, Ceph OSD Daemons can compare
object metadata in one placement group with its replicas in placement groups
stored on other OSDs. Scrubbing (usually performed daily) catches bugs or
filesystem errors. Ceph OSD Daemons also perform deeper scrubbing by comparing
data in objects bit-for-bit. Deep scrubbing (usually performed weekly) finds
bad sectors on a drive that weren’t apparent in a light scrub.

erasure coding
~~~~~~~~~~~~~~
EC pool 是从 luminous 开始的一种新的数据存储方式. 这种方式在保证 HA 的基础上,
相比 replica 方式能大大减少存储空间占用.

If you are writing lots of data into big objects, EC pools are usually faster
then replicated pools: less data is being written (only 1.5x what you provided,
vs 3x for replication).  The OSD processes consume a lot more CPU than they did
before, however, so if your servers are slow you may not realize any speedup.

Small writes, however, are slower than replication, for two main reasons:

- First, all writes have to update the full stripe (all k + m OSDs), which is
  usually a larger number of OSDs than you would have replicas. That increases
  latency.

- Second, if a write only updates part of a stripe, we need to read in the
  previous value of the stripe (from all k + m OSDs), make our update,
  reencode, and then write the updated shards out again.  For this reason we
  tend to make stripes very small by default (trading some CPU overhead for a
  lower likelihood of a partial stripe update), but the problem doesn’t always
  go away.

cache tier
~~~~~~~~~~
Cache tiering involves creating a pool of relatively fast/expensive storage
devices (e.g., solid state drives) configured to act as a cache tier, and a
backing pool of either erasure-coded or relatively slower/cheaper devices
configured to act as an economical storage tier.

ceph protocol
-------------
Ceph packages ceph protocol into the librados library so that you can create
your own custom Ceph Clients.

object watch/notify
~~~~~~~~~~~~~~~~~~~
looks like advanced inotify.

data striping
~~~~~~~~~~~~~
The most common form of data striping comes from RAID. The RAID type most
similar to Ceph’s striping is RAID 0, or a ‘striped volume’. Ceph’s striping
offers the throughput of RAID 0 striping, the reliability of n-way RAID
mirroring and faster recovery.

A Ceph Client converts its data from the representation format it provides to
its users (a block device image, RESTful objects, CephFS filesystem directories)
into objects for storage in the Ceph Storage Cluster.

The objects Ceph stores in the Ceph Storage Cluster are not striped. Ceph
Object Storage, Ceph Block Device, and the Ceph Filesystem stripe their data
over multiple Ceph Storage Cluster objects. Ceph Clients that write directly to
the Ceph Storage Cluster via librados must perform the striping (and parallel
I/O) for themselves to obtain these benefits.

The simplest Ceph striping format involves a stripe count of 1 object. Ceph
Clients write stripe units to a Ceph Storage Cluster object until the object is
at its maximum capacity, and then create another object for additional stripes
of data. The simplest form of striping may be sufficient for small block device
images, S3 or Swift objects and CephFS files. However, this simple form doesn’t
take maximum advantage of Ceph’s ability to distribute data across placement
groups, and consequently doesn’t improve performance very much.

If you anticipate large images sizes, large S3 or Swift objects (e.g., video),
or large CephFS directories, you may see considerable read/write performance
improvements by striping client data over multiple objects within an object
set. Significant write performance occurs when the client writes the stripe
units to their corresponding objects in parallel. Since objects get mapped to
different placement groups and further mapped to different OSDs, each write
occurs in parallel at the maximum write speed. A write to a single disk would
be limited by the head movement (e.g. 6ms per seek) and bandwidth of that one
device (e.g. 100MB/s). By spreading that write over multiple objects (which map
to different placement groups and OSDs) Ceph can reduce the number of seeks per
drive and combine the throughput of multiple drives to achieve much faster
write (or read) speeds.

Once the Ceph Client has striped data to stripe units and mapped the stripe
units to objects, Ceph’s CRUSH algorithm maps the objects to placement groups,
and the placement groups to Ceph OSD Daemons before the objects are stored as
files on a storage disk.

ceph clients
------------

RADOS gateway
~~~~~~~~~~~~~
a FastCGI service that provides a RESTful HTTP API to store objects and
metadata.

RADOS block device
~~~~~~~~~~~~~~~~~~
A Ceph Block Device stripes a block device image over multiple objects in the
Ceph Storage Cluster, where each object gets mapped to a placement group and
distributed, and the placement groups are spread across separate ceph-osd
daemons throughout the cluster.

RBD image 是不能分布式访问的. 只能用在一个 client 上. Ceph stripes a
block device across the cluster for high throughput (read/write) and
replication.

需要 RBD 这种功能是因为, thin-provisioned snapshottable Ceph Block Devices are
an attractive option for virtualization and cloud computing.

CephFS
~~~~~~
a POSIX-compliant filesystem as a service that is layered on top of the
object-based Ceph Storage Cluster.

Ceph FS files get mapped to objects that Ceph stores in the Ceph Storage
Cluster.

Ceph Clients mount a CephFS filesystem as a kernel object or as a Filesystem in
User Space (FUSE).

The purpose of the MDS is to store all the filesystem metadata (directories,
file ownership, access modes, etc) in high-availability Ceph Metadata Servers
where the metadata resides in memory. The reason for the MDS (a daemon called
ceph-mds) is that simple filesystem operations like listing a directory or
changing a directory (ls, cd) would tax the Ceph OSD Daemons unnecessarily. So
separating the metadata from the data means that the Ceph Filesystem can
provide high performance services without taxing the Ceph Storage Cluster.

Ceph FS separates the metadata from the data, storing the metadata in the MDS,
and storing the file data in one or more objects in the Ceph Storage Cluster.
The Ceph filesystem aims for POSIX compatibility. ceph-mds can run as a single
process, or it can be distributed out to multiple physical machines, either for
high availability or for scalability.

High Availability: The extra ceph-mds instances can be standby, ready to take
over the duties of any failed ceph-mds that was active. This is easy because
all the data, including the journal, is stored on RADOS.

Scalability: Multiple ceph-mds instances can be active, and they will split the
directory tree into subtrees (and shards of a single busy directory),
effectively balancing the load amongst all active servers.

Combinations of standby and active etc are possible, for example running 3
active ceph-mds instances for scaling, and one standby instance for high
availability.

RADOS Cluster
=============

user management
---------------

- user capability format::
    <daemon-type> '<cap-list>'
  其中 ``cap-list`` is a comma separated list of capabilities.

CephFS
======

client authentication
---------------------

- 访问 cephfs 的用户不需要使用 ``ceph auth caps`` 对 mon, osd, mds
  各自单独赋权限. 通过 ``ceph fs authorize`` 赋目录权限时, 它会自动
  设置随 mon, osd, mds 的合适权限.

RADOS block device
==================
