- actor-based concurrent programming.

- Akka is a scala library that implements an actor model similar to Erlang's.

- Akka's actor model implementation is based on message passing between
  threads. 它相当于利用线程间队列和其他 concurrency primitives 抽象和封装了一个
  功能丰富的、容易使用的、高性能的 actor model. 它的本质仍然是 message passing.
  这与自己手动在线程之间传递消息没有本质区别.
