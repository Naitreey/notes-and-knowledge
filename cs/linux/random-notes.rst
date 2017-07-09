- 线程的目的不仅仅是为了 *同时的* 并行计算, 而是为了构建多个独立的运算单元.
  将这些运算单元分配到不同的 CPU 核上才具有 "同时并行" (parallel computing) 的意义.
  python 虽然有 GIL, 但这影响的是单 python 进程进行 parallel computing 的能力,
  并没有影响多线程所带来的其他可能性.

  所谓 concurrency, 指的就是多个任务同时处于进行中的状态, 即多任务并发.
  这可以在单个线程中实现, 例如多任务的异步处理 (e.g., python 中的 asyncio);
  也可以在多线程和多进程中实现, 以实现多个独立的运算单元.

- 为什么 shared library 具有 executable bit set?

  1. 历史原因: 一些 unix 使用 shared library 文件的 rwx 权限来对应 `mmap()`
     至进程虚拟内存中的机器码的 rwx 权限.

  2. 一些 shared library 确实可以执行, 比如 `libc.so.6`.

- bash 的 fd 255 是用来临时保留 terminal file description 的. 例如, 一个命令执行时
  需要 redirect 0, 1, 2 都至 /dev/null, bash 只能先把自己的 0, 1, 2 指向的 file
  description 即一般是 `/dev/tty?` 或 `/dev/pts/?` `dup2(2)` 至 255, 等 fork 后
  再转回来.

- 在 systemd 的系统中, hostname 的设置逻辑大致是这样:
  * 在启动阶段:
    - initramfs 阶段使用镜像里保存的 `/etc/hostname`, 这是之前 `dracut` 做镜像
      时包含在里面的.
    - chroot 后, systemd 启动 systemd-hostnamed.service, 后者通过以下顺序决定
      hostname:
      * 使用 `/etc/hostname`.
      * 通过 `/etc/machine-info` 里的 `PRETTY_HOSTNAME` 推出一个 hostname.
      * 通过 IP 地址请求 reverse DNS 给出给出一个 "transient hostname".
      * 使用默认的 `localhost`.
  * 在运行阶段:
    用户可使用 `hostnamectl`, 通过 systemd-hostnamed.service 来控制 hostname,
    以及各种其他标识信息.

- 如何快速删除包含大量文件的目录?

  * 方案 1

      .. code:: sh

      mv bigdir bigdir.old
      mkdir bigdir
      rm -rf bigdir.old &
      #mkdir -p /tmp/empty
      #rsync -rd --delete /tmp/empty/ bigdir.old/ &
      #rmdir bigdir.old

    ..
    *需要了解原理并证明?*
    删除原目录还有一个附加的原因, `bigdir` 下第一层曾经可能有大量的文件, 而 dir file
    只增不减 , 即使已经空了仍然效率很差.
    使用 rsync 是因为文件系统中目录结构往往用 btree, rsync 的删除顺序避免了 btree
    rebalancing, 因此更高效. (我不理解这是啥意思?)

  * 方案 2: 把该文件系统中所有其他文件挪走, reformat 这个文件系统, 再把文件挪回来.

- 文件类型以及权限的信息保存在一起, 是一个 ``mode_t`` 大小的量, 可由 ``stat(2)``
  syscall 取得. 其中, 访问权限为最低 12 位, 即 4 组 base8 值 (mask ``0o1111``).
  文件类型是随后的 4 位 (mask ``0o170000``).
  权限部分最高 3 位分别对应 setuid, setgid, sticky-bit.

- Linux 中, symlink 的 permission 根本没用, stat 显示的是 ``0777``. ``chmod(2)``
  遇到 symlink 会 dereference 从而实际作用在它指向的文件上面, 根本不会去修改
  link 本身的权限. 对于 ``chmod(1)``, 若 recursively (``-R``) 修改权限, 遇到
  symlink 会直接跳过.

- ``stat(1)`` 中的 ``Device: xxxh/xxxxxd`` 实际上是 device id 的 hex 和 decimal
  两种表现形式. Device id 的类型为 ``dev_t``, 最低两个 bytes 分别是 major 和 minor
  device number. major 为设备类型, 对应为 ``/proc/devices`` 里的数值, minor 为
  该类型设备的实例编号. device id 和 major/minor 之间的转换可通过 ``makedev(2)``,
  ``major(2)``, ``minor(2)``.

