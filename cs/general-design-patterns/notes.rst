- The absolutely meaningful reason to write clear code is to make the life of other
  developers easier, to make their life more efficient.

- design patterns and refactoring (至少对于传统语言) 是通用的, 因为它们都是同一种思想的
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

- 多个进程或线程向同一个文件输出信息, 如果不谨慎处理, 很可能造成不同来源的输出相互
  覆盖, 残破不全. 所以最简单的办法是每一个来源 (进程或线程) 的输出先单独输出至一个
  文件, 后续如有合并的需要, 则根据 timestamp 等标志来将这些文件结合在一起.

  如果多个进程或线程一定要向同一个文件输出信息, 为了保证信息不相互覆盖, 有以下办法:

  * 使用访问控制, 如 file lock 或 mutex, 保证同一时间内只有一个进程或线程对该文件
    进行了写操作. 在此基础上, 仍需考虑不同的 file description 的 offset 是相互
    独立的, 否则仍然可能覆盖.

  * 所有进程或线程都使用 `O_APPEND`, 从而保证了写操作是 atomic appending, 不会相互
    覆盖. 为了保证信息不相互交错, 还应该使用 line-buffered 或 unbuffered. 这是唯一
    靠谱的方法.

  另一种更好的办法是, 让一个单独的进程或线程作为 receiver 去写文件, 所有其他信息源
  通过 socket 或者 queue 等方式向这个 receiver 发送要写的信息. 从而保证了时序性且
  不重叠.

  refs:
  https://stackoverflow.com/questions/7842511/safe-to-have-multiple-processes-writing-to-the-same-file-at-the-same-time-cent
  https://stackoverflow.com/questions/12942915/understanding-concurrent-file-writes-from-multiple-processes

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

- 关于 weekyear & week of year 方面的计算, 应该使用 ISO 8601 standard, 这样对于不同语言
  都可以做到一致. 例如, Python 中 datetime 和 Java 中的 GregorianCalendar 都支持 ISO 8601.

- 一个比较通用的日期和时间格式是 ISO 8601. 不同的语言和数据库等应用对它的支持比较普及.

- 如何设计数据统计逻辑

  两种基本实现思路:

  * 定期聚合并保存统计结果.

    - 优点: 统计数据持久保存. 多次访问不会增加运算负荷. 且原始历史数据的删除不影响
      历史统计数据.

    - 缺点: 由于是定期执行聚合统计, 实时性方面有妥协. 该问题可以通过部分实时聚合来解决.

  * 请求时再一次性聚合并返回统计结果.

    - 优点: 结果有实时性.

    - 缺点: 运算负荷与统计数据访问次数正相关. 由于是实时结果, 若删除原始历史数据,
      历史时间的统计数据也实时改变.

  孰优孰劣取决于具体需求对哪方面的要求更高.

- 意图是作为全局常量的量应当全部大写, 以示区别对待.

- 业务逻辑与底层数据库具体操作之间需要封装一个 middleware, 它提供业务逻辑与数据库交互
  的 API, 封装具体的数据库交互实现, 目的是做到业务逻辑中不暴露底层数据库操作, 从而
  将对数据库实现方面的修改限制在 middleware 模块中.

- loose coupling: 降低耦合, 概念清晰化, 实现模块化, 功能界限明确化. 这是任何设计要
  遵循的基本思想.

- Code without tests is broken by design. 模块化和单元测试是相互促进的.
  单元测试的实施, 要求代码是模块化的, 可单元测试的.

- test case 应该尽可能的多, 从而覆盖更多的场景、可能的情况.
  也就是说, 我们不介意 test case 的数量太多, 但需要仍需关心每个 test case 的实现质量.

- A separate test class for each model or view

- A separate test method for each set of conditions you want to test

- test method names that describe their function

- 设计 API 时, 如果它们有共同的前提条件, 则应该在模块加载时统一检查. 例如,
  一个类提供的所有公有方法有共同的前提条件, 则应该在对象初始化时进行检查.
  从另一个角度看, 就是说这个类不能在此环境创建对象.

- public and non-public members

  在设计类时, 一定要考虑好哪些 attributes/methods 是公有的, 哪些不是公有的.
  因为公有的就意味着你需要保证 (在至少一个 major version 内,) 这些公有 API 一直
  向后兼容.

  如果不知道是不是该公有, 那就先设置为非公有. it's easier to make it public later
  than to make a public attribute non-public.

  如果一个类可能被继承, 还需要考虑哪些 attributes/methods 是可以被继承的, 哪些
  只应该被这个类自己去使用, 并进行相应的设置.

