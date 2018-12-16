overview
========
- NTP: Network Time Protocol.

- One of the oldest Internet protocols in current use.

- Designed by David L. Mills.

- NTP is used for clock synchronization between computer systems. It uses the
  intersection algorithm, a modified version of Marzullo's algorithm, to select
  accurate time servers and is designed to mitigate the effects of variable
  network latency. NTP can usually maintain time to within tens of milliseconds
  over the public Internet, and can achieve better than one millisecond
  accuracy in local area networks under ideal conditions.

networking architecture
=======================
- a client-server model, but can as easily be used in peer-to-peer
  relationships where both peers consider the other to be a potential time
  source.
  
- They can also use broadcasting or multicasting.

- UDP, port 123.

design
======

clock stratum
-------------
- NTP time sources are hierarchical. Each level of this hierarchy is termed a
  stratum and is assigned a number starting with zero.

- A server synchronized to a stratum n server runs at stratum n + 1.

stratum 0
^^^^^^^^^
- high-precision clock devices: atomic clock, GPS, radio clock, etc.  Connected
  to a computer, which converts its physical ticks into digital timestamps.

- they are reference clocks.

stratum 1
^^^^^^^^^
- Servers that are synced to within a few microseconds (us) to stratum 0.

- they have direct connection to stratum 0 devices.

- stratum 1 servers may network/peer for checking and backup.

- they are primary time servers.

stratum 2
^^^^^^^^^
- synced over network to stratum 1.

- they often query several stratum 1 servers.

- they may peer to be more stable and robust.

stratum 3
^^^^^^^^^
- functionally similar to stratum 2.

clock synchronization algorithm
-------------------------------
.. TODO understand it

reference identifiers
=====================
- GOES. Geostationary Operational Environmental Satellite.

- GPS. Global Positioning System

- GAL. Galileo Positioning System

- PPS. Generic pulse-per-second

- IRIG. Inter-Range Instrumentation Group

- WWVB. LF Radio WWVB Ft. Collins, CO 60 kHz

- DCF. LF Radio DCF77 Mainflingen, DE 77.5 kHz

- ...

software implementations
========================
- Chrony

- windows time service

- Ntimed

version
=======
- NTPv4
