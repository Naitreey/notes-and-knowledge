Questions
=========
- reliable and complete installation/uninstallation steps?
  steps to start/stop cluster?
  steps to start/stop every services?

- how to make configuration taking effect immediately? Must reboot?

- what is placement group?? what's the effect of different number of pgs?

- wtf is CRUSH?

- RADOS paper. https://ceph.com/wp-content/uploads/2016/08/weil-rados-pdsw07.pdf

- CRUSH algorithm paper. https://ceph.com/wp-content/uploads/2016/08/weil-crush-sc06.pdf

- Paxos algorithm.

- erasure coding.

- WTF erasure coding has to do with PGs, replicas and anything?
  https://ceph.com/community/new-luminous-erasure-coding-rbd-cephfs/

- PG logs?

- WTF is epoch here?

- how many monitors in cluster is needed?

- what are bootstrap-... keyrings?

- data striping.

- how to: multiple mds, one active, other standby.

- cephfs non-root read/write.
  目前知道可以 chown 来让 non-root 读写. 不知是否最优.
  一个 cephfs 在各个客户端使用时, 必须使用相同的用户或相同的组. 即需要保证
  所要使用的用户都有 POSIX 形式的读写权限. 甚至是 chmod 0777.

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

- Object Storage Device 在 iSCSI 协议中有定义. SCSI command set 中有定义.

Deployment
==========

steps to install
----------------

preparation
~~~~~~~~~~~
- cluster node 若是 ubuntu, 最好是 16.04 以上. 可以考虑升级至最新的内核.
  client node 需要 4.x kernel. kernel 4.8+ 才支持多个 cephfs.

- 首先保证 admin, cluster nodes 等所有节点之间可以两两相互通信, 通过 DNS 或 hosts
  设置.

- admin node 用于控制部署过程. 安装 ceph-deploy package::
    wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
    echo deb https://download.ceph.com/debian-{ceph-release}/ {ubuntu-release} main | sudo tee /etc/apt/sources.list.d/ceph.list
    sudo apt-get update && sudo apt-get install ceph-deploy
  其中, ceph-release 为 `ceph release`_ code name; ubuntu-release 为恰当的
  官方支持的 ubuntu release code name. 很不幸官方到底支持哪些 ubuntu 版本,
  需要去 `download directory`_ 找. 例如, 17.10 系统也得使用 xenial.

- cluster node 上安装 ssh server::
    sudo apt-get install openssh-server

- admin node 设置至所有 cluster node 某用户的 password-less ssh::
    ssh-copy-id {username}@{node}
  设置 ``~/.ssh/config`` 从而连接某个 host 时, 自动使用配置好的用户::
    Host node1
       Hostname node1
       User {username}
    Host node2
       Hostname node2
       User {username}
    Host node3
       Hostname node3
       User {username}

- 每个 cluster node 上的 ssh 用户需要有 passwordless sudo 权限::
    echo "{username} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{username}
    sudo chmod 0440 /etc/sudoers.d/{username}

- cluster node 上安装 ntp server::
    sudo apt install ntp
  配置节点之间互为 ntp peer 并重启::
    # /etc/ntp.conf
    ...
    peer {another-node-hostname}
    peer ...

- admin node 上创建目录保存部署过程中生成的所有文件. 运行 ceph-deploy 是保证
  PWD 在这个目录. 不要使用 sudo.

.. _ceph release: http://docs.ceph.com/docs/master/releases/
.. _download directory: https://download.ceph.com/

deploy RADOS cluster
~~~~~~~~~~~~~~~~~~~~
- install ceph packages on all cluster nodes::
    ceph-deploy install --release {ceph-release} {node}...

- create new cluster::
    ceph-deploy new {monitor-node}...

- 修改 ``ceph.conf`` 添加 ``public network`` setting 为节点 IP 所在子网.

