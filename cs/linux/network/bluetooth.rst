
- implementation: BlueZ.

- systemd unit: bluetooth.service.

configuration
=============

commandline
-----------

- ``bluetoothctl``: CLI tool provided by bluez.

procedures
~~~~~~~~~~
- optionally select default controller: ``select <MAC address>``

- power on controller: ``power on``

- list available bluetooth devices: ``devices``

- scan new device: ``scan on``

- turn on agent: ``agent on``

- pair with device: ``pair <MAC address>``

- optionally trust device: ``trust <MAC address>``

- connect with device: ``connect <MAC address>``

GUI
---

KDE
~~~
- Bluedevil
