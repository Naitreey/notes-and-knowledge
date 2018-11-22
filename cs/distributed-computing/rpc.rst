- RPC: Remote Procedural Call.

- 一个 RPC 指的是一个程序中需要远程执行的 subroutine/procedure. 这个 subroutine
  需要通过网络去远程执行一段代码. 这段被远程执行的代码就相当于这个 subroutine
  的实现细节.

- 抽象执行流程:

  * The client calls the client stub. The call is a local procedure call, with
    parameters pushed on to the stack in the normal way.

  * The client stub packs the parameters into a message and makes a system call
    to send the message. Packing the parameters is called marshalling.

  * The client's local operating system sends the message from the client
    machine to the server machine.

  * The local operating system on the server machine passes the incoming
    packets to the server stub.

  * The server stub unpacks the parameters from the message. Unpacking the
    parameters is called unmarshalling.

  * Finally, the server stub calls the server procedure. The reply traces the
    same steps in the reverse direction.

- 一个 RPC 在调用时与 local call 形式是相同的. 所以称为 "procedural call".
  正因为它是一个 procedural call, 所以 RPC 要有返回值. 

- 一般定义的 RPC 指的是 synchronous RPC. 即 request side 处于 blocking 状态,
  等待 response side 执行完毕后返回结果, 再继续执行自己的逻辑.

  这样定义的 RPC 并不考虑返回 future/promise 作为结果封装的情况.

  这样, RPC 与一般性的远程任务分发的区别是, RPC 强调同步的操作. 而一般的远程
  任务分发可以是异步的, request side 无需阻塞式等待结果返回.

- The RPC model implies a level of location transparency, namely that calling
  procedures is largely the same whether it is local or remote, but usually
  they are not identical, so local calls can be distinguished from remote
  calls (For example remote calls are often orders of magnitude slower, they
  can fail because of network failure, etc.).

- 是否使用 RPC model 取决于 request side 是否要等待执行结果返回后才能继续执行.
  若使用 RPC model,

  * Make sure it's obvious which function call is local and which is remote.
  
  * Document your system. Make the dependencies between components clear.
  
  * Handle error cases. (How should the client react when the RPC server is
    down for a long time?)

  若 request side 不是必须等待执行结果才继续, 则可以使用异步执行的模型. 例如,
  event-driven/event-loop 形式, 结果作为 event 返回; 或者返回一个
  future/promise, 在需要的时候访问结果; 或者将远程执行结果发给下一个执行阶段,
  构成一系列相互依赖的任务 (类似 Celery Canvas).
