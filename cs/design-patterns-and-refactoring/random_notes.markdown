The absolutely meaningful reason to write clear code is to make the life of other
developers easier, to make their life more efficient.

design patterns and refactoring (至少对于传统语言) 是通用的, 因为它们都是同一种思想的
发展和延续, 也就是使逻辑不断清晰化, 简洁化, 条理化. 对于不同的传统语言, 有些已经在语言
层面提供了特性, 从而使一些 design pattern 变得简单实现且直接了当; 而另一些则需要手动将
这些思想进行实现. 但是本质上, 思路是相似的, 目的是相同的.

-----
写之前:
- 明确需求, requirement specification
- 程序设计, design pattern

写:
- 先构造和使用模块的 API.
- 再实现 API 的功能细节.
- 在过程中, 不断封装、抽象、提取公共成分、模块化、一般化, 不断迭代和重写.

写完之后:
- Make it work     , make it better                  , make it faster
- test (unit test) , source code checking (refactor) , profiling

(这些流程会自然地穿插进行或省略, 但是这是一个基本的思路和步骤.)

-----
- 程序中不要出现同一个名字代表两种不同的对象.

- refactoring: 只传递有用的参数进入函数或方法.

- refactoring: 对于可能重复利用的函数(或代码), 它对其他资源和信息的依赖需要尽量小,
  即提高通用程度.

- get... 这类方法不该有 side effect.

- 使用专有结构来 formalize 一定的数据定义, 例如结构体, 类等. 并将对这些结构的操作
  (例如, 检查, 转换形式等) 封装在它的类中 (或模块中).

- 能一般化的函数就尽量一般化, 一般化以后分出去成为一个模块.

- 类 (静态类除外) 的构造是围绕于数据的, 当我们发现有这么一些数据和另一个对数据的操作时,
  将一定数据和对数据的操作封装起来可能抽象程度更高更自然, 这时才需要构建类. 反之, 如果
  只是一个无状态的操作, 一个 procedure, 封装成一个类(并且进行尴尬的实例化)就显得没那么
  必要, 这时只需要将相关的操作归类到一个模块 (文件) 中即可达到归纳和抽象的作用.

- 若一个值需要复杂的过程才能算出, 并且这个运算过程没有 side effect, 则可以把运算结果
  缓存下来, 以后直接取结果, 而不再执行复杂的运算. Python 本身支持这种方式, 可以通过
  non-data descriptor 实现.

- 在完成代码后, 需要高效率时, 可进行整体 profile 以及每部分代码的 profile. 对每个部分
  进行 profilie, 可以得出哪个部分代码对效率影响大 (从而需要多加考虑), 哪个部分对效率
  影响小 (从而可以更加灵活地处理).

- profiling 时, 注意 unit test, 以保证结果不变.

- 在代码中布置全局函数时, (在解释器/编译器允许的前提下,) 顺序应该由抽象至具体.
  即由整体操作至具体操作. 因为认知的顺序就是先了解要做什么, 再了解该怎么做. 否则
  会出现只见树木不见森林的混乱情况. 一般的语言在编译或解释函数时, 都不直接执行函数体,
  因此可以做到由抽象至具体的函数布局. 然而 shell script 却不是这样, 因此无法做到.

- 每个函数的功能应该尽量纯粹, 警惕流水线式的、意大利面条式的代码. 比如, 取什么东西的
  函数就应该返回这个东西, 而不是在这个函数中插入不相关的逻辑. 尽量先把抽象的逻辑摆在
  一起, 并且先摆出来, 细节再步步深入.

- 警惕代码之间的依赖关系: 若两个功能部分在逻辑上不包含依赖关系, 在代码实现上也不该包
  含依赖关系. 尤其是, 两个逻辑上独立的部分, 一部分代码的执行异常不该导致其他部分代码的异常.

- 软件工程师最难得的一个良好思维模式就是能够做到:
  具体问题具体分析, 不被既往的经验所固化.

  经验是工具, 而不是教条. 只有最符合具体情况的解决方案才是最佳的解决方案.
  没有普遍适用的方案, 不是说大家都这样做, 你也就应该这么做. 你必须权衡, 考虑,
  从多种方法中选择一个, 更合适的.

