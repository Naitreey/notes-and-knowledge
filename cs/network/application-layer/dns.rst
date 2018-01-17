general
=======

- hierarchical decentralized naming system for TCP/IP network.

- 本质上是一个 directory service, 也是一个 distributed database system.

concept
=======

name server
-----------
A DNS name server is a server that stores the DNS records for a
domain; a DNS name server responds with answers to queries against its
database.

authoritative name servers for each domain, is responsible for
assigning domain names and mapping those names to Internet resources.

zone
----
每个 domain 是一个 zone, name server 在 domain 内部对 sub-domains 具有
自治权, 可将 DNS 解析自由分配给更低层的 name servers.

zone file
---------
一个 name server 用于存储各种 DNS 相关记录的 text file (可理解为 DNS
数据库). zone file 中包含一系列 resource records (RR). 每个 RR 一行, 各列即
name, ttl, record class, record type, record data.

在一些 DNS implementation 中, zone file 只是实际的 DNS 数据库的 textual
representation.

The name field may be left blank. If so, the record inherits the field from the
previous record.

Resource records may occur in any order in a zone file, with some exceptions.
For formatting convenience, resource records may span several lines by
enclosing in parentheses a set of parameters that spans several lines, but
belongs to the same record.

The file may contain line comment preceded by ``;``.

The zone file may also contain directives that are marked with a keyword
starting with the dollar sign character.

As a minimum, the zone file must specify the Start of Authority (SOA) record
with the name of the authoritative master name server for the zone and the
email address of someone responsible for management of the name server.
The parameters of the SOA record also specify a list of timing and expiration
parameters.

In the zone file, host names that do not end in a period are relative to the
origin. Names ending with a full stop (or point) are said to be fully qualified
domain names.

The zone files for the DNS root zone and for the set of top-level domains
contain resource records only for the authoritative domain name servers for
each domain name.

``dig``, ``drill`` 等命令给出的结果就是按照 zone file 的格式.
record
------
zone file 中的一条记录.

类型包括:
Start of Authority (SOA), IP addresses (A, AAAA), SMTP mail exchangers (MX),
name servers (NS), pointers for reverse DNS lookups (PTR), domain name
aliases (CNAME), responsible person (RP), DNSSEC records.

IP & domain name relation
-------------------------

- 在 TCP/IP network 中, DNS protocol 负责 domain name hierarchy namespace;
  IP protocol 负责 address namespace.

- 一个 domain name 可能对应多个 IP 甚至 IPv4 和 v6. DNS 的一个好处是可以根据
  与客户端最合适的 IP 协议、最近的距离给出最恰当的 IP 地址结果, 以及负载均衡.

- 一个 IP 也可以反向对应多个 domain name, 例如 virtual hosting.

transport
=========
TCP/UDP on port 53. normally UDP.

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

operations
==========

addresss resolution mechanism
-----------------------------

standard address resolution procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 从最右边 null label 开始. 访问 root name servers, 询问要找的 FQDN 的 IP 是什么.
  root name server 会根据 FQDN 的 TLD label, 找到自己存储的该 TLD 对应的 NS record,
  告诉你去相应的 name server 询问.

  * host must initially caches a list of ip addresses of known root name servers.
    不然的话无从开始. 这个缓存应定期更新.

  * Name servers in delegations are identified by name, rather than by IP
    address. This means that a resolving name server must issue another DNS
    request to find out the IP address of the server to which it has been
    referred.

- 类似地, TLD domain 的 name server 会根据它存的 domain NS record 告诉你去问具体
  domain 自己的 name server. 直到某个 name server 给出了 authoritative answer.

若每个主机都按照这种标准方式查询 DNS:

1. 越顶层的 name server 会越忙网络负担越重;

2. internet 上的 DNS 流量将非常大;

3. DNS 解析会很慢;
  
4. 每个类型的主机都需实现一套查询算法.
   
