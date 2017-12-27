General & Concepts
==================
- Why use container?

  * short answer:

    容器提供了虚拟化的能力, 却避免了虚拟机带来的严重的 overhead.
    因此, 能用轻量化的容器解决的问题, 就没必要浪费资源和时间跑什么虚拟机了.

  * long answer:

    要回答这个问题, 首先我们考虑另一个问题: 虚拟机的意义是什么?
    答案是虚拟机让我们能够在一台设备中 (及其运行的操作系统平台下),
    运行多个相互独立的、互不干扰的、可以与宿主机迥异的运算环境.

    这种能力带来了非常多的可能性和用途. 例如, host 和 guest 以及
    guest 之间具有隔离性, 因此可以同时提供给多个用户使用, 而且不怕相互干扰或干扰
    宿主机; guest 与 host 之间可以是不同的运算环境, 因此可以用于解决单一平台的
    软件和功能等局限性, 同时应用多个平台带来的能力; 等等.

    容器提供了类似于虚拟机的能力 (从而暗示着类似的可能性和用途),
    却避免了虚拟机带来的严重的 overhead. 例如, 不同的容器之间是独立的,
    因此可以各自做自己所需的修改, 做自己要做的任何事而不怕相互干扰 (除了修改内核);
    不同容器可以是不同的操作系统版本或发行版, 因此可以用于解决单一发行版或者固定
    系统版本带来的局限性, 同时使用多个版本带来的能力; 可以很 cheap 地在同一台机器上
    对一个程序开多个实例, 让它们并行做相同的事等等.

    虚拟机的 overhead 是多方面的, CPU, memory, IO, 硬盘空间等都有很大的 overhead;
    容器的 overhead 仅为硬盘空间占用, 并且仍比虚拟机在这方面的 overhead 小很多.

    (Before VMs, bringing up a new hardware resource took days.
    Virtualization brought this number down to minutes.)

    容器能解决虚拟机的 overhead 的最重要原因是共用一个内核.
    而这相应地也限制了容器带来的能力. 也就是说, 大家都不能修改内核; 而且要求
    容器必须与宿主机是同一类操作系统, 且它的发行版或版本与宿主机的内核兼容.

    在 Linux 环境中, 这种不同发行版和新旧系统版本容器之间的兼容性,
    完全以 Linux 内核的 ABI backward-compatibility 为前提条件.

- Why use Docker?

  The feature that really sets Docker apart, is the layered file
  system and the ability to apply version control to entire containers. The
  benefits of being able to track, revert and view changes is well-understood
  and, overall, a highly desirable and widely-used feature in software
  development. Docker extends that same idea to a higher construct; the entire
  application, with all its dependencies in a single environment. This is
  unprecedented.

- 容器和 docker 带来的一些具体的好处和使用场景:

  * 应用、它所有的依赖和各种杂七杂八的配置, 都只需配置一次 (在一个镜像中),
    然后可以在任何 PaaS 上运行, 无论是开发环境还是生产环境, Amazon or Google.

  * 容器可以使用不同的发行版和版本, 解决了单一 distro 和 version 带来的局限性.

  * 应用隔离和服务隔离, 避免依赖冲突、配置冲突等问题.

  * 比虚拟机轻量化得多的 server consolidation, 服务器资源利用密度更高.

  * 快速、轻量化的部署, 让改动不再是 heavy-lifting, 不会每次修改都花费
    很多时间和资源重新部署. 这个好处同样也适用于测试阶段.

  * docker 提供了一些便利的容器操作 (commit, diff, etc.), 让开发更方便.

  * 轻量的服务并行.

- 为什么使用 docker 强调一个容器里只有一个功能 (functionality/service/concern)?

  单一功能的好处.

  * Scaling containers horizontally is much easier if the container is isolated
    to a single function. 由于一个功能的容器镜像是构建好的不变的, 在不同的机器
    上起多个实例仅仅是 docker run 同一个 image 而已. 而且可以保证服务完全相同.

  * Having a single function per container allows the container to be easily
    re-used for other projects and purpose, and at different location.

  * Changes (both the OS and the application) can be made in a more isolated
    and controlled manner. CI/CD can push updates to any part of a distributed
    application. 当以水平扩展为前提时, 我们可以一次只修改部分容器,
    让剩下的继续工作, 从而维持整个系统 online 和高可用.

  此外, 虽然容器和虚拟机都是独立的虚拟运行环境, 但只有容器强调单一功能.
  这是因为, 运行一台虚拟机的代价太高, 如果只运行一个服务的话, 太不划算了.
  换句话说, 容器的低成本、轻量级特性, 才允许它开多个, 每个里面只运行一个
  服务或进程.

