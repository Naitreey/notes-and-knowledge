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
  - read traceback
  - print, dump, etc.
  - logging
  - pdb
  - code.interact, jump to interactive interpreter at the exact point you want
  - python -i, 简单的 post-mortem debugging
  - python -v[v], 检查 import 是否符合预期 (sys.path 是否正确, pyc 是否正确等)

- testing methods:
  - python -W default, 所有 warnings 都显示, 即开启默认不显示的那些警告
  - doctest
  - unittest

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
  实际上 `dict` 类型实现了 key-order 符合 key 的 creation order.
  Ref: https://mail.python.org/pipermail/python-dev/2016-September/146327.html
  Ref: https://docs.python.org/3/whatsnew/3.6.html#pep-520-preserving-class-attribute-definition-order
  但是我还是更愿意用 `OrderedDict`.

- 不该在 iterate list 或 map 的时候修改该对象的长度, 例如删除 element or key-val pair.
  对于 dict, 在 py3 中这是 `RuntimeError: dictionary changed size during iteration`.

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

