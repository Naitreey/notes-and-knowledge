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
^^^^^^^^^
- client/server authentication (key exchange).

- provides cryptographically encrypted connection to upper layers.
  于是上层可以直接从 transport layer 接受和发送 clear text data.

- key re-exchange usually after 1 GB of data has been transferred or after 1
  hour has passed, whichever occurs first.

- optional data compression.

SSH-USERAUTH
^^^^^^^^^^^^
- runs on top of transport layer.

- provides several mechanisms to authenticate client user to server.

- mechanisms including but not limited to: password, public-key, PAM,
  GSSAPI, keyboard-interactive.

SSH-CONNECT
^^^^^^^^^^^
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
^^^^^^^^^^^^^^^

- server/client version exchange.

- server provides its host key. client check server's host key to see if server
  is really the intended host.

- negotiate a session key for encryption, via Diffie-Hellman algorithm.

- establish encrypted session.

authentication layer
^^^^^^^^^^^^^^^^^^^^

- user auth

connection layer
^^^^^^^^^^^^^^^^

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

encryption
----------
- SSH uses symmetric encryption to encrypt the entire connection.

- The client and server both contribute toward establishing encryption key.
  Through key exchange algorithm, client and server both arrives at the
  same key independently.

- encryption key is session-based.

- Diffie-Hellman key exchange algorithm.

  * Both parties agree on a large prime number, which will serve as a seed value.
  
  * Both parties agree on an encryption generator (typically AES), which will be
    used to manipulate the values in a predefined way.
  
  * Independently, each party comes up with another prime number which is kept
    secret from the other party. This number is used as the private key for this
    interaction (different than the private SSH key used for authentication).
  
  * The generated private key, the encryption generator, and the shared prime
    number are used to generate a public key that is derived from the private
    key, but which can be shared with the other party.
  
  * Both participants then exchange their generated public keys.
  
  * The receiving entity uses their own private key, the other party's public
    key, and the original shared prime number to compute a shared secret key.
    Although this is independently computed by each party, using opposite private
    and public keys, it will result in the same shared secret key.
  
  * The shared secret is then used to encrypt all communication that follows.

authentication
--------------

public-key (SSH key pairs)
^^^^^^^^^^^^^^^^^^^^^^^^^^
- A SSH key pair consists of a public key and a private key.
  本质上这是一种非对称加密方法. SSH 使用公私钥非对称加密的
  方式作为一种认证方式.

- 注意 key pairs 并没有用于通信加密. 仅用于 client identity challenge.

- authentication mechanism.

  * server keeps a list of authorized clients' public keys
    即 ``~/.ssh/authorized_keys``. 这个列表可以通过多种方式
    添加, 例如直接编辑, 或者客户端通过其他认证方式通过服务端
    的认证, 然后添加自己的公钥 (例如 ``ssh-copy-id``).
    总之, 只要公钥在这个列表里, 就表示相应的客户端已经认证.

  * client 连接时, server 向 client 发送一个 challenge message,
    若 client 能够回复正确的答案, 就证明自己拥有与公钥对应的私钥,
    即证明了自己的身份 (是已经认证了的那个 client).

- procedure.

  * The client begins by sending an ID for the key pair it would like to
    authenticate with to the server. (ID probably contains public key itself,
    ID is not public key's comment part.)

  * Server find authorized public key matching ID from ``authorized_keys``.

  * the server generates a random number and uses the public key to encrypt the
    number.

  * The server sends to the client this encrypted message.

  * Client decrypts message using private key.

  * client combines the decrypted number with session key and calculates the
    MD5 hash of this value.

  * client sends the hash back to server.

  * server does the same calculation, check if client's response matches its
    calculation. If so, client is authenticated.

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
