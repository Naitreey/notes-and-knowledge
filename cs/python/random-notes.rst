- 解释器直接执行脚本时, 该脚本中所有代码会在名为 ``__main__`` 的顶层 module
  中执行. (`__main__`, `sys`, `builtins` 是解释器默认 import 的三个 modules.)
  由于身在 `__main__` 中, namespace 中 默认并不包含 `__main__` 这个 identifier.
  需要手动 ``import __main__``.

- coroutine, awaitable, async def/with/for, await 等等这些概念并不适合一般情况下
  手动使用. 只有和某种 event loop 配合使用, 实现单线程的 asynchronous concurrency
  时, 才有价值.

- In CPython, generator-based coroutines (generators decorated with
  ``types.coroutine()`` or ``asyncio.coroutine()``) are awaitables,
  even though they do not have an ``__await__()`` method. Using
  ``isinstance(gencoro, Coroutine)`` for them will return ``False``.
  Use ``inspect.isawaitable()`` to detect them.
  Coroutine objects and instances of the Coroutine ABC are all instances
  of this ABC.
  即, 被 ``types.coroutine``/``asycio.coroutine`` decorated 的 generator
  是 coroutine (没有 ``__await__``), 使用 ``async def`` 定义的函数也是
  coroutine (有 ``__await__``).
  具有 ``__await__`` method 的 object 是 awaitable object. 所有 coroutine
  都是 awaitable object.

- 放在 ``yield from`` 后面的需要是 iterable.

- scheduler 的设置方式, 应该是在每次执行后, re-schedule self, 这样具有最大程度的
  调度灵活性, 也比较自然. 例如, 使用 `sched`:

    .. code:: python
    def periodic(scheduler, interval, action, actionargs=()):
        scheduler.enter(interval, 1, periodic,
                        (scheduler, interval, action, actionargs))
        action(*actionargs)

  使用 `asyncio`:

    .. code:: python
    def display_date(end_time, loop):
        print(datetime.datetime.now())
        if (loop.time() + 1.0) < end_time:
            loop.call_later(1, display_date, end_time, loop)
        else:
            loop.stop()

- ``StopIteration`` 只应该 raised by ``next()`` 和 ``__next__()``.
  对于 generator, generate 行为结束时, 应该直接返回 (``return``), 这样
  generator 的 ``__next__`` method 自动 raise 一个 StopIteration, 且
  它的 ``value`` attribute 是 generator function 的返回值.
  进一步, 对于 ``yield from`` 以及 ``await``, 这个 ``value`` 很自然地
  成为了整个表达式的值.

- 同理, ``StopAsyncIteration`` 只应该 raised by ``__anext__()``.

- 对于 pipe, write 端 close fd 时, read 端读时触发 EOF. 此时 read() == "".

- 命令行上 oneline 的动态输出可以用 sys.stdout.write("...\r")
  多行的动态输出的话就得用 curses 之类的

- 小心 python 中的 cyclic import problem. 需要明确, python 中对 import statement
  的执行逻辑 (排除 importlib 等复杂 paths, hooks 之类的问题) 很简单:

    'import' and 'from xxx import yyy' are executable statements.
    They execute when the running program reaches that line.

    If a module is not in sys.modules, then an import creates the
    new module entry in sys.modules and then executes the code in
    the module. It does not return control to the calling module
    until the execution has completed.

    If a module does exist in sys.modules then an import simply
    returns that module whether or not it has completed executing.
    That is the reason why cyclic imports may return modules which
    appear to be partly empty.

    Finally, the executing script runs in a module named __main__,
    importing the script under its own name will create a new module
    unrelated to __main__.

  因此, 对于以下两个文件

    .. code:: python
    # abcc.py
    from deff import xxx
    def yyy():
        pass
    # deff.py
    from abcc import yyy
    def xxx():
        pass

  会出现错误, 例如从 abcc 开始, import deff, 执行 deff, 又 import abcc, 而
  此时 abcc 的 namespace 里还没有定义 yyy.

  一个治标不治本的方法是遇到这个问题时, 不要使用全局 import, 在使用处使用
  local import, 例如在函数里 import.
  然而事实上, 从代码逻辑角度看, 这种问题根本不该出现. 一个合理的代码模块提供
  的功能, 使用 global import 与 local import 不该有任何使用上的区别. 没有
  任何正经的 python module 存在这个问题. 公共逻辑应该放在一个单独的模块中,
  然后各个执行者都从这个模块中 import 公共的功能.

- debugging methods:

  * read traceback

  * print, dump, etc.

  * logging

  * pdb

  * code.interact, jump to interactive interpreter at the exact point you want

  * python -i, 简单的 post-mortem debugging

  * python -v[v], 检查 import 是否符合预期 (sys.path 是否正确, pyc 是否正确等)

- testing methods:

  * python -W default, 所有 warnings 都显示, 即开启默认不显示的那些警告

  * doctest

  * unittest

