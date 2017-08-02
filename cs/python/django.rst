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

- URLconf 中的 url pattern 在载入时就都编译好了, 所以是高效的.

- 日期时间使用 django.utils.timezone 里的函数, 它们会自动根据 settings.py 里的时间
  相关设置来返回恰当的结果. 直接使用 datetime module 还需要去手动读取配置.

- model 里各个 field 的名字和类型直接影响它们在 admin.site 的显示和交互方式.
