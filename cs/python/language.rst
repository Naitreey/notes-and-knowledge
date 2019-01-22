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
包含对一系列类型的标准陈述.

module
^^^^^^

- module 中一般不该出现在 import 时会给出输出的 "裸代码". 它不该做奇怪
  的事情, 应该 keep silent.

- All global identifiers defined in a module are module's attributes.

- implicit predefined attributes. 注意这些相当于只是 predefined global
  identifier 而已.

  * ``__name__``

  * ``__file__``. pathname of the module file, can be a so file for C
    extension modules.

  * ``__path__``. For package. a iterable of strings specifying subpackage's
    import paths.

  * ``__doc__``. module doc.

  * ``__annotations__``. module-level variable annotations storage.

  * ``__dict__``. module's global namespace.

class
^^^^^
- class 的分类.
  
  对于 CPython, 按照实现方式不同, class 可以分为:

  * builtin types. implemented in C as part of CPython interpreter.

  * extension class. implemented in C as part of C module extension.

  * custom class. implemented in Python.

- 实例化.

  调用 ``cls(*args, **kwargs)`` 进行类实例化的执行逻辑:

  1. create instance:
     调用 static method ``object.__new__(cls, *args, **kwargs)`` 创建
     实例 ``instance``.

  2. customize instance:
     调用 ``instance.__init__(*args, **kwargs)``.

  最后返回 ``instance`` 给 caller.

  这套实例化逻辑在 ``type.__call__`` 中定义.

- attribute reference.

  搜索顺序. 首先搜索 class ``__dict__``, 然后搜索 parent class ``__dict__``
  in MRO order. 最后搜索 metaclass 的 attributes.
  即 (不考虑 descriptor)::

    class -> parent class -> ... -> metaclass -> parent metaclass -> ... -> type -> object

- MRO. python2.3+ uses C3 method resolution order. 若对于一个类, 无法根据 C3 MRO
  算法给出 ``__mro__`` attribute, 则无法创建这个类. 此时会 raise TypeError.

class instance
^^^^^^^^^^^^^^

* attribute reference.
  
  搜索顺序. 首先搜索 instance ``__dict__``, 然后搜索 class & parent
  classes attributes, in MRO order. 注意不会去搜索 metaclass 的 attributes.
  即 (不考虑 descriptor)::

    instance -> class -> parent class -> ... -> object

  若属性是一个 function object, 转变成 bound instance method, 它的
  ``__self__`` attribute is the instance. See also `instance method`_.

  若最终没找到, call ``__getattr__``.

  以上步骤详见 `attribute access`_.

* attribute modification. 修改和删除属性只更新 ``__dict__``. 若
  定义了 ``__setattr__``, ``__delattr__`` 则直接调用这两个方法.

user-defined function
^^^^^^^^^^^^^^^^^^^^^

- special attributes. ``object``'s common attributes are not listed.

  * ``__doc__``. docstring.

  * ``__module__``. defining module.

  * ``__defaults__``. argument's default value storage. A tuple containing
    default argument values for those arguments that have defaults, or None.

  * ``__code__``. The code object representing the compiled function body.

  * ``__globals__``. function's lexical global scope.

  * ``__closure__``. None or a tuple of cells that contain bindings for the
    function’s free variables. 注意只有在函数中真正使用到的 free varialbes
    才会 keep 在里面, 这样省内存. ``__globals__`` & ``__closure__`` 协助实现
    lexical scope and closure.

  * ``__dict__``. arbitrary storage.

  * ``__annotations__``. function annotation storage.

  * ``__kwdefaults__``. storage for defaults of keyword-only parameters.

class method object
^^^^^^^^^^^^^^^^^^^
- typical usage.

  * as alternative constructor for the class. The ``cls`` argument is the
    key for subclassing.
    
    如果一个 class 确实需要 从概念上完全不同的构造方式, 则完全可以创建多个
    ``__init__`` 之外的 class method 作为 alternative constructor. (When they
    want different ways, give it to them.)

    例如, ``datetime.datetime`` 的多个 constructor.

static method object
^^^^^^^^^^^^^^^^^^^^
- typical usage.

  * 当一个函数更多的是一种 utility 的地位, 与实例无关, 与 class 也无关, 并且也
    确实不需要子类去自定义的时候. 就可以用 static method.

    那么, 既然跟类都没有关系, 干嘛要放在类里面呢? 一个解释是, 有时候这样更便于
    用户找到他所需要的 utility, 并且 cls name 为这个 utility 提供了一个有意义
    的 context, 用以和其他类似的 utility 做区分. 实际上如果合适的话也可以放在
    module-level.

instance method
^^^^^^^^^^^^^^^
- A instance method can be created via a function, a classmethod object,
  etc. that are defined as attribute of class object.

- 从一个 instance method 中可以获取两方面信息:

  * 所属的 class instance or class (if classmethod).

  * 所源于的 function object.

  相应地, 它具有以下各点所述属性.

- ``__self__``. class instance or class itself (if classmethod).

- ``__func__``. underlying function object.

- ``__doc__``. function's docstring.

- ``__name__``. function's name.

- ``__module__``. the name of the module where the function is defined.

- Readonly access to arbitrary function attributes on the underlying function
  object.

- 不能直接对 instance method 赋值任意属性. 会 raise AttributeError.

- The transformation from function object to instance method object happens
  each time the attribute is retrieved from the instance.

special attributes & methods
----------------------------

instantiation
^^^^^^^^^^^^^
以下属性在 class & metaclass 上有.

- ``class.__new__(cls, ...)``. static method. 实例化时调用该方法创建 ``cls`` 的
  新实例. 剩下的参数定义就是 constructor 的参数 signature. 返回 new object
  instance. 如果定义时未使用 ``@staticmethod`` decorator, 解释器会自动将之转换
  为 static method.

  注意 ``__new__`` 是一个 static method, 而不是 class method. 因此, 调用时需要
  传入要实例化的 ``cls`` object. 它是 static method 的原因是为了解决以下两个
  应用场景 [SOPyNew]_:

  * explicitly call parent class ``__new__`` without using ``super()``.

  * Allows to create an instance of subclass.

