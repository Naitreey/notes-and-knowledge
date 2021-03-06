Questions
=========

- 使用 salt 管理 salt-master.

  两种方法:

  * 在 salt-master 节点上安装 salt-minion, 配置 master 节点为自身即可.

  * 使用 ``salt-call`` 本地执行 execution modules, 无需 minion.

Installation
============

upgrade
-------
- the master(s) should always be upgraded first.

Salt Jinja extension
====================

- 在 jinja2 模板中可访问的 salt 参数:

  * ``salt``, a python dictionary containing all of the functions available to
    the running salt minion.

  * ``opts``, a dict containing minion configurations.

  * ``grains``, a dict containing minion grains data.

  * ``pillar`` a dict containing salt pillar data.

  * ``saltenv``

  * ``sls``, the value used to include the sls in top files or via the include
    option.

  * ``slspath``, 什么鸡巴玩意儿.

- salt file server

  * builtin file server (``file_roots``)

  * git file server, 可以使用这个直接从 git server 中取文件.

Target matchers
===============

minion id glob matcher
----------------------
- minion id can be a shell glob pattern.

minion id PCRE matcher
----------------------
- minion id can be a PCRE pattern.
  
- When using regular expressions in a top file, you must specify the matcher
  as the first element of the SLS file list::

    base:
      'web1-(prod|devel)':
        - match: pcre
        - ...

minion list matcher
-------------------
- minion id can be a list of minion ids.

grains glob matcher
-------------------
format::

  [key[:key]...]:value

- Nested key (as above) is supported.

- value can contain glob pattern.

grains PCRE matcher
-------------------
ditto

- value can contain PCRE pattern.

pillar glob matcher
-------------------
format::

  [key[:key]...]:value

- Nested key (as above) is supported.

- value can contain glob pattern.

pillar PCRE matcher
-------------------
ditto

- value can contain PCRE pattern.

ipcidr matcher
--------------
format::

  x.x.x.x
  x.x.x.x/xx

- To use in top file, specify the ``ipcidr`` matcher::

    base:
      '127.0.0.0/8':
        - match: ipcidr
        - ...

nodegroup matcher
-----------------
- node groups are defined in master config file, under ``nodegroups`` key::

    nodegroups:
      group1: <pattern>
      group2: <pattern>

  The master must be restarted for those changes to be fully recognized.

- A node group pattern can be
  
  * a complete string of compound matcher. Then tokenization is performed by
    splitting on whitespace.

  * a list of strings that makes up a compound matcher. Tokenization is
    performed by treating each element of the list as a whole.

- A node group can reference another node group in its matcher.

- To use in top file, specify ``nodegroup`` matcher.

compound matcher
----------------
- All matchers above is supported.

- By default use minion id glob matcher

- All other matchers must be prefixed with proper letter ``X@``

  * minion id PCRE: ``E@``

  * minion id list: ``L@``

  * grains glob: ``G@``

  * grains PCRE: ``P@``

  * pillar glob: ``I@``

  * pillar PCRE: ``J@``

  * IP, CIDR: ``S@``

  * nodegroup: ``N@`` (only in master's nodegroups definition)

- Boolean operator: and, or, not

- precedence overriding: ``( ... )``. spaces are required between the
  parentheses and matchers.

Grains
======

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
  modules and ``__virtualname__``).

- ``grains.ls``, ``grains.items`` execution module 获取 grains 列表和 grains 数据.

- ``grains.get`` execution module 获取某项 grain 值.

- ``saltutil.refresh_modules`` execution module 更新 modules 和 grain data.

- ``saltutil.sync_grains`` 同步 custom grains modules 至各个 minion.

Execution
=========
- Remote execution is performed by ``salt`` command. See it for detailed
  formats.

- Execution functions vs State functions.

  Salt state functions are designed to make only the changes necessary to apply
  a configuration, and to not make changes otherwise. Salt execution functions
  run each time they are called, which may or may not result in system changes.

module structure
----------------
- A salt module is a python/cython module that contains functions called by
  salt command.

module name
^^^^^^^^^^^
- Module name is defined by one of the following:

  * defined by ``__virtual__`` function and ``__virtualname__``.

  * Otherwise, its filename.

module loading
^^^^^^^^^^^^^^
* cython module. must be named ``<modulename>.pyx``. The compilation of the
  Cython module is automatic and happens when the minion starts.

* zip module can be imported, as usual.

* If a Salt module has errors and cannot be imported, the Salt minion will
  continue to load without issue and the module with errors will simply be
  omitted.

function
^^^^^^^^
- Rules for objects loading as execution functions:
 
  * "public" python callables are loaded.

  * Private functions (whose name starts with ``_``) are  not exposed as
    execution functions.

- Function cross calling. via ``__salt__`` global variable::

    __salt__['mod.func']

- Function aliases.

  * Use ``__func_alias__`` to define function aliases.
  
  * This is to prevent defining a function that will directly shadow a python
    built-in. Instead, we define the function using an alternative name, but
    make an alias to the desired name.

special module attributes
^^^^^^^^^^^^^^^^^^^^^^^^^
- ``__salt__``.

  * a dict, where keys are all of the Salt execution functions in the form:
    ``mod.func``, and the values are the function object.

  * available in the modules after they are loaded into the Salt minion.

- ``__grains__``.

  * A dict containing all grains data of a minion.

- ``__opts__``.

  * A dict containing complete minion configuration.

- ``__salt_system_encoding__``.

  * A string representing the character encoding used by a salt system.

- ``__outputter__``

  * A dict mapping the functions defined in a module to their default outputter
    names.

  * This allows for a specific outputter to be set on a function-by-function
    basis.

- ``__virtualname__``.

  * A string used by the documentation build system to know the virtual name of
    a module without calling the ``__virtual__`` function.

- ``__func_alias__``.

  * a dictionary where each key is the name of a function in the module, and
    each value is a string representing the alias for that function.

  * When calling an aliased function from a different execution module, state
    module, or from the cli, the alias name should be used.

special module functions
^^^^^^^^^^^^^^^^^^^^^^^^
- ``__virtual__()``.

  * called before execution modules is loaded. So ``__salt__`` is unreliable
    (but other special names should be fine).

  * Returns:
    
    - string. the module is loaded using the name of the string as the virtual
      name. Modules which return a string that is already used by a module that
      ships with Salt will *override* the stock module.

    - True. the module is loaded using the current module name, as defined by
      ``__virtualname__`` or default file name.
     
    - False. the module is not loaded, probably because deps are not met.

    - A tuple of ``(False, error string)`` . The string contains the reason
      why a module could not be loaded.

- ``__init__(opts)``. Perform module initialization.

  * minion configuration is passed as ``opts``.

  * This is useful when a module needs to act differently based on minion
    configs.

