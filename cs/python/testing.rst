overview
========

- 单元测试时, 应该进一步开启所有 python warnings.::

    python -Wall ...

unittest
========

- What tests are put in one TestCase? What counts a new ``test_`` function?
  When to create a new TestCase? How to classify tests?

- why use ``assert*`` methods instead of assert statement?

- random notes:

  * Any method starts with ``test_`` is a test method.

  * ``test_`` method needs descriptive name for what it tests. Length is not
    a concern here.

  * setUp and tearDown is like context manager. If setUp raises exception,
    tearDown does not run.

  * ``fail`` method fails a test case unconditionally. When author hasn't
    finished written a test case, fail method can be used to signify unconditional
    failure.

unittest.mock
=============

- random notes:

  * Be careful when using ``Mock`` object's special assert methods. Unless you
    get the magic method name exactly right, then you will just get a "normal"
    mock method, which just silently return another mock, and you may not
    realise that you’ve written a test that tests nothing at all.

factory boy
===========

overview
--------
- A fixture tool.

- The purpose of factory_boy is to provide a default way of getting a new
  instance, while still being able to override some fields on a per-testcase
  basis.  从而 DRY, 避免了重复相同的部分.

- 支持 Django, Mogo, MongoEngine, SQLAlchemy ORMs.

- Factory declaration is like django model.

- multiple build strategies.

- Multiple factories per class support, including inheritance.

Factory
-------

- A factory is associated with a model, and it declares a set of fields and
  their values.

Create a model factory
^^^^^^^^^^^^^^^^^^^^^^

Basic procedure:

1. subclass ``Factory`` class or one of its ORM subclasses.

2. add ``class Meta:`` inner class, setting ``model``.

3. Add default values for fields to pass to the associated model's
   constructor.

factory inheritance
^^^^^^^^^^^^^^^^^^^

- A model factory can be subclassed to a more specific version or modified
  version.

methods
^^^^^^^
- A Factory class's constructor call is the same as calling the factory's
  default strategy.

- ``build(**kwargs)``. a build strategy where the instance is not saved. fields
  can be customized by ``kwargs``.

- ``create(**kwargs)``. a build strategy where the instance is saved.

- ``stub(**kwargs)``. a build strategy where a stub object is created, which is simply
  a namespace object with declared attributes.

- ``build_batch(n, **kwargs)``. build a batch of objects.

Meta options
^^^^^^^^^^^^

- ``model``. factory's model class.

- ``inline_args``. specify which of the attributes should be passed as
  positional arguments (rather than kwargs) into model constructor.

- ``strategy``. factory's default strategy.

lazy attributes
---------------
- Some attributes (such as fields whose value is computed from other elements)
  will need values assigned each time an instance is generated.

LazyFunction
^^^^^^^^^^^^
- Useful when the value of a field is determined dynamically. So it can be 
  simulated by a function.

- Use this if the value logic is not related to the model instance.  Otherwise
  use LazyAttribute.

LazyAttribute
^^^^^^^^^^^^^

- When the value of a field is determined dynamically and related to the
  specific instance.

- ``lazy_attribute()`` decorator.

Sequential values
-----------------

Sequence
^^^^^^^^
- Useful when a field has unique constraint, so a sequential value ensures
  that there is no collision.

- ``sequence()`` decorator

Relational attributes
---------------------

SubFactory
^^^^^^^^^^

RelatedFactory
^^^^^^^^^^^^^^

Parameters
----------

Traits
------

Strategies
----------

- built-in strategies

  * build. instantiate a model instance.
  
  * create. build and save it to database.

- During factory call, the strategy of the related factories will use the
  strategy of the parent factory.

- A factory's default strategy can be set by ``Meta.strategy`` attribute.

ORMs
----
对于配合不同的 ORM 使用时, 需要使用不同的 Factory subclass. 这些子类对
每个 ORM 的特性有个性化的处理.

django ORM
^^^^^^^^^^

DjangoModelFactory
""""""""""""""""""
- factory.django.DjangoModelFactory.

- ``create`` strategy uses ``Model.objects.create()`` or
  ``Model._default_manager.create()``.

- If the factory contains at least one ``RelatedFactory`` or ``PostGeneration``
  attributes, the base object will be ``.save()``-ed again to update fields
  possibly modified by post-generation hooks.

DjangoOptions
"""""""""""""
DjangoModelFactory automatically use DjangoOptions as its Meta inner class.

该 Meta class 支持以下特性

- ``Meta.model`` 支持指定字符串形式的 ``app_label.Model``

- ``Meta.database`` specify the database to use.

- ``Meta.django_get_or_create``. Specify the fields to be used for
  filtering in ``Model.objects.get_or_create()``. 指定这个属性后, 创建 instance
  会使用 ``get_or_create()``, 而不使用 ``create()``.

extra attribute classes
""""""""""""""""""""""""

- FileField.

- ImageField.

disabling signals
""""""""""""""""""
- If signals are used to create related objects, they may interfere with
  RelatedFactory. 如果一个 factory 中指定了 RelatedFactory, (反向) 相关联
  的实例也会自动创建, 这是由 factory boy 实现的. 所以在 django 系统中设置
  的 signal 就需要 disable 掉.

- ``mute_signals(signal1, ...)``. a decorator and context manager.

Debugging
---------

- Detailed logging is available through the ``factory`` logger.

- ``factory.debug()`` context manager.

.. code:: python

  with factory.debug():
      obj = TestModel2Factory()
  
  import logging
  logger = logging.getLogger('factory')
  logger.addHandler(logging.StreamHandler())
  logger.setLevel(logging.DEBUG)
