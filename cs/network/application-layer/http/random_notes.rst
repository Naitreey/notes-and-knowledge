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

    浏览器根据 ``Expires`` 或 ``Max-Age`` 决定何时删除 cookie. 若两个 directives
    都有, 优先使用 Max-Age. 若两个都没有则认为是 session cookie, 在关闭浏览器时就删除.

    服务端保留着与 cookie 值相关的一系列数据, 即 cookie 值所代表的状态信息.

  * 登录状态即服务端 session 就是通过 cookie 来做的. 设置 session id 之类
    的 cookie 以及过期时间, 来进行 session 控制.

  * cookie 术语: session cookie, persistent cookie, secure cookie, HttpOnly Cookie,
    SameSite cookie, third-party cookie, supercookie, zombie cookie.

  * HttpOnly cookie 可以防止 cookie 因 cross-site scripting attack 而泄露.

  * SameSite cookie 可以防止 CSRF attack.

  * tracking cookie, third-party cookie. 用于 tracking/advertising. 原理是在不同的
    站点加入向同一 domain (例如广告提供商) 的请求 (例如获取广告内容). 该 domain
    在 response 中设置 cookie, 从而标识用户. 在请求中, 包含 origin 信息, 从而
    广告提供商能够建立该用户对不同网站的访问历史等信息. 该请求可能是静态文件加载,
    或者是跨站 CORS 脚本请求.

  * ``Set-Cookie`` header

    - directives: ``<cookie-name>=<value>``, ``Expires=``, ``Max-Age=``,
      ``Domain=``, ``Path=``, ``Secure``, ``HttpOnly``, ``SameSite=``.

    - cookie name 若包含 ``__Secure-`` prefix, 必须搭配 ``Secure`` flag.

    - cookie name 若包含 ``__Host-`` prefix, 必须搭配 ``Secure`` flag, 不能有
      ``Domain=`` directive (从而只应用在同一个 FQDN 上), 并且必须 ``path=/``.

    - ``Domain=<domain>`` 必须是与当前 subdomain 位于同一个 site 中的 domain name.
      浏览器会拒绝跨站的 cookie, 这是出于安全考虑. 否则任何一个网站可以随意给别的
      网站设置 cookie. 若指定了 ``<domain>``, 则它所有的 subdomains 都包含在内.

    - 一个 response 中可以有多个 Set-Cookie, 但是 cookie-name 应该不同.

- Session management:

  * 注意 session 概念在不同语境下的区别.

    从 server side 的角度看, 用户从登录至登出是一次 login session. 由于 session
    信息保存在数据库中或 cache 中, 且过期时间可以很长, 这个 session 完全有可能
    跨越多次 client side 浏览器的打开关闭过程, 甚至跨越后端服务的起停.

    从 client side 角度看, 浏览器打开至关闭即是一次 browser session, 这是 client-side
    session cookie 的时间跨度定义. 也即 session cookie 中的 session 之意.

- Same Orgin Policy 指的是 protocol schema, FQDN/hostname, port number 三者
  必须相同, 才认为是同一个 origin. 注意 FQDN 必须是完全相同, 例如根域名不匹配
  子域名.

- 默认情况下脚本发起的 http 请求必须满足 Same Origin policy, 因此 cross origin 的
  请求不能成功. 实际上浏览器实现了 CORS 机制, 面对 cross origin request, 会特殊处理,
  如果服务端没有给出 CORS 机制预期的响应, 则会报错, 抛弃响应.

- Cross Site Scripting: 在 js 代码中进行 cross-origin request. 一般情况下不能也不需要
  这么做, 除非通过 CORS 机制. 这既是一个可能需要的功能, 也是一个 vulnerability.