- ``class.__init__(self, ...)``. Must return None.

以下属性在 class instances 上有.

- ``instance.__class__``. the class of the instance.
  
  这个属性是 writable 的. 隐含之意是 technically, we can change an instance's
  class dynamically at runtime. 然后所有的 MRO 相关机制在执行时都会通过新的
  ``__class__`` 类. 这样做在正常情况下是不推荐的, 但不是说完全没有用处.

  用处:

  * 允许用户临时给某个实例增加一些兼容的子类方法. 例如
    ``django_mysql.models.add_QuerySetMixin()``

  * If you have a long time running application and you need to replace an old
    version of some object by a newer version of the same class without loss of
    data, e.g. after ``importlib.reload()``.

  可能的问题[SOPyChangeClass]_:

  * confuses people reading or debugging your code.

  * ``__init__`` 时使用的是原来的类, 因此可能实例上没有新的类方法所需的数据.

  * If you use ``__slots__``, all of the classes must have identical slots.

  * 如果两个类使用了不同的 metaclass, more confusion.


attribute store
^^^^^^^^^^^^^^^
- ``object.__dict__``. 一个对象自身存储的属性. 如果 class 定义了 ``__slots__``,
  实例就没有 dict store.

- ``__slots__``. explicitly declare instance members, suppressing the creation
  of ``__dict__`` and ``__weakref__``, unless they are explicitly specified in
  ``__slots__`` or available in parent class.

  * slots 的用处:

    - 对于需要大量构建实例, 而实例本身不会出现任意属性时, 可以使用 slots 来优化
      内存使用效率.

    - 更快的属性访问.

  * Any non-string iterable may be used in slots definition.
  
  * slots 本质上以 data descriptor 方式作为 class attribute 来定义, 其类型为
    ``member_descriptor``. slots 定义所在类中, 若再定义同名的 class member,
    会造成冲突 raise ValueError. 但是在子类中, 可以定义 class member 来覆盖
    父类中定义的 slot member.

  * 当前类的 slots 与各个父类的 slots 的并集为类实例实际具有的 slots. 在多继承
    中, 只有一个直接父类允许具有 non-empty slots. 其他直接父类如果有 slots 则必
    须是 empty 的. Otherwise raises TypeError: multiple bases have instance
    lay-out conflict.

  * 如果父类没有 ``__slots__`` declaration (``object`` 除外), 则即使子类设置了
    slots, ``__dict__`` 和 ``__weakref__`` 也会存在. 从而 defeat the purpose
    of slots.

  * 如果父类设置了 slots, 但子类没有设置, 子类实例仍会有 ``__dict__`` and
    ``__weakref__``. 这是为了保证兼容, 即假设父类本来没有设置 slots, 那么在
    未来如果父类选择去设置 slots 来进行优化, 子类代码不会 break.
    
    为保证子类也没有那两个存储, 需要设置额外的 slots 定义, 即使为空.

  * Assigning to the name of attribute not declared in slots raises
    AttributeError.  Read the value of uninitialized slots raises
    AttributeError.

  * Without ``__weakref__``, instances can not be weakref-ed.

  * Nonempty ``__slots__`` does not work for classes derived from
    variable-length built-in types such as int, bytes and tuple.

object identification
^^^^^^^^^^^^^^^^^^^^^

class, function-like definitions, generator instance (including those from
generator functions and generator expressions), and module.

- ``definition.__name__``. the name of definition. for module, the qualified
  import path of module.

- ``definition.__qualname__``. the qualified name of definition.
  这是 the “path” from a module’s global scope to the object. module object
  没有这个属性.

class relations
^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``instance_method.__self__``, instance reference, readonly.

- ``instance_method.__func__``, underlying function defined in class, readonly.

- ``instance_method.__doc__``, same as ``__func__.__doc__``, readonly.

- ``instance_method.__module__``, same as ``__func__.__module__``, readonly.

container protocol
^^^^^^^^^^^^^^^^^^

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

make it callable
^^^^^^^^^^^^^^^^

- ``object.__call__(self, ...)``. make an object callable. Anything that
  is supposed to be callable needs to define this method.

attribute access
^^^^^^^^^^^^^^^^

- ``object.__getattribute__(self, name)``. 负责一个对象上的所有属性访问.
  In order to avoid infinite recursion in this method, its implementation
  should always call the base class method with the same name to access any
  attributes it needs.

  ``object`` base class 实现了基础的 ``__getattribute__``, 即默认情况下, 所有
  ``instance.attr`` 使用以下属性访问逻辑:

  1. 尝试 data descriptor. 若有, 调用::

       descriptor.__get__(self, instance, type(instance))

  2. 尝试 instance attribute (``__dict__``). 若有, 直接返回.

  3. 尝试 non-data descriptor 和 class attribute. 若存在, 
      
     * 对于 non-data descriptor, 调用::

         descriptor.__get__(self, instance, type(instance))

       注意 class 中定义的函数本质上就是 non-data descriptor. 访问 method
       function 时 ``__get__`` 给出一个 bound method.

     * 对于 class attribute, 直接返回.

  4. 若以上全败, 调用 ``__getattr__``. 对这一点应用的一个例子是
     ``pymongo.MongoClient``.

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

stringify and formating
^^^^^^^^^^^^^^^^^^^^^^^

- ``object.__str__``

- ``object.__bytes__``

- ``object.__repr__``. Try always create a ``__repr__`` for your class to make
  debugging easier.

- ``object.__format__(self, format_spec)``. used by ``format()``, ``str.format()``
  formatted string literal. 当 object 作为被 format 的对象时使用. `format_spec`
  是与该对象对应的 ``{:spec}`` 部分. 该方法根据 format spec 进行格式化, 输出恰当
  的 string 形式. most classes will either delegate formatting to one of the
  built-in types, or use a similar formatting option syntax.

  object 的默认 ``__format__`` 实现只接受 ``""``, 并输出 ``__str__`` 形式.
  对任何 non-empty string, raise TypeError.