- About logging.

  * 对于长期运行的进程, 该怎么记日志?

    如果你能访问 production system, 并且能够实时 debug, 那就只在开发时记日志, 这些日志
    只是便于开发; 放到生产系统之后, 则关掉 (绝大部分) 日志, 或者根本不记日志, 只依赖
    exception handling 和 core dump 之类的.

    如果不能访问, 就只能多记录一些日志.

    无论哪种情况, 都需要仔细考虑任意一处日志是否必要, 只在绝对必要的地方写日志.
    Resist the tendency to log everything.

  * 日志该向哪里输出?

    对于 long-running program: 比较完善的做法是, 日志单独开一个 stream
    输出至一个文件或一个目录 (rolling periodically). 日志不占用 stdout, stderr.
    这两个标准流用于输出需要在 terminal 中输出的信息. 例如, stderr 仅输
    出那些完全意外的信息, 即不是写在程序里的日志, 而是 uncaught exception,
    segfault 等不可控, 也不该控制的绝对错误. 对于具有 exception 机制的语言,
    应该在最外层包含一个 "catch all, log error and reraise/print-to-stderr" 语句,
    这样 uncaught exception 在输出至 stderr 的同时也输出在日志中, 方便理解发生错误
    的 context. stdout 则平时可以空闲, 也可以输出比如 `--help`, `--version` 等信息.
    当程序长期运行时, stdout 与 stderr 可以一起转至一个文件, 阅读起来方便.

    对于 one-off program: 一般不具有日志, 但开启 verbose/debug mode 后,
    相关信息也相当于日志, 应输出至 stderr (是否开启 verbose/debug, 可通过
    handler 是否添加等方式实现). 特殊比如 make, 则单开 stream 写日志.

  * 在哪里产生 log 就在哪里创造 Logger, 因为 Logger 包含位置信息, 没必要也不该传来传去.

- You should always write your code as if comments didn't exist. This forces you to
  write your code in the simplest, plainest, most self-documenting way you can humanly
  come up with.
  when you can't possibly imagine any conceivable way your code could be changed to
  become more straightforward and obvious -- then, and only then, should you feel
  compelled to add a comment explaining what your code does.

- 命令行参数的处理和 stdout/stderr.
  当用户指定参数 `--version`, `--help` 等, 不是 error condition, 因此输出应该在 stdout.
  只有出现参数错误时, 显示的 错误信息和 usage 信息才去 stderr.
  `--help` 时输出至 stdout 的 usage 信息可以是相对详细的, 错误时输出至 stderr 的 usage
  信息可以是相对简略的.

- 对于编程这门艺术, 算法之外, 另一个很重要的能力是分析问题和理解问题的能力, 对问题理解清晰、合理分解 (有哪些步骤, 哪些方面, 哪些模块, 哪些抽象层次) 是写出逻辑流畅、模块化清晰易理解的程序的前提.

- how to organize source tree?
  不同类型的项目有不同的组织和命名方式、规则. 但总体来讲, when in doubt,
  想想 linux, 尤其是 FHS 是如何对文件目录进行分类和命名的.

- 命令行语法说明规则
  使用 () 或 {}, 即 `(a|b|c)` 或 `{a|b|c}` 的格式来表达必须从多项中选择一个.

- 两个看上去类似的 class A B (功能类似, 作用类似, etc.), 何时该 B 继承 A? 何时该
  B wrap A?
  解决这个问题, 既有一些通用的逻辑, 又需要具体问题具体分析.
  1. 如果 B 不要暴露 A 的所有 public method, 则 B wrap A.
  2. 如果 B extends A, 或者对 A 的一部分 API 进行修改, 则 B subclass A.
  3. 面对具体问题, 最终才能决定到底是 subclass/wrap. 例如, 虽然 B 看上去是
     比较自然的 extends A, 但又要求 B 的一些功能可以独立与 A, 比如 python
     中 io.RawIOBase, io.BufferedIOBase, 则不能是 extends, 而是 wrap.

