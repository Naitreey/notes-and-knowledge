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

Mechanism
=========


version
=======
- NTPv4
