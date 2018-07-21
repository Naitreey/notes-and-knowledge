general
=======
- PEP8 or other style guide is important, but the most important is being
  consistent with sensible code around you.

- style guide 并不是一定总是适用的, 也就是说不要教条化, 而要根据具体情况
  构建出一套最符合实际情况的规则. (虽然很多时候, 如果能从一开始就基本上
  按照官方的来, 效果一定不会糟糕. 所以官方的风格规范实际上已经足够.)

- 不要让你的注意力从写出优质量的 pythonic code 分散至仅仅关注肤浅表面的
  styling format 上面. 在关注 style 之前, 要首先关注的是, 代码本身的结构
  是否合理, 封装是否良好, 逻辑是否流畅等. 然后才是 styling 方面的优化.

indentation and line continuation
=================================
- 4-space per indentation level.

- Always use space for indentation, avoid hard tab character.

- 关于 implicit line continuation 的两种缩进处理方式:

  1. 每行元素与 opening parenthesis/bracket/brace 等对齐. 例如

     .. code:: python

       abc = function_something(a, b, c,
                                d, e, f)

  2. hanging indent 风格, 类似 javascript 中的风格. 此时, opening delimiter 是
     首行的最后一个字符, 此后的元素按照标准缩进对齐, 最后 closing delimiter 单独
     位于最后一行, 与首行的第一个字符对齐. 例如

     .. code:: python

       abc = function_something(
           a, b,
           c, d,
           e, f,
       )

  对于 simple statement, hanging indent 更常用一些.
  在 compound statement 中的头部, 即开启一个 code block 的位置, 应该尽量使用第一种
  对齐方式, 因为 hanging indent 可能显得很怪.

  .. code:: python

    def func(
        var1, var2, var3
    ):
        pass

    def func(var1, var2,
             var3):
        pass

  然而, 如果 compound statement 的头部太长, 第一种对齐方式带来的换行效果不明显,
  因此应该酌情只 hanging 起始部分, 但结束部分不单独换行对齐.

  .. code:: python

    for name, mac, model in zip_longest(
            nic_names, macaddresses, nic_models):
        pass

  起始本质上这种情况下该在哪里换行哪里对齐还是要看具体的语义, 比如如果是函数定义,
  就应该使用第一种方式, 因为参数列表应该对齐.

  .. code:: python

    def this_is_very_long_how_can_it_be_so_long(and_it_has, many_many_very_long,
                                                parameters_like_this, yeah,
                                                so_cool):
        pass

- 若在 compound statement 的头部, line continuation 之后在缩进时导致与 code block
  的缩进量相同, 可以增加缩进量. 例如

  .. code:: python

    if (a > b and
        c < d):
        x = 1

    # better choice

    if (a > b and
            c < d):
        x = 1

- 对于必须使用 backslash line continuation 的情况, 例如 multiple-with statement,
  应在各个元素处的起始处对齐.

  .. code:: python

    with NamedTemporaryFile() as temp,
         open(file, "w") as f:
        pass

- Do not mix tab with spaces in indentation. Actually, do not ever use tab
  in indentation.

- 在 line continuation 时, 若涉及 binary operator, 算符应该位于下一行的行首,
  并逐行对齐. 原因是, 在数学公式的 typesetting 中我们已经发现, 这样有清晰的
  显示效果.

  (Although formulas within a paragraph always break after binary operations
  and relations, displayed formulas always break before binary operations.
  -- Donald Knuth, The TeXBook)

  .. code:: python

    income = (gross_wages
           + taxable_interest
           + (dividends - qualified_dividends)
           - ira_deduction
           - student_loan_interest)

  若现有的代码习惯了在 operator 后面去换行, 则继续这个风格也可.

line length
===========
- 代码部分每行最佳状态是 79 字符以内. 根据实际情况某些行允许多几个字符.
  但这样的行应该是极少数的. 一个固定字符数的限制, 目的在于提醒程序员,
  maybe this line is doing too much, maybe it's not doing great, maybe
  it's better to split up into more of lines.

- 文字描述部分, 例如注释或 docstring 最多 72 字符.

- 行太长时, 最好是使用 implicit line continuation 方式去 wrap line.
  但仍有一些必须使用 backslash line continuation 的地方, 例如 multi-with statement.

blank lines
===========
- Surround top-level function and class definitions with two blank lines.

- Method definitions inside a class are surrounded by a single blank line.

- Use blank lines in functions, sparingly, to indicate logical sections.

source file encoding
====================
- 源代码使用 utf8 编码, 对于 py2, 必须在源代码中声明字符集.

- 使用 unix LF line terminator, 不要出现 windows CRLF.

import
======
- 全局范围的 import 要尽量放在 module 的起始部分, 在 comment/docstring 以及
  ``__future__`` import 之后.

- 不要在一个 import statement 中载入多个模块.

- import 语句的分组顺序:

  1. standard library

  2. related third party library

  3. 本地应用或者库模块的 imports

- 一个 package 内部模块之间的 import 应该使用 explicit relative imports,
  除此之外都使用 absolute imports. 禁止使用 implicit relative imports.

