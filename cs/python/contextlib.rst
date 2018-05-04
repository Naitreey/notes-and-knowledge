overview
========
- `contextlib` 将 python 中的 context manager 概念和 protocol 封装成了一组具体的
  context manager 类型, 即以 `AbstractContextManager` 为基础的一组 class.

contextmanager
==============
- `contextlib.contextmanager` 利用 generator 来快速构建 context manager, 省去了
  构建单独的 class 实现 ``__enter__``, ``__exit__`` method 的麻烦.
