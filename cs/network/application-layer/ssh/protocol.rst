overview
========
- SSH -- Secure Shell protocol

- 当前版本 SSHv2. The current protocol is described in RFC 4250 through RFC
  4256 and standardized by the IETF secsh working group.

- 主要用于 secure remote login 以及 file transfer.  替代 unsecured remote
  access 例如 telnet, rlogin, rsh, rexec 等, 以及通过 SFTP 替代 FTP.

architecture
============
- client-server model.

- use TCP.

- normally one ssh session per tcp connection, multiple ssh sessions
  can be multiplexed over a single tcp connection.

layers
------
- three layers, 从底层至上层: the transport layer, the authentication layer,
  and the connection layer.

SSH-TRANS
~~~~~~~~~
- client/server authentication (key exchange).

- provides cryptographically encrypted connection to upper layers.
  于是上层可以直接从 transport layer 接受和发送 clear text data.

- key re-exchange usually after 1 GB of data has been transferred or after 1
  hour has passed, whichever occurs first.

- optional data compression.

SSH-USERAUTH
~~~~~~~~~~~~
- runs on top of transport layer.

- provides several mechanisms to authenticate client user to server.

- mechanisms including but not limited to: password, public-key, PAM,
  GSSAPI, keyboard-interactive.

SSH-CONNECT
~~~~~~~~~~~
- runs on top of authentication layer.

- defines the concept of channels, channel requests and global requests.

- multiplex multiple concurrent channels into one logical channel.

- provides flow control for channels.

- manages the SSH session, session multiplexing, X11 forwarding, TCP
  forwarding, shell, remote program execution, invoking SFTP subsystem.

workflow
--------
see: https://upload.wikimedia.org/wikipedia/commons/f/fc/SSH-sequence-password.svg

transport layer

- server/client version exchange

- client/server key exchange

- Diffie-Hellman Key Exchange

authentication layer

- user auth

connection layer

- channel open

- exec shell, and send/receive application data through channels.

channel
-------
- 执行每个命令时, 创建一个 channel. channel 的两边分别连着执行的程序和
  client 控制端.
  
  * 在 server side, 执行的程序的 stdin/stdout/stderr streams 全都连着这一个
    channel. 通过是对这个 channel fd 的 read 或 write 操作来区别数据来自
    哪个 stream. 对于 stdout/stderr 都是对 channel 进行写, SSH 能够通过
    其他方式区分两种写的数据.

  * 在 client side, 对 channel 的 write, 即传输至 server side 程序的 stdin,
    read 时, 通过不同的请求, 分别对程序的 stdout/stderr 读取.

SFTP
====

- SFTP: SSH File Transfer protocol.

sftp vs ftp
-----------

- ftp 的适用场景: for publicly available, read-only, file downloads etc,
  otherwise forget about FTP. 因为 ftp protocol 本身不安全. 即使是 readonly
  file downloads, 使用 https + nginx 静态文件加载的方式更好.

- While old FTP succeeded very well in achieving its main goal to promote use
  of networked computers by allowing users at any host on the network to use
  the file system of any cooperating host, it cannot be made secure. There's
  nothing to be done about that, so it is past time to get over it.

- FTP + SSL/TLS == FTPS, which is the wrong way to go. tunneling FTP over
  SSL/TLS is complex to do and far from an optimum solution.
