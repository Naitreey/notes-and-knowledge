Interesting stuffs in sys module.

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

