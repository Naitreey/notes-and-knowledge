overview
========

- In Linux, directory hierarchy from root (/) downwards is standardized by
  the Linux Filesystem Hierarchy Standard (FHS).

- FHS 中, 各目录层级的设计思路就是从抽象至具体的思路. 从顶层至下层, 由一般化的
  类型至具体的程序实例. 这与 OOP 或者泛一般性的程序设计思路有共通之处.

the root filesystem
===================

/run
----

- contains system runtime data since this particular boot instance.
  Data under this directory should be transient in nature and potentially
  different across multiple boots.

- Files under this directory must be cleared on bootup. For some Linux distro,
  this is achieved by mounting tmpfs at ``/run``.

- ``/run`` is historically served by ``/var/run``.

- examples of files under ``/run``:

  * process PID file.
    
    - naming convention: ``<program>.pid``.

    - content: A PID number with a newline.

  * process's transient Unix domain socket files.

- permissions.

  * ``/run`` is owned by root, with permission bits 0755, i.e., only writable
    by root.

  * For unprivileged user, user-specific subdirectories can be created (for
    example ``/run/user/$UID``), and its ownership/permissions must ensure only
    the target user can write.

- Different type of programs and where to put their runtime files
  [SOPIDLocation]_:

  * Program that has root privilege (at least on startup): put runtime
    files under ``/run``.
    
    Program that needs to put multiple files under ``/run`` is encouraged to
    create its dedicated subdirectory (and maybe chown/chmod accordingly).

  * Program that runs as a logged-in human user, which is usually non-root:
    put runtime files under ``/run/user/$UID``.

  * Program that runs as some non-root system user and has no access to 
    root privileges: put runtime files under ``/tmp`` or ``/var/tmp``.

reference
=========

.. [SOPIDLocation] `Must my pidfile be located in /var/run? <https://stackoverflow.com/questions/5173636/must-my-pidfile-be-located-in-var-run>`_
