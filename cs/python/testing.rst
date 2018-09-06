overview
========

- 单元测试时, 应该进一步开启所有 python warnings.::

    python -Wall ...

unittest
========
- random notes:

  * ``fail`` method fails a test case unconditionally. When author hasn't
    finished written a test case, fail method can be used to signify unconditional
    failure.


terms
-----
- test failure and test error.

  * failure. a known assertion error (likely AssertionError), meaning the test
    failed.

  * error. an unknown logical error (anything else), meaning the test aborted.

test structure
--------------
- test hierarchy.

  * A ``TestSuite`` is a collection of test cases that tests all functionalities,
    features of a module.
  
  * A ``TestCase`` is a set of related test cases that collectively tests
    certain unit (which probably implements a functionality/feature).

  * A test method is a single test case that checks whether the UUT passes a
    particular criterion.

而对于该功能的各方面的具体测试, 则写成 test method.

- A testcase is created by subclassing ``TestCase`` or instantiate
  ``FunctionTestCase``.

  * Each test of a test case is a method whose name starts with
    ``TestLoader.testMethodPrefix``.

  * In test methods, ``assert*`` methods are invoked to actually test stuffs.

test cases
----------

TestCase
^^^^^^^^

logic
"""""
- 当定义 TestCase 时, 一个 TestCase 是一系列实际要执行的 test cases (以 method
  形式定义) 的集合. 这是一个抽象 grouping 级别.

- 当实例化后, 每个 TestCase instance 实际上只执行 class body 中定义的一个 test
  method. (这证明了 TestCase 只是一个方便的抽象集合.) 所有相关的 fixture 等
  utils 只为这一个 test method 服务.

constructor
"""""""""""
- ``methodName='runTest'``. 当 TestCase 实例化时, 它要测试的 test method.

class attributes
""""""""""""""""
- ``failureException``. the exception class of assertion error.

- ``longMessage``. True is the default value. In this case, the custom message
  is appended to the end of the standard failure message. When set to False,
  the custom message replaces the standard message.

  can be overridden in individual test methods by assigning an instance attribute.
  It gets reset before each test call.

- ``maxDiff``. maximum length of diffs output. default 80*8. set None for
  unlimited.

running test
""""""""""""
- ``run(result=None)``. run tests. collect test results into ``result`` if
  passed in, or return a new TestResult.

fixture methods
""""""""""""""""
- see `test fixtures`_.

common assertion methods
""""""""""""""""""""""""
unittest 使用 custom assertion methods 而不是 ``assert`` statement, 这是为了
更方便地控制 assertion 的执行和结果收集.

- ``assertEqual(a, b, msg=None)``. For arguments of known types, dispatch
  equality checkings to `type-specific assertion methods`_.

- ``assertNotEqual(a, b, msg=None)``

- ``assertAlmostEqual(a, b, places=7, msg=None, delta=None)`` and
  ``assertNotAlmostEqual(a, b, places=7, msg=None, delta=None)``.
  The difference of a and b, is smaller than ``places`` decimal places
  (``10^-n``) or ``delta``. Only one of ``places`` and ``delta`` can be
  specified. ``delta`` is useful when the difference is not a real number.

- ``assertGreater(a, b, msg=None)``,
  ``assertGreaterEqual(a, b, msg=None)``,
  ``assertLess(a, b, msg=None)``,
  ``assertLessEqual(a, b, msg=None)``.

- ``assertTrue(x, msg=None)``

- ``assertFalse(x, msg=None)``

- ``assertIs(a, b, msg=None)``

- ``assertIsNot(a, b, msg=None)``

- ``assertIsNone(x, msg=None)``

- ``assertIsNotNone(x, msg=None)``

- ``assertIn(a, b, msg=None)``

- ``assertNotIn(a, b, msg=None)``

- ``assertIsInstance(a, b, msg=None)``

