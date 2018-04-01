overview
========
- python is a dynamic and strongly typed language.

  * strongly typed 与 statically typed. 这是两个互不相关概念, 没有必然联系.
    In a dynamically typed language, a variable is simply a value bound to a
    name; the value has a type -- like "integer" or "string" or "list" -- but
    the variable itself doesn't. You could have a variable which, right now,
    holds a number, and later assign a string to it if you need it to change.
    In a statically typed language, the variable itself has a type; if you have
    a variable that's an integer, you won't be able to assign any other type of
    value to it later. Some statically typed languages require you to write out
    the types of all your variables, while others will deduce many of them for
    you automatically. A statically typed language can catch some errors in
    your program before it even runs, by analyzing the types of your variables
    and the ways they're being used. A dynamically language can't necessarily
    do this, but generally you'll be writing unit tests for your code either
    way (since type errors are a small fraction of all the things that might go
    wrong in a program); as a result, programmers in dynamic languages rely on
    their test suites to catch these and all other errors, rather than using a
    dedicated type-checking compiler.

  * weakly typed 与 strongly typed. In a weakly typed language, the compiler or
    interpreter can perform behind-the-scenes conversions of variable types to
    make certain types of operations work. Like in JS, you can add strings to
    numbers 'x' + 3 becomes 'x3'. In a strongly typed language, you are simply
    not allowed to do anything that's incompatible with the type of data you're
    working with.

  Refs: [PythonFAQ]_.

- interpreted language. CPython interpreter pre-compiles source to bytecode
  then executed. cpython does not has JIT engine. But PyPy has.

Data model
==========

The standard type hierarchy
---------------------------
包含对一系列类型概念的标准陈述.

class
~~~~~

- 实例化.

  调用 ``cls(*args, **kwargs)`` 进行类实例化的执行逻辑:

  1. create instance:
     调用 static method ``object.__new__(cls, *args, **kwargs)`` 创建
     实例 ``instance``.

  2. customize instance:
     调用 ``instance.__init__(*args, **kwargs)``.

  最后返回 ``instance`` 给 caller.

- attribute reference.

  搜索顺序. 首先搜索 class ``__dict__``, 然后搜索 parent class ``__dict__``
  in MRO order. 最后搜索 metaclass 的 attributes.
  即 (不考虑 descriptor)::

    class -> parent class -> ... -> metaclass -> parent metaclass -> ... -> type -> object

- MRO. python2.3+ uses C3 method resolution order. 若对于一个类, 无法根据 C3 MRO
  算法给出 ``__mro__`` attribute, 则无法创建这个类. 此时会 raise TypeError.

class instance
~~~~~~~~~~~~~~

* attribute reference.
  
  搜索顺序. 首先搜索 instance ``__dict__``, 然后搜索 class & parent
  classes attributes, in MRO order. 注意不会去搜索 metaclass 的 attributes.
  即 (不考虑 descriptor)::

    instance -> class -> parent class -> ... -> object

  若属性是一个 function object, 转变成 bound instance method, 它的
  ``__self__`` attribute is the instance.

  若最终没找到, call ``__getattr__``.

* attribute modification. 修改和删除属性只更新 ``__dict__``. 若
  定义了 ``__setattr__``, ``__delattr__`` 则直接调用这两个方法.

special attributes & methods
----------------------------

instantiation
~~~~~~~~~~~~~
以下属性在 class & metaclass 上有.

- ``class.__new__(cls, ...)``. static method. 实例化时
  调用该方法创建 ``cls`` 的新实例. 剩下的参数定义就是 constructor 的参数
  signature. 返回 new object instance.

- ``class.__init__(self, ...)``. Must return None.

以下属性在 class instances 上有.

- ``instance.__class__``. the class of the instance.

attribute store
~~~~~~~~~~~~~~~
以下属性在非 ``__slots__`` objects 上有.

- ``object.__dict__``. 一个对象自身存储的属性.

object identification
~~~~~~~~~~~~~~~~~~~~~

class, function-like definitions, generator instance (including those from
generator functions and generator expressions), and module.

- ``definition.__name__``. the name of definition. for module, the qualified
  import path of module.

- ``definition.__qualname__``. the qualified name of definition.
  这是 the “path” from a module’s global scope to the object. module object
  没有这个属性.

