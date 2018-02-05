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

concepts and best practices
---------------------------
- 在 docker 语境下, image 指的是程序文件以及它的一整套运行环境,
  包括文件系统, 依赖项, 环境变量, 配置等等. 注意, 镜像本身不包含要在
  其中运行的进程. 它仅仅包含运行任何可能进程的环境.

- How to keep image small.

  * start with appropriate base image.

  * avoid installing unnecessary packages.

  * use ``.dockerignore`` file to exclude files which are not relevant to the
    build, syntax similar to ``.gitignore``.

  * use multistage builds. Your final image shouldn't include dependencies
    needed for building your app, just for running.

  * 若不使用 multistage build, 尽量减少 dockerfile 中镜像的层数, 即减少
    ``RUN`` command 的数量.

  * 若多个 app 镜像实际上基于一些共同的基础环境, 则制作一个能够最大程度通用
    和减少重复的 base image. 然后各个镜像再基于它来制作. 除了显而易见的好处
    之外, 这样做还可以减少内存用量和提高加载速度. 因相同的 readonly layers
    docker 只加载一份至内存.

- 基镜像的选择.
  
  * Whenever possible, use current official repositories as the basis for your
    image.

  * 若需要 start from scratch, 可以谨慎选择 alpine linux 作为基镜像. 注意
    musl libc 问题.

  * 研发时使用基于 debian 的镜像. 保证方便, 什么都有. 测试和部署时使用基于
    alpine 的镜像. 保证轻量.

base image
----------

制作基镜像
~~~~~~~~~~
两种制作 base image 的方法.

* ``docker image import``. 这种方式的问题是只有结果, 没有过程.

* 为了将 base image 的制作与普通镜像统一起来, 使用 dockerfile 制作 (从而
  可以清晰地记录构建步骤以及使用 cache 等好处), 使用 ``FROM scratch``.

Using the scratch “image” signals to the build process that you want the next
command in the Dockerfile to be the first filesystem layer in your image.

While scratch appears in Docker’s repository on the hub, you can’t pull it or
run it.

选择基镜像
~~~~~~~~~~
- 当需要同时运行多个服务时, 尽量选择存在共同基镜像的镜像版本. 例如
  基于 debian image 各个版本, alpine 等的镜像.

image tag
---------
完整的 tag 由 registry domain, username, repository name, tag version
四部分组成. 完整格式是 ``[[<registry>/]<username>/]<repository>[:<tag>]``.
若省略 registry, 默认是 docker.io. 若省略 username, 默认是 library.
若省略 tag, 默认是 latest.

若要把 image 上传到某个 registry, 或从某个 registry 下载镜像, 必须指定相应
的 tag.

tag 应该尽量详细, 包含 version, release stage, purpose (test/production) 等.

image layers
------------
- Each RUN, COPY, ADD instructions in a Dockerfile creates a layer in the
  image. When you change the Dockerfile and rebuild the image, only those
  layers which have changed are rebuilt.

build cache
-----------
During an image, as each instruction in dockerfile is examined, Docker by default
looks for existing local images that have a local parent chain. These images
may come from previous builds, or loaded via ``docker image load``.

- Starting with a parent image that is already in the cache, the next
  instruction is compared against all child images derived from that base image
  to see if one of them was built using the exact same instruction. If not, the
  cache is invalidated.

- In most cases simply comparing the instruction in the Dockerfile with one of
  the child images is sufficient. However, certain instructions require a
  little more examination and explanation.

- For the ADD and COPY instructions, the contents of the file(s) in the image
  are examined and a checksum is calculated for each file. The last-modified
  and last-accessed times of the file(s) are not considered in these checksums.
  During the cache lookup, the checksum is compared against the checksum in the
  existing images. If anything has changed in the file(s), such as the contents
  and metadata, then the cache is invalidated.

- Aside from the ADD and COPY commands, cache checking does not look at the
  files in the container to determine a cache match. Just the command string
  itself is used to find a match.

- 环境变量的影响.
  If a Dockerfile defines an ARG variable whose value is different from a
  previous build, then a “cache miss” occurs upon its first usage, not its
  definition. In particular, all RUN instructions following an ARG instruction
  use the ARG variable implicitly (as an environment variable), thus can cause
  a cache miss.

  修改 pre-defined ARGs 值不会造成 cache miss. 因为 All predefined ARG
  variables are exempt from caching unless there is a matching ARG statement in
  the Dockerfile. 

- Once the cache is invalidated, all subsequent Dockerfile commands generate
  new images and the cache is not used.

