Overview
========
- ``typing`` module and ``typing_extensions`` modules provides tools for
  specifying function annotations and variable annotations.

- Most of the constructs in this module aim to provide utilities for type
  checking, and interpreted by a type checker, rather than to be useful at
  runtime.

- See also [pep3107]_, [pep483]_, [pep484]_, [pep526]_, [pep563]_.

why type annotation and checking
================================
- type annotation makes it possible for static type checking of python program,
  which in turn makes it easier to find bugs at earlier stages of development,
  so that it's easier to fix bug, with less cost, less debugging, etc.

- type annotation serves as an machine-checked documentation of interfaces.

- Static typing makes it practical to build very useful development tools that
  can improve programming productivity or software quality, including IDEs with
  precise and reliable code completion, static analysis tools, etc.

- 注意, type annotation 并没有让 python 失去 dynamic typing 的灵活性. 实际上,
  类型注释 combined the power of dynamic typin and static typing. 这是因为, 一
  些注释的类型不过是 interface (例如 Sized, Awaitable, 不过是要求具有某些
  special methods), 这样不但保持了 python 原有的 dynamic typing 特性, 还更准确
  地说明了对参数的要求是什么.

- With type annotation, fully dynamic typed code and static type-annotated code
  can live together. Use static typing when it makes sense. There's no need to
  be fully statically-typed.

Type definition syntax
======================
type
----
- A type is a set of values and a set of functions that can be applied to these
  values.

subtype relationship
--------------------
Type B is a subtype of type A, if and only if the following two criteria holds:

- every value from B is also a value from A

- every function that can be applied to A can also be applied to B

- additional rules about Any.

  * Any is consistent with every type. (But Any is not a subtype of every
    type.)

  * Every type is consistent with Any. (But every type is not a subtype of
    Any.)

这些标准导致的一些现象:

- List[int] is not a subtype of List[float], Because: The first condition of
  subtyping holds, but appending a float only works with List[float].

- this places Any partially at the top (it has all values) and bottom (it has
  all methods) of the type hierarchy.

types vs clases
---------------
- In Python, class is object factory. it's a dynamic, runtime concept. Used
  by interpreter.

- Type appear in variable and function type annotation. it's a static, author
  time concept. Used by static type checker.

- static types described in PEP 484, should not be confused with the runtime
  classes.

- 构成一个 type 的所有元素不一定是同一个 class 的实例.

- subtype 不一定是 subclass, subclass 也不一定是 subtype.

- Except for non-abstract subclasses of ``Generic``, no types can be
  instantiated.

- Except for ``Generic`` and its subclasses, no types can be subclassed.

- Except for unparameterized generics, all types will raise TypeError if used
  in isinstance or issubclass.

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

- Generic type aliases.

  * Subscripted aliases are equivalent to original types with substituted type
    variables, so the number of type arguments must match the number of free
    type variables in the generic type alias.
    
  * Unsubscripted aliases are treated as original types with free variables
    replaced with Any.

Type object annotation
----------------------
- ``Type``. A special construct useful to annotate class objects. 注意一般情况
  下, ``var: int`` 指的是 var 是 int 实例, 若要指定 var 是 int class object,
  可使用 ``Type[int]``.

- ``Type[C]`` refers to the subclasses of C.

- it is legal to use a Union of classes as the parameter for Type[].

- Plain Type without brackets is equivalent to Type[Any] and this in turn is
  equivalent to type.

- Type[T] where T is a type variable is allowed when annotating the first
  argument of a class method.

- Any other special constructs like Tuple or Callable are not allowed as an
  argument to Type.

- Type is covariant in its parameter. This implies that all subtypes of C
  should implement the same class method signatures as C.

type variable
-------------
- ``TypeVar(name, *constraints, bound=None, covariant=False, contravariant=False)``.
  定义 type variable.

  name 是变量名 (必须与被赋值 identifier 相同), constraints 是允许的 concrete
  types (必须有至少 2 个 constraints), type 必须是 constraints 规定的类型,
  subclasses of the constrained types are allowed, but replaced by the
  most-derived base class among t1, etc.; bound 是允许的类型的 upper boundary,
  也就是说允许的 concrete type 必须是 subtype of the boundary type; constraints
  和 bound 两者只能指定一个; covariant 和 contravariant 只能有一个是 True, 意义
  见 `covariance and contravariance`_.
  
  usage:
  
  * 用于对 generic function 的参数和返回值等进行注释
   
  * 作为 Generic types 中的 type variable.

  * upper bound 可用于定义 decorator that preserves the signature of the
    function it decorates.

    .. code:: python

      FuncType = Callable[..., Any]
      F = TypeVar('F', bound=FuncType)
      
      # A decorator that preserves the signature.
      def my_decorator(func: F) -> F:
          def wrapper(*args, **kwds):
              print("Calling", func)
              return func(*args, **kwds)
          return cast(F, wrapper)

- A ``TypeVar()`` expression must always directly be assigned to a variable.
  一般是 type checker 去使用这个信息. At runtime, ``isinstance(x, T)`` will
  raise TypeError.

- 对一个 generic function 进行注释时, 多处出现的同一个 type variable is always
  bound to the same concrete type.

- 使用 type variable 定义 generic type 时, 多处出现的同一个 type variable is
  always bound to the same concrete type.

- A type variable used in a method of a generic class that coincides with one
  of the variables that parameterize this class is always bound to that
  variable. (For the type checker)

- A generic class definition that appears inside a generic function should not
  use type variables that parameterize the generic function.

- A generic class definition that appears inside a generic function should not
  use type variables that parameterize the generic function.

- A generic class nested in another generic class cannot use the same type
  variables.

Generic types
-------------
- Generic type constructor: takes a type and "returns" a type.

- Generic type: Classes, that behave as generic type constructors are called
  generic types.  A generic type when given concrete types as type arguments,
  returns a concrete type.

  * Tuple, Callable, Mapping, etc. 都是 generic types.

  * ``Generic`` is ABC for defining generic type class.

- User defined generic types is declared by inheriting from an instantiation of
  Generic abstract type with one or more type variables.::

    class GenericKlass(Generic[<params>]):
      pass

  The previous code defines a generic type GenericKlass over type variables
  ``<params>``. GenericKlass itself becomes parameterizable.

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

