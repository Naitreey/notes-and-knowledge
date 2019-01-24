overview
========

- 单元测试时, 应该进一步开启所有 python warnings.::

    python -Wall ...

unittest
========
terms
-----
- test failure and test error.

  * failure. a known assertion error (likely AssertionError), meaning the test
    failed.

  * error. an unknown logical error (anything else), meaning the test aborted.

test structure
--------------
- test hierarchy.

  * A ``TestSuite`` is a grouping of related test cases and test suites. It can
    be all tests in a TestCase, or a test module.
  
  * A ``TestCase`` is a set of related test cases that collectively tests
    certain unit (which probably implements a functionality/feature).

  * A test method is a single test case that checks whether the UUT passes a
    particular criterion.

- A testcase is created by subclassing ``TestCase`` or instantiate
  ``FunctionTestCase``.

  * Each test of a test case is a method whose name starts with
    ``TestLoader.testMethodPrefix``.

  * In test methods, ``assert*`` methods are invoked to actually test stuffs.

- 对于一个 TestCase 中的公共部分, 应抽象成 utility methods, 这些 method 应该放
  在所有 test method 的前面. 因为新增的 test case 总会向下罗列.

- 对于多个 TestCase class 公共的部分, 可以抽象至 base class. 这样的 base class
  最好放在单独的 python module 中, 其文件名设置应避免被 unittest discovery 机制
  加载.

  若准备将 base class 放置于 test module 中, 则需要避免包含
  ``TestLoader.testMethodPrefix`` 的 method name.

  在 test module 中加载 base TestCase subclass 时, 最好不让 base TestCase 直接
  位于 global namespace. 这样避免了 TestLoader 在加载 TestCase subclass 时误将
  base class 实例化成 test case.

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
  utils 只为这一个 test method 服务. 这些 test cases 实例组成一个 test suite.

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

- ``assertCountEqual(a, b, msg=None)``. Test two containers (of any type)
  contain the same number of corresponding elements, regardless of order.

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
- ``fail(msg=None)``. fail the test case unconditionally. 可以用于在某种情况下
  强制 test failure.

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

- 继承. 允许将 helper functions and other common stuffs 抽象到基类和 mixins 中.
  但只要是不准备直接实例化的 TestCase subclasses, 就不能包含任何 test methods.

- 可以使用 ``TestCase.fail()`` 配合 ``@expectedFailure`` 来标记尚未完成的
  tests.  在未完成的 test method 中添加 ``fail()``. 当我们还不想处理 TODO 时,
  避免 failure clutter output, 使用 ``@expectedFailure`` 先隐藏 traceback, 只留
  下 dotted indication.

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
  environment-specific 的时候; 当一些测试是在包含 optional dependencies 的情况下
  执行.

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
  test body 还没有完成时进行标记. 当 test method/case 完成后, 这个测试就不再是
  expected failure 了, 而是 expected success (by implementing corresponding
  functionality). 此时就要把这个 decorator 去掉.

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

attributes
^^^^^^^^^^
- ``testMethodPrefix``. valid prefix of test methods.

- ``sortTsetMethodsUsing``. function used to sort test methods.

- ``suiteClass``. test suite class.

- ``testNamePatterns``. test method name patterns to match.

methods
"""""""
- ``loadTestsFromTestCase(testCaseClass)``. returns a test suite containing
  all test cases in a TestCase class.

- ``loadTestsFromModule(module, pattern=None)``. returns a test suite
  containing test suites from a test module.

- ``loadTestsFromName(name, module=None)``. return a suite of test suites/cases
  given a dotted name, which can be a module, a TestCase, a test method, a
  test suite instance, a callable that returns a TestCase or TestSuite instance.

- ``loadTestsFromNames(names, module=None)``.

- ``getTestCaseNames(testCaseClass)``. get test method names from a TestCase.

- ``discover(start_dir, pattern='test*.py', top_level_dir=None)``. support
  test discovery. return a test suite.

test result
-----------
- stores the results of a set of tests.

TestResult
^^^^^^^^^^

