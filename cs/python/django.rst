- django term: project vs app.

  一个 project 就是一个 project, 一个项目. 一个项目可以是一个组相互关联的事物、
  事情和功能的集合, 它们构成一个抽象整体.

  一个 app 就是这个 project 中的一件事情, 一个功能, 一个模块等. 它可以单独存在,
  具有自洽的逻辑和组成. 也可以是更大整体 (即 project) 的组成部分.

  注意适当地按模块化思路将 project 拆成 apps. Your apps don't have to be reusable,
  they can depend on each other, but they should do one thing.

  Try to answer question: "What does my application do?". If you cannot answer
  in a single sentence, then maybe you can split it into several apps with cleaner
  logic.

  对于仅有一个功能模块的项目, 可以简单地将 project 直接应用为 app.

- app

  django 提供了很多方便的功能使得 project 在 app 尺度的模块化成为可能, 例如
  模块化的 URLconf, ``include()``. 每个 app 可以独立存在, 又可以在整个项目中
  plug-and-play (PnP). 与 app 模块化配合的是 RESTful url 的模块化, 并要求
  url 层级清晰. 每个 app 的 URLconf 自成体系, 有 index, 有 object, 有 method.

- URLconf

  * URLconf 中的 url pattern 在载入时就都编译好了, 所以是高效的.

  * 每个 app 的 URLconf 中应该包含 ``app_name``, 即它是 url name 的 namespace.
    可避免不同 app 的 url name 相互覆盖.

- 日期时间使用 django.utils.timezone 里的函数, 它们会自动根据 settings.py 里的时间
  相关设置来返回恰当的结果. 直接使用 datetime module 还需要去手动读取配置.

- model

  * model 里各个 field 的名字和类型直接影响它们在 admin.site 的显示和交互方式.

  * model 是一个数据对象类型, 它是数据库表的抽象. 或者从另一个角度来看, 由于 model
    的存在, 要求数据库表应该按照 object-oriented 的方式进行设计. 而一个 entry 就是
    一个 instance. 这是一种比较好的设计思路.

  * model 定义时 field 以 class attribute 方式去定义, 而实例化后, 每个实例会
    生成同名的 attribute 在自己的 ``__dict__`` 中, 覆盖 class attribute.

- view

  * view 这个概念没有什么很好的意义. 应该说, 从一定程度上, HTTP 的请求可以看作是
    对整个 app 的不同视角 (view), 但这种说法有些牵强. 总之, views 就是对 url
    请求的 server 端实现.

  * 每个 view 都必须返回 HttpResponse instance 或者 raise some exception. 任何其他
    结果 django 都认为是有问题的.

- template

  * template namespace. 每个 app 下可以有 ``templates/`` 目录, 不同 app 的 templates 目录
    在一个 namespace 中, 因此会相互覆盖. 所以需要再创建 ``templates/<app>`` 子目录.

  * template 中 object 的 ``.`` operator 的查找顺序:
    dict key, object attribute, list index.

  * 在 template 中使用 symbolic url, 即使用 url 的名字, 而不写死 url 路径在模板中.
    这样可以降低 template 和 URLconf 之间的耦合. 在重构 url 结构时, 不需要修改模板
    文件.

- test

  * model 层的 test 的测试点是测试 model 的正确性、合理性;
    view 层的 test (配合 urlconf) 测试的是操作是否符合预期.
    因此前者手动操作数据库, 而后者模仿 useragent 用 client.