- 当需要对一个结果进行 if else 形式的分支处理时, 如果每个可能情况严格地处理都需要
  进行条件判断, 则严格地进行条件判断. else 分支只用于进行默认情况下的处理, 若逻辑
  上根本没有默认情况, 则应该添加 else 报错处理, 而不是忽略 else 分支.
  ```
  if condition1
      operation1
  else if condition2
      operation2
  else
      raise/set error
  ```

- 写数据库等的 client driver 时, 应该使用 lazy connection, 即不在创建 connection
  object 时就进行实质的连接, 而在第一次操作之前进行连接, 并且在断开连接后自动
  重新连接. 提供连接检查机制, 即可选地在创建 connection object 时就创建连接.
  提供在真实操作前连接以及断开重连的机制, 目的在于对服务端重启或意外断开连接等
  情况进行冗余.

- 修改文件的内容不该直接修改原文件, 应该写入 tempfile, 然后 mv. 这样的好处是若出错,
  原文件不会损坏. 使用 mv 的原因是, 操作 atomic, 对于 userspace 而言, 文件只存在新旧两状态.
  同理, 若要进行文件替换, 应使用 mv.

- 多线程程序的设计问题: 设现在有两个对象 A,B, B 是 A 的成员. 且要求 B 的主要逻辑单独
  在一个线程中执行. 仔细考虑到模块化, 对 B 的设计应该是以下这样:
  * B 的逻辑应该可以在单一线程情况下执行, 即 B 可以独立执行. 因此 A 不应该拥有
    B, 而是应该拥有一个去执行 B 的线程 B', 并且拥有一些同步机制成员和 B' 线程共享, 以
    控制 B' 的运行状态.
  * 更进一步, 这个 B' 线程可以封装成一个 B 的 manager, 负责线程的起停, 和主线程同步等.
    (从实现上, 可以 subclass `Thread` class.) 注意 B-manager 和 B 的逻辑区别, B-manager
    在主线程中工作, 它去 spawn 包含 B 逻辑的线程实例, 负责该线程的起停等操作.

- 不要怕 instantiation, 不要觉得某某操作每操作一次就创建一次对象是一件听起来很恐怖的事.
  实例化确实有损耗, 但是这个非常非常小, 在设计和实现阶段就担心这种损耗并进行代码逻辑
  调整是绝对的 "premature optimization".
  重要的是 **Write the code the way that makes sense to you.** 当所有程序逻辑实现已经
  完成, 才要去考虑效率问题, 去 profiling, 找效率瓶颈. 然而到那时, 更多的情况下, 效率
  瓶颈在于 I/O 等需要跟慢介质打交道的地方, 而不在于实例化.
  当然, 这不是说任意实例化都是合理的, 对于 really costly 的实例化, e.g., 实例化时需要
  初始化诸多东西, 需要做 I/O 等等慢操作, 则需要少做甚至只做一次. 或者从另一个角度, 优化
  class 的实现逻辑, 优化 instantiation 的消耗.

- 写 daemon 需要考虑的东西:
  * fork() 一次, 父进程退出, 做到 detach from controlling terminal,
    setsid() 获得新的 session; 再次 fork, 父进程退出, 子进程不再是 session leader,
    从而不具有重新获得 controlling terminal 的能力.
  * 所有的程序都会默认 stdin/out/err (0, 1, 2) 是 properly opened streams, 而它们
    到底是什么并不重要. 对于 daemon, stdin/out/err 显然不该再与 detach 之前的 tty
    相连, 而具体该如何处理, 则是需要考虑的.
    stdin should redirect to `/dev/null`. 这样无论谁从 stdin 读东西都会马上读到 EOF.
    stdout/err 根据程序设计, 可以 redirect 至一个输出信息的文件, 或者 `/dev/null`.
    对于转至 `/dev/null`, 则要求程序设计中有专门输出日志的逻辑实现.
  * daemon 不需要 one-off 程序那样的完整的执行流 (从 main 开始, 最后回到 main,
    并返回恰当的 exit status 至父进程). 这是因为:
    - daemon 需要长期运行, 执行 loop;
    - daemon 需要对 signal 作出反馈. 这基本上会包含对 SIGTERM 处理后 exit() 这种逻辑.
    由于对 signal 处理时, 是在当前的 stack 上叠加 signal handler stack, 因此如果
    SIGTERM handler 最后是 return 而不是 exit, 就会回到循环中. 所以 exit() 只能在
    stop() 中做, 不能在 main() 中做.