- 当设计接口、配置文件等时, 可以通过某种方式来指定版本, 以做到轻易的向后兼容.
  此时, 只需根据不同的版本号, 选择不同的处理逻辑即可.
  例如 url API 的话, 可以 ``/v1`` ``/v2`` 下面再是具体的功能接口; 配置文件可以
  设置 ``version`` 字段.

- In today’s complex real world environments there isn’t a single best way
  to do anything.

- 在框架中提供各种 hooks, 作为可以任意扩展的衔接点, 是很重要的灵活性设计.
  参考 django 中, ModelAdmin, View, Form 等的设计. 对于一个参数或操作, 它们
  往往提供了默认值或默认实现, 以及各种 ``get_XXX`` 方法. 用户除了可以重新
  赋值、覆盖等静态自定义之外, 还可以通过自定义 ``get_XXX`` 来动态自定义.

  hooks 一般地讲都是函数, 但对于很多语言, 函数概念是一般化为 callable object.
  因此, hooks 定义很多时候也可以是 class 定义. 当 hook 逻辑很复杂时, 这有助于
  优化代码组织方式和重用等可能.

- code reuse

  * mixin class.
    Mixins are an excellent way of reusing code across multiple classes, but they
    come with some cost. The more your code is scattered among mixins, the harder
    it will be to read a child class and know what exactly it is doing, and the
    harder it will be to know which methods from which mixins to override if you
    are subclassing something that has a deep inheritance tree.

  * 抽象一般化函数.
    若需要重用的逻辑仅仅是单一的函数逻辑, 则可以简单地抽象出一个公有的函数.
    组织化地放在恰当的全局位置或单独的模块中. 然后在需要的类中调用它. 这没有什么
    不对的. 没必要一定去写 mixin class, 不要过分复杂化.

- multiprocessing, concurrency, race condition, conflict

  * 多进程、多线程写入、修改同一资源, 或 unique key 资源时, 若遇到冲突或竞争关系,
    最基本的解决办法就是使用循环.

- A common pattern in computing: Systems start off in a very simple mode,
  probably the first invented. Then, by examining their environment and
  possibly talking to other systems, they shift up to more advanced, and
  probably more efficient, modes - provided circumstances are right. Look at,
  for example, the way USB systems climb up from USB 1 to 2 to 3 when they find
  that the other end is capable of doing the more advanced operation; CPU
  starts off in real mode then gets switched to protected mode or long mode
  when firmware (needs and) finds that CPU is capable of advanced modes.

- 如何优化递归算法, 防止 stack overflow:

  * 使用 tail recursion. 注意前提是解释器、编译器等本身可以识别和优化 tail recursion.

  * 通过 recursion counter 来检测递归层数, 避免 overflow or OOM. 很多语言自己就有
    recursion level limit, 所以这个不一定需要.

  * Use right algorithm for right problem. In many times, iteration solutions are better.

- 代码文档、设计文档一定要保存在源代码仓库或者单独的文档仓库中, 或者是 wiki 形式
  保存, 并随着代码及时更新. 决不能把所有详细信息放在 issue 中, 然后一个 close 就
  淹没在了历史中, 变得难以查询和关联.

The principle of least privilege/exposure
=========================================
对于一个模块化的系统中, 任何一个组件按照设计功能工作, 只应对它提供绝对必须的资源,
赋予最小可能的权限集合.

意义:

* better system stability, 提高系统容错性. 因为 malfunction 被限制在了最小可能的影响范围.

* better system security. vulnerability & exploitation is restricted.

* 多个组件之间发生冲突或相互影响的可能性降低了, 非预期的行为更不易发生.

* 组件更容易部署和相互协作.

* 根据这个原理设计的组件往往功能更清晰, 更易用.

例子:

* 在代码实现时, 程序中的对象实体应该定义在所需的最小作用域 (scope) 内. 无论这些
  实体是 variable, function, class, etc. 这才是好代码.

* 在设计 API 时, 一个功能只应提供必须的参数. 功能本身也只返回必须的结果.

* 在 Linux 中, 一个进程的正常运行, 应限制在最低可能的用户和 capabilities.

* 用户的权限, 应该设置在他正常工作所需的最低权限.

Callback -- Inversion of control
================================
- 当使用 library API 去传入 callback 时, 是把程序的控制权交给了这个 library, 这样
  造成了 inversion of control, 即变成了 library 去控制接下来你的程序该怎么运行.
