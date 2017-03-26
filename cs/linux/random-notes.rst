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
      mkdir -p /tmp/empty
      rm -rf bigdir.old &
      #rsync -rd --delete /tmp/empty/ bigdir.old/ &
      #rmdir bigdir.old

    ..
    *需要了解原理并证明?*
    删除原目录还有一个附加的原因, `bigdir` 下第一层曾经可能有大量的文件, 而 dir file
    只增不减 , 即使已经空了仍然效率很差.
    使用 rsync 是因为文件系统中目录结构往往用 btree, rsync 的删除顺序避免了 btree
    rebalancing, 因此更高效. (我不理解这是啥意思?)

  * 方案 2: 把该文件系统中所有其他文件挪走, reformat 这个文件系统, 再把文件挪回来.