class relations
~~~~~~~~~~~~~~~
以下属性在 class objects 上有.

- ``class.__bases__``. 一个类定义时使用的直接父类. 不包含 MRO resolved result.

- ``class.__mro__``. class 的 MRO order. It is considered when looking for base
  classes during MRO.

- ``class.mro()`` 该方法不是定义在 class 上的, 而是定义在 metaclass 上的. 所以
  在 class 中是作为 instance method 方式调用. 在生成 class object 时, 计算
  MRO order 并存储在 ``class.__mro__`` 中. 由于在 metaclass 上定义, 在 instance
  中不可见.

- ``class.__subclasses__()``. 一个类的所有现存子类. 通过 weakref 保存关系.

instance method attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``instance_method.__self__``, instance reference, readonly.

- ``instance_method.__func__``, underlying function defined in class, readonly.

- ``instance_method.__doc__``, same as ``__func__.__doc__``, readonly.

- ``instance_method.__module__``, same as ``__func__.__module__``, readonly.

container protocol
~~~~~~~~~~~~~~~~~~

- ``object.__len__()``

- ``object.__len_hint__()``, optional.

- ``object.__getitem__()``

- ``object.__missing__()``, dict 定义了该 hook, 在 ``__getitem__`` 中使用.
  当 key 不存在时, 调用 ``__missing__`` 进行自定义处理. dict 是啥都不做.

  ``collections.defaultdict`` overrides ``__missing__`` method to define
  default value for the missing key.

- ``object.__setitem__()``

- ``object.__delitem__()``

- ``object.__iter__()``

- ``object.__reversed__()``, optional.

- ``object.__contains__()``, optional.

attribute access
~~~~~~~~~~~~~~~~

- ``object.__getattribute__(self, name)``. 负责一个对象上的所有属性访问.
  In order to avoid infinite recursion in this method, its implementation
  should always call the base class method with the same name to access any
  attributes it needs.

  ``object`` base class 实现了基础的 ``__getattribute__``, 即默认情况下, 所有
  ``instance.attr`` 使用以下属性访问逻辑:

  1. 尝试 data descriptor. 若有, 调用::
       descriptor.__get__(self, instance, type(instance))

  2. 尝试 instance attribute (``__dict__``). 若有, 直接返回.

  3. 尝试 non-data descriptor 和 class attribute. 若有, 且是 non-data descriptor,
     调用::

       descriptor.__get__(self, instance, type(instance))

     若是 class attribute, 直接返回.

  4. 若以上全败, 调用 ``__getattr__``.

  5. raise AttributeError.

  ``type.__getattribute__`` 适用于所有 ``class.attr`` 的访问. 它在此基础上,
  对第二步做了修改:

  2. 尝试 instance (此时是 class object) 以及它的所有基类的 ``__dict__``. 若有,
     且是 descriptor, 调用::

       descriptor.__get__(self, None, class)

     若不是 descriptor, 直接返回.

  ``super.__getattribute__`` 对 super object 的属性访问也不同于 object 基类的实现.
  它实现了 super object 的属性访问逻辑, 对于 ``super(B, type_or_object_or_none)``

  1. 从 ``B.__mro__`` B 后面一个类开始, 尝试 descriptor 和 class attribute.
     若是 descriptor, 调用::

       descriptor.__get__(type_or_object_or_none, B)

     若不是 descriptor, 直接返回.

  由于 ``__getattribute__`` 完全决定属性访问, 并且具有以上复杂的逻辑, 所以
  subclass/submetaclass 一般不该完全自定义该方法, 而是在调用父类的方法基础上
  进行适当的自定义.

descriptor protocol
-------------------
Descriptors are a powerful, general purpose protocol. They are the mechanism
behind properties, methods, static methods, class methods, and super(). They
are used throughout Python itself to implement the new style classes introduced
in version 2.2. Descriptors simplify the underlying C-code and offer a flexible
set of new tools for everyday Python programs.

一个 descriptor 实例作为类的成员时, 才能发挥它的作用. 当通过不同的方式 (从 owner
class 访问, 从 instance of owner class 访问, 直接访问), 进行不同的操作 (get, set,
delete) 时, 表现为不同的行为.