由于更多的 dockerfile instruction 只检查命令本身是否一致,
而不考虑文件内容是否一致, 如果需要重新执行相应命令, 使用 ``--no-cache`` option
during ``docker build``.

若要直接指定一个镜像作为 cache source, 跳过上述 image layer 搜索过程, 使用
``--cache-from``. Images specified with ``--cache-from`` do not need to have a
parent chain and may be pulled from other registries.

builder pattern
---------------
Traditionally, it was often desirable to have two dockerfiles:

- ``Dockerfile.build`` is used for development (which contained everything
  needed to build your application),

- ``Dockerfile`` is a slimmed-down one to use for production, which only
  contained your application and exactly what was needed to run it.

And a ``build.sh`` script to orchestrate the building process: build the first
image, create a container from it to copy the artifact out, then build the
second image.

multi-stage build
-----------------
Multi-stage build made build pattern unnecessary.

multi-stage build 的用处:

- Multi-stage build allow you to copy only the artifacts you need into the final
  image. This allows you to include tools and debug information in your
  intermediate build stages without increasing the size of the final image.

- 可以控制最终 build 到哪个 stage 结束. 这对从研发到部署的不同阶段生成不同
  镜像非常方便. 即每个 build stage 生成一个镜像, 适合某个阶段来使用.
  例如, 可以在 develop/test 镜像阶段添加所有需要的依赖和 debug 工具,
  方便研发和调试; 在 production 镜像阶段仅添加构建结果和必要依赖.

Every FROM instruction in dockerfile begins a new build stage.
Stages are indexed from 0. Build stage can be named at FROM line
``FROM ... as <name>``.

Use ``COPY --from=<name|index>`` to copy artifacts from previous stages into
current build stage.

在 multi-stage build 中, production stage 的基镜像可以是 apline based images.

container
=========

- container. container 是 image 的实例. 也就是在 image 提供的环境中真正
  运行所需进程.

  一个容器是由它基于的 image 以及容器创建时指定的配置选项共同决定的. 镜像
  提供各种运行环境, 包括文件, 依赖, 环境变量等. 而配置选项指定非常多的
  运行类参数, 包括运行的命令行, 网络, 存储, 等等.

- 可以基于容器当前的状态去创建新的镜像.

- 可以控制容器的 isolation level, 即控制几个 namespace 的独立情况.

concepts and best practices
---------------------------
- Containers should be as ephemeral as possible. By “ephemeral,” we mean that
  it can be stopped and destroyed and a new one built and put in place with an
  absolute minimum of set-up and configuration. 

- 一个容器里只有一个功能 (functionality/service/concern).

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

  单一功能不是单一进程的意思. 例如一些服务自己会开子进程, 甚至有些时候需要在容器
  中开 init system.

configuration
=============

- let non-root use docker.

  docker group 的用户都可以使用 docker.

dockerfile
==========

concepts and best practices
---------------------------
- RUN, COPY, and ADD instructions create layers. Other instructions create
  temporary intermediate images, and not directly increase the size of the build.

- When appropriate, break arguments into multi-lines, and sort them
  alphanumerically.  This helps you avoid duplication of arguments and make the
  list much easier to update.

format
------
.. code:: dockerfile
  # Comment|directive=value
  INSTRUCTION arguments

A Dockerfile must start with zero or more ``ARG`` instructions followed by a
``FROM`` instruction. 这个主要目的是为了将 FROM instruction 参数化.

对于 array 形式的参数, 使用 valid JSON array syntax.

instruction
~~~~~~~~~~~
INSTRUCTION is case-insensitive. Convention is to be uppercase to distinguish
them from arguments easily.

Instructions is executed in order. 

comment
~~~~~~~
Line comments (and parser directives) must start at the beginning of lines.

parser directive
~~~~~~~~~~~~~~~~
All parser directives must be at the very top of a Dockerfile.
Each directive may only be used once.

Parser directives are not case-sensitive. However, convention is for them to be
lowercase. Convention is also to include a blank line following parser directives.

instructions
------------

FROM
~~~~
::
  FROM <image>[:<tag>|@<digest>] [AS <name>]

- ``<image>`` 可以是任何 image identifier, local or remote, with or without tag,
  with or without hash, etc. 还可以是之前 build stage 生成镜像的名字.

- An ARG declared before a FROM is outside of a build stage, so it can’t be
  used in any instruction after a FROM. To use the default value of an ARG
  declared before the first FROM use an ARG instruction without a value inside
  of a build stage.

SHELL
~~~~~
::
  SHELL ["cmd", ...]