- If Generic appears in the base class list, then it should contain all type
  variables needed by the generic type, and the order of type parameters is
  determined by the order in which they appear in Generic. If there are no
  ``Generic[...]`` in immediate bases, then all type variables are collected in
  the lexicographic order (i.e. by first appearance).

- The metaclass used by Generic is a subclass of abc.ABCMeta. A generic class
  can be an ABC by including abstract methods or properties, and generic
  classes can also have ABCs as base classes without a metaclass conflict.

- Classes that derive from generic types become generic. A class can subclass
  multiple generic types, 从而引入一些其他 ABC 的行为. However, classes derived
  from specific types returned by generics are not generic.

  .. code:: python

    class MyMapping(Iterable[Tuple[K, V]], Container[Tuple[K, V]], Generic[K, V]):
      pass

- Using a generic class without specifying type parameters assumes Any for each
  position. Such form could be used as a fallback to dynamic typing.

- During runtime, the type of an instance of an indexed generic type (i.e. a
  concrete type) is the generic type itself. The concrete type itself can not
  be used in ``isinstance()`` check.::

    class A(Generic[T]):
      pass

    a = A[int]()
    isinstance(a, A) # True

  This can be seen as the type variables are erased at runtime.

Generic containers
------------------
- Generic containers are also generic types.

- Generic containers 形式上类似 Generics in Java. 用于指定 container 参数的类型.
  support subscription to denote expected types for container elements.::

    Mapping[str, int]
    Sequence[dict]

pre-defined generic classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Everything from collections.abc, 它们仍然是 ABC, 但是作为 generic types,
  注意原来的 Set renamed to AbstractSet. 因为 Set 要留给 set.

  * ``Iterable[T_co]``

  * ``Iterator[T_co]``

  * ``Reversible[T_co]``

  * ``Container[T_co]``

  * ``Hashable``, not generic

  * ``Sized``, not generic

  * ``Collection[T_co]``

  * ``AbstractSet[T_co]``

  * ``MutableSet[T]``

  * ``Mapping[KT, VT_co]``, note only covariant in value.

  * ``MutableMapping[KT, VT]``

  * ``Sequence[T_co]``

  * ``MutableSequence[T]``

  * ``ByteString``, not generic, ABC for bytes, bytearray, memoryview.

  * ``MappingView[T_co]``

  * ``KeysView[KT_co]``

  * ``ValuesView[VT_co]``

  * ``ItemsView[KT_co, VT_co]``

  * ``Awaitable[T_co]``

  * ``Coroutine[T_co, T_contra, V_co]``, type variables for types of yield,
    send, return.

  * ``Generator[T_co, T_contra, V_co]``, type variables for types of yield,
    send, return. send and/or return types can be None, if no need for send
    and/or return.

    Alternatively, annotate your generator as having a return type of either
    ``Iterable[YieldType]`` or ``Iterator[YieldType]``.

  * ``AsyncGenerator[T_co, T_contra]``. for yield and send types. Send type
    can be None, like above. Or alternatively, annotate your generator as
    having a return type of either ``Iterable[YieldType]`` or
    ``Iterator[YieldType]``.

  * ``AsyncIterable[T_co]``

  * ``AsyncIterator[T_co]``

- ``Dict[KT, VT]``, ``DefaultDict[KT, VT]``, ``OrderedDict[KT, VT]``,
  ``List[T]``, ``Set[T]``, ``FrozenSet[T_co]``, ``Deque[T]``,
  ``ContextManager[T_co]``, ``AsyncContextManager[T_co]``, ``Counter[T]``,
  ``ChainMap[KT, VT]``, ``IO[AnyStr]``, ``TextIO``, ``BinaryIO``,
  ``Pattern[AnyStr]``, ``Match[AnyStr]``

- The readonly collection classes are all declared covariant in their type
  variables.

- The mutable collection classes are declared invariant.

covariance and contravariance
-----------------------------
- A generic type ``GenType`` defined using a type variable can be covariant or
  contravariant. If t2 is a subtype of t1, then a generic type constructor
  GenType is:

  * covariant, if ``GenType[t2]`` is subtype of ``GenType[t1]``, for all such
    t1 and t2.

  * contravariant, if ``GenType[t2]`` is supertype of ``GenType[t1]``, for all
    such t1 and t2.

  * invariant, if neither of the above is true.

- common type's variance property:

  * Union is covariant in all its arguments.
  
  * FrozenSet is covariant.
  
  * List is invariant. 虽然两个集合符合子集关系, ``List[T1]`` 可以 append T1 元
    素, ``List[T2]`` 不能 append T1 元素. Mutable types are typically
    invariant.
  
  * Callable is covariant in the return type, but contravariant in the
    parameter types.
  
    - covariant 的部分很容易理解.
  
    - contravariant 的部分的解释如下: 允许的参数值越广, 对函数的限制越强, 因此,
      ``Callable[[t2], None]`` 所包含的可能函数要比 ``Callable[[t1], None]`` 更
      少.  具体来说, 如果一个函数允许任意 t1 类型的参数值, 它当然允许 t2 类型的
      参数值, 即一个 ``Callable[[t1], None]`` 的函数可以替代 ``Callable[[t2],
      None]`` 的函数; 反之越不然.
  
      This shows how to make more precise type annotations for functions:
      choose the most general type for every argument, and the most specific
      type for the return value. 这其实就是 axiomatic semantics 中的 the rule
      of consequence 所表达的思想.

- To declare the variance for user defined generic types, use ``covariant`` and
  ``contravariant`` kwargs of type variables being used. User defined generic
  types are invariant by default.

  By convention, type variable with ``covariant=True`` or
  ``contravariant=True`` should be named with ``_co`` or ``_contra`` suffix.

  Covariance or contravariance is not a property of a type variable, but a
  property of a generic class defined using this variable. Variance is only
  applicable to generic types; generic functions do not have this property.
  Generic function's annotation should not use type variables with variance
  defined.

Any type and object type
------------------------
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

Union
-----
- Types that are subtype of at least one of types in the Union are subtypes of
  the Union::

    Union[t1, t2, ...]