numerical operations
^^^^^^^^^^^^^^^^^^^^
注意 operator overloading 仅限于 numerical operators. 不能对 logical operators
进行重载. 在 logical context 下, 每个对象的 ``__bool__`` is called to get a
boolean value for logical evaluation.

bitwise operators
"""""""""""""""""
- ``__invert__``. bitwise not (``~``)

- ``__and__``. bitwise and ``&``

- ``__or__``. bitwise or ``|``

- ``__xor__``. exclusive or ``^``

context manager protocol
------------------------
A context manager manages some "context". They usually do some setup work
before code entering its enclosed cotext; then do some cleanup work after
code exiting from the context.

使用 context manager 的意义在于省事. 它自动保证所需资源和环境等的获取和释放,
而不用在业务逻辑代码周围添加 explict ``try...finally`` block 等. 使得代码更
清晰.

context manager 和 decorator 的关系和区别.

* context manager 适用于当我们需要把某一操作置于一个特定的 context 下, 并封装有
  方便的建立 context 和消除 context 的操作. 注意重点是操作, context manager
  只是一个方便的工具, 为这个操作提供 context 服务.

* decorator 比 context manager 涵盖的范围宽泛许多. 它 decorate 下面的操作 (class/
  function), 而这种含义的附加和修改不局限于 "prepare-cleanup" 的 context manager
  使用场景, 而是任何的含义附加以及操纵. 简单的可以是 `classmethod` 等基本的含义
  微调, 复杂的可以是将一定的操作 attach 至某个更大的完整的框架, 例如 `Flask.route`,
  `unittest.skipIf`.

``contextlib`` 提供了很多有助于利用 context manager 的工具. See also:
`contextlib <contextlib.rst>`_.

API
^^^
- ``object.__enter__(self)``. 在 ``with obj [as a]:`` statement 中, 进入
  context 时, call ``obj.__enter__`` to setup context. 若 ``as a`` clause
  is present, ``__enter__()``'s return value is assigned to it, whatever it is.

- ``object.__exit__(self, exc_type, exc_value, exc_tb)``.
  退出 context 时, call ``__exit__`` to cleanup context. If exception is raised
  in the context, its info will be passed in as arguments, otherwise they're
  None.
  
  该方法的返回值决定 cpython 是否会 suppress exception. Truthy value
  means to suppress, falsy value otherwise. 因此 cleanup 逻辑说了算.
  建议返回值只使用 True/False/None (implicitly).
  (一般情况下 cleanup logic 没有 suppress 的意愿, 而是直接写上 cleanup 逻辑,
  这样返回的是 None. 这是很自然的方式.)

  Exceptions that occur during execution of this method will replace any
  exception that occurred in the context.

  The exception passed in should never be reraised explicitly, it's caller's
  responsibility.

common context managers
^^^^^^^^^^^^^^^^^^^^^^^
- io objects, file-like objects, auto-close on finish, like ``TextIOWrapper``.

- lock objects. automatic acquiring/releasing lock.

- connection objects. auto-close on finish, like ``pymongo.MongoClient``.
  auto-commit on finish. like ``MySQLdb.connections.Connection``.

design patterns
^^^^^^^^^^^^^^^
- When an operation requires setup and teardown logic, use context manager to
  encapsulate it.

- When a resource is local to a particular section of code, use a context manager
  to ensure it is cleaned up promptly and reliably after use. A try/finally
  statement is also acceptable.

- Context managers should be invoked through separate functions or methods whenever
  they do something other than acquire and release resources. For example:

  Yes:

  .. code:: python

    with conn.begin_transaction():
        do_stuff_in_transaction(conn)
  No:

  .. code:: python

    with conn:
        do_stuff_in_transaction(conn)

  The latter example doesn't provide any information to indicate that the
  ``__enter__`` and ``__exit__`` methods are doing something other than closing
  the connection after a transaction. Being explicit is important in this case.

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``descriptor.__get__(self, instance, owner)``. ``obj.descr`` 获取时调用.
  当 obj 为 instance of owner class 时, ``instance = obj``, ``owner = type(obj)``;
  当 obj 为 owner class 时, ``instance = None``, ``owner = obj``.

- ``descriptor.__set__(self, instance, value)``. ``obj.descr = ...`` 赋值时
  调用. 对 descriptor 赋值只能在 instance of owner class 中生效.

- ``descriptor.__delete__(self, instance)``. ``del obj.descr`` 删除时调用.
  删除 descriptor 只能在 instance of owner class 中生效.

定义以上任意方法, 则 class 成为 descriptor.

分类和调用优先级
^^^^^^^^^^^^^^^^
- data descriptor: 定义 ``__get__`` 和 ``__set__``. 若定义 readonly descriptor,
  让 ``__set__`` raise AttributeError 即可.
  
- non-data descriptor: 只定义 ``__get__``.

typical use cases
^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^
- 确定 metaclass.
  The appropriate metaclass for a class definition is determined as follows:

  * if no bases and no explicit metaclass are given, then type() is used

  * if an explicit metaclass is given and it is not an instance of type(),
    then it is used directly as the metaclass

  * if an instance of type() is given as the explicit metaclass, or bases
    are defined, then the most derived metaclass is used

  The most derived metaclass is selected from the explicitly specified
  metaclass (if any) and the metaclasses (i.e. type(cls)) of all specified base
  classes.  **The most derived metaclass is one which is a subtype of all of
  these candidate metaclasses. If none of the candidate metaclasses meets that
  criterion, then the class definition will fail with TypeError.**

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

- Execute class body in the created namespace. 注意, class body 的定义本身不过
  是一个 namespaced execution environment. class body 包含的内容不需要局限于
  对 class members 的定义. Everything that can be done at module namespace
  level, can be similarly done in a class namespace.

- 执行 ``name = metaclass(name, bases, namespace, **kwargs)`` 创建 class object.
  这实际上就是按照正常的实例化流程进行 (metaclass 仍然是 object 的子类, 遵从
  实例化步骤). 调用:

  * ``metaclass.__new__``, 创建 class object.

  * ``cls.__init__`` (instance method, 此时 instance 为 class), customize class
    object.

  若任意 method 中包含 ``super``, 过程中创建 implicit ``__class__`` reference,
  指向创建的 class object. 这用于 argumentless ``super()``.

metaclass
^^^^^^^^^
指定自定义的 metaclass. 定义 class 时, 在 definition line 中, 使用
``metaclass`` keyword argument 指定 metaclass, 其他 kwargs 则传入
后续一系列流程中.

metaclass 和 class 的关系与 class 和 instance 的关系是类似的.

在 metaclass 定义中, 它的 instance 就是 class, 因此, metaclass 的
instance method 定义第一个参数是 ``cls``, class method 的第一个
参数是 ``metaclass``.

注意 metaclass 仍然是 object 的子类. 遵从一般的逻辑.

metaclass methods
"""""""""""""""""