- pdb 的四种主要用法:

  * debug 整个脚本: ``python -m pdb program.py``

  * debug 一段代码: ``import pdb; pdb.run("<code-snippet>")``

  * 从某个点插入 debug 模式: ``import pdb; pdb.set_trace()``

  * debug 已死的程序 (post-mortem): ``import pdb; pdb.pm()``

- Creating pipelines with subprocess
  It is possible to create process pipelines using ``subprocess.Popen``,
  by just using ``stdout=subprocess.PIPE`` and ``stdin=otherproc.stdout``.
  开启第二个子进程后, 需要在父进程中关闭前一个子进程的 `stdout`. 这样
  pipe 的两端才分别只有一个 fd 连接着, 保证了 SIGPIPE 的生成.
  Ref: http://www.enricozini.org/blog/2009/debian/python-pipes/

- python 中每个线程本质上成为 cpython interpreter 的线程.
  默认情况下, 最后一个 "普通线程" 退出后解释器退出, 即程序终结.
  `threading.Thread` class 的 `daemon` attribute 实际意思是将一个线程标记为
  所谓 "后台线程", daemon thread 不是 "普通线程", 不在程序是否退出的考虑范围内.
  因此, 相应线程可能受到影响, 比如资源未释放等.

- Set and Change buffering mode

  python3 不允许 text stream 的 buffering mode 为 unbuffering.
  也就是说, 只能是 line buffering (``buffering=1``) 或 block buffering
  (``buffering=<size>``). (也许因为 text 是 unicode, 因此没有真正的
  unbuffered text IO?) 对于 interactive file (a.k.a. terminal device),
  默认为 line buffering, 对于 regular file, 默认是 block buffering.
  若要对 text stream 模拟 unbuffering mode, 只能在写入时强行 flush.
  例如, ``print(..., flush=True)``, ``TextIOWrapper.flush``.

  对于 binary stream, unbuffer, line buffer, block buffer 都可以.

  若要修改 stdout/err stream (text stream) 的 buffering mode, 可以 ``open``
  来 reopen underlying file descriptor in other buffering mode:

    .. code:: python
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1024)
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", buffering=1024)

- 线程的目的不仅仅是为了 *同时的* 并行计算, 而是为了构建多个独立的运算单元.
  将这些运算单元分配到不同的 CPU 核上才具有 "同时并行" (parallel computing) 的意义.
  python 虽然有 GIL, 但这影响的是单 python 进程进行 parallel computing 的能力,
  并没有影响多线程所带来的其他可能性.

- 通过 `Thread` object constructor 的 `args`, `kwargs` 参数传递的只应该是 `target`
  API 所需的量. 并不是说线程间共享的量都需要从这里传递进线程.
  在设计时, 不要忘了模块化, 设计一个线程的逻辑时, 只该考虑这个线程的事务, 不该考虑其他
  线程如何调用这个线程.

- 如何 redirect stdin/out/err:
  1. 直接给 `sys.stdin|stdout|stderr` 赋值一个新的 file-like object.
  2. 使用 python3 的 `contextlib.redirect_stdin|stdout|stderr`.
  3. 注意以上方法都只是在 python 层面上转移了 stream, cpython 解释器的 fd 0,1,2
     根本没受影响. 根本的办法是调用 `os.dup2()` 直接将想要的目的文件 fd 复制到
     0,1,2 fd 上面. 例如:

       .. code:: python
       class _RedirectStream:
           """
           Redirect standard stream `_stream` at OS level, rather at python level.

           This differs with `contextlib._RedirectStream`.
           """

           _stream = None

           def __init__(self, target_stream):
               self._target_stream = target_stream
               self.new_fd = target_stream.fileno()
               self.old_fd = None
               self.copied = None

           def __enter__(self):
               stream = getattr(sys, self._stream)
               stream.flush() # flush buffer that dup2 knows nothing about
               self.old_fd = stream.fileno()
               self.copied = os.dup(self.old_fd)
               os.dup2(self.new_fd, self.old_fd)
               return self._target_stream

           def __exit__(self, type, value, tb):
               self._target_stream.flush()
               os.dup2(self.copied, self.old_fd)
               os.close(self.copied)
               return False

- python3.6+ class 的 `__dict__` 中 key 的顺序符合 method 定义的顺序,
  函数的 `**kwargs` dict 中 key 的顺序符合 keyword args 的传递顺序.
  实际上 `dict` 类型实现了 key-order 符合 key 的 creation order. 在 dict 的 ``repr``
  输出中, key 按照 collating sequence order 来排序, 但实际的 key 的顺序仍然是
  creation order, 这可以用 ``dict.keys()`` 看出. 但是我还是更愿意用 `OrderedDict`.
  Ref: https://mail.python.org/pipermail/python-dev/2016-September/146327.html
  Ref: https://docs.python.org/3/whatsnew/3.6.html#pep-520-preserving-class-attribute-definition-order

