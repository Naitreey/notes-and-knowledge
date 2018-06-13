language
========

class
-----

old-style class and new-style class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- old-style class vs new-style class.

  * 从 OOP 角度, new-style class 是 object 的子类, 这样的类是一个类型, 地位与
    int, str 等 built-in 类型等同. 形成了一个以 object 为 root 的继承树 (类似
    Java).

    old-style class 不是这样. 它不是 object 的子类. 没有继承, 就没有乐趣.

  * descriptor.
    
    old-style class::
   
     instance -> class -> parent

    new-style class::
   
     data descriptor -> instance -> class attr and non-data descriptor
     -> parent -> ... -> object

    因此 new-style class 可以使用 descriptor (e.g., property). More fun.


  * MRO. a.k.a. class hierarchy linearization.
    
    example: diamond problem.::

         C
        / \
       /   \
      A     B
       \   /
        \ /
         D

    old-style class: DACBC (left-to-right, depth first.)
    new-style class: BABC

- syntax.

  .. code:: python

    # - py2 -

    class A: # old-style class
        pass

    class A(object): # new-style class
        pass

    # - py3 -

    class A: # new-style class
        pass

    class A(object): # new-style class
        pass

  compatibility:

  .. code:: python

    class A(object):
        pass

definition
^^^^^^^^^^
- python3 去掉了 unbound method 概念. ``class.func`` 得到的就是定义的函数本身;
  ``instance.func.__func__ is class.func`` 成立. ``class.func`` 不再具有
  ``__func__`` 属性.

inheritance
^^^^^^^^^^^

- MRO see above.

- method overriding. argumentless ``super()``. 

  .. code:: python

    class A(object):
        def func(self):
            pass

    # - py2 -

    class B(A):
        def func(self):
            super(B, self).func()
            # ...

    # - py3 -

    class B(A):
        def func(self):
            super().func()
            # ...

  compatibility: use ugly one.

- py2 中, 若 class decorator 中要对类实例化或要生成新类, 原类定义中使用
  ``super()`` 时会造成麻烦 (NameError 或无限递归).

metaclass
^^^^^^^^^
- compatibility.

  .. code:: python

    from future.utils import with_metaclass
    class Cls(with_metaclass(Meta, Parent)):
        pass

exception
---------

- ``except`` clause.

  .. code:: python

    # - py2 -

    try:
        # ...
    except Exception, exc:
        pass
    # or
    except Exception as exc:
        pass

    # - py3 -

    try:
        # ...
    except Exception as exc:
        pass
    # which makes it possible to catch by multiple exception classes
    except (FileNotFoundError, PermissionError) as exc:
        pass

  compatibility: latter form.

- context and cause.

  .. code:: python

    # - py2 -

    try:
        raise SyntaxError
    except Exception as exc:
        # handle exception but failed
        raise IndexError

    # output:
    # Traceback (most recent call last):
    #   File "<stdin>", line 5, in <module>
    # IndexError

    # - py3 -

    try:
        raise SyntaxError
    except Exception as exc:
        # handle exception but failed
        raise IndexError

    # output:
    # Traceback (most recent call last):
    #   File "<stdin>", line 2, in <module>
    # SyntaxError: None
    # 
    # During handling of the above exception, another exception occurred:
    # 
    # Traceback (most recent call last):
    #   File "<stdin>", line 5, in <module>
    # IndexError

    try:
        raise SyntaxError
    except Exception as exc:
        # handle exception
        raise IndexError from exc

    # output:
    # Traceback (most recent call last):
    #   File "<stdin>", line 2, in <module>
    # SyntaxError: None
    # 
    # The above exception was the direct cause of the following exception:
    # 
    # Traceback (most recent call last):
    #   File "<stdin>", line 5, in <module>
    # IndexError

- ``raise`` statement.

  .. code:: python

    # - py2 -

    raise exc_type|exc_value, exc_value|args|None, None|exc_tb

    # - py3 -

    raise exc_value[.with_traceback(exc_tb)] [from None|exc_value]

  compatibility:

  .. code:: python

    from future.utils import raise_, raise_from, raise_with_traceback