descriptor 的这种设计, 让它非常适合封装具有适应性的逻辑, 即以不同的方式访问, 执行
不同的逻辑.

the mechanism for descriptors is embedded in the ``__getattribute__()`` methods
for ``object``, ``type``, and ``super()``.

descriptor class definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``descriptor.__get__(self, instance, owner)``. ``obj.descr`` 获取时调用.
  当 obj 为 instance of owner class 时, ``instance = obj``, ``owner = type(obj)``;
  当 obj 为 owner class 时, ``instance = None``, ``owner = obj``.

- ``descriptor.__set__(self, instance, value)``. ``obj.descr = ...`` 赋值时
  调用. 对 descriptor 赋值只能在 instance of owner class 中生效.

- ``descriptor.__delete__(self, instance)``. ``del obj.descr`` 删除时调用.
  删除 descriptor 只能在 instance of owner class 中生效.

定义以上任意方法, 则 class 成为 descriptor.

分类和调用优先级
~~~~~~~~~~~~~~~~
- data descriptor: 定义 ``__get__`` 和 ``__set__``. 若定义 readonly descriptor,
  让 ``__set__`` raise AttributeError 即可.
  
- non-data descriptor: 只定义 ``__get__``.

在 ``obj`` instance 上进行 attribute lookup  ``obj.attr`` 时, attr 的搜索优先级
为:

- data descriptor.
 
- instance attribute.
 
- non-data descriptor and class attribute. (注意 method 实际是 non-data descriptor.)

- ``__getattr__``. 

typical use cases
~~~~~~~~~~~~~~~~~

- property: properties are data descriptors.

- function: all functions are non-data descriptors which return bound methods
  when they are invoked from an object.

  bound method 是在 instance 上访问时才从 ``__get__`` 中生成的. 每次访问都会
  生成一个全新的 bound method 实例 (内存地址不同). 在它上面添加了 ``__self__``
  ``__func__`` ``__class__`` 等属性.

- static method, class method.

class creation
--------------
- class definition block 与动态使用 ``metaclass(name, bases, namespace)``
  创建 class 本质相同.

  .. code:: python

    class A:

        x = 1

        def a(self):
            pass

    A = type("A", (object,), {'x': 1, 'a': a})

- 默认的 metaclass 是 ``type()``.

class creation procedure
~~~~~~~~~~~~~~~~~~~~~~~~
- 确定 metaclass.
  The appropriate metaclass for a class definition is determined as follows:

  * if no bases and no explicit metaclass are given, then type() is used

  * if an explicit metaclass is given and it is not an instance of type(),
    then it is used directly as the metaclass

  * if an instance of type() is given as the explicit metaclass, or bases
    are defined, then the most derived metaclass is used

  The most derived metaclass is selected from the explicitly specified metaclass
  (if any) and the metaclasses (i.e. type(cls)) of all specified base classes.
  **The most derived metaclass is one which is a subtype of all of these candidate
  metaclasses. If none of the candidate metaclasses meets that criterion, then
  the class definition will fail with TypeError.**

  例如, 以下代码会失败:

  .. code:: python

    class MetaA(type): pass
    class MetaB(type): pass

    class A(metaclass=MetaA): pass
    class B(metaclass=MetaB): pass

    class C(A, B): pass # TypeError!!!!!

  创建并使用 MetaA 和 MetaB 的共同子类 MetaC 则可以解决这个问题:

  .. code:: python

    class MetaC(MetaA, MetaB): pass

    class C(A, B, metaclass=MetaC): pass

- 调用 ``metaclass.__prepare__`` class method 准备 class namespace (pre-populate
  it), 返回 namespace.

- Execute class body in the created namespace.

- 执行 ``name = metaclass(name, bases, namespace, **kwargs)`` 创建 class object.
  这实际上就是按照正常的实例化流程进行 (metaclass 仍然是 object 的子类, 遵从
  实例化步骤). 调用:

  * ``metaclass.__new__``, 创建 class object.

  * ``metaclass.__init__``, customize class object.

  若任意 method 中包含 ``super``, 过程中创建 implicit ``__class__`` reference,
  指向创建的 class object. 这用于 ``super()``.

