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

- 容器和容器之间、与各种非容器组件之间, 主要靠网络通信, 这样各组件之间的协作是
  与 docker platform 无关的. 容器可以等价代换非容器组件, 反之亦然.

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

- 构建镜像时, 如果设置了可以通过在 runtime 传入环境变量改变设置, 应该同时
  支持通过读取相应文件的方式修改设置. 例如 mysql, MYSQL_PASSWORD 环境变量
  同时可以从 MYSQL_PASSWORD_FILE 环境变量指向的文件读取. 这样可以更好地利用
  docker config & docker secret.

  这些逻辑一般在 dockerfile + docker-entrypoint.sh 中设置.

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

- 当一个项目中需要构建多个相互关联的镜像时, 各自的 dockerfile 中可能存在很多完全
  相同的部分. 那么如何避免重复, 提高重用性? 由于目前 dockerfile 还不支持 INCLUDE
  instruction, 可以尝试以下几个解决办法:

  * 重用镜像: 使用 multi-stage build 和 intermediate image, 来封装需要重用的部分.

  * 使用 m4/jinja2 等 macro/template processor 将模块化的 dockerfile snippets
    拼成一个 dockerfile.

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
  两部分都可以使用默认值或在 docker run 时 override 默认值.

  entrypoint:

  * 默认值来自 dockerfile 中指定的 ENTRYPOINT 或默认 ``["/bin/sh", "-c"]``.
    这保存在镜像中.

  * 使用 ``docker run --entrypoint`` 指定 entrypoint override 镜像中的.
    注意此时 CMD 也会被 override, 完全使用 docker run 后面跟的参数作为
    命令参数. (This makes sense, since original command has been overridden.)

  args:

  * 默认值来自 dockerfile 中 CMD 提供的参数或默认 ``[]``. 这保存在镜像中.

  * 使用 ``docker run ... args`` 提供的参数 override 镜像中的.

- entrypoint script ``docker-entrypoint.sh``.

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
    You can use secrets to manage any sensitive data which a container needs at
    runtime but you don’t want to store in the image or in source control.
  
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

在非 swarm mode 时, when a container stops or is removed, the volume still exists.
Volumes are only removed when you explicitly remove them. 对于同一个容器, 重新
启动后仍然使用原来的容器.

在 swarm mode, 由于 container 不是持久的, 只有 service 和 task 数目是持久的,
一般重启服务面临着 re-deploy 相应的 tasks. 若容器的 volume 是 anonymous 的,
就会被删除, 创建新的.

在 docker-compose 中, 重新部署一个 service 同样包含 destroy/re-create 容器.
原有的 volume 若是 anonymous, 不会被删除, 但重新创建容器时会新建 anonymous
volume. 原来 anonymous volume 里的数据会迁移至新的 anonymous volume.

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

keep in mind that the tasks (containers) backing a service can be deployed on
any node in a swarm, and this may be a different node each time the service is
updated.

In the absence of having named volumes with specified sources, Docker creates
an anonymous volume for each task backing a service. Anonymous volumes do not
persist after the associated containers are removed.

**If you want your data to persist, use a named volume and a volume driver that
is multi-host aware, so that the data is accessible from any node**. Or, set
constraints on the service so that its tasks are deployed on a node that has
the volume present.

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

tmpfs mounts cannot be shared among containers. 每次指定 tmpfs mount,
都会新生成一个内存区域挂载.

docker config
-------------
configs are not encrypted. they are mounted directly into container,
without using RAM disk.

A node only has access to configs if the node is a swarm manager or if it is
running service tasks which have been granted access to the config.

config file 以 base64 编码存储在 docker config 中.

A config that is being used by any tasks can not be deleted.

configurations are immutable, so you can’t change the file for an existing
service. 只能先删除再创建, 或换个名字. 若使用 docker service update 进行
rolling update, 只能换个名字然后使用 ``--config-add`` & ``--config-rm``
更换配置.

若 config 在 stack 中定义 (通过 compose file), 在 remove stack 时, 所有相关
configs 跟着删除.

mechanism
~~~~~~~~~
docker config 基本上和 bind mount 机制差不多. 但它是作用在 service 
上的, 因此自动分布式应用在所有相关 tasks 上而无论节点. 没有重复操作.
这是它相比与 bind mount config 的主要好处.

