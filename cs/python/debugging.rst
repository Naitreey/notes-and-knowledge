overview
========
- debugging methods:

  * read traceback

  * print, dump, etc.

  * logging

  * pdb/ipdb

  * code.interact, jump to interactive interpreter at the exact point you want

  * python -i, 简单的 post-mortem debugging

  * python -v[v], 检查 import 是否符合预期 (sys.path 是否正确, pyc 是否正确等)

pdb
===
- pdb 的用法:

  * debug 整个脚本: ``python -m pdb program.py``

  * debug 一段代码: ``pdb.run("<code-snippet>")``

  * debug 一个函数: ``pdb.runcall(func, *args, **kwargs)``

  * debug 一个表达式: ``pdb.runeval(expression, globals=None, locals=None)``

  * 从某个点插入 debug 模式: ``import pdb; pdb.set_trace()``

  * 在预期会抛异常的地方加入 try...except compound statement, 在
    except 里加入 ``import pdb; pdb.post_mortem()``. 这对调试
    异常很方便.

  * 在 interactive 解释器中 debug 已死的程序 (post-mortem):
    ``import pdb; pdb.pm()``

ipdb
====

- 提供比 pdb 更友好的 CLI 交互. 类似 ipython 的界面.

- 支持上述 pdb 各主要用法. 在此基础上, 优化 ``set_trace()`` 提供了
  context line 参数: ``set_trace(context=3)``.
