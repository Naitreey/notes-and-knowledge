file metadata
=============

implementation
--------------
- 文件类型以及权限的信息保存在一起, 是一个 ``mode_t`` 大小的量, 可由 ``stat(2)``
  syscall 取得. 其中, 访问权限为最低 12 位, 即 4 组 base8 值 (mask ``0o1111``).
  文件类型是随后的 4 位 (mask ``0o170000``).
  权限部分最高 3 位分别对应 setuid, setgid, sticky-bit.

permissions
-----------

setuid bit
^^^^^^^^^^
- representation: ``s`` bit on owner's ``x`` position.

- 如果一个文件系统在 mount 时设置了 ``nosuid``, 则里面的所有 setuid executable
  效果都不生效. 这是一个安全机制, 即通过限制非必要的文件系统或目录的 suid, 减小
  系统的攻击面 (attack surface).

  ``user`` mounts implies ``nosuid``. 显然这是为了安全.[SESUIDTMP]_

restricted deletion bit
^^^^^^^^^^^^^^^^^^^^^^^
- representation: ``t`` bit on other's ``x`` position.

- useful for directories.

- Restricted deletion bit prevents unprivileged users from removing or renaming
  a file  in  the  directory  unless they  own  the  file or the directory.
  This is commonly seen on world-writable directories, e.g. ``/tmp``.[ManChmod]_

- Historically, it's called sticky bit and useful for regular files. On those
  older systems, the bit saves the program's text image on the swap device so
  it will load more quickly when run.

references
==========
.. [SESUIDTMP] `SUID-bit not working for executables within /tmp directory <https://unix.stackexchange.com/questions/157314/suid-bit-not-working-for-executables-within-tmp-directory>`_
.. [ManChmod] chmod(1)
.. [SEStickyBit] `How does the sticky bit work? <https://unix.stackexchange.com/questions/79395/how-does-the-sticky-bit-work>`_
