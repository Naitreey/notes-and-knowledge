The absolutely meaningful reason to write clear code is to make the life of other developers easier, to make their life more efficient.

design patterns and refactoring (至少对于传统语言) 是通用的, 因为它们都是同一种思想的发展和延续, 也就是使逻辑不断清晰化, 简洁化, 条理化. 对于不同的传统语言, 有些已经在语言层面提供了特性, 从而使一些 design pattern 变得简单实现且直接了当; 而另一些则需要手动将这些思想进行实现. 但是本质上, 思路是相似的, 目的是相同的.

-----
写之前:
- 明确需求, requirement specification
- 程序设计, design pattern

写:
- 实现

写完之后:
- Make it work     , make it better                  , make it faster
- test (unit test) , source code checking (refactor) , profiling

(这些流程会自然地穿插进行或省略, 但是这是一个基本的思路和步骤.)

-----
- 程序中不要出现同一个名字代表两种不同的对象. 例如, mount_info 可以是一个数据对象, 而保存它的表则可以称作 t_mount_info.

- refactoring: 只传递绝对必要的参数进入函数或方法.

- refactoring: 对于作为 API 的函数, 函数的 signature 应该告诉使用者它干了什么事情 (即操作目的) 以及它需要什么相关信息即参数表. 这样才可能具有通用性, 因为所有需要的信息都明确地定义了. 使用者只要传递满足的参数就可以实现对应的操作, 而不论这些参数是如何聚集起来的. 反之, 如果函数的参数表只是一个 dict, 绝大部分情况下使用者必须知道字典的结构才能有效地使用这个函数. 这就增加了使用上的不确定性. 因此一般的函数应该有确定的 signature, 并且 signature 中的每一项都有不具有不确定性.

- 通过将所需数据 formalize 为一个固定的数据结构, 降低了界面和后台的耦合; 通过明确化 API 函数的接口 signature, 进一步降低了模块和模块之间的耦合.

- refactoring: 对于内部的根本不准备通用的函数, 其实怎么方便怎么来就好了.

- refactoring: 对于可能复用的函数(或代码), 它对其他资源和信息的依赖需要尽量小, 即依赖程度降低复用程度提高.

- 界面的变化不造成保存的有效数据的变化, 即界面与系统数据弱耦合.

- get... 这类方法不该有 side effect.

- 使用专有结构来 formalize 一定的数据定义, 例如结构体, 类等. 并将对这些结构的操作 (例如, 检查, 转换形式等) 封装在它的类中 (或模块中).

- 能一般化的函数就尽量一般化, 一般化以后分出去成为一个模块.

- 类 (静态类除外) 的构造是围绕于数据的, 当我们发现有这么一些数据和另一个对数据的操作时, 将一定数据和对数据的操作封装起来可能抽象程度更高更自然, 这时才需要构建类. 反之, 如果只是一个无状态的操作, 一个 procedure, 封装成一个类(并且进行尴尬的实例化)就显得没那么必要, 这时只需要将相关的操作归类到一个模块(文件) 中即可达到归纳和抽象的作用.

- 若一个值需要复杂的过程才能算出, 并且这个运算过程没有 side effect, 则可以把运算结果缓存下来, 以后直接取结果, 而不再执行复杂的运算. Python 本身支持这种方式, 可以通过 non-data descriptor 实现.
- 在完成代码后, 需要高效率时, 可进行整体 profile 以及每部分代码的 profile. 对每个部分进行 profilie, 可以得出哪个部分代码对效率影响大 (从而需要多加考虑), 哪个部分对效率影响小 (从而可以更加灵活地处理).
- profiling 时, 注意设置每次调整后自动进行结果检查, 以保证结果不变.
- 在代码中布置全局函数时, (在解释器/编译器允许的前提下,) 顺序应该由抽象至具体. 即由整体操作至具体操作. 因为认知的顺序就是先了解要做什么, 再了解该怎么做. 否则会出现只见树木不见森林的混乱情况. 一般的语言在编译或解释函数时, 都不直接执行函数体, 因此可以做到由抽象至具体的函数布局. 然而 shell script 却不是这样, 因此无法做到.
- 每个函数的功能应该尽量纯粹, 警惕流水线式的、意大利面条式的代码. 比如, 取什么东西的函数就应该返回这个东西, 而不是在这个函数中插入不相关的逻辑. 尽量先把抽象的逻辑摆在一起, 并且先摆出来, 细节再步步深入.
- 警惕代码之间的依赖关系: 若两个功能部分在逻辑上不包含依赖关系, 在代码实现上也不该包含依赖关系. 尤其是, 两个逻辑上独立的部分, 一部分代码的执行异常不该导致其他部分代码的异常.

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
    segfault, 等. 这类不可控, 也不该控制的绝对错误. stdout 则平时可以空闲,
    也可以输出比如 `--help`, `--version` 等信息. 当程序长期运行时, stdout
    与 stderr 可以一起转至一个文件, 阅读起来方便.

    对于 one-off program: 一般不具有日志, 但开启 verbose/debug mode 后,
    相关信息也相当于日志, 应输出至 stderr (是否开启 verbose/debug, 可通过
    handler 是否添加等方式实现). 特殊比如 make, 则单开 stream 写日志.

  * 在哪里产生 log 就在哪里创造 Logger, 因为 Logger 包含位置信息, 没必要也不该传来传去.

- You should always write your code as if comments didn't exist. This forces you to write your code in the simplest, plainest, most self-documenting way you can humanly come up with.
when you can't possibly imagine any conceivable way your code could be changed to become more straightforward and obvious -- then, and only then, should you feel compelled to add a comment explaining what your code does.

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
  使用 (), 即 `(a | b | c)` 的格式来表达必须从多项中选择一个.

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