virtual module
^^^^^^^^^^^^^^
- A virtual module is an abstract module that corresponds to different concrete
  modules based on specific environment or platform.

- 在不同的环境下, 加载了不同的 module, 但 expose 为相同的 virtual module name.
  从而在用户角度, 体验是统一的.

- A vritual module is defined by a ``__virtual__`` function and a
  ``__virtualname__`` global name. To avoid setting the virtual name string
  twice, you can implement ``__virtual__`` to return the value set for
  ``__virtualname__``.

- A virtual module's concrete module (provider) can be overridden
  unconditionally via ``providers`` config key in minion config file or SLS
  state file.

configuration
^^^^^^^^^^^^^
- module can access minion configs directly. So their configs are written in
  minion yaml configs.

- config key naming convention::

    <module>.<key>

- Any valid YAML is allowed as config value.

- testing configuration. Configuration can be tested using modules.test module.

string handling
^^^^^^^^^^^^^^^
- strings fed to the module have already decoded from bytes into Unicode.

- Cross calling should use Unicode for text strings, and bytes for binary data.

logging
^^^^^^^
- Use standard python logging procedure.

- logging should not be done anywhere in a Salt module before it is loaded.
  This includes all code that would run before the ``__virtual__()`` function,
  as well as the code within the ``__virtual__()`` function itself.

documentation
^^^^^^^^^^^^^
- A function's docstring is printed as its documentation by sys.doc.

- The module itself should also contain a docstring.

metadata
^^^^^^^^
- Added to the module-level docstring.

- format::

    :maintainer:    Author <email@em.cm>
    :maturity:      new
    :depends:       package,package
    :platform:      all

  The maintainer field is a comma-delimited list of developers who help
  maintain this module.
  
  The maturity field indicates the level of quality and testing for this
  module. Standard labels will be determined.
  
  The depends field is a comma-delimited list of modules that this module
  depends on.
  
  The platform field is a comma-delimited list of platforms that this module is
  known to run on.

utilities
^^^^^^^^^
- salt.utils.decorators.depends. A decorator will check the module when it is
  loaded and check that the dependencies passed in are in the globals of the
  module or the check command run successfully. If not, it will cause the
  function to be unloaded (or replaced).

modules
-------
service
^^^^^^^
a virtual module that is fulfilled by a concrete module depending on environment.

- service.available

- service.restart

file
^^^^

- file.write

- file.rename

- file.remove
if path is directory, it will be recursively deleted.

- file.stats

- file.read

- ``file.set_mode``. set file mode. returns new mode as text string.
  args.

  * path. local file path.

  * mode. in octal format.

- ``file.get_mode``. get file mode. returns mode as text string.
  args.

  * path. local file path.

  kwargs.

  * ``follow_symlinks=True``

cmd
^^^
- ``cmd.run_all``. execute the passed command.

  Returns: a dict containing pid, retcode, stdout, stderr.

  args:

  * cmd. the command to run.

  kwargs:

  * cwd. command's cwd. Defaults to the home directory of the user specified by
    ``runas``.

  * stdin. string passed as stdin.

  * runas. effective user running the command. default is salt's effective
    user.

  * password.

  * shell. shell path. default to default shell.

  * ``python_shell``. when False, cmd is splitted by shlex, otherwise cmd is
    passed directly to shell. Default to python_shell=True when run directly
    from remote execution system.

  * env. a dict to merge into salt process's env.

  * ``clean_env``. whether to remove any existing env.

  * ``prepend_path``. prepend multiple path segments.

  * template. render cmd and cwd strings through template engine.

  * rstrip. strip all whitespace off the end of output before it is returned.

  * umask. set this umask before running cmd.

  * ``output_encoding``. which encoding should be used to decode output.

  * ``output_loglevel``. when output is logged to minion log. default is debug.

  * ``ignore_retcode``. Pass this argument as True to skip logging the output
    if the command has a nonzero exit code.

  * ``hide_output``. If True, suppress stdout and stderr in the return data.

  * timeout. A timeout in seconds for the executed process to return.

  * use_vt.

  * encoded_cmd.

  * redirect_stderr. If set to True, then stderr will be redirected to stdout.

  * bg. If True, run command in background and do not await or deliver its
    results.

archive
^^^^^^^

minion
^^^^^^
- minion.list

test
^^^^

- ``test.ping``

- ``test.arg``

- ``test.arg_repr``

state
^^^^^

- ``state.apply``

  * parameters

    * ``test`` 进行 dry-run, 需要进行的状态改变会标黄, 不需要改变的状态
      维持绿色.

    * ``pillar`` 指定额外的 pillar data, 它覆盖 pillar file 中的同名参数.

- ``state.show_sls``

pillar
^^^^^^
- ``pillar.items``

- ``pillar.get``

- ``pillar.raw``

event
^^^^^
- ``event.send``

sys
^^^
- ``sys.doc`` 获取 module/function doc.

grains
^^^^^^
- ``grains.ls``

- ``grains.items``

- ``grains.get``

cp
^^
The cp module is the home of minion side file server operations. The cp
module is used by the Salt state system, salt-cp, and can be used to
distribute files presented by the Salt file server.

cp module is based on ``salt.fileclient`` module.

caching
""""""""
- ``cp.cache_dir``

- ``cp.cache_file``. cache a single file to the minion. 如果源文件没有修改, 就
  不会再次传输 (这是通过检查 salt-master 上源文件 hash 保证的). 对于 http,
  https, ftp 等 remote url, 由于无法直接验证 hash, 可提供 ``source_hash`` 来进
  行验证.
  
  Returns location of the cached file on minion. If salt url path does not
  exist, returns False.

  args:

  * path. the file is saved as ``$cachedir/files/$saltenv/$path``. 注意最后一部
    分 ``$path`` 包含源文件路径的各个中间目录. 即会创建不存在的中间目录.  支持
    salt url, http, https, ftp, etc. 等协议类型.

  kwargs:

  * saltenv. 指定 saltenv, 可通过 salt url 指定. default ``base``.

  * ``source_hash``. 指定 remote url's hash, 避免重新下载.

download
""""""""
- ``cp.get_file``. kwargs:

  * ``template``. render source and destination string.

  * ``gzip=N``. enable gzip compression on file transfer.

  * ``makedirs=True|False``. make intermediate directories leading to
    destination file.

- ``cp.get_dir``. kwargs:

  * ``template``. ditto

  * ``gzip`` ditto.

saltutil
^^^^^^^^
- used to manage the state of the salt minion.