attributes
""""""""""
- ``errors``. a list of 2-tuples of TestCase instance and traceback string.
  This is about test errors.

- ``failures``. ditto for test failures.

- ``expectedFailures``. ditto for expected failures.

- ``skipped``. a list of 2-tuples of TestCase instance and reason of skipping.

- ``unexpectedSuccesses``. a list of TestCases of unexpected success.

- ``testsRun``. the number of tests have been run.

- ``shouldStop``

- ``buffer``

- ``failfast``

- ``tb_locals``

methods
"""""""
- ``wasSuccessful()``. True if tests are successful so far.

- ``stop()``

- ``startTest(test)``

- ``stopTest(test)``

- ``startTestRun()``

- ``stopTestRun()``

- ``addError(test, error)``

- ``addFailure(test, error)``

- ``addSuccess(test)``

- ``addSkip(test, reason)``

- ``addExpectedFailure(test, error)``

- ``addUnexpectedSuccess(test)``

- ``addSubTest(test, subtest, outcome)``

TextTestResult
^^^^^^^^^^^^^^
- TestResult subclass, used by TextTestRunner.

- formatting:

  * success: "."

  * failure: "F"

  * error: "E"

  * skip: "s"

  * expected failure: "x"

  * unexpected success: "u"

test runner
-----------
- A test runner is a component which orchestrates the execution of tests and
  provides the outcome to the user.

- It runs a test suite and collect results into test result object.

TextTestRunner
^^^^^^^^^^^^^^
- A runner that outputs result to a text stream. default is stderr.

methods
"""""""
- ``run(test)``. run a test case/suite.

load_tests protocol
-------------------
- Customize tests loading from module and packages.

- used during normal test runs and also test discovery.

- protocol. A callable that has a signature of::

    load_tests(loader, standard_tests, pattern)

  returns a test suite for this module or package (defining in
  ``__init__.py``).

- If discovery is started in a directory containing a package, ``__init__.py``
  will be checked for load_tests. If that function does not exist, discovery
  will recurse into the package as though it were just another directory.
  Otherwise, discovery of the package’s tests will be left up to
  ``load_tests``.

CLI
---

TestProgram
^^^^^^^^^^^
- The ``unittest.main.TestProgram`` is both used to make a test module
  conveniently executable and also serve as the CLI entrypoint of unittest
  module.

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
overview
--------
- usage of mock objects.

  * dependency isolation. patching/mocking objects and methods so that
    dependencies are eliminated.
  
  * behavior checking. check the SUT used an object correctly.
  
  * inspecting and learning the behavior of an unknown component and mechanism.

NonCallableMock
---------------
- 在创建每个 mock 实例时, 会先创建一个这个实例自己使用的子类. 这是避免在创建
  和修改 method definition 时, 不同的 mock 之间相互影响.

Mock
----
- Without considering autospeccing, arbitrary attributes can be set on a mock
  object.  access to arbitrary attribute of a mock object returns a new
  descendent mock object.

- When subclassing a Mock/MagicMock, all dynamically created attributes,
  ``return_value`` etc., will use the subclass automatically.

constructor
^^^^^^^^^^^
- name. the name of mock used by its repr, also propagated to mock objects
  derived from this mock object.

- ``return_value``. the value to be returned when the mock object is called. by
  default it's DEFAULT, in which case a new Mock object with the name
  ``<name>()`` is returned.

- ``side_effect``. The more complex behavior specs when the mock object is
  called. Its value can be:

  * A function. To be called when the mock is called, signature:
   
   - it's passed with the same arguments that are passed to the mock's call.
     
   - return value: If DEFAULT is returned, then the ``return_value`` is
     returned. Otherwise, the function's return value is used as mock call's
     return value.

  * an exception class or instance, which will be rasied on call.

  * an iterable. an iterator is built from it, which must yield a value on
    every call. Each value yielded from the iterator can be an exception class
    or instance to be raised (like the second form), or a value to be returned
    (like the first form, DEFAULT still applies).

  * None. The side effect is cleared, fallback to ``return_value``.

- spec. a list of strings or an existing object (a class or instance) that acts
  as the specification for the mock object. If an object is passed, ``dir()``
  is called to retrieve a list of strings. Unsupported magic attributes and
  methods are excluded. Accessing any attribute not in this list will raise an
  AttributeError.

  When spec is an object, the created mock's ``__class__`` is set to be the
  object's class or the object itself when it's a class. This makes mock object
  passes ``isinstance()`` test.

  When the spec is a callable object, this also enables a smarter matching of
  calls made to the mock, where the equivalence of calls to the mock object can
  be interpreted based on the more accurate parameter assignment semantics,
  rather than rudimentary positional/kwargs matching.

- ``spec_set``. A stricter variant of ``spec``, also preventing setting
  attributes that are not on the passed in spec.

attributes
^^^^^^^^^^
- called. whether the mock object has been called

- ``call_count``. the number of times the mock object has been called.

- ``return_value``. same as constructor parameter.

- ``side_effect``. same as constructor parameter.

- ``call_args``. None (if the mock hasn't been called), or the ``call``
  instance representing the arguments that the mock was last called with.

- ``call_args_list``. a list of all calls made to the mock object, in calling
  order, as ``call`` instances.

- ``method_calls``. calls to method of mock object and methods of all levels of
  mocks generated by attribute access. 不包含 calls to special methods.

- ``mock_calls``. a list of all calls to the mock object and all its descendant
  mocks, in calling order, as ``call`` instances.

assertions
^^^^^^^^^^
- ``assert_called()``. assert the mock has been called, at least once.

- ``assert_called_with(*args, **kwargs)``. assert *the last time* the mock was
  called with the specified args and kwargs.

- ``assert_called_once()``. assert the mock has been called exactly once.

- ``assert_called_once_with(*args, **kwargs)``. assert the mock has been called
  exactly once with the specified args and kwargs.

- ``assert_any_call(*args, **kwargs)``. assert the mock has ever been called at
  least once with the specified args and kwargs.

- ``assert_has_calls(calls, any_order=False)``. assert the mock has been called
  with the specified calls. If ``any_order=False``, the calls must be happened
  sequentially in order. The ``mock_calls`` is checked for this, therefore the
  calls made to descendant mocks are checked too. 这可用于检测 mock object 的
  部分调用历史. 若要检查全部调用历史, 使用 ``call_args_list``,
  ``method_calls``, ``mock_calls`` 等.

configuration
^^^^^^^^^^^^^
- ``attach_mock(mock, attribute)``. Attach a mock as an attribute of this one,
  replacing its name and parent. Calls to the attached mock will be recorded in
  the ``method_calls`` and ``mock_calls`` attributes of this one. In this case,
  the parent mock acts as a manager of the attached mock.

- ``configure_mock(**kwargs)``

MagicMock
---------
MagicMock 相对于 Mock 增加了一些功能, 它是 Mock 的子类. 这包含:

* 能够 mock special methods.

patch decorators
----------------
``patch()``, ``patch.object()``, ``patch.dict()`` can all be used as function
decorator, class decorator, context manager.

patch
^^^^^
``patch()`` decorator/context manager is useful when global objects need to be
patched/mocked. This is because

* patching on global objects must be undone when the relevant test's execution
  is finished;

* it also serves as a prominent documentation about what dependencies are
  needed by SUT.

parameters
""""""""""
- target. the target of patching, as an import path string. The right target to
  patch is where they are looked up by the SUT, which is not always the same as
  where it's defined. 盲目 patch 定义的地方会不可靠, 因为 SUT 的模块可以预先将
  定义加载到自己的 global scope 中, 创建 alias reference.