- deploy initial monitors::
    ceph-deploy mon create-initial
  创建 cluster 时, 同时会生成管理员 ``client.admin`` keyring 以及各种 bootstrap
  keyrings, 每个 keyring (用户) 具有用于部署相应的服务的所需权限.

- push configuration and admin.client keyrings to Ceph Nodes. 让
  各个节点成为 admin node, 执行 ceph CLI 时自动以 client.admin 认证::
    ceph-deploy admin {node}...

- add/remove a monitor::
    ceph-deploy mon add {node}
    ceph-deploy mon destroy {node}...
  Ensure that you add or remove monitors such that they may arrive at a consensus
  among a majority of monitors according to Paxos algorithm.

- deploy manager daemons on all monitor hosts::
    ceph-deploy mgr create {monitor-node}...

- deploy Ceph OSD::
    ceph-deploy osd create {node}:{device} ...
  若 OSD 设备本身有分区表信息, 创建会失败. 需要先破坏分区表信息::
    ceph-deploy disk zap {node}:{device}

- remove Ceph OSD::
    ceph osd out {N}
    systemctl stop ceph-osd@{N}.service
    ceph osd purge {N} --yes-i-really-mean-it
    umount /var/lib/ceph/osd/ceph-{N}

- push/pull configuration to cluster nodes::
    ceph config {push|pull} {node}...

- 设置节点为 admin node::
    ceph admin {node}...

deploy CephFS
~~~~~~~~~~~~~
- create MDS servers::
    ceph-deploy mds create {node}...

- create a cephfs filesystem and pools for its data::
    ceph osd pool create <fs>_data <pg_num>
    ceph osd pool create <fs>_metadata <pg_num>
    ceph fs new <fs> <fs>_metadata <fs>_data 
  只能创建一个, 目前创建多个 cephfs 还没有 production ready.

- 创建文件系统的 ceph user, 进行访问控制::
    ceph fs authorize <fs> client.<user> [<directory> <permission>]+
  输出的 key 即是 mount 时需要使用的密码.

- CephFS client kernel >=4.5 才能支持 jewel release 以上的 CRUSH tunables v5
  配置. 否则需要切换至 hammer release 的 tunables v4 profile::
    ceph osd crush tunables hammer

- cephfs user node 安装 ceph packages::
    ceph-deploy install --release {ceph-release} {client-node}...
  客户端系统需要是 ceph 支持的版本.

- 客户端 mount cephfs. 需要 4.x kernel::
    mount -t ceph -o name=<user>,secretfile=<secret-file> \
          <monitor-1>:6789,<monitor-2>:6789,...:<dir-in-fs> <mountpoint>
  secret-file 应保证只有相关用户可读.

- 修改所需访问目录的 owner, group 以及读写权限让客户端 non-root 程序可以读写::
    chown ...
    chmod ...

deploy RGW
~~~~~~~~~~
- 如果需要 RESTful API 访问 ceph cluster, deploy RGW server::
    ceph-deploy rgw create {gateway-node}...
  可以部署在一个 client node 或 cluster node 上.

steps to uninstall
------------------
- 各客户端停止使用 RGW, unmap RBD images, unmount CephFS.

- 删除节点和客户端上的 ceph packages::
    ceph-deploy purge <hostname>...

- 删除节点上的 ceph data::
    ceph-deploy purgedata <hostname>...

- admin node 上删除 ceph-deploy package.

- admin node 上删除 ceph keyrings, configurations, 等等所在目录.

steps to start
--------------

steps to stop
-------------

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

- MGR. Ceph Manager.

- Ceph Client. The collection of Ceph components which can access a Ceph
  Storage Cluster. These include the Ceph Object Gateway, the Ceph Block
  Device, the Ceph Filesystem, and their corresponding libraries, kernel
  modules, and FUSEs.

  Note Ceph Client differs from Ceph client node.

  Irrespective of the type of Ceph client (e.g., Block Device, Object Storage,
  Filesystem, native API, etc.), Ceph stores all data as objects within pools.

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