metaclass
~~~~~~~~~
指定自定义的 metaclass. 定义 class 时, 在 definition line 中, 使用
``metaclass`` keyword argument 指定 metaclass, 其他 kwargs 则传入
后续一系列流程中.

metaclass 和 class 的关系与 class 和 instance 的关系是类似的.

在 metaclass 定义中, 它的 instance 就是 class, 因此, metaclass 的
instance method 定义第一个参数是 ``cls``, class method 的第一个
参数是 ``metaclass``.

注意 metaclass 仍然是 object 的子类. 遵从一般的逻辑.

methods.

- ``metaclass.__new__(metaclass, name, bases, namespace, **kwargs)``. 
  本质上就是 ``object.__new__``. 不同的是, 在 metaclass 语境下, 第一个
  参数即要实例化的类, 现在变成了 metaclass. 后面的三个参数也是解释器
  自动添加的. kwargs 是在 class definition line 上指定的.

- ``metaclass.__prepare__(metaclass, name, bases, **kwargs)``.
  这是一个 class method. 定义时需要使用 classmethod decorator.
  在上述的 prepare class body namespace 步骤中调用, 返回一个准备好的
  namespace. 返回的应该是一个 MutableMapping instance, e.g. dict,
  OrderedDict.

Expressions
===========

Primaries
---------

Subscriptions & slicing
~~~~~~~~~~~~~~~~~~~~~~~

- subscription
  
  BNF::
      subscription ::= primary "[" expression_list "]"

- slicing
  
  BNF::
      slicing      ::=  primary "[" slice_list "]"
      slice_list   ::=  slice_item ("," slice_item)* [","]
      slice_item   ::=  expression | proper_slice
      proper_slice ::=  [lower_bound] ":" [upper_bound] [ ":" [stride] ]
      lower_bound  ::=  expression
      upper_bound  ::=  expression
      stride       ::=  expression
  
  这是最一般化最广义的 slicing expression 定义. 它是 subscription 的
  generalization. 即: 在 slicing syntax 中, 当 slice_list 中 的每一项 slice_item
  都不包含 proper_slice 的时候, 就是 subscription. 用人话 说, 就是当 ``[a,b,c]``
  中没有 ``:`` 出现时, 就认为是 subscription, 否则就是 slicing.

  当 slice_list 中包含 ``,`` 时, key 是 tuple.
  当 slice_list 中包含 proper_slice 时, proper_slice 部分转化为 slice object.

  e.g.::
      p[1,2,] => p[(1,2)]
      p[1,2:,] => p[(1, slice(2, None, None))]
      p[::2] => p[slice(None, None, 2)]

slicing (包含 subscription) 是通过 ``__getitem__`` 实现.

Exception
=========

- instantiate exception 时, 它的 ``__traceback__``, ``__cause__``, ``__context__``
  还都是 None (因为在实例化处本来就没有这些). 之后 raise 之后, 解释器才会根据执行
  情况设置这三个属性.

builtin functions
=================
注意很多 builtin function 本质上应该看作是该 class 的 constructor.

iteration
---------

- ``enumerate()``, enumerate object constructor. ``start=`` 设置第一项的序号值.

number
------

- ``float()``, float object constructor. 输入是 number, string 或 object.

  对于 string:
  可以包含 leading or trailing whitespace chars;
  可以包含 +/- sign;
  值的部分可以是 ``infinity|inf|nan`` (case-insensitive), 对应正负无穷和 NaN.

  对于 object, ``object.__float__`` method is called.

  无参数时返回 0.0.

scope
-----
- ``vars()``, return ``__dict__`` of any object.
  无参数时, 返回 local dictionary, 即当前 scope 中可以访问到的所有量. 等价于
  ``locals()``.

memory
------

- ``id()``. identity of object. 该值保证为整数, 且在 object 的生命周期中保持
  不变. 在 CPython 中, 用对象的内存地址作为 id. id 值用于 ``is`` operator
  的判断.

inheritance
-----------