- Unions whose components are all subtypes of a Union's types are subtypes of
  this Union. E.g., ``Union[int, str]`` is subtype of ``Union[int, float, str]``.

- If ti in a Union is itself a Union, the type is flattened.::

    Union[Union[int, float], str] == Union[int, float, str]

- If ti and tj in Union have a subtype relationship, it's equivalent to a Union
  with only the less specific type.::

    Union[int, float] == Union[float]
    Union[..., object, ...] == Union[object] == object

- ``Union[t]`` is just ``t``.

- Duplicate types in Union are skipped::

    Union[int, str, int] == Union[int, str]

Tuple
-----
- A tuple whose items are instances of ti types.::

    Tuple[t1, t2, ...]

- ``Tuple[u1, u2, ..., um]`` is a subtype of ``Tuple[t1, t2, ..., tn]`` if they
  have the same length n==m and each ui is a subtype of ti.

- Type of empty tuple: ``Tuple[()]``

- A variadic homogeneous tuple type can be written ``Tuple[t1, ...]``.

callable
--------
- Specifying the signature of a callable object::

    Callable[[argType, argType, ...], ReturnType]

  To omit the parameter signature, but declare the return type, use::

    Callable[..., ReturnType]

- ``Callable`` is also an ABC, similar to collections.abc.Callable.

- There is no way to indicate optional or keyword arguments, nor varargs; such
  function types are rarely used as callback types.

- A bare Callable as annotation is equivalent to::

    Callable[..., Any]

type or None
-------------
- A value of a type, or None.::

    Optional[t] == Union[t, None] == Union[t, type(None)]

numeric tower
-------------
- ABCs in numbers module can be used.

- Variance is only applicable to generic types; generic functions do not have
  this property.

- For type checking, ``float`` is a subtype of ``complex``, and ``int`` is a
  subtype of ``float``.

NoReturn type
-------------
useful to annoatate a function's return value, when the function never returns
normally. E.g., when a function raises exception unconditionally.

The NoReturn type is only valid as a return annotation of functions, and
considered an error if it appears in other positions

singleton as annotation
-----------------------
python 中 singleton 有多种实现方式, 为了限制 singleton 参数的类型,
应该使用 class 去定义 singleton.

annotating instance and class methods
-------------------------------------
- In most cases the first argument of class and instance methods does not need
  to be annotated, and it is assumed to have the type of the containing class
  for instance methods, and a type object type corresponding to the containing
  class object for class methods.

annotating args and kwargs
--------------------------
- For ``*args`` in function signature, annotate the type of each element in the
  tuple.::

    def f(*args: int):
      pass

  在函数内部, args 类型成为 ``Tuple[int, ...]``

- For ``*kwargs`` in function signature, annotate the value of each key in the 
  dict, 注意到 key 必然是 str, 无需注释.::

    def f(**kwargs: int):
      pass

  在函数内部, kwargs 类型成为 ``Dict[str, int]``.

Annotating generator functions and coroutines
---------------------------------------------
- the return type of a generator function is Generator, annotate it with the
  following::

    Generator[yield_type, send_type, return_type]

  注意 Generator type is covariant in ``yield_type`` and ``return_type``;
  contravariant in ``send_type``.

- Coroutines are annotated with the same syntax as ordinary functions.  The
  return type annotation corresponds to the type of await expression, not to
  the coroutine type.

- ``Coroutine`` generic type should be used to annotate coroutine object.::

    Coroutine[yield_type, send_type, return_type]

  注意 Coroutine type is covariant in ``yield_type`` and ``return_type``;
  contravariant in ``send_type``.

  ``Coroutine`` generic type is a subtype of ``Awaitable[T]``.

- More abstract generic ABCs: Awaitable, AsyncIterable, AsyncIterator.

Typed NamedTuple
----------------
- ``NamedTuple``, a typed version of namedtuple. The resulting class has extra
  attributes:

  * ``__annotations__``

  * ``_fields``, a tuple of field names.
   
  * ``_field_types``, an ordered dict mapping field names to types
   
  * ``_field_defaults``, a dict mapping field names to default values.

  Fields with a default value must come after any fields without a default. 用
  法:

  .. code:: python

    class Employee(NamedTuple):
        name: str
        id: int = 3

    # or
    Employee = NamedTuple('Employee', name=str, id=int)

    # or
    Employee = NamedTuple('Employee', [('name', str), ('id', int)])

IO types
--------
以下仅用于 annotation

- ``IO[AnyStr]`` generic type

- ``BinaryIO``, subtype of ``IO[bytes]``.

- ``TextIO``, subtype of ``IO[str]``

regular expresion types
-----------------------
以下是 generic type, actual classes.

- ``Pattern[AnyStr]``

- ``Match[AnyStr]``

class and instance attribute annotations
----------------------------------------
- class and instance attributes can be annotated in class scope.

- Use ``ClassVar[T_co]`` to mark class variable, otherwise it's instance
  variable.  这倒是提供了一个好方法来清晰分辨哪些是 class attribute, 哪些是提供
  了默认值的 instance attribute.

- ``ClassVar[T_co]`` accepts only types as argument, the type argument can not
  include any type variables.

- ``ClassVar`` generic type is covariant.

- instance variables can be annotated in ``__init__`` or other methods, rather
  than in the class. But they won't be processed at runtime nor will they be
  saved in ``__annotations__``.

forward references
------------------
- 默认情况下, type annotations are evaluated at module import time, 这样如果一
  个 module level annotation 中要引用下面才定义的全局对象, 就会造成 NameError.
  此时, 解决办法是使用 string literal form of annotation. 这样的 annotation
  type checker 会识别. 若在 runtime 需要使用 annotation, 使用
  ``get_type_hints()`` 会将 string form 解析成真实的 reference.

  这种 evaluation at import time 的 annotation will be deprecated at
  python3.8+. 所有 type annotation 都应该使用下述的 postponed 模式.