- ``new=DEFAULT``. when DEFAULT, use a MagicMock object. When ``patch`` is used
  as a decorator and new is omitted, the created mock is passed in as an extra
  argument to the decorated function.

patch.object
^^^^^^^^^^^^

parameters
""""""""""
- target. the object (rather than import path) on which to make patches.

- attribute. The name of attribute to patch.

- ``new=DEFAULT``. see ``patch()``.

patch.dict
^^^^^^^^^^
- Used to setting values in a mapping just during a scope and restoring the
  dictionary to its original state when the test ends

parameters
""""""""""
- target. a dict-like mapping object to patch.

patch start/stop
^^^^^^^^^^^^^^^^

autospeccing
------------
- When mocking a function/method, the original function/method is replaced by
  an actual mocking function (or method which is also a function). The mocking
  function has the same call signature as the original function/method, but
  delegates to a mock object under the hood, so that behavior assertions are
  possible.

  This also makes accessing the mocked method on a class instance return a
  bound method as expected.  如果没有使用 autospec, 则无法实现上述现象, 此时,
  the method is replaced by a mock instance, as a plain class attribute.
  Without descriptor protocol implementation, the unbound-to-bound conversion
  is not performed.

helpers
-------
call
^^^^

ANY
^^^
可用于辅助进行 equality 检测. ANY equals to anything. 因此当一些 assertion 只想
要检查部分内容, 而其他内容可以是任意情况或任意值时, 就可以用 ANY 作为
placeholder.

例如:

.. code:: python

  m.assert_called_once_with(a=1, b=ANY)

- random notes:

  * Be careful when using ``Mock`` object's special assert methods. Unless you
    get the magic method name exactly right, then you will just get a "normal"
    mock method, which just silently return another mock, and you may not
    realise that you’ve written a test that tests nothing at all.

design patterns
---------------
- Use ``spec``, ``create_autospec`` 等使 mock object 与 code implementation 的
  interface 保持一致, 避免构建的 mock 与被 mock 的依赖项的 API 不符. 从而一定程
  度上避免在测试用例中 patch 的 mock object 的行为与 SUT 依赖项的实际行为已经不
  符, 而测试仍然通过, 即测试结果已经不能反映 SUT 与依赖项的交互是否正确. 即
  spec 能在一定程度上 enforce the correct contract between boundaries. 这是对
  isolation 导致的集成问题的一部分解决方案 (另一部分解决方案则是更加整体性的测
  试.)

- 对于 callable object 以及 method calls 的 mock, 要使用 spec and auto speccing
  从而让 call equivalence 的检验能基于准确的语义, 而独立于 actual parameter
  passing method (positional/kwarg).

- Attributes of built-in/extension types can not be mocked. 若要 mock 相关内容,
  做法是 make patches in the module that imported the relevant builtin objects.
  例如, 在 somemodule 中使用了 datetime.datetime.now, 现在想要 mock 这个操作返回
  固定时间, 做法是

  .. code:: python

    # somemodule.py
    from datetime import datetime

    def some_op():
      # use datetime.now

    # test module
    with patch("somemodule.datetime") as mock_datetime:
      # make assertions with mock_datetime

- 使用 patch 的方法有 3 种:

  * function decorator or class decorator. 这种方式具有最明显的 dependency
    documentation 效果. 但也会可导致过长的 method signature.

  * context manager. 这种方式避免了多个 patch decorator 导致过长的 method
    signature. 但仍存在至少一级 indentation 的问题.

  * create patch in test case with start/stop. 这种方式避免了 indentation 问题.

      .. code:: python

        class MyTest(TestCase):

            def create_patch(self, name):
                patcher = patch(name)
                thing = patcher.start()
                self.addCleanup(patcher.stop)
                return thing

            def test_foo(self):
                mock_foo = self.create_patch('mymodule.Foo')
                mock_bar = self.create_patch('mymodule.Bar')
                mock_spam = self.create_patch('mymodule.Spam')

                assert mymodule.Foo is mock_foo
                assert mymodule.Bar is mock_bar
                assert mymodule.Spam is mock_spam

- patch local imports. 由于 import statement 只是从 sys.modules 中获取所需的
  module object, 可以使用 patch.dict 替换所需的 module 为 mock.

- mock can be used to inspect and learn the behavior, mechanism, inner workings
  of an unknown component or system. 例如, 要知道 ``{**d}`` dict unpacking 过程
  中发生了什么, 可这样

  .. code:: python

    m = MagicMock()
    {**m}
    m.mock_calls

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