- ``assertNotIsInstance(a, b, msg=None)``

- ``assertRegex(text, re, msg=None)``, ``assertNotRegex(text, re, msg=None)``.
  The ``re`` can be regex object or string.

- ``assertCountEqual(a, b, msg=None)``. Test two sequence (of any type) contain
  the same number of corresponding elements, regardless of order.

message assertion methods
"""""""""""""""""""""""""
- ``assertRaises(exc, func, *args, **kwargs)`` or  ``assertRaises(exc, msg=None)``.
  The test passes if the expected exception is raised, is an error if another
  exception is raised, or fails if no exception is raised.

  * ``exc`` can be a tuple of exception classes.

  * the second form returns a context manager. Its ``__enter__`` returns the
    context manager itself. After the context, it has the following attributes:

    - ``exception``. the caught exception.

- ``assertRaisesRegex(exc, r, func, *args, **kwargs)`` or ``assertRaisesRegex(exc, r, msg=None)``.
  ditto, but also tests ``r`` matches the string form of the raised exception.
  ``r`` can be a regex object or a string. ``r`` is ``re.search``-ed.

- ``assertWarns(warn, func, *args, **kwargs)`` or ``assertWarnsRegex(warn, msg=None)``.
  ditto for warnings.

  * context manager's attributes:

    - ``warning``. the caught warning.

    - ``filename``. the source file triggered the warning.

    - ``lineno``. the line number.

- ``assertWarnsRegex(warn, r, func, *args, **kwargs)`` or ``assertWarnsRegex(warn, r, msg=None)``.
  ditto with regex tests for warning messages.

- ``assertLogs(logger=None, level=None)``. at least one message is logged on
  the logger or one of its children, with at least the given level.
  ``logger`` is a Logger or its name string, default is root logger.
  ``level`` is a numeric logging level or its string equivalent, default
  is INFO.

  * context manager's attributes:

    - ``records``. A list of matched LogRecord.

    - ``output``. A list of matched output messages.

type-specific assertion methods
"""""""""""""""""""""""""""""""
- ``addTypeEqualityFunc(typeobj, function)``. register a function to check
  equality of instances of typeobj (not including subclasses).

- ``assertMultiLineEqual(a, b, msg=None)``. for comparing string. A diff
  is generated if differ.

- ``assertListEqual(a, b, msg=None)``, ``assertTupleEqual(a, b, msg=None)``.
  for list, tuple comparison.

- ``assertSetEqual(a, b, msg=None)``. for set, frozenset comparison.

- ``assertDictEqual(a, b, msg=None)``. for dict.

- ``assertSequenceEqual(a, b, msg=None, seq_type=None)``. for generic
  sequences.