- 关于 list 和 dict 等 `Sequence` 和 `Mapping` iteration 的一些 pitfalls.

  * 不该在 iterate list 或 map 的时候修改该对象的长度, 例如删除 element or key-val pair.
    对于 dict, 在 py3 中这是 `RuntimeError: dictionary changed size during iteration`.

  * ``dict.keys|.values|.items`` 这些 methods 返回的 view object 与原 dict 是同步的.
    因此, 若在 iterate 这些 view object 时要对原来字典的 key, value 等进行修改,
    需要在必须的时候先生成一个 list, 即 ``list(dict.keys())``, 再遍历这个 list.
    否则, 遍历时, 可能会漏掉一些项或重复一些项.

- `io.StringIO` constructor 的 `initial_value` 是用于设置 buffer 的初始值以便于
  接下来修改的. 相当于一个文件以 "r+" mode 打开. fd 指向 buffer 起始位置. `write()`
  会覆盖掉 `initial_value` 的部分.

- Context manager 的 ``__exit__(self, type, value, tb)`` method 的返回值严格地讲应该是
  ``True|False``. ``True`` 则在退出时 suppress 在 with block 中 raise 的 exception,
  ``False`` 则任传入的 exc_info propogate 至外层.

- `contextlib` 将 python 中的 context manager 概念和 protocol 封装成了一组具体的
  context manager 类型, 即以 `AbstractContextManager` 为基础的一组 class.

- context manager 和 decorator 的关系和区别.

  * context manager 适用于当我们需要把某一操作置于一个特定的 context 下, 并封装有
    方便的建立 context 和消除 context 的操作. 注意重点是操作, context manager
    只是一个方便的工具, 为这个操作提供 context 服务.

  * decorator 比 context manager 涵盖的范围宽泛许多. 它 decorate 下面的操作 (class/
    function), 而这种含义的附加和修改不局限于 "prepare-cleanup" 的 context manager
    使用场景, 而是任何的含义附加以及操纵. 简单的可以是 `classmethod` 等基本的含义
    微调, 复杂的可以是将一定的操作 attach 至某个更大的完整的框架, 例如 `Flask.route`,
    `unittest.skipIf`.

- class decorator 的一个很好的应用: ``django.utils.python_2_unicode_compatible``

- 对于明确只能使用一次的 context manager, 可以利用 `contextlib.contextmanager`
  使用 generator 来生成. 在 generator function 中只写一个 ``yield``, 这样只能
  yield 一次, 所以同一个 generator 不能在不同 ``with`` statement 中重用.
  但是其实这也不一定. 写一个完整的类并实现 context manager protocol 很多时候
  是更好的选择.

- python3.4+ 中, module ``__file__`` attribute 总是该 module 的绝对路径, 唯一的
  例外是作为 `__main__` module 执行的命令行脚本. ``__main__.__file__`` 的值与
  命令行上的脚本路径一致, 因此可能是相对或绝对. 这有助于对脚本 invocation 方式
  的判断.
  ref: https://docs.python.org/3.4/whatsnew/3.4.html#other-language-changes

- python class member vs java class member

  ``self.__identifier`` 类似于 Java 的 private member. 这种成员只要是在 class 或
  instance 的 namespace 中定义, 就会被 name mangling. 而且 prefix 的 class name
  取决于 lexical scope 的类名. 因此实现了子类无法访问的 private member.

  ``self._identifier`` 意在作为类似 protected member. Subclass 可以访问, 外界不该
  (而非不能) 访问.

  ``self.identifier`` 是共有成员. 谁都可以访问.

  在 python class 的定义中应该遵守这个规则, 非共有成员一律以 ``_`` 起始.

- 关于编译. 直接在命令行上指定的 python module (一般是可执行脚本) 的编译结果不会被
  cache 到文件系统中.
  编译的 pyc 文件是 platform-independent.
  对于 non-source distribution, 编译后的 pyc 必须位于源文件的目录, 且必须不能有源文件
  存在.
  `-O` 去掉 ``assert``, `-OO` 进一步去掉 docstring. 因此一般不该也不需要优化编译.
  编译只会加载更快, 不会影响运行速度.
  ref: https://docs.python.org/3/tutorial/modules.html#compiled-python-files

- py3 中, bytes 的 printf-style string formatting 支持 `b` 和 `a` conversion
  specifiers. `b` 生成对象的 bytes object 表达形式 (``__bytes__`` 或 buffer
  protocol); `a` 生成对象的 ascii 表达形式, 即将所有非 ascii 字符转义为
  escape sequence, 严格地讲是 ``repr(obj).encode("ascii", "backslashreplace")``.
  bytes 的 `b` 和 `a` 对应于 str 的 `s` 和 `r`. 对于 str, 也有 `a` 这种 ascii
  表达形式.

- py3 中, exception object 包含一切 exception 相关信息::

    exc_type    type(e)
    exc_value   e
    traceback   e.__traceback__

- py3 中没有 basestring, 因为 string 就是 string, bytes 就是 bytes, 是两码事.

