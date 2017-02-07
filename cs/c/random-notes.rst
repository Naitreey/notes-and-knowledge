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
