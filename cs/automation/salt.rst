- salt 支持多种 management models:
  agent-server (agent-based), agent-only, agent-less.

  不同的方式仅在 Salt 的使用方式上有区别 (例如 ``salt``, ``salt-call`` 等),
  salt 的所有 modules 可以在任何一种方式中使用.

- 在 jinja2 模板中可访问的 salt 参数 (除了标准 jinja 功能之外):

  * minion configuration values

  * grains

  * salt pillar data

  * salt execution modules

- salt file server

  * builtin file server (``file_roots``)

  * git file server, 可以使用这个直接从 git server 中取文件.

target selection
----------------

- target selection (``man salt(1)``).

  * minion id.

  * shell globbing.

  * PCRE regex.

  * Grain system with glob.

  * Grain system with PCRE.

  * target list.

  * all above combined.

Grains
------

- The static information SaltStack collects about the underlying managed system.

- grains types

  * core grains modules, 在 salt package 中 grains 部分的所有公有函数.

  * 自定义静态 grains data. 在 ``/etc/salt/minion`` 的 ``grains:`` 下面添加, 或者
    ``/etc/salt/grains`` 文件中添加. 例如, Add custom ``role`` grain to categorize
    minions by functionality.

  * custom grains modules. Custom grains modules should be placed in a
    subdirectory named _grains located under the file_roots specified by the
    master config file. The default path would be /srv/salt/_grains. Custom
    grains modules will be distributed to the minions when state.highstate is
    run, or by executing the saltutil.sync_grains or saltutil.sync_all
    functions.

  注意, grains 数据对特定的 minion 应该是相对静态的. 因此 custom grains module
  对特定 minion 应该生成比较稳定的输出. 并且这些数据是用于 targeting minions.

- grains 数据优先级从高至低:

  * custom grains modules ``salt://_grains``

  * custom grains data ``/etc/salt/minion``

  * custom grains data ``/etc/salt/grains``

  * core grains modules

- The content of /etc/salt/grains is ignored if you specify grains in
  the minion config.

- Since grains are simpler than remote execution modules, each grain module
  contains the logic to gather grain data across OSs (instead of using multiple
  modules and __virtualname__).

- ``grains.ls``, ``grains.items`` execution module 获取 grains 列表和 grains 数据.

- ``grains.get`` execution module 获取某项 grain 值.

- ``saltutil.refresh_modules`` execution module 更新 modules 和 grain data.

- ``saltutil.sync_grains`` 同步 custom grains modules 至各个 minion.

Execution
---------

- 格式 ``salt <target> <module>.<function> [args]...``
  对于 positional args 一般就做普通的 positional 在命令行上,
  对于 keyword args 使用 ``key=value`` 形式作为命令行参数.
  对于 list 和 dict 类型参数, 直接写 json 在命令行上.

- Execution functions.

  * ``state.apply``

    - parameters

      * ``test`` 进行 dry-run, 需要进行的状态改变会标黄, 不需要改变的状态
        维持绿色.

      * ``pillar`` 指定额外的 pillar data, 它覆盖 pillar file 中的同名参数.

  * ``state.show_sls``

  * ``pillar.items``

  * ``event.send``

  * ``sys.doc`` 获取 module/function doc.

  * ``grains.ls``

  * ``grains.items``

  * ``grains.get``

  * ``saltutil.refresh_modules``

  * ``saltutil.sync_grains``

  * ``saltutil.sync_all`` 同步各种 custom modules 至 minion.


- Execution functions vs State functions

  Salt state functions are designed to make only the changes necessary to apply
  a configuration, and to not make changes otherwise. Salt execution functions
  run each time they are called, which may or may not result in system changes.

State
-----

- State.

  A declarative or imperative representation of a system configuration.

- salt state tree.

  * A directory tree of state files located at ``file_roots``.

  * any other files and folders you place in ``file_roots`` are available
    to your Salt minions.

  * 在 salt states 中, 使用 ``salt://<path>`` 来引用 ``file_roots`` 下的文件,
    其中 ``<path>`` 是相对于 ``file_roots`` 的路径.