- ``stat(1)`` 中与文件相关的 3 个时间:

  * access time (``st_atime``): 创建文件以及访问文件内容时会更新,
    例如读取大于 0 bytes 的数据. 注意如果文件已经存在, 写数据时不会更新.

  * modified time (``st_mtime``): 创建文件以及修改文件内容时会更新, 例如
    写入大于 0 bytes 的数据. 注意文件的 metadata 方面的修改 (而不是内容的修改)
    不会导致 mtime 的改变.

  * change time (``st_ctime``): 修改文件的 metadata 时会更新.

- cron 和 anacron 的关系.

  cron 负责 ``crontab``, ``cron.d`` 里的项, ``cron.d`` 里一般会有 ``0hourly``,
  用于执行 ``cron.hourly`` 里的项. 由于使用了 ``run-parts``, ``cron.hourly``
  允许使用 ``jobs.allow``, ``jobs.deny`` 来执行或不执行任务.

  anacron 负责 ``anacrontab``, 后者会指定去执行 ``cron.daily``, ``cron.weekly``,
  ``cron.monthly`` 三个目录. 这样是把所有需要 daily/weekly/monthly 执行的任务
  各自合成一个大任务来执行的. 如需细粒度的方式, 则需在 anacrontab 中对每个任务
  注册.

  anacron 不是 daemon, 它要靠在 crontab 中注册, 每小时运行一次, 来检查和执行
  需要的任务. anacron 的注册方式是 ``cron.hourly/0anacron``.

- linux FHS 的思路实际上就是从抽象至具体, 从 class/interface 至实例一层层递进
  的思路. 这与 OOP 程序设计的思路 (或者宽泛的一般性的程序设计思路) 实际上是一致的.

- ``/dev/sd?`` 已经失去它原本的含义了 (sd: SCSI device). 如今, 它更像是一个泛泛的
  对存储设备的概括 (sd: storage device). 因为使用 SAS, SATA, PATA, SCSI, USB, 等协议
  和总线的设备往往都显示为 ``sd?``. 注意, 这些协议本身都是不同的, 不一定有兼容性.
  只是在 kernel 中这些 HBA 的驱动和 generic disk driver 这层通信时, 经常使用的是
  scsi 协议. 并不是说这些协议和总线与 SCSI 一定有什么从属关系.

- Shared MIME-info database 位于 ``/usr/share/mime``. ``mimetype(1)`` 命令依据这个目录
  判断文件的 MIME type. ``file(1)`` 没有使用这个 mime 数据库, 而是使用自己的
  ``magic(5)`` 格式的数据库来识别文件, 并输出这里面定义的 mime type.

  在判断 mime type 方面, 貌似 ``mimetype(1)`` 比 ``file(1)`` 要准确一些.

- ``xdg-open(1)`` 和 ``mimeopen(1)`` 的区别是:

  ``xdg-open`` 是直接和当前使用的桌面系统耦合的,
  本质上只是不同桌面系统的 open 命令的一个统一封装, 也就是说它到底调用什么程序取决于
  在 DE 中是怎么配置的, 而不一定与 mimetype 和 desktop application 的关联性有关.
  与 ``xdg-open`` 相关的配置命令是 ``xdg-mime``, 它相当于是在命令上对不同 DE 的应用和
  mimetype 的关联性的统一封装. ``xdg-mime`` 在查询和设置默认应用时也是直接访问 DE.

  ``mimeopen`` 是另一套手动的关联关系, 它不取决于当前的 DE. 而是直接读取一些确定的配置文件
  中的映射关系, 例如 ``~/.local/share/applications/defaults.list``.

- some useful options of ``file(1)`` command.

  ``-i|--mime``, ``-l|--list``, ``-p|--preserve-date``, ``-s|--special-files``

- bash job control 中, current job (``+``) 和 previous job (``-``) 的 job spec 是
  ``%+`` (或 ``%``), ``%-``. 编号为 n 的 job 可写为 ``%n`` (或直接是 ``n``).

  而且实际上这些 ``%`` 开头的 job spec 可以直接在命令行上执行, 等价于 ``fg ...``,
  而 ``%.. &`` 则等价于 ``bg ...``.

  从这个角度看, ``%`` 可以认为是 job control 的标志符, 相应于 ``!`` 是 command history
  substitution 的标志符.

- SMBIOS/DMI 信息由 kernel 提供给 userspace 使用. 这些信息保存在 sysfs 里:
  ``/sys/firmware/dmi/tables/smbios_entry_point``
  ``/sys/firmware/dmi/tables/DMI``
