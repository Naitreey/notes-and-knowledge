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

- block element vs inline element.

  * block element 占据多个整行 -- 一个 block.

  * inline element 位于 block element 之中, 不占整行, 可以在一行中并排出现.

global attributes
~~~~~~~~~~~~~~~~~

- ``id``, 包含 ASCII letters, ``_``, ``-``, ``.``. Starting with underscore
  or letter, must not contain whitespace. Must be unique in the whole document.

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

- 三种 list: ol, ul, dl.

- ``<ol>``, ordered list.

  attributes.

  * ``reversed``

  * ``start``, 起始序数.

- ``<ul>``, unordered list.

- ``<li>``, 必须出现在 ol, ul, menu element 中.

  attributes.

  * ``value``, 当前序数. 下面的 li element 会从该值起递增.

- ``<dl>``, description list. 里面是一系列的 dt-dd element groups.
  对于每个 group, 由一个或多个 dt elements 起始, 表示要表述的 term
  以及它的 aliases, followed by 一个或多个 dd elements, 是对它们的
  解释.

- ``<dt>``, description term.

- ``<dd>``, description description. Indented.

- ``<figure>``

  类似于 latex 中的 figure 或 listing environment. 它用于构建图例、
  代码 listing 等等为文章或页面的内容进行辅助的内容. 一般包含一个
  figcaption, 用于内容说明.

  figure 不仅仅可以放图片. Usually a figure is an image, illustration, diagram,
  code snippet, etc., that is referenced in the main flow of a document, but
  that can be moved to another part of the document or to an appendix without
  affecting the main flow.

  Being a sectioning root, the outline of the content of the <figure> element
  is excluded from the main outline of the document.

  里面若有 figcaption element, 必须是第一个或最后一个.

- ``<figcaption>``, 必须在 figure element 里.

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

- ``<a>``, anchor.

  不要滥用 a element + onclick event 来模拟 button, 还给 href 赋值
  ``javascript:void(0)`` 来避免页面重载. 这种情况下请直接用 button.
  You should only use an anchor for navigation using a proper URL.

  attributes.

  * ``download``, 下载资源, 而不是 navigate to it. 即使后端没有返回
    ``Content-Disposition: attachment`` 也会下载. 只对 same-origin url
    有效. 若有值, 为预设的文件名.

  * ``href``, 值可以是 url 或 url fragment.

    对于指向其他网站、其他协议等的 url, 显然需要是包含 schema, domain 等部分的
    absolute url; 对于指向本站的其他资源的 url, 一般是使用从 document root
    开始的 full path 形式 relative url; 注意一般不使用相对于本资源的 relative
    url, 不然若本资源位置更改, 里面的 url 都得更改.

    url fragment 由 fragement identifier ``#`` 起始, 指向本资源 (文档) 内部的
    location. ``#top`` 和 ``#`` fragment url 指向当前页面顶部.

  * ``ping``

  * ``referrerpolicy``, 何时加上或不加 Referer header, 以及其值是什么.

  * ``rel``, link types.

  * ``target``, where to display linked url. It's a name of, or keyword for,
    a browsing context, i.e., a window, a tab, a iframe. 一些特殊 keywords:

    - ``_self``, to current context, default;

    - ``_blank``, to new context, 这个 new context 是在 new tab 还是 new window
      取决于用户设置;

    - ``_parent``, to parent context, 若没有 parent 则等于 ``_self``;

    - ``_top``, to top context, 若没有 parent 则等于 ``_self``.

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

image and multimedia
~~~~~~~~~~~~~~~~~~~~

