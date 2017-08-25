- 文本类在传输时需要压缩, jpeg, png 等图片本身就是压缩过的, 进一步压缩可能并不会减小
  体积, 甚至可能增大体积, 而浪费了计算资源.

- 压缩算法的选择. 对于 gzip 和 deflate 应该选择 gzip.

  gzip 和 deflate 都使用的 zlib format, Lempel-Ziv coding (LZ77) 算法. 引用:

    we have 2 compression mechanisms that use the same algorithm for compression,
    but a different algorithm for headers and checksum.

  对于 checksum, 前者用 CRC-32, 后者用 ADLER32. CRC-32 is slower than ADLER32.
  (只慢一点.)

  但是:

    Turns out many browsers over the years implemented an incorrect deflate algorithm.

  所以应该使用 gzip.

  ref: http://stackoverflow.com/questions/388595/why-use-deflate-instead-of-gzip-for-text-files-served-by-apache

- modern browser will cache http basic authentication credientials. 对于一组
  ``(realm, uri)``, 首次遇到 401 + `WWW-Authenticate` 的 response 时, 提示用户
  输入 username + password. 然后浏览器会对应这组 ``(realm, uri)`` 做缓存. 下次
  再遇到这种情况就自动在 headers 添上
  ``Authorization: Basic <base64-encoded-username:password>`` 完成认证.

- 有 body 时, `Content-Length` 或 `Transfer-Encoding: chunked` 必须二者中选择一个设置.
  否则接受方不能保证接受到了完整的 body.
  到底选择哪个不取决于 body 的大小, 而取决于 body 的长度能否预先知道.
  也就是说, 取决于 body 的生成方式是否是随着传输而流式生成的.

  `Transfer-Encoding: chunked` 适用于在传输 body 时并不能预先知道 body 的长度,
  从而不能设置 `Content-Length`, 需要 end of transfer indicator. 典型的情况是
  body 是在内存中流式生成并传输的, 而不是单纯的静态文件或已经生成好的固定大小
  的数据体. 例如, 传输一个文本文件, 为了减小体积需要 gzip 压缩, 这样 body 就是
  流式生成并传输的, 这时会发现 response headers 包含::

    Content-Type: text/...
    Content-Encoding: gzip
    Transfer-Encoding: chunked

- 上传和下载文件的一些问题.

  * 文件大小不是问题. 无论多大的文件都可以统一地处理. 唯一要注意的是, server 接受
    文件上传时, 若文件大于某个 threshold, 需要把文件写入硬盘. 避免占用太多内存.

  * 文件上传要求 `Content-Type: multipart/form-data; boundary=...`, 并在文件的 "part"
    部分 headers::

      Content-Disposition: form-data; name="..."; filename="..."
      Content-Type: ...

    注意必须有 `filename` directive 才能识别为文件上传.

  * 文件下载要求::

      Content-Disposition: attachment; filename="..."

    并配合恰当的 `Content-Type`.

  * 返回与文件类型相符的 `Content-Type`, 而不是 `application/octet-stream`.
    后者仅用于你不知道这个文件到底是什么类型的时候.
    配合 `Content-Disposition: attachment; filename="<name>"` 来告知浏览器该 resource
    是要保存到本地的, 并设置默认的文件名.
    ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition

  * 不需要关心 body 比较大时会不会在 client/server 之间传输时造成数据丢失. 因为
    在 TCP 层保证了两端的 socket 连接之间数据传输是有接受反馈的. 如果接受端的
    kernel buffer 满了, 自然会告知发送端暂停发送. 此时发送端的 ``send(2)`` 会
    blocking 直至所有数据发送完成.

- 在 URI 的 userinfo field ``username[:password]`` 中, 已经不该指定 ``:password``
  部分. 这种明文的密码指定方式已经 deprecated by RFC3986.