- 恰当地使用 wildcard import. 当一个 module 提供了大量的 utility 并且我们
  很可能大量使用时, 可以使用; 当我们需要子模块提供的资源 republish 到
  package 的 namespace 中时, 可以使用 (注意子模块此时应定义 ``__all__``).

- ``__all__``, ``__version__``, ``__author__`` 等 metadata 应尽量靠上, 尽量
  位于所有 import 之前.

- import 时如果一行放不下, 应使用 ``()`` 进行 implicit line continuation,
  并且符合以下格式:

    .. code:: python

      from somemodule import (
          name1, name2,
          name3, ...
      )

- 有时候 import 的时候引入整个或部分 namespace 的名字, 而不是 namespace 下面的具体
  要使用的内容, 具有更好的代码可读性. 因此时调用任何所需量的时候, 需要 prefix
  namespace 的名字. 这样提供了 context:

  .. code:: python

    import liba
    liba.func(...)

  但这是一个细致的问题, 需要具体看情况选择不同的 import 方式, 没有绝对好坏之分.

strings literal
===============
- For triple-quoted string, always use double quote character.
  即 ``"""abcdef"""``, 而不要用 ``'''abdef'''``.

- 在可行时, ``[]`` 里的 key 使用 single quote char, value 使用 double quote char.
  dict literal 全部使用 double quote char, 与 json 对应.

whitespace in expressions and statements
========================================
- Opening parenthesis/bracket/brace 之后以及相应的 closing delimiter 之前,
  不要出现空格. 例如, 不要这样: ``spam( ham[ { 2, 3 } ] )``

- 作为分隔符时 ``,`` ``;`` ``:`` 的前面不要出现空格.

- ``:`` 作为 slice operator 时是一个 binary operator, 因此要求两侧有对称的
  空格量. when a slice parameter is omitted, the space is omitted. 例如:
  ``ham[: f(x) : g(x)]``, ``ham[:: g(x)]``

- 不要在 function call 的 opening parenthesis 前面加空格.

- Avoid trailing whitespace anywhere.

- 常见的 binary operator 两侧要有一个空格::

    =, +=, -=, /=, ==, <, >, !=, <=, >=, in, not in, is, is not, and, or, not

- 当等号用在 function 定义或调用的参数中, 即表示 keyword arg 或默认值时,
  不要在两侧加空格, key, value 要紧跟着.

- function/variable annotation 中, ``:`` 与 dict 中类似, 后面加空格, 前面
  不加空格, ``->`` 两侧要有空格.

  .. code:: python

    def func(x: int) -> str:
        return str(x)

    a: int

- 当 function/variable annotation 后需要设置默认值或者需要赋值时, ``=`` 两侧
  需要空格.

  .. code:: python

    def func(x: int = 0) -> str:
        return str(x)

    a: int = 1

- 尽量不要在一行中用 ``;`` 连写多个 simple statement.

- 对 one-liner compound statement, 不要把那一行 body 跟 header 部分放在同一行.

trailing commas
===============
- 当构建 one-tuple ``e,`` 时, 为了清晰并通用, 应该加上括号 ``(e,)``.

- 在 parentheses/brackets/braces 中, 往往允许末尾加上一个 trailing comma.
  当这些元素分多行写时, 才加上这个 trailing comma. 这是为了在 diff 时
  没有因增加 ``,`` 导致的多余的行修改.

  .. code:: python

    a = [
        1, 2, 3,
        4, 5, 6,
    ]

comments
========
- 尽量 write code that explains itself, 而不是写一堆难以理解的代码然后靠边上的
  注释去解释.

- 代码修改时, 注释和相应的文档也要一起修改. Comments that contradict the code
  are worse than no comments.

- 注释的首字母要大写, 符合英文句子规则.

- 一段代码相应的注释要有相同的 indentation level.

- Paragraphs inside a block comment are separated by a line containing a single #.

- An inline comment is a comment on the same line as a statement.
  Inline comments should be separated by at least two spaces from the statement.
  They should start with a # and a single space.

- 对 function/class 等进行解释的 comment 应该放在 ``def`` ``class`` 等行的下面.
  有 docstring 的话, 放在它下面.

docstrings
==========
- A docstring is a string literal that occurs as the first statement
  in a module, function, class, or method definition.

- 所有公有 package, 公有模块, 公有函数, 公有类, 公有方法都要有 docstring.

- 对于 multiline docstring, closing triple quote 单独放一行.

- 对 one liner docstring, triple quote 可放在同一行也可单独放一行.
  虽然 pep8 推荐前者, 但是明显后者更统一, 且方便扩展.

- One-liners are for really obvious cases. Triple quotes are used even though
  the string fits on one line. This makes it easy to later expand it.

- A package may be documented in the module docstring of the __init__.py
  file in the package directory.

- For consistency, always use ``"""triple double quotes"""`` around docstrings.
  Use ``r"""raw triple double quotes"""`` if you use any backslashes in your
  docstrings.