- 不要随便使用 binary IO mode, 只有需要时才使用. 如果担心 line ending 的转换
  等问题, 使用 ``open`` 的 `newline` 参数.

- 不能 ``bytes("string")``, 必须指定 `encoding`.

- `zip` object is iterator, i.e. it has ``__next__`` method.
  所以 `zip` object 不能重复使用.

- py3 中 `int` type 自带与 bytes 相关的方法:
  `int.from_bytes`, `int.to_bytes`, `int.bit_length`.

- 对于 py2 py3 兼容的代码, 不能用 py3 特有的 syntax, 否则在解释器第一步 lexical analysis
  时就会报出 `SyntaxError`. 所以必须用 py2 py3 兼容的语法来写. 然后在 runtime 对不同版本
  的 python 进行不同的调用和处理.

- python 的 executable script 一般设计为把代码的主要实现部分放在一个 package/module
  中, 将极其少量的调用部分, 即 entrypoint 放在单独的可执行脚本中. 并且该 entrypoint
  具有明确的返回值, 如下所示:

    .. code:: python

    import sys
    from somemodule import main # main is the typical entrypoint name
    # ...
    # preparations
    # ...
    sys.exit(main(...))

- ``install_requires`` of `setup.py` vs `requirements.txt`:

  * ``install_requires`` 是从 package 发布的角度来规定 dependency 的.
    因此, 它规定的依赖应该是这个 package 的直接依赖, 并且它对 deps 的版本限定是
    必要性的限制, 即不满足这些限制这个 package 就无法正常工作. 这也意味着, 不该
    限制 deps 的来源, 只该相对抽象地说明所需的包和至少需要满足的版本.

  * `requirements.txt` 是从部署和运行的角度来规定要安装的包和所需安装的版本的.
    也就是说, `requirements.txt` 描述的是 "如果你想要干某件事情, 你需要首先
    用 `pip` 保证当前环境满足 `requirements`". 比如, 某个软件包含一系列 python
    写的 tests, 那么要运行这些测试, 当前环境需满足 `test_requirements.txt` 里
    指定的条件. 注意我们不是要发布这些测试代码, 因此没有 `setup.py`. 再比如,
    生产部署时当然需要所有包的版本是固定的经过测试的, 所以应该将开发或测试环境
    中的所有 packages 用 `pip freeze` 生成一个严格的包含所有 packages 的列表,
    以在生产机器上对这个完整的 python 运行环境进行 repeatable installation.

  Ref: https://packaging.python.org/requirements/

- 正则表达式字符串应该使用 raw string. 这样才能保证出现在字符串中的任何 literal 字符,
  经过解释器处理之后得到的值仍然是其原始的 literal 的内容.
  这是因为 ``\`` backslash 在 string syntax 和 regex syntax 都是转义作用. 所以对于一个
  正则的 escape sequence, 在代码中输入时必须 escape 两次. 为避免这种 clumzy, 需要使用
  raw string.

- 正则的 ``$`` 会匹配

  * end of string 这个空字符串位置

  * just before the newline at the end of string 这个空字符串位置, 因此 ``abc\n`` 有
    两个可能的匹配位置.

  在 multiline mode, ``^`` ``$`` 还会对以 ``\n`` 分隔的每行进行匹配.

- python 正则的 character class 只支持 single char escape sequence, 不支持 ``[:name:]``
  形式的 POSIX name.

- 设置了 ``re.VERBOSE`` flag 的 pattern 里, 所有的 whitespace chars, 无论所在的位置和
  层级, 都会被忽略掉, 除了两种情况:

  * 位于 character class 中的 whitespace chars, e.g., ``[ \t\n]``.

  * 使用 ``\`` 进行转义的 whitespace chars.

  此外, 在 char class 以外且没有被转义的 ``#`` 代表 comment 的开始.

- `types.SimpleNamespace` 可以用于集成一组任意的 key-value, 功能上与一个 dict
  并无本质区别, 只是在 access key-value 时稍方便一点. 实际上, 可以用 `SimpleNamespace`
  来方便地实现可以同时以 attribute 和 key 两种方式访问的 mapping:

    .. code:: python

    class DictNamespace(SimpleNamespace):
        def __getitem__(self, k):
            return self.__dict__[k]
        def __setitem__(self, k, v):
            self.__dict__[k] = v
        def __delitem__(self, k):
            del self.__dict__[k]

- ``__getattr__`` vs ``__getattribute__``

  * 获取一个 attribute 时, 如果在 object 自身以及在它的类的 MRO chain 上都
    找不到这个 attribute 时, 就会 call 它的 ``__getattr__``. 这可用于动态的
    attribute access. ``pymongo`` 是很好的例子.

  * 如果实现了 ``__getattribute__``, 则所有 attribute access 的操作都会走这个
    method.

- Indentation is rejected as inconsistent if a source file mixes tabs and spaces
  in a way that makes the meaning dependent on the worth of a tab in spaces;
  a `TabError` is raised in that case.

    .. code:: python

    if __name__ == '__main__':
        print("b")
    	print("a")

  以上代码会导致 `TabError`, 因为 第二行 print 前面是 tab char, 对它的大小的解释依赖于
  第一行.

