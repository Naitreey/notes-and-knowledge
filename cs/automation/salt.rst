- ``salt <target> <module>.<function> [args]...``

- 使用 ``sys.doc`` module 获取 module/function doc.

- target selection (``man salt(1)``).

  * minion id.

  * shell globbing.

  * PCRE regex.

  * Grain system with glob.

  * Grain system with PCRE.

  * target list.

  * all above combined.

- Grains.

  * The static information SaltStack collects about the underlying managed system.

  * Add custom ``role`` grain to minion configuration file to categorize minions
    by functionality.

- Execution functions vs State functions

  Salt state functions are designed to make only the changes necessary to apply
  a configuration, and to not make changes otherwise. Salt execution functions
  run each time they are called, which may or may not result in system changes.

- 在 jinja2 模板中可访问的参数:

  * minion configuration values

  * grains

  * salt pillar data

  * salt execution modules

- salt file server

  * builtin file server (``file_roots``)

  * git file server, 可以使用这个直接从 git server 中取文件.

Execution
---------

- Execution functions.

  * ``state.apply``

    - parameters

      * ``test`` 进行 dry-run, 需要进行的状态改变会标黄, 不需要改变的状态
        维持绿色.

      * ``pillar`` 指定额外的 pillar data, 它覆盖 pillar file 中的同名参数.

  * ``state.show_sls``

  * ``pillar.items``

  * ``event.send``

State
-----

- Formula.

- State.

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

- Top file.

  The Top file is used to apply multiple state files to your Salt minions
  during a highstate. Targets are used within the Top file to define which
  states are applied to each Salt minion.

  Top file 中的 target pattern, 是对其下的状态的应用对象进行限制.

- Highstate.

  A highstate causes all targeted minions to download the /srv/salt/top.sls
  file and find any matching targets. If a matching target is found, the minion
  applies all of the states listed under that target.

  ``state.apply`` with no arguments starts a highstate.

- Pillar file.

  * Pillar 实际上是一系列分配给各 minion 的数据或参数. 它根据 target selection
    机制 对数据进行分配. 将 salt state 模板化, 对各个 minion 传入自定义的
    pillar data, 从而达到 salt state reuse 的目的.

  * 与 state file 不同, pillar data 不是对所有 minion 共享的, 只有 matched target
    minion 才会收到分配给他的 pillar data. 所以可以用这个来存储 secure data.

  * 查看 pillar data: ``pillar.items`` execution module.

- Salt YAML requirements.

  * 每层缩进必须是 2 spaces.

  * quick vim config: ``# vim:ft=yaml:expandtab:tabstop=2:shiftwidth=2:softtabstop=2``.

  * 使用 ``vim-salt`` plugin.

- Execution order.

  * By default, each ID in a Salt state file is executed in the order it
    appears in the file. Additionally, in the Top file, each Salt state file is
    applied in the order listed.

  * ``state.show_sls`` execution module 查看某个 state file 中状态执行顺序.

- Requisites

  * 用于在 states 之间建立联系. 这可以包含修改默认的 states execution order 或者
    conditional state apply. 例如某文件修改时, 重启某服务.

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
          [- expr_form: <type>]
          - arg: <arg_list>

Runner
------

- Runners are modules that execute on the Salt master to perform supporting tasks.

- runner modules

  * ``state.event``

Configuration
-------------

- 不同方面的配置项应放在 ``master.d`` 或 ``minion.d`` 中的单独文件中.
  而不该直接修改 ``master`` ``minion`` 配置文件.
