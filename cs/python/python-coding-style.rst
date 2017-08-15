general
-------
- PEP8 or other style guide is important, but the most important is being
  consistent with sensible code around you.

- style guide 并不是一定总是适用的, 也就是说不要教条化, 而要根据具体情况
  构建出一套最符合实际情况的规则. (虽然很多时候, 如果能从一开始就基本上
  按照官方的来, 效果一定不会糟糕. 所以官方的风格规范实际上已经足够.)

indentation and line continuation
---------------------------------
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

  对于 simple statement, hanging indent 更常用一些. 然而如果是在 compound statement
  中的头部, 即开启一个 code block 的位置, hanging indent 可能不太合适. 例如

  .. code:: python

    def func(
        var1, var2, var3
    ):
        pass

  这样就很怪. 这时就比较适合第一种对齐方式:

  .. code:: python

    def func(var1, var2,
             var3):
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
-----------
- 代码部分每行最佳状态是 79 字符以内. 根据实际情况某些行允许多 2-3 个字符.
  但这样的行一定是极少数的.

- 文字描述部分, 例如注释或 docstring 最多 72 字符.

- 行太长时, 最好是使用 implicit line continuation 方式去 wrap line.
  但仍有一些必须使用 backslash line continuation 的地方, 例如 multi-with statement.

blank lines
-----------
- Surround top-level function and class definitions with two blank lines.

- Method definitions inside a class are surrounded by a single blank line.

- Use blank lines in functions, sparingly, to indicate logical sections.

source file encoding
--------------------
- 源代码使用 utf8 编码, 对于 py2, 必须在源代码中声明字符集.

- 使用 unix LF line terminator, 不要出现 windows CRLF.

import
------
- Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
-  Imports should be grouped in the following order:
    1. standard library imports
    2. related third party imports
    3. local application/library specific imports
- Absolute imports are recommended, as they are usually more readable and tend to be better behaved (or at least give better error messages) if the import system is incorrectly configured.
- However, explicit relative imports are an acceptable alternative to absolute imports, especially when dealing with complex package layouts where using absolute imports would be unnecessarily verbose.
- Wildcard imports ( from <module> import * ) should be avoided, as they make it unclear which names are present in the namespace, confusing both readers and many automated tools.
- import 时如果一行放不下, 应使用 ``()`` 进行 implicit line continuation, 并且符合以下格式:

    .. code:: python

    from somemodule import (
        name1,
        name2,
        name3,
    )

quoting strings
---------------
-  When a string contains single or double quote characters, however, use the other one to avoid backslashes in the string. It improves readability.
- For triple-quoted strings, always use double quote characters.

whitespace in expressions and statements
----------------------------------------
- Avoid extraneous whitespace in the following situations:
    Immediately inside parentheses, brackets or braces.
    Immediately before a comma, semicolon, or colon.
    Immediately before the open parenthesis that starts the argument list of a function call.
    Immediately before the open parenthesis that starts an indexing or slicing.
- Always surround these binary operators with a single space on either side: assignment ( = ), augmented assignment ( += , -= etc.), comparisons ( == , < , > , != , <> , <= , >= , in , not in , is , is not ), Booleans ( and , or , not ).
- If operators with different priorities are used, consider adding whitespace around the operators with the lowest priority(ies).
- Don't use spaces around the = sign when used to indicate a keyword argument or a default parameter value.
- Do use spaces around the = sign of an annotated function definition. Additionally, use a single space after the : , as well as a single space on either side of the -> sign representing an annotated return value.
- Compound statements (multiple statements on the same line) are generally discouraged.
- While sometimes it's okay to put an if/for/while with a small body on the same line, never do this for multi-clause statements.

comments
--------
- Always make a priority of keeping the comments up-to-date when the code changes.
- Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code. Each line of a block comment starts with a # and a single space.
- An inline comment is a comment on the same line as a statement.