librados
~~~~~~~~

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

RBD image 是不能同时从多个客户端修改的. 某个 client 对一个 block image 的修改,
不会在其他 client 处同时可见.

Ceph stripes a block device across the cluster for high throughput (read/write)
and replication.

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

configuration
-------------

network settings
~~~~~~~~~~~~~~~~
- public network and cluster network.

  A RADOS cluster should have two networks: a public (front-side) network and a
  cluster (back-side) network. Thus each Ceph Node needs to have 2 NICs.

  Unless you specify a cluster network, Ceph assumes a single “public” network.

- cluster network is dedicated to Ceph OSD network traffics. Advantages:

  * OSD replication and heartbeat performance. When Ceph OSD Daemons replicate
    data more than once, the network load between Ceph OSD Daemons easily
    dwarfs the network load between Ceph Clients and the Ceph Storage Cluster.
    This can introduce latency and create a performance problem.

  * Better security. 只要 cluster network 不连入公网, 就不受 public network
    可能问题的影响. 如果 public network 受到 DDoS 攻击, 不影响 OSD 集群运行.
    从而客户端数据读写不受影响.

monitor settings
~~~~~~~~~~~~~~~~
- Filesystem ID (fsid): the unique identifier for current RADOS cluster,
  Since you can run multiple clusters on the same hardware.

- For high availability, you should run a production Ceph cluster with AT LEAST
  three monitors. Ceph uses the Paxos algorithm, which requires a consensus
  among the majority of monitors in a quorum. With Paxos, the monitors cannot
  determine a majority for establishing a quorum with only two monitors. A
  majority of monitors must be counted as such: 1:1, 2:3, 3:4, 3:5, 4:6, etc.

- Monitors and OSDs should not run on same host.

authentication
--------------

authentication
~~~~~~~~~~~~~~

- 默认开启用户认证. 认证机制为 cephx.

- cephx 在认证时, 需要提供 username 和 keyring file. 若省略用户名,
  默认使用 client.admin; 若省略 keyring,
  Ceph will look for a keyring via the keyring setting in the Ceph
  configuration (一般为 ``/etc/ceph/$cluster.$name.keyring`` 等文件).

authorization
~~~~~~~~~~~~~
- Ceph has the notion of a type of user.
  Ceph identifies users in period (.) delimited form consisting of the user
  type and the user ID ``TYPE.ID``. types are: client, osd, mgr, mds.

- A user capability has following format::
    <daemon-type> '<cap-list>'
  其中 ``cap-list`` is a comma separated list of capabilities::
    cap-list := <cap>, <cap>*
  ``cap`` 的具体格式为::
    cap := allow <access-spec> <match-spec>?
    cap := profile <name>
  ``access-spec`` 限制可以进行的操作, profile 指的是使用预设的某个权限 profile::
    access-spec := * | all | [ r || w || x ]
    access-spec := class <class-name> <method-name>?
  ``match-spec`` 进一步限制允许的 pool 或 namespace::
    match-sepc := pool=<pool-name> [namespace=<namespace-name>]? [object_prefix <prefix>]?
    match-spec := [namespace=<namespace-name>]? tag <application> <key>=<value>

- A typical user has at least read capabilities on the Ceph monitor and read
  and write capability on Ceph OSDs. Additionally, a user’s OSD permissions are
  often restricted to accessing a particular pool.

- 对 RBD user 的权限限制.

  useful profiles.

  * profile rbd (for mon and osd daemon type).

    Gives a user permissions to manipulate RBD images. When used as a Monitor
    cap, it provides the minimal privileges required by an RBD client
    application. When used as an OSD cap, it provides read-write access to an
    RBD client application.

  * profile rbd-read-only (for osd daemon type).

    Gives a user read-only permissions to RBD images.

  还应该进一步限制可访问的 pools.

common operations
~~~~~~~~~~~~~~~~~
 