- 由于涉及 forward reference 的 annotation 需要程序员去识别并转换成 string
  form, 比较繁琐. python3.7 引入了 postponed evaluation of annotation 机制,
  作为 optional ``__future__`` feature. (Enforced at python4.0)::

    from __future__ import annotations

  Function and variable annotations will no longer be evaluated at definition
  time. Instead, a string form will be preserved in the respective
  ``__annotations__`` dictionary. Static type checkers will see no difference
  in behavior.

  The string form is obtained from the AST during the compilation step, which
  means that the string form might not preserve the exact formatting of the
  source. Note: if an annotation was a string literal already, it will still be
  wrapped in a string (which makes it a double string...).

  To resolve the annotations at runtime, ``get_type_hints()`` can be used as
  before.

  注意, 在 postponed evaluation of annotation 时, 由于不在 import time 运算
  annotations, using local state in annotations is no longer possible in
  general. 只有 global state can be used reliably. 例如:

  .. code:: python

    def generate():
        A = Optional[int]
        class C:
            field: A = 1
            def method(self, arg: A) -> None: ...
        return C

    X = generate()

  type alias A is local, trying to resolve annotations of X will fail.

- Forward references in other typing areas is not addressed by the postponed
  evaluation scheme. This involves all constructs where a type object is
  required:

  * type variable definition

  * new type definition

  * Type aliases

  * type casting

  * generic types as base class

  Depending on the specific case, some of the cases listed above might be
  worked around by placing the usage in a if TYPE_CHECKING: block. 
 
mark ignore type checking
-------------------------
- ``# type: ignore`` comment. should be put on the line that the error refers
  to. A ``# type: ignore`` comment on a line by itself means to ignore type
  checking for the rest of current indented block. If used at top indentation
  level, the rest of the file is not type-checked.

  In some cases, linting tools or other comments may be needed on the same line
  as a type comment. In these cases, the type comment should be before other
  comments and linting markers.

- ``no_type_check`` decorator. prevent class or function from being
  type-checked, indicating that annotations (if exists) are not type hints.

  With a class, it applies recursively to all methods defined in that class
  (but not to methods defined in its superclasses or subclasses).

- ``no_type_check_decorator`` gives the wrapped class or function decorator
  the ability to prevent type checking.

declaring multiple variable types at a time
-------------------------------------------
To declare types of multiple variables at once, only type comment can be used.

.. code:: python

  i, found = 0, False # type: int, bool
  p, q, *rs = 1, 2 # type: int, int, List[int]

Protocols and structural subtyping
----------------------------------
Mypy provides support for both nominal subtyping and structural subtyping.

* Nominal subtyping is strictly based on the class hierarchy. B is a subtype of
  A if B is a subclass of A. Instance of B can be used when instances of A are
  expected (principle of substitution).

* Structural subtyping is based on the structure of classes. B is a subtype of
  A if the former has all attributes and methods of the latter, and with
  compatible types. B need not be a subclass of A.

Structural subtyping can be thought of as “static duck typing”.

一些类型实际上是 interface 定义, type checker 只需检查 actual parameter 的类型
是否满足 interface 即可, 而不去判断是否是子类实例.

pre-defined protocols
^^^^^^^^^^^^^^^^^^^^^
- iterable protocol ``Iterable[T]``.

  .. code:: python

    def __iter__(self) -> Iterator[T]

- iterator protocol ``Iterator[T]``.

  .. code:: python

    def __next__(self) -> T
    def __iter__(self) -> Iterator[T]

- async iterable protocol ``AsyncIterable[T]``

  .. code:: python

    def __aiter__(self) -> AsyncIterator[T]

- async iterator protocol ``AsyncIterator[T]``

  .. code:: python

    def __aiter__(self) -> AsyncIterator[T]
    def __anext__(self) -> Awaitable[T]

- awaitable protocol ``Awaitable[T]``

  .. code:: python

    def __await__(self) -> Generator[Any, None, T]

- sized protocol ``Sized``.

  .. code:: python

    def __len__(self) -> int

- container protocol ``Container[T]``.

  .. code:: python

    def __contains__(self, x: object) -> bool

- collection protocol ``Collection[T]``.

  .. code:: python

    def __len__(self) -> int
    def __contains__(self, x: object) -> bool
    def __iter__(self) -> Iterator[T]

- reversible protocol ``Reversible[T]``.

  .. code:: python

    def __reversed__(self) -> Iterator[T]

- supports abs protocol ``SupportsAbs[T]``.

  .. code:: python

    def __abs__(self) -> T

- supports bytes protocol ``SupportBytes``.

  .. code:: python

    def __bytes__(self) -> bytes

- supports complex protocol ``SupportsComplex``.

  .. code:: python

    def __complex__(self) -> complex

- Supports float protocol ``SupportsFloat``.

  .. code:: python

    def __float__(self) -> float

- supports int protocol ``SupportsInt``.

  .. code:: python

    def __int__(self) -> int

- supports round protocol ``SupportsRound[T]``

  .. code:: python

    def __round__(self) -> T

- context manager protocol ``ContextManager[T]``

  .. code:: python

    def __enter__(self) -> T
    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]

- async context manager protocol ``AsyncContextManager[T]``

  .. code:: python

    def __aenter__(self) -> Awaitable[T]
    def __aexit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Awaitable[Optional[bool]]

user-defined protocol
^^^^^^^^^^^^^^^^^^^^^
- define protocol by inheriting ``typing_extensions.Protocol``, and define the
  interface methods.

- Protocols can be extended and merged using multiple inheritance. Note that
  inheriting from an existing protocol does not automatically turn the subclass
  into a protocol – it just creates a regular (non-protocol) class or ABC that
  implements the given protocol (or protocols). The ``Protocol`` base class
  must always be explicitly present if you are defining a protocol

- The interface stub methods need full annotation, function body 可以是 ``...``
  placeholder, 或者 defult implementation (只有明确继承 Protocol 才有用).

- type checker 会根据实际值的类型是否与 annotation 定义的 protocol 相符, 来判断
  是否满足 structural subtyping.

- Explicitly including a protocol as a base class is also a way of documenting
  that your class implements a particular protocol, and it forces the type
  checker to verify that your class implementation is actually compatible with
  the protocol.

runtime protocol check
^^^^^^^^^^^^^^^^^^^^^^
Predefined protocols and user-defined protocols decorated with
``typing_extensions.runtime`` class decorator can be checked at runtime,
using ``isinstance()``.

``isinstance()`` with protocols is not completely safe at runtime. For example,
signatures of methods are not checked. The runtime implementation only checks
that all protocol members are defined.