- ``metaclass.__prepare__(metaclass, name, bases, **kwargs)``.
  这是一个 class method. 定义时需要使用 classmethod decorator.
  在上述的 prepare class body namespace 步骤中调用, 返回一个准备好的
  namespace. 返回的应该是一个 MutableMapping instance, e.g. dict,
  OrderedDict. By default, class namespace is initialised as an empty ordered
  mapping.

  注意这个 classmethod 是在调用 ``name = metaclass(...)`` 之前执行的, 其输出
  作为 ``metaclass()`` call 中的 namespace 参数值. 因此, ``__prepare__``
  应定义在 ``__new__`` 的前面.

- ``metaclass.__new__(metaclass, name, bases, namespace, **kwargs)``. 
  本质上是 override ``object.__new__`` classmethod. 不同的是, 在 metaclass
  语境下, 第一个参数是现在变成了 metaclass. 后面三个 positionals 形式和意义
  是固定的. 使用 ``metaclass(...)`` 手动提供或使用 class definition statement
  由解释器自动添加. kwargs 是在 class definition line 上指定的.

methods
^^^^^^^
- why in python, we need ``self`` (or whatever you like) as the first parameter
  of method, rather than making it implicit (like in Java or JavaScript)?

  * This is an accidental good design. Guido 在设计 python 时, 一开始没有想到
    要 class. 后来只花了一天引入 class. What he basically did was indent all
    module-level functions into a new namespace. But he needed a way to pass
    instance into method via ``.`` operator, so ``self`` is introduced as a
    quick fix.

Expressions
===========

Atoms
-----

- General comprehension syntax. list, set, dict's comprehension and generator
  expression use a common inline for-loop (with filtering) syntax.

  scope rule. 与一般的 for loop 不同, comprehension 中的 loop variable is scoped
  inside the expression itself, whereas for loop does not build a scope (python
  does not have block scope).

identifiers
^^^^^^^^^^^
- name mangling. Occurs when an identifier that textually occurs in a class
  definition begins with two or more underscore characters and does not end in
  two or more underscores. Basically, ``__name`` in ``cls`` becomes
  ``_cls__name``.

  name mangling 是在 bytecode 生成之前, 类似于预处理.

  如果 identifier 只有 ``_`` 组成, 不会 mangling.

  什么时候使用 name mangling?

  * 当我们需要指定私有成员, 从而避免子类能够无意或刻意地去 override/extend 在基
    类中的定义.

  * 当我们在实现一个函数, 如果它一定要使用在这个类中实现的方法, 而不能因为实例是
    子类的, 就自动使用了子类中同名的方法.

tuple, list, set, dict's display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

literal display form
""""""""""""""""""""
- tuple, list, set use a common display form: a list of ``star_item``::

    starred_list  ::=  starred_item ( "," starred_item )* [","]

  * each ``stared_item`` is an expression or an iterable unpacking
    operation.

  * iterable unpacking: The iterable is expanded into a sequence of items,
    which are included in the new tuple, list, or set, at the site of the
    unpacking.

  * The trailing comma is only required when creating a tuple singleton.

  examples::

    (1,)
    {*(1,2,3), 3, 4, *{"a":1, "b":2}, 5, 6,}

- dict display form: a list of ``key_datum``::

    key_datum_list  ::=  key_datum ("," key_datum)* [","]

  * each ``key_datum`` is a ``key: value`` pair, or a mapping unpacking.

  * mapping unpacking: The mapping's key-value pairs are expanded and
    added to the new dict.

  examples::

    {}
    {"a":1, **dict(a=1, b=2), "c": 3, **OrderedDict(c=3, d=4),}

comprehension form
""""""""""""""""""

generator expression
^^^^^^^^^^^^^^^^^^^^
- comprehension.

Primaries
---------

Subscriptions & slicing
^^^^^^^^^^^^^^^^^^^^^^^

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


Calls
-----
- 当 function call 中使用了 iterable unpacking ``*iterable`` syntax, the
  following operation is performed on ``iterable`` to obtain the necessary
  information and values to be passed to the call:

  * ``__iter__`` is called to get an iterator to generating values.

  * ``__len__`` is called to inspect the number of values that is available
    here. 这用于计算传入的 args 数目, 与 function signature 进行比较. (当
    args 数目大于 function 接受的 positional 数量, 则 raise TypeError.)

comparisons
-----------
- comparison operators::

    < > == >= <= !=
    is [not]
    [not] in

- All comparison operators have the same precedence.

- Comparison operations can be chained together arbitrarily. And the overall
  evaluation order is strictly left-to-right and short-circuit. In other words,
  if::
  
    a, b, c, …, y, z
    
  are expressions and::
  
    op1, op2, …, opN
    
  are comparison operators, then::
  
    a op1 b op2 c ... y opN z
    
  is equivalent to::
  
    a op1 b and b op2 c and ... y opN z

  except that each expression is evaluated at most once.

- Note that ``a op1 b op2 c`` doesn’t imply any kind of comparison between
  ``a`` and ``c``. So it's legal to say ``x < y > z``

Statements
==========

assignment statements
---------------------
以下 BNF 有所简化.

::

  assignment_stmt ::= (target_list "=")+ expression_list
  target_list ::= target ("," target)* [","]
  target ::= identifier
             | "(" [target_list] ")"
             | "[" [target_list] "]"
             | attributeref
             | subscription
             | slicing
             | "*" target