utils
"""""
- ``fail(msg=None)``. fail the test unconditionally.

- ``addCleanup(function, *args, **kwargs)``. add an additional cleanup method
  at runtime. 用于当只有某个 test 需要的单独的或条件性的 cleanup 操作. It'll
  be called after ``tearDown()``. Functions will be called in reverse order to
  the order they are added.

- ``TestCase.subTest(msg=None, **kwargs)`` context manager.

  Used when some of your tests differ only by a some very small differences,
  for instance some parameters. 此时, 在一个 test method 中使用多个 subTest, 在
  测试结果中将一个 test method 展成多个测试结果, 每个对应一个 ``kwargs`` 的值.
  ``kwargs`` 的值会输出在相应的测试结果后面.

  在 subTest context manager 中, assertion error 不会 abort 这个 test method,
  只会退出这个 context, 执行下面的逻辑.

  subTest can be nested.

- ``skipTest(reason)``. see `skipping`_.

- ``debug()``.

internal APIs
"""""""""""""
- ``doCleanups()``. called unconditionally after ``tearDown()``, or after
  ``setUp()`` if ``setUp()`` raises an exception.

- ``countTestCases()``. the number of tests represented by this test case.
  Always 1 for TestCase instances.

- ``defaultTestResult()``. return a TestResult for ``run()``.

- ``id()``. a string identifying the TestCase instance. ``module.class.method``

- ``shortDescription()``. A description of the test. default first line of
  docstring of test method.

FunctionTestCase
^^^^^^^^^^^^^^^^
- A TestCase subclass, used to wrap an existing "legacy" test function so that
  it can be run by unittest.

- 注意 FunctionTestCase 不能直接 import 进入 test module 的 global namespace,
  因为它是 TestCase subclass, 这样会被认为是一个需要执行的 test case.

- FunctionTestCase 应该用在 test setup module 中, 而不是 test case modules 中.
  它的使用必须配合 manually created test suite and test runner. 例如:

  .. code:: python

    from test_module import testfunc

    TextTestRunner().run(TestSuite([FunctionTestCase(testfunc)]))

design patterns
^^^^^^^^^^^^^^^
- Isolation.
  
  * Each test (by TestCase method) must be self-contained and independent from
    other tests so that it can be run in isolation and mixed in any order with
    other tests.

  * Each test case must also be isolated from other test cases.

- Test methods.
  
  * Test methods need descriptive names for what they test. Length is not a
    concern here.

test fixtures
-------------
- In unittest, test fixtures are defined by ``setUp*``/``tearDown*`` functions
  and methods.

test method level fixtures
^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``TestCase.setUp()``. called immediately before calling the test method.

- ``TestCase.tearDown()``. called immediately after calling the test method.
  在 tearDown 中 raise 出来的 unexpected exception 会认为是一个额外的 error,
  这会增加 error count, 并在输出结果中增加一条 traceback.

Exceptions raised in setup/teardown phase of a test method results in failure
or error of the related test.

``setUp()`` and ``tearDown()`` works like enter/exit of a context manager:

* If ``setUp()`` succeeded, ``tearDown()`` is run regardless of the result of
  the test method.

* If ``setUp()`` failed, ``tearDown()`` does not run.

test case level fixtures
^^^^^^^^^^^^^^^^^^^^^^^^
- ``TestCase.setUpClass()``. a class method.

- ``TestCase.tearDownClass()``. ditto.

When the test suite encounters a test from a new class then ``tearDownClass()``
from the previous class (if there is one) is called, followed by ``setUpClass()``
from the new class.

If there are any exceptions raised during setup of the case level fixture
functions the entire test case is not run, and teardown is not run.

The failed fixture method is reported as an error.

test suite level fixtures
^^^^^^^^^^^^^^^^^^^^^^^^^
- ``setUpModule()``

- ``tearDownModule()``

If a test is from a different module from the previous test then
``tearDownModule()`` from the previous module is run, followed by
``setUpModule()`` from the new module.

If there are any exceptions raised during setup of the suite level fixture
functions the entire test suite is not run, and teardown is not run.

The failed fixture function is reported as an error.

design patterns
^^^^^^^^^^^^^^^
- Use proper `test fixtures`_ to prepare environment common to *all* tests
  under a specific scope (test method level, test case level, test suite level,
  etc.)

- If not *all* test methods in a TestCase needs a common setup/teardown logic,
  you should either setup/teardown in those methods who need this (例如使用
  manual setup/teardown, 以及使用 ``TestCase.addCleanup()``); or move those who
  don't into another TestCase.

- Shared fixtures (test case level and test suite level fixtures) are not
  intended to work with suites with non-standard ordering. If you randomize the
  order, so that tests from different modules and classes are adjacent to each
  other, then these shared fixture functions may be called multiple times in a
  single test run.

- Shared fixtures break test isolation. They should be used with care.

skipping tests and expected failures
------------------------------------
- 这些 decorator 都可以 decorate a single test method or an entire test case.

skipping
^^^^^^^^
- ``@skip(reason)``. A decorator that marks the decorated test method or test
  case should be skipped unconditionally. 这是当你需要 disable 一个测试的时候
  来使用. 可能是因为短期内没时间去处理相应的问题, 或者其他原因, 你选择让这个
  测试先跳过. ``reason`` 是提供你决定 skip test 的原因. 在 verbose mode 中,
  ``reason`` is printed.

- ``@skipIf(condition, reason)``. ditto for conditional skipping. 这用于根据环
  境情况来选择是否执行某些测试. 例如当软件需要兼容多个环境, 而一些测试是
  environment-specific 的时候.

- ``@skipUnless(condition, reason)``. ditto, in reverse.

- ``SkipTest(reason)``. skip a test when this exception is raised. 
  
  唯一需要 Explicitly raise this exception 的情况是在 at module level. 这样会
  skip the entire test suite.

- ``TestCase.skipTest(reason)``. fine-grained skipping at test runtime.

  这主要用在 test method body 中, 根据 runtime 情况选择性地 skip current test.

- test fixture with ``SkipTest``.
  
  * 使用 decorator 来标记要 skip 的 test method/case 时, skipped test
    method/case will not have setup/teardown fixtures run around them.

  * 在 module-level raise ``SkipTest`` exception 时, 该 module 整个 test suite
    的 ``setUpModule()`` and ``tearDownModule()`` won't run.

  * 在 test fixture 中, raise ``SkipTest`` 会 skip 当前的 test
    method/case/suite.

expected failure
^^^^^^^^^^^^^^^^
- ``@expectedFailure``. A decorator that marks the test is an expected failure.
  如果 test fails, 则在结果中 mark 为 expected failure; 如果 test 没有 fail, 则
  mark 为 unexpected success.

design patterns
^^^^^^^^^^^^^^^

- Skipping 用于当作者决定在测试集中 skip a test method/case 的时候.  这个 skip
  不是因为测试没完成或者对应的实现还没完成, 而是基于一种考虑、选择和设计.

- ``@expectedFailure`` 用于当需要临时标记 failure is expected 的时候, 例如当
  test body 还没有完成时. 注意你是准备要完成测试以及对应的功能实现的. 也就是说
  你是准备将 expected failure 变成 expected success 的, 你准备当一切都完成之后
  将这个 decorator 去掉.

test suite
----------
- In unittest, a ``TestSuite`` is a collection of test cases, or a mixture of
  hierarchical test suites and test cases.

TestSuite
^^^^^^^^^
- A test suite can be run in the same way as a test case by test runner.
  They are used to aggregate tests into groups of tests that should be run
  together. 

- Running a TestSuite instance is the same as iterating over the suite, running
  each test individually.

constructor
"""""""""""
- ``tests``. a sequence of test cases and test suites to be added to this
  test suite initially.

