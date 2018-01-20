Data model
==========

The standard type hierarchy
---------------------------
包含对一系列类型概念的标准陈述.

- class instance.

  * attribute reference.
    
    搜索顺序. 首先搜索 instance ``__dict__``, 然后搜索 class & parent
    classes attributes, in MRO order.

    若属性是一个 function object, 转变成 bound instance method, 它的
    ``__self__`` attribute is the instance.

    若最终没找到, call ``__getattr__``.

  * attribute modification. 修改和删除属性只更新 ``__dict__``. 若
    定义了 ``__setattr__``, ``__delattr__`` 则直接调用这两个方法.

special methods
---------------

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