- Cross Origin Resource Sharing.

  一个网页可以包含来自其他 origin 的一些种类的 resource,
  这包含各种静态文件 (css, img, script, video) 以及 iframes. 但是 cross-origin 的 ajax
  请求则默认情况下是禁止的 (根据 SOP).

  CORS 对脚本发起的 http request 的规定: request 包含 ``Origin`` header (即请求的来源),
  response 包含 ``Access-Control-Allow-Origin: ...``. 只有响应中这个 header 的域名列表
  包含了 ``Origin`` 的值时浏览器才认为请求合法, 把结果返回给脚本.

  对于非 GET 类型的跨域请求, 还有一个 preflight request. 这个请求通过 ``OPTIONS``
  method 进行, 加上 ``Access-Control-Request-Method`` 和 ``Access-Control-Request-Headers``
  headers. 只有响应中 ``Access-Control-Allow-Origin`` ``Access-Control-Allow-Methods``
  ``Access-Control-Allow-Headers`` 包含请求中的值时浏览器才允许接下来的真正请求.

- 为什么需要不同的 method, 为什么不能全都用 GET?

  理论上可以. 但没有意义. 这是因为, 客观上要进行的操作类型是固定的, 仍然要建立
  一套规范进行区分. 即使全部用 GET, 该取数据的还是要取数据, 该修改数据的还是要修改数据.
  不过此时需要在 GET下面再建立一套规范, 说比如什么参数什么 header 时代表什么操作.
  那么这不是跟 GET POST PUT 之类的定义没什么区别么.

  我们这样区分的原因是, 将 "获取" 操作与 "修改" 操作区分, 从而便于对不同安全性质的操作
  进行不同方式的校验和防护.

- 构建指向某个对象的 url 时, for url to be meaningful, 可以在指定 object id 同时
  指定 slug. 例如 https://www.stackoverflow.com/questions/id/question-title

design patterns
===============

web form
--------

- GET and POST are the only HTTP methods to use when dealing with forms.

  submit form 的时候不一定是 POST, 也有 GET 的 form. 到底是 GET or POST
  取决于 form 提交后是否修改服务系统状态. 例如, 搜索栏就是一个 GET form,
  配置页面就是一个 POST form. 此外, GET would also be unsuitable for
  a password form, for large quantities of data, or for binary data,
  such as an image.

- 尽量使用同一个 url 去获取 form 和处理 form data. 无论 GET/POST form.

- 在 server-side, 若收到 post data 中包含多个相同 name 项, 程序逻辑应该能够
  将之组成一个 value list. 即一个 name key 对应一个 value list.

- 如果 form 中包含敏感信息, 例如密码, 用户身份信息等, 则整个 form data
  应该通过 https 传输. 如今浏览器对 insecure login forms 都有警告.

- form data validation:

  client-side validation 和 server-side validation 都需要, 但两者的用途不同.

  * client-side validation 属于易用性设计, 理论上讲, 可以没有. 它旨在给用户
    提供即刻的错误反馈, 以帮助用户纠正输入错误, 比如非法字符啦, 格式错误啦,
    迅速在 input 附近提示一下, 这种提示的要点是快速, 方便, 不需要访问服务端.
    client-side validation 不能防止 data tampering, 即绕过 form
    验证机制直接向服务端提交请求.

  * server-side validation 属于合法性设计. 旨在为数据合法性做最终的把关.
    这是必须有的.

