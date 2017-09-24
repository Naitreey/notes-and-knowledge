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

- 在 google dns (8.8.8.8) 可以访问的情况下, 没必要进行任何 dns 转发. 无论是
  ss-tunnel 转发 udp dns 请求还是 dns-forwarder 转换 tcp 的请求方式都没有必要.
