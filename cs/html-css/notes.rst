- html/css 的相对性和 (la)tex 的绝对性:
  webpage 和 pdf 应用场景最大的区别是: 一个是面向显示器的, 具有适应性, 因此里面的尺寸
  大部分都是相对的; 另一个是面向纸张和印刷的, 具有精确性, 因此里面的尺寸大部分
  都是绝对的.

- 如果 ``<form>`` element 没有 ``action`` attribute 或者是空的值, 且内部没有
  ``<button>`` 有 ``formaction`` attribute, 则浏览器默认 action uri 是当前
  页面. 这经常用于: 一个 url 设计为 GET 时返回 form 页面, POST 时接受 form data.