- factory boy, faker 等假数据工具不该用于一般的单元测试, 也不该用于 model-level
  单元测试. 在 model-level 单元测试中, 应手动构建 model instance, 使用 factory
  boy 会太耗时. 并且, 在 model-level 单元测试中, 无需大量构造实例, 一般只需构造
  一个实例, 对逻辑进行检查.

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

- The subclassed Factory will inherit all declarations from its parent, and
  update them with its own declarations.

attributes
^^^^^^^^^^
- ``_options_class``. The FactoryOptions subclass associated with a Factory
  subclass.

- ``_meta``. A Factory's FactoryOptions instance.

class methods
^^^^^^^^^^^^^
instance generation
"""""""""""""""""""
- A Factory class's constructor call is the same as calling the factory's
  default strategy (defined by ``Meta.strategy``). This is defined in
  ``FactoryMetaClass.__call__``.

- ``build(**kwargs)``. a build strategy where the instance is not saved. fields
  can be customized by passing kwargs.

- ``create(**kwargs)``. a build strategy where the instance is saved.

- ``stub(**kwargs)``. a build strategy where a stub object is created, which is
  simply a namespace object (factory.base.StubObject) with declared attributes
  resolved.

- ``generate(strategy, **kwargs)``. generic generate by strategy.

- ``simple_generate(create, **kwargs)``. create or build.

- ``build_batch(n, **kwargs)``. build a batch of objects.

- ``create_batch(n, **kwargs)``. ditto for create.

- ``stub_batch(n, **kwargs)``. ditto for stub.

- ``generate_batch(strategy, n, **kwargs)``. ditto for generic generate.

- ``simple_generate_batch(create, n, **kwargs)``. ditto for simple generate.

utilities
"""""""""
- ``reset_sequence(value=None, force=False)``. Reset the sequence counter
  to the specified value or to the first value.

  例如对每个 TestCase 都保证 sequence 是重新计算的, 从而独立. 可以在
  ``TestCase.setUp()`` method 中重置 sequence.

extension points
""""""""""""""""
- ``_adjust_kwargs(**kwargs)``. adjusting resolved kwargs. It's called after
  a Factory's kwargs are resolved, in ``FactoryOptions.prepare_arguments()``.

- ``_setup_next_sequence()``. Returns the first value to use for the sequence
  counter of this factory. called when the first instance of the factory (or
  one of its subclasses) is created.

- ``_build(model_class, *args, **kwargs)``. called to actually build the model
  instance. will be called once the full set of args and kwargs has been
  computed. It's called by ``FactoryOptions.instantiate()``.

- ``_create(model_class, *args, **kwargs)``. called to actually create the
  model instance. otherwise ditto.

- ``_after_postgeneration(instance, create, results=None)``. Called after
  post generation hooks are called.

Meta options (FactoryOptions)
-----------------------------
- factory options are declared as ``Meta`` inner class inside a Factory class
  body.

options
^^^^^^^
- ``abstract``.  This indicates that the Factory subclass should not be used to
  generate objects, but instead provides some defaults. An abstract Factory
  can not be used to generate model instance.

  When unspecified, if ``model`` is not defined, it's set to True, otherwise
  False. A Factory's subclass will not inherit this attribute from parent
  Factory's Meta option.

- ``model``. factory's model class. default is None. If unset, inherit from
  parent factory's Meta option.

- ``inline_args``. a list of attribute names which should be passed as
  positional arguments (rather than kwargs) into model constructor. They
  must be listed in passing order. If unset, inherit from parent.

- ``strategy``. factory's default strategy. default is ``CREATE_STRATEGY``.
  If unset, inherit from parent.

- ``exclude``. a list of attributes to exclude when creating model instances.
  例如当 factory class 中定义的一些列属性只是作为 helper attributes.  If unset,
  inherit from parent.
  
  这与 `Parameters`_ 的作用有类似之处, 但 Params 在很多情况下更方便使用. 目前
  没发现必须使用 exclude 而不使用 Params 的地方.

- ``rename``. A dict whose keys are class attribute names of a Factory, and
  values are actual field names of the model class. 这用于, 当需要定义的 field
  与 Factory class 本身的一些属性和方法命名冲突时, 可以先换一个名字, 然后设置
  rename option, 在生成实例时转换一下.  If unset, inherit from parent.

option inheritance
""""""""""""""""""
Unlike django model's Meta option, there's no way to inherit a parent Factory's
Meta option class *explicitly*. (During class creation, Meta class itself is
popped out of class namespace.)

.. code:: python

  class Parent(factory.Factory):

    class Meta:
      abstract = True

  class Child(Parent):

    class Meta(Parent.Meta): # not possible!
      # ...

A Factory Meta option is inherited if it can be inherited as defined by
``_build_default_options()``, and detailed above.

attributes
^^^^^^^^^^
- all Meta options are defined as instance attributes.

methods
^^^^^^^
- ``contribute_to_class(factory, meta=None, base_meta=None, base_factory=None, params=None)``.

  * All options' values are resolved, and set on Factory class as normal
    attributes.

- ``get_model_class()``. Returns the resolved model class, because the
  ``model`` option might be a ORM-specific stuff, rather than an actual
  model class.
  
  This should be overridden by ORM-specific FactoryOptions subclass.

Parameters
----------
- Factory's ``Params`` inner-class 用于设置生成 model field 所依赖的参数.  当多
  个 model field value 的生成具有一定的相关性, 依赖于几个共同的参数, 则可以通过
  Params class 来指定. 各个 dependent field 使用 LazyAttribute 等 declaration
  引用这些 parameters.