- 指定默认的 shell. 这个 shell 用于执行所有使用 shell form 的 instructions.

- 默认为 ``["/bin/sh", "-c"]``.

- The SHELL instruction can appear multiple times.

RUN
~~~
::
  RUN <command>
  RUN ["cmd", ...]

- Each RUN instruction in dockerfile is run independently. I.e., 前一个
  RUN 对运行环境的修改对后一个是不可见的. 例如, ``cd``, ``shopt`` 只对当前
  命令有效. 要修改运行环境, 必须使用相应的 dockerfile instruction.

- 避免对 packages 进行批量的版本升级, 例如 ``apt-get upgrade|dist-upgrade``.
  若基镜像本身版本低了, 应该 pull 更新的版本. 若需要对某些软件更新, 单独对
  这些软件操作.

- Always combine ``RUN apt-get update`` with ``apt-get install`` in the same
  RUN statement.
  
  这是为了在后续修改 install 的 packages 参数时, invalidate 整个命令的 cache,
  从而 apt-get update 重新执行. This is called "cache busting".  必要时, 还可以
  在 install 参数后面固定 package 的版本, 从而保证 apt cache 总是能及时更新, 
  即使只是修改要安装的软件版本.
  .. code:: dockerfile
    RUN apt-get update && apt-get install -y \
        abc=1.2.* \
        def \
        ghi \
        ;

  若将 update 和 install 分成两个 RUN instructions, 修改 install 命令后, 还是
  用的旧的 apt cache, 从而不能安装新版本的 packages, 甚至找不到要安装的 packages
  从而 install 命令失败.

- 应当考虑设置常用的 shell options, 避免一些 pitfalls. 
  例如, 对于 commands involving pipelines, 设置 ``pipefail`` option.

ENTRYPOINT
~~~~~~~~~~
::
  ENTRYPOINT ["cmd", ...]

- 不建议使用 shell form entrypoint, 因进程不是 PID1, 而是 sh -c 的子进程,
  pass signal 可能有问题.

- ENTRYPOINT 是提供镜像 (所生成的容器的) 要执行的命令.

- default entrypoint is ``["/bin/sh", "-c"]``.

- 添加 ENTRYPOINT 的镜像, 一般是成型的服务类型的镜像.

- CMD 和 ENTRYPOINT 的使用和关系.

  * ENTRYPOINT 或 CMD 必须至少有一个.

  * CMD 单独使用时, 一般是对一个 generic 的镜像提供 default command. 就是说该
    镜像的主要目的是作为基镜像, 而不是作为服务镜像. 此时若执行基镜像, 提供一个
    默认的 CMD 可执行. 例如 interactive interpreter, 或者输出使用说明之类的.

  * ENTRYPOINT 和 CMD 配合使用时, CMD 提供 ENTRYPOINT 之外的默认参数. 注意 CMD
    总是可以被命令行参数 override.

- 容器运行时, 执行的命令总是由两部分组成::
    entrypoint + args
  entrypoint 可以有两个来源:

  * 使用镜像中保存的 entrypoint. 它来自 dockerfile 中指定的 ENTRYPOINT 或默认的
    ``["/bin/sh", "-c"]``.

  * 使用 ``docker run --entrypoint`` 指定的 entrypoint, override 镜像中的.

  args 可以有两个来源:

  * 使用镜像中保存的 args. 它来自 dockerfile 中 CMD 提供的参数或默认的 ``[]``.

  * 使用 ``docker run ... args`` 提供的参数 override 镜像中的.

- ENTRYPOINT 可进一步被 ``docker run --entrypoint`` override.

- entrypoint script ``entrypoint.sh``.

  ENTRYPOINT 经常写成一个 script, 在里面可以进行任何设置、操作等等, 然后在
  最后一步 exec 成为所需执行的命令或服务 (保证是 PID 1 以接受 docker 发的
  signal).

  若服务应该以 non-root user 运行, 在 entrypoint script 最后使用 ``gosu`` 执行命令.
  gosu 比 su/sudo 更适合 container 使用, 因为它保证 PID1 是要执行的命令, 而
  su/sudo 只是 fork 要执行的命令, 自己作为父进程, 导致它们在容器中是 PID1, 造成
  不必要的麻烦.

CMD
~~~
::
  CMD ["cmd", ...]
  CMD ["param", ...]
  CMD <command>

- Only one CMD instruction in one build stage.

- The main purpose of a CMD is to provide default command execution for an
  executing container.  Don’t confuse RUN with CMD. RUN actually runs a command
  and commits the result at build time; CMD does not execute anything at build
  time, but specifies the intended command for the runtime container.