synchronization
""""""""""""""""
- ``saltutil.refresh_modules``

- ``saltutil.refresh_pillar``

- ``saltutil.sync_grains``

- ``saltutil.sync_all`` 同步各种 custom modules 至 minion. Sync down all of the
  dynamic modules from the file server for a specific environment ``saltenv``.

  kwargs:

  * ``saltenv``. 要同步的环境. default base.

  * ``refresh``. refresh the execution modules and recompile pillar data
    available to the minion. default True.

  * ``extmod_whitelist``.

  * ``extmod_blacklist``.

  Returns the modules that are actually synced. 没有修改的 modules 不会显示在
  输出中.

job state
""""""""""
- ``saltutil.running``

- ``saltutil.find_cached_job``

- ``saltutil.find_job``

- ``saltutil.is_running``

- ``saltutil.kill_all_jobs``

- ``saltutil.kill_job``

- ``saltutil.signal_job``

- ``saltutil.term_all_jobs``

- ``saltutil.term_job``

cache
""""""
- ``saltutil.clear_cache``

- ``saltutil.clear_job_cache``


schedule
^^^^^^^^
- ``schedule.add(name, **kwargs)`` 支持 `scheduled jobs` 部分的全部
  specification 参数.

- ``schedule.modify(name, **kwargs)``. 修改时要指定全部所需参数, salt 会 diff
  前后差别, 进行所需修改. 对于一个 host, 只有现有 schedule 的时候才能 modify 成
  功.

- ``schedule.delete(name)``.

- ``schedule.copy``

- ``schedule.move``

- ``schedule.disable``, disable all jobs on target hosts.

- ``schedule.disable_job(name)``. disable one job.

- ``schedule.enable``. enable all jobs on target hosts.

- ``schedule.enable_job(name)``. enable one job.

- ``schedule.reload``

- ``schedule.save``

- ``schedule.purge``

- ``schedule.is_enabled``. show a scheduled job if enabled.

- ``schedule.list``. show scheduled jobs.

- ``schedule.show_next_fire_time``

- ``schedule.run_job``

- ``schedule.postpone_job``

- ``schedule.skip_job``

- ``schedule.build_schedule_item`` mainly used internally, to build schedule
  config.

ret
^^^
useful to use or test returner directly.

- ``get_fun(returner, fun)``. similar to the samely named function

- ``get_jid(returner, jid)``.

- ``get_jids(returner)``

- ``get_minions(returner)``

timezone
^^^^^^^^
- ``timezone.get_zone()``. get timezone. format: ``region/city``, by inspecting
  system timezone configuration files.

- ``timezone.get_zonecode()``. get timezone as code. e.g., CST, PMT, etc.

- ``timezone.get_offset()``. get offset. format: ``{+|-}HHMM``

State
=====

- State.

  A declarative or imperative representation of a system configuration.

- salt state tree.

  * A directory tree of state files located at ``file_roots``.

  * any other files and folders you place in ``file_roots`` are available
    to your Salt minions.

  * 在 salt states 中, 使用 ``salt://<path>`` 来引用 ``file_roots`` 下的文件,
    其中 ``<path>`` 是相对于 ``file_roots`` 的路径.

  * 整个 state tree 是在不同 minion 之间共享的. 各个 minion 获取到这些文件后
    在本地编译模板生成最终版本的 state tree. 这与 pillar data 是不同的.

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

  top file 中 pattern 下面的列表, 可以是包含的单个 state file, 也可以是整个
  目录. 后者情况时, 目录中所有 sls 文件都被包含.

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

  * ``state.show_highstate`` execution module 查看对于某个 minion 的整体
    highstate 时各任务执行顺序.

- Requisites

  * 用于在 states 之间建立联系. 这可以包含修改默认的 states execution order 或者
    conditional state apply. 例如某文件修改时, 重启某服务.

  * ``require``, 要求 required state 必须成功, 本状态才执行.

  * ``watch``, add additional behavior when there are changes, but otherwise
    the state executes normally. 具体来讲, 如果 watched state 失败, watching
    state 不会执行; 如果 watched state 成功但没有修改, watching state 执行,
    但无 additional behavior; 如果 watched state 成功且有修改, watching state
    执行, 然后 additional behavior 也执行.

    additional behavior 由 ``<module>.mod_watch`` function 定义. 该函数的
    参数在 watching state function 的参数列表中指定 (它会把自己不需要的参数
    传入 mod_watch).

    A good example of using watch is with a ``service.running`` state.

  * ``onchanges``, makes a state only apply if the required states generate
    changes, and if the watched state's "result" is True. ``onchanges`` 用于
    在某个其他系统产生修改时执行 posthook.

File server
===========

overview
--------
- File server is used for distributing files to the Salt minions. The file
  server is a stateless ZeroMQ server that is built into the Salt master.

- the Salt file server can be used for any general file transfer from the
  master to the minions.

- The Salt file server is environment-aware. This means that files can be
  allocated within many root directories and accessed by specifying both the
  file path and the environment to search. 

- Files are manipulated via salt.modules.cp.

backends
--------
- specify file server backend via ``fileserver_backend`` master option.

- available backends: azure, git, hg, minion, roots, s3, svn.

environments
------------
- 每个 backend 都定义了 environment 至 file namespace 的映射关系.

- ``base`` environment is mandatory. This environment MUST be defined and is
  used to download files when no environment is specified.

- querying files.
  
  * ``salt://path/to/file?saltenv=<env>`` refers to files in salt file server.

  * escaping ``?``: ``salt://|dir/file?name``

  * Non-ascii 字符及空格等非 url metachar 的特殊字符可以直接写入 salt url,
    使用与 filepath 相同的形式, 无需 escape.

- specifying environment

  * globally: A minion can be pinned to an environment using the
    ``environment`` option in the minion config file.

  * set for a single state operation: ``saltenv`` parameter.

  * per-state SLS definition: ``saltenv`` key. (If the SLS file containing a
    state was in the environment, then it would look in that environment by
    default.)

minion-side file server
-----------------------
This is primarily to enable running Salt states without a Salt master. To use
the local file server interface, copy the file server data to the minion and
set the file_roots option on the minion to point to the directories copied from
the master. Once the minion file_roots option has been set, change the
file_client option to local to make sure that the local file server interface
is used.

Custom module distribution
--------------------------
Under any environment, the following directories can exist inside file root,
which saves custom modules of various kinds:

* _beacons

* _clouds

* _engines

* _grains

* _modules

* _output

* _proxy

* _renderers

* _returners

* _states

* _tops

* _utils

Custom modules can be synced via:

- implicitly: When states are run, they are automatically synced.

- explicitly: use saltutil execution module to sync explicitly.

synced custom modules are available globally, without environment restrictions.

Any custom modules which have been synced to a minion that are named the same
as one of Salt's default set of modules will take the place of the default
module with the same name.

注意, 对于 master's extension modules, 要通过 ``salt-run saltutil.sync_*`` 来同
步 (同步至 ``extension_modules`` 配置路径). ``salt salutil.sync_*`` 只能同步至
minion.