When you add a config to the swarm, Docker sends the config to the swarm
manager over a mutual TLS connection. The config is stored in the Raft log,
which is encrypted. The entire Raft log is replicated across the other
managers, ensuring the same high availability guarantees for configs as for the
rest of the swarm management data.

rotate a config
~~~~~~~~~~~~~~~
在服务运行过程中更新 docker config, you first save a new config with a
different name than the one that is currently in use. You then redeploy the
service (via ``docker service update`` or ``docker stack deploy``), removing
the old config and adding the new config at the same mount point within the
container.

docker secret
-------------
docker secret & docker config 在很多方面是相同的, 故不再重复.
除了 tmpfs mount & 加密等方面不同.

Secrets must be under 500KB in size.

A node only has access to (encrypted) secrets if the node is a swarm manager or
if it is running service tasks which have been granted access to the secret.
When a container task stops running, the decrypted secrets shared to it are
unmounted from the in-memory filesystem for that container and flushed from the
node’s memory.

mechanism
~~~~~~~~~
docker secret 使用 tmpfs mount, 并且加密保存和传输. 单独使用 tmpfs mount
在安全性和便利性上不如 docker secret.

When you grant a newly-created or running service access to a secret, the
decrypted secret is mounted into the container in an in-memory filesystem.

rotate secret
~~~~~~~~~~~~~
使用 ``--secret-add``, ``--secret-rm``. 其他类似 docker config.

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
  指定 hostname. 设置 ``/etc/hostname``.

  ``--network-alias``. 在网络中, 该容器的 dns label. 默认为 ``--name``.

  ``--dns``, ``--dns-search``, ``--dns-option``. DNS 相关参数, 通过这些
  参数设置 ``/etc/resolv.conf``.

  ``--volume=[HOST-SPEC:]MOUNTPOINT[:OPTIONS]``.
  支持 bind mount data volume 或 host dir.
  HOST-SPEC can be:

  * absolute path on host. bind mount.

  * a name. use the specified data volume. if not pre-exist, create one.

  * omitted. create a anonymous data volume.

  MOUNTPOINT must be a absolute path in container.

  OPTIONS can be a combination of:

  * ro, rw. access mode.

  * consistent, cached, delegated. consistency requirement (macOS).

  * nocopy. disable automatic copying of data from the container path to the volume.

  * [r]shared, [r]slave, [r]private. bind propagation.

  * z, Z. selinux.

  ``--tmpfs=MOUNTPOINT[:OPTIONS]``.

  ``--mount=type=TYPE[,OPTIONS]``.
  combine ``--volume`` 和 ``--tmpfs``.

  TYPE can be bind, volume, tmpfs.
  OPTIONS can be a combination of:

  * src, source. mount source. for bind mount, still needs to be absolute path.

  * dst, destination, target. mountpoint.

  * readonly.

  以及 type-specific options.

  For bind mount, ``--volume`` will create source directory if not already
  exist, whereas ``--mount`` will throw error in that case.

  ``--network={bridge|host|none|container:<name|id>|<network-name|id>}``
  连接的网络.

  ``--attach``. 决定 PID1 的相应 stream 是连接到 docker logs 还是容器外的
  console 的对应 stream 上. 不 attach 相应 stream 则与 docker logs 连接.
  若不设置, 默认 attach stdout/stderr.

  .. TODO WTF???????????????????????????? 乱七八糟, 看系统编程, 看源代码!!!!!!!!!

  ``--interactive``. 控制是否 keep stdin open. 设置这个 flag 后同时会 attach
  stdin. 若要保证 PID1 能从外界获取输入, 必须设置这个 flag. 若不设置这个 flag,
  则 stdin 会被 close (除非设置了 -t flag, 此时 stdin 连着一个 char device).
  若是 shell 等 interactive 程序, 读不到东西就自动退出了.

  .. TODO WTF???????????????????????????? 乱七八糟, 看系统编程, 看源代码!!!!!!!!!

  ``--tty``. 分配 pseudio terminal. 一些程序会根据自己连接的 stdin/stdout/stderr
  streams 是否是 tty 作出不同的响应. 例如 shell 是否输出 prompt. 以及连接 tty
  则会 pass through signal to PID1. 此时, 连接 PID1 的 3 个 streams 都是 tty
  character device, 若没有 tty flag, 三个 stream 都是 pipe. 无论
  stdin/stdout/stderr 是否 attach. 若 attach 则输出到 容器外的 console 上,
  否则就输出到 docker logs 中.

  .. TODO WTF???????????????????????????? 乱七八糟, 看系统编程, 看源代码!!!!!!!!!

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

