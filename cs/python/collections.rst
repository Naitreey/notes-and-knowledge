- 若要结合 ``OrderedDict`` & ``defaultdict`` 的功能, 不能直接 subclass 两个,
  因为是 builtin class, implemented in C. 它们各自的 struct 结构体不兼容.
  此时只需适当 subclass ``OrderedDict`` 添加 ``__missing__`` 方法即可.
  见 `snippet <snippets/ordereddefaultdict.py>`_.

- 由于 dict 已经保证了 key 的 insertion order, ``OrderedDict`` 不再必要, 且
  ``defaultdict`` 已经自动包含了 ``OrderedDict`` 的行为. 不再需要自定义
  subclass.
