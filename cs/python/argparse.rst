misc
====
* 局限性:

  无法指定 ``--foo`` ``--bar`` 必须同时存在或同时不存在.

* 用 ``nargs='?'`` 指定 optional positional argument.

* ``store_const|store_true|store_false`` action 意味着这个 cmdline option 是 flag,
  不能再设置 ``nargs``, 即不跟参数.

* ``store`` action 可以设置 ``nargs``, 且 ``nargs='?'|'*'`` 时
  ``const``, ``default`` 有用处.

* 若要在 help text 中显示 default value, 应该在 help text 中使用 ``%(default)s``
  format specifier. 不要使用 ``ArgumentDefaultsHelpFormatter``, 因为它会在
  所有参数后面都加上 ``(default: ...)`` 这种. 即使是不存在默认值的 required option.

* help text 支持 format specifier. available specifiers include ``%(prog)s`` and
  most keyword arguments to ``add_argument()``.

* SUPPRESS 的各种用处.
  解释 subparsers 的描述问题. title, description, metavar, choices, ...

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
各个参数的 parser-wide default. 当某个参数是 optional 的时候, 且并没有明确设置
默认值时, 就会 fallback 至这个默认值.

``argparse.SUPPRESS`` 是一个特殊值, 若设置它为 argument_default, 则此时在结果
Namespace 中不包含默认的属性.

- default: None.

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

注意 long option 不能参数连着写, 必须使用 ``=`` or 空格分隔.

- default: True.

add_argument
------------

dest
~~~~

若 dest 未指定,

- 对于 optional parameter, 使用第一个 long option 或第一个 short option
  作为 dest.

default
~~~~~~~
- default: None.

- default value 的 fallback 顺序:

  * 明确指定.
  
  * ``set_defaults()`` 关于相应 dest 的设置.
  
  * ``ArgumentParser.argument_default`` 的值.
  
  * default: None.

nargs
~~~~~

choices
~~~~~~~

metavar
~~~~~~~

add_subparsers
--------------
- 添加 subcommands.

- 从解析逻辑上看, subparsers 与 parser 本身的各种 parameters 是同一层级的.
  因此, 本质是 subparsers action.

- 由于 ``add_subparsers`` 与 ``add_argument()`` 一样生成 action instance,
  所以两者接受的参数是差不多的. (但它还多出来可能会生成 argument group.)

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

prog
~~~~

metavar
~~~~~~~
指定 subcommands 在 usage 命令行上的形式. override choices 形式.

- default: None. 此时使用 choices 形式即 ``{cmd1,cmd2,...}``

help
~~~~

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