- ``super(type, object_or_type=None)``. super object constructor.

  Return a proxy object that delegates attributes access to a parent or sibling
  class of type. 尽管一般用于获取 overrided method, 但必须清楚, super 的作用是
  将 ``getattr`` 的起点拉高到了 parent class 中, 所以 class attribute & method
  都可以获取.

  注意 super class 有自定义的 ``__getattribute__``, 决定属性行为.

  若两个参数都省略, 相当于 ``super(__class__, self)``. 其中 ``__class__``
  是解释器在编译过程中加入的 implicit reference to lexically current class.

  若 second argument is:

  * omitted (None), the super object is unbound. This is
    actually historical and **USELESS**.
    http://www.artima.com/weblogs/viewpost.jsp?thread=236278

  * a subclass ``type2`` of ``type``. 此时, 访问 ``super(type, type2).x``
    给出的是定义在父类中的 function ``x``, 或者说 unbound method ``x``.
    ``type2`` 除了告诉 super object 要返回 unbound function 本身之外,
    没别的作用.

  * a instance ``instance`` of ``type``. 此时, ``super(type, instance).x``
    给出的是 bound method ``x``, bound to ``instance``, i.e. ``self=instance``.

builtin types
=============

text sequence type - str
------------------------

methods
~~~~~~~

- ``isidentifier()``. 检查字符串是否是合法的 python identifier.
  Use ``keyword.iskeyword()`` tests for reserved keywords.

- ``__mod__(arg)``. 字符串的 modulo operation 即 string formatting.
  See `docs <https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting>`_. 对于 ``format % value``:

  * 对于 positional 形式, format 要求的参数必须与 value 部分提供的值一一对应.
    对于 keyword 形式, mapping object 的 keys 可以比 format 中多.

  * If format requires a single argument, values may be a single non-tuple
    object. Otherwise, values must be a tuple with exactly the number of items
    specified by the format string, or a single mapping object.

  * format specifier 形式:

    - ``%``

    - ``(key)`` optional

    - conversion flags: ``#0- +``. optional.

    - minimum field width. optional. can be ``*``.

    - precision. optional. ``.`` + precision number or ``*``.

    - length modifier. optional. ``hlL``, ignored by python.

    - conversion type. ``diouxXeEfFgGcrsa%``.

      * ``r``: ``repr()``

      * ``a``: ``ascii()``

- ``format()``.

  * DNF notation. see
    `docs <https://docs.python.org/3/library/string.html#format-string-syntax>`_.

  * literal ``{}`` ``{{}}``

  * field can be referenced by digit and key index. 对于顺序的 positionals,
    可以 omit digit. 然后可以进一步指定 ``.`` attribute 或 ``[]`` element.

    field name is not quoted.

  * 获取到的值可进一步通过 ``!rsa`` 转换, 以及 ``:`` 进行 formatting.

  * A ``format_spec`` field can also include one-level nested replacement
    fields within it. 形式:

    - DNF::
        [[fill]align][sign][#][0][width][grouping_option][.precision][type]

    - fill can be any char.

    - align: ``<>=^``

    - sign: ``+ -``

    - ``0``. When no explicit alignment is given, preceding the width field by
      a zero ('0') character enables sign-aware zero-padding for numeric types.
      This is equivalent to a fill character of '0' with an alignment type of
      '='.

    - grouping: ``,_`` thousands separator.

    - type: ``sbcdoxXneEfFgGn%gg``.


string formattings
~~~~~~~~~~~~~~~~~~
几种 string interpolation 的方式:

- ``%`` printf-style formatting. 即 modulo operation.
  implemented in ``str.__mod__``.

- ``str.format()``.

- formatting string. ``f"..."``.

- Shell-like string template: ``string.Template``.

set types
---------

operations
~~~~~~~~~~
the non-operator versions methods will accept any iterable as an argument.
In contrast, their operator based counterparts require their arguments to be
sets. 然而两种方式并没有效率上的区别, 因为虽然接受任何 iterable, 但是仍然
会在内部转换成 set 再进行比较.

- ``issubset()``, ``<=``

- ``issuperset()``, ``>=``

- ``union()``, ``set | other | ...``

- ``intersection()``, ``set & other & ...``

- ``difference()``, ``set - other - ...``

- ``symmetric_difference()``, ``set ^ other``

References
==========
.. [PythonFAQ] `Why is Python a dynamic language and also a strongly typed language? <https://wiki.python.org/moin/Why%20is%20Python%20a%20dynamic%20language%20and%20also%20a%20strongly%20typed%20language>`_.
