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