- Post/Redirect/Get (PRG) pattern.

  * 流程: 需要用 POST method 的 form 在提交后, server 应返回 302/303
    redirection 提供 user agent 接下来要访问的 location, UA 随后 GET 该 url
    获取 form submission 的结果页面.

  * 302/303 redirection 是关键. 无论是 302 Found, 303 See other, 主要效果是
    告诉浏览器, all references to the POST url should be temporarily replaced
    by the ``Location`` header's url. Side effect 是浏览器会自动 GET 这个
    location url, 最终完成工作流.

  * RFC 规定使用 303 See other 作为 PRG 中的 redirection response code. 用于
    消除与 302 Found 的含义混淆情况. 但是实际中 302 才是使用最广且兼容性最好
    的 PRG redirection code.

  * 意义:
    
    1) 刷新按钮可以正常工作, 且不会造成 form resubmission. 这是因为, 
    GET 之后, 刷新的就是 GET request (form submission 的结果页面), 无副作用.
    而直接 POST 返回结果页面的设计则存在 resubmission 问题. 此时, 刷新重放的
    是当前的请求, 即 POST 操作.

    注意, 如果在 POST 尚未接受到响应期间就 refresh, 则还是会 resubmit.
    
    2) 后退按钮可以正常工作. 即按预期返回 GET form 的页面. 这是因为, POST
    request 的 302/303 响应让浏览器记得该 POST 请求应该 被后面的 GET 替换.
    也就是说, 在浏览器历史中, 不存在 POST 了, 只有前一个 GET 和后一个
    GET.[HttpWatchBackBtn]_ 对于直接 POST 的情况, 在后退时可能造成 resubmission
    或者浏览器会为了避免 resubmission 而拒绝加载页面.

    3) 让 POST request 的结果页面能够 bookmark. 因为此时记录的是最后一个 GET 的
    结果 url. 对于直接 POST 的情况, 记录的是 POST 的 url. 而 bookmark 的访问
    只会是 GET, 这样保存的就不是想要的结果页面, 而可能是一个 empty form.

user authentication
-------------------
- logout should be GET or POST?

  我觉得应该是 post. 这是从安全性 (CSRF) 角度考虑, 以及与 login post 操作对应.
  但是 post 的 logout 确实处理起来不太方便 (要 ajax), 一个办法是做成 hiddenform,
  含 csrf token hidden input.

  很多网站都用的是 get, 也有很多用的是 post.

URI
===

overview
--------
- URI 是 URL + URN 的统称. 但一般说 URI 就指的是 URL.

- IRI (internationalized resource identifier) 是 URI 的扩展.
  URI 本身只支持 ASCII, IRI 扩展为 Unicode. 所以说现今的 URL
  实际上是 IRI.

- schema 后面的 ``//`` 本来并不必须, Tim Berners-Lee 为此错误道过歉.
  事实上一些协议并不添加这部分, 例如 ``javascript:``, ``mailto:``, ``tel:``.

components
----------
- absolute url 包含 schema, userinfo, domain, port, path, query parameters,
  url fragment 等.

- relative url 包含 path, query parameters, url fragment 等部分.

URI characters
--------------
- reserved: characters that have special meaning.

- unreserved: characters without special meaning.

url encoding
------------
- A mechanism for encoding information to be used in URI and related usage,
  such as ``application/x-www-form-urlencoded`` form data.

types of encodings
^^^^^^^^^^^^^^^^^^

- reserved characters.
  
  * reserved characters needs to be encoded to be used literally in a url
    segment, if and only if it has special meaning in that url segment.

    例如, / is special in url's path segment, but not special in query string.

  * converting the character to its corresponding byte value in ASCII and then
    representing that value as a pair of hexadecimal digits prefixed with ``%``.

- unreserved ASCII characters.

  * unreserved characters need not be percent-encoded.

- binary data.

  * the representation of binary data in a URI must divide the data into 8-bit
    bytes and percent-encode each byte.

- unicode characters.

  * converted to utf-8 encoded byte sequence, then url-encoded as binary data.

- in ``application/x-www-form-urlencoded`` media type.

  * special treatment: spaces is encoded as ``+``

url design
----------

* A clean, elegant URL scheme is an important detail in a high-quality
  Web application.

  Cool urls don't change. Try to make your url last as long as possible.

* 遵从 REST 思想.

* ajax 返回 json 的 url api 可以直接以 ``.json`` 结尾, 以示与普通 view
  的区别.

url length limit
----------------

* HTTP 协议本身并不限制 url 长度. 但建议接收方和发送方都支持至少 8000 bytes
  长度的 url.

* 若 url 太长服务端无法处理, 应返回 414 (URI Too Long).