- docker container attach, docker attach.
  attach container 实际上就是将 PID1 的 stdin/out/err 与 local console 的相应
  流连接起来. 从而可以看进程输出或者进行交互. 可以 *同时* 对一个容器 attach 多次.

  .. TODO attach 之后如何 detach, 根据不同的 docker run 模式和 docker attach
  选项有不同的结果!!!!! 看源代码解决.

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

  build 过程中每个 layer 构建完成后会输出该层的 sha256 hash.
  若该层使用了 cache, 会输出 `Using cache`.

  ``--tag`` 可以指定多次, 设置多个 tag.

  ``--cache-from``, 直接指定 cache source, 能用就用, 不能用拉倒, 别搜索.
  可以指定 remote image, 会自动 pull 下来.

  ``--target``. 指定目标 build stage. 用于 multi-stage build 生成不同阶段的
  镜像.

  ``--file``. 指定 dockerfile.

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

  ``--advertise-addr`` 若 node 有不止一个 NIC, 则需要指定这个参数.
  否则可能造成服务之间无法通信.

  ``--datapath-addr``

- docker swarm join.

  ``--advertise-addr`` 若 node 有不止一个 NIC, 则需要指定这个参数.

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

  * ``--compose-file``

- docker stack rm.

- docker stack ls. list stacks in swarm.

- docker stack ps. list tasks in the specified stack.

- docker stack services. list services in the stack.

service
~~~~~~~
- docker service create. create a service.
  支持一些类似 docker run 的参数以及 compose file 的内容.

  * ``--config=[NAME|OPTIONS]``. 给 service 分配 docker config.

    NAME 即 config name. 此时其他参数全默认值.

    OPTIONS can be a combination of:

    - src, source.

    - target. 默认为 ``/<source>``

    - uid. 可以是 uid or username.

    - gid. 可以是 gid or group name.

    - mode.

  * ``--secret=[NAME|OPTIONS]``. 分配 docker secret.

    NAME 即 secret name. 此时其他参数全默认值.

    OPTIONS can be a combination of:

    - src, source.

    - target. 默认为 ``/run/secrets/<source>``.

    - mode.

  * ``--endpoint-mode={vip|dnsrr}``. 访问 service 时如何 load balance 各个 tasks.

  * ``--network={NAME|host}`` NAME 为 overlay network name, 或者使用 host network.

  * ``--publish={<published:target>|OPTIONS}``. OPTIONS can be:

    - published.

    - target.

    - protocol.

    - mode.

  * ``--hostname``.
    
  对于 ``--hostname``, ``--mount``, ``--env`` 支持参数化 template.

- docker service ls. list services in swarm.

- docker service ps. list tasks of the specified services.

- docker service update. update a running service.
  更新服务还可以通过修改 compose file, 然后 re-deploy stack.

- docker service logs. 可以查看一个服务的整体日志, 按照 task 分开显示.

config
~~~~~~
- docker config create.
  支持从 stdin 创建配置. config name 必须唯一, 不能重复.

- docker config ls.

- docker config inspect.

  ``--pretty``. use yaml-like format output.

- docker config rm.

secret
~~~~~~

- docker secret create.

- docker secret ls.

- docker secret inspect.

- docker secret rm.

object
~~~~~~

- docker inspect. insepct any docker objects.
  实际上各个主要 docker object 的子命令中还有 inspect 命令专门查看该类型对象.

registry
~~~~~~~~

- docker login.

- docker logout.

network
~~~~~~~

- docker network create.

  ``--driver``. 默认使用 bridge driver.
  只有 swarm manager 可以创建 overlay network.

  ``--subnet``. 指定 subnet.

  ``--ip-range``. allocate container ip from this range.

  ``--gateway``. gateway ip.

  ``--ingress``. create swarm routing-mesh network.

  ``--attachable``. 

  ``--ipv6``. enable ipv6.

  ``--opt``. 自定义网络参数.

- docker network ls.

- docker network inspect.
  输出还包括各个 attached container 的网络信息, 例如 ip.

- docker network connect.
  一个容器可以连接多个网络.

  ``--ip``, ``--ip6``, 连接时可以指定 ip. 对于自定义的网络.

