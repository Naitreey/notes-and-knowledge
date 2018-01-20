dnsmasq
=======

- operations: DNS, DHCP, PXE, TFTP, router advertisement

- config file

  * ``/etc/dnsmasq.conf``

  * 配置项的 key/value 与命令行上的 long option 相同.

  * 对于只能指定单次的 option, 配置文件覆盖命令行.

- DNS

  * able to load ``/etc/hosts`` for local DNS lookup

systemd-resolved
================

general
-------
- systemd-resolved.service(8) 是一个本地的 DNS resolver. 它实现了 caching,
  即作为 caching name server; 可以进行 recursive query; 可以进行 reverse DNS
  lookup. 貌似不能做 iterative query.

- systemd-resolved 为本地程序提供 DNS 服务. 该服务启动时, 默认情况下
  接管 ``/etc/resolv.conf``, 设置 nameserver 指向该服务.

配置文件
--------
 
* 全局配置: resolved.conf(5)
  
  - ``/etc/systemd/resolved.conf``. main configuration file.
   
  - ``/etc/systemd/resolved.conf.d/*.conf``. admin customizations.

  - ``/run/systemd/resolved.conf.d/*.conf``. runtime.

  - ``[/usr]/lib/systemd/resolved.conf.d/*.conf``. vendor packages'
    customizations.

  主配置文件优先级最低. 在 conf.d/ 中的文件的 entries override 主配置
  中的内容. 两个 conf.d/ 中的文件放在一起按 ASCII 排序后读. 相同文件名
  时 etc 下的覆盖 lib 下的. 当某个 entry 为单值时, 最后读取的项生效;
  当为多值时, 各处的值合并在一起.

* per-link: 使用 systemd 的 NIC 配置文件. ``/etc/systemd/network/*.network``
  等 systemd.network(5) 规定的配置文件.

默认情况下, ``/etc/resolv.conf`` 由 systemd-resolved 接管. 直接对
该文件进行的修改会被覆盖掉 (systemd-resolved 或 networkd restart 时).
里面只包含 127.0.0.53 即 systemd-resolved.

配置项
~~~~~~
详见 resolved.conf(5)

- DNS

- Domains. 当 resolve single-label host names 时, 使用这些作为默认的 domain
  部分 (即认为属于这些 DNS zone), 从而将 hostname 补全成 FQDN 再去解析.

query 机制
----------

* Lookups for the special hostname "localhost" are never routed to the
  network.

* Single-label names are routed to all local interfaces capable of IP
  multicasting, using the LLMNR protocol.

* Multi-label names are routed to all local interfaces that have a DNS server
  configured, plus the globally configured DNS server if there is one.
  Address lookups from the link-local address range are never routed to DNS.

当 DNS 请求发给多个 interfaces 时, 输出第一个成功的响应作为 query result.

signals
-------

* SIGUSR1 to dump RR caches to system logs.

CLI
---

- systemd-resolve(1)
