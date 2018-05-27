misc
====
* 局限性:

  无法指定 ``--foo`` ``--bar`` 必须同时存在或同时不存在.

* argparse.SUPPRESS 各种抑制各种输出. 它可用的地方有:

  - 所有 argument group, 包括 subparsers, 的 title & description.

  - ArgumentParser 的 usage, description, epilog.

  - 所有 help 参数. 若 help 是 SUPPRESS, 则不输出参数的 help, 以及不在 usage 中
    包含该参数.

general
=======
- 根据命令行配置自动生成 help messages 和自动进行命令行校验.

- 基本执行逻辑:

  * 在构建命令行语法阶段 (相当于 compile-time), 根据 add_argument 等方法调用,
    构建一组 action list. 这组 action list 是对命令行语法形式的 token 化和拆解.
    它决定了程序接受的命令行参数以及对解析结果的相应影响.

  * 在解析实际命令行阶段 (相当于 runtime), 将各式各样的命令行书写方式拆解成可与
    action list (的 option strings) 进行匹配的形式. 匹配并执行 action, 在 result
    namespace 中产生相应的输出或影响.

ArgumentParser
==============

constructor parameters
----------------------

prog
~~~~
控制 help 中 usage 行的程序名字.

- default: 是取 ``sys.argv[0]`` 的 basename 部分.

也许想要在 usage 中连路径也包含进去, 那就直接使用 ``sys.argv[0]``.

usage
~~~~~
控制 help 中 usage 行的 usage 内容.

- default: 根据各种命令行配置生成.

- interpolation kwargs: prog.

description
~~~~~~~~~~~
控制 help 中 usage 行下面的描述信息.

- default: 什么都没有.

- interpolation kwargs: prog.

epilog
~~~~~~
在所有信息最后的一部分说明. 一般用于某种补充说明, 注释, 示例等等.

- default: 不存在.

- interpolation kwargs: prog.

parents
~~~~~~~
这个参数不是指定 parent parser, subparser 之类的不同层级的关系. 也就是说不是
在构建不同层级的 parser 处理不同层级的命令行参数. 那是 ``add_subparsers()``
负责的.

这个参数实现的是抽象不同 parser 中相同的参数部分至统一的 "abstract" parser.
它们作为所有 parser 的 parents. 然后在 child parser 中通过该参数, 将 parent
的所有 positional/optional 参数添加至 child parser 中.

formatter_class
~~~~~~~~~~~~~~~
控制 description, epilog, 各参数的 help message 等部分如何 formatting.

- default: HelpFormatter.

prefix_chars
~~~~~~~~~~~~
一组 optional parameters 允许的 prefix 字符.

- default: ``-``

fromfile_prefix_chars
~~~~~~~~~~~~~~~~~~~~~
一组 prefix 字符, 它后面的参数认为是包含额外命令行参数的文件.
文件中应该每行一个参数. 文件中可以再次包含别的文件, 即递归.

- default: 没有.

argument_default
~~~~~~~~~~~~~~~~
- 各个参数的 parser-wide default. 当某个参数是 optional 的时候, 且并没有明确设置
默认值时, 就会 fallback 至这个默认值.

  * default: None.
  
  * ``argparse.SUPPRESS`` 是一个特殊值, 若设置它为 argument_default, 则此时在结果
    Namespace 中不包含默认的属性.

conflict_handler
~~~~~~~~~~~~~~~~
若 parser 添加的各个参数之间有重复、冲突等不一致的地方, 该如何处理. 可选的方式是
``error``, ``resolve``. error 就报错, resolve 就 simply override any older
arguments with the same option string.

- default: error.

add_help
~~~~~~~~
控制是否自动添加 ``-h, --help`` 参数.

对于包含公共 parser 逻辑的 "abstract" parser, 应该设置 False.

- default: True.

allow_abbrev
~~~~~~~~~~~~
控制:

- 是否允许 long options to be abbreviated to its unambiguous prefix;

- 是否允许 short option 与它的参数连在一起写;

- 是否允许多个 short options 连在一起写, 并且最后一个 short option 还
  可以有参数.

default: True.

add_argument()
--------------
在什么都不自定义的情况下,

- optional argument 默认是 optional 的, 若设置则默认接受一个参数.

- positional argument 默认是 required 的, 默认接受一个参数.