- docker network disconnect.
  disconnect container from network. 断掉后容器内的相应虚拟网卡直接消失.
  注意这个操作是在修改容器的网络连接配置, 所以是持久的 (make sense).

- docker network rm.

- docker network prune.
  remove unused networks.

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

同一个 compose file 在通过 docker-compose 和 docke stack deploy 使用时,
在效果上具有一些不同之处. 但绝大部分参数具有共同之处.

networking
----------
- By default Compose sets up a single network for your app. Each container for
  a service joins the default network and is both reachable by other containers
  on that network, and discoverable by them at a hostname identical to the
  container name.

- 可以通过 service-level 的 ``networks`` key 以及 top-level ``networks`` key
  自定义每个服务要连接到的网络. compose 默认创建的那个网络叫做 ``default``.

compose file
============

overview
--------

- Format: yaml.

- content: defining services, network, volumes, configs, secrets, etc.
  for a docker stack (in swarm mode) or a composed container set (in
  standalone mode).

parameter substitution
~~~~~~~~~~~~~~~~~~~~~~
- compose file 内支持 shell parameter substitution syntax 使用环境变量的值.
  这可用于将某些 flag 或量参数化. 避免每次修改都要该 compose file.

支持的语法:

- ``$var``

- ``${var}``

- ``${var:-default}``

- ``${var-default}``

- ``${var:?err}``

- ``${var?err}``

- ``$$``

extension fields and merge
~~~~~~~~~~~~~~~~~~~~~~~~~~
top-level keys can be named starting with ``x-``, where the entire
tree is ignored by parser. This is useful to construct yaml anchor nodes,
for collecting common configs into one place.

yaml ``<<`` merge indicator is also supported.

使用 yaml 的这些语法, 相当于 compose file 具有了变量抽象、赋值和引用能力.

version info
------------

version
~~~~~~~
String. Compose file format is versioned.

compose file versions:

- Version 1, the legacy format. This is specified by omitting the version key.

- Version 2, specified with ``version: '2'`` ``version: '2.1'`` etc.

- Version 3, designed to be cross-compatible between Compose and the swarm mode,
  ``version: '3'`` ``version: '3.1'`` etc.

build configs
-------------

build
~~~~~
one of the either:

- A string to build context.

- A mapping with keys:
  
  * context
   
  * dockerfile
   
  * args. build args. A mapping of key-vals or a list of ``key=val``.
    You can omit the value when specifying a build argument, in which case its
    value at build time is the value in the environment where Compose is
    running

  * cache_from. a list of images.

  * labels. a mapping of labels.

  * shm_size.

  * target.

若该服务下还有 image key, build result image 会被 tag 为相应镜像和 tag.

注意: docker stack 只接受 pre-built images, 在 swarm mode 中不能使用 build
option.

service configs
---------------

cap_add, cap_drop
~~~~~~~~~~~~~~~~~
注意 not usable in docker stack.

command
~~~~~~~
override ``CMD`` in dockerfile. string or list.

configs
~~~~~~~
a list of docker configs applied to this service.

对于每个 config, 可以:

* 使用 short syntax, 此时只需指定 config name as string.

* 使用 long syntax, 此时每项是 mapping. 包含: source, target, uid, gid, mode.

secrets
~~~~~~~
a list of secret names, or a list of mappings with keys source, target, uid,
gid, mode.

cgroup_parent
~~~~~~~~~~~~~
ignored in swarm mode.

container_name
~~~~~~~~~~~~~~
ignored in swarm mode.

deploy
~~~~~~
only usable in docker swarm, otherwise ignored. define docker service parameters.

keys:

* endpoint_mode.

* labels.

* mode

* placement

  keys:
  
  - constraints.
  
  - preferences.

* replicas.

* resources.

* restart_policy.

* update_config.

labels
~~~~~~
container labels.

devices
~~~~~~~
ignored in swarm mode.

depends_on
~~~~~~~~~~
ignored in swarm mode.

dns
~~~
a string or list.

dns_search
~~~~~~~~~~
a string or list.

tmpfs
~~~~~
ignored in swarm mode.

entrypoint
~~~~~~~~~~
a string or list.

env_file
~~~~~~~~
a string or list.

environment
~~~~~~~~~~~
a mapping or list of ``key=val``.

expose
~~~~~~
expose ports to other containers in the composed network.
.. TODO why needed? all ports are available from beginning.