roots
^^^^^
- environment 定义.

  * 每个 environment 下定义 a list of file directory roots.

  * 当在某个环境中定位文件时, 是根据 directory roots 的定义顺序遍历查找. 取第一
    个找到的文件.

Pillar
======

- Pillar 实际上是一系列分配给各 minion 的数据或参数. 它根据 target selection 机
  制对数据进行分配. 将 salt state 模板化, 对各个 minion 传入自定义的 pillar
  data, 从而达到 salt state reuse 的目的.

- 与 state file 不同, pillar data 不是对所有 minion 共享的, 只有 matched target
  minion 才会收到分配给他的 pillar data. 所以可以用这个来存储 secure data.

- Pillar data is compiled on the master and is never written to disk on the
  minion.  In-memory pillar data 是在 minion 启动时生成的.

- Running states 以及 ``pillar.items`` 时, minion 会从 master 获取最新的 pillar
  data.  但不会更新 in-memory pillar data. 若要更新, 需要执行
  ``saltutil.refresh_pillar``.

- pillar data 位于 ``pillar_roots``, 其中文件结构与 ``file_roots`` 相同.
  pillar_roots 必须在 file_roots 之外, 不能是后者的子目录, 为了保密.

- pillar data merging:
  
  * Pillar files are applied in the order they are listed in the top file.

  * 对于不同 pillar sls file 中的同名 key, 其值若是 dict, 则 recursively
    merged; 否则后执行的值覆盖先前执行的值.

- pillar file 可以相互 ``include``.

- 查看 pillar data: ``pillar.items`` execution module. 从 master 获取最新的
  pillar data.

- 查看当前的 pillar data: ``pillar.raw`` execution module. 不会从 master 获取最新
  pillar data.

- 获取某个 pillar data: ``pillar.get`` execution module.

- 更新 in-memory pillar data: ``saltutil.refresh_pillar`` execution module.

- 程序中使用 ``__pillar__`` 访问 in-memory pillar data.

- 为了保密, pillar yaml file 可以放在一个 private git repo 中.

Salt Mine
=========

- The Salt mine is used to share data values among Salt minions.

- 当某个数据是动态变化的, 可以由 master 或某个 minion 生成后放在 salt mine
  里进行共享.
  This is a better approach than storing it in a Salt state or in Salt pillar
  where it needs to be manually updated.

Event
=====
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

event returners
---------------
- all events seen by a salt master may be logged to one or more returners.

- To enable event logging, set the ``event_return`` master config.

- Not all returners support event returns. Verify a returner has an
  ``event_return()`` function before using.

Beacon
======

- 用于监控 salt 之外的系统状态, 当预设的状态、条件等满足时, 向 bus 发送
  该事件. 它应用 event system 实现.

- beacon 和 event 的唯一区别是, event 系统负责生成 salt 自己运行过程中发生
  的事件; beacon 基于 event 机制, 负责系统内发生的任何的自定义事件, 它是
  event 的扩展.

- 在 minion config 中的 ``beacons`` 部分或者单独的 ``beacons.conf`` 文件中配置.

Reactor
=======

- Reactor trigger reactions when events occur on event bus.

- 配置: master config 中的 ``reactor`` section. 只允许一个 reactor section.

- reactor sls file

  * 跟 state file 一样支持 jinja2. 它的 jinja context:

    - grains & pillar 不存在.

    - salt object.

    - tag -- tag of triggering event.

    - data -- event's data.

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
======
- Runners are modules that execute on the Salt master to perform supporting
  tasks. 这些操作可能是关于 master 自己的, 或者是整个 salt 系统的管理性质的操
  作, 总之不是直接去对 minion 进行操作.

- Runner modules can be executed by ``salt-run`` command.

mechanism
---------
- Any output from a runner function will be sent as an event to event bus.

- Runners can be run synchronously or asynchronously.

  * Sync mode, i.e., blocking mode, control will not be returned until the
    runner has finished executing. And output is printed directly to cli.

  * Async mode, control will be returned immediately. If results are desired,
    they must be gathered either by firing events on the bus from the runner
    and then watching for them or by some other means.

modules
-------
state
^^^^^
* ``state.event``

jobs
^^^^
inspect active jobs and ran jobs.

- ``jobs.active``. runs saltutil.running on all minions and formats the return
  data about all running jobs in a job-oriented way.

- ``jobs.exit_success``

- ``jobs.last_run``. show last-run job.

- ``jobs.list_job``. show detail of one job.

- ``jobs.print_job``. 似乎基本同上.

- ``jobs.lookup_jid``. show job output.

- ``jobs.list_jobs``.

- ``jobs.list_jobs_filter``

Orchestrate Runner
==================

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
=====

Job
===

job id
------
- just fucking current time, 精确到 microsecond.

- 若设置了 ``unique_jid``, append current pid.

- 其实无法保证唯一性.

job management
--------------
- proc system. Under ``$cachedir/proc``, 保存着当前正在执行的任务的信息.  对于
  每个任务, 有一个文件与之对应, 以 job id 命名.

- Manage running jobs at each minion, via ``saltutil`` execution module.

- Inspect historical or currently active jobs via ``jobs`` runner module.

job cache
---------

querying job cache
^^^^^^^^^^^^^^^^^^
- Job cache can be queried by ``salt.runners.jobs`` runner module.

- 这个模块会按顺序选择 ``ext_job_cache``, ``master_job_cache`` 中的一个
  returner 来查询 job cache.

default job cache
^^^^^^^^^^^^^^^^^
- Default job cache 等价于 ``master_job_cache: local_cache``.

- This cache is maintained by master, it caches results of job execution by
  minions.

- 路径: local storage on the Salt Master, ``$cachedir/jobs``

- 缓存时间: 既然说是一个缓存, 就不会持久保存. ``keep_jobs`` master config
  option 控制任务结果的缓存时间. 默认 24h.

- 优化:

  * 提高 cache 读写效率: job cache 路径使用更快 IO 的存储设备, 或 tmpfs.

  * 完全不保存 job result. ``job_cache`` option.

external job cache
^^^^^^^^^^^^^^^^^^
- Mechanism:
  
  * Job execution result is returned to external job cache, in addition to
    return to ``master_job_cache``.

  * 这个额外的操作, 是由 minion 执行 minion-side returner module 来实现的.

- 注意设置 external job cache 后, 任务结果会在 ``master_job_cache`` 和
  ``ext_job_cache`` 中都写入.

- 优点:

  * Data is stored without placing additional load on the Salt Master.

- 缺点:

  * A large number of concurrent connections to external cache system.

