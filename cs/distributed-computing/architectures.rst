shared-nothing architecture
===========================
- In shared-nothing architecture (SN), each node is independent and
  self-sufficient. No single point of failure. Each node runs their
  portion of work on their own disks or partitions.

- advantage of SN architecture:

  * no single point of failure

  * allowing self-healing

  * allowing no-disruptive upgrade.

  * scalability, by simply adding nodes.

shared-memory architecture
==========================
- In distributed-shared-memory architecture (DSM), physically separated
  memories can be addressed as one logically shared address space.

- Note address space is shared, rather than a single centralized memory
  hardware is used.

- Each node's local memory is connected by a general interconnection network.

- DSM can be seen as an extension to virtual memory

- DSM can be implemented at OS level, or library level.

- advantages:

  * message passing is hidden

  * can handle complex and large databases without replication or sending data
    to processes.

  * Large virtual memory space

  * programs are more portable 由于分布式 primitives are implicit.

- disadvantages:

  * slower to access memory than other architectures

  * Shared memory is extremely sensitive to contention.  Processes must compete
    for access to memory and coordinate their activities at a low level.

shared-disk architecture
========================
- In shared-disk architecture (SD), all disks are accessible from all cluster
  nodes.

- Multiple processors can access all disks directly via intercommunication
  network and every processor has local memory.

- Shared Disk has two advantages over Shared memory. Firstly, each processor
  has its own memory, the memory bus is not a bottleneck; secondly, the system
  offers a simple way to provide a degree of fault tolerance.
