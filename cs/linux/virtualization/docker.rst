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
    很多时间和资源重新部署.
    
    这个好处同样也适用于测试阶段. 即测试时不需要可能十分繁琐的手动安装,
    一步完成部署, 可以直接开始测试.

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

image
=====

- image. 在 docker 语境下, image 指的是程序文件以及它的一整套运行环境,
  包括文件系统, 依赖项, 环境变量, 配置等等. 注意, 镜像本身不包含要在
  其中运行的进程. 它仅仅包含运行任何可能进程的环境.

- image tag. 完整的 tag 由 registry domain, username, repository name, tag version
  四部分组成. 完整格式是 ``[[<registry>/]<username>/]<repository>[:<tag>]``.
  若省略 registry, 默认是 docker.io. 若省略 username, 默认是 library.
  若省略 tag, 默认是 latest.

  若要把 image 上传到某个 registry, 或从某个 registry 下载镜像, 必须指定相应
  的 tag.

- Each instruction in a Dockerfile creates a layer in the image. When you
  change the Dockerfile and rebuild the image, only those layers which have
  changed are rebuilt. 

container
=========

- container. container 是 image 的实例. 也就是在 image 提供的环境中真正
  运行所需进程.
  
  一个容器是由它基于的 image 以及容器创建时指定的配置选项共同决定的. 镜像
  提供各种运行环境, 包括文件, 依赖, 环境变量等. 而配置选项指定非常多的
  运行类参数, 包括运行的命令行, 网络, 存储, 等等.

- 可以基于容器当前的状态去创建新的镜像.

- 可以控制容器的 isolation level, 即控制几个 namespace 的独立情况.

configuration
=============

- let non-root use docker.

  docker group 的用户都可以使用 docker.

dockerfile
==========

networking
==========

engine
======
docker engine 是 docker ecosystem 最根本的组成部分, 所有其他工具都是建立
在它的基础上的.

architecture
------------
Docker Engine is a client-server application.

components:

- server daemon - dockerd.
  
- CLI client - docker command.

- REST API to interact with daemon, either from docker CLI or by using
  API directly.

The Docker client and daemon can run on the same system (communicate via unix
socket), or you can connect a Docker client to a remote Docker daemon (communicate
via TCP network).

dockerd
-------
- The daemon creates and manages Docker objects, such as images, containers,
  networks, and volumes.

- A daemon can also communicate with other daemons to manage Docker services.

- run as root.

- binds to unix socket: ``/var/run/docker.sock``. 这个 socket 的 user 是
  root, group 是 docker. 所以 docker 组里的用户可以访问.

- docker 命令的执行设计中, 命令和文件一同传递给 daemon. 这种设计保证了
  跨机器协作. 通过几个简单的环境变量修改, 一个 docker (CLI) client 可以
  切换控制本地或远端等多个 daemon. 

CLI
===

engine
------

container
~~~~~~~~~

- docker container run, docker run.

  ``--hostname``. 默认情况下容器的 hostname 是它的 short UUID, 该选项
  指定 hostname.

- docker container stop, docker stop.
  ``docker stop`` 的效果不受 ``docker run --restart=`` 参数影响. 即使
  ``--restart=always``, docker stop 也能把容器停下来.

- docker container kill, docker kill.
  main process inside container will be killed by SIGKILL or other signal
  specified by ``--signal`` option.

- docker contaienr logs, docker logs.

  ``-f, --follow`` follow output. 此时 docker attach to the running container.

  ``-t, --timestamps`` 显示日志的时间. 这是 docker 给记录的. 也就是说, docker
  化的应用, 即使是异常崩溃等本身并无时间记录的输出信息, 也会有时间信息. 这很有用.

image
~~~~~

- docker image build, docker build.
  build context 可以是本地目录, tarball, URL 或 stdin. 但无论哪种方式,
  最终的根目录下或指定的 ``--file`` 路径都要有 Dockerfile 文件.

  对于 local path, 该目录作为 build context 全部传输给 daemon;

  对于 tarball 等 url, daemon 先下载再解压作为 build context;

  若 url 指向一个 git repository, daemon 先 clone 再作为 build context.

- docker image pull, docker pull.

  ``docker pull <name>`` 命令后面的 image name 即标准的 image tag 形式.

  e.g., ``docker pull ubuntu`` 实际是 ``docker pull docker.io/library/ubuntu:latest``.

swarm
~~~~~

- docker swarm init. initialize a swarm.
  并自动让当前节点成为 swarm manager.

- docker swarm join.