- 根据镜像目的不同, 默认的 CMD 命令也有所不同. 对于 service 类型的镜像, 默认
  执行的命令应该就是要执行的 service command, in foreground mode. 对于一些
  无专属功能的, 或者说更加通用的镜像, 例如一个 distro image, python image, etc,
  默认的 CMD 常常就是一个 interactive shell. 例如 bash, python.

- CMD 可被 ``docker run`` 的命令行执行的命令和/或参数覆盖.

EXPOSE
~~~~~~
::
  EXPOSE <port>[/<protocol>] ...

- Expose one or more ports. expose port 指的是将容器的端口绑定到 host system
  的指定端口上. 也就是做一次端口转发. 这是为了便于其他系统连接宿主机来访问容器
  服务. 若容器之间通过 bridged network 或者 overlay network 连接, 内部通信
  是不需要 expose 端口的. 这就是普通的同网段内机器通信.

- The EXPOSE instruction does not actually publish the port. It functions as a
  type of documentation between the person who builds the image and the person
  who runs the container, about which ports are intended to be published.

- To actually publish the exposed ports, use ``-p`` or ``-P`` during ``docker run``.

- 镜像 exposed ports 可通过 ``docker inspect`` 看到.

ARG
~~~
::
  ARG <name>[=<default>]

- 设置 current build stage 的环境变量.

- scope. 从变量的定义处开始, 至当前 build stage 结束. To use an arg in multiple
  stages, each stage must include the ARG instruction.

- 注意 ARG 环境变量的目的是为 build time 的各个指令提供环境变量. 不会保存在镜像
  中. 在 runtime, 即对于容器最终运行的进程不可见.

- 在 build time, 对 ARG 变量赋值或 override dockerfile 中提供的默认值,
  使用 ``docker build --build-arg``.

- predefined ARGs::
    HTTP_PROXY, http_proxy, HTTPS_PROXY, https_proxy, FTP_PROXY, ftp_proxy,
    NO_PROXY, no_proxy
  它们无需在 dockerfile 中声明可以直接赋值和引用.
  为避免信息泄露, by default, these pre-defined variables are excluded from the
  output of docker history. (注意在 docker history 中, ``ARG var=default`` 会
  泄露, 但引用时不会泄露因为历史中显示为 ``... $var``.)

- ARG 和 ENV 的关系.

  * 两者都是设置环境变量的. 但是它们的生效范围不同.

  * 两者的 override 方式不同.

  * At build time, ENV variable always override ARG variable of the same name.

ENV
~~~
::
  ENV <key>=<value> ...

- 设置 build-time 和 runtime 环境变量.

- ENV 变量在 build time 与 ARG 变量同时生效, 但只有 ENV 变量才最终保留在
  镜像中, 在 container runtime 生效.

- 在 runtime, override ENV 变量值是通过传入环境变量的方式, 即
  ``docker run -e``.

- ENV 环境变量可通过 ``docker inspect`` 查看.

COPY
~~~~
::
  COPY [--chown=<user|id>:<group|id>] <src> ... <dest>

- ``<src>`` may be file, directory.

- Multiple ``<src>`` may be specified, but if they are files or directories,
  their paths are interpreted as relative to the source of the context of the
  build.

- If ``<src>`` is a directory, the entire contents of the directory are copied,
  including filesystem metadata. The directory itself is not copied, just its
  contents.

- ``<src>`` may contain Go wildcards, like shell glob.

- ``<dest>`` ends with ``/`` 才会认为是 directory, 否则就认为是 regular file.

- ``<dest>`` 所指 pathname 的所有缺失层级目录会自动创建, 对于 directory, 目录
  本身也会自动创建.

- ``--from=<name|index>`` flag, set source location as previous build stage
  or an existing image.

- 对 build 的每个步骤, 只 COPY 该步骤所需文件, 即每个步骤一个 COPY, 不要一次
  把所有文件 COPY 进来. 这样可以保证只要相应步骤所需文件内容没有变化, 相应步骤的
  cache 能够重用. Each step’s build cache is only invalidated if the
  specifically required files change.

ADD
~~~
::
  ADD [--chown=<user|id>:<group|id>] <src> ... <dest>

- ADD 不支持 COPY 的 ``--from`` flag. 除此之外, 支持 COPY 的所有功能.

- ``<src>`` 除了可以是 file, directory, 还可以是 url.