- builtin exception hierarchy.

  * py2. https://docs.python.org/2/library/exceptions.html#exception-hierarchy

  * py3. https://docs.python.org/3.6/library/exceptions.html#exception-hierarchy

  主要在于对 OSError 的细化, 方便处理.

  .. code:: python

    import errno

    # - py2 -

    try:
        # ...
    except (IOError, OSError) as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

    # - py3 -

    try:
        # ...
    except FileNotFoundError as exc:
        pass

  compatibility: use ugly one.

- exception info. All exception-related info is locally available.

  .. code:: python

    # - py2 -
    import sys
    try:
        # ...
    except Exception as exc:
        exc_type, exc_value, exc_tb = sys.exc_info

    # - py3 -
    try:
        # ...
    except Exception as exc:
        exc_type, exc_value, exc_tb = type(exc), exc, exc.__traceback__

    # context and cause
    exc.__context__
    exc.__cause__

  compatibility: use the ugly one.

scope
-----

- py2.

  * ``global`` keyword.

- py3.

  * additional ``nonlocal`` keyword.

  .. code:: python

    # - py2 -

    def f():    
        a = 1
        def g():
            a = 2
            print(a)
        g()
        print(a)
        
    # - py3 -

    def f():    
        a = 1
        def g():
            nonlocal a
            a = 2
            print(a)
        g()
        print(a)
        

builtin types
-------------
py3 removed following types: long, unicode, xrange.

- 整数类型. int & long -> int.

  py2:
  
  * int -- hardware-based (``sys.maxint``, ``long`` in C, 2**63-1).

  * long -- software-based. unlimited. Indicated by ``L`` suffix.

  py3:

  * int. 自动切换.

- arithmetic -- 除法.

  py2:

  * `/`: floor division. result is `int`, rounding downwards.::

      1/2=0, -1/2=-1

  py3:
    
  * `/`: float division. 两整数转换为 `float` 后再做除法, 结果是 `float`.

  * `//`: floor division, as in py2.


  compatibility::
  
    from __future__ import division

    # use / for float division, // for floor division

- range object.

  py2:

  * ``range()`` returns a list of integers.

  * ``xrange()`` returns an xrange object that generates the numbers in the
    range on demand.

  py3: ``xrange`` renamed to be ``range``. ``range()`` is now a builtin type.

  compatibility::

    range = xrange

    # or

    from builtins import range

- builtin sequence types:

  py2: list, tuple, str, unicode, xrange object, bytes (alias for str), bytearray

  py3: list, tuple, bytes, str, range object, bytearray


- object.

  * string and bytes representation of object
  
    * py2 中实现: `__unicode__` 和 `__str__`
  
    * py3 中实现: `__str__` 和 `__bytes__`

    compatibility

    .. code:: python

      from six import *

      @python_2_unicode_compatible
      class A:
        def __str__(self):
            # ...

  * boolean test.

    - py2. ``__nonzero__``

    - py3. ``__bool__``

    compatibility:

    .. code:: python

      def implements_bool(cls):
          if not PY3:
              cls.__nonzero__ = cls.__bool__
              del cls.__bool__
          return cls

      @implements_bool
      class Container(object):

          def __init__(self):
              self.bucket = []

          def __bool__(self):
              return bool(self.bucket)

  * type coercion
  
    - py2. 通过类中定义的 __coerce__ method 以及 coerce() 函数来完成不同数值
      类型值的转换.
  
    - py3. type coercion is removed from language.
  
- dict

  * test for key existence. ``dict.has_key()`` is removed.

    .. code:: python

      "key" in d

  * iteration of keys, values, items. See `iteration`_.

  * (py3.6) order of dict key is implicitly ensured.

    For compatibility and correctness, still use ``OrderedDict``.

- basestring, removed. Since ``str`` is the only and actual string type.

string formatting
-----------------
python 中有 4 种 string interpolation 的方式:

- ``%`` printf-style formatting. 即 modulo operation.
  implemented in ``str.__mod__``.

- ``str.format()``.

- Shell-like string template: ``string.Template``.

- formatted string literals. ``f"..."``. (py3.6)

第一种最常见最简单, 但不如第二种方便;