action
~~~~~~
- builtin actions:

  * store. positional/optional 都可以. nargs 必须 > 0.

  * store_const. 存储 const 指定的值. 此时 const 参数是必须的, nargs
    必须不指定, 且 ``nargs=0``. 该参数只对 optional argument 有意义.
    适用于构建 flag.

  * store_true. 存储 True. 其他同 store_const.

  * store_false. 存储 False. 其他同 store_const.

  * append. 同一个参数多次出现时, 每次的值 append 至一个 list.
    其他类似于 store. 该参数只对 optional argument 有意义.

  * append_const. 同一个参数多次出现时, 将固定的 const 值 append 至 list.
    其他类似于 store_const. 该参数只对 optional argument 有意义.

  * count. 统计一个参数的出现次数. 必须不指定 nargs 且 ``nargs=0``.
    该参数只对 optional argument 有意义. 适用于表达程度. 例如 verbosity
    ``-vvvv``.

  * help. print help. 一般没啥用.

  * version. 输出版本信息. 要求指定 ``version`` 参数, 其值可包含 ``prog``
    interpolation argument.

  * parsers. 内部用于生成 subparsers.

- default: store.

nargs
~~~~~

- 选项:

  * ``N``, 对于 optional/positional argument 都是接受 N 个命令行参数. 生成一个 list.
  
  * ``?``, 对于 positional, 接受 1 个或使用 default; 对于 optional, 当该命令行参数
    出现时, 接受 1 个值或使用 const.
  
  * ``*``, 对于 optional argument, flag 后面的 0 个或多个参数 (直到下一个 flag 为止)
    都进入一个 list; 对于 positional argument, 命令行上剩余所有 0 个或多个 positional
    进入一个 list. 因此, 对于多个 optional, ``nargs="*"`` 可使用多次; 对于 positional,
    只能使用一次, 且应该是最后一个 positional.
  
  * ``+``, 与 ``*`` 类似, 除了要求必须至少有一个.

  * ``argparse.REMAINDER``, 命令行上所有右侧剩余参数放在 list 中. 用于传参数至别的程序.
    应作为最后一个参数. 它与 ``*`` 的区别是, ``*`` 在 positional 时是只识别
    positional 的, 若中间夹杂 optional 形式的参数会报错, 需要 ``--`` 进行分隔.
    而这个参数会直接把右侧所有剩余参数都扔进去.

- default: 根据不同 action 而不同.

required
~~~~~~~~
只有 optional argument 可以设置 required.

对于 positional, required 不能设置, 而是通过 nargs 的设置来推断 required 的值.

const
~~~~~

default
~~~~~~~
对于 optional argument, 未指定时使用.
对于 positional argument, 当 nargs 的设定允许参数省略时, 即: ``nargs="?", nargs="*"``
时使用.

- default:

  * ``store``, ``store_const`` action, None.

  * ``store_true`` action, False.

  * ``store_false`` action, True.

  * ``append``, ``append_const`` action, 相当于 [].

  * ``count`` action, 相当于 0.

  .. TODO 待确认各种情况无遗漏.

- default value 的 fallback 顺序:

  * 明确指定.

  * ``set_defaults()`` 关于相应 dest 的设置.

  * ``ArgumentParser.argument_default`` 的值.

  * default: None.

- 若 default is SUPPRESS, 结果 namespace 中不添加 dest 对应的默认值.

- 从效果上看, 除非 ``default`` 值为 ``SUPPRESS`` 或者 fallback 至 ``SUPPRESS``,
  在 ``parse_args()`` 阶段, 生成的 namespace 中一定会有相应的参数项, 若命令行
  没有指定, 则取根据上述逻辑确定的默认值. 

type
~~~~
参数值格式检查和类型转换.

choices
~~~~~~~
any sequence supporting ``in`` operator will do.
由于先转换再检查 choices, the type of its values should match that of ``type``
argument.

dest
~~~~

- default:

  * 对于 optional parameter, 使用第一个 long option 或第一个 short option
    作为 dest.
  
  * 对于 positional parameter, 使用第一个参数.

若 dest is SUPPRESS, namespace 中不添加相应结果.

help
~~~~
控制各参数的 help message.

- interpolation args: 这个 action 的全部参数. 去除 SUPPRESS 参数.

metavar
~~~~~~~
控制 usage 行和参数帮助行中的形式参数.

- default: 对于 positional, dest value; 对于 optional, uppercased dest value.

add_argument_group()
--------------------
create new argument group. positional arguments 和 optional arguments,
以及 subcommands 都是 argument group.

一般的 argument group 只是在修改 help message 的表现方式方面有意义.

