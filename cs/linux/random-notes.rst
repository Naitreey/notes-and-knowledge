- 线程的目的不仅仅是为了 *同时的* 并行计算, 而是为了构建多个独立的运算单元.
  将这些运算单元分配到不同的 CPU 核上才具有 "同时并行" (parallel computing) 的意义.
  python 虽然有 GIL, 但这影响的是单 python 进程进行 parallel computing 的能力,
  并没有影响多线程所带来的其他可能性.

  所谓 concurrency, 指的就是多个任务同时处于进行中的状态, 即多任务并发.
  这可以在单个线程中实现, 例如多任务的异步处理 (e.g., python 中的 asyncio);
  也可以在多线程和多进程中实现, 以实现多个独立的运算单元.

- 为什么 shared library 具有 executable bit set?

  1. 历史原因: 一些 unix 使用 shared library 文件的 rwx 权限来对应 `mmap()`
     至进程虚拟内存中的机器码的 rwx 权限.

  2. 一些 shared library 确实可以执行, 比如 `libc.so.6`.
