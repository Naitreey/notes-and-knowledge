type
====
- It is generally considered more readable to declare the type of members
  exposed in a public API. Do not rely on type inference when defining public
  APIs.

- Sometimes the inferred type can be too specific that it prevent the variable
  to be useful in the following code. In those cases, declare types explicitly.

  .. code::

    var x = null
    x = 1  // do not compile

method call
===========
- keyword argument parameter binding syntax, 与 python 的风格不同, 这里 ``=``
  两边应该各空一格::

    func(a = 1, b = 2)
