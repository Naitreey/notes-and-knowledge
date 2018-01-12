systemd-based system
====================

- network configuration is managed by systemd-networkd.

- config directories.

  * ``/lib/systemd/network``. upstream.

  * ``/run/systemd/network``. runtime volatile.

  * ``/etc/systemd/network``. global configuration.

- All configuration files are collectively sorted and processed in lexical
  order, regardless of the directories in which they live.

  files with identical filenames replace each other. Files in /etc have the
  highest priority, files in /run take precedence over files with the same name
  in /lib.

  The first (in lexical order) of files that matches a given device is applied,
  all later files are ignored, even if they match as well. A file is said to
  match a device if each of the entries in the "[Match]" section matches, or if
  the section is empty.

- 修改配置之后, 需要重启 systemd-networkd.service.

  WTF: 有时候这样是不够的, 需要删除 ``/run/systemd/{network/*, resolve/*}``.
  我日什么鸡巴玩意儿.

network configuration
---------------------

- network configuration file must have the extension ``.network``.

- 有许多配置都可以通过命令行上的相应命令进行 runtime 设置.
  很显然, 这里提供这些配置是提供了一种统一的方便的静态配置方法.
  将各个命令的繁杂临时设置规范化成为配置状态.

Match section
~~~~~~~~~~~~~
``Match`` section matches network device to be applied.
详见 systemd.network(5)

常见: MACAddress, Name, udev attributes.

Link section
~~~~~~~~~~~~
设置链路属性.
详见 systemd.network(5)

Network section
~~~~~~~~~~~~~~~
设置网络属性.
常见: Description, DHCP, Address, Gateway, DNS.

Address section
~~~~~~~~~~~~~~~
可以设置多个 address section. 每个进行的配置类似于 ``ip address`` command.

Route section
~~~~~~~~~~~~~
设置路由规则, 可以设置多个 section. 相当于 ``ip route`` command.

DHCP section
~~~~~~~~~~~~
常见: UseDNS
