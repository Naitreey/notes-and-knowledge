overview
========
主要两个功能:

- ``recursive_repr`` decorator. 检测 recursive ``repr()`` 调用, 避免死循环.
  如果一个类的 repr 可能发生递归调用, 可应用这个 decorator.

- ``Repr`` class. alternative ``repr`` implementations that limit the verbosity
  of object's representation.

  * this class implements repr methods for builtin container types, str and int
    type.

  * subclass can add additional methods to handle repr of extra types.

convenience function:

- ``repr()``. repr method of a ``Repr`` instance.
