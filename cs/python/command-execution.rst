invoke
======

Context
-------

methods
^^^^^^^
- ``run(command, **kwargs)``. returns Result. raises: UnexpectedExit, Failure,
  ThreadException. kwargs:

  * ``shell``. default /bin/bash.

  * ``warn``. Whether to warn and continue, instead of raising UnexpectedExit
    when command exit nonzero. default False.

  * ``hide``. prevent stdout/stderr from printing to local terminal. default
    None, print everything. can be: out/stdout, err/stderr, both/True, None.

  * ``pty``. Open a pty that connects to the command, rather than connects
    directly to the invoked process and reads its stdout/stderr streams.
    Due to their nature, ttys have a single output stream, so the ability to
    tell stdout apart from stderr is not possible. As such, all output will
    appear on ``out_stream``. default False.

  * ``fallback``.

  * ``echo``. whether run prints the command string to local stdout prior to
    executing it. Default: False. ``hide=both/True`` overrides this.

  * ``env``. a dict of environs updating/replacing environ of child.

  * ``replace_env``. If True, replace env rather than update. default False.

  * ``encoding``. Override auto-detection of decoding of output streams.

  * ``in_stream``. A stream as child's stdin. default is current python
    process's sys.stdin. 也就是说, 可以从 python script 外面 write 至
    sys.stdin, 然后让 child 读取. If False, will disable stdin mirroring
    entirely. If False, will disable stdin mirroring entirely.
    .. XXX 似乎无法输入 EOF? 这导致 child 一直等待无法退出, 例如 cat.

  * ``out_stream``. write child's stdout to this stream (as well as captured to
    Result instance). default is current python process's sys.stdout.

  * ``err_stream``. ditto for stder (as well as captured to Result instance).
    default is sys.stderr.

  * ``echo_stdin``. Whether to write data from in_stream back to out_stream.
    default None. In this case, the echoing is occurred when both of the following
    is true:

    - Not using a pty to run the subcommand, tty does its own echoing.

    - ``in_stream`` appears to be a valid tty.

  * ``watchers``. A list of StreamWatcher for auto-response. default [].

  run method 不适合从 stdin 进行文件传输, 因读取太慢 (chunk 太小, 可能是 1byte
  为单位).
