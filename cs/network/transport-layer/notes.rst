General
=======
- tcp 和 udp 都通过 internet checksum 来保证数据的完整性.
- 在传输层, 1 -- 1023 端口是 "trusted ports". 在 unix 中, 只有 root 可以 bind(2)
  这些端口. 这么设计的目的是, 常见的协议都在这个端口范围内, root priviledge 的要求
  保证了 bind 这些端口的进程确实是该服务器中可信的进程 (前提是没被 hack). 这些
  进程在 bind 时 ``euid == 0``, 所以是系统进程或管理员启动的进程.


Transmission Control Protocol (TCP)
===================================
- TCP 的机制在 99.9%+ 的概率上保证了数据的完整和正确, 因此其上的应用层协议不需要
  实现 checksum 来再次验证数据完整性.
  Internet checksum 实际上不是完全可靠, 确实在极其罕见的情况下会让错误漏过, 但
  绝大部分情况下都不需要担心, 只有对数据完整性要求很高的时候, 才需要在应用中 (注意
  仍不是在应用层协议设计中) 检验 hash/checksum.

User Datagram Protocol (UDP)
============================