- If ``<src>`` is a local tar archive in a recognized compression format then
  it is unpacked as a directory. 注意这只针对 local tar, 若 url 下载结果是 tar,
  不会被 unpack. 根据文件内容来判断文件是否是 tar archive, 而不是根据文件名后缀.

- copy local files 应该使用 COPY. add tar archive or add remote url files 时使用
  ADD.

- Because image size matters, using ADD to fetch package source from remote URLs is
  strongly discouraged. 使用 RUN 去下载、使用、删除一个命令完成.

VOLUME
~~~~~~
::
  VOLUME ["mountpoint", ...]

指定一系列 mountpoints, 在容器运行时, 会自动创建一个 anonymous volume 挂载在
mountpoint.  docker run 可以通过 ``-v``, ``--mount`` 参数明确指定 volume 或
bind mount, override 默认创建 的 anonymous volume.

The docker run command initializes the newly created volume with any data that
exists at the specified location within the base image. If any build steps
change the data within the volume mountpoint after it has been declared, those
changes will be discarded.

USER
~~~~
::
  USER <user|id>[:<group|id>]

Specify user and/or group name/id used by any following RUN, CMD, ENTRYPOINT
instructions.

WORKDIR
~~~~~~~
::
  WORKDIR /path

- Set working directory in image for any following RUN, CMD, ENTRYPOINT,
  COPY, ADD instructions, for current build stage.

- If the WORKDIR doesn’t exist, it will be created.

- For clarity and reliability, you should always use absolute paths for your
  WORKDIR.

- use WORKDIR instead of ``RUN cd … && do-something``.

STOPSIGNAL
~~~~~~~~~~
::
  STOPSIGNAL <signal|id>

Set the signal to be sent to container when ``docker stop``.

HEALTHCHECK
~~~~~~~~~~~
::
  HEALTHCHECK [--interval=<duration>|--timeout=<duration>|
               --retries=N|--start-period=<duration>]
               (CMD <command>) | NONE

指定应用层级的 health check 命令. 这非常有用, 甚至有必要.

``<duration>`` is number + unit, like ``3s``, ``5m``.

``NONE`` disable healthcheck from base image.

选项默认值:

- interval: 30s

- timeout: 30s

- start period: 0s

- retries: 3

设置 HEALTHCHECK 之后, 容器在运行时, ``docker container ps`` 的 STATUS 列输出
会包含 health status 信息. This status is initially starting. Whenever a health
check passes, it becomes healthy (whatever state it was previously in). After a
certain number of consecutive failures, it becomes unhealthy.

检查逻辑:

- 当容器启动后, 首先等待 ``--interval`` time, 执行第一次检查. 此后每隔
``--interval`` time 执行一次检查 (当前一次检查结束后开始计算).

- If a single run of the check takes longer than ``--timeout`` then the
  check is considered to have failed.

- 若连续 ``--retries`` 次检查都失败, 则认为容器 unhealthy.

- ``--start-period`` provides initialization time for containers that need time
  to bootstrap. Probe failure during that period will not be counted towards
  the maximum number of retries. However, if a health check succeeds during the
  start period, the container is considered started and all consecutive
  failures will be counted towards the maximum number of retries.

命令 exit code 与状态的对应关系:

- 0: healthy.

- 1: unhealthy.

- 2: 目前没用, reserved.

不要返回其他的值.

debug info. To help debug failing probes, any output text (UTF-8 encoded) that
the command writes on stdout or stderr will be stored in the health status and
can be queried with docker inspect. Such output should be kept short (only the
first 4096 bytes are stored currently).

event. When the health status of a container changes, a `health_status` event is
generated with the new status.

LABEL
~~~~~
::
  LABEL <key>=<value> ...

- add metadata to image.

- Labels included in base or parent images (images in the FROM line) are
  inherited by your image.

ONBUILD
~~~~~~~
::
  ONBUILD <instruction>

- The ONBUILD instruction adds to the image a trigger instruction to be
  executed when the image is used as the base for another build.

- ONBUILD instruction 会保存在当前镜像的 manifest 中, 可通过 inspect 查看.
  除此之外, 它不影响当前镜像的 build result.

- The trigger will be executed in the context of the downstream build, in the
  same order they were registered, as if it had been inserted immediately after
  the FROM instruction in the downstream Dockerfile.

- 当一个镜像本身的目的是作为 build 应用镜像的工具时, ONBUILD instruction 很有用.
  例如用于 automating the build of your chosen software stack.
  .. code:: dockerfile
    FROM maven:3-jdk-8
    
    RUN mkdir -p /usr/src/app
    WORKDIR /usr/src/app
    
    ONBUILD ADD . /usr/src/app
    
    ONBUILD RUN mvn install