所以需要能够代替 host 进行查询和缓存查询结果的服务.

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
它返回给主机所需的解析结果, 如果需要, 代替主机进行查询.

Caching name server 首先是 name server, 然后是具有 cache & recursive query
附加功能的 name server. 也就是说, 它可能对于部分 domain 而言是 authoritative
name server. 例如, 对于对局域网路由器, 它对网内的 hostname 具有解析权威.

这就是我们平时在网络配置中写入的 DNS server. 需要明确, 我们写入的实际上都是
caching name server, 我们理应能够从它 (或者它们中的某一个, 如果配置了多个 DNS)
那里获取到需要查询的所有域名结果. 它才是真正去参与标准 DNS 查询流程的终端.

平时在局域网中, 常用的子网路由器 (3 层交换机) 就是这样的 caching name server;
ISP 提供的 DNS 配置, 也指向一个或多个 caching name server;
平时配置的 google DNS 等也是 caching name server;
若主机上有本地的 name server daemon, 也是 caching name server, 例如 dnsmasq,
systemd-resolved.

DNS resolver
------------
DNS resolver is responsible for initiating and sequencing the queries that
ultimately lead to a full resolution (translation) of the resource sought.

The DNS resolver will almost invariably have a cache (see above) containing
recent lookups.

DNS resolver 可以是客户端主机, 可以是局域网路由器, 可以是 ISP DNS server 等等.

resolution methods
------------------

- recursive query. the DNS client requires that the DNS server respond to the
  client with either the requested resource record or an error message stating
  that the record or domain name does not exist. The DNS server cannot just
  refer the DNS client to a different DNS server. If a DNS server does not have
  the requested information when it receives a recursive query, it queries
  other servers until it gets the information (by recursive or iterative method),
  or until the name query fails.

  一般 DNS client 向配置的 DNS server 发送的查询是 recursive query.

- iterative query. a DNS client allows the DNS server to return the best answer
  it can give based on its cache or zone data. If the queried DNS server does
  not have an exact match for the queried name, the best possible information
  it can return is a referral (that is, a pointer to a DNS server authoritative
  for a lower level of the domain namespace). The DNS client can then query the
  DNS server for which it obtained a referral. It continues this process until
  it locates a DNS server that is authoritative for the queried name, or until
  an error or time-out condition is met.

  caching name server 一般需要进行 iterative query 向客户端给出最终结果.

circular dependency
-------------------
若某个 domain `example.com` 的解析被 refered to authoritative name server
`ns1.example.com`, 则显然出现 circular dependency. 此时, 上层 name server
需要同时提供 referred-to name server 的 IP address. 这些信息叫做 glue.

The delegating name server provides this glue in the form of records in the
additional section of the DNS response, and provides the delegation in the
authority section of the response. A glue record is a combination of the name
server and IP address.


record caching
--------------
A standard practice in implementing name resolution in applications is to
reduce the load on the Domain Name System servers by caching results locally,
or in intermediate resolver hosts. Results obtained from a DNS request are
always associated with the time to live (TTL), an expiration time after which
the results must be discarded or refreshed.

Negative response caching. 如果查询的 RR 不存在, 这个结果也需要缓存起来.
为了让此时作为客户端的 caching name server 知道这个结果需要缓存多久, negative
DNS caching 要求此时返回的是该 name server 的 SOA record. 这里面有 TTL 信息.

reverse lookup
--------------
A reverse lookup is a query of the DNS for domain names when the IP address is
known. Multiple domain names may be associated with an IP address.

为支持反向查询时, IP 以 domain name 的形式存储在 pointer record 中 (PTR).
The IP address is represented as a name in reverse-ordered octet representation
for IPv4, and reverse-ordered nibble representation for IPv6.

例如, 8.8.4.4 -> 4.4.8.8.in-addr.arpa.
2001:db8::567:89ab -> b.a.9.8.7.6.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.