docstrings
----------
- A docstring is a string literal that occurs as the first statement in a module, function, class, or method definition.
- Write docstrings for all public modules, functions, classes, and methods. Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does. This comment should appear after the def line.
-  A package may be documented in the module docstring of the __init__.py file in the package directory.
- For consistency, always use """triple double quotes""" around docstrings. Use r"""raw triple double quotes""" if you use any backslashes in your docstrings. For Unicode docstrings, use u"""Unicode triple-quoted strings""" .
- One-liners are for really obvious cases. Triple quotes are used even though the string fits on one line. This makes it easy to later expand it.
- There's no blank line either before or after the docstring.
- Multi-line docstrings consist of a summary line just like a one-line docstring, followed by a blank line, followed by a more elaborate description. It's important that the first line fits in one line and is separated from the rest of the docstring by a blank line.
- The entire docstring is indented the same as the quotes at its first line.
- The docstring of a script (a stand-alone program) should be usable as its "usage" message, printed when the script is invoked with incorrect or missing arguments (or perhaps with a "-h" option, for "help").

naming conventions
------------------
- 所有的 identifier 必须使用 ASCII 字符集之内的字符.
  (注意 py3 中支持 unicode identifier.)

- identifier 的命名应是能体现其含义的英文单词组合或恰当的缩写形式.

- Names that are visible to the user as public parts of the API should follow conventions that reflect usage rather than implementation.

- `_single_leading_underscore` : weak "internal use" indicator. E.g. from M import * does not import objects whose name starts with an underscore.
- `single_trailing_underscore_` : used by convention to avoid conflicts with Python keyword.
- `__double_leading_underscore` : when naming a class attribute, invokes name mangling.
- `__double_leading_and_trailing_underscore__` : "magic" objects or attributes that live in user-controlled namespaces.
- Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.
- When an extension module written in C or C++ has an accompanying Python module that provides a higher level (e.g. more object oriented) interface, the C/C++ module has a leading underscore (e.g. `_socket` ).
- Class names should normally use the CamelCase convention.
- Function, method and instance variable names should be lowercase, with words separated by underscores as necessary to improve readability.
-  Always use self for the first argument to instance methods. Always use cls for the first argument to class methods.
- Constants are usually defined on a module level and written in all capital letters with underscores separating words.
- Always decide whether a class's methods and instance variables (collectively: "attributes") should be public or non-public. If in doubt, choose non-public; it's easier to make it public later than to make a public attribute non-public.
- take care to make explicit decisions about which attributes are public, which are part of the subclass API, and which are truly only to be used by your base class.
- Public attributes should have no leading underscores.
- If your class is intended to be subclassed, and you have attributes that you do not want subclasses to use, consider naming them with double leading underscores and no trailing underscores. This invokes Python's name mangling algorithm, where the name of the class is mangled into the attribute name. This helps avoid attribute name collisions should subclasses inadvertently contain attributes with the same name.
- To better support introspection, modules should explicitly declare the names in their public API using the __all__ attribute. Setting __all__ to an empty list indicates that the module has no public API.
- Comparisons to singletons like None should always be done with is or is not , never the equality operators.
- Use is not operator rather than not ... is . While both expressions are functionally identical, the former is more readable and preferred.
- When implementing ordering operations with rich comparisons, it is best to implement all six operations ( __eq__ , __ne__ , __lt__ , __le__ , __gt__ , __ge__ ) rather than relying on other code to only exercise a particular comparison. To minimize the effort involved, the functools.total_ordering() decorator provides a tool to generate missing comparison methods.
- Always use a def statement instead of an assignment statement that binds a lambda expression directly to an identifier. The use of the assignment statement eliminates the sole benefit a lambda expression can offer over an explicit def statement (i.e. that it can be embedded inside a larger expression, they can be of ad-hoc use).
- Derive exceptions from Exception rather than BaseException . Direct inheritance from BaseException is reserved for exceptions where catching them is almost always the wrong thing to do.
- When catching exceptions, mention specific exceptions whenever possible instead of using a bare except: clause.
-  If you want to catch all exceptions that signal program errors, use except Exception: (bare except is equivalent to except BaseException: ).
- for all try/except clauses, limit the try clause to the absolute minimum amount of code necessary.
- When a resource is local to a particular section of code, use a with statement to ensure it is cleaned up promptly and reliably after use. A try/finally statement is also acceptable.
- Be consistent in return statements. Either all return statements in a function should return an expression, or none of them should.
- Use string methods instead of the string module (whenever possible).
- Object type comparisons should always use isinstance() instead of comparing types directly. When checking if an object is a string, keep in mind that it might be a unicode string too! In Python 2, str and unicode have a common base class, basestring.
- function annotation 可能并不一定是好的. python 是 duck type language, 函数的输入和返回值都可以是恰当的任何类型的量, 过早地使用 annotation 可能限制函数的使用范围和可扩展性.
- finally clause 一定要小心. 这个 statement 里面的东西最好不可能再 raise exception, 否则 解释器将不再处理 try 里面的 exception, 而去处理新的 exception. 这样从 traceback 里就看不出原来的错误了.
- 不要轻易连等赋值. 提醒自己这将导致两个 identifier 指向同一个对象哦... 问问自己你真的想要这样么?
- Python 的 duck typing 思想与物理学思想一致, 即我们认识事物的方式是根据事物表现出来的行为, 而不是事物的所谓 "本质". 这样的本质并不存在, 因其不可观测.
- when possible, public methods should avoid "get_xxx()" 这种指明动作的 naming style. 而是应该直接使用 obj.xxx 或者 obj.xxx(). 但很多时候如果需要输入参数, 指明动作更自然一些.
- 如果只需要一个 logging level, 默认使用的应该是 INFO, 因为在 DEBUG level, 一些库可能输出
  很多没用的 debug 信息.