- ONBUILD triggers are not inherited by grand-children images.

parser directives
-----------------

escape
~~~~~~
设置 dockerfile 中用于 escape 的 char. default is ``\``.

parameter substitution
----------------------
dockerfile 中支持进行 bash-like parameter substitution syntax. 可以替换的
变量是 ENV 设置的环境变量.

支持的语法:

- ``$var``

- ``${var}``

- ``${var:-default}``

- ``${var:+default}``

注意: Environment variable substitution will use the same value for each
variable throughout the entire instruction.
.. code:: dockerfile
  ENV abc=hello
  # the following "def" is "hello"
  ENV abc=bye def=$abc
  # the following "ghi" is "bye"
  ENV ghi=$abc

dockerignore
============
``.dockerignore`` 放在 root directory of build context.
It is a newline-separated list of patterns similar to the file globs of Unix
shells.
Line comment ``#`` is allowed and must start at the beginning of lines.

Allowed patterns:

- ``*``

- ``**``

- ``?``

- ``!<pattern>``. negate exclusion.

Note: the last line of the .dockerignore that matches a particular file
determines whether it is included or excluded.

dockerignore file 中甚至可以或者应该包含 ``Dockerfile`` & ``.dockerignore``
entries. 因为 dockerignore file 控制的是 build context 的组成. 进而影响
例如 ``COPY .`` 等复制进镜像的文件有哪些.

如果希望只在 build context 中包含指定文件, 排除所有其他文件::
  *
  !file-1
  !file-2

networking
==========

data
====
数据的存储方式
--------------

四种方式.

* volume.
  应用数据、日志等有价值的 persistent data 应使用 volume 存储在容器环境之外.

* bind mount.
  在研发阶段, bind mount 用于共享源代码进容器环境.
  bind mount 也用于 production 时在容器之间、容器和 host 之间等进行文件和配置
  共享.

  - docker config.
    swarm service 使用的线上配置类型的数据, 例如配置文件, 使用 docker
    config 保存. 将配置从 image 中抽离出来, 提高了容器镜像的通用性,
    让一些必须在 runtime 进行配置的项修改起来方便很多 (避免了 bind mount).

* tmpfs mount.

  适合放置 non-persistent state data. 例如敏感信息密码、证书, 或者为了某些情况下
  需要高速读写.

  - docker secret.
    swarm service 需要使用的不该明文保存的敏感数据, 例如 password,
    SSH private key, SSL certificate 等, 使用 docker secret 保存.
  
* writeable layer.
  直接写在 container writeable layer 上的内容, 只应该是体积不大的, 临时
  性质的、可随时销毁的 runtime content.


- 在 writable layer of container 保存数据的问题:

  * 难以将数据从容器中取出来. 即 persistent content (data) 和 disposable content
    (container + runtime products) 的耦合关系太密切.

  * writable layer 通过 union filesystem 工作, 是多层的叠加. 因此它的效率
    是低于直接读写 host filesystem 的 (data volume).

  * increase the size of container.

data volume
-----------
Volumes are stored in a part of the host filesystem which is managed by Docker,
under ``/var/lib/docker/volumes/``.
Non-Docker processes should not modify this part of the filesystem.

Multiple containers can use the same volume in the same time period. This is
useful if two containers need access to shared data. For example, if one
container writes and the other reads the data.

By default, when a container stops or is removed, the volume still exists.
Volumes are only removed when you explicitly remove them.

copy
~~~~
对于 mountpoint 位置本身有数据时, empty volume, non-empty volume 和 bind mount
的处理是不同的:

- empty volume: 容器内挂载点的数据会复制到 volume 中.

- non-empty volume & bind mount: Linux 正常方式, 直接挂载.

swarm mode notice
~~~~~~~~~~~~~~~~~
swarm mode 与 named volume 注意事项.
Swarm does not currently orchestrate volumes. The syntax
is very purposefully ``--mount`` and not ``--volume`` for this reason.
对于一个 service 的多个 replicas, 是 "mount" 这个 volume, 创建 volume 只是
副作用. 注意若一个节点上有多个 replicas, named volume 只创建一个, 而多次
bind mount. 这可能不是想要的结果. 此时, 应使用 anonymous volume.

volume drivers
~~~~~~~~~~~~~~
除了 local driver 之外, volume drivers 可以是别的形式, 例如 remote hosts, cloud
storage. volume drivers 是 docker plugins.

