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

general
=======
- 根据命令行配置自动生成 help messages 和自动进行命令行校验.

ArgumentParser
==============

constructor parameters
----------------------

prog
~~~~
控制 help 中 usage 行的程序名字.

- default: 是取 ``sys.argv[0]`` 的 basename 部分.

usage
~~~~~
控制 help 中 usage 行的 usage 内容.

- default: 根据各种命令行配置构成.

description
~~~~~~~~~~~
控制 help 中 usage 行下面的描述信息.

- default: 什么都没有.

epilog
~~~~~~
在所有信息最后的一部分说明. 一般用于某种补充说明, 注释, 示例等等.

- default: 不存在.

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

prefix_chars
~~~~~~~~~~~~
一组 optional parameters 允许的 prefix 字符.

- default: ``-``

fromfile_prefix_chars
~~~~~~~~~~~~~~~~~~~~~
一组 prefix 字符, 它后面的参数认为是包含额外命令行参数的文件.

- default: 没有.