external_links
~~~~~~~~~~~~~~
ignored in swarm mode.

extra_hosts
~~~~~~~~~~~
a list of "<host>:<ip>" strings added to /etc/hosts

healthcheck
~~~~~~~~~~~
like HEALTHCHECK.

image
~~~~~
image:tag or id.

isolation
~~~~~~~~~

logging
~~~~~~~
keys:

* driver.

* options. a mapping.

networks
~~~~~~~~
a list of networks. a network can be a string or a mapping of options.

keys:

- aliases. a list of strings.

- ipv4_address, ipv6_address.

pid
~~~
pid namespace.

ports
~~~~~
a list of port mapping strings in form of ``docker run --publish`` option,
or a list of mapping in form of ``docker service create --publish`` option.

security_opt
~~~~~~~~~~~~
ignored in swarm mode.

stop_grace_period
~~~~~~~~~~~~~~~~~
how long to wait for container stop before SIGKILL.
``[<n><unit>]+``

stop_signal
~~~~~~~~~~~
ignored in swarm mode.

sysctls
~~~~~~~
kernel parameters to set in the container.
ignored in swarm mode.

ulimits
~~~~~~~
a mapping of ulimit keys and values.
value can be a number or a mapping of soft and hard values.

userns_mode
~~~~~~~~~~~
ignored in swarm mode.

volumes
~~~~~~~
short syntax: a list of strings conforming to ``docker run --volume`` option
syntax.

long syntax: a list of mappings conforming to ``docker run --mount`` option
syntax. 对于每种类型, 支持 bind, volume, tmpfs 三个 key 指定 type-specific
options.

restart
~~~~~~~
ignored in swarm mode.

hostname
~~~~~~~~

ipc
~~~
ipc namespace

mac_address
~~~~~~~~~~~

privileged
~~~~~~~~~~
boolean.

read_only
~~~~~~~~~
boolean.

shm_size
~~~~~~~~

stdin_open
~~~~~~~~~~
keep stdin open. like ``docker run --interactive``

tty
~~~
boolean

user
~~~~
like ``docker run --user``

working_dir
~~~~~~~~~~~


docker config configs
---------------------

configs
~~~~~~~
declare docker configs. a mapping.

对每个 config:

* file. 配置源文件.

* external. 使用已经定义好的 docker config.

* name.

docker secret configs
---------------------

secrets
~~~~~~~

similar to configs key.

volume configs
--------------

volumes
~~~~~~~

volume mapping can be key-only. all options fallbacks to default.

keys:

* driver.

* driver_opts.

* external.

* labels.

* name.

network configs
---------------

networks
~~~~~~~~

keys:

* driver.

* driver_opts.

* attachable.

* ipam.

* internal.

* labels.

* external.

* name.

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

- network drivers: bridge, host, overlay, macvlan, none.

bridge network
--------------
当需要把多个独立的容器通过一个网络在一起, 可以相互通信时, 一般使用 bridge
network.

bridge network 中, 各个容器以及 host 主机与一个 software bridge 通过 veth 连通.
从而可以相互访问. 没有与该 bridge 连接的容器无法访问该网络内资源.
The Docker bridge driver automatically installs rules in the host machine so
that containers on different bridge networks cannot communicate directly with
each other.

由于 software bridge 由 host OS 实现, 位于 host 主机内部. 所以它构建的子网
只能覆盖同一台机器上的容器 (以及主机自身). 子网不能跨机器. 
bridge 默认设置了 NAT 和路由, 可以访问外网. 这样, software bridge 成为了
layer-3 switch. 若还需要外界能主动访问容器, 需要手动配置路由规则.

由于这些麻烦的存在, 使用 bridge network 时, 不同机器上的容器不容易相互直接通信.
这通过 overlay network 来解决. (或者使用 host network 来避免网络隔离.)

default bridge
~~~~~~~~~~~~~~
bridge 是创建 docker network 时默认使用的 driver.
It is considered a legacy detail of Docker and is not recommended for
production use.

默认的 bridge network 名为 bridge, 它在 OS level 中名字为 docker0
(``Options.com.docker.network.bridge.name``), 且不能删除. 新创建的
容器自动连接到这个 bridge network.

To configure the default bridge network, you specify options in daemon.json.
Then restart docker daemon to take effect.

default bridge vs user-defined bridge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
User-defined bridge networks are superior to the default bridge network.