- Parameters can be accessed during attribute resolution (on Resolver
  instance). But they are not accessible on resulting model instance.

Parameter inheritance
^^^^^^^^^^^^^^^^^^^^^
- Params defined in parent Factory classes are automatically inherited
  by child Factory class.

- Child Factory may override any inherited parameters.

SimpleParameter
^^^^^^^^^^^^^^^
- A simple parameter can be *any declarations* like in Factory class body.

- Any attribute value in Params class body is wrapped in SimpleParameter
  instance.

Trait
^^^^^
- A trait is a special kind of parameter. It's a flag that when toggled, a
  number of fields are set accordingly. In other words, traits are useful when
  a number of fields' values needs to be set based on a boolean flag.

- A Trait can be enabled/disabled inside a Factory subclass (as normal
  declaration).

- Values set in a Trait definition can be overridden by call-time values.

- Trait can be chained. 意思是, 在一个 Trait 的定义中, set 另一个 Trait flag.

constructor
"""""""""""
- ``**overrides``. For each kwarg, key is the field name to be set, and the
  value is the value to be set. This can be like any Factory attribute
  declaration.

Declarations
------------
- These are special class-level declarations.

- All these declarations can also be used as kwargs during a Factory call.  In
  other words, 它们不仅可以在 class body 中声明, 还可以直接作为 Factory 参数值
  传递. 这是因为, 无论是哪种方式, 都是在 generation 阶段才 resolve 至最终使用值
  , 所以都是可行的.

Faker
^^^^^
- ``factory.Faker`` is a factory declaration subclass, utilizing ``faker``
  module to provide more real fake data.

constructor
""""""""""""
- provider. A faker provider method's name.

- locale. locale passed to faker.Faker.

- ``**kwargs``. additional kwargs passed to the provider method.

class methods
"""""""""""""
- ``override_default_locale(locale)``. A context manager, used to temporarily
  override the default locale of all Faker instances.

  .. code:: python

    with factory.Faker.override_default_locale("zh_CN"):
      SomeFactory()

- ``add_provider(provider, locale=None)``. Add a provider to the faker.Faker
  instance of the specified locale.

LazyFunction
^^^^^^^^^^^^
- Useful when the value of a field is determined dynamically. So it can be 
  simulated by a function.

- Use this if the value logic is not related to the model instance. Otherwise
  use LazyAttribute.

constructor
"""""""""""
- function. the function to generate field's value.

LazyAttribute
^^^^^^^^^^^^^
- Useful When the value of a field is dynamically determined and related to
  other fields/parameters of the instance being generated.

constructor
"""""""""""
- function. A function that accept the object being built as sole argument, and
  return a value suitable for the field.

  * 注意 the passed-in object is not an instance of model class, but a
    ``Resolver`` instance.

decorator
"""""""""
- The ``lazy_attribute()`` decorator is similar. The decorated function is
  the function to be called. It's appropriate when a passed-in function
  can not be a simple lambda, but a more complex function.

- 由于 decorator 的机制, 这与 ``name = LazyAttribute(func)`` 完全是等价的.

Sequence
^^^^^^^^
- Useful when a field has unique constraint, so a sequential value ensures
  that there is no collision.

- The sequence counter is shared across all Factory classes.

- Forcing a sequence number for a factory call: pass ``__sequence`` keyword
  argument to the generation methods. This will not alter the shared value.

constructor
"""""""""""
- function. The function accepts the current sequence counter, and returning
  the field value.

decorator
"""""""""
- ``sequence()``. similar above.

LazyAttributeSequence
^^^^^^^^^^^^^^^^^^^^^
- merge functionality of LazyAttribute and Sequence.

constructor
"""""""""""
- function. A function that takes:
 
  * the object being generated (Resolver)

  * the sequence number

decorator
"""""""""
- ``lazy_attribute_sequence(func)``. similar above.

SubFactory
^^^^^^^^^^
- useful when a model instance depends on another model instance, via FK etc.
  relations. To generate a factory instance, the depending factory must be
  generated in advance.

- The Factory in a SubFactory declaration is generated before the main factory
  (``BuildStep.recurse()`` 创建 StepBuilder 进行 recursive build).

- The same build strategy is used for the SubFactory.

- To override kwargs passed to the SubFactory on a per-call basis, use::

    name__field=value

  in the main factory call.

- If a SubFactory generated instance is passed for the SubFactory's attribute,
  generation is disabled, and the passed-in instance is assigned directly.

constructor
"""""""""""
- factory. A Factory class or the import path to it (to avoid circular import).

- ``**kwargs``, additional kwargs to pass to the factory.

SelfAttribute
^^^^^^^^^^^^^
- When a field value equals to the value of the self attribute, or parent
  attribute, etc.

- Can reference
 
  * any (deep) attribute of the Resolver object, need not be a field.

  * any (deep) attribute of the parent Resolver object.

constructor
"""""""""""
- ``attribute_name``. path to the attribute.::

    attr           # current resolver
    attr.subattr   # current resolver
    .attr.subattr  # current resolver
    ..attr.subattr # parent resolver

- default. default value if attribute is not found.

Iterator
^^^^^^^^
- Produces successive values from the given iterable.

- By default, the iterable can be cycled, which means the produced values must
  be stored in memory.

