Web
===

- 在中国, 不使用 https 而使用 plain text http 绝对是作死. 因为 http 劫持
  非常常见, 导致客户端中弹广告等现象. 更不用说由此带来的安全性问题, 例如:

  * MITM attack: 任何人可以截取 http 通信中的敏感信息, 例如帐号密码信息.
    任何中间设备 (如果有人黑了不靠谱的大陆运营商) 可能在 payload 中插入
    修改或插入链接, 指向恶意地址. 若使用 SSL, 这些都无法做到.

  * DNS poisoning: 将 server FQDN 转移到攻击者的地址后, http payload 直接被
    收到. 若使用 SSL, 即使通信被转移至攻击者那里, 由于首先要建立加密信道,
    攻击者必须预先拿到原始网站的 SSL 证书, 从而无法实现或者不再有意义.

- SOP 限制了默认情况下 AJAX 不能 make cross-origin request. 但是这不影响
  ``window.location`` 向其他 origin 的修改, 静态文件 url 的不同来源, POST form
  ``action`` 的不同来源之类的 cross-origin 操作.

  只要攻击者的服务端实现了 CORS 机制, cross-orgin request 照样会成功, 所以
  SOP 不能防止 XSS 攻击.

密码传输和存储
--------------

- 标准的密码传输方式是传输明文密码, 使用 TLS 进行传输加密.

  理由:
  As long as you verify a valid SSL connection to the correct server,
  then the password is protected on the wire and can only be read by
  the server. You don't gain anything by disguising the password before
  sending it.

  The only way that the information could get lost anyway is if the SSL
  connection was compromised and if the SSL connection was somehow compromised,
  the "disguised" token would still be all that is needed to access the account,
  so it does no good to protect the password further.

- password should be hashed and stored as hashes on server side.

  理由: 如果在 client 进行 hash, 那相当于 server 本质上认证的密码是这些 hash 值,
  也就是说实际上现在 hash 值成了明文密码. 服务端的数据库中存储的虽然是 hash 值但
  现在实际上是明文密码. 一旦被拖库, 相当于明文密码泄露, 这些可以直接用于认证.

  所以应该在服务端做 hash 存 hash, 这样就不怕拖库.