- configuration.

  * Configure the relevant returner. The precedence of reading config:

    - minion config file

    - minion grains

    - minion pillar data

  * enable the returner as external job cache, by configuring ``ext_job_cache``
    at *master* configuration. (在 master 是因为 runner modules 也要知道到哪里
    去找 job cache.)

master job cache
^^^^^^^^^^^^^^^^
- Mechanism:
  
  * Salt Minions send data to the Default Job Cache as usual, and then the Salt
    Master sends the data to the external system.
   
  * 这个额外的操作, 是由 master 执行 master-side returner module 来实现的.

- 注意设置 master job cache 后, 任务结果会在 ``master_job_cache`` 中写入, 不再
  写入 default job cache (因由同一个配置负责).

- 优点:

  * A single connection is required to the external system.

- 缺点:

  * Places additional load on your Salt Master.

- configuration.

  * Configure the relevant returner in master configuration file.

  * enable the returner as master job cache, by configuring
    ``master_job_cache`` at master configuration.

scheduled jobs
--------------
- 两种任务可以设置 schedule.

  * execution modules on minion

  * runner modules on master

- 设置 scheduled jobs 的 4 种方式:

  * ``schedule`` option in master or minion config. Restart master/minion to
    have effect.

  * ``schedule`` key in minion pillar data. Run saltutil.refresh_pillar to
    distribute schedule.

  * ensure scheduling by ``schedule`` state module.

  * apply scheduling by ``schedule`` execution module.

  除了直接修改 master/minion config file 之外, 其他所有方法创建的 scheduling
  都会转化为 config 项, 持久化在 ``$confg_dir/$include_dir/_schedule.conf``.

specification
^^^^^^^^^^^^^
一个 scheduled job 需要以下信息:

- job name: ``name``.

- 要执行的函数: ``function``. 对于 master scheduled job, 识别为 runner module
  function; 对于 minion scheduled job, 识别为 execution module function.

- 函数 positionals: ``args``. 为消歧义, 在命令行上名为 ``job_args``.

- 函数 kwargs: ``kwargs``. 为消歧义, 在命令行上名为 ``job_kwargs``.

- scheduling parameters:

  * ``days``, ``hours``, ``minutes``, ``seconds``. 可以结合使用. 即以此为周期执
    行.

  * ``when``. 指定执行时间. 可以是 time string 或 a list of time string. 对于
    每个时间, 可以是以下内容:

    - dateutil 日期和时间字符串. 无论格式如何, 只要解析出的时间在未来, 就会执行.
      这样就可以指定每天某时间执行, 周几执行, 每月某天执行, 等. 但格式的最小单
      位是一个固定时间的字符串. 要求安装 python-dateutil.

    - ``whens`` pillar/grains data 定义的日期时间字符串.

  * ``cron``. use crontab format. See croniter module for supported formats.
    尤其是这里支持秒级的 crontab. 要求安装 croniter.

  * ``once``. 在指定日期时间执行一次. 执行完却仍然是 enable 状态. 需手动删除.

  * ``once_fmt``. 默认 ISO 8601. 可使用 strftime(3) 格式.

  * ``run_on_start``. true/false. default false. 对于纯周期性任务, 在起点时是否
    执行一次任务. 这里起点是指任务新增、修改等操作的时候. 该参数不适合与 cron
    类型任务一起使用.

  * ``splay``. 随机漂移范围, 单位是秒: [0, splay].

    - ``start``. 指定随机漂移起始值.

    - ``end``. ditto for 结束值.

  * ``range``. 在此时间范围内执行. dateutil 日期和时间字符串.

    - ``start``

    - ``end``

    - ``invert``. true/false. 指定在或不在此时间范围内执行.

  * ``maxrunning``. 任务的最大同时执行实例数. 默认 1.

  * ``return_job``. true/false. 是否返回任务结果至 master.

  * ``metadata``. a dict. 设置 metadata 用于任务的识别和筛选.

  * ``until``. run until the time, specified as dateutil date/time string.
    当任务执行完后, 并不会自动 disable, 仍然是 enable 状态. 目前没发现任何标识
    能说明任务已经不再执行. 可以与所有计划任务格式配合使用.

  * ``after``. run only after the time. 其他同上.

    - 对于纯周期性任务, after 时间点之后一个 delta 时间范围内会执行一次.

    - 对于 cron 类型任务, 若 after 时间点与 cron 触发时间匹配, 也不会执行. 这是
      因为存在一个 delta 滞后.

  * ``returner``. 指定该任务使用的 returner. 全局的 scheduled job's returner 由
    ``schedule_returner`` 配置项指定.

  * ``enabled``. 是否启用.

result data
^^^^^^^^^^^
以下部分内容格式见 ``returner()`` function 定义::

  {
      "tgt_type": "glob", # not sure
      "fun_args": ["positional1", ..., {"k1": "v", "k2": "v"}],
      "jid": "....",
      "return": <function's return data>,
      "retcode": 0,
      "success": True|False,
      "schedule": "scheduled-task-name",
      "tgt": "...", # not sure
      [ "cmd": "_return", ]
      "pid": N, # pid running schedule job
      "_stamp": "YYYY-mm-DDTHH:MM:SS.FFFFFF", # return time
      "arg": [...], # not sure
      "fun": "...",
      "id": "minion-id"
      "metadata": {
          "_TS": "Mon Jan  7 07:09:29 2019", # job start time
          "_TT": "2019 January 07 Mon 07 01", # not sure
          "_TOS": "+HHMM", # OS timezone offset
          ... # arbitrary metadata
      }
  }

Returner
========
- returner module 的用途.

  * minion-side, external job cache.

  * master-side, job cache.

  * minion-side, 在返回 job results to master-side job cache 之外, 任意的
    额外处理. (把 job result 交给 returner 去处理, 所以想干嘛就干嘛.)

- returner can be tested using salt.modules.ret.

module structure
----------------
module name
^^^^^^^^^^^
- same as execution module.

special module functions
^^^^^^^^^^^^^^^^^^^^^^^^
- ``returner(data)``. required. This is called during ``--return=MODULE``.
  作为 master job cache 时, 也会调用一次保存结果.

  * data. return data from the called minion function. Run the following
    command to get a sample of the data::

      salt-call --local --metadata --out=pprint <mod>.<fun>

    data format::

      {
          "fun": "...",
          "fun_args": ["positional1", ..., {"k1": "v", "k2": "v"}],
          "jid": "...",
          "return": <function's return data>,
          "retcode": N,
          "success": True|False,
          "cmd": "_return",
          "_stamp": 'YYYY-mm-DDTHH:MM:SS.FFFFFF',
          "id": "minion-id"
      }

master job cache support
""""""""""""""""""""""""
- ``prep_jid(nocache=False, passed_jid=None)``. Return the prepared jid.

  * ``nochache``. an optional boolean that indicates if return data should be
    cached.

  * ``passed_jid``. a caller provided jid which should be returned
    unconditionally.