- 注意不要使用过大的数据集, 因为都会保存在内存中.

constructor
"""""""""""
- iterable. the iterable to produce value from.

- cycle. default True. Whether to cycle the iterable. 注意即使 iterable can
  not be cycled, 生成过的值也会保存在内存中. 这是很恶心的.

- getter. a custom getter applied to the iterable generated value.

methods
"""""""
- ``reset()``. Reset the iterator, produce from the beginning.

decorator
"""""""""
- ``iterator(func)``. the func is called to generate an iterator. so it
  can be a generator function, etc.

Dict
^^^^
- Produce a dict with the fixed keys, and values can be any declaration.

- 实现原理:

  * 这是一个 SubFactory, wraps a factory.DictFactory.
  
  * dict 实际由 DictFactory 生成. 本质上, 生成一个 dict 与生成任何 model
    instance 的逻辑是一致的. 这是利用了 dict 可以解释成 class namespace
    definition.

- 若在 dict 定义中需要 reference main factory 的 attributes, 需要使用
  ``..attr``, 这是因为本质上是一个 SubFactory.

- Since it's a SubFactory, to override definition on a per-call basis,
  use ``name__field=value`` pattern.

constructor
"""""""""""
- params. a dict defining the scheme of the resulting dict instances.
  这可以使用与定义 Factory class 相同的任何内容.

- ``dict_factory``. default factory.DictFactory. specify alternative
  dict Factory.

List
^^^^
- Produce a list.

- 实现原理.
  
  * Internally, the fields are converted into a ``index=value`` dict.

  * 这是一个 SubFactory, wraps factory.ListFactory.

  * list 有 ListFactory 生成. 将 list 转换成 ``{index: value}`` 形式,
    从而可以套用标准 build 流程进行操作. 在输出时再转换回 list.

- Since it's a SubFactory, to override definition on a per-call basis,
  use ``name__<N>=value`` pattern.

constructor
"""""""""""
- params. a list defining the scheme of the resulting list instances.
  每一项可以使用与定义 Factory class 相同的任何内容.

- ``list_factory``. default factory.ListFactory. specify alternative list
  Factory.

Maybe
^^^^^
- Useful when the value of a field depends on another attribute, and forms an
  if-else relation.

- When the ``decider`` is truthy, select ``yes_declaration``, otherwise select
  ``false_declaration``.

constructor
"""""""""""
- decider. A decider can be:

  * Any declaration.

  * For a plain value, it's wrapped inside a SelfAttribute.

  最常见的是使用一个 attribute reference string 作为 decider, 类似
  SelfAttribute 那种.

- ``yes_declaration``. The declaration to use for the field when decider is
  truthy.

- ``no_declaration``. The declaration to use for the field when decider is
  falsy.

post-generation hooks
^^^^^^^^^^^^^^^^^^^^^
- All Post-generation hooks (RelatedFactory, PostGeneration,
  PostGenerationMethodCall) are called in the same order they are declared in
  the factory class, so that functions can rely on the side effects applied by
  the previous post-generation hook.

- All post-generation hooks are called *after* model instance's generation,
  therefore their declarations are not passed during instantiation.

- usage examples.

  * 在生成实例后, 设置 ManyToMany relationship.

RelatedFactory
""""""""""""""
- Generate a Factory *after* the generation of the main factory. This is the
  opposite of SubFactory. Useful for reverse related fields, etc.

- Like a SubFactory, to override definition on a per-call basis, use
  ``name__field=value`` pattern.

- If a related factory generated instance is passed for the RelatedFactory's
  attribute, RelatedFactory generation is disabled, and the passed-in instance
  is assigned directly.

- RelatedFactory is evaluated after the initial factory has been instantiated.
  However, the build context is passed down to that factory; this means that
  attribute reference can go back to the calling factorry’s context.

constructor
~~~~~~~~~~~
- factory. same as in SubFactory.

- ``factory_related_name``. The name under which the model instance generated
  by main factory will be passed to the related factory. In other words, the
  main instance will be passed to the ``factory`` call, with
  ``<factory_related_name>=instance`` as a kwarg. if not set, the main instance
  will not be passed at all.

- ``**kwargs``. Additional default kwargs to be passed to ``factory``.

PostGeneration
""""""""""""""
- Useful for 生成实例之后执行的进一步自定义处理和定义.

constructor
~~~~~~~~~~~
- function. The function to be called after main instance is generated.
  The function has the following signature:

    .. code:: python

      def callback(obj, create, extracted, **kwargs):
          pass

  * the name of callback function becomes a valid kwarg of Factory constructor.

  * When post-generation hook is called, ``obj`` is the instance created by
    base factory; ``create`` is True if the strategy is "create", otherwise
    False.

  * During factory call, if the kwarg is passed value, it will become the
    value of ``extracted`` arg of the callback. Otherwise ``extracted`` is
    None.

  * Any argument in the form ``<callback>__<field>`` will be extracted, its
    ``<callback>__`` prefix removed, and added to the ``kwargs`` passed to the
    callback. Extracted arguments won’t be passed to the Meta.model class.

  * post generation hook does not need to return anything.

decorator
~~~~~~~~~
- ``post_generation(func)``. the decorator form.

PostGenerationMethodCall
""""""""""""""""""""""""
- Useful when there's need to call a method of instance after its generation.

- an overriding value can be passed directly to the method through a keyword
  argument of main Factory call matching the attribute name.

- Keywords extracted from the factory arguments are merged into the defaults
  defined in PostGenerationMethodCall declaration.

constructor
~~~~~~~~~~~
- ``method_name``. the name of the method to call.

- ``**kwargs``. The default kwargs to be passed to method.

Strategies
----------
- built-in strategies

  * build (``BUILD_STRATEGY``). Simply instantiate a model instance.
  
  * create (``CREATE_STRATEGY``). build and save it to database.

  * stub (``STUB_STRATEGY``). returns an instance of StubObject whose
    attributes have been set according to the resolved declarations.

- During factory call, the strategy of the sub/related factories will use the
  strategy of the parent factory.

- Setting a factory's default strategy.
 
  * ``Meta.strategy`` attribute.

  * ``factory.use_strategy(strategy)`` class decorator.

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
- A subclass of base.Factory.

class methods
~~~~~~~~~~~~~
- ``_create(model_class, *args, **kwargs)``. overrides base definition,
   uses ``Model.objects.create()``, if not defined, use
   ``Model._default_manager.create()``. 这影响 create strategy 的处理.

- ``_after_postgeneration(instance, create, results=None)``. 这里, 如果使用的是
  create strategy, 并且至少一个 post generation hooks is run, object is saved
  again to update fields possibly modified by those hooks.

  * 若在 post generation hook 中进行的操作更新了数据库值, 却没有更新 instance
    的 in-memory field value, 则会导致覆盖.  此时记得刷新 model instance
    ``.refresh_from_db()``.

DjangoOptions
"""""""""""""
DjangoModelFactory automatically use DjangoOptions as its Meta inner class.

new options and modifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- model. 支持指定字符串形式的 ``<app_label>.<Model>``.

- database. specify the database to use.

- ``django_get_or_create``. Specify the fields to be used for filtering in
  ``QuerySet.get_or_create()``. 指定这个属性后, 创建 instance 会使用
  ``get_or_create()``, 而不使用 ``create()``. 这样, 可通过过滤来避免重复
  创建或由于重复导致的 IntegrityError.

additional declarations
"""""""""""""""""""""""
FileField
~~~~~~~~~
- for django FileField.