- ``types.DynamicClassAttribute`` 是个 descriptor, 它在很大程度上的使用与 `property`
  类似, 而它的目的是如果对这个 attribute 的访问是基于 class, 则转至 ``__getattr__``,
  从而达到对结果自定义的目的. ``enum.Enum`` 是个例子. `Enum` 需要使用
  ``DynamicClassAttribute`` 的原因是:

  - `Enum` object 需要支持 ``.name`` ``.value`` 两个属性.

  - `Enum` 的成员可能命名为 ``name`` ``value`` 等, 这要求 ``Enum.name`` 是 instance,
    ``Enum.name.name`` 是 instance 的名字. 所以需要对 ``.name`` attribute 的访问进行
    控制.

- locale settings, 准确地讲是 ``LC_CTYPE`` 会影响 python 中读写文件系统时使用的
  encoding, 即 `sys.getfilesystemencoding()`. 所以为了保证 UTF-8 的 filesystem encoding,
  恰当的 locale 环境变量必须被设置. 否则的话, 默认的 C locale 会导致 filesystem encoding
  变成 ascii. 在读取普遍编码为 utf-8 的 linux 文件系统时会报错.

- `os` module 里有大量的 syscall wrapper.

- ``logging`` module 中, 对于 ``propagate == True`` 的 logger, ``LogRecord`` 在向上层
  传递时, 不会考虑父级 logger 的 level 和 filters, 而是直接传递个父级的各个 handlers.

- argparse 的局限性:
  无法指定 ``--foo`` ``--bar`` 必须同时存在或同时不存在.

- 关于 python3 中 filesystem encoding 的处理相关问题.

  * 默认情况下, 所有的文件系统上的文件路径都会使用固定的 encoding 来 decode/encode.
    这样, 在 python 中出现的路径默认都是解码后的 str 类型量, 而不是原始的 bytes.
    这个固定的 encoding 可以通过 ``getfilesystemencoding`` 来获取, 通过 ``LC_CTYPE``
    来设置或影响. 在 encode/decode 过程中的错误处理, 则是依据 ``getfilesystemencodeerrors``
    来获取.

    这个 encode/decode 的结果, 可以通过 ``os.fsencode`` ``os.fsdecode`` 来模拟.

  * `os`, `os.path` 中的很多函数支持输入 str 或 bytes 两种类型参数, 输入前者时结果中
    自动对文件名进行默认的 encode/decode 处理; 输入后者时则返回 bytes 不做处理.

  * ``sys.argv`` 的值已经用 ``os.fsdecode`` 解成了 str. 若要访问原始的 bytes 参数值,
    应对参数值 ``os.fsencode``.

  * 环境变量的访问, 提供了 ``os.environ`` 和 ``os.environb``, 分别是解码和未解码的版本.

  * 在 unix-like 系统中, 这种自动的编码解码使用的 error handler 是 ``'surrogateescape'``.
    使用这个 error handler, 解码时无法识别的 bytes 会转换成一个 unicode 字符集中的占位
    字符, 从而保留了全部原始信息, 保证了再次编码时能够恢复原始的 bytes.

  * 在 native unix-like 文件系统中, 一般情况下使用 str 类型量作为 pathname 是最合适的.
    str 与 bytes 对一个 pathname 的表达通过 ``os.fsencode`` ``os.fsdecode`` 来转换.
    如果一个程序需要处理任意编码的二进制文件名 (比如使用了不同的字符编码集), 则应该
    在程序中使用 bytes objects 来代表 pathname.

- 注意 json format 不支持 binary data 这种类型. 所有的 binary data 都必须使用某种数字
  进制编码成字符串, 才能用 json format 来传递.

  由于 json 数据要求是纯文本, 因此 ``json.dumps`` 的结果一定是 `str` 而不会是 `bytes`.

- ``__str__`` 默认 call ``__repr__``, 反之却不行. 即严格的 ``__repr__`` 可以代替
  informal 的 ``__str__``, 但反之不能用 ``__str__`` 代替 ``__repr__``.

- ``__debug__`` 是 builtin constant. cpython 解释器默认情况下设置 ``__debug__ == True``,
  此时 assert statement 会执行; 使用 ``-O`` 命令行参数后为 ``False``, assert statement
  被忽略.

- 启动时, `site` module 会给 __main__ module 增加 ``quit()``, ``exit()``, ``copyright``,
  ``license``, ``credits`` 这几个 callable 对象. 它们本意是用在 interactive session 中,
  平时的程序中不该使用它们.

- ``NotImplemented`` vs ``NotImplementedError``

  * ``NotImplemented`` 用在 rich comparison method 中. 当某个 rich comparison method
    返回该值时, 表示该操作 (在这个具体情况下) 未被实现.

  * ``NotImplementedError`` 用在 method definition 中, 就是一个 exception,
    表示该方法没有被实现或尚未完成. 例如是一个 abstract method, 或者是开发中的
    method.