methods
"""""""
- ``addTest(test)``. Add a TestCase or TestSuite.

- ``addTests(tests)``.

- ``run(result)``. same as TestCase.

- ``debug()``. same as TestCase.

- ``countTestCases()``. the number of test cases in this suite, recursively.

- ``__iter__()``. iterate the tests in this suite.

test loader
-----------
TestLoader
^^^^^^^^^^
- TestLoader is used to load test suites from modules.

test result
-----------
- stores the results of a set of tests.

TestResult
^^^^^^^^^^

attributes
""""""""""
- ``errors``.

test runner
-----------
- A test runner is a component which orchestrates the execution of tests and
  provides the outcome to the user.

CLI
---

testing module as script
^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

  if __name__ == "__main__":
      unittest.main()

unittest as cli tool
^^^^^^^^^^^^^^^^^^^^
run individual testing modules
""""""""""""""""""""""""""""""
::

  python3 -m unittest [test]...

- Each ``test`` positional can be a testing module or file path to testing
  module, fully qualified name to test case classes and test methods.

  * When zero ``test`` is specified, test discovery is initiated.

  * When using file path as ``test`` target, The file specified must still be
    importable as a module. The path is converted to a module name by removing
    the ‘.py’ and converting path separators into ‘.’

  * 由于允许使用 file path, 所以 specifying shell glob is possible.

- options.

  * ``-v``. verbose output including test method name, import path, and result.

  * ``-c``. first ctrl-c waits current test completion then reports results so
    far. A second ctrl-c aborts execution immediately.

  * ``-f``. fail fast.

  * ``-k <pattern>``. Only run test methods and classes that match the pattern.
    A pattern is a substring containing ``*`` metachar, which matches against
    the fully qualified test method name as imported by the test loader.

  * ``--locals``. show locals in traceback. useful when rerunning tests aren't
    easy, e.g. in CI environment.

test discovery
""""""""""""""
::

  python3 -m unittest discover [<start-directory>] [<pattern>] [<top-directory>]

- all of the test files must be modules or packages (including namespace
  packages) importable from the top-level directory.

- options.

  * all options from parent ``unnitest`` parser.

  * ``-s <directory>``. starting directory. default cwd. This option is the
    same as the positional arg.

  * ``-p <pattern>``. pattern matching test files to be discovered. This option
    is the same as the positional arg.

  * ``-t <directory>``. top-level directory used as the root directory of
    package/module import. 也就是说, top-level directory 加入 ``sys.path`` 中.
    这对 relative import 的解析是关键的. default to start directory. This
    option is the same as the positional arg.

- The start directory can also be an importable module name, regardless where
  it is on the filesystem, as long as it can be imported by python in cwd.

unittest.mock
=============

- random notes:

  * Be careful when using ``Mock`` object's special assert methods. Unless you
    get the magic method name exactly right, then you will just get a "normal"
    mock method, which just silently return another mock, and you may not
    realise that you’ve written a test that tests nothing at all.

  * patch 直接使用的地方, 这样是最可靠的, 而且是影响最小的; 不要 patch 定义的地方,
    因为不可靠, 在使用处的 import 可能比 patch 应用要早, 这样就会 patch 失败.

  * 关于对 module level 和 top-level class attributes 等依赖的处理. 如果需要考
    察相应依赖的行为, 则需要 mock, 否则就没必要 mock. 无论是否要 mock, 必须首先
    要避免 ImportError. 如果依赖项还不存在, 至少要创建一个相应的 placeholder,
    否则就会有 ImportError, 导致单元测试逻辑无法进行.

  * autospec is useful to enforce the correct contract between boundaries. 这是
    对 isolation 导致的集成问题的一部分解决方案 (另一部分解决方案则是更加整体性
    的测试. 对于 UT 导致的 isolation 问题, 则需要 IT 去解决. IT 导致的
    isolation 问题通过 ST 解决). 无论这个 boundary 是模块之间的 boundary
    (mocked in UTs), 还是服务和组件之间的 boundary (mocked in ITs).


doctest
=======

integration with unittest
-------------------------
DocTestSuite

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

- ``create_batch(n, **kwargs)``.

Meta options
^^^^^^^^^^^^

- ``model``. factory's model class.

- ``inline_args``. specify which of the attributes should be passed as
  positional arguments (rather than kwargs) into model constructor.

- ``strategy``. factory's default strategy.

- ``exclude``. a list of attributes to exclude when creating model instances.
  例如当 factory class 中定义的一些列属性只是作为 helper attributes. 这与
  `Parameters`_ 有类似之处.

Parameters
^^^^^^^^^^
- Factory's ``Params`` inner-class 用于设置生成 model field 所依赖的参数.

- Parameters can be accessed during attribute resolution.

- 例如, 当多个 model field value 的生成具有一定的相关性, 依赖于几个共同的参数,
  则可以通过 Params class 来指定. 然后设置 field 使用 ``LazyAttribute`` 来生成.

Traits
^^^^^^


declarations
------------
- These are special class-level declarations.

lazy attributes
^^^^^^^^^^^^^^^
- Some attributes (such as fields whose value is computed from other elements)
  will need values assigned each time an instance is generated.

LazyFunction
""""""""""""
- Useful when the value of a field is determined dynamically. So it can be 
  simulated by a function.

- Use this if the value logic is not related to the model instance.  Otherwise
  use LazyAttribute.

LazyAttribute
"""""""""""""
- When the value of a field is determined dynamically and related to the
  specific instance.

- It takes as argument a function to call; that function should accept the
  object being built as sole argument, and return a value suitable for the
  field.

- 注意 the passed-in object is not an instance of model class, but a
  ``Resolver`` instance.

- The ``lazy_attribute()`` decorator is similar. The decorated function is
  the function to be called.

Sequence
^^^^^^^^
- Useful when a field has unique constraint, so a sequential value ensures
  that there is no collision.

- ``sequence()`` decorator

Relational attributes
^^^^^^^^^^^^^^^^^^^^^

SubFactory
""""""""""