- Subclass of ParameteredAttribute, therefore like SubFactory they support
  passing kwargs from Factory call.

constructor
```````````
- ``from_path``. use file at this path-like object as file content, and use
  the basename of this path as filename, if ``filename`` is not provided.

- ``from_file``. use this file-like object as file content, and use basename of
  its ``name`` attribute as filename, if ``filename`` is not provided.

- ``from_func``. call this func that returns a file-like object as content, and
  its ``name`` attribute as filename, if ``filename`` is not provided.

- ``data``. use this data as file content. should be bytes. default to b"".

- ``filename``. specify the overriding filename. default filename is example.dat

Only one of ``from_*`` can be defined.

ImageField
~~~~~~~~~~
- for django ImageField.

- Subclass of ParameteredAttribute, therefore like SubFactory they support
  passing kwargs from Factory call.

constructor
```````````
- all kwargs from FileField, except ``data``. ``data`` is useless here.

- width. specify the dummy image's width. default 100.

- height. ditto for height.

- color. ditto for color, default blue.

- format. ditto for format, default JPEG.

disabling signals
""""""""""""""""""
- If signals are used to create related objects, they may interfere with
  RelatedFactory (例如因为要创建一些更具体的 related model instance, 而不是默认
  的). 在 django 系统中设置的 signal 就需要 disable 掉.

- ``mute_signals(signal1, ...)``. a decorator and context manager.

- 如果要 mute ``pre_save``, ``post_save`` 等 signal, 所有使用了 post generation
  hook 的相关 factory 都要使用这个 decorator, 因为会再保存一遍.

Utility factories
-----------------
- StubFactory. A Factory whose default strategy is ``STUB_STRATEGY``.

- DictFactory. A Factory that produces dict instances.

  * pass definitions as kwargs on a per-call basis, or subclass it to
    define your scheme.

- ListFactory. A Factory that produces list instances.

  * pass definitions as kwargs on a per-call basis, or subclass it to
    define your scheme.

Utility functions
-----------------
- ``make_factory(klass, **kwargs)``.

- ``create(klass, **kwargs)``

- ``create_batch(klass, n, **kwargs)``

- ``build(klass, **kwargs)``

- ``build_batch(klass, **kwargs)``

- ``stub(klass, **kwargs)``

- ``stub_batch(klass, **kwargs)``

- ``generate(klass, strategy, **kwargs)``

- ``generate_batch(klass, strategy, **kwargs)``

- ``simple_generate(klass, create, **kwargs)``

- ``simple_generate_batch(klass, create, n, **kwargs)``

Debugging
---------
- Detailed logging is available through the ``factory`` logger.

- ``factory.debug()`` context manager.

.. code:: python

  with factory.debug():
      obj = ModelFactory()

Internals
---------

Resovler
^^^^^^^^