第二种明显优点有 2 个, 1) 灵活方便, 功能丰富; 2) 使用 `__format__` protocol
可以自定义 format 逻辑, 实现多态性的封装 (duck typing), e.g., datetime.

第三种克服了第二种的 verbosity 问题, 并且增加灵活性可以执行 python 表达式.
所以, 对于 py3.6+, 应该用第三种, 之前的最好用第二种.

第四种仅用在特殊场合, 例如为了填充使用了 shell syntax 的模板, 或者为了与常见的
formatting 语法相区别.

iteration, generation, async programming
----------------------------------------

iteration
^^^^^^^^^
- 在 py2 中直接生成 a list of results 的很多方法和函数, 转换成了生成一个
  iterator, 而不直接生成结果.

  * dict

    .. code:: python

      # dict
      .iterkeys(), .itervalues(), .iteritems()
      keys(), values(), items()

    don't use ``iter*`` anymore.

  * zip, range, map, filter.

    compatibility

    .. code:: python

      from itertools import imap as map, izip as zip, ifilter as filter
      range = xrange

      # or

      from builtins import map, zip, range, filter

  * other iterable functions in itertools

    .. code:: python

      from itertools import ifilterfalse as filterfalse, izip_longest as zip_longest

- ``iterator.next()`` -> ``iterator.__next__()``

  compatibility:

  .. code:: python

    from future.utils import implements_iterator
    @implements_iterator
    class Counter(object):

        def __init__(self, start=0):
            self.count = start

        def __iter__(self):
            return self

        def __next__(self):
            self.count += 1
            return self.count

coroutine
^^^^^^^^^
- py3.5+ 添加了 coroutine.

builtin functions
-----------------
py3 removed following built-in functions: apply, cmp, coerce, execfile, file,
raw_input, reduce, reload.

- comparision and key functions.::
 
    orted(), min(), max(),
    heapq.nlargest(), heapq.nsmallest(),
    itertools.groupby()

  py2. keyword arg `cmp` is deprecated, use `key` to generate a sorting key

  py3. cmp is removed in 3, use `key`.

  compatibility::

    from functools import cmp_to_key

    [].sort(key=cmp_to_key(func))

- ``reload`` -> ``importlib.reload``, ``reduce`` -> ``functools.reduce``.

  .. code:: python

    from importlib import reload
    from functools import reduce

- ``round()``.  py2 中 round 函数只支持 float 且返回 float, py3
  中它支持任何实现了 ``__round__`` 的类型, 且对于 float 返回 int.

- ``unicode()`` is removed.

- ``exec()``.

  * py2. exec 是 keyword, 即 exec statement.

  * py3. exec 是 function, 返回值 None.

- ``apply()`` removed.

IO
--

- ``print``.

  * py2. print 是 keyword, print statement (not an expression).
    print 的格式比较局限, 在 script 中, 可以在末尾添加 `,` 做到不回行

  * py3. print function (therefore expression). Makes more flexible formatting
    and options possible.  Also In line with other languages.::

      print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

  compatibility::

    from __future__ import print_function

- ``input(), raw_input()``

  * py2. raw_input() 输入字符输出字符串; input() 即 ``eval(raw_input())``.

  * py3. ``input()`` is original ``raw_input()``.

  compatibility

  * future::

      input = raw_input

      # or

      from future.builtins import input

  * conversion::

      input -> eval(input())

- ``file``, ``open`` and ``io`` module.

  * 整个 IO 的对象封装重新设计. py3 中全部基于 ``io`` module.

  * open all files with ``open``, stop using ``file``.

    .. code:: python

      # - py2 -

      open(name[, mode[, buffering]])

      # - py3 -

      open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

  * compatibility

    .. code:: python

      from io import open

- ``StringIO``.

  * py3. 整合至 ``io`` module.

  * compatibility

    .. code:: python

      from io import StringIO, BytesIO

character set and encoding
--------------------------
- 字符集和编码. See `../characters-and-fonts/character-encodings.rst`.

