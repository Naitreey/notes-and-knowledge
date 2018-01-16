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