attributes
""""""""""
- ``factory_parent``. parent resolver.

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

base
^^^^
- ``random_int(min=0, max=9999)``. rand int between min and max.

- ``random_digit()``. a single digit, i.e. between 0-9.

- ``random_digit_not_null()``. non-zero digit.

- ``random_digit_or_empty()``. a random digit or empty string. note that due
  to implementation, the empty string's probability is 50%.

- ``random_digit_not_null_or_empty()``. a non-zero digit or empty string. 有同
  上的概率分布问题.

- ``random_number(digits=None, fix_len=False)``. A random number with given
  number of digits at maximum. If ``fix_len=True``, the number of digits is 
  fixed at ``digits``. If ``digits=None``, return single digit number.

- ``random_letter()``. a random ascii letter.

- ``random_letters(length=16)``. a list of random letters.

- ``random_lowercase_letter()``. a random lowercase letter.

- ``random_uppercase_letter()``. a random uppercase letter.

- ``random_elements(elements=('a', 'b', 'c'), length=None, unique=False)``.  A
  list of random elements. If ``length=None``, length is between 1 and number
  of elements.
  If `elements` is a dictionary, the value will be used as
  a weighting element.

- ``random_choices(elements=('a', 'b', 'c'), length=None)``.  ditto for
  non-unique results.

- ``random_element(elements=('a', 'b', 'c'))``. ditto for one element.

- ``random_sample(elements=('a', 'b', 'c'), length=None)``. like
  ``random_choices()``, for unique elements. Multiple occurrences of the same
  value increase its probability to be in the output.

- ``randomize_nb_elements(number=10, le=False, ge=False, min=None, max=None)``.
  A randomized number near by ``number``. When ``le=True``, result must be
  lower or equal to number; when ``ge=True``, result must be greater or equal
  to number; when both is True, result has to equal to number. min and max
  set lower and higher bounds of the allowed value.

- ``numerify(text='###')``. Replaces all placeholders in given text with
  randomized values, replacing: all hash sign ('#') occurrences with a random
  digit (from 0 to 9); all percentage sign ('%') occurrences with a random
  non-zero digit (from 1 to 9); all exclamation mark ('!') occurrences with a
  random digit (from 0 to 9) or an empty string; and all at symbol ('@')
  occurrences with a random non-zero digit (from 1 to 9) or an empty string.

- ``lexify(text="????", letters=string.ascii_letters)``. Replaces all question
  mark ('?') occurrences with a random letter.

- ``bothify(text='## ??', letters=string.ascii_letters)``. First numerify then
  lexify.

- ``hexify(text='^^^^', upper=False)``. Replaces all circumflex ('^')
  occurrences with a random hexadecimal character.

python
^^^^^^
- ``pybool()``.

- ``pystr(min_chars=None, max_chars=20)``.
  Generates a random string of upper and lowercase letters, with length within
  ``min_chars`` and ``max_chars``. if ``min_chars=None``, length is fixed to
  ``max_chars``.

- ``pyfloat(left_digits=None, right_digits=None, positive=False)``
  a random float number, left and right digits specify the number of digits
  at each side of decimal point. positive specify whether it's positive.

- ``pydecimal(left_digits=None, right_digits=None, positive=False)``. ditto
  for Decimal.

- ``pyint()``. random int.

- ``pytuple(nb_elements=10, variable_nb_elements=True, *value_types)``.
  return a tuple. size of ``nb_elements``, allowing a variance of size if
  ``variable_nb_elements`` is True. ``value_types`` if not specified, default
  to::
 
    ['str', 'str', 'str', 'str', 'float', 'int', 'int', 'decimal',
     'date_time', 'uri', 'email']

- ``pyset(nb_elements=10, variable_nb_elements=True, *value_types)``.
  ditto for set.

- ``pylist(nb_elements=10, variable_nb_elements=True, *value_types)``.
  ditto for list.

- ``pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)``.
  ditto for a random type of iterable, (tuple, list, set).

- ``pydict(nb_elements=10, variable_nb_elements=True, *value_types)``.
  keys are random words, values are like above.

- ``pystruct(count=10, *value_types)``.

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

phone_number
^^^^^^^^^^^^
- ``phone_number()``.

- ``msisdn()``. Mobile Station International Subscriber Directory Number.


company
^^^^^^^
- ``bs()``. business/bullshit word?

- ``company()``. company name

- ``company_suffix()`` company suffix, such as Inc., Ltd.

- ``catch_phrase()``.

lorem
^^^^^
- ``word(ext_word_list=None)``. generate a random word,
  optionally from the provided list.

- ``words(nb=3, ext_word_list=None)``. generate a list of
  words. default is 3.

- ``sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)``.
  a random sentence. ``nb_words`` 应包含的单词数目. ``variable_nb_words``
  对返回的单词数目进行一定的漂移.

- ``sentences(nb=3, ext_word_list=None)``. a list of sentences.

- ``paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)``.

- ``paragraphs(nb=3, ext_word_list=None)``

- ``text(max_nb_chars=200, ext_word_list=None)``. a string.
  Depending on the ``max_nb_chars``, returns a string made of words,
  sentences, or paragraphs.

misc
^^^^
- ``boolean(chance_of_getting_true=50)``.

- ``null_boolean()``. a random True, False, None.

- ``binary(length=(1 * 1024 * 1024))``. a random bytes of length.

- ``md5(raw_output=False)``. give a random md5 hash in hex digest format.
  if ``raw_output=True``, return raw bytes.

- ``sha1(raw_output=False)``. ditto for sha1.

- ``sha256(raw_output=False)``. ditto for sha256.

- ``locale()``. a random language locale string: ``<lang>_<region>``

- ``language_code()``. random language code.

- ``uuid4(cast_to=str)``. random uuid4.

- ``password(length=10, special_chars=True, digits=True, upper_case=True,
  lower_case=True)``.
  random password of length.


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
