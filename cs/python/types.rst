overview
========
- dynamic type creation utilites

- exposing extra builtin types that are more obscure and are not available in
  ``builtins`` module.

- some weird misc "convenient" classes.

type creations
==============
- ``new_class(name, bases=(), kwargs=None, exec_body=None)``.

  * 这个函数的好处主要在于它会根据 ``bases`` 自动选择合适的 metaclass 来创建
    class object. 若直接调用 ``type()`` 则固定使用 ``type`` metacalss.

  * ``kwargs`` 相当于 class definition block 的 header 中的 kwargs 部分.  所以
    如果这里包含 ``metaclass`` key, 会直接使用这个作为 metaclass.

  * ``exec_body`` is a callable to populate class namespace as returned by
    ``metaclass.__prepare__``. The callable must modify the passed in namespace
    in-place. 这么设计是因为 class namespace 的类型是由 ``__prepare__`` 决定的.

- ``prepare_class(name, bases=(), kwargs=None)``.  calls ``__prepare__`` of the
  resolved metaclass. returns a 3-tuple of ``(metaclass, namespace, kwds)``.
  ``kwds`` is a copy of ``kwargs`` with ``metaclass`` removed.

- ``resolve_bases(bases)``. return a tuple of resolved bases.

extra builtin types
===================
- FunctionType

- LambdaType. subclass of FunctionType.

- MethodType. bound method.

- BuiltinFunctionType, BuiltinMethodType. they are the same thing.

- WrapperDescriptorType. type of unbound method of some builtin types.

- MethodDescriptorType. type of unbound method of some builtin types.

- ClassMethodDescriptorType. type of unbound classmethod of some builtin types.

- MethodWrapperType. type of bound method of some builtin types.

- GeneratorType. generator iterator.

- CoroutineType. coroutine.

- AsyncGeneratorType.

- CodeType. code objects.

- ModuleType. module objects.

  * ``ModuleType(name, doc=None)``. useful when you need to create a module
    dynamically. E.g., ``six`` uses this to fake module structures.

- TracebackType.

  * ``TracebackType(tb_next, tb_frame, tb_lasti, tb_lineno)``.

- FrameType. frame objects in traceback.

- GetSetDescriptorType. C-level equivalent property type.

- MemberDescriptorType. type of class member definitions, such as members
  defined by ``__slots__``, or at C-level.

- MappingProxyType. Read-only proxy of a mapping. It provides a dynamic view on
  the mapping’s entries.

  * ``MappingProxyType(mapping)``. can be used to create proxy of a mapping.

  * ``__dict__`` attribute of classes are of this type.

  * 具有 ``collections.abc`` 相同的 APIs 以及 dict 的其他 non-modification 类型
    方法.

misc utillities
===============

SimpleNamespace
---------------
::

  SimpleNamespace(**kwargs)

- 可以用于集成一组任意的 key-value, 功能上与一个 dict 并无本质区别, 只是在
  access key-value 时稍方便一点.

- SimpleNamespace's ``repr()`` is useful.

- 实际上 SimpleNamespace 是 ``sys`` module 内部使用的一个 C-level record type.

  .. code:: python

    SimpleNamespace = type(sys.implementation)

- 用 ``SimpleNamespace`` 来方便地实现可以同时以 attribute 和 key 两种方式访
  问的 mapping:

  .. code:: python

    class DictNamespace(SimpleNamespace):
        def __getitem__(self, k):
            return self.__dict__[k]
        def __setitem__(self, k, v):
            self.__dict__[k] = v
        def __delitem__(self, k):
            del self.__dict__[k]

DynamicClassAttribute
---------------------
::

  DynamicClassAttribute(fget=None, fset=None, fdel=None, doc=None)

- 与 property 的用法和意义相同.

- 不同之处在于, 当在 class 中访问该属性时 (即 "ClassAttribute" 之名), 
  会 raise AttributeError, 从而 redirect to ``__getattr__`` (if defined),
  以动态给出合适的 (表征) 属性值.

- 也就是说, 这个 descriptor 应该配合 custom ``__getattr__`` method 来使用.

coroutine
---------

- ``coroutine(gen_func)``.

  .. TODO understand this
