language
========

class
-----

old-style class and new-style class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- old-style class vs new-style class.

  * 从 OOP 角度, new-style class 是 object 的子类, 这样的类是一个类型, 地位与 int, str
    等 built-in 类型等同. 形成了一个以 object 为 root 的继承树 (类似 Java).

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

exception
---------

- Syntax.

  .. code:: python

    # - py2 -

    try:
        pass
    except Exception, exc:
        pass
    # or
    except Exception as exc:
        pass

    # - py3 -

    try:
        pass
    except Exception as exc:
        pass
    # which makes it possible to catch by multiple exception classes
    except (FileNotFoundError, PermissionError) as exc:
        pass

  compatibility:

  .. code:: python

    try:
        pass
    except (FileNotFoundError, PermissionError) as exc:
        pass


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

builtin types
-------------

- 整数类型. int & long -> int.

  py2:
  
  * int -- hardware-based (``sys.maxint``, ``long`` in C, 2**63-1).

  * long -- software-based. unlimited. Indicated by ``L`` suffix.

  py3:

  * int. 自动切换.

- 除法.

  py2:

  * `/`: floor division. result is `int`, rounding downwards.::

      1/2=0, -1/2=-1

  py3:
    
  * `/`: float division. 两整数转换为 `float` 后再做除法, 结果是 `float`.

  * `//`: floor division, as in py2.


  compatibility::
  
    from __future__ import division

IO
--

- print:
    2. print 是 keyword, 后接要输出的表达式成为 print statement, 不是 expression
       print 的格式比较局限, 在 script 中, 可以在末尾添加 `,` 做到不回行
       print a, b, c 将对各自分别单独输出, 并非将 3 个表达式都运算后再输出, 而是运算一个输出一个.
       print (a,b,c) 是输出这个 tuple
    3. print 是 buitin function, 有完整的参数表, 灵活得多的参数配置, 返回值 None, 是 expression

- input(), raw_input():
    2. raw_input() 将输入的字符序列组成字符串; input() 即 eval(raw_input()), 返回相应的 python expression
    3. input() 返回 string, 等价于 2 里的 raw_input()

- "`x`":
    2. shortcut for repr(x), deprecated
    3. `x` syntax is removed

- binary I/O stream:
    2. communicate with binary I/O stream using `bytes`. Because str is also bytes, str can be read/written directly from/into binary I/O
    3. other type/class of objects has to be encoded/converted to bytes in order to be used with binary I/O. In particular, str is no longer bytes-compatible, which is now encoded in unicode.

- range() and xrange():
    2. range() returns a list of integers
       xrange() returns an xrange object that generates the numbers in the range on demand.
    3. xrange() in 2 is renamed to be range() (with slight modification), which returns a range object.

- builtin sequence types:
    2. list, tuple, str, unicode, xrange object, bytes (alias for str), bytearray
    3. list, tuple, str, range object, bytes, bytearray

- sort() & sorted():
    2. keyword arg `cmp` is deprecated, use `key` to generate a sorting key
    3. cmp is removed in 3, use `key`.

- `string` module:
    3. string.letters string.uppercase ... is removed. as unicode is default, these string constant make no sense any more. Use `ascii_` prefixed version

- translate chars in string:
    2. string.maketrans() provide translation table, str.translate() executes the translation and handles deletechars
    3. string.maketrans() is moved to be a function of str type. It is also more flexible. 并且删除字符也统一为映射的一部分, 从而在 maketrans() 中指明. str.translate() 只根据 translation table 执行 translation.


- dict.has_key():
    2. has_key() method is deprecated
    3. has_key() method is removed

- dict.items():
    2. return a list of 2-tuples of the form (k,v)
    3. return a view of dictionary, which is a set-like object. 对应于 2 中的 viewitems()

- dict.keys():
    2. return a list of keys
    3. return a view of keys in dictionary, which is a set-like object

- urllib & urllib2:
    2. urllib 和 urllib2 提供一些互补的功能, 例如只有 urllib 提供 urlretrieve
    3. urllib 和 urllib2 合并为 urllib package, 但不同的功能分至不同的模块中
       (e.g., urllib.request, urllib.parse, urllib.error)

- sequence packing/unpacking:
    2. automatic unpacking when appropriate, e.g., a, b, c = 1, 2, 3
    3. 除了 automatic unpacking, 还有一种 `*seq` syntax, 用于对 seq 这个 sequence object 进行赋值. 一个值的序列给 `*seq` 赋值时, 自动 pack 成 sequence object. 例如 `a, b, *rest = [1,2,3,4]`

- zip():
    2. returns a list of tuples
    3. returns a zip object

- exec:
    2. 在 2 中, exec 是一个 keyword, 即 exec statement, 不是表达式故没有返回值概念
       指定 namespace 的方式是 exec ... in scope
    3. 在 3 中, exec 是一个 function, 即 exec(), 返回值 None
       指定 namespace 的方式是 exec(..., scope)

- chr():
    2. ascii, for unicode use unichr()
    3. unicode

- rebind variables in intermediate scope/namespace:
    2. you cannot do that
    3. use `nonlocal` keyword

- function annotation:
    2. unavailable
    3. available

- indentation:
    2. allow tab/space mix indentation
    3. disallow tab/space mix indentation

- iterator:
    2. iterator object has next() method to get its next value, or use next() global function
    3. iterator object has `__next__()` method to get its next value, which should be called by global next() function

- reload():
    2. available for truly reloading a module
    3. removed, because it's not a good way of programming

- sys.platform:
    2. "linux" + major kernel version (which is always inconsistent)
    3. "linux" alone