about target list
^^^^^^^^^^^^^^^^^
- An assignment statement evaluates the expression list and and assigns the
  single resulting object to each of the target lists, from left to right.

- 一个 assignment 如何去给 LHS 赋值, 取决于 LHS 的形式.

  * 当 LHS 是一个 target list, 则需要对 RHS 进行 iterable unpacking.

  * 当 LHS 是一个 single target, 则 RHS 是整体赋值给 LHS.

- 注意到 BNF 中, target list 是递归定义的. 以下详述 target list 的可能形式.

  * target list 可以是 surrounded by ``()``, ``[]`` 或者裸的.  但是注意, ``()``
    中包含单个 target 时, 服从 tuple 的书写规则.  即 ``(x) = [1]`` 不会认为是
    target list, ``()`` 是括号, 自动去掉. 该赋值 LHS 是单层的 single target.
    ``(x,) = [1]`` 才是 target list, 对 RHS unpacking.

  * target list 可以是单层或多层的. 对于多层的, 则自然需要 ``()`` or ``[]``
    进行界限划分.

  * 对某一层, 最多只能有一个 ``*target`` 形式的 target.
    (否则无法确定性地分配剩余元素.) 该 target 可以出现在该层的任意位置.

  * 对于某一层, RHS unpacking 后的元素个数必须大于等于 target list 中除了
    starred target 以外的 target 个数. 若没有多余的元素可分配, starred target
    分配到的元素列表为空.

  * ``*target`` starred target 本身仍可以是一个下一层的 target list.

  * 赋值时, 除了 starred target 之外, 对于每一层的一个 target, 对应于 RHS
    相应的层 unpacking 后的一个元素, 无论这个 target 本身是否又是一个下一层的
    target list. 即使是下一层的 target list, 在本层也只对应于一个元素.

  * 对于 starred target, 接受本层的所有剩余的无法分配的元素.

  * 注意理论上 ``()`` ``[]`` 里面的 target list 可以为空, 此时在 RHS
    的对应位置上元素进行 unpacking 后结果也要为空.::

      () = []
      a, () = 1, ()

- 神经病示例.

  .. code:: python

    a, b, *(c, *[d, *(e, *f), g], h), i, j, (), l = *range(20), [], 20
    a, b, *(c, *[d, *(e, *()), f], g), h, i, (), j = *range(9), [], 9

about attributeref
^^^^^^^^^^^^^^^^^^
- If a target is attributeref, LHS 一定是对 instance attribute 的 set 操作,
  右侧则可以是对 class or instance attribute 的 get 操作.::

    class Cls:
        x = 3
    inst = Cls()
    inst.x = inst.x + 1   # writes inst.x as 4 leaving Cls.x as 3

about slicing
^^^^^^^^^^^^^
- If a target is a slicing, (for builtin sequence types) the assigned object
  should also be a sequence object. Then the sequence object is asked to
  replace the slice with the items of the assigned sequence. The length of the
  slice may be different from the length of the assigned sequence, thus
  changing the length of the target sequence, if the target sequence allows it.

about evaluation order
^^^^^^^^^^^^^^^^^^^^^^
- LHS & RHS 的运算顺序: RHS 部分先计算完毕, 然后对 LHS target list 进行赋值.

  因此, 以下是成立的::

    a, b = b, a # swap a and b

- LHS target list 的运算顺序: target list 中, 各 targets 按从左至右的顺序赋值.

  例如::

    x = [1, 0]
    i = 0
    i, x[i] = x[i], i
    print(x) # [1, 0]
    
import statement
----------------

with statement
--------------
::

  with expression [as target] [, expression [as target]]+ : suite

注意若 expression 生成的 context manager 仅仅是为了 setup/cleanup context, 并无
binding 需要, 没必要使用 binding to ``as`` target. 这也为一些情况下, context
manager 的重用提供支持. 例如 RDBMS connection object 可以多次
BEGIN/COMMIT/ROLLBACK.

何时在 with 后面跟多个 context manager? 只有当 with 下面的 block 需要同时访问这
些 manager 提供的资源时, 才应该这样使用. 凡是资源的获取和释放有先后顺序, 不是必
须同时进行的, 都不应这样使用. 而是多个 with 嵌套.

exception handling
------------------

raise statement
^^^^^^^^^^^^^^^
::

  raise [<exception> [from <original-exc>|None]]

- Exception's context. When raising an exception in an ``except`` or
  ``finally`` clause ``__context__`` is automatically set to the last exception
  caught.

- Exception's cause. When raising a new exception in an ``except`` or
  ``finally`` clause, an exception that caused the raising exception can be
  supplied by ``from exc`` syntax. The causing exception will be set as
  ``__cause__`` attribute of raising exception, and ``__suppress_context__``
  will be set to True automatically.

- When exception is just instantiated, its ``__traceback__``, ``__cause__``,
  ``__context__`` 还都是 None (因为在实例化处本来就没有这些). 只有 raise 之后,
  解释器才会根据执行环境设置这三个属性.

- When traceback is printed,

  * ``__cause__`` is shown when it's not None, with indication::
   
      During handling of the above exception, another exception occurred.

  * ``__context__`` is shown if ``__cause__`` is not None. Otherwise it's shown
    with indication::

      The above exception was the direct cause of the following exception.

  * ``raise ... from None`` can be used to suppress context exception.
    
  * In other words, 如果有 cause, 不会显示 context; 如果没有 cause
    但是有 context, 会显示 context.

  * the exception itself is always shown after any chained exceptions are
    printed.

try statement
^^^^^^^^^^^^^

- A bare except clause matches ``BaseException``::

    try:
        pass
    except:
        pass
    # equivalent to
    try:
        pass
    except BaseException:
        pass
 
  which is a very bad practice.

- 何时该创建各种 exception class 并在出错时 raise 出来, 何时该只返回操作的
  true/false 结果?

  如果是错误、异常情况, 则 raise exception;
  如果是对命题是否成立的条件判断, 则给出 boolean result.

  两者是不同的情况. 然而, 两个情况可能存在相互嵌套. 例如, 通过条件判断是否通过来决定
  是否 raise exception; 通过是否 raise exception 来决定条件判断是否通过.

