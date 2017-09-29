- 使用的工具:

  * LEDE (OpenWRT)

  * dnsmasq-full

  * libmbedtls

  * libsodium

  * libudns

  * luci-app-shadowsocks

  * shadowsocks-libev

  * gfwlist

  * iptables

  * ipset

- 实现

  * ss-local 做普通代理, ss-redir 做转发.

  * ss-redir 数目与 CPU 数目相同, 充分利用性能.

- 目前 dns 污染以及 dns 劫持导致 udp 查询 8.8.8.8 得到的结果不可靠.
  需要将 dnsmasq 的 udp dns 请求经过 dns-forwarder 转换 tcp.
  但是 gfw 貌似已经能拦截 tcp 的 dns 请求了, 所以还需要再把 tcp dns
  经过 ss 服务器转发. (ss 可能不能直接转发 udp 的 dns 请求, 因为
  一些 ss 提供商不允许 udp 转发.) 为能够将向 8.8.8.8 的 tcp dns 请求
  经过 ss-redir, 须首先在 ipset 中添加 8.8.8.8 ip.
