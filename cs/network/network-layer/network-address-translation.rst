overview
========
- NAT 是一种允许一组 IP address 集合能够自由分配给一个子网的机制. 所谓自由, 即
  IP 地址分配无需向某种权威机构 (例如 IANA) 申报和注册, 可由管理员自行决定. 不
  同 NAT 设备背后的子网 IP 地址可以重复.

- NAT 的设计初衷是为了缓解 IPv4 地址空间穷尽的问题, 在长期方案 (即 IPv6) 设计完
  善之前提供一个临时的解决方案. 这样, 一组需要联网的设备可以共享同一个在全球 IP
  网中唯一的地址 (或者共享一个其他网络内的地址, 例如对于内网中再创建的 NAT 子网,
  总之本质在于无需向权威机构注册和申报).

- Most routers support NAT, 往往是作为网关使用时.

- NAT is defined by IETF Behavior Engineering for Hindrance Avoidance (BEHAVE)
  working group.

terms
=====
- NAT session. an internal state data kept by NAT device. 一个 NAT session
  包含对特定的数据包进行 NAT 所需的全部信息, 例如 NAT mapping.

- NAT mapping. host IP/port 与 NAT device IP/port 之间的映射关系.

mechanism
=========

overview
--------
当内部主机第一次向外发送数据时, NAT device 转发数据至外网, 并在内存中建立并维持
一个 NAT session. 当 NAT device 收到外网来的数据包时, 根据目的端口, 检索 NAT
mapping, 将数据转发给应去的内部主机.

packet rewriting
----------------
- A NAT works by rewriting the identifying information in packets transiting
  through a router.

  * 从内至外时, 修改数据包中的 source IP/port. 从而看上去数据包是从 NAT device
    自身发出的.

  * 从外至内时, 修改数据包中的 destination IP/port. 从而到达 NAT device 的数据
    包能转发至目的主机.

- 修改 IP packet 的地址, 需求修改相应 TCP/UDP packet 中的 checksum. 对于一些
  应用层协议, 还需修改应用层的数据包内容, 例如 FTP.

NAT 内部的地址段
----------------
  
* 原则上, private network 可以使用任何 IP 地址段. 但是若使用了 globally
  routable address, 则会导致本地主机 "shadow" 了同样使用这些 IP 的公网主机
  (close proximity).

* 因此, 实际上往往使用 RFC1918 addresses for private networks.

work with TCP
-------------
- NAT session is established when internal host trying to initiate a TCP
  connection by a SYN.

- NAT session is destroyed when:

  * FINs are exchanged (four-way teardown).

  * RST is sent/received.

  * various timer timeout.

- Connection timeout mechanism.

  * when an outgoing SYN segment is observed, a connection timer is activated,
    and if no ACK is seen before the timer expires, the session state is
    cleared.

  * If an ACK does arrive, the timer is canceled and a session timer is
    created. If connection idles too long after established, session timer
    will timeout. And starts close timer.

  * During connection close phase (partially opened/closed connection), close
    timer is created. And session is cleared when it timeouts.

work with UDP
-------------
- 由于 UDP is connectionless, 只有 source IP/port and dest IP/port 可作为 NAT
  session 依据. UDP NATs use a mapping timer to clear NAT state if a mapping
  has not been used in a certain amount of time.

work with ICMP
--------------
- ICMP fix-up: when an ICMP message passes through a NAT, the IP addresses in
  the included message need to be rewritten by the NAT in order for them to
  make sense to the end client.

- For ICMP error message.

  * ICMP fix-up.

- For ICMP informational message.

  * ICMP fix-up.

  * Query ID field is used like TCP/UDP port number. A timer is set for
    address-query-ID pair, for returning response.

NAT mapping and filtering behaviors
===================================

- A NAT device can have different behaviors for different transport protocols.

TCP/UDP
-------
the following 3 levels of behaviors are defined:

- Endpoint-independent.
  
  * translation behavior: The NAT reuses the port binding for subsequent
    sessions initiated from the same internal IP address and port to any
    external IP address and port.

  * filtering behavior: The NAT does not filter and discard packets that are
    addressed to the external part of the binding, irrespective of the source
    values in the packet.

  这种工作方式也称为 full-cone NAT.

- Address-dependent.
  
  * translation behavior: The NAT reuses the port binding for subsequent
    sessions initiated from the same internal IP address and port only for
    sessions to the same external IP address.

  * filtering behavior: The NAT filters and discards packets that are addressed
    to the external part of the binding, unless the source address of the
    packet matches the destination address used in the binding.

  这种工作方式也称为 restricted-cone NAT.

- Address- and port-dependent.

  * translation behavior: The NAT reuses the port binding for subsequent
    sessions initiated from the same internal IP address and port only for
    sessions to the same external IP address and port.

  * filtering behavior: The NAT filters and discards packets that are addressed
    to the external part of the binding, unless the source address and port
    number of the packet matches the destination address used in the binding. 
  
  对于 TCP, 这是最常见的工作方式. 因为这具有最好的安全性. 对于一个 TCP
  connection 也完全足够.

  这种工作方式也称为 symmetric NAT.

categories
==========

basic NAT
---------
- Private address 与 public address 之间做映射.

- A private address is rewritten to be a public address, often from a pool or
  range of public addresses supplied by an ISP. The number of globally routable
  addresses must equal or exceed the number of internal hosts that wish to
  access the Internet simultaneously.

- 不做端口映射.

- basic NAT 没啥用, 它要求内网中必须只有少量的机器连接外网, 不能很好地解决地址
  不够的问题.

NAPT
----
- NAPT: Network Address Port Translation. a.k.a, IP masquerading. 一般说的 NAT
  指的是 NAPT.

- NAPT 在 basic NAT 的基础上提供 port translation 的功能. 这样, 可以用很少的
  global address (可能 1 个) 支持非常多的内网机器同时连接外网.

- NAPT 提供一定的 security features.

  * All systems on the private side of the NAT cannot be reached directly from
    the Internet.
 
  * It hides the number and configuration of internal addresses from the
    outside.

Port forwarding
===============
- 端口映射的目的在于让内网的设备能够对外提供服务.

- Port forwarding requires static configuration of the NAT with:
 
  * the address of the server
    
  * the associated port number

  * the associated protocol

  这就是创建了一个静态的 NAT mapping.

- 端口映射与一般 NAT 的区别是:

  * NAT mapping 的配置是固定的, 静态的, 预先配置的.

  * 能让外部设备向内部主机发起连接.

advantages
==========

- reduce the need for globally routable IP addresses

- convenient tool to create autonomous local network, without need for
  registration to an outer address authority.

- some degree of natural firewall capabilities.

- requires little configuration.

disadvantages
=============

- Require special configuration for a service behind NAT to be accessible from
  global Internet.

- For a NAT association to work, every packet in both directions of a
  association must pass through the same NAT.

- NAT 违反 Internet protocol 的一个基本设计原则: smart edge and dumb middle.
  若要 NAT 正常工作, NAT 设备必须理解和适当修改经过的数据包的多层协议内容. 这
  往往包含网络层、传输层甚至应用层的数据包内容.

Regarding IPv6
==============
- IPv6 should makes NAT unnecessary. IPv6 时, 可以给一个 subnet 分配足够多的地
  址, 这样无论子网内如何划分以及如何创建新的子网, 都可以从地址段中拿到一个唯一
  的地址. 无论这样的地址是 DHCPv6 分配的还是手动分配的.
