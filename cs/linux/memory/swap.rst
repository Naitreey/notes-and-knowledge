overview
========
- Swap support is provided by kernel, util-linux provides userspace tools for
  management.

- Swap space can be a disk partition, or a file. There is no performance
  advantage to either a contiguous swap file or a partition, both are treated
  the same way.

- The total amount of virtual memory of a system is the sum of physical memory
  and swap space.

limits
------
- The max size of a swap: ``UINT_MAX`` number of pages. The remaining space on
  the swap device is ignored.

- The min size of a swap: 10 pages.

- Max number of swap: 32.

When to use swap
----------------

* When host RAM is small, like < 1G. For systems with much larger RAM capacity, swap
  is generally not necessary for normal operation.

* When there's need for suspend-to-disk (hiberation) functionality.

swap detection
==============

systemd
-------
systemd looks at two places to generating swap units automatically.

* /etc/fstab (``/usr/lib/systemd/system-generators/systemd-fstab-generator``).

* gpt partition with linux swap partition type
  (``/usr/lib/systemd/system-generators/systemd-gpt-auto-generator``).

files
=====
- /proc/swaps

tools
=====
- swapon(8)

- swapoff(8)

- mkswap(8)

swapon(8)
---------
- enable swap device and file manually.

considerations
^^^^^^^^^^^^^^
* shouldn't use file with holes as swap file. Kernel expects to be able to
  write to swap directly bypassing filesystem layer. 这主要对于以下文件会造成问
  题:

  - preallocated files on XFS and ext4. Use dd and /dev/zero to avoid this.

  - files on COW filesystems like btrfs.

  - files on NFS.

options
^^^^^^^
- ``-a``. enable all configured swaps in fstab, except for "noauto".

- ``--discard[=policy]``. enable discard, for backing device/file that supports
  discard/trim operations. same to the same option of fstab.

- ``-L label``. use partition of label.

- ``-U uuid``. use partition of uuid.

- ``-o opts``. add opts (in fstab option form) when enabling swap.

- ``-p priority``.

- ``--show[=column...]``. show swap info with the defined columns.

- ``--noheadings``.

- ``--raw``. show in raw column format.

mkswap(8)
---------
- setup a device or file as swap.

- mkswap, like many others mkfs-like utils, erases the first partition block to
  make any previous filesystem invisible.

options
^^^^^^^
- ``-L label``. set a label.

- ``-U uuid``. set a uuid.

operations
==========

setup swap
----------

systemd-swap
^^^^^^^^^^^^
- swap managed by systemd-swap is not usable for hiberation purpose.

manually
^^^^^^^^

swap device
"""""""""""
- create a partition for swap. Set partition GUID type as linux swap.

- mkswap

- enable in fstab. adding possibly discard option for ssd.

swap file
"""""""""

- create swap file. ``dd`` is more general than ``fallocate``, for all filesystems.
  ``fallocate`` may not usable on XFS.

- onwership root, permission 0600.

- mkswap

- add to fstab::

    /swapfile               none        swap        defaults,discard 0 0

- remove swap file::

    swapoff ...
    rm ...

enable swap
-----------

manually
^^^^^^^^
- swapon

systemd
^^^^^^^
- enable detected swap service unit.

disable swap manually
---------------------
manually
^^^^^^^^
- swapoff

systemd
^^^^^^^
- disable detected swap service unit.

show swap
---------
::

  swapon --show
  # or
  free -h


performance
===========
- 对于内存充足的系统, 其实没必要使用 swap (用于 hibernation 除外).

- 对于内存紧张的系统, 使用 swap 可以将一些 inactive 的内存 swap 至硬盘上, 将内
  存资源留给 active 的程序和 VFS cache. 对于 VFS cache, 可以避免 disk IO (与
  swap 类似的慢), 所以是有意义的.

tuning
------
- swappiness. kernel parameter: ``vm.swappiness``.

  * default: 60.

  * range: 0~100. A low value causes the kernel to avoid swapping, a higher
    value causes the kernel to try to use swap space.

  * Using a low value on sufficient memory is known to improve responsiveness
    on many systems.

  * also as ``/sys/fs/cgroup/memory/memory.swappiness``

- VFS cache pressure. kernel paramter: ``vm.vfs_cache_pressure``

  * controls the tendency of the kernel to reclaim the memory which is used for
    caching of directory and inode objects.

  * default: 100, which is a "fair" reclaim rate.

  * lower value causes the kernel to prefer to retain dentry and inode caches.
    With 0, the kernel will never reclaim dentries and inodes due to memory
    pressure and this can easily lead to out-of-memory conditions.

  * higher beyond 100 causes the kernel to prefer to reclaim dentries and
    inodes.