RelatedFactory
""""""""""""""

post-generation hooks
^^^^^^^^^^^^^^^^^^^^^
- 在生成实例之后执行的进一步自定义处理和定义.

- usage examples.

  * 在生成实例后, 设置 ManyToMany relationship.

- Post-generation hooks are called in the same order they are declared in the
  factory class, so that functions can rely on the side effects applied by the
  previous post-generation hook.

- utils.
  
  * ``PostGeneration``. a BaseDeclaration subclass.

  * ``post_generation``. a decorator that functions exactly like PostGeneration
    class.

- define post-generation hook.

  * define a callback function in Factory class, of the form:

    .. code:: python

      @post_generation
      def callback(obj, create, extracted, **kwargs):
          pass

  * the name of callback function becomes a valid kwarg of Factory constructor.

  * During factory call, if the kwarg is passed value, it will become the
    value of ``extracted`` arg of the callback. Otherwise ``extracted`` is
    None.

  * Any argument starting with ``<callback>__<field>`` will be extracted, its
    ``<callback>__`` prefix removed, and added to the ``kwargs`` passed to the
    callback.

  * When post-generation hook is called, ``obj`` is the instance created by
    base factory; ``create`` is True if the strategy is "create", otherwise
    False.

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
- 在 app 中, 一系列测试共用的 factories 应该放在一个单独的 ``factories.py``
  文件中.

