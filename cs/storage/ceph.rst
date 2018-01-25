Questions
=========
- reliable and complete installation procedure?

- seriously, how many daemons are there?

- how to make configuration taking effect immediately? Must reboot?

- commands: rbd, rados, ceph?? relations??

- what is placement group?? what's the effect of different number of pgs?

- how to share something between clients?

- what's the point of rados block device?

- wtf is CRUSH?

- mount cephfs using default tunables requires kernel 4.5+.

- RADOS paper. https://ceph.com/wp-content/uploads/2016/08/weil-rados-pdsw07.pdf

- CRUSH algorithm paper. https://ceph.com/wp-content/uploads/2016/08/weil-crush-sc06.pdf

- Paxos algorithm.

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

CRUSH algorithm
~~~~~~~~~~~~~~~
CRUSH is used to compute object location.

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
