message queues
==============
- A message broker accepts and forwards messages.

- A general purpose message queue often used to:
  
  * dispatch background jobs, allowing web servers to respond to requests
    quickly instead of being forced to perform resource-heavy procedures while
    the user waits for the result.

  * message broker between (micro-)services 

task queues
===========
- task queue 是对异步执行任务这件事的完全实现. 它利用 message queue, persistent
  storage, etc. 工具, 实现了一套比较完整的异步任务执行方案.

- Asynchronous task queues 经常用在 web 后端架构中, 用于 delegrate long-running
  tasks to a separate execution unit. 从而作为服务响应主体的 web server 可以迅
  速返回响应给客户端, 完成 request-response cycle.

- The main idea behind task queues is to avoid doing a resource-intensive task
  immediately and having to wait for it to complete. Instead we schedule the
  task to be done later.

- 交给任务队列去执行的任务, 一般具有以下特征:

  * long-running task.

  * Calling external API, whose execution time is not under control of the
    calling program.

  一些例子:

  * email user.

  * spread really large bulk database operations over time.
