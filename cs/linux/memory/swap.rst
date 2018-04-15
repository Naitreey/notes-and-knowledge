overview
========
- Swap support is provided by kernel, util-linux provides userspace tools for management.

- Swap space can be a disk partition, or a file. There is no performance
  advantage to either a contiguous swap file or a partition, both are treated
  the same way.

- When to use swap:

  * When host RAM is small, like < 1G. For systems with much larger RAM capacity, swap
    is generally not necessary for normal operation.

  * When there's need for suspend-to-disk (hiberation) functionality.

swap setup
==========

systemd-swap
------------
- swap managed by systemd-swap is not usable for hiberation purpose.

manually
--------

swap file
^^^^^^^^^

- create swap file. ``dd`` is more general than ``fallocate``, for all filesystems.
  ``fallocate`` may not usable on XFS.

- onwership root, permission 0600.

- mkswap

- activate swap: ``swapon``

- add to fstab::

    /swapfile               none        swap        defaults,discard 0 0

- remove swap file::

    swapoff ...
    rm ...