- string literal.

  * py2.
    
    - ``str``: ASCII 字符集. 1byte for each char.::

        "string"

    - ``unicode``: Unicode 字符集. 1 code point for each char.::

        u"unicode"

  * py3. (sanitized.) ``str`` 即 unicode. ``bytes`` for byte string.::

      "string"
      b"bytes"

  compatibility

  - future::

      from __future__ import unicode_literals

      chr = unichr
      # or
      from builtins imoprt chr

  - use normal string as unicode string, use bytes for bytes::

      "string" # unicode in py2
      b"bytes" # str in py2

- source code encoding

  py2: default ascii encoding. 需要使用以下声明, 否则不能包含 ascii 以外
  的字符. 即使如此, 只允许 comment & string literal 中包含 ascii 之外的
  字符.

  .. code:: python

    # -*- coding: utf-8 -*-
    # vim:fileencoding=utf-8

  py3: default utf-8 encoding.

  .. code:: python

    哈哈哈 = 1


module and package
------------------

- implicit relative import vs explicit relative import.

  Suppose the following project hierarchy::

    proj/
    ├── __init__.py
    ├── app1.py
    └── utils.py

  .. code:: python

    # app1.py

    # - py2 -

    from utils import *

    # - py3 -

    # local
    from .utils import *
    # global
    from utils import *

  compatibility

  - future::

      from __future__ import absolute_import

  - always use absolute import

- namespace package. (not commonly used. But good to know.)

  * 相同名字的目录分散在 ``sys.path`` 的不同位置.
  
  * Without ``__init__.py``.

  ::

    root/
    ├── proj1
    │   └── parent
    └── proj2
        └── parent

  usage: 给一个由别人维护的 package 添加自己的功能和修改.

iterable unpacking, dict unpacking
----------------------------------

- in literal

  * py2. none

  * py3.

    .. code:: python

      [-1, *range(10), 10, 11, *{"what": "thefuck", "are you": "doing"}, 12, 13,]
      {"a":1, **dict(a=1, b=2), "c": 3, **OrderedDict(c=3, d=4),}

- in assignment

  * py2.

    .. code:: python

      a, b = range(2)
      a, b = b, a

  * py3.

    .. code:: python

      a, b, *rest = range(10)
      a, b, *(c, *[d, *(e, *f), g], h), i, j, (), l = *range(20), [], 20

- in function definition

  * py2.

    - positional without default.
      (required, can be provided by positional or kwarg.)

    - positional with default.
      (optional, can be provided by positional or kwarg.)

    - rest of positionals.

    - rest of kwargs.

    .. code:: python

      def func(a=1, b=2, *args, **kwargs):
          pass

  * py3.

    - positional without default.
      (required, can be provided by positional or kwarg.)

    - positional with default.
      (optional, can be provided by positional or kwarg.)

    - keyword-only without default.
      (required, must be provided by kwarg.)

    - keyword-only with default.
      (optional, must be provided by kwarg.)

    - rest of positionals

    - rest of kwargs

    .. code:: python

      def func(a=1, b=2, *args, c=3, d=4, **kwargs):
          pass

      def func(a=1, b=2, *, c=1, d):
          pass

      def func(*, c=1, d):
          pass

- in function call. 在定义中要求的 positional and kwarg 可以通过
  1) positional 2) kwarg 3) iterable unpacking 4) dict unpacking 提供.

  * py2. At most one iterable unpacking and one dict unpacking is allowed.

    .. code:: python

      f(*(1,2,3), **{"a": 1, "b": 2})

  * py3. any number of iterable unpacking and dict unpacking is allowed.

  additional rules.

  * 最终转换成 positionals 的部分 (包括 positional & iterable unpacking) 应该在
    最终转换成 kwargs 的部分 (包括 kwarg & dict unpacking) 的前面.

  * 在各自部分之内, 两种语法可以任意顺序和数量出现.

annotation
----------
Still too much?

- function annotation

  .. code:: python

    def func(a: int, b: str) -> None:
        pass

- variable annotation (py3.6)

  .. code:: python

    a: "hey, there"

