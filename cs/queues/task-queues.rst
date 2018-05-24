General
=======

- Asynchronous task queues 经常用在 web 后端架构中, 用于 delegrate
  long-running tasks to a separate execution unit. 从而作为服务
  响应主体的 web server 可以迅速返回响应给客户端, 完成 request-response
  cycle.

- 交给任务队列去执行的任务, 一般具有以下特征:

  * long-running task.

  * Calling external API, whose execution time is not under control of the
    calling program.

  一些例子:

  * email user.

  * spread really large bulk database operations over time.
