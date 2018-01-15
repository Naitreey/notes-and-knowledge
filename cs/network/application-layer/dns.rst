general
=======

- hierarchical decentralized naming system for TCP/IP network.

- 本质上是一个 directory service, 也是一个 distributed database system.

concept
=======
- 在 TCP/IP network 中, DNS protocol 负责 domain name hierarchy namespace;
  IP protocol 负责 address namespace.

- name server: A DNS name server is a server that stores the DNS records for a
  domain; a DNS name server responds with answers to queries against its
  database.

- authoritative name servers for each domain, is responsible for
  assigning domain names and mapping those names to Internet resources.

- 每个 domain 是一个 zone, 在 domain 内部对 sub-domains 具有自治权, 可将 DNS 解析
  自由分配给更低层的 name servers.

- zone file. 一个 name server 用于存储各种 DNS 相关记录的数据库.

- record. zone file 中的一条记录.
  包括: Start of Authority (SOA), IP addresses (A, AAAA), SMTP mail exchangers (MX),
  name servers (NS), pointers for reverse DNS lookups (PTR), domain name
  aliases (CNAME), responsible person (RP), DNSSEC records.

- 一个 domain name 可能对应多个 IP 甚至 IPv4 和 v6. DNS 的一个好处是可以根据
  与客户端最合适的 IP 协议、最近的距离给出最恰当的 IP 地址结果.

structure
=========

domain namespace
----------------
a tree structure.

- The tree sub-divides into zones beginning at the root zone.

- Administrative responsibility over any zone may be divided by creating
  additional zones. Authority over the new zone is said to be delegated to a
  designated name server. The parent zone ceases to be authoritative for the
  new zone.

- A DNS zone may consist of only one domain, or may consist of many domains and
  sub-domains.

- Each node or leaf in the tree has a label and zero or more resource records (RR).

- The domain name itself consists of the label, possibly concatenated with the
  label of its parent node on the right, separated by a dot.

- RRs hold information associated with the domain name.

domain name syntax
------------------
- A domain name consists of one or more labels, that are conventionally
  concatenated, and delimited by dots.

- The right-most label conveys the top-level domain (TLD).

- The hierarchy of domains descends from right to left; each label to the left
  specifies a subdomain of the domain to the right.

  Subdomains may have up to 127 levels.

- A label may contain 0-63 characters. The null label, of length zero, is
  reserved for the root zone. A label consists of ``[A-Za-z0-9-]``, LDH rule
  (letters, digits, hyphen). Labels may not start or end with a hyphen.
  
- The full domain name may not exceed the length of 253 characters in its
  textual representation. In the internal binary representation of the DNS the
  maximum length requires 255 octets of storage, as it also stores the length
  of the name.
  
- Domain names are interpreted in case-independent manner.

name servers
------------

- Name servers are nodes of the distributed database system (i.e., DNS system).

- Each domain has at least one authoritative DNS server that publishes
  information about that domain and the name servers of any of its sub-domains.

- The top of the hierarchy is served by the root name servers (for root zone),
  the servers to query when looking up (resolving) a TLD.

- authoritative name server is a name server that only gives answers to DNS
  queries from data that has been configured by an original source, in contrast
  to a name server that gives answers from its DNS cache.

- An authoritative name server can either be a master server or a slave server.
  A master server is a server that stores the original (master) copies of all
  zone records. A slave server uses a special automatic updating mechanism in
  the DNS protocol in communication with its master to maintain an identical
  copy of the master records.

- Every DNS zone must be assigned a set of authoritative name servers. This set
  of servers is stored in the parent domain zone with name server (NS) records.

- An authoritative server indicates its status of supplying definitive answers,
  deemed authoritative, by setting a protocol flag, called the "Authoritative
  Answer" (AA) bit in its responses.

addresss resolution mechanism
-----------------------------

standard recursive address resolution procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 从最右边 null label 开始. 访问 root name servers, 询问要找的 FQDN 的 IP 是什么.
  root name server 会根据 FQDN 的 TLD label, 找到自己存储的该 TLD 对应的 NS record,
  告诉你去相应的 name server 询问.

  * host must initially caches a list of ip addresses of known root name servers.
    不然的话无从开始. 这个缓存应定期更新.

- 类似地, TLD domain 的 name server 会根据它存的 domain NS record 告诉你去问具体
  domain 自己的 name server. 直到某个 name server 给出了 authoritative answer.

若每个主机都按照这种标准的递归方式查询 DNS:

1. 越顶层的 name server 会越忙网络负担越重;

2. internet 上的 DNS 流量将非常大;

3. DNS 解析会很慢;
  
4. 每个类型的主机都需实现一套递归查询算法.
   
所以需要能够代替 host 进行递归查询和缓存查询结果的服务.

recursive and caching name server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
the Domain Name System supports DNS cache servers which store DNS query results
for a period of time determined in the configuration (time-to-live) of the
domain name record in question. Typically, such caching DNS servers also
implement the recursive algorithm necessary to resolve a given name starting
with the DNS root through to the authoritative name servers of the queried
domain. With this function implemented in the name server, user applications
gain efficiency in design and operation.

Caching name server 的存在, 允许一个网络区域内的主机只访问该 name server 即可.
它返回给主机所需的解析结果, 如果需要, 代替主机进行递归查询.

这就是我们平时在网络配置中写入的 DNS server. 需要明确, 我们写入的实际上都是
caching name server, 我们理应能够从它 (或者它们中的某一个, 如果配置了多个 DNS)
那里获取到需要查询的所有域名结果. 它才是真正去参与标准 DNS 递归查询的终端.

平时在局域网中, 常用的子网路由器 (3 层交换机) 就是这样的 caching name server;
ISP 提供的 DNS 配置, 也指向一个或多个 caching name server;
平时配置的 google DNS 等也是 caching name server.