define callback types using protocol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Protocols can be used to define flexible callback types that are hard (or
  even impossible) to express using the ``Callable[...]`` syntax, such as
  variadic, overloaded, and complex generic callbacks. They are defined with a
  special ``__call__`` member.

- Callback protocols and ``Callable[...]`` types can be used interchangeably.

generic protocol
^^^^^^^^^^^^^^^^
- ``Protocol`` can be parametrized like ``Generic``, to form a generic
  protocol.

- Protocol's can be invariant, covariant, contravariant. A Type checker checks
  that the declared variances of generic type variables in a protocol match how
  they are used in the protocol definition. 

new type
--------
- ``NewType(name, type)`` function indicates to a typechecker a subtype of the
  original ``type``.   Note that this does NOT create an actual subtype, 它只对
  static type checker 有效.

  ``name`` is new type's name; ``type`` should be a proper class.  At runtime
  it returns an identity function, which accepts a value of the ``type``.

- useful for creating simple subclasses to avoid logical errors. NewType at
  runtime has almost zero overhead. Type checkers require explicit casts from
  ``type`` where new type is expected, while implicitly casting from new type
  where ``type`` is expected.

function overloading
--------------------
- ``overload(func)``. decorator for marking overloaded function, in stub file.
  如果只在 regular modules 做注释, a series of @overload-decorated definitions
  must be followed by exactly one non-@overload-decorated definition. The
  @overload-decorated definitions are for the benefit of the type checker only,
  since they will be overwritten by the non-@overload-decorated definition,
  while the latter is used at runtime but should be ignored by a type checker.
  At runtime, calling a @overload-decorated function directly will raise
  NotImplementedError.
  
- @overload should be used only in cases where a type variable is not
  sufficient. 例如, 输入允许多种格式, 每种格式对应的输出具有不同格式, 存在一一
  对应的关系. 这样使用 Union 等方式无法表达这种对应关系.

- 注意由于我们此时已经将 function signature 做了 static typing, 一个函数名可以
  有多个形式的 signature 和不同的 function body 这就是 function overloading, ad
  hoc polymorphism. 最后定义的 non-overload function 是一般的 dynamic language
  中的 generic function, parametric polymorphism.

- If there are multiple equally good matching variants, a type checker will
  select the variant that was defined first.

  Due to the “pick the first match” rule, changing the order of your overload
  variants can change how the checker type checks your program. To minimize
  potential issues, order your variants and runtime checks from most to least
  specific. 

typed dict
----------
- ``TypedDict(name, specs, total=True)`` define a dict that has predefined keys
  and value types for each of the keys. It's suitable when using dicts to
  represent simple data only objects.

  ``name`` is TypedDict's name, ``specs`` is a dict of key to value types,
  ``total`` flag defines whether to allow keys to be left out (partial
  TypedDict) when creating a TypedDict object.

  .. code:: python

    Movie = TypedDict('Movie', {"name": str, "year": int})

- class-based syntax to define a TypedDict:

  .. code:: python

    class Movie(TypedDict):
      name: str
      year: int

  Note it doesn’t actually define a real class. This syntax also supports a
  form of inheritance – subclasses can define additional items. 

  In addition to allowing reuse across TypedDict types, class-based syntax also
  allows you to mix required and non-required items in a single TypedDict.

  .. code:: python

    class ChildMovie(Movie, total=False):
      based_on: str

- ``TypedDict`` is mypy specific, defined in ``mypy_extensions``.

- Mypy will also reject a runtime-computed expression as a key, as it can’t
  verify that it’s a valid key. You can only use string literals as TypedDict
  keys.

- The TypedDict type object can also act as a constructor. It returns a normal
  dict object at runtime – a TypedDict does not define a new runtime type.

  .. code:: python

    movie = Movie(name="title", year=1995)

- Like all types, TypedDicts can be used as components to build arbitrarily
  complex types. For example, you can define nested TypedDicts and containers
  with TypedDict items. Unlike most other types, mypy uses structural
  compatibility checking (or structural subtyping) with TypedDicts. A TypedDict
  object with extra items is a compatible with (a subtype of) a narrower
  TypedDict, assuming item types are compatible

- A TypedDict object is not a subtype of the regular ``Dict[...]`` type (and
  vice versa), since Dict allows arbitrary keys to be added and removed, unlike
  ``TypedDict``. However, any TypedDict object is a subtype of (that is,
  compatible with) ``Mapping[str, object]``, since typing.Mapping only provides
  read-only access to the dictionary items.

final names, methods and classes
--------------------------------
final names
^^^^^^^^^^^
- Final names are variables or attributes that should not reassigned after
  initialization. They are useful for declaring constants.

- Use ``Final`` (defined in ``typing_extensions``) to define a final
  identifier.

- A type checker will prevent further assignments to final names in
  type-checked code. Another use case for final attributes is to protect
  certain attributes from being overridden in a subclass.

- How to use:
 
  * Provide an explicit type when using Final ``Final[<type>]``:

    .. code:: python

      ID: Final[float] = 1

  * Omit the type:

    .. code:: python

      ID: Final = 1

    The actual type is inferred by the type checker. Note that unlike for
    generic classes this is not the same as ``Final[Any]``.

  Final can be used for module-level variables; class-level attributes;
  instance attributes assigned in ``__init__``.

- There can be at most one final declaration per module or class for a given
  attribute. There can’t be separate class-level and instance-level constants
  with the same name.

- There must be exactly one assignment to a final name.

- A final attribute declared in a class body without an initializer must be
  initialized in the ``__init__`` method.

- Final can’t be used in annotations for function arguments.

final methods
^^^^^^^^^^^^^
- Final methods should not be overridden in a subclass.

- Use ``final`` decorator (defined in ``typing_extensions``) to make a method
  final.

- This @final decorator can be used with instance methods, class methods,
  static methods, and properties.

final classes
^^^^^^^^^^^^^
- Final classes should not be subclassed.

- Use ``final`` decorator to make a class final.

- Useful when:
  
  * A class wasn’t designed to be subclassed. Perhaps subclassing would not
    work as expected, or subclassing would be error-prone.

  * Subclassing would make code harder to understand or maintain. For example,
    you may want to prevent unnecessarily tight coupling between base classes
    and subclasses.

  * You want to retain the freedom to arbitrarily change the class
    implementation in the future, and these changes might break subclasses.