- string formatting:
    2. string formatting operator `%`, `string.Template` class, `str.format` method
    3. ditto, `str.format` is preferred.

- file type:
    2. 存在 builtin file type, file() 则生成新的 file object, file() 与 open() 效果相同, open() is preferred.
    3. 不存在 builtin file type, file object 由 io 等类构造得到, 只存在 open() 函数.

- builtin exception hierarchy:
  不同的 builtin exception hierarchy. 3 的更合理.

  * IOError 和 OSError 合并为 OSError, 并且在其下增加了很多具体的错误类型,
    例如 FileNotFoundError, ConnectionError 及其子类等,
    以代替在 py2 中必须要检查 errno 来判断系统错误类型的麻烦.

- source code character set:
    2. 使用 7-bit ASCII character set, 源文件默认为 ASCII 编码, 并向 ASCII 字符集映射. 因此不允许 ASCII 以外的字符码出现 (以 binary data 形式出现的除外. 若源文件使用 ASCII 编码的 compatible superset, 应该声明源文件的编码. 此时仍然向 ASCII 字符集映射, 但允许 string literals & comments 中出现 ASCII 以外字符码的字符. 这些字符将保留为编码的原二进制形式, 从而能够以 ASCII 字符所表示.
    3. 使用 unicode character set, 源代码可以使用任何编码, 并向 Unicode 字符集映射. 源代码的任何部分允许使用任何能够用 Unicode 字符表示的字符码.

- type coercion
    2. 通过类中定义的 __coerce__ method 以及 coerce() 函数来完成不同数值类型值的转换
    3. type coercion is removed from language.

- implicit & explicit relative import:
    2. 允许 implicit relative import, 即对于:
        package +
            __init__.py
            module1.py
            subpackage +
                __init__.py
                module2.py
                module3.py
        在 module3.py 中, 允许:
            import module2 (同一个层级: 同一个 subpackage 中的 module)
            import module1 (顶层 package 的 module)
       以及允许 explicit relative import
    3. 不允许 implicit relative import, 只允许 explicit relative import

- thread module
    2. 有 bug, Thread.join() 参数为空或 None 时, 彻底 block, KeyboardInterrupt 也没用. 这波及到例如 threading, multiprocessing.Pool 等众多模块.
    3. 修复了这个 bug.
- function definition
    3. `sulist` syntax is removed
- comparison
    2. dict comparision is undefined, but consistently behaved.
    3. dict comparision raises TypeError
- 很多 py23 的区别可以在 `2to3` 这个工具中找到.

- diff py2py3

  * str, bytes, encoding

  * old style class

  * absolute import

  * dict.keys|values|items, iteration

  * dict key order

  * map, range, zip

  * pyc, __pycache__

  * io module

  * __traceback__, __context__, __cause__

  * async, await

  * formatted string

  * pathlib 是更加一般化更加易用的路径处理工具, 以替代绝大部分 os.path 操作

- string and bytes representation of object

  * py2 中实现: `__unicode__` 和 `__str__`

  * py3 中实现: `__str__` 和 `__bytes__`

  这可以统一地解决 (django.utils):

  .. code:: python

    def python_2_unicode_compatible(klass):
        """
        A decorator that defines __unicode__ and __str__ methods under Python 2.
        Under Python 3 it does nothing.

        To support Python 2 and 3 with a single code base, define a __str__ method
        returning text and apply this decorator to the class.
        """
        if PY2:
            if '__str__' not in klass.__dict__:
                raise ValueError("@python_2_unicode_compatible cannot be applied "
                                 "to %s because it doesn't define __str__()." %
                                 klass.__name__)
            klass.__unicode__ = klass.__str__
            klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
        return klass

- py2 中 type 和 types.ClassType 分别对应 new/old style class 的类型.

- py2 中 round 函数只支持 float 且返回 float, py3 中它支持任何实现了 ``__round__``
  的类型, 且对于 float 返回 int.

- py2 中, 若 class decorator 中要对类实例化或要生成新类, 原类定义中使用 ``super()``
  时会造成麻烦 (NameError 或无限递归).

- py2 除了非常新的可能 2.7.6 以上的版本, ``shlex.split`` 无法处理 unicode 命令.
  至少在 2.7.2 中还有这个问题. 只能在 split 之前先 encode 至 bytes. 这为写向
  py3 兼容的代码又增加麻烦.

- py3 中 ``urlopen`` 的返回对象得到了优化. 可以用作 context manager.

- py3 中删除了 ``unicode`` builtin function.

- json decode 时报的 exception, 在 py2 中经常是非常一般化的错误, 难以 catch 单独处理;
  在 py3 中是 ``JSONDecodeError``, 很明确.

- python3 去掉了 unbound method 概念. ``class.func`` 得到的就是定义的函数本身;
  ``instance.func.__func__ is class.func`` 成立. ``class.func`` 不再具有 ``__func__``
  属性.

- django 2.0 不再支持 python2.

- coroutines 是在 python3.5+ 才有的功能.

- python3.4 添加了 enum module.

- python3.2 添加了 html module.

- py2py3 compatible

  * __future__

  * open, range, str, map

  * 根据不同 module 结构 import

  * 不能用 py3-only syntax

  * 设置一个 ``six`` or ``compat`` module 来实现所有能统一实现的 py2py3 兼容性逻辑.

  * ``django.utils.six`` 提供了非常多有价值的 py2py3 兼容性处理方案.

  * py2 中 user-defined class 的 ``bool()`` value 以及 truth testing 使用的是
    ``__nonzero__`` method, py3 中使用 ``__bool__``. 为 py2py3 兼容, 两个都要
    定义.