- 对于数据库. 数据库实例需要大量的资源占用, 这包括内存, I/O 等. 它对硬件资源的要求
  很高. 把它放在容器中并在单机上多开, 并不能提高效率. 相反会造成资源竞争, 降低效率.
  因此, 对于数据库的容器化, 需要构成多台机器的 swarm 集群. 每台机器上只有一个数据库
  容器.

  那么对于数据库而言, 仍需要使用容器的原因是, 至少在测试和部署、升级等方面, 容器
  化仍然相比于实体机要有很多如上述的便利之处.

versions
========

- CE or EE.

CE
--
- CE has two update channels.

  * stable: reliable updates every quarter.

  * edge: new features every month.

- A given Edge release will not receive any updates once a new edge release is
  available.

- Ubuntu: setup docker official package repository for up-to-date releases.
  使用 stable release channel.

- archlinux: pacman 安装的是 edge release channel.

EE
--
- EE major releases twice per year.

terms
=====

- image. 在 docker 语境下, image 指的是程序文件以及它的一整套运行环境,
  包括文件系统, 依赖项, 环境变量, 配置等等. 注意, 镜像本身不包含要在
  其中运行的进程. 它仅仅包含运行任何可能进程的环境.

- container. container 是 image 的实例. 也就是在 image 提供的环境中真正
  运行所需进程. 基于同一个 image 提供的环境可以运行不同的进程. 也就是说,
  基于同一个镜像的不同容器实例并不需要运行相同的进程或服务.

- image tag. 完整的 tag 由 registry domain, username, repository name, tag version
  四部分组成. 完整格式是 ``[[<registry>/]<username>/]<repository>[:<tag>]``.
  若省略 registry, 默认是 docker.io. 若省略 username, 默认是 library.
  若省略 tag, 默认是 latest.

  若要把 image 上传到某个 registry, 或从某个 registry 下载镜像, 必须指定相应
  的 tag.

configuration
=============

- let non-root use docker.

  docker group 的用户都可以使用 docker.

dockerfile
==========

networking
==========

dockerd
=======

- run as root.

- binds to unix socket: ``/var/run/docker.sock``. 这个 socket 的 user 是
  root, group 是 docker. 所以 docker 组里的用户可以访问.

commandline
===========

container
----------

docker run, docker container run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``--hostname``. 默认情况下容器的 hostname 是它的 short UUID, 该选项
  指定 hostname.

docker stop, docker container stop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``docker stop`` 的效果不受 ``docker run --restart=`` 参数影响. 即使
``--restart=always``, docker stop 也能把容器停下来.

docker kill, docker container kill
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main process inside container will be killed by SIGKILL or other signal
specified by ``--signal`` option.

docker logs, docker contaienr logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- ``-f, --follow`` follow output. 此时 docker attach to the running container.

- ``-t, --timestamps`` 显示日志的时间. 这是 docker 给记录的. 也就是说, docker
  化的应用, 即使是异常崩溃等本身并无时间记录的输出信息, 也会有时间信息. 这很有用.

image
-----

docker build, docker image build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
build context 可以是本地目录, tarball, URL 或 stdin. 但无论哪种方式,
最终的根目录下或指定的 ``--file`` 路径都要有 Dockerfile 文件.

- 对于 local path, 该目录作为 build context 全部传输给 daemon;

- 对于 tarball 等 url, daemon 先下载再解压作为 build context;
  
- 若 url 指向一个 git repository, daemon 先 clone 再作为 build context.

docker pull, docker image pull
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``docker pull <name>`` 命令后面的 image name 即标准的 image tag 形式.

  e.g., ``docker pull ubuntu`` 实际是 ``docker pull docker.io/library/ubuntu:latest``.

docker registry
===============

- docker hub 实际上是一个 public docker registry. 它是 docker CLI 默认使用的
  registry.

- A production-ready registry must be protected by TLS and should ideally use
  an access-control mechanism.

terms
-----

- registry. A registry is a collection of repositories grouped by
  usernames/scopes.

- repository. a repository is a collection of version-controlled (by tags) images.

- image name. 一个 repository 中的某个 image 通过 repository name + version tag
  来唯一识别.

docker compose
==============

misc
====
- ``/etc/hostname`` ``/etc/hosts`` ``/etc/resolv.conf`` 三个文件都是由 docker 生成后
  mount 至 container 文件系统相应位置的. 所以在容器内部的修改不会持久, 需要在命令行
  ``docker run|create`` 中修改或在 dockerfile 中修改.