- local.
  默认的 volume driver 是 ``local``. local data volume (with ``local`` driver),
  本质上和 bind mount 是类似的, 只不过 source 目录在 docker 自己控制下.


bind mount
----------
just bind mount. 读写效率高. data volume & bind mount 各有用途.

tmpfs mount
------------
mount tmpfs into container, i.e. memory only, non-persistent.
在容器启动时生成, 停止时销毁.

docker config
-------------

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

object label
------------
每种 docker object 都可以添加自定义的 label, 即 metadata.

CLI
===

engine
------

container
~~~~~~~~~

- docker container run, docker run.

  ``--hostname``. 默认情况下容器的 hostname 是它的 short UUID, 该选项
  指定 hostname.

  ``--volume=[HOST-SPEC:]MOUNTPOINT[:OPTIONS]``.
  支持 bind mount data volume 或 host dir.
  HOST-SPEC can be:

  * absolute path on host. bind mount.

  * a name. use the specified data volume. if not pre-exist, create one.

  * omitted. create a anonymous data volume.

  MOUNTPOINT must be a absolute path in container.

  OPTIONS can be a combination of:

  * ro, rw. access mode.

  * consistent, cached, delegated. consistency requirement.

  * nocopy. disable automatic copying of data from the container path to the volume.

  * [r]shared, [r]slave, [r]private.

  * z, Z. selinux.

  ``--tmpfs=MOUNTPOINT[:OPTIONS]``.

  ``--mount=type=TYPE[,OPTIONS]``.
  combine ``--volume`` 和 ``--tmpfs``.

  TYPE can be bind, volume, tmpfs.
  OPTIONS can be a combination of:

  * src, source. mount source.

  * dst, destination, target. mountpoint.

  * readonly.

  以及 type-specific options.

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
  最终的根目录下都要有 Dockerfile 文件, 或通过 ``--file`` 指定. 整个
  build context 会传给 docker daemon. build context & Dockerfile 是构建
  镜像的两个必须元素.

  对于 local path, 该目录作为 build context 全部传输给 daemon;

  对于 tarball 等 url, daemon 先下载再解压作为 build context;

  若 url 指向一个 git repository, daemon 先 clone 再作为 build context.

  ``--tag`` 可以指定多次, 设置多个 tag.

  ``--cache-from``, 直接指定 cache source, 能用就用, 不能用拉倒, 别搜索.
  可以指定 remote image, 会自动 pull 下来.

  ``--target``. 指定目标 build stage. 用于 multi-stage build 生成不同阶段的
  镜像.

  build 过程中每个 layer 构建完成后会输出该层的 sha256 hash.
  若该层使用了 cache, 会输出 `Using cache`.

- docker image pull, docker pull.

  ``docker pull <name>`` 命令后面的 image name 即标准的 image tag 形式.

  e.g., ``docker pull ubuntu`` 实际是 ``docker pull docker.io/library/ubuntu:latest``.

- docker image import, docker import.
  Create base image from imported filesystem tarball.

- docker image save, docker save.
  将一个 repository 以 tarball 形式保存导出. 即一系列 images, 它们的所有 layers,
  包含所有 parent layers, 以及所有的 image tags.

- docker image load, docker load.
  将 ``docker image save`` 导出的 repository tarball 导入 local registry.

- docker image history, docker history.
  输出镜像各层的构建历史. 包含构建镜像各层的 instructions, 各层的体积,
  时间, hash 等信息.

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

- docker stack deploy.
  deploy 时会自动 docker pull 所需镜像.

- docker stack rm.

- docker stack ls. list stacks in swarm.

- docker stack ps. list tasks in the specified stack.

service
~~~~~~~
- docker service create. create a service.
  支持一些类似 docker run 的参数以及 compose file 的内容.

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

volume
~~~~~~

- docker volume create.
  create named or anonymous volume.
  默认使用 local driver, 可以指定别的 driver.

  ``--opt, -o``. driver options. The built-in local driver on Linux accepts
  options similar to the linux mount command.

- docker volume ls.

- docker volume inspect.

- docker volume prune.
  remove unused volumes.

- docker volume rm.

plugin
~~~~~~

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

在设计应用时, 应该考虑到如何能够将应用以服务的方式扩展到多个实例, 水平扩展以及
HA. 利用 docker stack/service etc. 提供的 scale functionality.

即使只需运行一个应用实例, 也应该使用 docker swarm 方式部署. 因可以使用
docker secret, config 等让很多方面更便捷, 更通用.

swarm 中的各个 node 应该互为 ntp peer, 并设置相同的 upstream ntp server,
以保证时间一致.

