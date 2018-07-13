stateful and stateless protocols
================================

- 这里我们讲的 state, 指的是连接或通信所处的当前状态信息. 这些状态信息
  (若有), 则需要通信双方去保存.

- 一个协议的 state 属性 (stateful/stateless) 性质往往与 connection 属性
  (connection-oriented/connectionless) 是相关的.

- stateful and stateless protocols are often stacked into different
  layers in real world. E.g., session/cookies stateful protocol onto
  stateless HTTP, onto stateful TCP, onto stateless IP.

stateless protocol
------------------

- a communication protocol in which no information is retained by either
  sender or receiver.

- The stateless design simplifies the server design because there is no need to
  dynamically allocate storage to deal with conversations in progress. If a
  client session dies in mid-transaction, no part of the system needs to be
  responsible for cleaning up the present state of the server. A disadvantage
  of statelessness is that it may be necessary to include additional
  information in every request, and this extra information will need to be
  interpreted by the server.

- examples.
 
  * UDP

  * IP

  * HTTP

stateful protocol
-----------------

- a communication protocol that requires keeping of the internal state on the
  server.

- stateful protocol 往往是 connection-oriented 的. 相关连接配置参数在某些 packets
  中传递给对方 (例如 handshake 阶段), 然后就不用反复传递了.

- examples.
 
  * TCP. e.g., congestion window, advertised cwd, SACK enabled or not, acked
    sequence number, etc.

  * FTP. interactive session, during the session, a user is provided a means to
    be authenticated and set various variables (working directory, transfer
    mode), all stored on the server as part of the user's state.