- **Beware of pitfall of empty string**
  任一字符串里都有 N 个空字符串. 这是写代码时必须被考虑到并处理的问题, 否则就是一个
  very illusive hidden nasty bug and it will kick you back so hardly.
  在 python 中,

  ```python
  "" in "..."
  ```

  总是返回 True, 可以这样解决

  ```python
  substr and substr in string
  ```

  在 cmdline 中, 对于一个非空文件 test,

  ```sh
  grep '' test
  ```

  总是成功并输出全文件内容 (注意对于没有任何内容的文件, i.e. length == 0), `grep ''`
  是失败的. 比较合理的解决办法是

  ```sh
  [ -n "$pattern" ] && grep "$pattern" file
  ```

- 一个操作是否满足 thread safety 的关键是看它是否修改 global state.

- 一个操作是否满足 reentrancy 的关键是看它能否 survive 递归调用.

- Cascading configuration override: 从低优先至高优先, 一级一级覆盖.

  * 代码里写死的配置值, 作为 last resort、fallback value, 由开发者固定.
  * /usr/{lib|share}/package, 由 vendor 管理的默认配置.
  * /etc/package, 全局配置.
  * 根据程序功能性质的需要, 可能还需要在 (/usr/share|/etc)/package.d 目录下
    设置一系列独立配置文件, 并按照 lexicographical 顺序应用和覆盖.
  * $HOME/.package 或 $HOME/.config/package, 用户全局配置.
  * /dir/package.conf, 本地配置.
  * 在每个配置文件中, 可以分别设置 global 性质的配置和 section 的配置. 后者覆盖前者.
  * environ 值覆盖配置文件中的值.
  * 命令行参数覆盖 environ 里的值.

  参考的例子有 pip, udev, systemd, sysctl, git 等的配置设计.

- Design versioning scheme
  可以参考 [python setuptools 的版本识别逻辑][setuptools], 来设计 versioning scheme.

- 无论使用哪种程序部署逻辑, 一定要设置机制以保证整个程序不依赖于放置在某个绝对的文件
  系统位置. 例如, 如果写的是 python module, 只需保证能够安装到 site-packages 下即可;
  如果写的是一套完整的程序, 可以通过判断主文件所在位置或通过 environ variable 来确定
  项目根目录.

- 如今对数据库、队列等 client/server 结构的程序模型中, client library 部分的设计往往
  满足以下特点:
  在 client object 实例化时不立即向服务端发起连接, 即 laziness, 只等到真正向服务器发起
  操作请求时, 即不得不连接时, 才会发起连接.
  这样做的好处有多个, 我能想到的有:
  * 避免维持没用的连接.
  * 面对多个 server 时 (分布式), 预先连接在逻辑上就不合理. 必要时才连接的话,
    client 可以在不同操作时选择不同的 server, 提高 availability 以及 load balancing.
  * client 的地位发生改变, 不再是一个 client 只对应于一个 server.
    当 client 可以选择多个 server, 预先连接就变得不合适, 除非开一个线程在后台创建
    connection pool.

- about software bug

  > Most coders think debugging software is about fixing a mistake, but that's bullshit.
  > Debugging's actually all about finding the bug, about understanding why the bug
  > was there to begin with, about knowing that its existence was no accident. It came
  > to you to deliver a message, like an unconscious bubble floating to the surface,
  > popping with a revelation you've secretly known all along.

  > A bug is never just a mistake. It represents something bigger. An error of thinking.
  > That makes you who you are.

  > The bug forces the software to adapt, evolve into something new because of it.
  > Work around it or work through it. No matter what, it changes. It becomes something
  > new. The next version. The inevitable upgrade.

  *Quote by Elliot from Mr. Robot*

[setuptools]: https://setuptools.readthedocs.io/en/latest/setuptools.html#specifying-your-project-s-version