- ``save_load(jid, load, minions=None)``. save job result. 在每个任务执行过程中,
  会调用两次, 一次 ``cmd: publish``, 一次 ``cmd: _return``.

  * jid. A id generated by ``prep_jid()``. should be considered unique.

  * load. job result returned to a Salt master by a minion. data format::

      {
          "fun": "...",
          "fun_args": ["positional1", ..., {"k1": "v", "k2": "v"}],
          "jid": "...",
          "return": <function's return data>,
          "retcode": N,
          "success": True|False,
          [ "cmd": "publish" | "_return", ]
          "_stamp": "YYYY-mm-DDTHH:MM:SS.FFFFFF", # return time
          "id": "minion-id"
      }

  * minions. a list of minions that the job was run against.

- ``get_load(jid)``. get load of jid, saved by ``save_load()``. If not found,
  return empty dict.

external job cache support
""""""""""""""""""""""""""
- all APIs required by master job cache support.

- ``get_jid(jid)``. Return the information returned when the specified job id
  was executed. Format is a dict, where keys are minion ids, and values are
  job results.

- ``get_jids()``. Return a dict mapping all job ids to job information.

- ``get_fun(funcname)``. Return a dictionary of minions that called a given
  Salt function as their last function call. Format: keys are minion ids, and
  values are function name.

- ``get_minions()``. Return a list of minions.

event support
"""""""""""""
- ``event_return(events)``.

configuration
^^^^^^^^^^^^^
- same way as execution module.


modules
-------

local_cache
^^^^^^^^^^^
- return data to local filesystem on master.

- they are saved under ``$cachedir/jobs``

functions
"""""""""
- all required APIs to support returner, master job cache, external job cache.

- ``clean_old_jobs()``. manual cleaning.

- ``get_endtime(jid)``. Retrieve the stored endtime for a given job.

- ``update_endtime(jid, time)``

- ``get_jids_filter(count, filter_find_job=True)``

- ``load_reg()``.

- ``save_reg(data)``

redis_return
^^^^^^^^^^^^
- return data to a redis server.

- virtual module name: ``redis``

- deps:

  * redis python client

- data storing.
 
  * data are saved to a hash key.

  * the key are set with a ttl according to ``keep_jobs`` config.

configuration
"""""""""""""
single host
~~~~~~~~~~~
One of host/port and unix socket must be specified.

- redis.db: default '0'

- redis.host: default 'salt'

- redis.port: default 6379

- redis.unix_socket_path: default /var/run/redis/redis.sock

cluster mode
~~~~~~~~~~~~
- redis.cluster_mode: default false. enable or not cluster mode.

- redis.cluster.skip_full_coverage_check: default false. skip checks that
  required advanced privileges.

- redis.cluster.startup_nodes: a list of cluster members, in format
  ``{"host": hostname, "port": num}``.

functions
"""""""""
- all required APIs to support returner, master job cache, external job cache.

- ``clean_old_jobs()``. manual cleaning.

Salt Cloud
==========

docker
------
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

Salt SSH
========

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
=========

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

  * command interface

  每个 subsystem 都可以通过不同的 plug-ins (subsystem modules) 来实现,
  满足相同的 API 即可.

- virtual module

  相同的 module name 在不同的 OS 等环境下实际上是对不同的 implementation module
  的重命名. 这类似于 ``os.path`` 与 ``posixpath``, ``ntpath`` 的关系.

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
=============

master
------
- 不同方面的配置项应放在 ``master.d`` 的单独文件中. 而不该直接修改 ``master``
  文件.

Primary configurations
^^^^^^^^^^^^^^^^^^^^^^
* ``interface``. default 0.0.0.0. bind ip.

* ``cachedir``, ``/var/cache/salt/master``. master cache data.

* ``publish_port``. default 4505. master publish server port.

job management configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ``job_cache``. default True. Set to False to disable job cache. But the
  ``$jid`` directory for each job is still created. The creation of the JID
  directories is necessary because Salt uses those directories to check for JID
  collisions.

* ``keep_jobs``. number of hours to keep old job information. set to 0 to
  keep forever.

* ``ext_job_cache``. default "". This is the default returner for all minions.

* ``master_job_cache``. default: ``local_cache``. for master job cache.

Scheduling configurations
^^^^^^^^^^^^^^^^^^^^^^^^^
* ``schedule``. scheduling configurations.

Master file server settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``fileserver_backend``. default ``["roots"]``. Multiple backends can be
  configured and will be searched for the requested file in the order in which
  they are defined here.

