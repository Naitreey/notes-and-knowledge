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

class instance
~~~~~~~~~~~~~~

* attribute reference.
  
  搜索顺序. 首先搜索 instance ``__dict__``, 然后搜索 class & parent
  classes attributes, in MRO order. 注意不会去搜索 metaclass 的 attributes.
  
  即对于 class instance, 搜索是
  ``instance -> class -> parent class -> ... -> object``
  对于 class object (metaclass instance), 搜索是
  ``class -> metaclass -> parent metaclass -> ... -> type -> object``
  这两条线是平行的.

  若属性是一个 function object, 转变成 bound instance method, 它的
  ``__self__`` attribute is the instance.

  若最终没找到, call ``__getattr__``.

* attribute modification. 修改和删除属性只更新 ``__dict__``. 若
  定义了 ``__setattr__``, ``__delattr__`` 则直接调用这两个方法.

special attributes & methods
----------------------------

general objects:

- ``object.__dict__``. 一个对象自身存储的属性.

- ``object.__new__(cls, ...)``. static method. 实例化时
  调用该方法创建 ``cls`` 的新实例. 剩下的参数定义就是 constructor 的参数
  signature. 返回 new object instance.

- ``object.__init__(self, ...)``. Must return None.

class instances:

- ``instance.__class__``. the class of the instance.

class, function-like definitions, generator instance (including those from
generator functions and generator expressions), and module:

- ``definition.__name__``. the name of definition. for module, the qualified
  import path of module.

- ``definition.__qualname__``. the qualified name of definition.
  这是 the “path” from a module’s global scope to the object. module object
  没有这个属性.

class:

- ``class.__bases__``. 一个类定义时使用的直接父类. 不包含 MRO resolved result.

- ``class.__mro__``. class 的 MRO order. It is considered when looking for base
  classes during MRO.

- ``class.mro()`` 该方法不是定义在 class 上的, 而是定义在 metaclass 上的. 所以
  在 class 中是作为 instance method 方式调用. 在生成 class object 时, 计算
  MRO order 并存储在 ``class.__mro__`` 中. 由于在 metaclass 上定义, 在 instance
  中不可见.

- ``class.__subclasses__()``. 一个类的所有现存子类. 通过 weakref 保存关系.

instance methods:

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
----------------

descriptor protocol
~~~~~~~~~~~~~~~~~~~
Descriptors are a powerful, general purpose protocol. They are the mechanism
behind properties, methods, static methods, class methods, and super(). They
are used throughout Python itself to implement the new style classes introduced
in version 2.2. Descriptors simplify the underlying C-code and offer a flexible
set of new tools for everyday Python programs.

descriptor 的效果是一个对象以不同的方式去访问它, 得到的是不同的结果.
descriptor object ``x`` 出现在某个 owner class ``A`` 的定义中, 成为这个类的
attribute. 当获取这个 attribute 时 (``a.x``, ``A.x``, ``super().x``, or whatever)
python 发现这个 attribute 实际上是 descriptor, 不会直接返回这个 descriptor,
而是进一步执行 descriptor 的 ``__get__``, ``__set__`` 或 ``__delete__`` method
来完成操作.

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

builtin types
=============

set types
---------

operations
~~~~~~~~~~
- the non-operator versions of ``union()``, ``intersection()``,
  ``difference()``, and ``symmetric_difference()``, ``issubset()``, and
  ``issuperset()`` methods will accept any iterable as an argument. In
  contrast, their operator based counterparts require their arguments to be
  sets. 然而两种方式并没有效率上的区别, 因为虽然接受任何 iterable, 但是仍然
  会在内部转换成 set 再进行比较.