utilities
=========
- ``TYPE_CHECKING``. A flag indicates whether the code is being run under type
  checker. Useful to make some code conditional according to we are at type
  checking time or runtime.

- ``cast(type, expr)``. tells the type checker that we are confident that the
  type of expr is type. At runtime a cast always returns the expression
  unchanged.

- ABCs for special methods: SupportsAbs, SupportsComplex, SupportsFloat,
  SupportsInt, SupportsRound, SupportsBytes.

- ``Text``. alias for str in py3, unicode in py2.

- ``AnyStr``, a type variable constrainted to be Text or bytes. It is meant to
  be used for functions that may accept any kind of string without allowing
  different kinds of strings to mix (注意是一个 type variable, 所以若出现多次必
  须是积类型一致).

- ``get_type_hints(obj, globalns=None, localns=None)``. Given a function,
  method, class, or module object, it returns a dict with the same format as
  ``__annotations__``, but evaluating forward references. If necessary,
  ``Optional[t]`` is added for function and method annotations if a default
  value equal to None is set. For a class C, return a dictionary constructed by
  merging all the ``__annotations__`` along ``C.__mro__`` in reverse order.

stub file
=========
why need stub file
------------------
stub file 专门用于记录 type hinting, only type checker will use it, not at
runtime. 如果在源代码中进行 type annotation, 则不需要 stub file, 然而有些时候
无法在源代码中直接 type annotation, 这时就需要 stub file 来补充说明, 而不动
源代码. 基于这个设计目的, 常见的 stub file use case 包含:

* for C-level extension module 进行 type annotation.

* for third play modules whose authors have not yet added type hints 添加注释.

* for standard library modules for which type hints have not yet been written.

* modules that must be compatible with both python2 and python3.

* modules that uses inline annotations for other purposes.

format
------
- syntactically valid Python modules, but use ``.pyi`` extension (refering:
  python interface).

- Place in the same directory as the corresponding real module. If a stub file
  is found the type checker should not read the corresponding "real" module.

- variable annotations are allowed in stub files.

- It is recommended that function bodies in stub files just be a single
  ellipsis.

- Modules and variables imported into the stub are not considered exported from
  the stub unless the import uses the import ... as ... form or the equivalent
  from ... import ... as ... form. However, all objects imported into a stub
  using from ... import * are considered exported.

- Just like in normal Python files, submodules automatically become exported
  attributes of their parent module when imported.

- Stub files may be incomplete. To make type checkers aware of this, the file
  can contain the following code

  .. code:: python

    def __getattr__(name) -> Any: ...

where to store stub files
-------------------------
- If you can control source code, put them alongside Python modules in the same
  directory.

- If you cannot control source code, third-party stubs installable by pip from
  PyPI are also supported.

migrating codes
===============
- Python's type annotation design makes it very easy to migrate existing codes
  to be statically type checked. Because dynamic typed and static typed codes
  can be mixed together. Static typing can be added incrementally.

- when you are prototyping a new feature, it may be convenient to initially
  implement the code using dynamic typing and only add type hints later once
  the code is more stable.

PEP 561 compatible packages
===========================
- PEP 561 notes three main ways to distribute type information.
  
  * The first is a package that has only inline type annotations in the code
    itself.
    
  * The second is a package that ships stub files with type information
    alongside the runtime code.
  
  * The third method, also known as a “stub only package” is a package that
    ships type information for a package separately as stub files.

- packages that supply type information via type comments or annotations in the
  code should put a ``py.typed`` in their package directory.

  packages that supply type information via type comments or annotations in the
  code should put a ``py.typed`` in their package directory.

  Stub files are placed next to the module they annotate.

- If the package is stub-only (not imported at runtime), the package should
  have a prefix of the runtime package name and a suffix of ``-stubs``. A
  ``py.typed`` file is not needed for stub-only packages.

typeshed
========
overview
--------
- contains external type annotation *stub files* for python stdlib and
  builtins, as well as some third-party packages.

- it's used primarily for static anlysis, including static type checking and
  type inference.

- typeshed is bundled with mypy, to use typeshed rather than develop it,
  there's no need to clone it directly.

mypy
====
overview
--------
- mypy is static type checker for python, meaning it will check for errors
  without ever running the code.

- By default, mypy will not type check dynamically typed functions.

install
-------
- install from pypi, typeshed is included automatically.

Type inference
--------------
- When type hints are added to a function, mypy will automatically check the
  function's body, by interpreting its logic and type inference.

- Mypy considers the initial assignment as the definition of a variable. When a
  variable's type is not explicitly annotated, it's inferred by mypy based on
  the static type of the value expression.

handling imports
----------------
- Mypy follows imports by default.

- how mypy handles imports.

  * mypy finds the module similar to the way python finds it.

  * mypy's own module search path. including:

    - MYPYPATH environ

    - ``mypy_path`` config file option.

    - directories containing files passed to mypy, by crawling up from the
      given file or package to the nearest directory that does not contain an
      ``__init__.py`` or ``__init__.pyi`` file.

    - installed packages.

    - directories of typeshed repo.

  * When searching a module in the said search path, the order of precendence
    is:

    - a package with matching name, i.e., a directory containing
      ``__init__.py`` or ``__init__.pyi`` file.

    - a stub file with matching name.

    - a python module with matching name.

  * missing imports.

    - For project's own codebase, ensure the code can be found by mypy by
      looking into its search path.

    - For stdlib, update mypy; if typeshed does not provide the module, or does
      not provide a complete set of type annotations file a bug; in the
      meantime, ``# type: ignore`` the relevant errors or add the module to
      ``ignore_missing_imports`` config option.

    - For third-party library, write your own stub files; or silence the
      missing import error, by ``# type: ignore`` the relevant errors or add
      the module to ``ignore_missing_imports`` config option.

CLI
---
::

  mypy [options] {[-m MODULE | -p PACKAGE]... | -c PROGRAM_TEXT | [file]...}