misc language features
----------------------
- ``\`x\```:

  * py2. shortcut for ``repr(x)``, deprecated

  * py3. ``\`x\``` syntax is removed

cpython
=======

bytecode
--------

- ``__pycache__``

- 按照版本保存.

REPL
----
- gnu readline library for autocompletion.

library
=======
- Standard library reorganization `PEP 3108 <https://www.python.org/dev/peps/pep-3108/>`_

  涉及 44 modules. 例如: urllib, http.

  compatibility:

  * 根据 py 版本选择不同的 import path.

  * 使用 future.

    .. code:: python

      from future import standard_library as _standard_library
      _standard_library.install_aliases()

- new packages. e.g., pathlib, enum, ipaddress, html.

  compatibility:

  * install explicit backport packages. e.g., enum, singledispatch, pathlib.

  * install backports namespace packages.

py2 py3 compatible code
=======================

prerequisites
-------------

- understand what is changed and how to fix.

  * See above.

  * See also `Writing Python 2-3 compatible code <http://python-future.org/compatible_idioms.html>`_.

- tools.

  * future. 提供诸多 python3 功能的 backport. 提供 ``futurize`` 脚本
    自动转换源代码至 py3-compatible.

  * six (implicit)

  * 2to3 (implicit)

  * argparse (pip, py2.6 only)

  * importlib (pip, py2.6 only)

- 不要盲目信任这些工具. They do have bugs and limitations (like every software).
  这就是为什么需要从原理上理解 py2, py3 的区别. 当这些工具失效时, 需要手工去实现
  合适的兼容性修改.

  这也是要看源代码的原因之一.

conversion
----------
- ``futurize``

  .. code:: sh
  
    futurize2 -a -0 <file|dir>

- 检查转换结果.

coding 
------
- `Writing Python 2-3 compatible code <http://python-future.org/compatible_idioms.html>`_.

- 不能用 py3-only syntaxes. 即使 conditionally 也不行. 因为解释器在
  语义分析阶段就会报错 SyntaxError.

- 每个文件中设置 ``__future__`` imports.

- 项目中设置一个 ``six`` module/subpackage, 包含所有项目中需要使用到的
  兼容性定义. 在项目的各个文件中, import 该文件.

  example:

  .. code:: python

    # six.py
    # -*- coding: utf-8 -*-
    # vim:fileencoding=utf-8

    from __future__ import division
    from __future__ import absolute_import
    from __future__ import print_function
    from __future__ import unicode_literals

    import sys
    from builtins import *
    from future import standard_library as _standard_library
    _standard_library.install_aliases()
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    # optional additional tests
    PY26 = sys.version_info[0:2] == (2, 6)

- 其他兼容性定义也放在该文件中. 可以参考 django (1.11), celery 等.

- 在其他项目文件中加入以下代码. 然后直接按照 python3 风格书写.

  .. code:: python

    # another file
    # -*- coding: utf-8 -*-
    # vim:fileencoding=utf-8
    from __future__ import division
    from __future__ import absolute_import
    from __future__ import print_function
    from __future__ import unicode_literals

    from .six import *

- 在具体情况下, 需要分别对 py2, py3 进行不同实现时, 做版本判断, 再分别实现.

  .. code:: python

    if PY2:
        # ...
    else PY3:
        # ...

tools
-----

python-future
^^^^^^^^^^^^^
features
""""""""
- 提供从 py2-only code 向 py2py3-compatible 的兼容性 module 和转换脚本.
  (向前兼容)

- 提供从 py3-only code 向 py2py3-compatible 的兼容性 module 和转换脚本.
  (向后兼容)

- 实现 standard library reorganization. 使用 python3 的 library
  hierarchy 来 import module.

tools
"""""
- ``future`` package (forward-compatibility)
  
  * ``future.builtins`` py3 builtins

  * ``future.utils`` compatible utils

- ``past`` package (backward-compatibility)

- ``futurize`` script

- ``pasteurize`` script

- import tools. 实现 PEP 3108 standard library reorganization.
  
  * 诸多 wrapper packages

  * extensions on existing packages

  * included backports

usage
""""""
- use ``futurize`` script to convert existing py2 code.

- use ``future`` and ``builtins`` package to write forward-compatible code.
  (Together with ``__future__``.)

multi-version management
========================

See `here <multi-version.rst>`_.