design patterns
^^^^^^^^^^^^^^^
- Create custom exception classes for your code, your library etc. Design a
  hierarchy suitable for your need.

- 所有自定义的 exception 都应是 ``Exception`` 的子类, 而不是 ``BaseException`` 的.
  Catching subclasses of ``BaseException`` is almost always the wrong thing to do.

- When catching exceptions, mention specific exceptions whenever possible instead
  of using a bare ``except:`` clause. If you want to catch all exceptions that
  signal program errors, use ``except Exception:`` (Bare except is equivalent to
  ``except BaseException:``).

- Design exception hierarchies based on the distinctions that code catching the
  exceptions is likely to need, rather than the locations where the exceptions
  are raised. Aim to answer the question "What went wrong?" programmatically,
  rather than only stating that "A problem occurred".

- For all try/except clauses, limit the try clause to the absolute minimum amount
  of code necessary. This avoids masking bugs.

function definitions
--------------------

- 避免使用递归逻辑. 这是因为 Python 中没有对 tail recursion 进行优化. 所以递归调用
  都是实实在在地叠加 stack. 如果可能递归次数很多, 很快会触及 ``sys.getrecursionlimit()``
  的上限, 导致 ``RecursionError``.
   
  解决办法:
  
  * 将递归逻辑转变成循环逻辑来实现.

  * 使用一个修改的 Y combinator 将递归算法转变成非递归算法 [SOPyRecur]_, 将运算结果以
    函数返回, 再循环 unwrap 每层函数. See also tco module [TCO]_.


class definitions
-----------------

- class lexical scope 的内容对 inner scope 从来不会直接可见. 在除了 class
  lexical scope 本身的任何地方, 访问 class scope 的内容, 都必须通过直接或间接
  访问 class namespace 本身, 然后再 resolve 至其中的内容.

  例如,

  .. code:: python

    class A:
        x = 1

        class B:
            # NameError
            print(x)
            # ok
            print(A.x)

        def y(self):
            # ok
            print(self.x)

  ``A.x`` 是直接访问, ``self.x`` 是间接访问.

- 什么时候应该规定使用 factory function 来获取类实例, 什么时候不需要这层封装
  只简单地对类进行实例化就行?

  factory function 相对于类的 constructor, 其根本特点是可以对返回实例的逻辑进行
  自定义, 而 constructor 简单地每次调用生成一个新实例. 例如, 使用 factory function
  可以做到:

  * 条件性生成新实例, 例如依据 identifier 存储实例, match 时只返回原来生成的实例.

    何时需要考虑条件性生成新实例呢? 当实例应该具有某种全局存在性质, 而不是某个
    其他类的实例的属性, 或者局限于某个范围. 例如 Logger 就应该是全局的, 不属于某个
    类, 对于一个 module 而言应该唯一, 因此以 module.__name__ 作为标识符来条件性
    生成新实例. 相应地, 数据库连接等 client object (例如 MongoClient) 往往不需要
    全局存在, 而是作为某个其他类对象的一部分, 在该类对象生成时创建连接状态, 析构
    时消除状态.

  * 需要对实例进行额外的修改, 且这些修改在逻辑上不是该类的一部分.

assertion statement
-------------------
::

  assert expression1[, expression2]

- 用于任何需要进行中断式声明判断的情况, 而不是正常程序逻辑的条件判断. 例如,

  * 单元测试.

  * debug code 部分.

- expression1 is used in boolean context (as test), expression2 if present is
  argument of ``AssertionError``.

- Assertions is run under normal interpreter invocation, and skipped if
  interpreter is run with optimization (``__debug__ == False``).

iterable and mapping unpacking
==============================

- builtin types 的 unpacking 似乎是直接访问内部存储的. 而不会访问 python-level
  的 iterable/mapping protocol 各个方法.

iteration, generation and asynchronous programming
==================================================

generator function
------------------

- Generator function 的重要意义在于两点:
  
  * 简化对 iterable protocol 的实现流程. 手动构建 iterable 需要处理:
  
    - 构建含 ``__iter__`` 方法的 iterable 类
     
    - 构建包含 ``__next__`` 方法的 iterator 返回值
     
    - 手动维持 iterator 内部状态.

    这些麻烦通过 generator function (yield) & interpreter magic 可以方便地解决.

    注意, generator function is not inherently more CPU/memory efficient than
    manually defined iterables, when generating a large sequence of values.
    无论是 generator 还是 iterator, 写好了都可以高效, 也都可以低效.

  * 为基于 async/await 的单线程异步编程范式提供基础. (注意 generator or async/await
    等高级语言机制并不是实现单线程异步的必要条件, 但是会很方便, 通过 event 机制同样
    可以做到.)

- 基于 generator function + promises 已经可以实现比较方便的单线程异步编程, 但
  async/await 将它升华成了语言 builtin 的一种范式. 通过提供语言层的基础性支持,
  无需手动实现 所需机制, 从而更统一 (所有人用一样的实现) 更高效 (在解释器中去优化,
  在 C/C++ 层优化).

generator
---------
- generator workflow.
  
  When generator function is called, a generator iterator is generated. 这个
  iterator 封装了 generator function body 编译后的等价逻辑.

  generator 的抽象执行逻辑:
  
  * 调用 ``__next__``, ``send()``, ``throw()`` 等方法, generator 开始执行.

  * 到 yield 后, 返回至 caller, 并给出 yield 值.

  * caller 再次调用上述控制方法, 进入 generator context, 从 yield 处继续执行.

  * generator function 结束时, raise ``StopIteration(<retval>)``, 结束 generator
    执行.

  这种 execution context 和控制权的交替执行, 是逻辑上的描述. 在内存中并不存在一个保留的
  generator function stack, 也不能让执行流在两个 stack 之间交替. 它本质上是解释器根据
  编译 generator function body 结构, 生成了一个等价的 iterator, 它来维持 generator 的
  内部状态.

- A generator object is both an iterator and iterable.
  Its ``__iter__`` method simply returns itself.

async, await
------------
- async/await 机制提供了 builtin 的完整的单线程异步编程的解决方案. 避免了通过 generator
  + promises, 甚至是更基础的机制 (e.g., event + callback) 去手动实现单线程异步所缺失的部分.