- module 中绝不该出现在 import 时会给出输出的 "裸代码". 也就是说它不该做奇怪的事情, 应该
  keep silent.
- python 中有 4 种 string formatting 方式:
  %-formatting, str.format(), formatted string literal 以及 string.Template.
  其中, 最后一种根本不该使用;
  第一种最常见最简单, 但不如第二种方便;
  第二种明显优点有 2 个, 1) 灵活方便, 功能丰富; 2) 实际上使用 `__format__` protocol,
  即可以自定义 format 逻辑, 实现多态性的封装 (duck typing), e.g., datetime;
  第三种克服了第二种的 verbosity 问题, 并且增加灵活性可以执行 python 表达式.
  所以, 对于 py3.6+, 应该用第三种, 之前的最好用第二种.

- 什么时候应该规定使用 factory function 来获取类实例, 什么时候不需要这层封装只简单地对类
  进行实例化就行?

  factory function 相对于类的 constructor, 其根本特点是可以对返回实例的逻辑进行自定义,
  而 constructor 简单地每次调用生成一个新实例. 例如, 使用 factory function 可以做到:

  * 条件性生成新实例, 例如依据 identifier 存储实例, match 时只返回原来生成的实例.

    何时需要考虑条件性生成新实例呢? 当实例应该具有某种全局存在性质, 而不是某个
    其他类的实例的属性, 或者局限于某个范围. 例如 Logger 就应该是全局的, 不属于某个
    类, 对于一个 module 而言应该唯一, 因此以 module.__name__ 作为标识符来条件性
    生成新实例. 相应地, 数据库连接等 client object (例如 MongoClient) 往往不需要
    全局存在, 而是作为某个其他类对象的一部分, 在该类对象生成时创建连接状态, 析构
    时消除状态.

  * 需要对实例进行额外的修改, 且这些修改在逻辑上不是该类的一部分.

- 何时该创建各种 exception class 并在出错时 raise 出来, 何时该只返回操作的 true/false
  结果?