roots
"""""
- ``file_roots``. define the root directories of various environment.  Its
  value is a dict, where the key is environment key, and the value is a list of
  file root directories (Each environment can have multiple root directories.).

minion
------
- 不同方面的配置项应放在 ``minion.d`` 的单独文件中. 而不该直接修改 ``minion``
  文件.

Primary configurations
^^^^^^^^^^^^^^^^^^^^^^
* ``master``. Default ``salt``. can be

  - hostname or IP address of master node. 

  - A list of above for multi-master mode.

  - A valid value based on ``master_type``.

* ``master_type``. default ``str``. can be ``str``, ``failover``, ``func``,
  ``disable``.

* ``publish_port``. default 4505. master publish server port.

* ``master_port``. default 4506. master ret server port.

* ``minion_id_caching``, 将 minion id 缓存在 ``minion_id`` file 中. 这是为了当
  minion 配置文件中没有定义 ``id`` 时, resolved minion id 值不随 hostname 的
  改变而改变, 避免 master 不认识这个 minion.

* ``id``, 指定 minion id. minion id 的 resolution order:

  - ``id`` 配置值

  - ``socket.getfqdn()``

  - ``/etc/hostname``

  - ``/etc/hosts`` 中 127.0.0.0/8 子网下的任何域名.

  - publicly-routable ip address

  - privately-routable ip address

  - localhost

* ``cachedir``, ``/var/cache/salt/minion``. minion cache data.

Scheduling configurations
^^^^^^^^^^^^^^^^^^^^^^^^^
* ``schedule``. scheduling configurations.

* ``schedule_returner``. scheduled job's default returner. One or a list of
  returners.

Output
======

- CLI 中默认使用的 output module 是 highstate.

API
===

python
------

- python API 只有等到全面支持 python3 时才有用.

- 不同的 salt 部分通过不同的 client 来访问.

- ``salt.client.LocalClient``

  * 在 master 上使用, 用于向 minion 发送命令. 对应 ``salt`` command.

  * methods.

    - ``cmd()``, 执行 remote execution. ``tgt`` 可以是 list, 明确指定多个 minion.
      ``fun`` 可以是 list, 一次性执行多个操作, 同时 ``arg`` must be a list of lists
      of arguments.

    - ``cmd_async()``, 返回 job id, 不等待任务完成.

    - ``cmd_batch()``, 每次并行向一个 batch 的 minion 执行命令, 返回 a generator
      of returns.

    - ``cmd_iter()``, return a generator of minion returns.

    - ``cmd_iter_no_block()``, return a generator, which yields minion return data
      if available or None if not available. 不会 blocking 等待返回.

    - ``cmd_subset()``, execute a command on a random subset of the targeted systems.

    - ``get_cli_returns()``, ``get_event_iter_returns()``, 接收之前 async 执行的 job
      结果. 有啥区别不知道.

    - ``run_job()``, 什么玩意儿.

- ``salt.client.Caller``

  * 对应 ``salt-call``.

- ``salt.runner.RunnerClient``

  * 对应 ``salt-run``

- ``salt.wheel.WheelClient``

- ``salt.cloud.CloudClient``

  * 对应 ``salt-cloud``

- ``salt.client.ssh.client.SSHClient``

  * 对应 ``salt-ssh``

netapi
------
- 提供 REST API 方式访问 salt.

rest cherrypy
~~~~~~~~~~~~~

- installation. 安装 salt-api 时自动作为依赖安装了 cherrypy.

- SSL 配置.

  * generate self-signed certificate.

  * edit master config to create external auth user/group with proper
    permissions.

  * edit master config for ``rest_cherrypy`` module, with appropriate
    configurations.

  * restart salt-master.

- salt-api cherrypy server configurations. see salt doc.

- authentication.
  首先通过 ``/login`` endpoint 认证, 获得 session. session 通过一个
  session token 维持, session token 同时出现在 login response 的 json body
  和 response ``Set-Cookie`` header 中. 在后续的请求中, session token
  可以通过 ``Cookie`` header 传递或者手动添加一个 ``X-Auth-Token`` 来传递.

- request/response format.

  * request body 包含要执行的 salt 操作. 其抽象形式是 an array of commands. A
    command is mapping of the following fields:

    - ``client``. a client interface. main Python classes in Python API.

    - ``fun``. a function.

    - remaining parameters for the function.

    具体的 request body 可以是以上数据结构的 JSON, YAML, urlencoded 形式.
    只需设置相应的 Content-Type 即可.

  * response body 为操作结果. 抽象形式如下::

    {
        "return": [
            //command-1-result
            //command-2-result
            ...
        ]
    }

  * request/response 的实际形式可分别通过 ``Content-Type`` & ``Accept``
    headers 指定. 支持 JSON, YAML, urlencoded.

- url endpoints.

  * /. primary endpoint.

    - GET. return available clients.

    - POST. salt primary operations.

  * /login.

    - GET. basic message, boring.

    - POST. authenticate. return session token, permissions, etc.

  * /logout.

    - POST. logout, destroy session.

  * /minions[/<minion-id>].

    - GET. getting a list of minions and their grains, etc.

    - POST. Start an execution command and immediately return the job id.

  * /jobs[/<jid>].

    - GET. List jobs or show a single job from the job cache.

  * /run.

    - POST. Run commands bypassing the normal session handling Other than that
      this URL is identical to /.

      This endpoint accepts either a username, password, eauth trio, or a token
      kwarg and does not make use of sessions at all.

  * /events.
    
    - GET. access to Salt master event bus in http stream.

  * /hook.
    
    - POST. fire event on salt's event bus.

  * /keys[/<minion-id].

    - GET. List all keys or show a specific key.

    - POST. Generate a public and private key for minion and return both as a
      tarball.

  * /ws.

    - GET. Open a WebSocket connection to Salt's event bus.

  * /stats.

    - GET. statistics on cherrypy server.

pepper client module
~~~~~~~~~~~~~~~~~~~~
- use ``libpepper`` in python for remote salt access.

- use ``pepper`` CLI script to execute salt commands at remote command line
  as if the specified command was run locally.

Access Control
==============
access control system includes the peer system, the external auth system and
the publisher acl system.

general syntax
--------------
这三个系统的配置, 在 master config file 中, 在指定权限时, 具有相同的语法.
某个用户或实体的权限形式如下::

  - <function-pattern>
  ...
  - <target-pattern>:
      - <function-pattern>
      - <function-pattern>:
          args:
            - <arg1-pattern>
            ...
          kwargs:
            kw1: <kw1-pattern>
            ...
      ...

- 若 list element 是字符串则是 function pattern.
  此时, 对所有 minion 赋权限, 可以执行匹配的 functions.

- 若 list element 是 mapping, 则是对具体的某些 minion 赋权限. 其下
  是 a list of 可执行的 function patterns.

- function pattern 可以进一步限制允许的参数情况. If an kwarg isn't specified
  any value is allowed. To skip an positional arg use "everything" regexp ``.*``.

- all patterns can be specified by exact match, shell glob or regular
  expression.

- 对于允许在 master 上执行的 wheel, runner, jobs modules, 必须使用::
    - '@wheel'
    - '@runner'
    - '@jobs'
  globs does not work on this.

publisher acl system
--------------------
``publisher_acl`` is useful for allowing local system users to run Salt
commands without giving them root access.

publisher acl 还支持 whitelist/blacklist.

为了让 non-root user 可以确实执行命令, 访问所需的目录等, 需要修改 salt
各目录的 unix permissions::

  chmod 755 /var/cache/salt \
            /var/cache/salt/master \
            /var/cache/salt/master/jobs \
            /var/run/salt \
            /var/run/salt/master \
            /var/log/salt

configuration
~~~~~~~~~~~~~
``publisher_acl`` key in master config file.

其值是 a mapping from username patterns to permissions.
username patterns can be exact match, shell glob, regex, 与 unix username
匹配.

external authentication
-----------------------
``external_auth`` is useful for salt-api or for making your own scripts that
use Salt's Python API.

目前 eauth 支持 PAM 和 LDAP.

configuration
~~~~~~~~~~~~~
``external_auth`` key in master config file. 结构如下::

  <eauth-backend>:
    <user>|<group>%:
      <permissions>

usage
~~~~~
- CLI::

    salt -a <eauth> ...

  * generate a token to avoid re-auth each time::

      salt -T -a <eauth> ...

    Now a token will be created that has an expiration of 12 hours (by
    default). This token is stored in a file named salt_token in the active
    user's home directory.
    Once the token is created, it is sent with all subsequent communications.
    User authentication does not need to be entered again until the token
    expires.
Architecture
============
* management modes: agent-server (agent-based), agent-only, agent-less.

  不同的方式仅在 Salt 的使用方式上有区别 (例如 ``salt``, ``salt-call`` 等),
  salt 的所有 modules 可以在任何一种方式中使用.

agent-server mode
-----------------
职责
^^^^
The Salt master is responsible for sending commands to Salt minions, and then
aggregating and displaying the results of those commands.

连接模型
^^^^^^^^
- TCP 连接从 minion 向 master 发起. minion 上不需要开放端口允许 external
  initiating connections. Master 不会主动向 minion 发起 TCP 连接.

- master 与 minion 之间有两种通信:

  * publication communication. 即任务分发. 使用 publisher-subscriber model.
    minion 连接 master, 监听任务信息. default publisher port 4505.
   
    这个 TCP 连接是持续性的, 一旦建立只要两端都保持运行一般不会断开.  当 minion
    和 master 的连接经过 NAT 设备时, 虽然 NAT 对 idle connection 存在超时断开的
    机制, master 和 minion 之间的连接也会保持, 因为 zeromq 的 heartbeat 机制.

    publication communication 是异步的. 此时, master 是 producer -- 生产任务,
    minion 是 consumer -- 获取 (消费) 任务. master 不需要等待所有 minion 获取
    到了任务再去做别的, 是非阻塞式的.

  * direct communication. minion 按需连接 master 以获取各种所需文件和数据以及发
    送执行结果回 master. default request server port 4506.

    这个连接是短期的. 只有 minion 需要时才连接到 master 该端口.

    direct communication 是同步的. 此时, minion 连接到 master 后, 无论是 master
    发送数据还是 minion 返回结果, 都是阻塞式的.

节点认证和数据加密
^^^^^^^^^^^^^^^^^^
* publication communication.  minion 向 master 首次连接时, 发送自己的公钥.
  master 接受 minion 的连接后, 返回自己的公钥和 rotating AES key. 这些信息用
  minion 的公钥加密, 以保证只有 minion 可以解密.

  认证后, master 和 minion 的通信通过 TLS 进行, 使用 rotating AES key 对称加
  密.

* direct communication. Encrypted using a unique AES key for each session.

CLI
===

server
------

salt-master
^^^^^^^^^^^
Run master node.

run options
""""""""""""
- ``-d``. as a daemon. by default run in foreground.

logging options
"""""""""""""""
- ``-l LOGLEVEL``. console log level. all, garbage, trace, debug, info,
  warning, error, quiet.  default warning.