- 对于 user-defined bridges, 容器运行时自动设置它在 network 中的 alias, 默认为
  container name. 自动 DNS 解析. 即在该网络中, alias 是该容器的 DNS A record.

- default bridge can only be configured via daemon configuration file. And
  daemon must be restarted to take effect. User-defined bridge can be
  configured at will.

overlay network
---------------
Overlay network lies over host-specific networks, 可以跨多个 docker hosts. 效果是
每个 host 上的容器所在的子网都是相通的, 可以抽象地认为这些不同机器上的容器都位于
同一个子网. 不同机器上的容器之间可以通过名字或 IP 直接访问.

overlay network 不是仅仅依靠标准的网络原理和配置实现的. 要借助应用层的实现和流量
转发. Docker daemons on multiple machines connect together to form the overlay
network, 并使用一个分布式存储维护网络状态. Docker transparently handles routing
of each packet to and from the correct Docker daemon host and the correct
destination container.

overlay network 一般用于 docker swarm mode.
使用 ``--attachable`` flag 创建的 overlay 支持独立容器使用, 从而 swarm 可以与
独立容器 (以及独立容器之间) 相互跨机器直接通信. (注意不是只有 swarm service
才可以直接跨机器通信的. 独立容器连入 overlay network 照样可以.) swarm service
和 standalone container 连入 overlay network 时, 都通过 --publish 实现整个集群
可见.

一个应用或者一组应用应该使用一个独立的 overlay network, 从而相互隔离.


default ingress & docker_gwbridge networks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When you initialize a swarm or join a Docker host to an existing swarm, two new
networks are created on that Docker host:

- an overlay network called ``ingress``, which handles control and data traffic
  related to swarm services. When you create a swarm service and do not connect
  it to a user-defined overlay network, it connects to the ingress network by
  default.

  Customizing the ingress network involves removing and recreating it. Creating
  an ingress overlay network uses ``--ingress`` flag.

  ingress overlay network 不支持 attach standalone container.  You can name your
  ingress network something other than ingress, but you can only have one ingress
  network.

- a bridge network called ``docker_gwbridge`` that connects the overlay
  networks (including the ``ingress`` network) to an individual Docker daemon’s
  network.

  If you need to customize its settings, you must do so before initializing swarm
  or joining the Docker host to the swarm. By recreating the bridge network with
  custom settings. When entering swarm mode, Docker does not create it with
  automatic settings since it already exists.

ports
~~~~~

- TCP port 2377 for cluster management communications.

- TCP/UDP port 7946 for container network discovery.

- UDP port 4789 for the container ingress network.

routing mesh
~~~~~~~~~~~~
By default, swarm services which publish ports do so using the routing mesh.
When you connect to a published port on any swarm node (whether it is running a
given service or not), you are redirected to a worker which is running that
service, transparently. Effectively, Docker acts as a load balancer for your
swarm services. Services using the routing mesh are running in virtual IP (VIP)
mode. Even a service running on each node (by means of the --global flag) uses
the routing mesh. When using the routing mesh, there is no guarantee about
which Docker node services client requests.

To bypass the routing mesh, you can start a service using DNS Round Robin
(DNSRR) mode, by setting the --endpoint-mode flag to dnsrr. You must run your
own load balancer in front of the service. A DNS query for the service name on
the Docker host returns a list of IP addresses for the nodes running the
service. Configure your load balancer to consume this list and balance the
traffic across the nodes.

在 overlay network 中, standalone container 也有 DNS entry. 这与在 bridge
network 中相同.

published ports 只在从外部向 overlay network 连接时使用. 即这些端口是 publish
至 network 上的 (把整个 overlay network 看成一个整体.). 在网络内部, 服务之间
仍然使用本来的端口直接连接. 对于 user-defined overlay network, virtual IP
在网络内部服务之间相互访问, 以及从外部向网络访问, 都可用.

encryption
~~~~~~~~~~
All swarm service management traffic is encrypted by default.
To encrypt application data as well, add ``--opt encrypted`` when creating the
overlay network. This enables IPSEC encryption at the level of the vxlan.

management and data traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~
swarm management traffic is encrypted by default. And by default, management
and data traffic run on the same network. The two traffic can be separated
to different network, if your nodes have two NICs. For each node joining the
swarm, specify --advertise-addr and --datapath-addr to separate management
and data traffic.

