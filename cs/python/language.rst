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
