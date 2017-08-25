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