- 各种 docstring 前面都不要加空行; package/module 的 docstring 后面要加一个空行,
  function/method 的 docstring 后面不要加空行, class 的 docstring 后面要加一个
  空行.
  (注意是否加空行的判断标准: 被注释的对象是否由多个逻辑自洽的单元组合而成.
  例如, 在类中每个方法是一个逻辑单元, 我们在方法之间加空行, 所以类的注释和第一个
  方法之间也应加空行. 而函数本身是一个逻辑单元, 所以它的注释和代码之间不加空行.)

- Multi-line docstrings consist of a summary line just like a one-line docstring,
  followed by a blank line, followed by a more elaborate description. It's
  important that the first line fits in one line and is separated from the rest
  of the docstring by a blank line.

- The entire docstring is indented the same as the quotes at its first line.

- Docstring should NOT be a "signature" reiterating the function/method parameters.

naming conventions
==================
- 所有的 identifier 应该使用 ASCII 字符集之内的字符.
  (注意 py3 中支持 unicode identifier.)

- identifier 的命名应是能体现其含义的英文单词组合或恰当的缩写形式.

- Names that are visible to the user as public parts of the API should
  reflect usage rather than implementation.

- class name 使用 CamelCase 时, 注意当名字中包含缩写时, 需要将所有缩写大写,
  而不是只大写缩写的首字母, e.g., 是 ``HTTPConnection``, 不是 ``HttpConnection``.

- 表示公有 API 的一部分使用 ``identifier``. 谁都可以访问.

- 表示内部使用的量用 ``_name`` 命名. 如果这个量在 module level 定义,
  ``from module import *`` 不会 import 这个量. 如果这个量定义为 class
  成员, 则不是 public API 的一部分. 这个量会被子类继承, 相当于 Java 中的
  protected member.

- 表示类的私有成员的量用 ``__name`` 命名, Java 的 private member. 这样的量在
  class 或 instance 的 namespace 中定义后, 就会被 name mangling. 不能在不失去灵
  活性的前提下 在子类中直接访问.  如果某个类成员确实只应该这个类自己去使用不 让
  子类访问, 请这样命名.

- 避免与 keyword 冲突时, 用 ``keyword_``.

- 不要自创 ``__name__``, 这些是 python 定义的 magic objects/methods, 每一项都有特殊
  用途, 不要混淆这个命名空间.

- modules 命名使用全小写, 并允许使用 ``_`` 进行分隔.

- 私有模块命名以 ``_`` 起始.

- 一般情况下 Class names 以 CamelCase 方式命名. 若这个类主要是当作一个函数来
  使用, 而不是看作实例化, 则可以按照函数的方式命名. 例如, ``slice()``,
  ``range()``, ``bool()`` 等 builtin function/class.

- 若一个 exception class 确实是错误, 应该以 ``Error`` 结尾.

- 全局常量命名全部大写和 ``_``.

- 全局变量、非全局变量和函数使用全小写加 ``_`` 的命名方式.

- instance method 的第一个变量用 ``self`` 命名, class method 的第一个变量用
  ``cls`` 命名.

- 对于 public attribute, 若有复杂的 set/get 操作需求, 最好使用 property.
  这保证了 API 简洁.

  property 之类的特殊方法, 是作为 attributes 来使用, 因此应该放在 class 最
  前面, ``__init__`` 后面. 与普通 instance attributes 靠得比较近, 这样意义
  更清晰.

- module 应该设置 ``__all__`` 来定义自己提供的公有 API. 注意此时非公有的部分仍然
  应该加上 ``_``.

- An interface is considered internal if any containing namespace (package,
  module or class) is considered internal.

- Imported names should always be considered an implementation detail, unless
  it's imported to constitute part of API.

Programming
===========
- Singleton 类型的量之间的比较, 一定要用 ``is`` ``is not``.

- ``if something is not None`` 不等价于 ``if something``.

- 要用 ``something is not another``, 不要用 ``not something is another``.

- 实现 rich comparisons 时, 要实现全部 6 个比较操作, 或者借助
  ``functools.total_ordering``.

- 如果需要把 lambda 表达式赋值给变量, 那就不该用 lambda, 用 ``def``.

- 一个函数里可以完全没有 return; 但如果有 return statement, 所有的返回点都要
  有 return, 且如果没有明确的返回值, 需要 ``return None``.

- 使用 ``isinstance()`` 进行类型判断, 不要使用 ``type(obj) is sometype``.

- function annotation 可能并不一定是好的. python 是 duck type language, 函数的输入
  和返回值都可以是恰当的任何类型的量, 过早地使用 annotation 可能限制函数的使用范围
  和可扩展性.

- 在 python2 中, finally clause 一定要小心. 这个 statement 里面的东西最好不可能再
  raise exception, 否则 解释器将不再处理 try 里面的 exception, 而去处理新的
  exception. 这样从 traceback 里就看不出原来的错误了.

- 不要轻易连等赋值. 提醒自己这将导致两个 identifier 指向同一个对象哦... 问问自己
  你真的想要这样么?

- Python2 中, 判断一个对象是否是字符串时, 要用 ``basestring``; python3 中没有这个
  问题.

- For container types, use the fact that empty containers are false.
