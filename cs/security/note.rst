Web
===

HTTPS
-----
- 在中国, 不使用 https 而使用 plain text http 绝对是作死. 因为 http 劫持
  非常常见, 导致客户端中弹广告等现象. 更不用说由此带来的安全性问题, 例如:

  * MITM attack: 任何人可以截取 http 通信中的敏感信息, 例如帐号密码信息.
    任何中间设备 (如果有人黑了不靠谱的大陆运营商) 可能在 payload 中插入
    修改或插入链接, 指向恶意地址. 若使用 SSL, 这些都无法做到.

  * DNS poisoning: 将 server FQDN 转移到攻击者的地址后, http payload 直接被
    收到. 若使用 SSL, 即使通信被转移至攻击者那里, 由于首先要建立加密信道,
    攻击者必须预先拿到原始网站的 SSL 证书, 从而无法实现或者不再有意义.

SOP & CORS
----------
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

CSRF & XSS attacks
------------------
* CSRF 是恶意页面假冒为用户, 向可信站点的请求行为.

* XSS 是比较宽泛的攻击分类. 凡是未授权的脚本插入和运行, 都可算是 XSS. 例如,
  页面中嵌入了恶意的脚本, 或嵌入了恶意的链接然后执行了恶意的脚本.

  XSS vulnerabilities already let an attacker do anything a CSRF vulnerability
  allows and much worse.

* CSRF 和 XSS attack 的区别:

  - CSRF 的形式不一定是脚本请求, 或者说往往不是脚本请求, 它往往是通过某种方式
    伪装一个 GET url, 例如 img, link 等; 或者伪装一个 POST form.
    XSS 特指的是通过脚本发起的跨域请求.

  - CSRF 一般是伪造向用户信任的站点的请求, 以企图冒充用户实现某种行为;
    XSS 一般是向 attacker 自己的站点发送请求, 包含从用户端收集到的敏感信息.

* CSRF attack 的应对方式:

  - 在 form 中加入 CSRF token field, 由于不是 same origin 的请求拿不到该页面上的
    token, 即使拿到敏感 cookie 也无法让 POST 合法. 当然, 伪造方可以猜测 CSRF token
    值应该是什么. 所以这还要求服务端去实现难以猜中的 token 值 (以及每次刷新 form
    都有不同的 csrf token 值).

  - 对于 js ajax 请求, 手动设置某个 csrf token header. 跨域请求虽然能带上
    csrf token cookie, 但读不到 cookie 的值, 不能设置 csrf token header,
    这样的请求会被服务端拒绝. ajax 的 post 请求必须使用 csrf token header.

  - 目前一种新方式是使用 SameSite cookie. 这样不是相同来源的请求根本拿不到敏感
    cookie, 不再需要额外的 csrf token 的验证. 让浏览器自己去限制, 省去了人工实现
    csrf token 的麻烦.

  - 考虑到 MITM attack, CSRF token 提供的保护如果没有 HTTPS 加密传输做配合,
    是完全没有意义的.

- GET/POST & CSRF.

  CSRF 的对抗手段一般只保护状态改变类的操作比如 PUT/POST. 因为 GET 等 "safe"
  methods 只应该做安全的事.

  这也是不能用 GET 进行 state change 操作的最致命原因: 默认 GET 是安全操作,
  一般不做 CSRF 防护.

  注意浏览器提交的 form POST 不涉及脚本, 不受到 Same-Origin Policy 限制, 可以
  post 至其他 domain. 因此必须采用一些避免 CSRF attack 的安全措施.

- subdomain problem.
  Subdomains within a site will be able to set cookies on the client for the
  whole domain. By setting the cookie and using a corresponding token,
  subdomains will be able to circumvent the CSRF protection. The only way to
  avoid this is to ensure that subdomains are controlled by trusted users (or,
  are at least unable to set cookies). Note that even without CSRF, there are
  other vulnerabilities, such as session fixation, that make giving subdomains
  to untrusted parties a bad idea, and these vulnerabilities cannot easily be
  fixed with current browsers.

- 作为客户端用户, 防止 XSS/CSRF attack 的唯一靠谱方式就是不访问不靠谱的网站.
  剩下的只能依靠 "靠谱" 网站的研发能重视安全性, 使用了 HttpOnly/SameSite cookie,
  检查输入的 html 和 js 代码, 等防范手段.

Session fixation attack and re-login
------------------------------------
如果浏览器本身具有未过期的合法 session id, 那么可以认为当前浏览器 "可能是" session
对应用户, 可以显示基本的用户信息如用户名, 以及应用用户的自定义设置等 (例如 google
search); 但是当浏览器访问敏感信息时, 需要要求用户重登录, 认证确实用户本人. 在认证
后, 返回新的 session id, 并标识用户 session 已经认证 (例如在 session 数据中添加
已认证的 key).

这么做 (认证当前用户确实是声称的用户) 一般化地讲, 是为了避免 session fixation attack.
就是用户 B 使用 A 的合法 session id, 仿冒用户 A. 这种仿冒在重登录操作处被截断.