- docker swarm leave. leave the swarm.

  ``--force``. 作为 swarm 的最后一个 manager, leave 会导致所有状态信息丢失,
  故此时需要强制离开.

- docker swarm join-token. 获取 join current swarm 的 token. worker & manager
  需要不同的 token.

node
~~~~

- docker node ls.

stack
~~~~~

- docker stack deploy

- docker stack rm.

- docker stack ls. list stacks in swarm.

- docker stack ps. list tasks in the specified stack.

service
~~~~~~~

- docker service ls. list services in swarm.

- docker service ps. list tasks of the specified services.

inspect
~~~~~~~

- docker inspect. insepct any docker objects.
  实际上各个主要 docker object 的子命令中还有 inspect 命令专门查看该类型对象.

registry
~~~~~~~~

- docker login.

- docker logout.

network
~~~~~~~

- docker network create.

- docker network ls.

- docker network inspect.
  输出还包括各个 attached container 的网络信息, 例如 ip.

- docker network connect.
  显然一个容器可以连接多个网络.

  ``--ip``, ``--ip6``, 连接时可以指定 ip. 对于自定义的网络.

- docker network disconnect.
  disconnect container from network. 断掉后容器内的相应虚拟网卡直接消失.
  注意这个操作是在修改容器的网络连接配置, 所以是持久的 (make sense).

compose
-------

machine
-------

- docker-machine create.

- docker-machine ls.
  其中 ACTIVE 列表示当前控制的 virtual host 是哪个.

- docker-machine ssh.

- docker-machine env. 将输出的环境变量导入当前 shell 环境中, 再直接执行各种
  docker commands 时就直接控制 docker engine on virtual host.

  此时, docker CLI 与 virtual host dockerd 通过 TCP 2376 端口通信 (而不是与本地
  dockerd 的 /var/run/docker.sock unix socket 通信). docker client 不但把
  命令传递给 daemon, 也包括命令执行所需文件. 这点无论是本地 unix socket
  或 TCP 方式都是统一的.

  ``--unset``. 清除远程 dockerd 环境变量. CLI 回归本地.

- docker-machine scp. copy files between local-remote or remote-remote.

  ``--delta``. 使用 rsync 从而只传输 difference.

- docker-machine ip.

- docker-machine start.

- docker-machine stop.

- docker-machine rm.

registry
========
- docker registry stores images.

- docker hub 实际上是一个 public docker registry. 它是 docker CLI 默认使用的
  registry.

- hierarchy.

  * registry. A registry is a collection of repositories grouped by
    usernames/scopes.
  
  * repository. a repository is a collection of version-controlled (by tags) images.
  
  * image name. 一个 repository 中的某个 image 通过 repository name + version tag
    来唯一识别.

- A production-ready registry must be protected by TLS and should ideally use
  an access-control mechanism.

compose
=======
docker compose is a tool for defining and running multi-container Docker
applications. 就是说, 一个 project 需要同时使用多个 containers 时, 使用
compose 可以方便地管理.

It is a frontend to the same api's used by the docker cli, so you can reproduce
it's behavior with usual docker commands.

docker-compose vs docker-swarm. 两者的适用场景不同, 并不存在取代关系.
docker-compose is needed to manage multiple containers as a service outside of
swarm mode, on a single docker engine.

swarm
=====
A swarm is a group of machines that are running Docker and joined into a
cluster.

A node is a docker host in swarm. (managed by docker daemon residing on it.)

Swarm managers are the only machines in a swarm that can execute commands,
or authorize other machines to join the swarm as workers.

Workers are just there to provide capacity and do not have the authority to
tell any other machine what it can and cannot do.

Swarm manager 执行的 docker commands 自动影响整个集群, 而不是仅仅影响本机.

strategies
----------
Swarm managers can use several strategies to distribute containers in the
cluster.

stack
=====

A stack is a group of interrelated services that share dependencies, and can be
orchestrated and scaled together, these may be defined using a docker-compose.yml
file.

docker stack 重用 docker-compose.yml 配置. 原因是两者在配置上是十分相似的.
它在 docker-compose.yml 中可以配置多实例并行和负载均衡.

修改 compose file 之后 re-deploy 不需要先删除当前的 stack, 而是直接 in-place
update. 其实这也容易理解, 因为有状态的存储部分和无状态的容器部分在 compose
file 中区分和定义的是清晰的. 所以知道该如何更新.

一个 stack 就是一个 app. 一个 stack/app 可以有多个 services, 每个 services
可以有多个 tasks.

