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

extended file attributes
------------------------
overview
^^^^^^^^
- Extended file attributes (xattr) are file system features that enable users
  to associate files/directories with metadata not interpreted by the
  filesystem, whereas regular attributes have a purpose strictly defined by the
  filesystem. An xattr is a ``name:value`` pair.

- An attribute may be defined or undefined.  If it is defined, its value may be
  empty or non-empty.

- extended attributes are usually limited in size to a value significantly
  smaller than the maximum file size.

- xattr 这种文件系统特性只适合在比较固定的场景下使用. 因为在不同的系统和工具下
  并不是十分通用, 有一定的丢失可能性.

format
^^^^^^
- Attribute names are null-terminated strings. The attribute name is always
  specified in the fully qualified ``namespace.attribute`` form.

- The namespace mechanism is used to define different classes of extended
  attributes.

- Four namespaces are defined: security, system, trusted, user.

namespaces
^^^^^^^^^^
security
""""""""
- The security attribute namespace is used by kernel security modules, such as
  SELinux, and also to implement file capabilities.

- Read and write access permissions to security attributes depend on the
  policy implemented for each security attribute by the security module.
  When no security module is loaded, all processes have read access to
  extended security attributes, and write access is limited to processes
  that have the ``CAP_SYS_ADMIN`` capability.

system
""""""
- system attributes are used by the kernel to store system objects such as
  Access Control Lists.
  
- Read and write access permissions to system attributes depend on the policy
  implemented for each system attribute implemented by filesystems in the
  kernel.

trusted
"""""""
- trusted namespace is used to implement mechanisms in user space (i.e.,
  outside the kernel) which keep information in extended attributes to which
  ordinary processes should not have access.

- Trusted extended attributes are visible and accessible only to processes that
  have the CAP_SYS_ADMIN capability.

user
""""
- user namespace is used for storing arbitrary additional information such as
  the mime type, character set or encoding of a file.
  
- The access permissions for user attributes are defined by the file permission
  bits: read permission is required to retrieve the attribute value, and writer
  permission is required to change it.

- Extended user attributes are allowed only for regular files and directories,
  and access to extended user attributes is restricted to the owner and to
  users with appropriate capabilities for directories with the sticky bit set.

implementations
^^^^^^^^^^^^^^^
Linux
""""""
- 主流文件系统一般都支持 xattr.

- The Linux kernel allows extended attribute to have names of up to 255 bytes
  and values of up to 64KiB, as do XFS and ReiserFS, but ext2/3/4 and btrfs
  impose much smaller limits, requiring all the attributes (names and values)
  of one file to fit in one "filesystem block" (usually 4 KiB).

macOS
""""""
- The macOS APIs support listing, getting, setting, and removing extended
  attributes from files or directories. From the command line, these abilities
  are exposed through the xattr utility.

- Files originating from the web are marked with com.apple.quarantine via
  extended file attributes.

usage
^^^^^
storing:

- the author of a document
 
- the character encoding of a plain-text document
 
- a checksum, cryptographic hash or digital certificate
 
- access control information (e.g., SELinux).

- they are not yet in widespread use by user-space Linux programs, but are used
  by Beagle, OpenStack Swift, Dropbox, KDE's semantic metadata framework
  (Baloo), Chromium, Wget and cURL.

references
==========
.. [SESUIDTMP] `SUID-bit not working for executables within /tmp directory <https://unix.stackexchange.com/questions/157314/suid-bit-not-working-for-executables-within-tmp-directory>`_
.. [ManChmod] chmod(1)
.. [SEStickyBit] `How does the sticky bit work? <https://unix.stackexchange.com/questions/79395/how-does-the-sticky-bit-work>`_
xattr(7)
