web components
==============

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

- file uploading.

  * 文件大小不是问题. 无论多大的文件都可以统一地处理. 唯一要注意的是, server 接
    受文件上传时, 若文件大于某个 threshold, 需要把文件写入硬盘. 避免占用太多内
    存.

  * 文件上传时, 需设置 ``<form enctype="multipart/form-data">``.
    
  * 文件上传时, request header 中包含::
   
     Content-Type: multipart/form-data; boundary=...
    
    并在文件的 "part" 部分包含以下 headers::

      Content-Disposition: form-data; name="..."; filename="..."
      Content-Type: ...

    注意必须有 ``filename`` directive 才能识别为文件上传.

user authentication
-------------------
- logout should be GET or POST?

  我觉得应该是 post. 这是从安全性 (CSRF) 角度考虑, 以及与 login post 操作对应.
  但是 post 的 logout 确实处理起来不太方便 (要 ajax), 一个办法是做成 hiddenform,
  含 csrf token hidden input.

  很多网站都用的是 get, 也有很多用的是 post.

REST design
===========
- It's not necessary or even possible to design your web service sticking
  strictly to REST rules. But they are great guidelines for that matter.

- REST suggests that we have a URL structure that matches our data structure.

security
========

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
- Same Orgin Policy 指的是 protocol schema, FQDN/hostname, port number 三者
  必须相同, 才认为是同一个 origin. 注意 FQDN 必须是完全相同, 例如根域名不匹配
  子域名.

- 默认情况下脚本发起的 http 请求必须满足 Same Origin policy, 因此 cross origin
  的请求不能成功. 若要进行 cross origin request, 必须遵守 CORS 请求的规则.  如
  果服务端没有给出 CORS 机制预期的响应, 则会报错, 抛弃响应.

- SOP 限制了默认情况下 AJAX 不能 make cross-origin request. 但是这不影响
  ``window.location`` 向其他 origin 的修改, 静态文件 url 的不同来源, POST form
  ``action`` 的不同来源之类的 cross-origin 操作.

  只要攻击者的服务端实现了 CORS 机制, cross-orgin request 照样会成功, 所以
  SOP 不能防止 XSS 攻击.

- Cross Origin Resource Sharing.

  一个网页可以包含来自其他 origin 的一些种类的 resource, 这包含各种静态文件
  (css, img, script, video) 以及 iframes. 但是 cross-origin 的 ajax 请求则默认
  情况下是禁止的 (根据 SOP).

  CORS 对脚本发起的 http request 的规定: request 包含 ``Origin`` header (即请求
  的来源), response 包含 ``Access-Control-Allow-Origin: ...``. 只有响应中这个
  header 的域名列表包含了 ``Origin`` 的值时浏览器才认为请求合法, 把结果返回给脚
  本.

  对于非 GET 类型的跨域请求, 还有一个 preflight request. 这个请求通过
  ``OPTIONS`` method 进行, 加上 ``Access-Control-Request-Method`` 和
  ``Access-Control-Request-Headers`` headers. 只有响应中
  ``Access-Control-Allow-Origin`` ``Access-Control-Allow-Methods``
  ``Access-Control-Allow-Headers`` 包含请求中的值时浏览器才允许接下来的真正请求.

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

  XSS 在实现时就是在 js 代码中进行 cross-origin request. 它需要通过 CORS 机制
  进行.

* CSRF 和 XSS attack 的区别:

  - CSRF 的形式不一定是脚本请求, 或者说往往不是脚本请求, 它往往是通过某种方式
    伪装一个 GET url, 例如 img, link 等; 或者伪装一个 POST form.
    XSS 特指的是通过脚本发起的跨域请求.

  - CSRF & XSS 的请求目标不同. CSRF 一般是伪造向用户信任的站点的请求, 以企图冒
    充用户实现某种行为; XSS 一般是向 attacker 自己的站点发送请求, 包含从用户端
    收集到的敏感信息.

  - CSRF & XSS 利用的信任不同. XSS attacks exploit the trust a user has for a
    web site, while CSRF attacks exploit the trust a web site has for its
    users.

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

session fixation attack 有以下实施方法:

- 简单的物理攻击. 一台电脑上 A 用户未登出, B 用户使用该电脑, 使用 A 用户的合法
  session, 仿冒用户 A.
  
  这种仿冒在敏感信息重登录处被截断.

- attack with cross-subdomain cookie. 这在以下情况下发生:
  一个正常 domain ``example.com`` 的 subdomain ``bad.example.com`` 由攻击者控制.
  cookie 机制允许一个 subdomain 设置 cookie 的 domain 为 ``*.example.com``, 这样
  攻击者可以给 client 设置一个对 ``good.example.com`` 来讲合法的 session, 等
  用户访问后者网站时, 自动以攻击者控制的账户认证. 若用户输入自己的敏感信息, 攻击者
  可以之后获取.
  
  这实际上是一种反向的仿冒, 诱导. 这也可以通过重登录处理. 此外, 还要注意的是,
  不应该把子域名交给 untrusted user 去管理, 除非是 compromised.

Clickjacking attack
-------------------
指的是恶意网站欺骗用户去点击某些看似正常的按钮、链接等, 进行一些看似正常的交互.
由于这些点击严格讲是完全由用户触发的单纯操作, 所以浏览器无法清楚区分这些操作
是否是用户的本意.

实施方法一般是通过 iframe 嵌套一个希望用户点击的页面. 然后通过某种方式 trick 用户
去点击. 用户以为自己点击的是该网站的一个元素, 但实际上点击的是目标页面上的东西.

There is no way of tracing such actions to the attackers later, as the users
would have been genuinely authenticated on the hidden page.

clickjacking 的实现需要一些 orchestration, 例如被劫持的页面需要已经登录, 并且
可能需要劫持前后一系列点击事件, 最终达到攻击者的目的.

攻击例子: downloading and running malware; make someone follow on twitter/facebook
or google plus +1 (likejacking); click ads to generate pay-per-click revenue;
playing youtube videos to gain views.

mitigation
~~~~~~~~~~
网站应使用 ``X-Frame-Options``, 指定是否允许在 iframe 内加载.

file uploading
--------------

- 接收用户上传的文件时, 需要校验文件是否确实是 ``Content-Type`` header 所声称的
  类型. 如果是 ``text/*`` 类型, 还需校验字符编码是否为 ``charset`` 所声称的
  编码. 若否, 且判断为不合法, 需要拒绝掉.
