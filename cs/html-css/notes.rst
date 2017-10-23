general
=======
- html/css 的相对性和 (la)tex 的绝对性.
  webpage 和 pdf 应用场景最大的区别是: 一个是面向显示器的, 具有适应性, 因此里面的尺寸
  大部分都是相对的; 另一个是面向纸张和印刷的, 具有精确性, 因此里面的尺寸大部分
  都是绝对的.

- 别指望用户会使用最新版本的浏览器, 所以一般选择使用主流浏览器支持的功能.

- 很多公司并不自己购买服务器 serve 网站, 而是购买 web hosting company 的服务,
  例如云服务公司.

html
====

syntax
-------

- element & tag.
  A html element comprises an opening tag and closing tag and contents in between,
  or just an empty tag.

- attribute of elements.

- whitespace collapsing. 文档中多个连续的 whitespace chars 会合并成一个.

elements
--------

- 每个元素都可以设置定义为 global attributes 的那些属性.

- 在 html5 中, 曾经仅表示某种确定的 physical styling 的元素都被语义化地
  使用了. 它们的存在是不可代替的. 因为它们提供了 generic 的语义化
  方式 (通过 class 属性去任意具体化). 例如, i vs em; b vs strong, hr 等.
  我们可以定义 class 赋予 i, b, hr 不同的语义, 而不限于它们默认的表现
  形式. 可以理解为, i 是 em 的一般化; b 是 strong 的一般化等等.

main root
~~~~~~~~~

- ``<html>``, 表示里面都是 html code. the only root element. All must be
  descendant of it.
  里面允许 one ``<head>`` element and one ``<body>`` element.

  attributes.

  * ``xmlns``, xml namespace of the document. Required in documents parsed with
    XML parsers, and optional in text/html documents.

document metadata
~~~~~~~~~~~~~~~~~

- ``<head>``, general information or metadata.
  里面必须有一个 ``<title>`` element. 除非是 iframe srcdoc.

- ``<title>``, 在 browser title bar 或 tab bar 中显示, 只能包含 text.

sectioning root
~~~~~~~~~~~~~~~

- ``<body>``, body 里的内容才显示在页面上.

  attributes.

  * 一系列 callback function 定义.

content sectioning
~~~~~~~~~~~~~~~~~~

- ``<h1>-<h6>``, html 支持 6 层 headings. 不同的 heading 层级应该在文章逻辑
  上进行考虑和使用, 而不是文章的展现样式上.

  Avoid skipping heading levels: always start from <h1>, next use <h2> and so on.

  如果一个页面需要有标题, 应使用 h1 element, 此时 h1 显然只应出现一次.

- ``<address>``, 为它最近的 parent article/body element 联系信息. 这是
  sectioning element, 是比较大的 block 范围. 它里面不能有 heading content,
  sectioning content, header/footer elements, 以及 address element.

  如果地址信息不是为了某个 parent element 服务, 而只是一个独立的地址, 不需要使用
  address element.

text content
~~~~~~~~~~~~

- ``<p>``.

- ``<hr />``, 表示某种 paragraph-level elements 之间的 separation.
  It may be displayed as a horizontal rule in visual browsers, but is now
  defined in semantic terms, rather than presentational terms.

- ``<blockquote>``, (indented) quote block. inline quote 使用 q element.

  attributes.

  * ``cite``, quotation source url.

inline text semantics
~~~~~~~~~~~~~~~~~~~~~

- ``<b>`` 注意 html5 中, b 不是样式上加粗而已. 而是代表 bold 语义, 具体
  是什么样式, 要靠 CSS 定义. 如果仅是为了加粗, 可定义 CSS font-weight.
  它不同于 ``<em>`` ``<strong>`` 等有语义的元素. 如果要使用, 仅应用在
  所有其他有语义的 tag 不合适的时候.

- ``<i>``, 在 html5 中, i 不是样式上 italic. The ``<i>`` tag should represent a
  range of text with a different semantic meaning whose typical typographic
  representation is italicized. This means a browser will typically still
  display its contents in italic type, but is, by definition, no longer
  required to. Use this element only when there is not a more appropriate
  semantic element.

- ``<sub>``, used for simple typographical reasons only. 不要滥用. 对于复杂的
  上下标或其他排版要求, 应该使用 MathML. 对于纯粹的 vertical alignment 修改,
  而不是上下标, 应使用 CSS.

- ``<sup>``, ditto ``<sub>``.

- ``<br />``, line break.

- ``<strong>``, strong importance for its contents. can be nested.

  em vs strong. 两者的区别实际上很模糊, 没有明确的用法定义. 我定义:
  对于 normal emphasis, 使用 em; 如果是想要让读者迅速找到要点, keyword 等,
  使用 strong.

- ``<em>``, emphasis. can be nested.

  i vs em. The ``<em>`` tag represents stress emphasis of its contents, while the
  ``<i>`` tag represents text that is set off from the normal prose, such a foreign
  word, fictional character thoughts, or when the text refers to the definition
  of a word instead of representing its semantic meaning.

  An example for ``<em>`` could be: "Just <em>do</em> it already!". A person or
  software reading the text would pronounce the words in italics with an emphasis.

  An example for ``<i>`` could be: "The <i>Queen Mary</i> sailed last night". Here,
  there is no added emphasis or importance on the word "Queen Mary".

- ``<q>``, inline quote. for short quote that does not require paragraph break.
  Most modern browsers will automatically add quotation marks around text inside.

  attributes.

  * ``cite``, quotation source url.

- ``<abbr>``, abbreviation.

  attributes.

  * ``title``, 提供缩写对应的全称.

- ``<cite>``, a reference to a work. 里面的内容是 cite 的内容的名字或 url.

- ``<dfn>``, definition. 里面是要定义的 term.

- ``<s>``, strike-through. Represent things that are no longer relevant or no
  longer accurate. 这不同于表示 document editing 的 ``<del>``. 两者在不同的
  语义下使用. 注意不同于 del element, 这是 inline element.

document edits
~~~~~~~~~~~~~~

- ``<del>``, 表示内容删除. 里面可以是任何的内容, flow content, phrasing content,
  whatever. 都会被 (默认) strike-through. 遵循 transparent content model, 它的
  存在, 不影响其中内容的展示效果, 除了 strike-through 之外.

  所以注意 del 和 ins element 完全不是 inline text element.

  attributes.

  * ``cite``, url for reasoning of deletion.

  * ``datetime``, date and time of deletion.

- ``<ins>``, 表示内容是插入的, 默认以下划线表示. 其他 ditto.

forms
~~~~~

- 如果 ``<form>`` element 没有 ``action`` attribute 或者是空的值, 且内部没有
  ``<button>`` 有 ``formaction`` attribute, 则浏览器默认 action uri 是当前
  页面. 这经常用于: 一个 url 设计为 GET 时返回 form 页面, POST 时接受 form data.

accessibility
-------------

- 理想情况下, 网站实现时须应用 accessibility features, 使得具有视力障碍的人也能
  通过 screen reader 了解网站内容.

misc
====
- Content management system (CMS). CMS 的核心在于它是为了管理某种 content 而建立的
  系统. 例如, wordpress 的 content 是文章、博客; gitlab 的 content 是 git repo、
  代码. 它是围绕着所管理的内容, 去构建所需的功能.

  不同的 CMS 都有一些共有的特性和功能. 这包含:

  * integrated online help

  * user, group functionality and permission control

  * templating support

  * audit logs

  有很多开源的 CMS 框架, 方便快速构建 CMS. 现今最流行的 CMS 框架是 wordpress.