service
=======
A service consists of one or more replica containers for the same image and
configuration within swarm, multiple containers provide scalability.

task. A single container running in a service is called a task.
一个 service 的多个 task replica 是自动负载均衡的. 多个 replica
成为一个整体 (service), 从 consumer 的角度看, 只有 service, 而
不见 tasks. 所以在 swarm mode 中, service 是功能单元.

service is named by ``<stack-name>_<service-name>``

一个 service 里的每个 task 命名为 ``<stack-name>_<service-name>.<N>``.

compose file
============
Definition file for a group of containers, used by docker-compose and by swarm
mode.

服务端口设置. 注意到 ports 是对 service 进行设置的, 而不是对 task 设置的.
service 属于整个 stack. 所以在整个 swarm 的所有节点上, 这个端口映射至相应
服务都要成立. 这与各个 tasks 部署在哪个节点上无关. 无论从哪个节点访问, 都
可以 load balance. 这由一个 ingress routing mesh 实现.

network
=======

- 三个默认网络: none, host, bridge.

  docker container 默认使用 bridge network.

  默认的 bridge network ``Options.com.docker.network.bridge.name`` 为 docker0.
  默认的 bridge network 不能删除.

- 网络内使用容器的名字可以 DNS 解析到 IP 地址.

ingress routing mesh
--------------------

- Port 7946 TCP/UDP for container network discovery.

- Port 4789 UDP for the container ingress network.

drivers
-------

bridge
~~~~~~

bridge 指的是各个容器与一个网桥或交换机 (通过 veth) 连通. 从而可以相互访问.
通过 ip_masquerade 等设置, 该交换机能够兼有 NAT 路由器功能, 即成为 layer-3 switch.

根据网络原理, 一个 bridge network 显然只能独立于一台 docker host machine 上面.
(指的是 bridge network 这个子网的范围. 里面的容器和外界或者其他机器上的容器是
有办法互通的.)

overlay
~~~~~~~

overlay network 可以跨多个 docker hosts. 这指的是, 每个 host 上的容器所在的
子网都是相通的, 或者说, 可以抽象地认为这些不同机器上的容器都位于同一个子网.
不同机器上的容器之间可以通过名字或 IP 直接访问.

overlay network 之所以可能, 不是仅仅依靠标准的网络原理和配置实现的. 要借助
应用层的实现和转发. 即若访问不在一台机器上的容器时, 要靠 dockerd 保持的
分布式的网络状态存储, 来知道该向哪个机器转发.

machine
=======
Docker Machine is a tool that lets you install Docker Engine on virtual hosts,
and manage the hosts with docker-machine commands. 

docker-machine 是用于管理专门用于 docker 运行的虚拟机的. 只有需要使用虚拟机来
运行 docker 时, 并且是专门用于运行 docker 时, 才需要使用 docker-machine.

严格地讲, docker-machine 所在机器如果只是用于管理 virtual docker hosts,
本地是不需要安装 docker engine 的.

driver. docker-machine 有很多云服务商的 driver. 本地虚拟机使用 virtualbox driver.

docker-machine 在 VM 中安装专门为了运行 docker 的 linux distro Boot2Docker.

cloud
=====
docker cloud 是专门用于基于云服务的 dockerized environment. 它是一项 Docker Inc.
提供的在线服务. 这与 docker-machine 有本质区别.

internals
=========

namespace
---------
Each aspect of a container runs in a separate namespace and its access is
limited to that namespace.

- The pid namespace: Process isolation (PID: Process ID).

- The net namespace: Managing network interfaces (NET: Networking).

- The ipc namespace: Managing access to IPC resources (IPC: InterProcess
  Communication).

- The mnt namespace: Managing filesystem mount points (MNT: Mount).

- The uts namespace: Isolating kernel and version identifiers. (UTS: Unix
  Timesharing System).


control groups (cgroups)
------------------------
A cgroup limits an application to a specific set of resources. Control groups
allow Docker Engine to share available hardware resources to containers and
optionally enforce limits and constraints.

UnionFS
-------
operate by creating layers, making them very lightweight and fast.

Docker Engine can use multiple UnionFS variants, including AUFS, btrfs, vfs,
and DeviceMapper.

container format
----------------
- libcontainer.

misc
====
- ``/etc/hostname`` ``/etc/hosts`` ``/etc/resolv.conf`` 三个文件都是由 docker 生成后
  mount 至 container 文件系统相应位置的. 所以在容器内部的修改不会持久, 需要在命令行
  ``docker run|create`` 中修改或在 dockerfile 中修改.
