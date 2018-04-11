extension class
===============

- multi-inheritance issue. 一个 class 往往不能继承多个 builtin type 或
  extension class. 此时会报错::

    class x(dict, list): pass

    TypeError: multiple bases have instance lay-out conflict

  这是因为每个 C 实现的类型的 struct layout is fixed. 因此这种冲突
  无法解决.