- ``<img>``, image.

  一些分辨率概念:

  * ppi: (对于显示屏) pixels per (square) inch -- ppi.

  * dpi: (对于打印材料) dots per (square) inch -- dpi.

  image formats: bitmap and vector.

  * jpeg. 适合照片等具有自然色彩、多种细致复杂的色彩和渐变等图像.

  * png. 适合具有少数几种单一色彩的人工图像等 (flat color).

  * gif. 适合具有少数几种色彩的静态或动态图像.

  * svg. 矢量图 (一般是人工的).

  attributes.

  * 通过一些属性来明确图像的尺寸有助于在图像尚未加载完全时保持页面的 layout
    固定.

  * ``src``, source url. 必须有这个属性.

  * ``srcset``, for responsive images.

  * ``sizes``, for responsive images.

  * ``height``, 图像的高度, in pixels.

  * ``width``, 图像的宽度, in pixels.

  * ``alt``, 描述图片的 alternative text.
    You should provide a useful value for alt whenever possible, 这是为了
    图片无法显示时或为了视觉障碍人士使用 screen reader 所考虑.
    若不设置 alt, 表示该图片是文章内容的关键组成部分, 不可或缺.

  * ``referrerpolicy``, which referrer to use when fetching the resource.

  * ``crossorigin``, 明确指定跨站图片要用 CORS 方式获取, 从而让浏览器检验
    external source 服务器是否允许该 url 访问. CORS 检验通过通过的跨站图片
    能够在 canvas 中重用并保持 canvas not being tainted, 即 canvas 的数据
    仍然可以提取出来. 这是为了避免敏感数据泄露.

    若不指定该属性, resource is fetched without CORS, preventing its non-tainted
    usage in canvas elements.

  * ``ismap``, whether the image is part of a server-side map. If so, the
    precise coordinates of a click are sent to the server.

  * ``usemap``, 与图片关联的 map element id (``#id``).

table content
~~~~~~~~~~~~~

- ``<table>``, table.

  它允许的 children, 按照下述顺序:

  * one optional caption element;

  * zero or more colgroup element;

  * one optional thead element;

  * zero or more tbody element 或者 one or more tr element;

  * one optional tfoot element;

- ``<caption>``, 若存在, 必须是 table element 里第一个元素.
  When the ``<table>`` element that is the parent of this ``<caption>`` is the only
  descendant of a ``<figure>`` element, use the ``<figcaption>`` element instead.

- ``<thead>``, header part of table.

- ``<tbody>``, body part of table. 可以有多个, 作为 table 的多个语义部分.
  各自独立应用样式.

- ``<tfoot>``, 若存在, 必须在 table 最后.

- ``<tr>``, table row.
  里面可以是 th or td element. tr element 可位于 table, thead, tfoot element 中.

- ``<th>``, table header. 必须在 tr element 内.

  attributes.

  * ``colspan``

  * ``rowspan``

  * ``scope``, 定义与这个 th 关联的 cells 是一行 (``row``) 还是一列 (``col``)
    还是别的什么.

- ``<td>``, table data. 必须在 tr element 内.

  attributes.

  * ``colspan``

  * ``rowspan``

forms
~~~~~

- ``<form>``
  form 里可以有任何 flow content. submit 时 form 里的各层所有
  input elements 的值都会一起提交.

  attributes.

  * ``accept-charset``, server 端接受的 character encodings. 默认是
    ``UNKNOWN``, 表示使用与当前文档相同的编码.

  * ``action``, uri where to send form data. form 里的 input/button
    的 ``formaction`` attribute 会 override this.

    如果 ``<form>`` element 没有 ``action`` attribute 或者是空的值, 且内部没有
    ``<button>`` 有 ``formaction`` attribute, 则浏览器默认 action uri 是当前
    页面. 这经常用于: 一个 url 设计为 GET 时返回 form 页面, POST 时接受 form
    data.

  * ``autocomplete``, 是否允许浏览器自动补全输入, ``on/off``, default on.
    注意这个自动补全指的是弹出的可选输入列表.
    注意对于 login form 的话, modern browsers 会忽略 这个选项的值, 即使是 off
    也会提示是否保存至 password manager 并提供自动补全. 这是安全性考虑, 可以
    设置强密码.

  * ``enctype``, 只影响 post 时. 其值是 form data 要转换成的 mime type 格式.
    ``application/x-www-form-urlencoded`` 默认; 自动变成 ``multipart/form-data``
    若有 file input; ``text/plain``.
    This value can be overridden by a ``formenctype`` attribute on a button/input
    element.

  * ``method``, get/post. 若是 get, form data 添加到 action uri 后面的 query
    string 部分然后再 GET.

  * ``novalidate``, 提交时不验证数据. can be overridden by a ``formnovalidate``
    attribute on a button/input element belonging to the form.

  * ``target``, where to display response of submitted request. 其值和 anchor
    element 的 target attribute 一样.
    This value can be overridden by a ``formtarget`` attribute on a
    input/button element.

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

