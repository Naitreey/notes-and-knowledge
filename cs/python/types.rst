- ``types.SimpleNamespace`` 可以用于集成一组任意的 key-value, 功能上与一个 dict
  并无本质区别, 只是在 access key-value 时稍方便一点. 实际上, 可以用
  ``SimpleNamespace`` 来方便地实现可以同时以 attribute 和 key 两种方式访问的
  mapping:

  .. code:: python

    class DictNamespace(SimpleNamespace):
        def __getitem__(self, k):
            return self.__dict__[k]
        def __setitem__(self, k, v):
            self.__dict__[k] = v
        def __delitem__(self, k):
            del self.__dict__[k]

