- 对于以下情况: 如果写一个库函数来封装第三方库, 该库函数所应达到的目的是, 封装第三方
  库函数调用的相关细节, 从而方便使用. 由于 C 缺乏 exception 机制, 只能靠返回值判断
  错误 (what? 实现一个 errno?), 因此只应返回与使用者相关的必要错误, 遇到其他的非预期
  的错误则直接输出错误信息并 abort.

- header file 中应该有 guard.

  .. code:: cpp
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

- kernel space buffer (Linux buffer cache): 总是存在, 在用 read(2), write(2)
  syscall 时, 隐性地在内核中从这种缓存中读写数据.
  userspace buffer: 使用 C stdio 时, 隐性地使用了这种 buffer, 以减少 syscall
  的次数. 对 python 而言, io module 的 BufferedIOBase 自己有实现一个 userspace
  buffer.

- 在 syscall 层面上只有一个 read(2), 它只能读指定数目的 bytes. 对于一般情况
  下的 blocking mode, read 不到时就 block (kernel 把它放到了 wait queue 中),
  若 kernel 发现 EOF 了 (file seek past EOF, 或 pipe write fd closed 等),
  则调度返回给 read, 然而 read 发现读不到东西, 就返回 0, 表示 EOF.
  In other words, 对于 read(2), 在遇到 EOF 之前, 执行 read(2) 可能产生两种
  情况: 1) 读到东西, 返回读到的数目; 2) blocking, 直到读到东西. 对于 non-blocking
  mode, 第二种情况为报错 EAGAIN. 然而注意, 这些情况都可以与 EOF 区分开.
  在 stdio 层面, read(2) 的结果存在 stdio buffer 里. fgets 以及 python readline
  等都是在这个 buffer 里进行读一行或读 N bytes 的操作. 否则岂不是要做很多的 syscall.

- `O_RDWR` 中, 读写操作共用一个 file offset position.

- 可以使用 `setvbuf` 设置 stdio stream 的 buffer 情况. 该函数要求在 `open` 后和首次
  操作之前使用, 因此若要重设 stdin/out/err 的 buffer 类型, 应该先将底层的 file
  descriptor 重新包一次 stdio `FILE *`.

    .. code:: cpp
    stdout = fdopen(fileno(stdout), "w");
    setvbuf(stdout, NULL, _IOFBF, SIZE);

  NOTE: 一般而言, 对于 stdout/stderr 没必要设置为 unbuffered, 一般情况下 line buffering
  is fine, 需要立即输出时只需 fflush.

- 由于 vararg function 在 prototype 和 definition 时不规定函数的参数个数, 函数本身
  需要有某种办法知道传递到 stack 上的 (应该) 有几个参数, 以及这些参数的类型是什么,
  然后在函数体中使用 `stdarg.h` 获取 stack 上连续存放的值.
  因此, 在设计 variadic function 时, 一些规定了需要一个 format (e.g., `printf` etc.),
  一些规定了特定的 param list 的结束标志 (e.g., `execl` 的 ``(char *) NULL`` etc.).

- create shared library:

    .. code:: sh
    # compile PIC object file
    gcc -c -o foo.o -fPIC foo.c
    # link PIC object files into shared library
    gcc -o libfoobar.so -shared -fPIC foo.o bar.o

- create shared library and also executable by itself:

    .. code:: sh
    # compile PIC object file as above
    gcc -c -o foo.o -fPIC foo.c
    # link PIC object files into shared library (-fPIC), telling the linker
    # that this is a position independent executable (-pie), and make its
    # symbol table exportable (-Wl,-E) such that it can be linked against.
    gcc -o libfoobar.so -fPIC -pie -Wl,-E foo.o bar.o

  Position-independent executables (PIE) are executable binaries made entirely
  from position-independent code.

  ref: http://unix.stackexchange.com/questions/223385/why-and-how-are-some-shared-libraries-runnable-as-though-they-are-executables

- data structure alignment

  * alignment/padding 的意义在于:

    对于 primitive data type 类型的数据 (长度小于等于 bus width/word size),
    可以通过一次操作完成读写; 对于 compound data type 类型的数据 (struct,
    array, 等长度大于 bus width 的数据) 可以通过 ``sizeof (type) / wordsize + 1``
    次操作完成读写.

  * 一个 struct 类型的 alignment 由它最大元素的 alignment 要求所决定, 并且
    在结构体内部, 进行必要的 padding. struct 整体的 alignment 要求, 配合
    struct 内部各元素之间的 padding, 最终的效果就是让所有元素的内存地址都
    位于符合该元素 alignment 要求的地方.

    例如,

      .. code:: cpp
      struct mixeddata {
        char d1;
        short d2;
        int d3;
        char d4;
      };

    整个 ``struct mixeddata`` 结构体需要位于与 4-byte 对齐的地址上 (由 ``int``
    元素决定), 这是让结构体内部的 padding 能够正确发挥作用的基础; `d1` 后面
    pad 1 byte, 才能保证 `d2` 是 2-byte aligned; `d2` 后面 pad 2 bytes, 才能
    保证 `d3` 是 4-byte aligned; `d4` 后面 pad 3 bytes, 以保证结构体是 4-byte
    aligned.

    struct 的 alignment 要求, 对 struct 类型的大小 (``sizeof``) 有直接影响.

- notes on bit fields

  * bit fields 本质上是出现在结构体中的一系列特殊的元素. In other words,
    一个结构体中可以只有 bit fields, 也可以和其他普通的元素参杂在一起.
    而对于整个结构体而言, 仍然是结构体. 例如, 它的 alignment 仍然取决于
    最大 alignment 的元素 (对于 bit field, 则是它的 allocation unit, 即
    它的类型).

  * bit fields 的 allocation unit 只能是 4 个类型: unsigned int, signed int,
    int, bool. 这里的 int 不是 signed int, 而是 int with implementation-defined
    signedness.

  * bit fields 的类型和它占用的 bit length, 决定了它能存储的值的范围.

  * 对于 bool 类型, 它的 allocation unit 不是 1 bit, 而是 1 byte.

  * 对于 ``type : 0;`` 导致下一个 bit field 的起始地址在下一个 ``type``
    allocation unit 的地址边界处. 例如,

      .. code:: cpp
      struct x {
        int a : 1;
        bool : 0;
        int b : 1;
      };

    导致 b 从第 2 个 byte 位置开始.

      .. code:: cpp
      struct x {
        int a : 1;
        int : 0;
        int b : 1;
      };

    导致 b 从第 5 个 byte 位置开始. (假设 int allocation unit 的大小为 4 bytes).

  * bit fields 的地址无法获取, 因为 field 的起始位置不一定在 memory byte boundary 上.
