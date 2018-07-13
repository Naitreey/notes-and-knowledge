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