* 各浏览器有不同的 url 长度限制 (可输入的或可接受的 url 长度). IE8+ ~ 2000 bytes,
  其他浏览器都比这个长, 甚至长很多. 所以 2000 bytes 可看作是长度的上确界.

methods
=======



Headers
=======

Referer
-------

request header. 包含该请求来自的那个页面对应的 url.
浏览器自动加上它. 可被后端用于识别来源, 从而 logging, tracking 等等.
url fragment (``#id``) 和 userinfo ``user@pass`` 不被包含.

若原页面是 local ``file:`` ``data:`` uri 则不设置该 header;
若原页面是 https 的, 但本请求是 http 的, 则不设置该 header.

事实上这个单词拼错了: Referrer.

Expect
------

request header: 指定为了完成请求, 预期服务器要满足的条件.

目前仅定义了 ``Expect: 100-continue``. 这用于避免白白时间和资源将整个请求
传递给了服务端, 结果请求本身不合法. 对于体积比较大的 POST 类请求时, 可首先
传递 header 部分, 加上这个 header, 若相应返回 status code 100 (Continue),
则继续上传 body 部分, 若返回 417 (Expectation Failed) 则中断.

这个 header 目前没有主流浏览器实现, 只有 cURL 会在 POST 大文件时这么做.
对于 curl, 它发出 header 部分后, 会等待一个 ``expect100-timeout`` 时间,
若没等到任何相应, 则继续传 body.

X-Forwarded-Host
----------------

在包含 reverse proxy (反向代理) 的环境中, 代理服务器
(即直接接受客户端请求的服务器, cache, CDN 等) 向真实处理请求的服务器转发时,
要加上这个 header, 其值为原始的 ``HOST`` header 值. 从而真实服务端能够判断
客户端请求的 host 是什么.

X-Forwarded-For
---------------

在 proxy 向服务端请求时, 或者 reverse proxy 向真实服务端
请求时, 通过这个 header, 来识别原始的请求客户端 IP 地址.

X-Forwarded-For, X-Forwarded-Host 的值都可能包含多项地址, 因经过了多次代理或
转发. 从而第一个是最原始那个.

X-Requested-With
----------------

现代的 js library 在做 AJAX 请求时, 都会添加这个 header,
并设置值为 ``XMLHttpRequest``. 这是为了防止 AJAX 来源的 CSRF attack.

当服务端本身允许某个 ajax 跨域, 为了区别合法和非法的跨域请求, 要对请求来源进行验证.
浏览器发现 ajax 请求包含了这个 header 时, 会添加 CORS 相关 headers 或 preflight
请求, 这样服务端就可以验证 ajax 的真伪. 若请求本身不包含这个 header, 服务端可以
直接拒绝掉.

Host
----

* A `Host` header field must be sent in all HTTP/1.1 request messages.
  A 400 (Bad Request) status code will be sent to any HTTP/1.1 request
  message that lacks a Host header field or contains more than one.

* `Host` header can contain port number or not.

* `Host` header can be used for virtual hosting.

Vary
----

* 与 cache 相关. Vary 的值是一系列 comma separated headers, 这些 headers
  是出现在 request 中的. cache 在缓存 response 时, 将根据 Host, url path,
  以及 Vary 中出现的各个 request headers, 来对 response 进行分类缓存.
  达到的效果是, cache 将根据 request 中的 header 的值选择 cached response
  版本.

  例如, ``Vary: User-Agent`` 可以避免 mobile browser 收到 desktop 版的页面.
  因如果 cache 中没有 mobile 的 user agent 对应的页面, cache miss 从而向
  原始服务端请求.

Cache-Control
-------------

* request 和 response 都可以设置.

* directives.

  - ``public``, response only. response may be cached by any cache.

  - ``private``, response only. response is intended for single user and should
    not be stored by a shared cache. A private cache may store the response.

  - ``no-cache``, request/response. cache must submit the request to origin
    server for validation before returning the cached copy.

  - ``no-store``, request/response. cache should not store anything about
    request/response.

  - ``only-if-cached``, request only. client only want the cached response.

  - ``max-age=<seconds>``, request/response. the max time the resource will
    be considered fresh.

  - ``must-revalidate``, response only. stale resoures must be validated before
    serving.

Strict-Transport-Security
-------------------------

response header.
response 包含该 header 告知浏览器启动 HSTS 机制.

directives.

* max-age. 持续 ``max-age`` 时间 (in seconds). 意思是浏览器会记这么久, 在这段时间
  内, 所有对该 domain 的所有访问, 都强制使用 https. 无论是不是一个 browser session.
  只考虑绝对时间. 过期后的非指定 scheme 的首次访问转回 http.

  每次响应中出现该 header & max-age directive, 过期时间都会刷新, 重新计算.
  若想 disable HSTS, 设置 max-age=0.

* includeSubDomains. this rule applies to all of the site's subdomains as well.

* preload. 表示该 domain 在 browser 预加载的 HSTS domain list 中.

X-Frame-Options
---------------

response header.
服务端通过设置该 header, 告知浏览器是否允许以 ``<iframe>``, ``<frame>``,
``<object>`` 等嵌入式方式 render 这个响应. 这用于解决 clickjacking.

directives.

* DENY. 禁止一切嵌入.

* SAMEORIGIN. 当该资源与触发请求的页面同源时才允许嵌入.

* ALLOW-FROM <uri>. 只允许匹配的 domain 来源时嵌入.

X-Content-Type-Options
----------------------

防止浏览器根据自己 sniff 到的 (即自己认为的)
content type 而 override 服务端设置的 Content-Type header.

directives.

* nosniff.

X-XSS-Protection
----------------

directives.

* 0. disable xss filtering.

* 1. enable. If a cross-site scripting attack is detected, the browser will
  sanitize the page (remove the unsafe parts).

* 1; mode=block. prevent rendering of the page if an attack is detected.

Status code in response
=======================
- 5 classes of responses:
  
  * informational responses,
    
  * successful responses,
    
  * redirects,
    
  * client errors,
    
  * servers errors.

informational
-------------

100 Continue
^^^^^^^^^^^^
- Used with ``Expect`` request header. 表示 client should continue with the request,
  or ignore it if the client has finished request.  See also `Expect`_.

101 Switching Protocol
^^^^^^^^^^^^^^^^^^^^^^

102 Processing
^^^^^^^^^^^^^^

- In WebDAV

successful
----------

200 OK
^^^^^^

Browser development tools
=========================
- 若从浏览器已经发出请求, 但尚未收到响应 (无论成功失败) 也尚未超时, 此时在 dev
  tools 的 Network 部分是看不到该请求记录的.
  确认请求是否发出的方式是查看浏览器左下角 是否有 "Waiting for <some website>...",
  即浏览器在等待 server 返回该请求的响应. 若有则已经发出. 实在不行可以抓包查看是否有
  HTTP request 流量.

HTTPS
=====

HTTP Strict Transport Security
------------------------------
concept
~~~~~~~
- It allows web servers to declare that web browsers (or other complying user
  agents) should only interact with it using secure HTTPS connections, and
  never via the insecure HTTP protocol.

- 在 HSTS 机制下,
  
  * same domain 的任何 insecure plain http url 都会在请求时转换为 https.

  * 若连接的安全性不能保障, 例如 TLS 证书不可信, 则不允许访问该站点.

- HTTPS + HSTS 能很大程度上解决 MITM attack.

- 主流浏览器都 pre-load 了默认启用 HSTS 机制的网站列表.

headers
~~~~~~~
- ``Strict-Transport-Security``

References
==========
.. [HttpWatchBackBtn] `60% of Web Users Can’t be Wrong – Don’t Break the Back Button! <https://blog.httpwatch.com/2007/10/03/60-of-web-users-cant-be-wrong-dont-break-the-back-button/>`_