specifying what to check
^^^^^^^^^^^^^^^^^^^^^^^^
- Paths passed to mypy are type-checked, which can be a python source or
  directories that is recursed by mypy. Any file path starting with ``@`` reads
  additional command-line options and files from the file.

- check a module with ``-m MODULE``. specify module as would do import.
  Only the module itself is checked, not any submodule/subpackage etc.

- check a package with ``-p PACKAGE``. recursively check the package.

- check a program as string with ``-c PROGRAM_TEXT``.

config file
^^^^^^^^^^^
- ``--config-file CONFIG_FILE``. read config from file. default is mypy.ini
  or setup.cfg in cwd, or fallback to ``$XDG_CONFIG_HOME/mypy/config``,
  ``~/.config/mypy/config``, and ``~/.mypy.ini``, in that order.

- ``--warn-unused-configs``, warn about unused ``[mypy-<pattern>]`` section.

import discovery
^^^^^^^^^^^^^^^^
- ``--namespace-packages``. also discover namespace packages.

- ``--ignore-missing-imports``. ignore all unresolved module imports. this flag
  does not suppress errors about missing names in successfully resolved
  modules.

- ``--follow-imports {normal|silent|skip|error}``. how mypy follows imported
  modules that were not explicitly passed in via the command line. default is
  normal.

- ``--python-executable EXECUTABLE``. collect type information for packages
  installed for EXECUTABLE. default collect for python executable that is
  running mypy.

- ``--no-site-packages``. Use this flag if mypy cannot find a Python executable
  for the version of Python being checked, and you don’t need to use PEP 561
  typed packages.

- ``--no-silence-site-packages``. By default, mypy will suppress any error
  messages generated within PEP 561 compliant packages. This disables that.

platform configuration
^^^^^^^^^^^^^^^^^^^^^^
- ``--python-version X.Y``. make mypy type check your code as if it were run
  under Python version X.Y.  by default use current python version. This flag
  will attempt to find a Python executable of the corresponding version to
  search for PEP 561 compliant packages.

- ``-2, --py2``. alias to ``--python-version 2.7``

- ``--platform PLATFORM``. This flag will attempt to find a Python executable
  of the corresponding version to search for PEP 561 compliant packages.
  default is current platform.

- ``--always-true NAME``. make NAME a compile-time constant that is always
  true.

- ``--always-false NAME``. ditto for false.

disallow dynamic typing
^^^^^^^^^^^^^^^^^^^^^^^
- ``--disallow-any-unimported``. disallows usage of types that come from
  unfollowed imports.

- ``--disallow-any-expr``. disallows all expressions in the module that have
  type Any. If an expression of type Any appears anywhere in the module mypy
  will output an error unless the expression is immediately used as an argument
  to cast or assigned to a variable with an explicit type annotation. declaring
  a variable of type Any or casting to type Any is not allowed. Note that
  calling functions that take parameters of type Any is still allowed.

- ``--disallow-any-decorated``. disallows functions that have Any in their
  signature after decorator transformation.

- ``--disallow-any-explicit``. disallows explicit Any in type positions such as
  type annotations and generic type parameters.

- ``--disallow-any-generics``. disallows usage of generic types that do not
  specify explicit type parameters.

- ``--disallow-subclassing-any``. This flag reports an error whenever a class
  subclasses a value of type Any. This may occur when the base class is
  imported from a module that doesn’t exist, or is ignored. Since the module is
  silenced, the imported class is given a type of Any.

untyped definitions and calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``--disallow-untyped-calls``. reports an error whenever a function with type
  annotations calls a function defined without annotations.

- ``--disallow-untyped-defs``. reports an error whenever it encounters a
  function definition without type annotations.

- ``--disallow-incomplete-defs``. reports an error whenever it encounters a
  partly annotated function definition.

- ``--check-untyped-defs``. type checks the body of every function, regardless
  of whether it has type annotations. (By default the bodies of functions
  without annotations are not type checked.)

- ``--disallow-untyped-decorators``. reports an error whenever a function with
  type annotations is decorated with a decorator without annotations.

None and Optional handling
^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``--no-implicit-optional``. stop treating arguments with a None default value
  as having an implicit Optional[...] type.

- ``--no-strict-optional``.

configure warnings
^^^^^^^^^^^^^^^^^^
- ``--warn-redundant-casts``. report an error whenever your code uses an
  unnecessary cast that can safely be removed.

- ``--warn-unused-ignores``. report an error whenever your code uses a
  ``# type: ignore`` comment on a line that is not actually generating an error
  message.

- ``--no-warn-no-return``. By default, mypy will generate errors when a
  function is missing return statements in some execution paths. The only
  exceptions are when: 1) The function has a None or Any return type; 2)
  The function has an empty body or a body that is just ellipsis.

- ``--warn-return-any``. This flag causes mypy to generate a warning when
  returning a value with type Any from a function declared with a non-Any
  return type.

misc strictness flags
^^^^^^^^^^^^^^^^^^^^^
- ``--allow-untyped-globals``. suppress errors caused by not being able to
  fully infer the types of global and class variables.

- ``--allow-redefinition``. By default, mypy won’t allow a variable to be
  redefined with an unrelated type. This flag enables redefinion of a variable
  with an arbitrary type in some contexts: only redefinitions within the same
  block and nesting depth as the original definition are allowed.

- ``--strict``. enables all optional error checking flags.

configuring error messages
^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``--show-error-context``. precede all errors with “note” messages explaining
  the context of the error.

- ``--show-column-numbers``. add column offsets to error messages.

incremental mode
^^^^^^^^^^^^^^^^
By default, mypy will store type information into a cache. Mypy will use this
information to avoid unnecessary recomputation when it type checks your code
again. 

- ``--no-incremental``. do not reference cache. Note that mypy will still write
  out to the cache even when incremental mode is disabled.

- ``--cache-dir DIR``. By default, mypy stores all cache data inside of a
  folder named ``.mypy_cache`` in the current directory. To disable writing to
  the cache, use ``--cache-dir=/dev/null``

- ``--skip-version-check``. By default, mypy will ignore cache data generated
  by a different version of mypy. 

report generation
^^^^^^^^^^^^^^^^^
- ``--any-exprs-report DIR``. generate a text file report documenting how many
  expressions of type Any are present within your codebase.