- ``urlparse`` vs ``urlsplit`` of `urllib.parse`

  URL 的一般化结构::

    scheme://netloc/path1;params[/path2;params...]?query#fragment

  注意根据 RFC 2396 ``params`` 是属于每个 path segment 的. ``urlparse`` 会把最后一个
  path segment 的参数和路径本身分隔开来, 这是不合规范的. ``urlsplit`` 不会这样做.
  所以 ``SplitResult`` 比 ``ParseResult`` 少一个 ``params`` attribute.

  一般情况下, 应该用 ``urlsplit``.

- buffer protocol 的意义在于避免复制内存, 使得代码高效很多, 甚至接近 C/C++ 代码效率.
  ``bytes``, ``bytearray``, ``array.array`` 都实现了 buffer protocol. 配合
  ``memoryview`` 和 file-like object 的 ``.readinto`` 和 socket object 的 ``.recv_into``
  等 methods, 达到避免复制的目的.

- ``__slots__``

  * ``__slots__`` 使得实例中没有 ``__dict__`` 和 ``__weakref__``.

  * 某个类和它所有的父类都定义了 ``__slots__``, 这个类的实例才没有 ``__dict__``.
    ``__slots__`` 的作用局限在定义类中. 不同类中定义的 slots 取并集得到了当前类
    实例化后的 attributes.

  * slots 中的 attributes 实际上以 data descriptor 方式在类中定义, 定义为
    ``member_descriptor`` descriptor object.

  * 使用 slots 的好处是

    - faster attribute access

    - potential memory savings

- descriptor protocol

  descriptor 的效果是一个对象以不同的方式去访问它, 得到的是不同的结果.
  descriptor object ``x`` 出现在某个 owner class ``A`` 的定义中, 成为这个类的
  attribute. 当获取这个 attribute 时 (``a.x``, ``A.x``, ``super().x``, or whatever)
  python 发现这个 attribute 实际上是 descriptor, 不会直接返回这个 descriptor,
  而是进一步执行 descriptor 的 ``__get__``, ``__set__`` 或 ``__delete__`` method
  来完成操作.

  python 中很多东西实际上都是某种 descriptor class 的实例. 例如, 所有函数都是
  non-data descriptor, 它们在单独使用和通过类访问是表现为函数自身, 通过实例访问时表现为
  bound method. ``property`` object 都是 data descriptor, 是 ``property`` descriptor
  class 的实例.

- ``\b`` backspace char 只是把光标向左移动 1 格, 并不删除涉及的字符;
  ``\r`` carriage return 只是把光标移至当前行首, 并不删除本行内容.

- C 的 struct 对应到 python 中和 struct sequence 或 namedtuple 比较像.

  namedtuple 为了和 field 区分, 它自己的 methods 和 attributes 都是以 ``_`` 起始的,
  让人误以为 API 只有 tuple 的 ``.index`` 和 ``.count``. 实际上它还有 ``_make``,
  ``_asdict``, ``_replace``, ``_source``, ``_fields``.

- ``key=`` parameter in various comparison-related functions

  ``sorted``, ``list.sort``, ``max``, ``min`` 等函数中的 ``key`` keyword parameter
  的逻辑是输入要排序的元素, 然后对每个元素的输出值进行比较, 根据这个比较结果进行排序.
  注意它不要求 key function 输出的是数值, 而只需要是可以比较大小的 object 即可.

  ``functools.cmp_to_key`` 通过实现 rich comparison methods 很好地利用了这一点.

- User-defined class 默认有 ``__hash__`` method. 这个默认的 hash method 保证它实例
  的 hash value 与该实例的 identity 一致. 即所有实例的 hash 不同, 通过 hash 值可以
  判断是否是同一个对象.

- interesting stuffs in `sys` module

  * ``sys.base_prefix``, ``sys.base_exec_prefix``,
    ``sys.prefix``, ``sys.exec_prefix``: 前两个和后两个在 virtual environment 中不同.

  * ``sys.byteorder``

  * ``sys.builtin_module_names``: modules built in cpython interpreter

  * ``sys._current_frames()``: 包含所有线程号和各自的 top stack frame

  * ``sys.displayhook()``, ``sys.excepthook()``,
    ``sys.__displayhook__``, ``sys.__excepthook__``:
    用于输出运算结果 (interactive) 和输出 traceback. ipython 解释器给前两个 hooks
    赋了自己的值.

  * ``sys.exc_info()``: 当前正在处理的 exception 信息. py3 中一般情况下没有理由直接
    访问这个量.

  * ``sys.executable``: absolute pathname of python interpreter

  * ``sys.exit()``: exit by raise ``SystemExit``.

  * ``sys.getdefaultencoding()``: default encoding used for ``bytes <--> str``
    decoding/encoding.

  * ``sys.getfilesystemencoding()``, ``sys.getfilesystemencodeerrors``:
    文件系统中文件名的 bytes 和 str 转换时, 使用的 encoding 和 error handler.
    即 ``os.fsencode``, ``os.fsdecode`` 使用.

  * ``sys.getrefcount()``

  * ``sys.getswitchinterval()``, ``sys.setswitchinterval()``:
    thread switch interval in secs

  * ``sys._getframe()``

  * ``sys.__interactivehook__``: called during startup in interactive mode. 默认
    这个 hook 用于加载 readline.

  * ``sys.maxsize``, ``sys.maxunicode``: max hardware integer, max unicode point

  * ``sys.modules``: loaded modules

  * ``sys.path``: module search pathes

  * ``sys.platform``

  * ``sys.ps1``, ``sys.ps2``

  * ``sys.stdin``, ``sys.stdout``, ``sys.stderr``,
    ``sys.__stdin__``, ``sys.__stdout__``, ``sys.__stderr__``:
    When interactive, standard streams are line-buffered.
    Otherwise, they are block-buffered like regular text files.
    To write or read binary data from/to the standard streams,
    use the underlying binary ``buffer`` object.

  * ``sys.version_info``