built-in exception hierarchy
============================
::

  BaseException
   +-- SystemExit
   +-- KeyboardInterrupt
   +-- GeneratorExit
   +-- Exception
        +-- StopIteration
        +-- StopAsyncIteration
        +-- ArithmeticError
        |    +-- FloatingPointError
        |    +-- OverflowError
        |    +-- ZeroDivisionError
        +-- AssertionError
        +-- AttributeError
        +-- BufferError
        +-- EOFError
        +-- ImportError
        |    +-- ModuleNotFoundError
        +-- LookupError
        |    +-- IndexError
        |    +-- KeyError
        +-- MemoryError
        +-- NameError
        |    +-- UnboundLocalError
        +-- OSError
        |    +-- BlockingIOError
        |    +-- ChildProcessError
        |    +-- ConnectionError
        |    |    +-- BrokenPipeError
        |    |    +-- ConnectionAbortedError
        |    |    +-- ConnectionRefusedError
        |    |    +-- ConnectionResetError
        |    +-- FileExistsError
        |    +-- FileNotFoundError
        |    +-- InterruptedError
        |    +-- IsADirectoryError
        |    +-- NotADirectoryError
        |    +-- PermissionError
        |    +-- ProcessLookupError
        |    +-- TimeoutError
        +-- ReferenceError
        +-- RuntimeError
        |    +-- NotImplementedError
        |    +-- RecursionError
        +-- SyntaxError
        |    +-- IndentationError
        |         +-- TabError
        +-- SystemError
        +-- TypeError
        +-- ValueError
        |    +-- UnicodeError
        |         +-- UnicodeDecodeError
        |         +-- UnicodeEncodeError
        |         +-- UnicodeTranslateError
        +-- Warning
             +-- DeprecationWarning
             +-- PendingDeprecationWarning
             +-- RuntimeWarning
             +-- SyntaxWarning
             +-- UserWarning
             +-- FutureWarning
             +-- ImportWarning
             +-- UnicodeWarning
             +-- BytesWarning
             +-- ResourceWarning

BaseException
-------------

attributes.

- ``args``. constructor arguments.

methods.

- ``with_traceback(tb)``. raise exception with new ``__traceback__``.

- ``__str__()``. By default, exception's string form is ``repr()`` of
  its ``args`` attribute.

LookupError
-----------
- When both IndexError and KeyError are expected, LookupError should be used
  instead.

ImportError
-----------
- 包含两种情况:

  * a module can not be loaded.
    
    - For a more specific error where a module can not be found,
      ModuleNotFoundError subclass is raised.

  * a name in a module can not be loaded.

OSError
-------
For a syscall returning a system-related error.

constructor:

- ``OSError(errno, strerror, [filename [, winerror [, filename2]]])``.
  The constructor often actually returns a subclass of OSError, depending on
  ``errno``. This behavior is not inherited by subclasses.

attributes.

- ``errno``. C errno.

- ``strerror``. C strerror().

- ``filename``, ``filename2``. For exceptions that involve a file system path.
  For functions that involves two paths, ``filename2`` is set, like
  ``os.rename``.

Warning
-------
Warnings are all exceptions.

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

- ``super([type[, object_or_type=None]])``. super object constructor.

  Return a proxy object that delegates attributes access to a parent or sibling
  class of type. 尽管一般用于获取 overrided method, 但必须清楚, super 的作用是
  将 ``getattr`` 的起点拉高到了 parent class 中, 所以 class attribute & method
  都可以获取.

  注意 super class 有自定义的 ``__getattribute__``, 决定属性行为.

  参数和意义:

  * 若两个参数都省略, ``super()`` 必须出现在 method definition 内部, 否则 raise
    RuntimeError. 此时, ``super()`` 相当于 ``super(__class__, <first-arg>)``.
    其中 ``__class__`` 是解释器在编译过程中加入的 implicit reference to lexically
    current class. ``<first-arg>`` 是函数的第一个参数, 即 self or cls (classmethod).

  * 若只有一个参数, 第二参数省略 (None), the super object is unbound. This is
    actually historical and **USELESS**.
    http://www.artima.com/weblogs/viewpost.jsp?thread=236278

  * 若第二个参数是 a subclass ``type2`` of ``type``. 此时, 访问
    ``super(type, type2).x`` 给出的是定义在父类中的 function ``x``, 或者说
    unbound method ``x``. 这可用于在子类 classmethod 中访问父类的相同 classmethod
    (此时 type2 也是 type). 若在 class definition 之外单独使用, 则只是给出 type
    的父类的 function 而已, type2 并无别的意义.

  * 若第二个参数是 a instance ``instance`` of ``type``. 此时,
    ``super(type, instance).x`` 给出的是 bound method ``x``, bound to
    ``instance``, i.e. ``self=instance``.

  一般情况下在类里面使用无参形式 ``super()`` 访问父类成员. 两个参数形式的一个
  用处是明确指定 MRO 的起点, 例如要绕过 parent class 去访问 grandparent 的成员.
  (但也许这是一个信号: 应该抽象出一个共同的基类, 再分别继承后实现各自所需.)

builtin types
=============

text sequence type - str
------------------------

methods
^^^^^^^

- ``isidentifier()``. 检查字符串是否是合法的 python identifier.
  Use ``keyword.iskeyword()`` tests for reserved keywords.

- ``join(iterable)``.

  * 虽然 ``somelist.join("...")`` 貌似更合理, 但是实际上并不是这样. 这是因为
    1) any iterable can be joined, 显然把 join logic 放在 str class 中实现是
    最统一的方式; 2) join logic is tightly coupled with str object's internals.

