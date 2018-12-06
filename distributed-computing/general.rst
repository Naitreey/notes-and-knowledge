CAP theorem
===========
it is impossible for a distributed data store to simultaneously provide more
than two out of the following three guarantees:

- Consistency: Every read receives the most recent write or an error

- Availability: Every request receives a (non-error) response – without the
  guarantee that it contains the most recent write

- Partition tolerance: The system continues to operate despite an arbitrary
  number of messages being dropped (or delayed) by the network between nodes

No distributed system is safe from network failures, thus network partitioning
generally has to be tolerated. In the presence of a partition, one is then left
with two options: consistency or availability. When choosing consistency over
availability, the system will return an error or a time-out if particular
information cannot be guaranteed to be up to date due to network partitioning.
When choosing availability over consistency, the system will always process the
query and try to return the most recent available version of the information,
even if it cannot guarantee it is up to date due to network partitioning.

In the absence of network failure – that is, when the distributed system is
running normally – both availability and consistency can be satisfied.

The choice is really between consistency and availability only when a network
partition or failure happens; at all other times, no trade-off has to be made.
