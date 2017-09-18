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

Execution
---------

- Execution functions.

  * ``state.apply``

    - ``test`` 参数, 进行 dry-run, 需要进行的状态改变会标黄, 不需要改变的状态
      维持绿色.

State
-----

- Formula.

- State.

- State file.

  A file with an SLS extension that contains one or more state declarations.

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

- Salt YAML requirements.

  * 每层缩进必须是 2 spaces.

- Execution order.

  * top to bottom.