ingress overlay network vs user-defined overlay network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- The ingress network is special-purpose and only for handling publishing.

- Ingress network is not for production use.

- VIP 在 user-defined overlay network 内部服务之间也可以使用, 对于 ingress
  不能, 只能从外部访问时使用.

host network
------------
不使用网络隔离, 直接使用 host OS 的网络. 即在网络方面, 容器内部和 host OS 是
完全相同的. 例如, interface 相同, ip 相同, hostname 相同, 端口使用相同等等.

默认存在名为 host 的 network, 使用的就是 host driver.

none network
------------
不使用任何网络.

默认存在名为 none 的 network, driver 为 null.

macvlan network
---------------
Macvlan networks allow you to assign a MAC address to a container, making it
appear as a physical device on your network. The Docker daemon routes traffic
to containers by their MAC addresses. Using the macvlan driver is sometimes the
best choice when dealing with legacy applications that expect to be directly
connected to the physical network, rather than routed through the Docker host’s
network stack.

caveats:

- It is very easy to unintentionally damage your network due IP address
  exhaustion or to “VLAN spread”, which is a situation in which you have an
  inappropriately large number of unique MAC addresses in your network.

- Your networking equipment needs to be able to handle “promiscuous mode”,
  where one physical interface can be assigned multiple MAC addresses.

- If your application can work using a bridge (on a single Docker host) or
  overlay (to communicate across multiple Docker hosts), these solutions may be
  better in the long term.

networking configs
------------------
- ``/etc/hostname`` ``/etc/hosts`` ``/etc/resolv.conf``

  三个文件都是由 docker 生成后 mount 至 container 文件系统相应位置的.
  所以在容器内部的修改不会持久, 需要在命令行 ``docker run`` 中修改.

  docker 会自动在 hosts 中添加容器 hostname 和 IP 之间的映射; 指定
  DNS server 为 daemon 自己的 DNS.

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

alpine
------
那么小的 alpine 镜像里面居然有 ip, ping etc.

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

- 主要镜像分类:

  - ``nginx:<version>``
   
    based on debian slim images. defacto images.
  
  - ``nginx:*alpine*``

- 根据 nginx 的使用方法不同, nginx container 的部署方式也不同.
  
  在 swarm 中, 如果 nginx 就是为某一个服务的前端服务器, 提供请求转发和
  静态文件服务等, 即容器化的 nginx 是专门为单一应用服务的,  则可以部署一组
  nginx tasks 作为一组应用 tasks 的前端服务器. 不同应用创建不同的
  nginx service.

  如果是为多个服务做 proxy 或者别的, 则应该部署一个公用的 nginx service.

- logging.
  
  简单的 logging 配置使用默认的 ``/var/log/nginx/{access,error}.log`` 即可.
  它们 link 至 ``/dev/{stdout,stderr}`` 了. 从而默认就输出 main log 至 docker
  logs.

  复杂的 logging 需要配置 volume for logs.

- 配置文件.
 
  专门服务一个应用时, 覆盖 ``/etc/nginx/conf.d/default.conf`` 即可.
  服务多个应用时, 每个应用配置放在 ``/etc/nginx/conf.d`` 下面, 和平时一样.

- 静态文件应该放在 ``/usr/share/nginx/html`` 下面.

- expose 80, 443.

rabbitmq
--------

* 主要镜像分类:

  - ``rabbitmq:<version>``
  
    based on debian slim images. defacto images.
  
  - ``rabbitmq:*management*``
  
    ditto, with management plugin.
  
  - ``rabbitmq:*alpine*``

- 注意需要设置容器 hostname, 因为 rabbitmq stores data based on what it calls the
  "Node Name", which defaults to the hostname.

- ``/var/lib/rabbitmq`` 默认是一个 volume.

- environs:

  * RABBITMQ_VM_MEMORY_HIGH_WATERMARK

  * RABBITMQ_ERLANG_COOKIE

  * RABBITMQ_NODENAME

  * RABBITMQ_DEFAULT_VHOST

  * RABBITMQ_DEFAULT_USER 
    
  * RABBITMQ_DEFAULT_PASS

  * RABBITMQ_HIPE_COMPILE

  * RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS

mysql
-----

- 主要镜像分类:

  - ``mysql:<version>``
  
    based on debian images.
  
  - alpine might be coming (sucks).

- expose 3306.

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

- volume: /var/lib/mysql