add_argument()
~~~~~~~~~~~~~~
给该组增加 action, 这与 ArgumentParser 的方法是同一个. (同一个父类的继承.)
增加的 action 同时注册在该组和整个 parser 中.

add_mutually_exclusive_group()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mutex group 也是 argument group. 但是这些组目前不会在 help 中单独分组, 它的
actions 散布在 positional/optional argument groups 中. 只在 usage 中
显示互斥性.

主要作用是在 parse_arg 时进行互斥性检查.

add_subparsers()
----------------
- 添加 subcommands.

- 从解析逻辑上看, subparsers 与 parser 本身的各种 parameters 是同一层级的.
  本质是 subparsers action.

- help message 形式. 与一般的 positional argument 类似, 会以 metavar 和
  help 两个参数的值为一行出现. 不同的是, 由于 subparsers action 存在
  subactions 即 subcommands. 在 metavar + help 行下面会 indent 以多行
  列出每个子命令的 name + help.

  此外, 若 add_subparsers() 指定了 title and/or description, 则单独生成一个
  argument group, 否则就放在 positional argument group 中.

  由于只可能有一个 subparsers group, 当有一个 subparsers action 单独放在一个
  argument group 中显示时, metavar + help 行以及 subcommands 的缩进实际上是
  有些多余的. 此时, 可以这样写 formatter 解决:

  .. code:: python
    from argparse import ArgumentParser, HelpFormatter, _SubParsersAction
    class NoSubparsersMetavarFormatter(HelpFormatter):

        def _format_action(self, action):
            result = super()._format_action(action)
            if isinstance(action, _SubParsersAction):
                # fix indentation on first line
                return "%*s%s" % (self._current_indent, "", result.lstrip())
            return result

        def _format_action_invocation(self, action):
            if isinstance(action, _SubParsersAction):
                # remove metavar and help line
                return ""
            return super()._format_action_invocation(action)

        def _iter_indented_subactions(self, action):
            if isinstance(action, _SubParsersAction):
                try:
                    get_subactions = action._get_subactions
                except AttributeError:
                    pass
                else:
                    # remove indentation
                    yield from get_subactions()
            else:
                yield from super()._iter_indented_subactions(action)

- add_subparsers 本应支持 ``required`` kwarg, 但目前不支持. workaround
  是直接对生成的 subparsers action ``required`` 属性赋值. (因为它是
  subclass of Action.)
  .. code:: python
    subparsers = parser.add_subparsers()
    subparsers.required = True

- 由于 ``add_subparsers`` 与 ``add_argument()`` 一样生成 action instance,
  两者接受的参数是差不多的. (但它还多出来可能会生成 argument group.)

title
~~~~~
当存在 title and/or description 时, 生成一个单独的 argument group.
title/description 就是该 group 的 title 和 description.

当 title and description 都不存在时, subparsers action 与其他 positionals
一起出现在 positional argument group 中.

- default: subcommands (若创建单独的组).

description
~~~~~~~~~~~
- default: None.

* 解释 subparsers 的描述问题.

prog
~~~~
subparsers group 整体的 prog_prefix. 它是 subcommand ``prog`` 值的统一
前缀 (如果 subparser 不自定义 prog 的话.)

- default: parent prog + parent positional arguments.

dest
~~~~
name of the attribute under which sub-command name will be stored.

- default: SUPPRESS. 即默认不存储 subcommand name.

metavar
~~~~~~~
指定 subcommands 在 usage 命令行上和参数 help 中的形式. override 默认的
choices 形式.

- default: None. 此时使用 choices 形式即 ``{cmd1,cmd2,...}``.
  默认的 choices 形式源于 _SubParsersAction 在实例化时将 choices 属性赋值为
  自身存储的 subcommand choices mapping.

help
~~~~
subparsers group 在 argument help 中的 help message.

parser_class
~~~~~~~~~~~~
parser class to use for subparsers.

action
~~~~~~
定义生成 subparsers action 使用的 action class.

- default: parsers.

add_parser()
~~~~~~~~~~~~
接受所有 ArgumentParser 参数和以下参数:

- name. subcommand name.

- aliases. a sequence of aliases for this subcommand. 即在 subcommand
  choice list 中增加这些 alias, 指向同一个 subparser.

- help. subcommand 在 parent parser help message 中的 help 部分.

以下参数需特殊说明:

- prog. 若不设置, 默认为 subparsers 的 prog 值 + subcommand name.

