overview
========
- OpenSSH is the most used SSH protocol implementation.

- support sshv2, sshv1 support has been removed.

forwarding
==========
X11 connections, arbitrary TCP ports and UNIX-domain sockets can also be
forwarded over the secure channel.

SSH port forwarding 也称为 SSH tunnel.

SSH 的 local/remote port forwarding 机制无需配置网关的端口映射规则, 是一种方便
好用的内网隧穿方法.

See also [SESSHForward]_, [SSHPortForwarding]_.
local port forwarding
---------------------
::

  ssh -L {[local_address:]local_port | local_socket}:{remote_host:remote_port | remote_socket} destination

The connections to the given TCP address and port tuple or local UNIX domain
socket at the client machine, are to be forwarded to the given remote host
and port pair or remote UNIX domain socket.

This works by ssh client allocating a socket to listen to either a TCP
address and port pair on the local side or to a Unix socket. 当有 socket 连
接上了 client host 监听的 TCP address/port 或 UNIX domain socket 时, 该连接
的通信内容经过 client host 和 destination host 之间的 ssh secure connection
至 destination host 上的 sshd, 后者向 remote host 的 address/port 或 UNIX
domain socket 转发这个通信内容. Remote host 与 destination host 可以是不同的
host.

local address 决定本地监听的地址, 允许的地址范围由 ssh_config(5) 中的
GatewayPorts 决定. 默认是 no, 不能指定 local address, 只能监听 loopback
address. 设置 yes 后才能选择监听的地址. 此时, an empty address
``:local_port`` or ``*:local_port`` address 表示监听所有地址.

local address and remote address can be ``localhost``. 在 client 端, 表示
bind to localhost/loop back interface, 这样只有本地应用可连接; 在 remote
端, 表示转发至的 remote host 就是 destination host 它自己.

``-L`` forwarding can be specified multiple times.

usage:

* jump server. 用户在公网上, jump server 作为内网的网关, 用户可 ssh 连接 jump
  server, 建立 local port forwarding, 让 jump server 去连接任意内网资源. 这样,
  用户虽然不可直接访问内网, 通过本地端口映射, 可访问任意内网服务.

remote port forwarding
----------------------
::

  ssh -R {[remote_address:]remote_port | remote_socket}[:{near_address:near_port | near_socket}] destination

The connections to the given TCP address/port pair or UNIX domain socket at
the destination host are to be forwarded to the given local near host's
address/port pair or local UNIX domain socket.

This works by remote sshd server allocating a socket to listen to either a
TCP address/port or a UNIX domain socket on the remote destination host. 当
有 socket 连接上 remote host 监听的 socket 时, 连接内容经过 client host 与
remote host 之间的 ssh 加密连接传到 client host, ssh client 再向 near host
的 address/port 或本地的 UNIX domain socket 转发这个通信内容.

If no explicit destination was specified, ssh client will act as a SOCKS 4/5
proxy and forward connections to the destinations requested by the remote
SOCKS client.

remote address 决定远端监听的地址, 允许的地址范围由 sshd_config(5) 中的
GatewayPorts 决定. 默认是 no, 不能指定 remote address, 只能监听 loopback
address. 设置 yes 后才能选择监听的地址. 此时, an empty address
``:remote_port`` or ``*:remote_port`` address 表示监听所有地址.

If the ``remote_port`` is ‘0’, the listen port will be dynamically allocated
on the server and reported to the client at run time.

``-R`` forwarding can be specified multiple times.

usage:

* 若外网用户想要访问内网服务, 但不能直接 ssh 网关服务器时, 不能使用 local port
  forwarding 来方便地访问任意服务. 此时, 必须通过内网人员的配合, 从某个内网设
  备 ssh 某个可从公网访问的服务器 (例如 AWS), 使用 remote port forwarding, 在
  该服务器上建立所需端口映射. 外网用户只能访问这些固定的内网资源.

X11 forwarding
--------------
On the client side, use ``-X`` when making ssh connection. Or specify
ForwardX11 in client configuration file on a per-host basis. When the
connection has been successfully established, DISPLAY and XAUTHORITY will be
automatically set to their proper values.

On the server side, enable X11Forwarding in sshd configuration file.
Install ``xauth`` on the server host.

Start any GUI program at the server side, the X11 protocol packages will be
automatically tunneled through ssh connection, and received by X server at
client host. The X server at client host then does all the graphics rendering
etc.

Vanilla X11 forwarding 有严重的效率问题, 可使用 x2go 等应用来解决这个问题.

See also [SEForwardXSSH]_.

configurations
--------------
- GatewayPorts (client and server side)

- AllowTcpForwarding (server side)

- AllowStreamLocalForwarding (server side)

- ForwardX11 (client side)

- X11Forwarding (server side)

privilege separation
====================
see: https://upload.wikimedia.org/wikipedia/commons/b/be/OpenSSH-Privilege-Separation.svg

Privilege separation is applied in OpenSSH by using several levels of
access, some higher some lower, to run sshd(8) and its subsystems and
components.

- a privileged process (root) that listens new connections.
  
- Unpon client connection, a privileged monitor process (root) forked to
  monitor the overall activity with the individual client.

- During initial authentication and network processing stages with the
  client, an unprivileged process (sshd) is forked to handle the contact
  with the remote client.

- After authentication is completed and a session established for user,
  unprivileged sshd process exits. a new user-privileged sshd process
  (username) is forked to handle user traffic, which then forks user's
  default shell, etc.

references
==========
.. [SESSHForward] `What's ssh port forwarding and what's the difference between ssh local and remote port forwarding <https://unix.stackexchange.com/questions/115897/whats-ssh-port-forwarding-and-whats-the-difference-between-ssh-local-and-remot>`_
.. [SSHPortForwarding] `ssh port forwarding example <https://www.ssh.com/ssh/tunneling/example>`_
.. [SEForwardXSSH] `How to forward X over SSH to run graphics applications remotely? <https://unix.stackexchange.com/questions/12755/how-to-forward-x-over-ssh-to-run-graphics-applications-remotely>`_