- binascii, base64, hashlib

  * binascii 包含 binary data 和各种基于 ASCII 的 printable 表达形式或编码形式,
    以及一些底层相关函数, crc 函数也在这里.

  * base64 包含更丰富的统一的 binary data 和各种进制转换.

  * hashlib 包含各种 hash 以及相关函数.

- interesting stuffs in `os.path` module

  * 一系列基于 ``stat(2)`` 的函数, 例如 ``exists()``, ``getatime()``, ``ismount()``,
    ``samefile()``, etc.

  * 一系列 path manipulation functions, 比较容易被忽略的有 ``split()``, ``splitext()``,
    ``commonpath()``, ``commonprefix()``, ``expanduser()``, etc.

- haskell 中的 ``fold*`` 和 ``scan*`` 对应于 python 中的 ``functools.reduce`` 和
  ``itertools.accumulate``.

- python 中, 各种 protocol 实际上是各种 interface 的规定. 满足这些协议 (interface)
  就可以按照相应的方式去使用. 这是 duck typing 的一种体现.

  已知的 protocols 有:

  * sequence protocol

  * iterator protocol

  * mapping protocol

  * context manager protocol

  * descriptor protocol

  * buffer protocol

- ``range`` 实际上是一种 builtin immutable sequence type. 因此支持常见的 sequence
  interface. 严格地讲, 就是 ``collections.abc.Sequence`` ABC 所定义的 interface.
  它是 iterable, 但不是 iterator.

- python 的一些函数和 haskell 类似函数的对应关系.

  * builtin::

      filter(pred, iterable)                 filter pred iterable
      range(stop)                            [0..(stop-1)]
      range(start, stop[, step])             [start,(start+step)..(stop-1)]

  * itertools::

      count(start[, step])                   [start,(start+step),..]
      cycle(p)                               cycle p
      repeat(elem[, n])                      take n $ repeat elem
      accumulate(p[, func])                  scanl1 func p
      takewhile(pred, iterable)              takeWhile pred iterable
      dropwhile(pred, iterable)              dropWhile pred iterable

  * functools::

      reduce(func, iterable[, initial])      foldl func initial iterable

- ``itertools.chain`` 用于将 iterable 连在一起, ``collections.ChainMap``
  用于将 mapping 连在一起.

- `struct` module

  * 对于一个 structure format ``fmt``, padding 只有在结构体成员之间自动添加, 而没有
    识别结构体末尾的 padding. 如需在 ``fmt`` 中指定结构体末尾的 padding, 可以用两种
    方式: 使用 ``x`` 来明确添加指定个数的 padding; 使用 ``0[t]`` 来隐性地添加 padding,
    其中 ``[t]`` 为 structure 的 alignment requirement (即结构体中各元素的最大 alignment
    需求).

  * 默认的模式是 ``@``, 即 byteorder, size of primitive types, alignment 都采用
    native value. 此外还有 ``=``, ``<``, ``>``.

- lambda 表达式中的变量是局域化在 Lambda 函数定义表达式中的:

    .. code:: python
      >>> [lambda x: x+1 for x in range(10)]
      [<function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>,
      <function __main__.<listcomp>.<lambda>>]

  ``lambda :`` operator 的优先级是所有算符中最低的. 注意 ``lambda`` 和 ``:`` 是一体的,
  整个部分要作为一个整体.

- 默认的 ``sys.stdout`` file-like object 使用的 error handler 是 strict,
  而 ``sys.stderr`` 使用的是 backslashreplace (从而向 stderr 输出的错误信息
  本身不会再次触发一个 ``UnicodeEncodeError``, 让原本的 traceback 等错误信息
  更加 messy). 若我们向 stdout 输出的信息可能包含无法编码的 binary data, 可以
  替换一个使用 backslashreplace handler 的对象:

    .. code:: python
      sys.stdout = open(sys.stdout.fileno(), mode="w", errors="backslashreplace")