client
------

salt-key
^^^^^^^^
manage public keys in salt system.

key's states
""""""""""""
- unaccepted. key is waiting to be accepted.

- accepted. accepted.

- rejected. key is rejected by admin.

- denied. something wrong and minion is denied. Occurs
  
  * when minion has a duplicate ID
   
  * when a minion was rebuilt or had new keys generated and the previous key
    was not deleted from the Salt master

actions
"""""""

list
~~~~
- ``-l STATE``. list keys. STATE can be unaccepted, accepted, rejected, all.

accept
~~~~~~
- ``-a ID``. accept key. globs are supported.

- ``-A``. accept all pending keys.

reject
~~~~~~
- ``-r ID``. reject key. globs are supported.

- ``-R``. reject all.

delete
~~~~~~
- ``-d ID``. delete key. globs are supported.

- ``-D``. delete all.

print
~~~~~~
- ``-p ID``. print key.

- ``-P``. print all.

- ``-f KEY``. print fingerprint.

- ``-F``. print all fingerprints.

options
~~~~~~~
- ``--include-all``. include non-pending keys when accepting/rejecting.

key generation
""""""""""""""

salt
^^^^
::

  salt <target> [options]
    <module>.<function>[,<module>.<function>]...
    [args]...[ , [args]...]...

- ``args`` 部分的形式:
  
  * 函数的 positional args 以空格分隔

  * 函数的 kwargs 使用 ``key=value`` 形式指定, 并以空格分隔.
  
  * 对于 list 和 dict 类型参数值, 使用 Python repr 形式即可.

- The following target matchers are recognized. See `Target matchers`_ for
  explanation.

  * default is minion id glob matcher

  * ``-E ...``.

  * ``-L ...``

  * ``-G ...``

  * ``--grain-pcre ...``

  * ``-N ...``

  * ``-C ...``. compound matcher.

  * ``-I ...``

  * ``-S ...``

- compound command execution.

  * ``module.function`` 和 ``args`` 两个部分都可以是 a comma separated list.
    The functions are executed on the minion in the order they are defined on
    the command line, and then the data from all of the commands are returned
    in a dictionary.

  * ``args`` list 必须与 ``module.function`` 一一对应. 若某些函数不需要参数,
    也要留出 empty element.

  * ``args`` list 中, separator 最好左右以空格间隔, 作为单独一个参数传入命令,
    这样在参数内容本身包含 comma 时, 可消除歧义.

execution options
"""""""""""""""""
- ``--async``. do not block in RPC mode, print the id of started job.

- ``-b BATCH``. simultaneously execute on at most the BATCH number or
  percentage of minions.

  The batch system maintains a window of running minions, so, if there are a
  total of 150 minions targeted and the batch size is 10, then the command is
  sent to 10 minions, when one minion returns then the command is sent to one
  additional minion, so that the job is constantly running on 10 minions.

- ``--subset=NUM``. Execute the routine on a random subset of the targeted
  minions.

- ``-d``. return doc for the execution function, rather than execute the
  function.

- ``--args-separator=SEPARATOR``. Set list separator for the list of args
  in compound command execution, instead of default comma.

output options
""""""""""""""
- ``--out=OUTPUTTER``. display data in format.

- ``-s``, ``--static``. Without static option, 每个 minion 的返回结果是立即输出
  的. 若 outputter 是 JSON, 效果是对每个 minion 返回结果输出一个独立的 json
  object. With static option, 结果整体输出一次, 作为一个 json object. 这便于
  程序化解析.

- ``--out-file=FILE``. write output to file.

return options
""""""""""""""
- ``--return=RETURNER``. send return data to this return system. Can also
  be a comma separated list of returners.

salt-run
^^^^^^^^
execute Salt Runner modules.

options
"""""""
- ``-d``. show doc.

salt-cp
^^^^^^^
::

  salt-cp <target> [options] SOURCE [SOURCE]... DEST

- copy sources to dest of the all matching targets.

- targets see salt command.

options
"""""""
- ``-C``. chunked mode. Supports large files, recursive directories copying and
  compression.
salt-call
^^^^^^^^^
Run modules locally on minion instead of from master.

The Salt Master is contacted to retrieve state files and other resources during
execution unless the --local option is specified.

actions
""""""""
- ``--grains``. return grains.

- ``--doc``. show doc.

options
"""""""
- ``--master=MASTER``. alternative master.

- ``--return=RETURNER``

- ``--local`` without connecting to master.

- ``--metadata``. print out metadata as well.

output options
""""""""""""""
- ``--out=OUTPUTTER``.
