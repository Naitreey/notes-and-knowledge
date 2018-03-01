General
=======
- tcp 和 udp 都通过 internet checksum 来保证数据的完整性.
- 在传输层, 1 -- 1023 端口是 "trusted ports". 在 unix 中, 只有 root 可以 bind(2)
  这些端口. 这么设计的目的是, 常见的协议都在这个端口范围内, root priviledge 的要求
  保证了 bind 这些端口的进程确实是该服务器中可信的进程 (前提是没被 hack). 这些
  进程在 bind 时 ``euid == 0``, 所以是系统进程或管理员启动的进程.