- 使用 http proxy 时, 是在向 proxy server 做 http request, 然后等待 proxy server
  返回 http response. 原始访问的完整 uri 放在了 request line 中 (没有使用代理
  时这里只含 path 部分和后面的 query string 等.)

  不使用代理时, 向 google 服务器发请求::

    GET /a/b/c HTTP/1.1
    Host: www.google.com

  变成向代理服务器发请求::

    GET http://www.google.com/a/b/c HTTP/1.1
    Host: www.google.com

- charset 参数.

  对于 MIME type 为 text/* 的文件, 在传输时 ``Content-Type`` 应该添加
  ``charset=<encoding>`` 参数, 来规定编码字符集.

- static files: 图片, js, css 之类的文件本身一般是不变的, 所以称为静态文件.
  而 html 很可能是动态生成的 (根据静态的 html 模板).

- always use relative paths to link your static files between each other.
  这样修改时只需修改一处绝对 url, 而所有其他 url 自动生成.

- http 中, 由于 url 是由 web server 去解析的. url 中的 ``/`` 分隔的 segments
  仅仅是逻辑上的分隔, 没必要对应实际的文件路径.

- `Host` header

  * A `Host` header field must be sent in all HTTP/1.1 request messages.
    A 400 (Bad Request) status code will be sent to any HTTP/1.1 request
    message that lacks a Host header field or contains more than one.

  * `Host` header can contain port number or not.

  * `Host` header can be used for virtual hosting.

- HTTP is stateless (无状态的), 指的是前一组 http 请求响应的结果不会平白无故地影响
  后一组请求响应. 若想要后一请求建立在前一请求的结果基础上, 必须在请求中传递某种
  状态信息, 作为依据.

- HTTP cookie

  * 为什么需要 cookie: 由于 http 本身是 stateless 的, 需要某种方式去标识状态信息,
    cookie 就是一种标准的在 client-server 之间传递状态信息的机制. 通过 cookie,
    我们将多个 stateless HTTP request-response 关联在了一起.

  * How cookie works: 一般情况下, Cookie 首先由 server 在 http response 中, 通过
    ``Set-Cookie`` header 指定内容, 过期时间等, 传递给 user agent. 浏览器将 cookie
    保存在自己的本地存储中. 当下次访问同一个 url 时, 自动在请求中添加 ``Cookie``
    header, 将之前设置的 cookie (仅包含 cookie 的值, 不包含 ``Expires`` 等属性)
    传回去.

    浏览器根据 ``Expires`` 决定何时删除 cookie. 若没有该属性则认为是 session cookie,
    在关闭浏览器时就删除.

    服务端保留着与 cookie 值相关的一系列数据, 即 cookie 值所代表的状态信息.

  * 登录状态即服务端 session 就是通过 cookie 来做的. 设置 session id 之类
    的 cookie 以及过期时间, 来进行 session 控制.

  * cookie 术语: session cookie, persistent cookie, secure cookie, HttpOnly Cookie,
    third-party cookie, supercookie, zombie cookie.

  * ``Set-Cookie`` 可以设置 ``Domain`` 属性, 给其他域名设置 cookie, 这称为
    third-party cookie. 这经常用于 tracking/advertising.

- Session management: 

  * 注意 session 概念在不同语境下的区别.
    
    从 server side 的角度看, 用户从登录至登出是一次 login session. 由于 session
    信息保存在数据库中或 cache 中, 且过期时间可以很长, 这个 session 完全有可能
    跨越多次 client side 浏览器的打开关闭过程, 甚至跨越后端服务的起停. 

    从 client side 角度看, 浏览器打开至关闭即是一次 browser session, 这是 client-side
    session cookie 的时间跨度定义. 也即 session cookie 中的 session 之意.

- CSRF
 
  * 由于 same-origin policy, 浏览器限制 js 脚本只能读取本网站的 cookie. 因此不能
    访问其他网站的 CSRF token, 从而避免了 CSRF attack.