- State file.

  A file with an SLS extension that contains one or more state declarations.

  * ``include:`` 可以引用其他 state file in salt state tree.
    对于子目录, 使用 ``.`` 作为目录分隔符.

- State declaration.

  A top level section of a state file that lists the state function calls and
  arguments that make up a state.

  每个 state declaration 的顶层是这个状态的 unique name/id.
  State ID 可以包含 space & digits, 所以可以是一句状态描述.
  The ID should describe what the state is doing, even though it might
  require more typing.

  第二层是该状态需要实现的各项操作和状态结果 (module.function).

  再下面是 function 参数列表. 注意这个列表的每一项都是一个 参数名到参数值
  的 map.

- State function.

  Commands that you call to perform a configuration task on a system.
  所有的 state module 位于 ``salt.states`` subpackage.

  * 参数格式:
    每个 positional arg 参数使用: ``- value``.
    每个 kwarg 参数使用: ``- key: value``.
    若 value 是 list 或 dict, 采用普通 yaml 的相应语法.

  * ``pkg.installed``

  * ``pkg.removed``

  * ``file.directory``

  * ``service.running``

    - 使用 ``sig`` 参数设置从 ps 输出中搜索的字符串. 若设置了该参数, 使用系统默认
      的服务机制查询结果为没有运行, 会 fallback 至 ps 的方式.

  * ``git.latest``

  * ``user.present``

  * ``host.present``

  * ``module.run``

  * ``file.managed``

  * ``file.append``

  * ``file.recurse``

  * ``module.run`` 用于在 salt state 中执行 execution module.

- Top file

  The Top file is used to apply multiple state files to your Salt minions
  during a highstate. Targets are used within the Top file to define which
  states are applied to each Salt minion.

  Top file 中的 target pattern, 是对其下的状态的应用对象进行限制.

- Highstate.

  A highstate causes all targeted minions to download the /srv/salt/top.sls
  file and find any matching targets. If a matching target is found, the minion
  applies all of the states listed under that target.

  ``state.apply`` with no arguments starts a highstate.

- Salt YAML requirements.

  * 每层缩进推荐是 2 spaces.

  * quick vim config: ``# vim:ft=yaml:expandtab:tabstop=2:shiftwidth=2:softtabstop=2``.

  * 使用 ``vim-salt`` plugin.

- Execution order.

  * salt 的 state apply 是遵从固定的顺序的. 无论是默认的顺序还是自定义的顺序.

  * By default, each ID in a Salt state file is executed in the order it
    appears in the file. Additionally, in the Top file, each Salt state file is
    applied in the order listed.

  * ``state.show_sls`` execution module 查看某个 state file 中状态执行顺序.

- Requisites

  * 用于在 states 之间建立联系. 这可以包含修改默认的 states execution order 或者
    conditional state apply. 例如某文件修改时, 重启某服务.

Pillar
------

- Pillar 实际上是一系列分配给各 minion 的数据或参数. 它根据 target selection
  机制 对数据进行分配. 将 salt state 模板化, 对各个 minion 传入自定义的
  pillar data, 从而达到 salt state reuse 的目的.

- 与 state file 不同, pillar data 不是对所有 minion 共享的, 只有 matched target
  minion 才会收到分配给他的 pillar data. 所以可以用这个来存储 secure data.

- Salt pillar data is never written to disk on the minion.

- 查看 pillar data: ``pillar.items`` execution module.

- 为了保密, pillar yaml file 可以放在一个 private git repo 中.

Salt Mine
---------

- The Salt mine is used to share data values among Salt minions.

- 当某个数据是动态变化的, 可以由 master 或某个 minion 生成后放在 salt mine
  里进行共享.
  This is a better approach than storing it in a Salt state or in Salt pillar
  where it needs to be manually updated.

Event
-----

- 所有 salt 内部组件通过 sending/listening events 相互沟通.