需要把 ip 反过来写是因为, 在 domain name 中, 从右至左是 zone 范围右大至小的过程.
这样每个反向的 ip 段都是嵌套的 domain, 完全符合正常的 DNS iterative query method
流程. 可以像正常的 domain 一样, 把 ip 的 PTR record 也分配给不同层的 name server,
然后 iterative query.

`arpa` TLD 的存在仅用于 reverse DNS lookup. 准确地讲, 该 TLD 下包含
``in-addr.arpa`` 和 ``ip6.arpa`` 两个 domain 用于 reverse DNS lookup.
(历史原因. arpa 即 ARPAnet 主机在 DNS 系统中的初始 TLD.)

进行反向查询时, client 将 IP 转换成上述的 domain name 形式, 然后按照与正常
DNS 相同的流程进行查询.

例如, 208.80.152.2 的 reverse lookup domain 形式是 2.152.80.208.in-addr.arpa.
When the DNS resolver gets a pointer (PTR) request, it begins by querying the
root servers, which point to the servers of American Registry for Internet
Numbers (ARIN) for the 208.in-addr.arpa zone. ARIN's servers delegate
152.80.208.in-addr.arpa to Wikimedia to which the resolver sends another query
for 2.152.80.208.in-addr.arpa, which results in an authoritative response.

client
------
当 IPv4, v6 同时支持时, client 一般会先后发出分别对应于 ipv4, v6 的两个 query 请求,
一个查询的 header 中 type = A, 另一个 header 中 type = AAAA.

message format
==============

- two type of messages: queries and responses. They both have same format.

- Each message consists of a header and four sections: question, answer,
  authority, and an additional space.

- The header section contains the following fields:
  
  * Identification. can be used to match responses with queries.
    
  * Flags.

  * Number of questions.
    
  * Number of answers.
    
  * Number of authority resource records (RRs).
   
  * Number of additional RRs.

- The question section contains the domain name and type of record (A, AAAA,
  MX, TXT, etc.) being resolved.

- The answer section has the resource records of the queried name. A domain
  name may occur in multiple records if it has multiple IP addresses
  associated. 每次返回的多个 IP 顺序可能不同, 用于负载均衡.

- The authority RR section 根据具体情况可能提供 authoritative name server 的
  SOA record, 或者 delegation 时的下一层 name server NS record.

- The additional RR section 在 delegation 时可能包含各个 name servers 的 IP
  (若出现 circular dependency 时).
resource records (RR)
=====================

- Each record has a type (name and number), an expiration time (time to live),
  a class, and type-specific data.

- Resource records of the same type are described as a resource record set
  (RRset).

- fields in a RR:

  * NAME. FQDN of the node in the DNS namespace tree.

  * TYPE. the record type. It indicates the format of the data and it gives a
    hint of its intended use.

  * CLASS. 不同的网络类型. Each class is an independent name space with
    potentially different delegations of DNS zones. It is set to IN (for
    Internet) for common DNS records involving Internet hostnames, servers, or
    IP addresses.

  * TTL. Count of seconds that the RR stays valid.

  * RDLENGTH.

  * RDATA. data of the specific record. such as the IP address for address
    records, or the priority and hostname for MX records.

- RR types (part of).

  * A. IPv4 address record.

  * AAAA. IPv6 address record. (32*4=128, hence 4 "A"s)

  * CNAME. canonical name record. Alias of one name to another: the DNS lookup
    will continue by retrying the lookup with the new name.

  * MX. Mail exchange record. Maps a domain name to a list of message transfer
    agents for that domain.

  * NS. Name server record. Delegates a DNS zone to use the given authoritative
    name servers.

  * PTR. Pointer record. Pointer to a canonical name.

  * RP. Responsible persion. Information about the responsible person(s) for
    the domain.

  * SOA. Start of [a zone of] authority record. Specifies authoritative
    information about a DNS zone, including the primary name server, the email
    of the domain administrator, the domain serial number, and several timers
    relating to refreshing the zone.

  * TXT. Text record. arbitrary text in a DNS record.

domain name
===========

registration
------------