DjangoModelFactory
""""""""""""""""""
- factory.django.DjangoModelFactory.

- ``create`` strategy uses ``Model.objects.create()`` or
  ``Model._default_manager.create()``.

- If the factory contains at least one ``RelatedFactory`` or ``PostGeneration``
  attributes, the base object will be ``.save()``-ed again to update fields
  possibly modified by post-generation hooks.

  * 这发生在 ``_after_postgeneration()``.

  * 有时候这会导致一些问题. 例如在 post generation hook 中调用
    ``QuerySet.update()`` 来更新列值的话, 必须记得刷新 model instance
    ``.refresh_from_db()``. 否则在 post generation hook 中的修改就会被覆盖.

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

Faker
-----
- ``factory.Faker`` is a factory declaration subclass, utilizing ``faker``
  module to provide more real fake data.

constructor
^^^^^^^^^^^

- ``provider``

- ``locale``

- ``**kwargs``. provider's optional arguments.

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

faker
=====

overview
--------
- Usage of faker module: generate fake data.

- When you needs fake data:

  * testing.

  * 业务逻辑示例展示.

  * anonymize data taken from a production service.

Faker
-----
- create a ``Faker`` object, call its methods to get the specified
  type of fake data.

constructor
^^^^^^^^^^^
- locale. specify locale of fake data. default ``en_US``.

attributes
^^^^^^^^^^

- ``random``. The ``random.Random`` instance used to generate fake data.

methods
^^^^^^^