- event 有两部分:

  * event tag.

    All salt events are prefixed with ``salt/``, with additional levels
    based on the type of event.

  * event data.

    Each event contains a timestamp ``_stamp``.

- custom events

  * presence events, default off.

  * state events, default off.

  * fire an event when a state completes: ``fire_event: True|<string>``

  * 使用 ``event.send`` 直接发送任意 event.

- salt beacon

  * 用于监控 salt 之外的系统状态, 当预设的状态、条件等满足时, 向 bus 发送
    该事件. 它应用 event system 实现.

  * 在 minion config 中的 ``beacons`` 部分配置.

Reactor
-------

- Reactor trigger reactions when events occur on event bus.

- 配置: master config 中的 ``reactor`` section. 只允许一个 reactor section.

- reactor file

  * 跟 state file 一样支持 jinja2.

  * Salt reactor SLS files execute on the Salt master.
    It is useful to think of them more as entry points into the salt and
    salt-run commands rather than as entry points into the Salt state system
    that executes on the Salt minion.

  * reactor file 中可以进行: remote execution, 执行 salt runner 操作, 执行 wheel 操作.

  * remote execution 格式:

    .. code:: yaml
      <operation_id>:
        local.<module>.<function>:
          - tgt: <target>
          [- tgt_type: <type>]
          - arg: <arg_list>

Runner
------

- Runners are modules that execute on the Salt master to perform supporting tasks.
  这些操作可能是关于 master 自己的, 或者是整个 master/minion 系统的管理性质的操作,
  总之不是直接去对 minion 进行操作.

- runner modules

  * ``state.event``

Orchestrate Runner
------------------

- orchestrate runner 用于配置 salt master 所管理的各系统之间的的依赖关系状态.
  默认情况下, salt 并发地对所有 minion 发布任务, 并且各 minion 之间是相互独立的.
  Orchestrate runner 允许配置 minion 之间的 dependency 关系, 状态应用的顺序,
  以及 (minion 级别的) 状态应用的条件等.

- The state.sls, state.highstate, et al. execution functions allow you to statefully
  manage each minion and the state.orchestrate runner allows you to statefully
  manage your entire infrastructure.

- orchestrate runner 与其他 runner 一样, 是运行在 master 上的 (这样才可以进行
  inter minion 的 orchestration, 就像乐团指挥一样).


Wheel
-----


Returner
--------

- 将执行结果 return 至某个数据库, 而不是返回至 master 端.


Salt Cloud
----------

docker
~~~~~~
docker 有两种使用模式, 这对应着 salt 与 docker 的搭配使用有两种模式:

1. 如果 docker container 是看作一个独立的虚拟机运行环境, 在其中运行一整套或者
   部分 userspace 进程体系, 这个运行环境一旦 spawn up 就不再轻易重建, 是持续
   运行的, 所需的修改是直接应用在容器环境中, 而不代表由 dockerfile 定义的状态.
   这样则适合在容器环境中安装 salt-minion, 进行自动化修改.

2. 如果 docker container 是看作一个 sandboxed 的应用, 对这个应用所做的所有修改
   都需要在 dockerfile 中保存状态、重新构建镜像、重新部署容器, 不会在容器内部
   进行应用状态修改. 这样意味着整个容器就代表着某个由 dockefile 定义的状态,
   从而不该在容器内部安装 salt-minion 进行 runtime 修改, 而是在 host machine
   中安装 salt-minion, 来应用容器状态 (即起停容器等操作).

对于第一种方式, 适合 docker cloud 的方式. 但是由于目前不支持 docker 作为
cloud privder, 所以只能手动做.

对于第二种方式, 有 docker-ng state module.

Configuration
-------------

- 不同方面的配置项应放在 ``master.d`` 或 ``minion.d`` 中的单独文件中.
  而不该直接修改 ``master`` ``minion`` 配置文件.

Salt SSH
--------

- Salt commands can be executed on remote systems using SSH instead of the Salt agent.
  这适用于以 agent-less 方式使用 salt.

- 要求 remote system 要有 sshd + python.