One particularly effective way of handling sub-commands is to combine the use
of the add_subparsers() method with calls to set_defaults() so that each
subparser knows which Python function it should execute. 每个 subparser 都
设置一个相同的 namespace attribute, e.g. ``operation``, 但每个 subparser
设置不同的值, 即不同 subcommand 对应不同的操作. 这样在结果中获取该属性就得到了
要进行的操作.
.. code:: python
  parser = ArgumentParser()
  subparsers = parser.add_subparsers()
  sub1 = subparsers.add_parser()
  sub2 = subparsers.add_parser()
  sub1.set_defaults(operation=op1)
  sub2.set_defaults(operation=op2)
  args = parser.parse_args()
  args.operation(**vars(args))

set_defaults()
--------------
设置各 dest 在 parser 中的默认值. 这是第二层 default.

parse_args()
------------

- optional/positional argument 的参数顺序:
  
  * 为避免麻烦, 一般遵循 optional 在先, positional 在后的规则.
    
  * 包含 subparsers 时, subcommand 之前的参数都是 parent parser 的参数,
    之后的参数都是 subparser 的参数.

  * 用 ``--`` 表示 optional argument 部分结束, 之后所有参数按照 positional
    去解析.

- optional arguments 形式:

  * short option 可以与值连着写.

  * 多个 short options 可以连写, 且最后一个可跟参数值 (连着或不连着).
  
  * long option 不能和值连着写, 必须使用 ``=`` or 空格分隔.

- ``--`` 表示 optionals 结束, 后面全是 positionals.

- ``allow_abbrev`` 允许的各种缩写形式.

- subparsers.

  * 在结果中, subparser 的解析结果 merge 到 main parser 中.

parse_known_args()
------------------
仅解析已知参数, 留下未知参数. 返回 a tuple of namespace and unknown args list.

这可用于向调用的脚本传递参数. 或者通过 REMAINDER 方式向调用的脚本传递参数.

exiting methods
---------------

- exit(), exit with custom message and status code.

- error(), exit with usage and custom message with status 2.

formatters
==========

HelpFormatter
-------------

- base class of all formatters.

constructor
~~~~~~~~~~~
- width: 默认使用 COLUMNS environ 或 80.

RawDescriptionHelpFormatter
---------------------------
保持 description & epilog 部分 verbatim. 注意其中 description 指的不仅是
ArgumentParser 整体的, 还包含 argument group (``add_argument_group()``)
的, 以及 subparsers group (``add_subparsers()``) 的.

RawTextHelpFormatter
--------------------
保持所有文字内容 verbatim.

ArgumentDefaultsHelpFormatter
-----------------------------
当 help message 中没有 ``%(default)`` format specifier, 即没有已经加入 default
信息时, 自动在末尾加入 default 值.

若想要某些 option 不显示这自动生成的 default, 使用 ``default=SUPPRESS``.

MetavarTypeHelpFormatter
------------------------
修改默认的 metavar 值为 type 参数值. 注意若有设置 metavar, 明确设置的仍然有
更高优先级.

actions
=======

concept
-------

- action 封装的是对命令行输入解析后的命令行操作单元. 这个操作 (action),
  指的是输入一定的解析完成的命令行参数, 会在结果集中插入什么样的内容,
  以及会做什么样的其他任意操作.

- action 存储这个操作关联的所有参数信息, 并且定义这个操作在 parse 结果 namespace
  中造成什么影响.

action API
----------
an action is a callable which returns a callable.

* the action callable itself must accept the two positional arguments plus any
  keyword arguments passed to ``ArgumentParser.add_argument()`` except for the
  action itself, i.e.::
    option_strings, dest, nargs=None, const=None, default=None, type=None,
    choices=None, required=False, help=None, metavar=None

* the callable returned by action callable must accept the following parameters:

  - parser. The ArgumentParser object which contains this action.

  - namespace. The Namespace object that will be returned by parse_args().
    Most actions add an attribute to this object using setattr().

  - values. The associated command-line arguments, with any type
    conversions applied. Type conversions are specified with the
    type keyword argument to add_argument().

  - option_string. The option string that was used to invoke this action. The
    option_string argument is optional, and will be absent if the action is
    associated with a positional argument.

  the callable may perform arbitrary actions, but will typically set
  attributes on the namespace based on ``dest`` and ``values``.

types
=====

FileType
--------
用于封装文件 type, 转换后在结果中直接成为 fileobj.

API
---
any callable that takes arg string, then checks and returns the converted value.
