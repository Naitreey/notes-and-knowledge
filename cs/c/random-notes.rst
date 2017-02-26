- 对于以下情况: 如果写一个库函数来封装第三方库, 该库函数所应达到的目的是, 封装第三方
  库函数调用的相关细节, 从而方便使用. 由于 C 缺乏 exception 机制, 只能靠返回值判断
  错误 (what? 实现一个 errno?), 因此只应返回与使用者相关的必要错误, 遇到其他的非预期
  的错误则直接输出错误信息并 abort.

- header file 中应该有 guard.

  .. code:: c
  #ifndef HEADER_H
  # define HEADER_H
  ...
  #endif

- When including headers, the order should go from *local to global*, each
  subsection in alphabetical order:

  1. header for this `.c` file
  2. headers from the same component
  3. headers from other components (within the same project, third party, etc.)
  4. system headers

  这样, 能够保证 local header 不对 global header 有 implicit dependency.

- All headers (and indeed any source files) should include what they need.
  They should not rely on their users including things.

- Always follow the clearest and most sensible coding style that you know of.
  有很多开源项目的代码不那么清晰 (e.g., util-linux), 但也有很多项目的代码
  是 clear and sensible 的. You want to be the latter not the former.

- 在 syscall 层面上只有一个 read(2), 它只能读指定数目的 bytes. 对于一般情况
  下的 blocking mode, read 不到时就 block (kernel 把它放到了 wait queue 中),
  若 kernel 发现 EOF 了 (file seek past EOF, 或 pipe write fd closed 等),
  则调度返回给 read, 然而 read 发现读不到东西, 就返回 0, 表示 EOF.
  In other words, 对于 read(2), 在遇到 EOF 之前, 执行 read(2) 可能产生两种
  情况: 1) 读到东西, 返回读到的数目; 2) blocking, 直到读到东西. 对于 non-blocking
  mode, 第二种情况为报错 EAGAIN. 然而注意, 这些情况都可以与 EOF 区分开.
  在 stdio 层面, read(2) 的结果存在 stdio buffer 里. fgets 以及 python readline
  等都是在这个 buffer 里进行读一行或读 N bytes 的操作. 否则岂不是要做很多的 syscall.