- ``add_provider()``.

- ``seed(seed)``. seed the shared random number generator. This is useful to
  ensure the reproducibility of fake data during unit test.

- ``seed_instance(seed)``. Use a private ``random.Random`` instance rather
  than the shared one.

providers
---------

- a provider provides a classification of fake data.

- builtin providers are in ``faker.providers`` subpackage.

internet
^^^^^^^^
- ``user_name()``

- ``email(domain=None)``. domain 若未指定, 可能是随机生成或使用 free emails.

- ``ascii_email()``. 保证 ascii.

- ``safe_email()``. domain 全是 ``example.%s``. 保证不真实存在.

- ``ascii_safe_email()``.

- ``free_email()``. domain 是几个免费邮箱: gmail, yahoo, hotmail.

- ``ascii_free_email()``.

- ``company_email()``. domain 随机生成.

- ``ascii_company_email()``.

file
^^^^

- ``file_path(depth=1, category=None, extension=None)``.
  depth is the level of directories.  Provide an extension or determine
  extension by category (audio, image, office, text, video). If both are
  None, use random one.

- ``file_name(category=None, extension=None)``. ditto without directory.

- ``file_extension(category)``. ditto with only extension (no leading dot).

- ``mime_type(category=None)``. category can be application, audio, image,
  message, model, multipart, text, video.

- ``unix_device(prefix=None)``. prefix if not provided is chosen from be sd,
  vd, xvd.

- ``unix_partition(prefix=None)``. ditto with partition number.

date_time
^^^^^^^^^

- ``date_time_this_century(before_now=True, after_now=False, tzinfo=None)``.
  A datetime instance within current century. ``tzinfo`` if provided must be a
  ``datetime.tzinfo`` instance. That'll make an aware datetime.

- ``date_time_this_decade(before_now=True, after_now=False, tzinfo=None)``.
  ditto for current decade.

- ``date_time_this_year(before_now=True, after_now=False, tzinfo=None)``.
  ditto for current year.

- ``date_time_this_month(before_now=True, after_now=False, tzinfo=None)``.
  ditto for current month.

- ``date_time_between(start_date="-30y", end_date="now", tzinfo=None)``.
  A datetime between ``start_date`` and ``end_date``, with optional timezone.
  ``start_date`` and ``end_date`` can be:

  * datetime.datetime object

  * datetime.date object

  * datetime.timedelta object, as relative to current time.

  * an integer, interpreted as ``timedelta(n)`` relative to current time, i.e.,
    days relative to current time.

  * a text string:

    - ``now``. current time.

    - a string of format::
     
        [{+|-}<int>y][{+|-}<int>w][{+|-}<int>d][{+|-}<int>h][{+|-}<int>m][{+|-}<int>s]

      每个部分相应于 timedelta 的 constructor params 意义: years, weeks, days,
      hours, minutes, seconds. years 会和 days 合并.

- ``past_datetime(start_date="-30d", tzinfo=None)``. A datetime between start date and
  1second ago. start date is the same as ``date_time_between()``

misc
^^^^

- ``password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)``.


custom provider
^^^^^^^^^^^^^^^
- Create a subclass of ``BaseProvider``

- define fake provider as a method.

- ``Faker.add_provider()`` to faker instance.

generator
---------
- By default all generators share the same ``random.Random`` instance,
  ``faker.generator.random``.

locales
-------

CLI
---
::

  faker [-h] [--version] [-o output]
        [-l {bg_BG,cs_CZ,...,zh_CN,zh_TW}]
        [-r REPEAT] [-s SEP]
        [-i {package.containing.custom_provider otherpkg.containing.custom_provider}]
        [fake] [fake argument [fake argument ...]]

- ``-l``. locale

- ``-r``. repeat number of entry.

- ``-s``. separator between entries.

- ``fake``. fake provider name.

- ``argument``. provider's optional argument.
