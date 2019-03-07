Overview
========
- typing module provides tools for specifying function annotations and variable
  annotations.

- Most of the constructs in this module aim to provide utilities for type
  checking, and interpreted by a type checker, rather than to be useful at
  runtime.

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

Type object annotation
----------------------
- ``Type``. A special construct useful to annotate class objects. 注意一般情况
  下, ``var: int`` 指的是 var 是 int 实例, 若要指定 var 是 int class object,
  可使用 ``Type[int]``.

subtype
-------
- ``NewType(name, type)`` function indicates to a typechecker a subtype of the
  original ``type``.  At runtime it returns an identity function. Note that
  this does NOT create an actual subtype, 它只对 static type checker 有效.

type variable definition
------------------------
- ``TypeVar(name, *constraints, bound=None, covariant=False, contravariant=False)``.
  定义 type variable. 这是一个 generic type.

  name 是变量名 (必须与被赋值 identifier 相同), constraints 是允许的 concrete
  types (必须有至少 2 个 constraints), type variable 必须是 constraints 规定的
  类型, 不能是子类; bound 是允许的类型的 upper boundary, 也就是说允许的
  concrete type 必须是 subtype of the boundary type; constraints 和 bound 两者
  只能指定一个; covariant 和 contravariant 只能有一个是 True, 意义见下.
  
  usage:
  
  * 用于对 generic function 的参数和返回值等进行注释
   
  * 对 variable 进行注释

  * 作为 Generic types 中的 type variable.

- A ``TypeVar()`` expression must always directly be assigned to a variable.
  一般是 type checker 去使用这个信息. At runtime, ``isinstance(x, T)`` will
  raise TypeError.

- A type variable used in a method of a generic class that coincides with one
  of the variables that parameterize this class is always bound to that
  variable. (For the type checker)

- A generic class definition that appears inside a generic function should not
  use type variables that parameterize the generic function.

- A generic class definition that appears inside a generic function should not
  use type variables that parameterize the generic function.

- A generic class nested in another generic class cannot use the same type
  variables.

callable
--------
- Specifying the signature of a callable object::

    Callable[[argType, argType, ...], ReturnType]

  To omit the parameter signature, but declare the return type, use::

    Callable[..., ReturnType]

- ``Callable`` is also an ABC, similar to collections.abc.Callable.

Generic types
-------------
- ``Generic``. ABC for generic types.

- User defined generic types is typically declared by inheriting from an
  instantiation of this class with one or more type variables.::

    class GenericKlass(Generic[<params>]):
      pass

  这样定义的 subclass 除了可用在 type annotation 中之外, 还可以正常在 runtime
  实例化. 它接收的 type variables 与 base generic class 相同, 即 ``<params>``
  参数.

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

- The metaclass used by Generic is a subclass of abc.ABCMeta. A generic class
  can be an ABC by including abstract methods or properties, and generic
  classes can also have ABCs as base classes without a metaclass conflict.

- Generic ABC can be used in multiple inheritance, 从而引入一些其他 ABC 的行为.

  .. code:: python

    class MyMapping(Iterable[Tuple[K, V]], Container[Tuple[K, V]], Generic[K, V]):
      pass

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
  这些 generic container class 同时也是 ABC, 地位类似于 collections.abc 里面那
  些.

covariance and contravariance
-----------------------------
A generic type ``GenType`` defined using a type variable can be covariant or
contravariant. For a subtype t2 of type t1,

* GenType is covariant, if ``GenType[t2]`` is subtype of ``GenType[t1]``.

* GenType is contravariant, if ``GenType[t2]`` is supertype of ``GenType[t1]``.

* GenType is invariant, if neither of the above is true.


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

Utilities
=========
References
==========
.. [pep3107] `PEP 3107 -- Function Annotations <https://www.python.org/dev/peps/pep-3107/>`_
.. [pep483] `PEP 483 -- The Theory of Type Hints <https://www.python.org/dev/peps/pep-0483/>`_
.. [pep484] `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_
.. [pep526] `PEP 526 -- Syntax for Variable Annotations <https://www.python.org/dev/peps/pep-0526/>`_