- 命令行: ``salt-ssh [target] [command] [arguments]``
  target 必须在 roster file 中定义, 且只能使用 file globs or regex 来匹配.

- roster file: 保存 remote system ssh info.
  无需在里面保存密码, 首次连接要求输入密码并创建 RSA key.

- salt ssh 使用 execution modules 进行远程操作. 使用 ``state.apply`` 应用 states
  时, 同样使用 ``file_roots`` 下面的文件.

- salt ssh 开多个进程并行连接远端.

Internals
---------

- All Salt minions receive commands simultaneously.

- 由于 minion 本地包含一切操作所需资源, 分配任务时仅需传输 instructions.
  The Salt master doesn’t do anything for a minion that it can do (often
  better) on its own.

- minion 向 master 的连接是持久的双向连接, 通过 ZMQ or raw TCP 连接,
  数据使用 MessagePack 格式传输, 用 tornado 实现 networking.

- 对于不同的系统, salt 的各种操作是相同的, 通用的.

- proxy minion 用于对本身不支持 python/salt 的系统进行转发管理.

- subsystems

  * authentication

  * file server

  * secure data store

  * state representation

  * return formatter

  * result cache

  * remote execution

  * configuration

  每个 subsystem 都可以通过不同的 plug-ins (subsystem modules) 来实现,
  满足相同的 API 即可.

- virtual module

  相同的 module name 在不同的 OS 等环境下实际上是对不同的 implementation module
  的重命名. 这类似于 ``os.path`` 与 ``posixpath``, ``ntpath`` 的关系.

- architecture model

  * 主要是 server-agent, 同时支持 agent-less 和 agent-only.

  * 连接从 minion 发起, minion 上不需要允许 incoming connections.

  * publish-subscribe model.

    - publisher port 4505, minion 连接 master 上的 4505 端口, 监听任务信息.
      任务异步地从该端口发送至所有 minions.

    - request server port 4506, minion 按需连接该端口以获取各种所需文件和数据,
      以及发送执行结果回 master. 这些数据的传输是同步的.

- authentication & secure communication

  * minion 向 master 连接时, 首先送上自己的公钥. master 接受 minion 后, 返回
    自己的公钥和 AES key. 后者用 minion 的公钥加密, 从而只有 master 和这个
    minion 知道 AES key 的内容.

  * master 和 minion 的通信通过 TLS 进行, 使用 AES key 对称加密.

- user access control

- remote execution

  * 所有的 minion 都会收到要执行的命令, 但根据 target pattern 去判断自己要不要执行
    这个命令.

  * minion 收到每个命令都会开一个 worker thread 去执行. 因此可以同时执行多个命令.

- state system

  * State modules contain logic to see if the system is already in the correct
    state. In fact, after this determination is made, the State module often
    simply calls the remote execution module to do the work.

- salt runner

- module types

  每个 subsystem 都有自己的一套 modules, 对于有些子系统比如 execution subsystem,
  每个 module 是扩展系统功能或者性能的; 对于另一些比如 returner subsystem,
  每个 module 是提供了相同功能的不同实现.

- python modules

  * function signature doc 并不一定包含了所有参数, 因为可能将额外参数传递至
    其他函数.

  * 注意到 salt yaml 配置中使用 list 里嵌 single-keyed map 的原因就是为了同时支持
    python 的 postional args 和 kwargs 两种参数形式.

Configuration
-------------

minion
~~~~~~

- Primary configurations

  * ``minion_id_caching``, 将 minion id 缓存在 ``minion_id`` file 中. 这是为了当
    minion 配置文件中没有定义 ``id`` 时, resolved minion id 值不随 hostname 的
    改变而改变, 避免 master 不认识这个 minion.

  * ``id``, 指定 minion id. minion id 的 resolution order:

    - ``id`` 值 override 所有其他.

    - ``socket.getfqdn()``

    - ``/etc/hostname``

    - ``/etc/hosts`` 中 127.0.0.0/8 子网下的任何域名.

    - publicly-routable ip address

    - privately-routable ip address

    - localhost