- ``--linecount-report DIR``. Causes mypy to generate a text file report
  documenting the functions and lines that are typed and untyped within your
  codebase.

- ``--linecoverage-report DIR``. generate a JSON file that maps each source
  file’s absolute filename to a list of line numbers that belong to typed
  functions in that file.

- ``--cobertura-xml-report DIR``. generate a Cobertura XML type checking
  coverage report.

- ``--html-report DIR, --xslt-html-report DIR``. generate an HTML type checking
  coverage report.

- ``--txt-report DIR, --xslt-txt-report DIR``. generate a text file type
  checking coverage report.

- ``--junit-xml JUNIT_XML``. generate a JUnit XML test result document with
  type checking results.

- ``--find-occurrences CLASS.MEMBER``. print out all usages of a class member
  based on static type information. 

advanced flags
^^^^^^^^^^^^^^
for people who are interested in developing or debugging mypy internals.

configuration
-------------
- configuration prcedence:

  * cmdline args

  * config file

  * mypy defaults

- config file format: ini file.

- Most options correspond closely to command-line flags.

- sections:

  * ``[mypy]`` must be present. specify the global flags.

  * ``[mypy-PATTERN1,PATTERN2,...]`` specify per-module flags, where each
    pattern is a fully-qualified module names, with some components optionally
    replaced by the ``*`` character. Pattern without ``*`` matches only the
    named module. Stars match zero or more module components, can be present in
    the middle of patterns. e.g.,::

      foo.bar.* matches foo.bar, foo.bar.baz, ...
      foo.*.bar matches foo.bar. foo.baz.bar, ...

gloal and per-module options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import discovery
""""""""""""""""
- ``ignore_missing_imports``. boolean. When used in a per-module section,
  the module name should match the name of the imported module, not the module
  containing the import statement.

- ``follow_imports``. string. In per-module section, the module name should
  match the name of the imported module, not the module containing the import
  statement.

- ``follow_imports_for_stubs``. boolean.

disallow dynamic typing
""""""""""""""""""""""""
- ``disallow_any_unimported``. boolean.

- ``disallow_any_expr``. boolean.

- ``disallow_any_decorated``. boolean.

- ``disallow_any_explicit``. boolean.

- ``disallow_any_generics``. boolean.

- ``disallow_subclassing_any``. boolean.

untyped definitions and calls
""""""""""""""""""""""""""""""
- ``disallow_untyped_calls``. boolean.

- ``disallow_untyped_defs``. boolean.

- ``disallow_incomplete_defs``. boolean.

- ``check_untyped_defs``. boolean.

- ``disallow_untyped_decorators``. boolean.

None and optional handing
""""""""""""""""""""""""""
- ``no_implicit_optional``. boolean.

- ``strict_optional``. boolean. default True.

configuring warnings
""""""""""""""""""""
- ``warn_unused_ignores``. boolean.

- ``warn_no_return``. boolean. default True.

- ``warn_return_any``. boolean.

suppressing errors
""""""""""""""""""
- ``show_none_errors``. boolean, default True. Shows errors related to strict
  None checking, if the global ``strict_optional`` flag is enabled.

- ``ignore_errors``. boolean. ignores all non-fatal errors.

misc strictness flags
""""""""""""""""""""""
- ``allow_redefinition``. boolean.

global-only options
^^^^^^^^^^^^^^^^^^^
import discovery
""""""""""""""""
- ``namespace_packages``. boolean.

- ``python_executable``. string.

- ``no_silence_site_packages``. boolean.

- ``mypy_path``. string. Specifies the paths to use, after trying the paths
  from ``MYPYPATH`` environment variable.

platform configuration
""""""""""""""""""""""
- ``python_version``. string.

- ``platform``. string.

- ``always_true``. comma separated list of strings.

- ``always_false``. comma separated list of strings.

incremental mode
""""""""""""""""
- ``incremental``. boolean. default True.

- ``cache_dir``. string.

- ``skip_version_check``. boolean.

configuring error messages
""""""""""""""""""""""""""
- ``show_error_context``. boolean.

- ``show_column_numbers``. boolean.

configuring warnings
""""""""""""""""""""
- ``warn_redundant_casts``. boolean.

- ``warn_unused_configs``. boolean.

misc
""""
- ``scripts_are_modules``. boolean.

- ``verbosity``. integer. default 0.

advanced options
""""""""""""""""

daemon
------
run mypy as a long-running daemon (server) process using ``dmypy`` and use a
command-line client to send type-checking requests to the server. 

This way mypy can perform type checking much faster, since program state cached
from previous runs is kept in memory and doesn’t have to be read from the file
system on each run.

running mypy using the mypy daemon can be 10 or more times faster for bigger
codebase than the regular command-line mypy tool.

Each mypy daemon process supports one user and one set of source files, and it
can only process one type checking request at a time. You can run multiple mypy
daemon processes to type check multiple repositories.

The mypy daemon is experimental. In particular, the command-line interface may
change in future mypy releases.

mypy plugins
------------
- Mypy supports a plugin system that lets you customize the way mypy type
  checks code. This can be useful if you want to extend mypy so it can type
  check code that uses a library that is difficult to express using just PEP
  484 types.

- The plugin system is experimental and prone to change.

- Plugins are Python files that can be specified in a mypy config file, under
  global ``[mypy]`` section, ``plugins`` key, using one of the two formats:
  
  * relative or absolute path to the plugin to the plugin file
   
  * a module name (if the plugin is installed using pip install in the same
    virtual environment where mypy is running).
  
  The two formats can be mixed.

monkeytype
==========
- You can collect types of existing codes from test runs. This is a good
  approach if the project's current test coverage is high.

References
==========
.. [pep3107] `PEP 3107 -- Function Annotations <https://www.python.org/dev/peps/pep-3107/>`_
.. [pep483] `PEP 483 -- The Theory of Type Hints <https://www.python.org/dev/peps/pep-0483/>`_
.. [pep484] `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_
.. [pep526] `PEP 526 -- Syntax for Variable Annotations <https://www.python.org/dev/peps/pep-0526/>`_
.. [pep563] `PEP 563 -- Postponed Evaluation of Annotations <https://www.python.org/dev/peps/pep-0563/>`_