- metalcass

  * 如何确定 the metaclass of a class:

    The appropriate metaclass for a class definition is determined as follows:

    - if no bases and no explicit metaclass are given, then type() is used

    - if an explicit metaclass is given and it is not an instance of type(),
      then it is used directly as the metaclass

    - if an instance of type() is given as the explicit metaclass, or bases
      are defined, then the most derived metaclass is used

    The most derived metaclass is selected from the explicitly specified metaclass
    (if any) and the metaclasses (i.e. type(cls)) of all specified base classes.
    **The most derived metaclass is one which is a subtype of all of these candidate
    metaclasses. If none of the candidate metaclasses meets that criterion, then
    the class definition will fail with TypeError.**

    例如, 以下代码会失败:

      .. code:: python

      class MetaA(type): pass
      class MetaB(type): pass

      class A(metaclass=MetaA): pass
      class B(metaclass=MetaB): pass

      class C(A, B): pass # TypeError!!!!!

    创建并使用 MetaA 和 MetaB 的共同子类 MetaC 则可以解决这个问题:

      .. code:: python

      class MetaC(MetaA, MetaB): pass

      class C(A, B, metaclass=MetaC): pass

  * 在 python3 中, class definition line 上面除了可以添加 ``metaclass=`` 这个 kwarg,
    还可以添加别的任意 kwargs, 只要 ``metaclass.__prepare__`` 以及 ``metaclass()``
    等操作支持即可.

- time, datetime

  * time.timezone 给出的 offset 是 localtime 和 utc-time 之差的相反数.

  * 对于 datetime.strptime classmethod, ``format`` 中包含 ``%z`` 时, 将生成一个
    timezone-aware 的 datetime object.

- membership test ``x in y`` 如何进行判断.

  * For container types such as list, tuple, set, frozenset, dict, or collections.deque,
    the expression ``x in y`` is equivalent to ``any(x is e or x == e for e in y)``.
    也就是说, 对于 builtin container types, 一个对象 ``is`` 或者 ``==`` container
    中的某个元素, 则认为这个对象在 container 中.

  * For the string and bytes types, ``x in y`` is True if and only if
    x is a substring of y.

  * 对于 user-defined class, 若实现了 ``__contains__`` 则使用这个 special methods
    来进行判断.

  * 对于 user-defined class, 若没有实现 ``__contains__``, 但实现了 ``__iter__``
    则通过 iterate 生成的 iterator 来找相等的元素.

- 一些 special methods:

  * ``object.__dict__`` 对象自身定义的所有 attrs.

  * ``instance.__class__`` 实例的类.

  * ``definition.__name__`` 对象的名字.

  * ``definition.__qualname__`` qualified name.

  * ``class.__bases__`` 一个类的基类们.

  * ``class.mro()`` 一个类 MRO 顺序. 该方法在 class instantiation 时调用, 结果存储
    在 ``class.__mro__`` 中.

  * ``class.__mro__`` 同上, 只记算一次.

  * ``class.__subclasses__()`` 一个类的所有直接子类. 使用 weakref 来保存这些子类的
    列表.

- 把整个 web 项目 (包含各种模板和静态文件) 做成一个 python package 用 setuptools
  打包成 pip 可安装的形式安装至 site-packages 目录下没有任何问题. 例如这是 django
  项目的推荐做法, ``django.contrib.*`` 等 subpackages 就是这么做的.

- 如何创建 read-only class attribute?

- django extension packages can be found on https://djangopackages.org/
  and downloaded from PyPI.

- pathlib

  * ``Path.resolve`` 有 ``strict`` 参数, 用于一步检查 resolve 的路径是否存在.

- string literal concatenation 操作具有最高优先级, 高于 subscription, slicing,
  call, attribute reference 等操作. 例如

  .. code:: python

    >>> ("{} sef"
    ... "sefe".format(111))
    '111 sefsefe'

- 当一个系统中需要多个 python 版本, 不同项目需要不同版本时, 或者仅仅是不想使用
  系统自带的 python 时, 使用 pyenv.
  当不同项目需要同一个 python 版本, 但各自的依赖有冲突时, 或者仅仅是因为不想
  将 package 安装至全局范围内时, 使用 venv.

- choose dnf/apt/pacman vs pip for python module installations

  * 在一个多用途的系统中, 例如 PC, 多服务共用的 server, 等场景中, 系统层的
    python 解释器被各个程序共用, 因此应该使用系统的 package manager 去安装
    python modules. 这样才能保证各个 package 的版本依赖关系得到满足, 即某个
    module 的版本是经过和其他 package 的兼容性测试的.

  * 对于某个用户、某个项目或某个程序自己使用的 python, 则使用 pip 安装.
    此时构建 virtualenv 或 pyenv, 将 modules 安装在局限的范围内, 与全局独立.

  * 对于为某个服务单独运行的容器, 可以使用 pip 安装系统层的 modules. 因整个
    容器为它服务, 不太需要考虑跟别的兼容.
