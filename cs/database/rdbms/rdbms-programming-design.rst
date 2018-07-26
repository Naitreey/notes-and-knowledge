- 是否应该利用数据库提供的 binary field type 去保存文件?

  不该. 原因:

  1. 在数据库中保存文件将导致数据库体积迅速增长, 这些二进制数据将占用数据库体积
     的绝大部分. 这导致的问题是: 不必要的内存占用量大大增加; 而且体积大的数据库
     更难以维护, 例如备份更慢, 甚至实际难以备份.

  2. 加重数据库的读写负担. 文件比数据需要更长时间的读写, 所以应用和数据库的连接
     需要维持更长时间, 整体上加重了并发连接数和负载. 而这些文件很多时候可以由
     前端服务器如 nginx 去提供. 此外, 由前端服务器去 serve 静态文件也更高效, 因为
     可以并发.

  3. 以 mysql 为例, 一些数据库在涉及到 binary field 类型的语句时, 反而会去硬盘
     上创建临时表, 这样反而降低了执行速度.

  4. 使用文件系统保存文件, 也很容易迁移存储架构, 例如从硬盘存储迁移至分布式存储.

- 对于具有少数几个确定字符串值的 enum 类型量, 应该在数据库里存储字符串本身还是
  integer flags?

  存储字符串, 或者使用 RDBMS 本身支持的 enum 类型 (例如 mysql), 这样存储时是数字、
  读写时是字符串. 理由:

  首先, 在现今的计算能力下, 从字符串至 int flag 的转换是 micro optimization.
  存储字符串 (或 enum) 带来的好处大于它造成的问题. 好处: 数据可读性更高, 不需要
  业务逻辑代码进行翻译, 且部分前端/GUI 可直接使用这些数据, 程序员不需要记忆无聊
  且易错的 enum table. 坏处: 需要更大的存储空间.

  由于硬盘相对于程序员的编程时间和排错时间便宜很多, so anything that trades
  development effort for disk space is also a good thing, from a business
  perspective.

  其次, 对于支持 enum 类型的数据库, 则可以使用这个类型在两方面之间达成一个折中.

  aside: the scripting language Lua, renowned for being direct and
  high-performance, used to write entire game engines, etc. They never bothered
  having a number type at all. Their string handling code is so effective, they
  can add numbers together that are actually strings, in time-sensitive game
  engine code. Like JavaScript, they don't even have objects - just very fancy
  hash tables. The C programmer's view of "a huge array of chars? How
  inefficient!" is outdated.

- 在 RDBMS 里保存 JSON 合适么?
  
  这取决于两方面:
  
  * 准备以 json 形式保存的数据到底是做什么用的.
  
    如果这个 json 数据虽然结构可能复杂, 但是从概念上实际上是一个完整的数据单元,
    也就是说, 你自己的业务逻辑并不需要 (频繁) 对这些数据内部的字段进行单独访问和
    操作, 而只是整块取出、整块写入时, 就可以使用 JSON 保存. 常见的场景有: 保存
    历史信息, 保存日志信息, 保存不需后端 manipulate 的复杂信息.

    如果你需要对 JSON 中的字段单独访问, 进行数据库操作, 例如 join, filter, index 等,
    则一般来讲不适合作为整块 JSON 保存. 但若数据库本身支持 JSON 类型的复杂操作,
    则需具体考虑.

  * 数据是否具有变化比较大的格式差别. 如果是这样, 可以考虑用 JSON 保存. 但
    如果需要对 JSON 中的字段进行单独访问、更新等操作, 见上述.

  A rule of thumb: 一般情况下尽量把数据 normalized 化. 尽量避免存储 json, 而是
  扩展成 fields 或者 foreign key 连接的 extension table 等形式. 这样可能长期看,
  对于 MVC 和减少重复是有好处的 (因为格式在 model 中都建立好了, 不需要手动解析
  数据构建 json 等).
