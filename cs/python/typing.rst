overview
========
- typing module provides tools for specifying function annotations and variable
  annotations.

- See also [pep3107]_, [pep484]_, [pep526]_.

Type definition syntax
======================
acceptable type hints
---------------------
- any classes.

- Any alias to classes.

- valid expressions that evaluate without raising exceptions.

- special constructs: None, Any, Union, Tuple, Callable, all ABCs and stand-ins
  for concrete classes exported from typing (e.g. Sequence and Dict), type
  variables, and type aliases.

  * None when used in a type hint, is considered equivalent to ``type(None)``.

type aliases
------------
- Make aliases to generic types, to express intention more preciously.

- Alias should be capitalized, because it represents a class.

- Generic types can be aliased, the alias accepts type parameters in the
  same way as the original generic type.::

    MyMap = Mapping[str, T]
    MyMap[int] # equivalent to Mapping[str, int]

subtype
-------
- ``NewType(name, type)`` function indicates to a typechecker a subtype of the
  original ``type``.  At runtime it returns an identity function. Note that
  this does NOT create an actual subtype, 它只对 static type checker 有效.

callable
--------
- Specifying the signature of a callable object::

    Callable[[argType, argType, ...], ReturnType]

  To omit the parameter signature, but declare the return type, use::

    Callable[..., ReturnType]

- ``Callable`` is also an ABC, similar to collections.abc.Callable.

Generic types
-------------
- User defined generic types are defined as::

    Generic[<params>]

  It can be used as base class for concrete class definition. 这样定义的
  subclass 除了可正常使用之外, 还可用在 type annotation 中, 与 base generic
  class 相同, 指定接收的 ``<params>`` 参数.

  .. code:: python

    class SomeType(Generic[T]):
      # class definitions
      pass

    def (a: SomeType[int]):
      pass

- ``<params>`` is a comma separated list of type parameters, all must be
  unique. 这是因为在定义 generic type 时, 每个 generic 参数作为抽象标识符, 必
  须是可分辨的. 这不代表根据 generic type 具体化的某个 type 的具体参数类型必须
  unique.

- Using a generic class without specifying type parameters assumes Any for each
  position.

Generic containers
------------------
- Generic containers are also generic types.

- Generic containers 形式上类似 Generics in Java. 用于指定 container 参数的类型.
  support subscription to denote expected types for container elements.::

    Mapping[str, int]
    Sequence[dict]

- pre-defined generic container classes: Mapping, Sequence, Set, List,

The Any type and object type
----------------------------
- Use object to indicate that a variable could be any type in a typesafe
  manner.  Use Any to indicate that a variable is dynamically typed.

Any
^^^
- A static type checker will treat every type as being compatible with Any (从
  而任何值可赋值给 Any type 的量), and Any as being compatible with every type
  (从而类型为 Any 的量可赋值给任何类型的变量.)

- function/variable without annotations should be treated as having the most
  general type possible.  Specifically,
  
  * When annotation is unspecified, the default annotation for arguments and
    for the return type is Any, except for the first argument of instance and
    class methods.

  * When annotation is unspecified, the annotation of a variable is also Any.

object
^^^^^^
- Similar to Any, every type is a subtype of object. However, unlike Any, the
  reverse is not true: object is not a subtype of every other type.

- That means when the type of a value is object, a type checker will reject
  almost all operations on it (because object has no public method), and
  assigning it to a variable (or using it as a return value) of a more
  specialized type is a type error.

References
==========
.. [pep3107] `PEP 3107 -- Function Annotations <https://www.python.org/dev/peps/pep-3107/>`_
.. [pep484] `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_
.. [pep526] `PEP 526 -- Syntax for Variable Annotations <https://www.python.org/dev/peps/pep-0526/>`_