strategies
----------
Swarm managers can use several strategies to distribute containers in the
cluster.

stack
=====

A stack is a group of interrelated services that share dependencies, and can be
orchestrated and scaled together, these may be defined using a docker-compose.yml
file.

一个 stack 就是一个 app. 一个 stack/app 可以有多个 services, 每个 services
可以有多个 tasks.

docker stack 重用 docker-compose.yml 配置. 原因是两者在配置上是十分相似的.
它在 docker-compose.yml 中可以配置多实例并行和负载均衡.

修改 compose file 之后 re-deploy 不需要先删除当前的 stack, 而是直接 in-place
update. 其实这也容易理解, 因为有状态的存储部分和无状态的容器部分在 compose
file 中区分和定义的是清晰的. 所以知道该如何更新.

docker re-deploys stack in non-disruptive way.

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

common images
=============

buildpack-deps
--------------
It includes a large number of "development header" packages needed by various
things like Ruby Gems, PyPI modules, etc.

The main tags of this image are the full batteries-included approach. With
them, a majority of arbitrary gem install / npm install / pip install should be
successful without additional header/development packages.

buildpack-deps is designed for the average user of docker who has many images
on their system. It, by design, has a large number of extremely common Debian
packages. This reduces the number of packages that images that derive from it
need to install, thus reducing the overall size of all images on your system.

主要镜像分类:

- ubuntu based releases

- debian based releases

- `curl` variants and `scm` variants

python
------
主要镜像分类:

- ``python:<version>``

  based on buildpack-deps debian images. defacto images.

- ``python:*slim*``

  based on debian slim images, 而不是 buildpack-deps. This image does not
  contain the common packages contained in the default tag and only contains
  the minimal packages needed to run python.

- ``python:*alpine*``

  Based on alpine. Recommended when final image size being as small as possible
  is desired. The main caveat to note is that it does use musl libc instead of
  glibc and friends, so certain software might run into issues depending on the
  depth of their libc requirements.

注意 python 应用为了能够稳定输出日志给 ``docker logs``, 需要设置解释器为 unbuffered
mode::
  ENV PYTHONUNBUFFERED=1

nginx
-----
- ``nginx-debug`` binary produces verbose output when using higher log levels.

- always run with ``nginx -g 'daemon off'``

主要镜像分类:

- ``nginx:<version>``
 
  based on debian slim images. defacto images.

- ``nginx:*alpine*``

rabbitmq
--------

主要镜像分类:

- ``rabbitmq:<version>``

  based on debian slim images. defacto images.

- ``rabbitmq:*management*``

  ditto, with management plugin.

- ``rabbitmq:*alpine*``

mysql
-----

主要镜像分类:

- ``mysql:<version>``

  based on debian images.

- alpine might be coming (sucks).

- 为了默认情况下可以远程连接,

  * bind address 使用了默认的 ``*``.

  * root user 已经设置为 ``root@%``. 所以接受从任何 host 访问.

- 配置文件. 设置完整的 my.cnf 放在 ``/etc/mysql.conf.d``. 因为
  容器的配置应该统一. 一个配置文件已经足够, 所有配置放在里面.

- 为了配置方便, 预设了一系列环境变量.

  * MYSQL_ROOT_PASSWORD. mandatory.

  * MYSQL_DATABASE. db to create on startup.

  * MYSQL_USER, MYSQL_PASSWORD. user to create. will be granted all
    perms on MYSQL_DATABASE.

  * ...

  Note that none of the variables will have any effect if you start the
  container with a data directory that already contains a database: any
  pre-existing database will always be left untouched on container startup.

  MYSQL_ROOT_PASSWORD, MYSQL_ROOT_HOST, MYSQL_DATABASE, MYSQL_USER, and
  MYSQL_PASSWORD 支持 ``_FILE`` suffix to load value from file. 这样就支持
  docker secret & docker config.

- initialization scripts.

  When a container is started for the first time, it will execute files with
  extensions .sh, .sql and .sql.gz that are found in /docker-entrypoint-initdb.d.
  Files will be executed in alphabetical order. 这可以用于与应用相关的初始化
  配置, 以及数据恢复. SQL files will be imported by default to the database
  specified by the MYSQL_DATABASE variable.

misc
====
- ``/etc/hostname`` ``/etc/hosts`` ``/etc/resolv.conf`` 三个文件都是由 docker 生成后
  mount 至 container 文件系统相应位置的. 所以在容器内部的修改不会持久, 需要在命令行
  ``docker run|create`` 中修改或在 dockerfile 中修改.