* list users, keys and capabilities: ``ceph auth ls``

* get a user's info: ``ceph auth get <name>``

* create a user.
  
  - ``ceph auth add``
   
  - ``ceph auth get-or-create``. creat or get (if exists) a user, return
    user keyring.

  - ``ceph auth get-or-create-key``. same as get-or-create, return key
    string only.

* delete a user: ``ceph auth del``.

* set capabilities: ``ceph auth caps``.
  To remove a capability, you may reset the capability. If you want the user to
  have no access to a particular daemon that was previously set, specify an
  empty string.

* print user's key. ``ceph auth print-key``

* import user. ``ceph auth import``.
  The ceph storage cluster will add new users or update existing users, with
  their keys and their capabilities.

commandline options
~~~~~~~~~~~~~~~~~~~
ceph commands 一般支持指定 user name & keyring 的选项:

- ``--name``

- ``--keyring``

keyring
~~~~~~~
Ceph Client 在访问 Ceph Cluster 时, 需要用户的 keyring file. 若没有明确指定
keyring, 自动到以下默认路径尝试:

- ``/etc/ceph/$cluster.$name.keyring``

- ``/etc/ceph/$cluster.keyring``

- ``/etc/ceph/keyring``

- ``/etc/ceph/keyring.bin``

security
~~~~~~~~
The keys used to authenticate Ceph clients and servers are typically stored in
a plain text file with appropriate permissions in a trusted host. 必须保证
只有 trusted user 可以获取 keyfile.

At the moment, none of the Ceph authentication protocols provide secrecy for
messages in transit. Thus, an eavesdropper on the wire can hear and understand
all data sent between clients and servers in Ceph, even if it cannot create or
alter them.

CRUSH map
---------

tunables
~~~~~~~~
Tunable options control what version of CRUSH algorithm is used by cluster.
In order to use newer tunables, both clients and servers must support the new
version of CRUSH.

Tunable profiles are named after the Ceph version in which they were introduced.

operations.

- adjust tunable profile: ``ceph osd crush tunables {profile}``.

- show current tunable values: ``ceph osd crush show-tunables``.

CephFS
======

notes
-----
multiple cephfs
~~~~~~~~~~~~~~~
multiple cephfs 还属于 experimental feature. 并且 kernel 4.8+ 的
kernel client 才支持 mount multiple cephfs (通过 ``mds_namespace``
option).

kernel requirement
~~~~~~~~~~~~~~~~~~
若使用 kernel client mount cephfs, 对 kernel version 有要求.

对于 jewel release 以上的 ceph, client kernel 应该是 4.0+.
对运行 3.x kernel 的 client node, 最好使用 FUSE client.

client authorization
--------------------

- 访问 cephfs 的用户不需要使用 ``ceph auth caps`` 对 mon, osd, mds
  各自单独赋权限. 通过 ``ceph fs authorize`` 赋目录权限时, 它会自动
  设置随 mon, osd, mds 的合适权限.

- 可以给一个 cephfs 里的不同层目录单独分配权限 (r and/or w).
  可以指定 all/``*`` 为 fs name, grant access to every file system.

- 可以指定 client 是否可以修改 layout and quota.

- 可以指定 free space reporting 是 subdirectory or the entire fs.
  If quotas are not enabled, or no quota is set on the sub-directory mounted,
  then the overall usage of the filesystem will be reported irrespective of the
  value of this setting.

configuration
-------------
- You must deploy at least one metadata server to use CephFS. 目前
  对 multiple MDS 的支持还不稳定.

RADOS block device
==================

Ceph Manager
============
MGR provides additional monitoring and interfaces to external monitoring and
management systems.

configuration
-------------
- In general, you should set up a ceph-mgr on each of the hosts running a
  ceph-mon daemon to achieve the same level of availability.

- By default, whichever ceph-mgr instance comes up first will be made active by
  the monitors, and the others will be standbys.