- ``__mod__(arg)``. 字符串的 modulo operation 即 string formatting.
  See `docs <https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting>`_.
  对于 ``format % value``:

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

  * BNF notation. see
    `docs <https://docs.python.org/3/library/string.html#format-string-syntax>`_.

  * literal ``{}`` ``{{}}``

  * field can be referenced by digit and key index. 对于顺序的 positionals,
    可以 omit digit. 然后可以进一步指定 ``.`` attribute 或 ``[]`` element.

    field name is not quoted.

  * 获取到的值可进一步通过 ``!rsa`` 转换, 以及 ``:`` 进行 formatting.

  * A ``format_spec`` field can also include one-level nested replacement
    fields within it.

    - ``format_spec`` 会传入要 format 的对象的 ``__format__`` method. 只有
      对象的类本身实现了 ``__format__`` method, 并对传入的 format spec 能
      识别, 才会输出 format result. 否则应 raise TypeError. 以下格式, 是
      ``str.__format__`` 识别的格式.

      注意如果 format spec 之前包含 ``!{r|s|a}`` 转换部分, 转换结果即字符串
      的 ``__format__`` method will be called with ``format_spec``, 而不是原
      object 的方法.

    - BNF::

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

- ``title()``. In string, first char of each word is uppercased, and remaining
  chars are lowercased. A word is defined as groups of consecutive letters.

string formattings
^^^^^^^^^^^^^^^^^^
python 中有 4 种 string interpolation 的方式:

- ``%`` printf-style formatting. 即 modulo operation.
  implemented in ``str.__mod__``.

- ``str.format()``.

- formatted string literals. ``f"..."``.

- Shell-like string template: ``string.Template``.

第一种最常见最简单, 但不如第二种方便;

第二种明显优点有 2 个, 1) 灵活方便, 功能丰富; 2) 使用 `__format__` protocol
可以自定义 format 逻辑, 实现多态性的封装 (duck typing), e.g., datetime.

第三种克服了第二种的 verbosity 问题, 并且增加灵活性可以执行 python 表达式.
所以, 对于 py3.6+, 应该用第三种, 之前的最好用第二种.

第四种仅用在特殊场合, 例如为了填充使用了 shell syntax 的模板, 或者为了与常见的
formatting 语法相区别.

set types - set, frozenset
--------------------------
- elements must be hashable.

- ``set`` is mutable, unhashable. ``frozenset`` is immutable and hashable.

operations
^^^^^^^^^^
the non-operator versions methods will accept any iterable as an argument.
In contrast, their operator based counterparts require their arguments to be
sets. 然而两种方式并没有效率上的区别, 因为虽然接受任何 iterable, 但是仍然
会在内部转换成 set 再进行比较.

set & frozenset instances can be mixed for binary operations. The returned
value is instance of first operand's type.

Common operations
""""""""""""""""""

- ``__len__()``, ``len()``.

- ``__contains__()``, ``in``.

- ``issubset()``, ``<=``. 注意 subset 判断是 ``<=`` 而不是 ``<``. 后者是
  subset proper, 严格子集.

- ``__lt__()``, ``<``. subset proper.

- ``issuperset()``, ``>=``

- ``__gt__()``, ``>``. superset proper.

- ``__eq__()``, ``=``. element-wise equality.

- ``isdisjoint()``.

- ``union()``, ``set | other | ...``

- ``intersection()``, ``set & other & ...``

- ``difference()``, ``set - other - ...``

- ``symmetric_difference()``, ``set ^ other``

- ``copy()``. shallow copy.

Set's mutable operations
""""""""""""""""""""""""

- ``update(*others)``, ``set |= other | ...``

- ``intersection_update(*others)``, ``set &= other & ...``

- ``difference_update(*others)``, ``set -= other | ...``

- ``symmetric_difference_update(other)``, ``set ^= other``

- ``add()``

- ``remove()``

- ``discard()``. remove if present.

- ``pop()``. pop arbitrarily.

- ``clear()``.

numeric types
-------------
- ``float`` type literal forms::

    NN.[NN]
    [0].NN
    # some exponential forms
    NN"e"NN
    NN"E"NN

  注意由于 ``NN.`` 是合法的 float number, digits 后面的第一个 ``.``
  会认为是 decimal point, 而不是 attribute reference. 例如::

    1.is_integer # SyntaxError
    (1).is_integer # OK
    1..is_integer # OK
    1.1.is_integer # Ok

mapping types
-------------

dict
^^^^
- Dictionaries compare equal if and only if they have the same ``(key, value)``
  pairs. 这说明:

  * key 之间和 value 之间的比较是通过 equality (``==``) 进行的.

- In Python 3.7+, Dictionaries preserve insertion order. Updating a key does
  not affect the order. Keys re-added after deletion are inserted at the end.

- Because dict preserves key's insertion order, ``collections.OrderedDict``
  is no longer necessary.

- dict 可以直接用来实现 ``OrderedSet`` 数据结构.

descriptor types
----------------

property
^^^^^^^^

- property and its alikes (``cached_property``, etc.) 是 python 对 attribute
  getter/setter methods 的一个清晰而简洁的解决方案.

- python 中不需要 getter/setter methods. 只需要对外开放的 attributes 以及
  property. 通过使用 property, 一个简单的 attribute 数据可以 transparently
  transform into a complex getter/setter combo, 而不做任何 API 改动. 仍然
  保持整洁、简单.

- 这种从 data attribute 与 getter/setter 的透明切换可以看作是 dynamic language
  的一个 feature, 这是 compiled language 不具有的.

built-in constants
==================

runtime constants
-----------------

- ``__debug__``. True if Python is not started with optimization (-O, -OO
  options).

References
==========
.. [PythonFAQ] `Why is Python a dynamic language and also a strongly typed language? <https://wiki.python.org/moin/Why%20is%20Python%20a%20dynamic%20language%20and%20also%20a%20strongly%20typed%20language>`_.
.. [SOPyRecur] `Using Y combinator to optimize tail recursion in Python <https://stackoverflow.com/a/18506625/1602266>`_
.. [TCO] `TCO module <https://github.com/baruchel/tco>`_
.. [SOPyChangeClass] `How dangerous is setting self.__class__ to something else? <https://stackoverflow.com/questions/13280680/how-dangerous-is-setting-self-class-to-something-else>`_
.. [SOPyNew] `Why isn't __new__ in Python new-style classes a class method? <https://stackoverflow.com/questions/9092072/why-isnt-new-in-python-new-style-classes-a-class-method>`_
