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

- 别用严格的 markup language 标准去要求 html 然后嫌人家垃圾, 功能不完善, 鄙视什么的.
  html 不过是一个工具, 它和 css, js 等一起支撑着 web 和相关技术栈, 创造着非常多的
  价值. 这就够了. 别介意太多. 反正你也不把它当平时写东西的标记语言用嘛.

html versions
-------------
html can be seen as a loosely formatted xml variants for the web.

xhtml 是应用 xml 语法, 对 html 进行部分严格化和修正而发明的. xhtml 可以看作是
xml 的严格子集, 是 html's serialized format. 不过 xhtml 已经死了. 根本没人 care,
大家去用 json 了.

document structure
------------------

1. byte order mark (BOM) character. (optional)

2. Any number of comments and ASCII whitespaces.

3. A DOCTYPE.

4. Any number of comments and ASCII whitespaces.

5. The document element -- ``html`` element.

6. Any number of comments and ASCII whitespaces.

syntax
------

- element & tag.
  A html element comprises an opening tag and closing tag and contents in between,
  or just an empty tag.

- attribute of elements.

  * boolean attributes. 存在为 true, 不存在为 false, 而无论设置值是多少.
    按照标准要求, 可以设置 ``attr=""``. 注意对于 boolean 属性,
    ``attr="false"`` 实际上是 true, 因为存在.

  * enumerated attributes. 必须设置在预定义的列表中的值. 这些值可能包含
    true, false. 但注意这仍然是 enumerated attribute, 而不是 boolean
    attribute.

- whitespace collapsing. 文档中多个连续的 whitespace chars 会合并成一个.

inline-level and block-level elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- block-level element 占据多个整行 -- 一个 block. Browsers typically display
  the block-level element with a newline both before and after the element.

  block element 中可以存在 block or inline elements.

  block elements 只能在 body 中出现.

- inline-level element 位于 block-level element 之中, 不占整行, 可以在一行
  中并排出现. An inline element does not start on a new line and only takes up
  as much width as necessary.

  inline element 中只能存在 inline elements.

- CSS ``display`` property 可以改变一个元素的 level.

- block & inline elements 的概念在 html5 中已经被 content categories 所替代.
  block elements 类似于 flow content, inline elements 类似于 phrasing
  content.

  但注意在 html5 中, flow & phrasing content 两种类型不是互斥的. 一个元素可以
  同时是这两种类型.

comment
^^^^^^^

- ``<!-- comment -->``

content preloading
------------------
- preloading 是指定一些资源不要等到 rendering 时遇到才下载, 而是在页面加载的
  早期, 在 rendering 发生之前就早早开始下载. 从而避免在 rendering 时卡住 (等待
  下载), 提高效率.

  例如预加载 font, This makes it much more likely that the font will be
  available by the time the page render is complete, cutting down on FOUT
  (flash of unstyled text) issues.

- link element 中包含 ``ref="preload"`` 以及 ``as=`` 指定 preload resource 的
  类型.

- 可加入 ``type=`` attribute 指定资源的 mime type, 帮助浏览器选择只 preload
  它支持的类型的资源. 以及 ``media=`` 选择满足 media query 的资源.

elements
--------

- 每个元素都可以设置定义为 global attributes 的那些属性.

- 在 html5 中, 曾经仅表示某种确定的 physical styling 的元素都被语义化地
  使用了. 它们的存在是不可代替的. 因为它们提供了 generic 的语义化
  方式 (通过 class 属性去任意具体化). 例如, i vs em; b vs strong, hr 等.
  我们可以定义 class 赋予 i, b, hr 不同的语义, 而不限于它们默认的表现
  形式. 可以理解为, i 是 em 的一般化; b 是 strong 的一般化等等.

- html element tag 提供语义结构 (semantics). 浏览器给每个 html element
  一组默认的 css 样式设置, 符合该元素的 conventional 表现形式.

main root
^^^^^^^^^

- ``<html>``, 表示里面都是 html code. the only root element. All must be
  descendant of it.
  里面允许 one ``<head>`` element and one ``<body>`` element.

  attributes.

  * ``xmlns``, xml namespace of the document. Required in documents parsed with
    XML parsers, and optional in text/html documents.

document metadata
^^^^^^^^^^^^^^^^^

- ``<head>``, general information or metadata.
  里面必须有一个 ``<title>`` element. 除非是 iframe srcdoc.

- ``<meta>``, generic metadata that cannot be represented by other metadata
  elements. 当没有其他更合适的 metadata element 可以使用时, 使用 meta element.

  attributes.

  * ``name``, 这个 metadata 的名字.

    当 itemprop, http-equiv, charset 设置时, 不设置该属性.

    values:

    - ``application-name``.

    - ``author``.

    - ``description``, 包含本页面的简短描述. 在搜索引擎中搜索时, 若关键字命中了
      description 的内容, 搜索引擎会在 title 下面展示 description 的所有内容.

    - ``generator``.

    - ``keywords``, useless. 在搜索引擎早期是靠关键字进行搜索的.

    - ``robots``, 影响 cooperative crawlers 的行为. 与 robots.txt 类似.
      对于非 html 内容, 使用 ``X-Robot-Tags`` 影响 crawlers 的行为.

    - ``viewport``, 用于移动端浏览器. viewport 是页面尺寸大小的范围, 它不同
      于屏幕的显示范围. 由于移动端屏幕尺寸可能很小, 为了保持页面元素的良好
      布局效果, 需要明确设置 viewport.

      对应的 ``content`` 值是 a list of ``key=val`` pairs.

      See also `viewport meta tag`_.

  * ``http-equiv``, 设置一个 http header 的名字, ``content`` 是内容.

  * ``content``, ``http-equiv`` or ``name`` 属性对应的值.

  * ``charset``, page's character encoding. 最好使用 utf-8. 其值必须和文件本身
    的 encoding 一致. 这个 encoding 会被 ``Content-Type`` header 值 override.

    尽管优先级不高, 但仍然建议设置 charset meta element.

- ``<title>``, 在 browser title bar 或 tab bar 中显示, 只能包含 text.

- ``<link>``, 声明该 document 与一个 external resource 的关系.
  link element 是否能出现在 body element 中 (或只能出现在 head element 中) 取决于
  它的 link type. 例如 stylesheet link 可以出现在 body 中.

  attributes.

  * ``crossorigin``, 使用 CORS 机制进行跨域请求. enumerated.

  * ``href``, url of the linked resource.

  * ``hreflang``, only used with ``href``. 指定资源的语言. only advisory.

  * ``media``, 定义该资源适合的 media type. 值是 media query.

  * ``rel``, 链接的资源相对于本文档而言是什么关系. 值是 a space separated link types.

  * ``sizes``, 与 ``rel="icon"`` 一起使用, 指定 icon size.

  * ``title``, 与 ``rel="stylesheet"`` 一起使用, 指定 prefered or alternate
    stylesheet.

  * ``as``, 与 ``rel="preload"`` 一起使用,

  * ``type``, mime type of the linked resource.

  * ``integrity``, a base64-encoded cryptographic hash of the resource (file)
    you’re telling the browser to fetch. 如果浏览器不支持就自动忽略, 所以使用
    CDN 时还是加上比较好.

- ``<style>``, 属于 metadata content, 从 html 规范上讲, 只能放在 head element 中.
  Although in practice, every browser allows style element in body.

  attributes.

  * ``type``, mime type of styling language.

  * ``media``, a media query defining which media the style applies to.

  * ``title``, 定义该 style definition 所属的 alternative stylesheet set.

sectioning root
^^^^^^^^^^^^^^^

- ``<body>``, body 里的内容才显示在页面上.

  attributes.

  * 一系列 callback function 定义.

content sectioning
^^^^^^^^^^^^^^^^^^

- ``<article>``, a self-contained composition in a page. 常用于表示各种文章内容
  主体. h1-h6 一般在 article 内部用于 section heading.

  When an ``<article>`` element is nested, the inner element represents an article
  related to the outer element.

  address element and time element 在 article 中表示作者地址和写作时间.

- ``<aside>``, 与页面主要内容相关联的但不属于主要内容的东西, 即 aside 字面意思.

- ``<nav>``, 提供 navigation links, 例如导航栏, menu, index, TOC.
  sectioning content element.

  Not all links of a document must be in a ``<nav>`` element, which is intended
  only for major block of navigation links; typically the ``<footer>`` element
  often has a list of links that don't need to be in a ``<nav>`` element.

- ``<section>``, a section of semantic/logical functionality in document.
  每个 section 应该由某种 heading element (e.g., h1-h6) 进行识别.

  section vs div. The ``<section>`` element is not a generic container element.
  When an element is needed only for styling purposes or as a convenience for
  scripting, authors are encouraged to use the ``<div>`` element instead.
  A general rule is that the ``<section>`` element is appropriate only if
  the element’s contents would be listed explicitly in the document’s outline.

- ``<h1>-<h6>``, html 支持 6 层 headings. 不同的 heading 层级应该在文章逻辑
  上进行考虑和使用, 而不是文章的展现样式上. 这些元素在各种 sectioning content
  中使用.

  Avoid skipping heading levels: always start from <h1>, next use <h2> and so on.

  如果一个页面需要有标题, 应使用 h1 element, 此时 h1 显然只应出现一次.

- ``<header>``, header to its nearest sectioning content or sectioning root element.
  The ``<header>`` ``<footer>`` elements are not sectioning content.

- ``<footer>``, footer to its nearest sectioning content or sectioning root
  element. 它包含例如 address element.

- ``<address>``, 为它最近的 parent article/body element 联系信息. 这是
  sectioning element, 是比较大的 block 范围. 它里面不能有 heading content,
  sectioning content, header/footer elements, 以及 address element.

  如果地址信息不是为了某个 parent element 服务, 而只是一个独立的地址, 不需要使用
  address element.

text content
^^^^^^^^^^^^

- ``<main>``, semantic main content, central functionality, etc. of the document,
  or application. 如果一个页面需要多个 article 构成主体, main 中可以有多个 article.

- ``<div>``, 任意的 content container block, 没有任何本征含义, 只用于
  wrap flow content, 以形成一个 division in the document. 方便对这个整体进行操作.

  div element 只该在别的 semantic sectioning element 不合适的情况下使用.

- ``<p>``.

- ``<pre>`` preformatted text. 虽然默认使用 monospace font, 但这在语义上
  不仅仅是代码, 可以是任何内容, 仅仅是 preformatted 而已. 注意 pre 里面
  的 html element 仍会解析.

  在一般情况下, html 中出现的任意多个连续的 whitespace chars 会 collapse
  成一个, 这是一个全局的效果, 而不论是什么 element 内部或外部. 可以认为,
  在 pre element 中, 只是屏蔽掉了这个 whitespace collapsing 算法而已.
  因此 pre 保证了它里面的 text 以及它里面任何元素的 text 部分的 whitespace
  chars 都会被保留下来. (这个 whitespace collapsing 算法实际上由 css 的
  ``white-space`` property 控制. 浏览器默认设置 pre element ``white-space: pre``.)

  对于 code block, 则一般使用

  .. code:: html
    <pre><code>
    ...
    </code></pre>

  注意虽然 pre 默认就是 monospace font, 但是由于 pre 代表的是禁用 whitespace
  collapsing, 本质上不一定用 monospace, 所以这里应理解为 code element
  提供了 semantics & monospace appearance.

  html is such a incompetent markup language that can not embed verbatim
  UNMODIFIED code written in itself. 无论是 pre 还是 code element, 都不能
  真正地 verbatim 包含代码. 所有 html 特殊字符都需要转义. Such a shame.
  (真正可以实现 verbatim 的 tag 是已经废除的 ``xmp`` example tag.)

  As a markup language, html is awful. That's why nobody use it to write
  serious article-like stuff -- only generates it from sources written in other
  markup languages, and only for purpose of display on the web.

  html is the tool of The Web. That's the fact, so be it. Eventually it's
  just a tool that either solves your problem or not. Let's use this ugly
  tool ONLY for the web and all its related tech stacks. And forget about
  it being a so-called markup language.

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

- ``<data>``, 主要用于将数据的文字表现形式和它的真实值关联起来, 跟
  ``data-*`` attribute 作用类似. 那么, 使用 data element 的场景是
  当这部分文字本省没有一个语义合适的 tag wrap it, 从而没处写 ``data-*``
  属性时, 可以使用 data element, 配合 value attribute.

  attributes.

  * ``value``, value of content of this element.

inline text semantics
^^^^^^^^^^^^^^^^^^^^^

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

- ``<mark>``, highlighted text. a run of text marked for reference purpose, due
  to its relevance in a particular context. 例如搜索结果中标记关键字.

  strong vs em vs mark.

  * The <strong> element represents strong importance for its contents. Changing
    the importance of a piece of text with the strong element does not change the
    meaning of the sentence.

    <strong> denotes important text, but does not affect meaning.

  * The <em> element represents stress emphasis of its contents. The placement
    of stress emphasis changes the meaning of the sentence.

    <em> denotes important text and affects the meaning of the content by saying
    that it should be read/spoken with emphasis.

  * The <mark> element represents a run of text in one document marked or
    highlighted for reference purposes, due to its relevance in another
    context.

    <mark> doesn't really have relevance to content, only context
    (e.g.  marking content that matches a search term, misspelled words,
    selected content in a web app, etc.).

- ``<q>``, inline quote. for short quote that does not require paragraph break.
  Most modern browsers will automatically add quotation marks around text inside.

  attributes.

  * ``cite``, quotation source url.

- ``<abbr>``, abbreviation.

  attributes.

  * ``title``, 提供缩写对应的全称.

- ``<cite>``, a reference to a work. 里面的内容是 cite 的内容的名字或 url.
  它存在的意义是 semantic meaning.

- ``<dfn>``, definition. 里面是要定义的 term.

- ``<s>``, Represent things that are no longer relevant or no longer accurate.
  默认显示为 strike-through. 这不同于表示 document editing 的 ``<del>``. 两者在
  不同的语义下使用. 注意不同于 del element, 这是 inline element.

- ``<u>``, Represents a span of text with an unarticulated, though explicitly
  rendered, non-textual annotation. 默认显示为 underline.

  The HTML 5 specification reminds developers that other elements are almost
  always more appropriate than <u>.

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

    href 属性省略时, anchor element is placeholder link. 若 href 属性存在但值为
    空字符串, 则指向当前页面 url.

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

- ``<code>``, inline code in monospace font. 注意 code 里面不会 escape
  html code, 或者准确的说, 里面允许包含并且浏览器会解释里面的其他 html elements.

- ``<kbd>``, keyboard input, 默认显示为 monospace text. 与 code element 的区别
  仅在于 semantic purpose.

- ``<samp>``, sample output from program. 默认显示为 monospace text.
  与 code element 的区别仅在于 semantic purpose.

- ``<small>``, represent side-comments and small print, including copyright and
  legal text, independent of its styled presentation. 默认 makes the text font
  size one size smaller down to the browser's minimum font size.

- ``<ruby>``, a ruby annotation (CJK 字符的旁注标记, 不是红宝石). 里面包含需要
  注记的文字部分, 以及 rp, rt 等注记 element. rt element 里面的文字会出现在
  它前面的文字部分的上面.

  .. code:: html
    <ruby>
    漢 <rp>(</rp><rt>Kan</rt><rp>)</rp>
    字 <rp>(</rp><rt>ji</rt><rp>)</rp>
    </ruby>

    <ruby>
      明日 <rp>(</rp><rt>Ashita</rt><rp>)</rp>
    </ruby>

- ``<rp>``, ruby parenthesis. fallback parentheses for browsers that do not
  support display of ruby annotations. ``<rp>`` must be positioned immediately
  before or after an ``<rt>`` element.

  the <rp> content provides what should be displayed in order to indicate the
  presence of a ruby annotation, usually parentheses.

  rp element is optional in ruby element.

- ``<rt>``, ruby text. it contains pronunciation of characters presented in a
  ruby annotation.

- ``<time>``, 表达时间. 这个的唯一目的是提供 semantic meaning to time,
  让机器也能轻易找到并理解时间 (通过 datetime attribute).

- ``<wbr>``, a word break opportunity, a position within text where the browser
  may optionally break a line. 这用于段内的 inline break hint. url 等长串字符
  浏览器有时候可能不知如何 break line, 可以通过 wbr element 添加 line break hint.

  注意 wbr & hr 的区别. 前者是 inline break, 不影响整个段的 text flow; 后者
  是 block element, 是强制在该处换行.

- ``<bdi>``, bidirectional isolation. 意思是不去继承 parent 的 dir value,
  使用默认的 auto 值, 让浏览器自动识别里面内容的 direction. 例如用于当一
  部分文字的方向性未知, 需要和周围文字的方向性隔离、并由浏览器自动识别时.

- ``<bdo>``, bidirectional override. override 外部的 dir, 使用指定的 dir
  属性值. 当没有更合适的 tag 来 wrap 要修改的文字部分时, 这比使用 ``<span>``
  在语义上更合适.

- ``<var>``, represents a variable in a mathematical expression or a
  programming context. 这玩意儿看上去超级没用啊, 为啥不用 MathML.

- ``<span>``, 没有任何本征含义, 用于 wrap phrasing content 以形成一个 inline
  division. 方便进行整体操作.

  span 相当于 inline 的 div.

  span 应该在没有其他合适的 semantic elements 的情况下使用.

document edits
^^^^^^^^^^^^^^

- ``<del>``, 表示内容删除. 里面可以是任何的内容, flow content, phrasing content,
  whatever. 都会被 (默认) strike-through. 遵循 transparent content model, 它的
  存在, 不影响其中内容的展示效果, 除了 strike-through 之外.

  所以注意 del 和 ins element 完全不是 inline text element.

  attributes.

  * ``cite``, url for reasoning of deletion.

  * ``datetime``, date and time of deletion.

- ``<ins>``, 表示内容是插入的, 默认以下划线表示. 其他 ditto.

image and multimedia
^^^^^^^^^^^^^^^^^^^^

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

  * ``height``, 图像的高度, in pixels. 如果 height, width 只指定一个,
    另一个自动调整, 以保持图像的原始宽高比.

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

- ``<video>``, video.

  视频源由 src attribute 或者 source elements 指定. 浏览器遍历 source elements
  选择第一个它支持的视频格式.

  video element 里面包含 source, track elements, 以及 fallback 内容. 若
  浏览器不支持 video element, 则显示 fallback 内容.

  attributes.

  * ``autoplay``, 是否自动播放.

  * ``controls``, 默认的 video controls. 一些网站不启用, 而是使用自定义风格
    和功能的控制键. 默认的 controls 就会显示 buffered 情况.

  * ``poster``, poster image.

  * ``src``, video url.

  * ``crossorigin``, 是否使用 CORS 方式获取 poster image, 与 img element 的
    属性相同.

  * ``height``

  * ``width``

  * ``loop``, 播放完后是否 loop back to start.

  * ``muted``, 是否静音.

  * ``preload``, 预加载什么内容.

- ``<audio>``, audio.

  音频源指定与 video element 类似.

  attributes.

  * autoplay, controls, loop, muted, preload, src

  * ``volume``, 0.0 ~ 1.0.

- ``<source>``, 指定资源的源. 常用于对同一个资源提供多个格式的源, 供浏览器选择.
  浏览器通过 ``type`` 属性或资源的 ``Content-Type`` 来确定自己能不能处理这个格式.

  attributes.

  * ``src``, url of resource. required attributes if it's in audio, video elements;
    ignored if it's in picture elements.

  * ``type``, MIME type of the resource.

- ``<track>``, 为 video elements 添加 time-based data, 例如字幕.
  track 必须是 ``.vtt`` file.

  attributes.

  * ``default``, 默认启动这个 track.

  * ``kind``, track 的类型, 即干嘛用的. value: ``subtitles`` (default), ``captions``,
    ``descriptions``, ``chapters``, ``metadata``.

  * ``label``, 这个 track 的名字, 在 controls 中选择 track 时显示它的 label.

  * ``src``, url of track.

  * ``srclang``, 语言.

- ``<map>``, used with <area> elements to define an image map (a clickable link
  area). 好像已经很少使用了.

- ``<area>``, used with map element. defines a hot-spot region on an image, and
  optionally associates it with a hypertext link. 好像已经很少使用了.

table content
^^^^^^^^^^^^^

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

- ``<tfoot>``, 用于放置对各列内容进行总结的列, 例如总计、平均等. 若存在, 必须在
  table 最后.

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
^^^^^

- ``<form>``
  form 里可以有任何 flow content. It's strictly forbidden to nest a form inside
  another form. submit 时 form 里的各层所有 input elements 的值都会一起提交.

  如果一个 form 中需要多个部分, 这些部分一般是通过 ``<section>`` 配合 ``<hN>``
  进行划分. 也可以通过 ``<fieldset>`` 划分.

  在 form submission 时, browser loads the URL where the data was sent, which
  means the browser window navigates with a full page load by ``method``.

  attributes.

  * ``accept-charset``, server 端接受的 character encodings. 默认是
    ``UNKNOWN``, 表示使用与当前文档相同的编码.

  * ``action``, uri where to send form data. form 里的 input/button 的
    ``formaction`` attribute 会 override this.

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
    ``application/x-www-form-urlencoded`` 默认; 若有 file input, 自动变成
    ``multipart/form-data``; ``text/plain``.
    This value can be overridden by a ``formenctype`` attribute on a button/input
    element.

  * ``method``, get/post, lowercased. 若是 get, form data 添加到 action uri 后
    面的 query string 部分然后再 GET.

  * ``novalidate``, 提交时不验证数据. can be overridden by a ``formnovalidate``
    attribute on a button/input element belonging to the form.

  * ``target``, where to display response of submitted request. 其值和 anchor
    element 的 target attribute 一样.
    This value can be overridden by a ``formtarget`` attribute on a
    input/button element.

- ``<fieldset>`` form controls groups.  里面允许是一个 optional legend element
  followed by flow content.

  It's a convenient way to create groups of widgets that share the same
  purpose, for styling and semantic purposes.
  
  Usage:
  
  * 把一组多个 checkbox/radio 放在一个 fieldset 中是很重要的应用.

  * sectioning inside form.

  attributes.

  * ``disabled``

  * ``form``

  * ``name``, name of the group.

- ``<legend>``, title of parent fieldset.

input in general
""""""""""""""""

- ``<label>`` label for a form control.
  
  One form control can be associated with multiple labels. 如果一个 form
  control 没有 label, 应该使用 ``aria-label`` attribute 作为 invisible label.

  you can click the label to activate the corresponding form control.

  attributes.

  * ``for``, id of the labeled element, 该 label 与之关联, 包含点击事件等.
    若 form control 位于 label 内部, for 可以没有.

- ``<input>``

  不同类型的 input element 有不同的验证要求 (以及 pattern attribute 的额外限制),
  若验证不通过, submit 时会提示问题, 无法提交. 并且 input 根据值是否合法, 随时
  有应用 ``:valid`` ``:invalid`` pseudo-class.

  general attributes.

  * ``type``. the holly attribute. 默认是 text.
    可能的类型:
    button, image, submit,
    checkbox, radio,
    color,
    date, time, datetime-local, month, week,
    tel, email, url,
    file,
    hidden,
    number, range,
    text, password,
    reset,
    search,

  * ``autocomplete``, values: on/off 或者是描述该 input 的目的, 以协助浏览器选择
    自动补全的 candidate list.
    若未指定, autocomplete 使用 form owner 的 autocomplete 值.

  * ``inputmode``, 对于使用 virtual keyword 的移动端等浏览器很有用, 提示
    应使用的 keyboard 形式. 例如, numeric, email, etc. 但若可以指定具体的
    合适的 input type, 则不需要指定这个值.

  * ``autofocus``, 页面加载后 autofocus 这个 input.

  * ``checked``, 对于 checkbox 和 radio, 设置默认选中.

  * ``disabled``, 禁用的 form control. 它的值不会 submit 至服务端.
    若没有设置, 会继承 parent element 的 disabled 状态.

  * ``form``, form owner of this form control. id value of that form.
    该属性允许 form control 不在 form 里, 也和 form 关联.

  * ``formaction``, for submit/image type.

  * ``formenctype``, for submit/image type.

  * ``formmethod``, for submit/image type.

  * ``formnovalidate``, for submit/image type.

  * ``formtarget``, for submit/image type.

  * ``list``, id to ``<datalist>`` element, a list of pre-defined options.
    The browser displays only options that are valid values for this input
    element. 此外, 如果 autocomplete attribute 没有禁用的话, datalist 还能
    帮助自动补全.

  * ``min``, for numeric (number, range) or date time (date, time, etc.).

  * ``max``, ditto.

  * ``step``, step from min to max.

  * ``minlength``, minimum number of characters user can enter. for
    text, email, search, password, tel, url.

  * ``maxlength``, ditto. 注意在 input UI 中, 这将限制用户根本不能输入大于
    这个值的字符串, 会自动 truncate.

  * ``multiple``, user can enter more than one value. for email, file.

  * ``name``, 若一个 form 中多个 form control 有相同的 ``name``, 则
    form data 中出现多个 name/value 数据, 且这些数据按 form control 的先后顺序
    而出现. 服务端有义务保持这个数据顺序.

  * ``value``, 注意它是 input 的初始值. form 里实际输入的值也不会更新到这里.
    若没默认值可以不设置.

  * ``pattern``, 在各个 type 的基本格式要求之外, 详细的 validation 要求.  格式
    为 javascript RegExp literal. 使用 ``title`` attribute 添加对 pattern 的输
    入提示.

  * ``placeholder``, 提示用户可输入的内容.

  * ``readonly``, 不同于 disabled. readonly 会 submit 至服务端. disabled 不会.

  * ``required``.

  * ``spellcheck``, 是否检查输入内容的拼写.

  * ``tabindex``, tabbling navigation order.

text input
""""""""""
- ``<input type="text">`` 用于 single-line value, 并且没有更合适的具体类型时.
  If you type text with line breaks, the browser removes those line breaks
  before sending the data.

- ``<input type="email">`` 自动根据 email format 进行验证.

  attributes.

  * ``multiple``, 允许输入多个 email address, separated by commas (and possible
    whitespaces). 此时, ``pattern`` attribute 须对每个值都匹配.

- ``<input type="password">`` the text is obscured so that it cannot be read.
  mobile devices often display the typed character for a moment before obscuring
  it.

  attributes.

  * ``autocomplete``. on: allow autocomplete. off: 对于 password input 浏览器会
    忽略这个值. current-password: 自动补全当前密码, 而不是建议生成新密码.
    new-password: 允许浏览器建议生成新密码, 禁止使用当前密码进行自动补全.

- ``<input type="search">`` 本质上跟 text input 一样, 单独分类是因为浏览器
  可能进行与 text 稍不同的一些处理方式: 一些浏览器在输入框右边设置一个 x;
  浏览器可能保存在不同地方的 search input 的输入, 用于提供 autocomplete.

  ``name`` of search input is often ``q``.

- ``<input type="tel">`` telephone number. 没有 validation 因为 telphone
  在全世界没有统一格式.

  tel input 实际上和 text input 相同, 但是它的作用在于移动设备可根据 tel type
  选择专门的 virtual keyboard; 以及便于进行 css, js 等 manipulation.

- ``<input type="url">`` 支持 absolute url, 还支持 relative url. 需要是合法格式
  的 url.

- ``<input type="number">``

  built-in validation to reject non-numerical entries.
  合法的输入可通过 min, max, step 等进一步限制.

  注意默认情况下 step == 1, 合法输入只能是整数. 调整 step 为小数后, 就可以输入
  floating point number (包含 1.5e3 形式), 但要注意精度与 step 一致.

  number input 不支持 pattern attribute, 理由是反正只能输入 number, 而且 min,
  step, max 已经足够.

  Browser usually provides some buttons to increase or decrease the value of
  the widget.

- ``<textarea>`` multiline plain-text. 许多属性与 input 的相应属性相同.

  它的初始值直接写在 open/closing tag 内部.

  注意 textarea 中, 所有 newline 都是 CRLF 的. 所以后端必须按照业务需要
  进行转换, 不可不加考虑地直接使用.

  textarea only accepts text content. any HTML content put inside is rendered
  as if it was plain text.

  attributes.

  * ``autocomplete``

  * ``autofocus``

  * ``required``

  * ``readonly``

  * ``disabled``

  * ``form``

  * ``minlength``, ``maxlength``

  * ``name``

  * ``placeholder``

  * ``rows``,
    
  * ``cols``, default 20.

  * ``spellcheck``

  * ``wrap``, 如何 wrap text.

    ``hard``: 自动添加 CRLF 以保证每行宽度不大于 cols.
    ``soft``: 不自动添加, 只是保证 linebreaks 都是 CRLF, 这是默认值.

button input
""""""""""""
- ``<input type="button">`` 没有默认行为, 也没有值. 要做什么
  都要靠 js 去定义. 这使得 button input element 可以做任何事,
  而 submit input & reset input 只能做各自确定的事.

  由于现在有 ``<button>`` element, input 的 button 类型不再推荐.
  button element 的优点有: button 上不仅可以是 text, 还可以任何
  其他 element, 而 input button 不行 (因为通过 value attribute
  指定文字).

  由于 button input element 没有任何值的概念, 因此没有 validation.
  submit 时也不会包含在数据里.

  将 label element 与 input element 搭配起来, 用户可以点击 label
  触发 input 的 click 效果, 增加了 input 的响应面积.

  attributes.

  * ``value``, button's label.

- ``<input type="submit">``
  When the click event occurs, the user agent attempts to submit the form.

- ``<input type="reset">`` default click event handler that resets all of the
  inputs in the form to their initial values. 各 input 的初始值可能是 value
  attribute, checked attribute, 等等.

  Normally, from a UX point of view, this is considered bad practice.

- ``<button>``, 里面可以是任何 phrasing content, 不仅是 text. 这让 button
  的形式很灵活 (相对于 button input).

  与相应的 button input 不同, button element 可以带值 (name, value), 并加入
  form data 中.

  attributes.

  * ``autofocus``

  * ``disabled``

  * ``form``

  * ``name``

  * ``value``

  * ``type``, submit (default), reset, button. 与相应类型的 input 类似.

  * formaction, formenctype, formmethod, formnovalidate, formtarget

- ``<input type="image">`` graphical submit buttons. 除了可以提交 form 之外, 和
  img element 的用法基本相同.

  没有 value 值, 因为是 submit button. 但点击时会自动包含 x, y 座标在
  数据中. 这是额外添加的值. 若有 ``name`` attribute, 会作为前缀:
  ``<name>.x``, ``<name>.y``. 座标系的原点在图片左上角.

  attributes.

  * formaction, formenctype, formmethod, formnovalidate, formtarget.

  * ``height``.

  * ``width``.

  * ``src``, image source.

rich input
""""""""""
- ``<input type="file">``

  the real path to the source file is not shown in the input's value attribute
  for obvious security reasons. Instead, the filename is shown, with
  ``C:\fakepath\`` prepended to it.

  attributes.

  * ``accept``, 允许的上传文件类型.
    值为 ``.<ext>``, mime type, ``audio/*``, ``video/*``, ``image/*``.
    可以是一个 list.

  * ``capture``, 从 camera/microphone 之类的地方获取文件.

  * ``multiple``, 从弹出的文件选择窗口中可以 (使用 ctrl) 选择多个文件.
    此时, DOM API ``value`` 值只保存第一个文件. 获取所有文件需要使用
    ``.files`` list (该 list 包含文件的一切信息, 是 file 在 js 中的
    对象封装).

- ``<input type="color">``, color is selected by a visual color picker or
  ``#rrggbb`` (1600 万色) hex format. No alpha channel is allowed.

  color input element 的值是 ``#rrggbb`` string (always lowercase). The value
  is never in any other form, and is never empty.

  A color input's value is considered to be invalid if the user agent is unable
  to convert the user's input into seven-character lower-case hexadecimal
  notation. 任何非法值导致颜色值成为 ``#000000`` 即黑色.

- ``<input type="range">`` 指定一个从 min ~ max 之间的数值, 而这个数值到底
  是多大并不重要. As a rule, if the user is more likely to be interested in the
  percentage of the distance between minimum and maximum values than the actual
  number itself, a range input is a great candidate.

  attributes.

  * ``value``, 默认初始值是 (min+max)/2.

  * ``min``, ``max``, ``step``, 默认值分别是 0, 100, 1.
    step == any 可以指定任意精度.

    设置关联的 datalist element 可以给 range control 加上刻度.

dropdown selection input
""""""""""""""""""""""""
- ``<select>`` select one or more choices from options. 这类似于 radio group
  或 checkbox group.

  它里面是 option/optgroup elements.

  设置 multiple 或 size 后不使用下拉列表, 使用滚动列表.

  attributes.

  * ``autofocus``. Only one form-associated element in a document can have this
    attribute specified.

  * ``disabled``

  * ``form``

  * ``multiple``, 允许选择多个.

  * ``name``

  * ``required``

  * ``size``, 设置滚动列表中可见行数.

- ``<datalist>``, 表示一系列可选的值, 需要配合其他 form control 使用, 设置为
  ``list`` attribute 指向的值. 里面是 zero or more option elements.

- ``<option>``, 只能在 datalist, select 或 optgroup element 中.

  attributes.

  * ``disabled``, 不能选这个选项.

  * ``label``, 与选项 text 一起出现的 label, indicating meaning of the option.

  * ``selected``, 初始选中.

  * ``value``, 单独指定 option 的 value, 以不同于 option text content. 若不设置,
    option value 就是文字内容.

- ``<optgroup>`` option group. 在 select element 中使用. 里面允许 zero or more
  option elements.

  attributes.

  * ``disabled``

  * ``label``, group name.

checkable input
"""""""""""""""
For maximum usability/accessibility, you are advised to surround each list of
related items in a ``<fieldset>``, with a ``<legend>`` providing an overall
description of the list.

- ``<input type="checkbox">``

  checkbox 除了可以处于 checked/unchecked 状态之外, 还可以处于 indeterminate
  状态. Like... a Schrödinger's checkbox... A checkbox in the indeterminate
  state has a horizontal line in the box. (这种状态的 checkbox 在 submit 时
  等价于 unchecked, 不会有数据在 post data 中.)

  注意 checkbox 不仅可以表达单项的选择或不选择; 还可以构建一个 checkbox group,
  进行多选. 此时, 它们的 name 相同, value 不同. form data 中出现多个相同的
  name 对应不同的 value.

  checkbox 的 label 应该在它的右侧.

  attributes.

  * ``value``

    submit form 时, 若有选中 checkbox, 数据中包含 ``name`` 下面的数据是 ``value``
    的值, 若没有设置 value, 默认使用 ``on``; 若没有选中, 数据中根本没有 checkbox
    input 相应的任何信息.

  * ``checked``

- ``<input type="radio">`` 使用时应该有多个 radio input 组成一个 radio group.
  一个 group 内只有一个 radio input 被选中.

  多个 name 相同的 radio input 组成一个 radio group. 在 group 中, 选中一项时
  自动反选其他任何. submit 时, form data 中只包含一项 name value 组合.
  若没有选择任何 radio input, form data 中将不包含 name 项.

  radio 的 label 应该在它的右侧.

  They are called radio buttons because they look and operate in a similar
  manner to the push buttons on old-fashioned radios.

  attributes.

  * ``value``, if omitted, value is ``on``.

  * ``checked``

datetime input
""""""""""""""
- ``<input type="date">``
  let the user enter a date, either using a text box that automatically
  validates the content, or using a special date picker interface.

  其值是 ``yyyy-mm-dd`` 形式, 不包含时间. 注意在 input 中显示的日期格式是
  locale-specific 的, 但保存的值是统一格式的.

  由于不同浏览器对 date, datetime-local, time 等 input element 的实现
  不尽相同, 为保证 cross-browser 一致的用户体验, 不该使用这些 input,
  而是使用 js library 比如 jquery date picker 或者 enter the day, month, and
  year in separate controls.

  attributes.

  * ``min``, ``max``. 因设置范围, 导致部分日期被禁用或者不可选.

- ``<input type="datetime-local">`` date + time, in local timezone.
  各浏览器对这个类型的 input 比 date, time 类型的支持还差.

  其值是 ``yyyy-MM-ddThh:mm`` 格式. 其他与 date input 类似.

- ``<input type="time">``, time only.

  其值是 ``hh:mm[:ss]`` 格式. 是否有秒的部分取决于 step.

  attributes.

  * ``step``. 时间变化步长, 以秒为单位, 默认是 60s. 若 step < 60s, 则
    时间值会包含 ``:ss`` 的部分.

- ``<input type="month">`` 输入 ``yyyy-MM`` 部分. 其他同上.

- ``<input type="week">`` 输入 year + week number.

  其值是 ``yyyy-Www`` 格式.

hidden input
""""""""""""
- ``<input type="hidden">`` include data that cannot be seen or modified by
  users when a form is submitted. 常见的应用场景是 security token (e.g. CSRF token),
  或 object id.

  没有任何方法 (除非修改源代码) 能够在页面上显示 hidden input.

  由于没有可修改的值, 没有 validation.

  attributes.

  * ``value``, 不能修改的数据值.

meter and progress bars
"""""""""""""""""""""""
- ``<meter>``, 包含一个值, 表示它在两个值 (min/max) 之间的程度.

  meter & progress element 本身都不是 form control, 而是配合其他 form control
  的状态指示.

  This is for implementing any kind of meter, for example a bar showing total
  space used on a disk, 再例如做输入密码的强度提示.

  attributes.

  * ``value``

  * ``min``, default 0.

  * ``max``, default 1.

  * ``low``

  * ``high``

  * ``optimum``

- ``<progress>``, 包含一个值, 表示一项任务的完成进度. 注意它的最小值固定是 0.

  This is for implementing anything requiring progress reporting, such as the
  percentage of total files downloaded, or the number of questions filled in on
  a questionnaire.

  attributes.

  * ``max``, default 1.

  * ``value``. 若没有值, progress bar 处于 indeterminate state, 否则是
    determinate state.

- ``<output>``, represents the result of a calculation or user action.

  attributes.

  * ``for``, a list of ids of form controls that contribute to input of
    the calculation.

  * ``name``

interactive elements
^^^^^^^^^^^^^^^^^^^^

- ``<menu>``, 定义一个用于交互的列表.

  注意除了 firefox, edge 目前其他浏览器不支持!!

- ``<menuitem>``, 定义 menu element 中的一项.

  注意除了 firefox, edge 目前其他浏览器不支持!!

- ``<details>``, 可打开可收起的 UI widget, 里面包含 one summary element
  和其他 flow content.

  attributes.

  * ``open``, boolean, 存在则默认是打开.

- ``<summary>``, summary of details element. 在 open/close line 显示.

- ``<dialog>``, a dialog box, inspector, or window. 可以单独使用或者与 form
  配合使用.

  除了 chrome, opera 目前其他浏览器不支持!!

  attributes.

  * ``open``, boolean, 存在则默认出现.

embedded content
^^^^^^^^^^^^^^^^

- ``<iframe>``, 将另一个 html document 嵌入外层的 html document. 这种嵌套构建了
  nested browsing context. 每个 browsing context 有它自己的 session history.

  iframe -- inline frame.

  attributes.

  * ``allowfullscreen``

  * ``height``, in pixel.

  * ``width``, in pixel.

  * ``name``, name of browsing context.

  * ``sandbox``, 设置对 iframe document 的操作限制.

  * ``src``, src url of document.

  * ``srcdoc``, embedded document 的内容. 和 ``sandbox`` 一起使用.

  何时可以使用 iframe? iframe 有哪些问题?

  * iframe 的用处在于展示一个独立于主体的页面. 也就是说, 它的存在应该是作为
    网站的一个 optional part, 而不是网站实现的主要方式: It should never be used
    as an integral part of your site.  例如, 用 iframe 加载一个小的 google map;
    嵌入一个 youtube video; 加载一个外部的静态页面等.

  * 原则: 凡是觉得 "iframe 好像能方便实现这个功能啊" 的时候, 先考虑有没有
    别的更好的选择. Use iframe as last resort.

  * iframe breaks bookmarks & navigation. 除非用脚本获取 iframe src/srcdoc,
    否则用户无法直接获得 iframe 里的 url. 也就是说浏览器无法 bookmark 整个
    页面以保存当前 iframe 的状态 (所指向的链接). 当用户再次打开外部页面的
    url 时, iframe 将被重置. 若 iframe 是网站的重要交互逻辑的组成部分, 则
    用户必须重复很多操作才能恢复到之前的状态, 不能靠 url + cookies 简单地
    保存状态.

  * iframe 提高了 debug 难度. 在 browser devtools 中很容易因为 iframe
    导致的 context 不同造成困惑, 浪费调试时间.

  * 将网站主要部分以 iframe 方式实现可能具有 clickjacking attack 风险.
    因时必须设置 ``X-Frame-Options: SAMEORIGIN`` 或不限制.

  * 一个常见的 iframe abuse 原因是为了在页面分栏的情况下提高加载效率, 只需
    加载一次的部分放在 iframe 外边, 需重复加载的部分放在 iframe 中. 但问题是
    这并没有很大的效率提高 (以至于能抵消它带来的麻烦). 因为 browser 的 local
    cache 会缓存静态文件.

- ``<embed>``, an integration point for an external application or interactive
  content. 这东西曾经用于嵌入视频和 flash 等, 现在基本上没啥用.

- ``<object>``, an external resource, which can be treated as an image, a
  nested browsing context, or a resource to be handled by a plugin. 这东西
  曾经用于 flash, svg 等, 现在基本没啥用.

web components
^^^^^^^^^^^^^^


global attributes
-----------------
- Global attributes are attributes common to all HTML elements; they can be
  used on all elements, though the attributes may have no effect on some
  elements.

  Global attributes may be specified on all HTML elements, even those not
  specified in the standard. That means that any non-standard elements must
  still permit these attributes.

- ``id``, 包含 ASCII letters, digits, ``_``, ``-``, ``.``. Starting with underscore
  or letter, must not contain whitespace. Must be unique in the whole document.

- ``accesskey``, 用于生成 keyboard shortcut for the current element.
  配合浏览器预设的激活键 (Alt, Alt + Shift, etc.) 使用.

  其值是 space separated list of characters. The browser uses the first one
  that exists on the computer keyboard layout.

- ``aria-*``, ARIA attributes, used for improve accessibility.

- ``on<event>``, event handler attributes.

- ``class``, a space-separated list of classes of element.

  class 名字应该按照元素的某种逻辑上、语义上的特质进行分类命名, 而不是
  按照 presentation 形式进行分类命名.

- ``contenteditable``, 是否允许直接编辑 element 的内容. 注意不能手写
  html tag (会被 escape), 这相当于对页面进行 WYSIWYG 式的编辑.

  这是 enumrated attribute, not boolean attribute. 其值必须是
  true/"": editable; false: not editalbe; 不设置该属性: inherited.

- ``contextmenu``, its value is the id of menu element to use as
  a context menu of this element.

  注意除了 firefox 目前没有浏览器支持!!

- ``data-*``, custom data attributes, 允许在 html 代码中保存任意数据, 然后在
  脚本中通过 DOM 来获取.

  标识符 ``*`` 部分不能包含大写字母, 但可以包含 ``-``. 获取数据时, data 标识符
  若包含 ``-``, key 须去掉所有 ``-`` 并将每个 dash 后面第一个字符大写.

  data attributes 的目的是提供一种标准的方式去实现在特定的 html element
  上存储与之相关的数据 (之前没有标准方式实现这个需求). 这些属性没有预定义的含义,
  从而允许自定义使用.

- ``dir``, direction of text in the element. ltr, rtl, auto.

- ``draggable``, whether the element can be dragged.

  enumerated value: true/false/auto. auto if not defined, meaning the behavior
  is the one defined by browser.

  By default, only text selections, images, and links can be dragged. For all
  others elements, the event ondragstart must be set for the drag and drop
  mechanism to work.

- ``hidden``, a Boolean attribute indicating that the element is not yet, or is
  no longer, relevant.

  If it should be hidden from everybody in all contexts, use semantic hidden.
  if it should only be hidden for specific browsing scenarios, use stylistic
  ``display: none`` (or, ``visibility: hidden`` maybe).

- ``lang``, language of the element.

- ``style``, for quick css styling. having the highest priority.

- ``tabindex``, 定义 tab navigation 的顺序.

  负数值表示不能通过 tab focus 到该元素, 一般写成 ``tabindex=-1``.
  0 表示按照元素在源代码中的出现顺序去 navigation, 这是元素的默认值.
  正整数值表示按照该值的递增顺序去 navigation, 若多个元素有相同的
  tabindex 值, 按照源代码顺序决定先后顺序.

  整体的 navigation 顺序是先是正值的 tabindex 元素, 然后是值为 0 的
  tabindex 元素.

- ``title``, containing text representing advisory information for the element.
  Usually displayed as tooltip.

  Use cases: 对元素内容进行描述、解释或补充; 对于文字段落等, 还可作为注释.

  一个元素的 title 会覆盖作用在它和它所以子元素上面, 除非子元素自己有 title.

  对于 link, abbr, input, menuitem 元素, title 属性有额外的语义和作用.

link types
----------

- alternate. alternative stylesheet, or syndication feed, or alternative page
  (例如指向 android app url, 移动端浏览器提示在 app 中打开).

- author. a link to page describing the author.

- bookmark.

- canonical. the "canonical" or "preferred" version of a web page as part of SEO.
  避免搜索引擎重复显示相同内容的不同 url.

- external.

- help. help materials for the element or the whole page.

- icon. 指定显示在 tab 上的 icon. The ``media``, ``type`` and ``sizes``
  attributes allow the browser to select the most appropriate icon for its
  context.

  iOS 的特殊情况要求使用 apple-touch-icon & apple-touch-startup-image.

- license. 指向 license 信息.

- manifest. web app manifest file.

- nofollow. the linked document is not endorsed by the author of this one.

- noopener. open the link without granting the new browsing context access to
  the document that opened it.

- noreferrer.

- pingback.

- prefetch.

- preload. Tells the browser to download a resource because this resource will
  be needed later.

- first, last, prev, next.

- search. the hyperlink references a document whose interface is specially
  designed for searching in this document, or site, and its resources.

  If the type attribute is set to application/opensearchdescription+xml the
  resource is an OpenSearch plugin that can be easily added to the interface of
  some browsers like Firefox or Internet Explorer.

- shortlink.

- stylesheet. 就是 stylesheet, type 若没设置默认是 text/css.

- tag.

accessibility
-------------

- 理想情况下, 网站实现时须应用 accessibility features, 使得具有视力障碍的人也能
  通过 screen reader 了解网站内容.

css
===

type of stylesheets
-------------------

- persistent, link element 中没有 ``rel="alternate"`` 以及 ``title=``.
  这种总是应用.

- prefered, link element 中没有 ``rel="alternate"`` 但有 ``title=``.
  这种默认使用. prefered stylesheet 只能有一个.

- alternate, link element 有 ``rel="alternate"`` 和 ``title=``.
  这种默认不使用, 用户可以通过浏览器提供的方式选择使用.

  alternate stylesheet 通过 ``rel="alternate stylesheet"`` link element
  定义. 用户可选择不同的 css 文件应用不同的页面风格. alternate stylesheet
  需要定义 ``title=`` 作为选择的名字. Style sheets linked with the same title
  are part of the same choice.

syntax
------

statement
^^^^^^^^^
- a css statement begins with any non-space characters and ends at the first
  closing brace or semi-colon.

- 一个 css 文件由多个 css statement 构成.

- css statement 包含两类: at-rules & rulesets.

ruleset
^^^^^^^
- ruleset 的作用是给 html 元素设置样式和布局.

- 一个 css ruleset (or simply rule) 由 a group of selectors + declaration block
  构成.

  * selector group:
    a selector group 由 a comma separated list of selectors 构成. selectors are
    case-sensitive.
  
  * declaration block:
    一个 declaration block 整体由一组 braces 包裹, 里面包含 0 或多个 declarations,
    由 semicolon 分隔. 最后一个 declaration 理论上没必要以 semicolon 结尾.
  
  * declaration:
    一个 declaration 由 property + value 构成. property 和 value 以 colon 分隔.
    property & value are case-insensitive.

property
^^^^^^^^

shorthand property
""""""""""""""""""
a css property that let you set the values of several
other css properties simultaneously. This is to make css declarations more
concise and readable.

* 在 shorthand property 中, 对于未设置值的子项, 将自动设置值为它的 initial value.
  这意味着, 对于在 shorthand property 中省略的子项, 并不是自动使用了其他地方设置
  的值, 而是设置了一个新值为 initial. 这个值是否最终会生效, 仍然要靠 cascade,
  specificity, inheritance 等算法计算给出结果.

* shorthand property 在参与 cascade/specificity/inheritance 等计算时, 会先拆成它
  所代表的各项属性后才输入的.

* shorthand property 中的子项的值不能是 inherit/initial, 只能说整体属性的值是
  inherit/initial.

* 当 shorthand property 中的各项值的类型不同时, 子项值的书写顺序并不重要, 解析
  时会自动识别值与属性的对应关系. 但对于各项值的类型相同时, 子项值的位置具有
  重要性.

  - 与 box 四边相关的属性, 可以指定 1-4 个值. 赋值是从 top 开始顺时针进行的.

    * 一个值 (top, right, bottom, left): 1, 1, 1, 1.

    * 两个值: 1, 2, 1, 2 (未指定的对边相同).

    * 三个值: 1, 2, 3, 2 (未指定的对边相同).

    * 四个值: 1, 2, 3, 4.

  - 与 box 四角相关的属性, 可以指定 1-4 个值. 赋值是从左上角开始顺时针进行的.

    * 一个值 (LT, RT, RB, LB): 1, 1, 1, 1.

    * 两个值: 1, 2, 1, 2.

    * 三个值: 1, 2, 3, 2.

    * 四个值: 1, 2, 3, 4.

  - ``font`` shorthand property 在指定 font-size & line-height 时使用
    ``<font-size>/<line-height>`` 形式.

at-rules
^^^^^^^^
- 与 ruleset 相比, at-rules 的作用是 instruct how CSS behaves. 也就是说, 
  ruleset statement 是控制 HTML 样式的, at-rule statement 是控制 CSS 逻辑的.

- starts with an at sign, followed by an identifier and then continuing up to
  the next semi-colon outside of a block or the end of the next block.

- 若 at-rule 后面是 block, 可能里面是一系列 descriptor/value pairs, 也可能是
  别的.

- 一些 at-rule 可以 nested, 即构成 nested at-rules.

comment
^^^^^^^
- c-style ``/* */``.

property value
^^^^^^^^^^^^^^
value definition syntax
""""""""""""""""""""""""

类似 BNF notation, 用于定义 property 的允许值.

* value types.

  - keywords. a word with a predefined meaning that appears literally,
    without quotation marks.

    所有 css properties 都支持 inherit, initial, unset 三个 keyword values.

  - literals. ``/``, ``,`` 等在 value 中 literally 出现的字符.

  - data types.

    * basic data types.

    * non-terminal data types.

* value combinators.

  - brackets ``[]``.

  - juxtaposition ``' '``. Placing several keywords, literals or data types,
    next to one another, only separated by one or several spaces. All
    juxtaposed components are mandatory and should appear in the exact order.

  - double ampersand ``&&``. the components are mandatory but may appear in any order.

  - double bar ``||``. at least one of the components must be present, and they may
    appear in any order.

  - single bar ``|``. exactly one of these options must be present.


* value multipliers.

  - no multiplier. exactly 1.

  - asterisk ``*``. 0 or more.

  - plus ``+``. one or more.

  - hash mark ``#``. one or more, separated by comma.

  - question mark ``?``. 0 or 1.

  - curly braces ``{A,B}``. at least A, at most B times.

  - exclamation point ``!`` (after the brackets group). the group is
    required, and must produce at least one value; even if the grammar of the
    items within the group would otherwise allow the entire contents to be
    omitted.

* precedences.

  - value multipliers have precedence over all value combinators.

  - Juxtaposition has precedence over the double ampersand. e.g.,
  ``bold thin && <length>`` equals to ``[ bold thin ] && <length>``.

  - The double ampersand has precedence over the double bar. e.g.,
  ``bold || thin && <length>`` is equivalent to ``bold || [ thin && <length> ]``.

  - the double bar has precedence over the single bar, meaning that
    ``bold | thin || <length>`` is equivalent to ``bold | [ thin || <length> ]``.

property value types
""""""""""""""""""""

* initial value. a property's default value, as listed in its definition table.
  对于任何元素, 可以通过 ``initial`` keyword 明确指定使用 initial value.

* specified value. the value it receives from the document's style sheet.
  就是经过 cascade/specificity/inheritance 等算法后得到的最终定义数值.
  注意这组数值是根据各 css declaration 得到的最终定义值, 还不是最终使用值.

  注意一个 css property 的 specified value 仍然是它定义中允许的任何值. 这
  与 computed value 不同.

* computed value. 根据 specified value 进行计算, 解析 inherit, initial,
  unset, revert 等特殊值至具体的值, 将所有 specified value 转换成属性定义
  允许的 computed value.

  The computed value of a CSS property is the value that is transferred from
  parent to child during inheritance. 这是 computed value & specified value
  & used value 的重要区别.

* used value. 这些值是从将 computed value 再解析成绝对数值可直接在页面中使用
  以确定各元素布局和位置等等绝对信息的值.

  注意 used value 这里已经是绝对值, 由于绝对值很多时候不适合去继承, 所以有
  computed value & used value 的区分.

  computed value & used value 只有当该属性与 layout 相关时才可能有区别.
  这是因为, computed value 可以是百分数等相对值, 而 used value 需要根据
  layout 去解析成绝对值. 除此之外, 两个值是相同的. 事实上, DOM API
  ``getComputedStyle()`` 会返回绝对数值, 即根据属性不同可能返回的是 computed
  value 或 used value. 所以从这个角度看, 两个值在实现中就是一个.

* actual value. the used value of that property after any necessary
  approximations have been applied by user agent. 这些值是最终浏览器使用的值,
  在考虑到具体环境的局限性等因素后的完全真实值.

replaced & non-replaced elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* replaced element 是具有 intrinsic dimension 的元素. 它的意思是这些元素的内容
  具有本征的长宽等尺寸 (这些内容替换了 tag 本身, 故命名 replaced). 这些尺寸不受
  css 控制.

  常见 replaced elements:
  iframe, video, embed, img, ``<input type="image">``;
  content property value: anonymous replaced elements;
  一些情况下的 audio, canvas, object, applet.

selectors
---------

任何一种 basic selector 可以单独出现. 而 pseudo-class, pseudo-element 等
按逻辑显然必须依附于一定的 basic selectors.

basic selectors
^^^^^^^^^^^^^^^
- universal selector. ``*``

  添加 css namespace 后, 成为:
  ``ns|*`` (in specified namespace),
  ``*|*`` (in any namespace),
  ``|*`` (匹配所有没有 namespace 的元素).

  除了给所有元素设置基准属性之外, 还可以有别的用处. 例如, 与 combinators 一起
  使用: ``.floating + *``.

- type selector. ``element-name``

- class selector. ``.class``

- id selector. ``#id``

- attribute selector.

  * ``[attr]``, match when attr is present.

  * ``[attr=value]``, value of attr is exactly ``value``.

  * ``[attr~=value]``, attr whose value is a whitespace-separated list of
    words, one of which is exactly value.

  * ``[attr|=value]``, attr whose value can be exactly value or can begin with
    value immediately followed by a hyphen. It is often used for language
    subcode matches.

  * ``[attr^=value]``, attr whose value is prefixed by value.

  * ``[attr$=value]``, attr whose value is suffixed by value.

  * ``[attr*=value]``, attr whose value contains at least one occurrence of
    value within the string.

  * ``[attr operator value i|I]``, any above but case-insensitive.

combinators
^^^^^^^^^^^

- child combinator. ``a > b``

- descendant combinator. ``a b``

- adjacent sibling combinator. ``a + b``

- general sibling combinator. ``a ~ b``

pseudo-classes
^^^^^^^^^^^^^^
- 作用: 在 selector 后面加上 ``:<...>``, 用于在已经选定的元素中进一步只选择
  它的某个子状态.

  关键字是状态.

- 一个 selector 中可以出现多个 pseudo-classes.

link status
"""""""""""
- ``:link``. match every ``<a>`` element that has a href attribute. 也就是说
  是个真正的 link 的 anchor element.
  (实际上还匹配同样的 ``<area>`` & ``<link>`` elements, 但这没用啊.)

  所以作为 selector, ``a`` & ``a:link`` 的区别是, 前者匹配所有 a tag, 后者
  只匹配有 href 的那些. 前者适合指定对对所有 a tag 都生效的基本属性, 例如
  text-decoration, font-family, etc. 后者的话, 则是对那些进行区别.

  当指定 anchor 的不同状态的样式时, 按照 LVHFA 顺序可获得正确的结果, 即
  ``:link``, ``:visited``, ``:hover``, ``:focus``, ``:active``.
  LVHFA -- Lord Vader's Handler Former Anakin.

- ``:visited``, match links that are visited.

  For privacy reasons, browsers strictly limit which styles you can apply using
  this pseudo-class, and how they can be used.

  Properties that would otherwise have no color or be transparent cannot be
  modified with :visited. Thus, if you want to modify the other properties,
  you'll need to give them a base value outside the :visited selector.

selection status
""""""""""""""""
- ``:hover``, match an element when pointing device is hovering upon it.
  注意是对任何元素都可用.

- ``:focus``, match when an element receives focus. 注意这个和 :active 不同.
  It is generally triggered when the user clicks or taps on an element or
  selects it with the keyboard's "tab" key. 例如常用于 form controls.

- ``:active``, match an element when it's being activated by pointing device.

validation status
""""""""""""""""""
- ``:valid``

- ``:invalid``

- ``:required``

- ``:optional``

- ``:in-range``

- ``:out-of-range``

pseudo-elements
^^^^^^^^^^^^^^^
- 作用: 在 selector 后附加 ``::<...>`` 语法, 用于在已经选定的元素中进一步限定
  只选择它的某个子部分.

  关键字是部分.

- 一个 selector 中只能出现一个 pseudo-element. 且必须位于所有 basic selectors
  之后.

- ``::before``
  creates a pseudo-element as the first child of the selected elements.
  The created element is inline by default.

  该 selector 对应的 declaration block 就是在对这个 created element 进行 styling.

- ``::after``
  与 ``::before`` 类似, 对应地创建最后一个子元素.

- ``::first-letter``, match first letter of the first line of a block element.
  注意它不能随便用在所有元素上以期待它能匹配该元素内的第一个字符. 它必须应用在
  block-level element 上.

- ``::first-line``, match first line of a block element.
  与 ``::first-letter`` 类似, 它必须应用在 block-level element 上.

- ``::selection``, match the part of text selected by user.

cascade, specificity, inheritance
---------------------------------

when to put css definitions at element-inline, document-level, external, etc.?



最终决定一套生效的 css 规则的基本流程:

1. 首先应用 cascade algorithm.

2. 结果中优先级相同的通过 specificity algorithm 进一步筛选.

3. 结果中再有具体性相同的, 通过定义顺序筛选.

4. 对于没有直接指定值的属性, 若是 inherited property, 从 parent element
   继承值或对于 root element 使用初始值; 若是 non-inherited property,
   使用初始值.

cascade
^^^^^^^

- cascade 是通过 css 定义的重要性和来源进行筛选的算法.

- cascading 只对 css declarations 有效. 这包括单纯的 ruleset 和 at-rule
  包裹的 nested statement.

- css 定义的三个来源: user-agent stylesheet, author stylesheet, user stylesheet.

- cascading procedure:

  1. 从三种定义源获取 css 定义, 对任意一个 element, 保留对它能够生效的那些
     css 规则 (通过考虑 selectors 以及 at-rules).

  2. 首先根据规则的 importance (``!important``) 然后根据规则的来源进行优先级
     排序.

     - 对于 important ruleset, 来源的优先级顺序 (依次递减):
       user-agent, user, author.

     - 对于 normal ruleset, 来源的优先级顺序 (依次递减):
       author, user, user-agent.

     注意对于 important ruleset 的来源优先级和普通的是相反的. 这是为了让本地
     端 have last say on what styles appear on my browser.

  3. 对于 cascading 后处于同优先级的 ruleset, 通过 specificity 来进一步选择.
     注意, 如果在 cascading 阶段就被排除 (重要性和来源), 你再多的具体性也没用.

- considerations on ``!important``

  * Always look for a way to use specificity before even considering ``!important``

  * Only use ``!important`` on page-specific CSS that overrides foreign CSS.

  * Never use ``!important`` when you're writing a plugin/mashup.

  * Never use ``!important`` on site-wide CSS.

  * 一些不得不使用 ``!important`` 的情况:

    - 某些你无法控制的外部插件使用 inline styles on elements 来强制一些样式.
      此时只能通过在 page-specific 或 site-wide css 中设置针对的 important
      rule.

specificity
^^^^^^^^^^^

- specificity 定义一个 css declaration 的权重.

- 非直接定义的 css declaration (即继承来的定义) 的 specificity 低于任何直接定义的
  css declaration. 无论它本身的 selector 定义的 specificity 如何.

- specificity 由四组数字构成, ``N.N.N.N``, 对应 specificity 由高至低.
  它们的值分别由以下四类定义贡献:

  1. inline style

  2. ID selector

  3. class selector, attribute selector, pseudo-class

  4. type selector, pseudo-element

  对于每个类型, 在 selector 中 (除了 inline) 每出现一次, 相应位置的数值加一.

- Universal selector (``*``), combinators (``+``, ``>``, ``~``, ``' '``)
  and negation pseudo-class (``:not()``) have no effect on specificity.

- selectors in ``:not()`` do have effect on specificity.

- The tree proximity of an element to other elements that are referenced in a
  given selector has no impact on specificity. e.g., ``body h1`` vs ``html h1``
  是相同的 specificity.

- css 定义无论是在 html 代码嵌入的 style element, 还是 link element 引用的
  完整 css stylesheet 文件, ``@import`` at-rule 导入的文件等等, 都不影响它
  的 specificity. 它们只影响规则的导入顺序, 从而在 speicificity 相同时, 根据
  先后顺序决定使用哪个规则.

inheritance
^^^^^^^^^^^

- 属性分为两类: inherited property & non-inherited property.

  * inherited property. 对于这种属性, 当某个元素上没有通过任何 css declaration
    指定该属性的值时, 该属性值为 computed value of that property on its parent
    element. 对于 root element, inherited property 的值为该属性的 initial value.

    e.g., color.

  * non-inherited property. 对于这种属性, 当某个元素上没有通过任何 css declaration
    指定该属性的值时, 该属性值为它的 initial value.

    e.g., border-style.

- 无论 inherited or non-inherited property, 都可以指定 value 为 ``inherit`` 来
  明确要求继承 parent element value.


box model
---------
- 每个 html element 都是由一个 invisible box 包裹起来的.

- A box has 4 parts:

  * content area. bounded by content edges.
    html 元素内的的所有内容全都在 content area 中.
  
  * padding area. between content edges and padding edges.
    box background 覆盖 content area + padding area.
  
  * border area. between padding edges and border edges.
  
  * margin area. between border edges and margin edges.
    元素之间的分隔区域. 实际效果与 margin collapsing 有关.

- 对于 non-replaced inline elements, 所占据的高度由 parent block-level element
  的 line-height property 决定, 而不论元素本身的 height 以及 padding, border,
  margin 的高度部分设置的值是什么.

- 当 ``box-sizing`` property 为 ``content-box`` 时, 各种 box width 和 height 属
  性限制的都是 content area 的宽度和高度; ``border-box`` 时, 这些属性限制的是
  content + padding + border 部分的宽度和高度.

margin collapsing
^^^^^^^^^^^^^^^^^
A behavior when the margin of adjacent blocks are combined into a single
margin whose size is determined based on the following conditions:

* for both positive margins, use the largest of the two.

* for one positive and one negative margins, the size of the collapsed margin
  is the sum of the largest positive margin and the smallest (most negative)
  negative margin.

* When both margins are negative, the size of the collapsed margin is the
  smallest (most negative) margin.

three types of margin collapsing:

- adjacent siblings. Margins of adjacent block-level elements are collapsed.

- parent and first/last child. 如果 parent block element 的 top margin 和它
  的第一个 child block element 的 top margin 之间, 或者 parent block element 的
  bottom margin 和它的最后一个 child block element 的 bottom margin 之间, 没有
  任何东西隔在中间, 则这两个元素的相应 margin 会 collapse 在一起. 合并的 margin
  在 parent element 的外边.

- empty element. 对于一个 empty block element, 如果它的 top margin 和 bottom
  margin 之间没有任何东西隔在中间 (border, padding, inline part, block
  formatting context created, or clearance), 则它的 top/bottom margins 会合成一
  个.

注意:

- margin collapsing 只发生在 block elements 之间. inline elements 的 margins
  从不 collapse, 按照指定的值放置.

- floated elements & absolutely positioned elements 不参与 margin collapsing.
  因此实际中 margin collapsing 只会发生在 top/bottom margin 之间.

自动计算属性
^^^^^^^^^^^^
对于 non-float block element, margin edge 一定会覆盖整行. 它的 left, right 
margin 根据 width, padding, border 等方面的属性值的设置综合计算得到.

margin box
^^^^^^^^^^
- negative margin. 在不考虑 margin collapsing 的情况下, 若某个元素有 negative
  margin,

  * it will pull the adjacent element's margin box inwards.

  * 若该元素是 first/last child of its parent element, it pushes the element's
    border box into parent element's padding area. 因为一定是 margin box 与
    parent element 的 content box 衔接.

properties
""""""""""
- margin-top.

  non-inherited.

  initial value: 0.

  specified value:

  * ``<length>``

  * ``<percentage>``
    relative to the width of the containing block.

  * auto.
    The browser selects a suitable margin to use.

- margin-right.

- margin-bottom.

- margin-left.

- margin.
  shorthand for all above.

  对于 non-float block element, 为了将元素占满整行, 会自动设置合适的 margin
  进行填充. 此时 margin-left, margin-right 只具有参考意义.

  任意一个或多个方向的 margin 设置 auto 时, 由浏览器决定如何设置相应的 margin.
  当相对的两个 margin 都是 auto 时, 会给这两个 margin 设置相等的数值. 这可以用于
  将 block element 的 border area 在 containing block 中水平居中 (对于 inline
  element, 不占据一整行, 没有所谓居中. 但可以 text-align 为 center).
  在竖直方向, 由于 block element 没有占据尽可能多的 vertical space 的要求, 因此
  margin-top/bottom 设置 auto 只会让相应 margin 为 0.

  更方便的元素水平和竖直居中问题, 使用 flexbox 解决.

Positioned Layout
-----------------
- A CSS module that defines how to position elements on the page.

type of positioning
^^^^^^^^^^^^^^^^^^^
- A static element.

  * positioned according to document flow.
  
  * ``static`` element can not be positioned.

  * top/bottom/left/right/z-index have no effect.

- A positioned element is one whose ``position`` is computed to be anything
  other than ``static``.  

  * positioned according to document flow.

  * left/right/top/bottom/z-index 属性只对 positioned element 有用.

- relatively positioned element:

  * computed position is ``relative``.

  * The element's original position according to document flow is kept.

  * left/right/top/bottom is relative to the element's normal position.

  * The offset does not affect the position of any other elements.

  * This creates a new stacking context when the value of ``z-index`` is not
    auto.

- absolutely positioned element:

  * computed position is ``absolute`` or ``fixed``.

  * The element is removed from the normal document flow, and no space is
    created for the element in the page layout.

  * left/right/top/bottom is relative to the element's containing block.

  * For ``absolute``, the element's containing block is its parent containing
    block. For ``fixed``, the element's containing block is initial containing
    block.

  * non-replaced, absolutely positioned element can be made to fill the
    available horizontal/vertical space, by setting left and right, or top and
    bottom, and leaving width/height to auto.

  * ``absolute`` element creates a new stacking context when the value of
    z-index is not auto. ``fixed`` element always creates a new stacking
    context.

  * The margin of ``absolute`` element do not collapse with other margins.

  * The display of absolutely positioned element can not be ``inline`` or
    ``inline-block``.

- stickily positioned element:

  * computed position is ``sticky``.

  * This is a mix of relative positioning and fixed positioning.

  * left/right/top/bottom is relative to initial containing block.
    
  * Normally the element is positioned as a relatively positioned element with
    0 offset at all sides. 当 scroll 时, 如果 element 与 initial containing
    block 的距离小于指定的 left/right/top/bottom, 则变为 fixed position, until
    it reaches the boundary of its containing block.

  * Sticky element always creates a new stacking context.

  * Usage. sticky element can be used for header bar, navigation, etc.

value precedence
^^^^^^^^^^^^^^^^

- When both ``top`` and ``bottom`` are not auto, ``top`` prevails.

- When both ``left`` and ``right`` are not auto, ``left`` prevails if
  ``direction`` property is ``ltr``; otherwise ``right`` prevails.

properties
^^^^^^^^^^
- position. ``position`` defines how the element is positioned in a document.
  It determines how left/right/top/bottom properties are interpreted.

  initial: static.

  specified values: static/relative/absolute/fixed/sticky.

- z-index. specify the z-axis order of the positioned elements, when they
  overlap each other. The element with higher z-index generally covers a lower
  one.

  ``z-index`` only works for an element with ``position`` other than ``static``.

Flexbox Layout
--------------

overview
^^^^^^^^
- flexible box layout, providing a more efficient way to lay out, align and
  distribute space among items in a container, even when their size is unknown
  and/or dynamic.

- Main idea: give the container the ability to alter its items' width/height
  (and order) to best fill the available space.

- flexbox layout 中, 不存在对 vertical and horizontal direction 在意义上的区分.
  两个方向是同质的, 可相互转换. 而在传统 layout 中, vertical 为 block element
  排列的方向, horizontal 为 inline element 排列的方向.

concepts
^^^^^^^^

- For a complete flexbox layout, some properties are set to flex container,
  some properties are set to flex items.

- the flex layout is based on the flex-flow direction.

- main axis. the primary axis along which flex items are laid out. It's
  determined by ``flex-direction``.

- main-start, main-end. main axis 的起始端和结束端. items are placed from
  starting side to ending side.

- main size. flex item's dimension on main axis's direction. could be its
  width or height.

- cross axis. the axis perpendicular to the main axis.

- cross-start, cross-end. cross axis 的起始端和结束端. lines of flex items
  are placed from starting side to ending side of cross axis.

- cross size. flex item's dimension on cross axis's direction.

working with margin
^^^^^^^^^^^^^^^^^^^
- When auto margins are applied to a flex item, it will automatically extend
  its specified margin to occupy the extra space in the flex container,
  depending on the direction in which the auto-margin is applied.

  See also: [FlexMarginAuto]_

- If you don’t specify a direction, simply applying ``margin: auto``, a flex
  item would evenly distribute any extra space on either side of the itself
  equally.

flex container properties
^^^^^^^^^^^^^^^^^^^^^^^^^
- ``display`` must be ``flex``.

- flex-direction. defines the main axis's orientation and its direction.

  specified values:

  * row.

  * row-reverse.

  * column.

  * column-reverse.

- flex-wrap. defines whether flex items should wrap into multiple flex
  lines if they don't fit in oneline.

  specified values:

  * nowrap

  * wrap

  * wrap-reverse.

- flex-flow. shorthand for flex-direction and flex-wrap.

- justify-content. items' alignment along the main axis. This is achieved by
  distributing extra free space left over when either all the flex items on a
  line are inflexible, or are flexible but have reached their maximum size.

  specified values:

  * flex-start

  * flex-end

  * center

  * space-between. items are evenly distributed along main axis. The spacing
    between each pair of adjacent items is the same. *The first item is flush
    with the main-start edge, and the last item is flush with the main-end
    edge* (所以如果只有一个 item, 将位于 main-start edge).

  * space-around

  * space-evenly

- align-items. On a flex line, this determines the alignment of flex items in
  cross axis direction.

  specified values:

  * normal. For flex items, behaves like ``stretch``.

  * flex-start

  * flex-end

  * center

  * baseline

  * stretch

  initial value: normal.

- align-content. 决定多个 flex line 在 cross axis 方向上, 如何去布局. 如果只有
  一行 flex items 则没有效果.

  * flex-start

  * flex-end

  * center

  * space-between

  * space-around

  * stretch

flex item properties
^^^^^^^^^^^^^^^^^^^^
- ``display``. 注意 flex item 的 ``display`` 可以是任何值, 并没有限制. 最终效果
  由 display, flex, width/height 等属性联合决定.

- order. By default, flex items are laid out in the source order. This
  redefines the order in which they appear in the flex container.

- flex-grow. the ability for a flex item to grow and take remaining spaces if
  necessary. It accepts a unitless value that serves as a proportion relative
  to other flex item's flex-grow value.

  specified value: ``<number>``

  initial value: 0. meaning do not grow.

- flex-shrink. the ability for a flex item to shrink if necessary.

- flex-basis. the default size of an element before the remaining space is
  distributed.

  specified values:

  * auto. default size is determined by the element's width and height property.

- flex. shorthand for flex-grow, flex-shrink and flex-basis.

  specified values:

  * none. equals to 0 0 auto.

  * 1 value:
    
    - a unitless number, interpreted as flex-grow;

    - any valid value for flex-basis;

  * 2 values: first value is for flex-grow; second value is for flex-shrink if
    it is unitless number, or for flex-basis if it is valid value for that.

  * 3 values: for 3 properties respectively.

- align-self. override this item's alignment at cross axis direction as defined
  by ``align-items``.

  specified values:

  * auto 
   
  * flex-start 
   
  * flex-end 
   
  * center 
   
  * baseline 
   
  * stretch


transition
----------
- CSS transition provides a way to control transitioning between old value and
  new value when changing CSS properties.

- 对于 transition, 每次 transition-property 覆盖到的属性值改变时, 都会进行相应
  的 transition effect.

- 当需要使用 JS 改变元素的一些属性时, 配合 transition effect 会让效果更顺畅. 

properties
^^^^^^^^^^
对于控制 transition 的各个属性, 如果 accepts a list of values, 这些值是循环应用
到每个 transition-property 指定的属性上面.

- transition-property. Specify properties to be transitioned. If you specify a
  shorthand property, all of its longhand sub-properties that can be animated
  will be.

  non-inherited.

  initial: none.

  specified values:

  * none. no transition.

  * all.

  * a list of ``<custom-ident>``, each of which specifies a property name.

- transition-duration. transition time.

  non-inherited.

  initial: 0s.

  specified values: a comma separated list of followings

  * ``<time>``

- transition-timing-function. see also animation-timing-function.

  non-inherited.

  initial value: ease.

  specified value: a comma separated list of followings

  * ``<timing-function>``

- transition-delay. time to delay before starting transitioning.

  non-inherited.

  initial: 0s.

  specified values: a comma separated list of followings

  * ``<time>``. see also animation-delay.

- transition. shorthand for all above.

  specified value: a comma separated list of transition configs,
  each for a single property.

  Each transition config can be a combination of above property
  values. For two time values, the first is duration, the second
  is delay.

animation
---------
overview
^^^^^^^^
- Used for animate the transition process of CSS style configuration.

- A CSS animation definition consists of two parts:

  * a style describing the CSS animation, with ``animation``-related
    properties.

  * a set of ``@keyframes`` that indicate the start, intermediate waypoints
    and end states of the animation's style.

- advantages over JS-based animation.

  * better performance.

keyframes
^^^^^^^^^
- Each keyframe describes how the animated element should render at a given
  time during the animation sequence.

- The timing is specified as a ``<percentage>``. Two special timing point.

  * 0%, from. the start of the animation.

  * 100%, to. the end of the animation.

  If from/0% or to/100% is not specified, the browser starts or finishes the
  animation using the computed values of all attributes.

properties
^^^^^^^^^^
对于控制 animation 执行的各个属性, 如果 accepts a list of values, 这些值
是循环应用到每个 animation-name 指定的动画效果上的.

- animation-name. The name of the animation to be applied.

  initial value: none.

  non-inherited property.

  specified values:

  * none. no keyframes. deactivate an animation.

  * a comma separated list of ``<custom-ident>``. 也就是说可以同时应用多个
    animation.

- animation-duration. The period of one animation.

  non-inherited.

  initial value: 0s.

  specified value.

  * a comma separated list of ``<time>``. units can be seconds or milliseconds.

- animation-timing-function. A function of the form ``x = f(t)``, where ``t``
  is the timing ratio in ``[0, 1]``, ``x`` is the property value ratio in
  ``[0, 1]``. 该函数定义 animated css property 的值如何随时间变化.

  该属性可以应用在整个 animation 的过程中, 或者只局限于从某个 keyframe 开始
  的一系列 keyframes. A keyframe's timing function is applied from the keyframe
  on which it is specified until the next keyframe specifying that property, or
  until the end of the animation.

  non-inherited.

  initial value: ease

  specified value:

  * a comma separated list of ``<timing-function>``

- animation-delay. when an animation should start.

  non-inherited.

  initial value: 0s.

  specified value:

  * a comma separated list of ``<time>``.
    
    A positive value indicates that the animation should begin after the
    specified amount of time has elapsed.

    0s means starting immediately.

    A negative value causes the animation to begin immediately, but partway
    through its cycle. 注意这个负值是取在 animation 的整个过程中的时间点,
    这包含 animation-duration and animation-iteration-count.

- animation-iteration-count. The number of times the animation should be
  played.

  non-inherited.

  initial: 1.

  specified value: a comma separated list of followings

  * infinite.

  * ``<number>``. specify non-integer values to play part of an animation cycle.

- animation-direction. an animation should play forwards or backwards. 这指的是
  animation 的各帧是正着放还是倒着放.

  non-inherited.

  initial: normal.

  specified value: a comma separated list of followings

  * normal. plays forwards during each cycle. After each cycle, the animation
    will reset to the beginning state and start over again.

  * reverse. plays backwards during each cycle. After each cycle, the animation
    will reset to the end state and start over again.  Animation steps and
    timing functions are both reversed.

  * alternate. 交替方向. 第一次正向.

  * alternate-reverse. 交替方向. 第一次反向.

- animation-fill-mode. element 在 animation 开始之前和结束之后是否保持
  animation 过程中设置的 styles 以及如何保持.

  non-inherited.

  initial: none.

  specified value: a comma separated list of followings

  * forwards. The target will retain the computed values set by the last
    keyframe encountered during execution.

  * backwards. The animation will apply the values defined in the first
    relevant keyframe as soon as it is applied to the target, and retain this
    during the animation-delay period.

  * both. both forwards and backwards.

- animation-play-state. Specify whether an animation is running or paused.
  修改该属性就可以 pause/resume animation.

  initial: running.

  specified value: a comma separated list of followings

  * running

  * paused.

- animation. shorthand for all above.

  specified value: a comma separated list of animation configs.

  each animation configs is a space separated list of:

  * 0 or 1 occurrences of all animation longhand properties.

  若有 2 个 ``<time>`` value, 第一个赋值给 animation-duration, 第二个
  赋值给 animation-delay.

transition vs animation
-----------------------
See also [TransitionVSAnimation]_

- trigger.

  * A transition is triggered 当指定的 property 的值通过某种机制发生了改变.
    无论是 pseudo-class state, or via JS code. 也就是说, transition needs a
    trigger to run.

  * An animation doesn't need a trigger to run. They can run automatically
    after page load.

- state specification.

  * transition 只能定义两个状态: 即初态和终态. 过程由 UA 根据其他参数自动计算生
    成. 这样, transition 适合比较简单的动画效果.

  * animation 可以指定任意数目的中间态. 因此会灵活许多.

- execution direction.

  * transition 只有一个方向. 从 old state to new state. 以及 possibly 在一些情
    况下还会发生从 new state reversely to old state. 但这本质是一回事.

  * animation 可以配置执行方向, 以及执行次数等等.

- usage.

  * 在实际中, 很多时候只需要简单的动画效果, 涉及两个状态及一个 trigger, 此时
    transition 足够了. 只有需要更加复杂灵活的效果时, 才需要 animation.

  * Reach for transitions first and reach for CSS animations when you want to
    create something you can’t create with transitions alone.

properties
----------

text
^^^^^
- color. 负责元素的 text content and text decoration 部分的颜色.

  specified value 是 a value of ``<color>`` data type.
  inherited property. computed value 是 ``rgb()`` or ``rgba()``.

  keyword 颜色值 ``currentColor`` 指的就是当前元素的 color 属性值. (无论 css 中
  是否有明确的 color 属性定义, 浏览器一定会通过 css 算法给每个元素确定一个 color
  值, 所以 currentColor 总是存在的.)

- font-family. a priorized, comma-separated list of ``<family-name>`` and/or
  ``<generic-name>``. 浏览器会使用第一个已安装的或可以通过 ``@font-face``
  at-rule 下载到的字体.

  inherited property.

  You should always include at least one generic family name in a font-family
  list, since there's no guarantee that any given font is available. This lets
  the browser select an acceptable fallback font when necessary.

  Font selection is done one character at a time, so that if an available font
  does not have a glyph for a needed character, the latter fonts are tried.
  意思是, 若一个高优先级字体虽然已经安装, 但无法完整显示所需的全部字符, 则不会
  使用该字体.

- @font-face. 定义一个字体. 通过 descriptors 指定字体的名字, 路径等信息.
  The @font-face rule should be added to the stylesheet before any styles.

  Web fonts are subject to the Same-Origin restriction (font files must be on
  the same domain as the css file using them), unless CORS are used to relax this
  restriction. 一个常见做法就是直接使用外部字体网站提供的 css file (通过 @import
  at-rule 或者 link element), 里面包含 @font-face rules 加载所需字体. 绕过了
  same-origin 问题.

  descriptors.

  * font-family. define name of the font.

  * src. the source of the font.
    ``[ <url> [format(<string>#)]? | local(<family-name>) ]#``

    a priorized, comma-separated list of external or local references. For
    ``url()``, If the url actually points to a file of font container format,
    ``#id`` fragment identifiers are used to indicate which font in the file to
    load.

    For url external font, there can be an optional ``format()`` describing
    the format of the font. If a UA does not support the format, it'll skip
    the font in ``src`` list.

  web font formats: just use woff, woff2.

- font-size. 相当于从 baseline 至 ascender 的高度.

  initial value: medium. inherited property. computed value: 相对长度转换成
  绝对长度.

  它的值影响 em, ex 等长度单位.

  字体值:

  * xx-small, x-small, small, medium, large, x-large, xx-large. Absolute-size
    keywords, based on user's default font size (usually 16px) which is medium.

  * larger, smaller. Relative-size keywords. Relative to parent element's font
    size.

  * ``<length>``. absolute or relative length values.
    
    For relative length units (``em``, ``ex``, etc.), relative to
    parent element's font size. For relative length unit ``rem``, relative to
    root.  rem 相对于 root html element. rem 相比 em 的好处是, 前者不存在叠加效
    应. 即结果是稳定的 (因相对的是 root, 是确定的元素).

  * ``<percentage>``. relative to the parent element's font size.

  root element 的 initial value 是 medium. 因此对于 relative font-size, 若没有在
  任何 parent element 设置 font-size, 则结果就是相对于 medium, 即浏览器默认字体
  大小.

  inherited.

  一般最好使用相对数值, 即与用户设置的默认字体大小相关的 font-size, 这样便于页面
  显示效果统一缩放. 而不使用绝对数值. 若必须使用绝对字体大小, 则应该使用 px.
  Setting the font size in pixel values (px) is a good choice when you need
  pixel accuracy. A px value is static. This is an OS-independent and
  cross-browser way of literally telling the browsers to render the letters at
  exactly the number of pixels in height that you specified.

- font-weight. boldness of font. 可用的值取决于使用的 font-family.

  initial value: normal. computed value: 相对值转换成绝对值, 其他不变.
  values: lighter, bolder, normal (400), bold (700), 100~900. inherited.

  100~900 大致对应:
  thin, extra light, light, normal, medium, semi bold, bold, extra bold, black.

- font-style. 首先从 font-family 字体中选择所需 style 的部分. 对于 italic/oblique,
  若其中一种不存在, 使用另一种代替. 若两种都不存在, 使用 normal 进行模拟.

  initial value: normal. values: normal, italic, oblique. inherited.

- text-transform. 根据 html element ``lang`` attribute 定义的当前语言, 该操作有
  不同的细节处理.

  initial value: none. values: capitalize, uppercase, lowercase, none.
  inherited.

- text-decoration.
  short for text-decoration-line, text-decoration-style, text-decoration-color.

  根据定义 text decorations 会覆盖到该元素的各层 children text elements. 并且
  子元素只能增加更多的 decoration 而无法 override 父元素设置的 decoration.

- text-decoration-line. position of line.

  initial value: none. non-inherited property.
  value: ``none | [underline || overline || line-through]``

- text-decoration-style. style of line.

  initial value: solid. values: ``solid | double | dotted | dashed | wavy``.
  non-inherited.

  If the specified decoration has a specific semantic meaning, like a
  line-through line meaning that some text has been deleted, authors are
  encouraged to denote this meaning using an HTML tag, like ``<del>`` or
  ``<s>``. As browsers can disable styling in some cases, the semantic meaning
  won't disappear in such a situation.

- text-decoration-color. color of line.

  initial value: currentColor. value: ``<color>``. non-inherited.

- line-height. 行的高度, 等于 font-size + leading 高度之和.
  Increasing line-height can make text easier to read.

  inherited.

  initial value: normal.
  values:

  * normal: 大致相当于 1.2

  * ``<number>``: number 倍的 font-size.

  * ``<length>``

  * ``<percentage>``: 相对 font-size.

  computed value: for percentage and length values, the absolute length,
  otherwise as specified.
  注意这决定了对于 line-height 属性指定数值是比较 合理的方式. 否则, 若
  subelement 继承了绝对的 line-height 长度值, 则无法 根据自身字体进行调整.

- letter-spacing. spacing between letters.

  inherited.

  initial: normal. values: normal, ``<length>``. length may be negative.

  User agents may not further increase or decrease the inter-character space in
  order to justify text.

  在全大写的情况下, 增加 letter spacing 有助于提高可读性. 对于普通的小写情况,
  一般无论增加或减小 letter spacing 都会降低可读性. 一般不动即可.

- word-spacing

  inherited.

  initial: normal. values: normal, ``<length>``, ``<percentage>``.
  对于 percentage, 是相对于当前字体的 character advance width.

  对于 bold 情况, 或者修改了 letter spacing 时, 适当修改 word spacing 会有更好
  的可读性.

- text-align. 即行内各 inline elements 如何进行 align & justification. 注意只
  管 inline elements, block elements 不管.

  inherited.

  initial: start (or left if direction is ltr, right if direction is rtl).
  values: start, end, left, right, center, justify, justify-all, match-parent.

  start & end 是 direction-aware (ltr/rtl) 的 left & right.
  justify-all 与 justify 的区别是前者会连最后一行也 justify 掉.

- vertical-align. 两种用途:

  1. 对于某个 inline element 相对于 line box 的 alignment.
     (平时用鼠标 select text 时, 高亮的部分大致就是 line box.)

  2. 对于 table cell content 相对于 cell box 的 alignment.

  注意该属性对 block-level element 不起作用.

  注意 text-align & vertical-align 作用对象是不同的. 前者是影响
  设置了该属性的 element box 内部的各元素之间的 alignment; 后者是影响
  设置了该属性的 element box 如何在它的父元素内部进行 alignment.

  non-inherited.

  initial: baseline.
  values:

  * for inline:

    - baseline. 该元素的 baseline 和 parent 的 baseline.

    - sub. 该元素的 baseline 和 parent 的 subscript baseline.

    - super. 该元素的 baseline 和 parent 的 superscript baseline.

    - text-top. 该元素的 top 和 parent 的字体的 top, 即 font-size 的高度.

    - text-bottom. 该元素的 bottom 和 parent 的字体的 bottom, 即 font descender.

    - middle. 该元素的 middle 位置和 parent 的 baseline + 1/2 * x-height.

    - top. 该元素的 top 和 parent 中一行的 top, 即行的最高点, 它在 text-top 之上.

    - bottom. 该元素的 bottom 和 parent 中一行的 bottom, 即行的最低点, 它在
      text-bottom 之下.

    - ``<length>``. baseline 以上 length 长度. 可以为负.

    - ``<percentage>``. 相对 line-height 的比例, 基于 baseline.

  * for table cell:

    - top. Aligns the top padding edge of the cell with the top of the row.

    - middle. Centers the padding box of the cell within the row.

    - bottom. Aligns the bottom padding edge of the cell with the bottom of the row.

    注意此时是直接调整 table cell 内部的 padding 情况的.

- text-indent. indent lines of text within an element.

  inherited.

  initial value: 0, 即没有缩进.
  value: 缩进量是从 containing block-level element 的 padding box 开始计算的.
  可以是负值. ``<length>``, ``<percentage>`` (containing block element 宽度).

  除了以上值还可以附加 keyword:
  ``each-line``: 每个 forced line break 后的第一行都会缩进;
  ``hanging``: 除了第一行之外的所有行都会缩进.

- text-shadow. 给文字添加影子文字. It accepts a comma-separated list of shadows
  to be applied, each of them is some combination of X and Y offsets from the
  element, blur radius, and color.

  The first two <length> values are the <offset-x> and <offset-y> values. The
  third, optional, <length> value is the <blur-radius>. The <color> value is the
  shadow's color. offset-x 的正向是向右的; offset-y 的正向是向下的. 若 offset-x
  offset-y 都是 0, 则依靠 blur radius 给效果. blur-radius 控制影子文字的线条扩散
  的情况, 它越小影子越清晰, 越大越有 blur 的效果.

  When more than one shadow is given, shadows are applied front-to-back, with
  the first-specified shadow on top.

  inherited.

  initial: none.

- quotes. 设置自动添加的 open/close quote marks 长什么样.
  例如 ``<q>`` element使用, 或者 ``open-quote`` ``close-quote`` value 使用.

  inherited.

  values:
  none, quote marks 为空;
  ``[<string> <string>]+``, 设置一级或多级 quotes 使用的 open/close quote mark
  pairs.

box
^^^

specifying box model
""""""""""""""""""""
- ``box-sizing``. 规定该元素上的 width/height 属性指定的是哪个 box 的
  width/height. 从而影响 user agent 如何确定一个元素的整体 dimension.

  non-inherited property.

  initial vlaue: content-box.

  specified value:

  * content-box. The width and height properties include the content, but does
    not include the padding, border, or margin.

  * border-box. The width and height properties include the content, padding,
    and border, but do not include the margin.

  For modern responsive design, 人们一般通过 percentage 的方式限制元素的
  dimension, 而不设置绝对尺寸. 此时, width/height 值为 border-box 就方便很多.
  推荐做法 [CSSTrickBoxSizing]_:

  .. code:: css

    html {
      box-sizing: border-box;
    }
    *, *:before, *:after {
      box-sizing: inherit;
    }

content box
"""""""""""
- width.
  width of element's context area (normally).

  non-inherited property.

  inline elements 和 table rows 不能修改 width 属性. 它们只能使用 auto. 即由
  浏览器自动计算所需的值.

  initial value: auto.

  specified value.

  * specified value 可以是 ``<length>`` 或 ``<percentage>`` 或 auto.
    指定 percentage 时, 是相对于 containing block's width. 但如果 containing
    block element 的宽度本身就依赖于它的 content, 则 result is undefined.

  * auto. 由浏览器自动计算所需宽度.

  computed value: percentage, length, or auto.

- min-width.
  prevents the used value of the width property from becoming smaller than the
  value specified here.

  non-inherited property.

  initial value: 0.

  可设置的值与 width property 一致.

- max-width.

  initial value: none. i.e., unlimited.

  当决定元素宽度时, max-width overrides width, but min-width overrides
  max-width.

- height.

  类似于 width.

  inline elements 和 table columns, column groups 不能修改 height 属性.
  它们只能使用 auto. 即由浏览器自动计算所需的值.

  The percentage is calculated with respect to the height of the generated
  box's containing block. If the height of the containing block is not
  specified explicitly (i.e., it depends on content height), and this element
  is not absolutely positioned, the value computes to auto.

- min-height.

  类似于 min-width.

  The percentage is calculated with respect to the height of the generated
  box's containing block. If the height of the containing block is not
  specified explicitly (i.e., it depends on content height), and this element
  is not absolutely positioned, the percentage value is treated as 0.

- max-height.

  类似于 max-width.

  max-height overrides height, but min-height overrides max-height.

  The percentage is calculated with respect to the height of the generated
  box's containing block. If the height of the containing block is not
  specified explicitly (i.e., it depends on content height), and this element
  is not absolutely positioned, the percentage value is treated as none.

padding
"""""""
- padding-top.

  non-inherited.

  initial value: 0.

  specified value:

  * ``<length>``

  * ``<percentage>``.
    The size of the padding as a percentage, relative to the width of the
    containing block.

- padding-right.

- padding-bottom.

- padding-left.

- padding.
  shorthand for all above.

border
""""""
- border-top-width.

  non-inherited property.

  initial value: medium.

  specified value is one of the following:

  * ``<length>``

  * thin, medium, thick. The actual effect is implementation specific.

- border-right-width.

  ditto.

- border-bottom-width.

  ditto.

- border-left-width.

  ditto.

- border-top-style.

  non-inherited property.

  initial value: none.

  specified values:

  * none. no border. In the case of table cell and border collapsing, the none
    value has the lowest priority.

  * hidden. no border. In the case of table cell and border collapsing, the
    none value has the highest priority.

  * dotted.

  * dashed.

  * solid.

  * double.

  * groove. 边框切割.

  * ridge. 边框突起.

  * inset. border 内容部分嵌入.

  * outset. border 内容部分突起.

- border-right-style.

  ditto.

- border-bottom-style.

  ditto.

- border-left-style.

  ditto.

- border-top-color.

  non-inherited property.

  initial value: currentColor.

- border-right-color.

- border-bottom-color.

- border-left-color.

- border-width.
  shorthand for ``border-{top,right,bottom,left}-width``.

- border-style.
  shorthand for ``border-{top,right,bottom,left}-style``.

- border-color.
  shorthand for ``border-{top,right,bottom,left}-color``.

- border.
  shorthand for ``border-{width,style,color}``.
  后者三个属性又是 shorthand, 依次展开.

  border shorthand 适合当需要给四边设置相同的属性时使用.
  border-top/right/bottom/left shorthands 适合分别给不同边设置不同属性时使用.

  border cannot be used to specify a custom value for ``border-image``, but
  instead sets it to its initial value, i.e., none.

  The border will be invisible if its style is not defined. This is because the
  style defaults to none.

  non-inherited property.

  specified value: ``<br-width> || <br-style> || <color>``

- border-top.
  shorthand for ``border-top-{width,style,color}``.

- border-right.

- border-bottom.

- border-left.

overflow
""""""""
- overflow. What to do when an element's content is too large to fit in its
  block formatting context. shorthand for overflow-x and overflow-y.

  When parent element's overflow is hidden, all child elements is hidden
  together with parent.

  关于 viewport 的 overflow 情况. ``<html>`` root element 决定整个 viewport 的
  scrollbar 情况. 作为 root element, spec 规定: If overflow on ``<body>`` is
  visible, overflow on ``<html>`` must be interpreted as auto. Otherwise
  ``<html>`` use what is specified on ``<body>``. 这导致, 最终效果是, viewport
  只能有 scrollbar 或者在相应方向上 hide overflowed content, 而不存在
  ``visible`` 值带来的效果. [SOBodyOverflow]_

  non-inherited.

  initial value: visible.

  specified value:

  * visible. content is show normally even if outside the padding edge.

  * hidden. the part of content out side of the padding edge is clipped.
    注意是 padding edge, 不是 content edge.

  * scroll. add a scrollbar. 无论内容是否确实放不下, scrollbar 都会存在.
    对于 overflow shorthand, 两个方向的 scrollbar 都会加上.

  * auto. 如果能放下, 就不加 scrollbar, 否则加上.

- overflow-x.
  overflow settings at x axis only.

  主要在两种情况下会出现 overflow:

  * block-level child element 的 width/height 大于 parent element, 导致凸出去.

  * inline child element, 当设置的 white-space 属性为 nowrap 等影响 layout
    engine 自动换行算法时, 或者文字内容难以自动换行时.

- overflow-y.

  一般只有通过某种方式限制了 box height 时, 才会有纵向的 overflow.

white space
"""""""""""
- white-space.
  控制元素内的 whitespace collapsing algorithm.

  inherited property.

  可以设置在任何元素上, 影响内部的 whitespace 处理算法.

  initial value: normal.

  specified value:

  * normal. whitespace chars are collapsed. Lines are broken as
    necessary to fill line boxes.

  * nowrap. 所有 whitespace chars collapse 成一个空格, 但不会在 line box
    的边界 wrap line. 最终效果是只有一行.

  * pre. 效果相当于 html pre element.

  * pre-wrap. 效果和 pre 一样, 除了一点: 如果 verbatim 行太长, 会自动在 line
    box 边界 wrap line.

  * pre-line. 效果和 normal 一样, 除了一点: newline char 也会 wrap line, 而不会
    collapse.

background
""""""""""

- background-color

- opacity. opacity 指定的不透明性对一个元素和它所有 dom children nodes 一起生效.

  specified value 是 0~1.0 的 ``<number>``. computed value 是 0~1.0 的数字,
  若不在范围内, 取最近的确界值.
  注意 opacity 本身是 non-inherited property. 它的初始值是 1, 完全不透明.

  一个元素的所有子元素上的 opacity值都是相对于该元素的 background
  (即父元素的区域) 的. 例如, 若 ``<a><b></b></a>`` 两层, a 透明 50%, b
  不设置, b 相对于 a opacity=1, 故 b 的整体效果是 50%. 若 b opacity!=1,
  则相对于 a 更透明一些.

  opacity vs alpha channel:

  * 通过 ``rgba()`` ``hsla()`` 等设置的 alpha channel 导致的透明性是绝对的,
    不是相对于该元素的 background. 即通过设置 alpha channel 子元素可以比父
    元素不透明.

  * rgba 等值经常设置在 inherited property 上. 由于子元素默认继承, 逻辑上是
    绝对效果而不是相对效果也比较合理.

pseudo-element
^^^^^^^^^^^^^^
- content.
  和 ``::before`` ``::after`` 一起使用. 通过这种方式生成的元素是
  anonymous replaced elements.

  non-inherited.

  initial: normal 或 none.
  values:

  * none. 不生成元素.

  * normal. same as none.

  * ``<string>``. text characters. 注意所有内容 verbatim 显示. 不做解析.

  * ``<url>``. an external resource to be displayed, e.g., image.

  * ``<counter>``. 设置 css counter 内容. 作为 counter 配置的一部分.

  * ``attr(x)``. value of attribute x. 注意 value 是 verbatim 显示. 不做解析.

  * ``open-quote``, ``close-quote``.

  * ``no-open-quote``, ``no-close-quote``.

  除了 none, normal 两个 keyword, 其他内容可以同时指定任意次数. 所以可以非常复杂.

counter
^^^^^^^
Counters 可以用于 auto-numbering headers 等.
相关属性和值: ``counter-reset``, ``counter-increment``, ``content``,
``<counter>``.

A new instance of the counter is automatically created in child elements.
但默认情况下, 这个新的实例的初始值是父元素中实例的当前值. 使用 counter-reset
则可以对这个新实例重新赋值. 配合 ``counters()`` function 使用效果很好.

- counter-reset. reset one or more counter to their specified values or 0.
  在受影响的 element scope 内部, 新的 counter identifier value 将重置.

  non-inherited.

  initial: none. 即默认情况下不会重置 counter.
  values: ``[ <custom-ident> <integer>? ]+ | none``

  注意到属性值中 (多个) identifier 后面若没有 integer 就重置为 0.

- counter-increment. increase the specified counter, optionally by the
  specified amount.

  non-inherited.

  initial: none. 不递增.
  values: ``[ <custom-ident> <integer>? ]+ | none``

例子
.. code:: css
  ol {
    counter-reset: section;                /* Creates a new instance of the
                                              section counter with each ol
                                              element */
    list-style-type: none;
  }

  li::before {
    counter-increment: section;            /* Increments only this instance
                                              of the section counter */
    content: counters(section, ".") " ";   /* Combines the values of all instances
                                              of the section counter, separated
                                              by a period */
  }


special
^^^^^^^
- all. a shorthand property representing all properties, apart from
  ``unicode-bidi`` and ``direction``.

  values: initial, inherit, unset, revert. 这属性用于方便地重置某元素
  的所有属性值.

  non-inherited property.

data types of values
--------------------
- ``<color>`` value, in sRGB color space, with optionally alpha-channel
  transparency value.

  颜色值的表达形式:

  * 在 RGB 笛卡尔座标系统下:

    - ``rgb()``, 每项 0-255 ``<integer>`` 或 0%-100% ``<percentage>``.

    - ``rgba()``, alpha 的部分是 0~1 的 ``<number>`` 或 0%~100% 的
      ``<percentage>``.

    - ``<hex-color>``, ``#RRGGBB[AA]`` 或 ``#RGB[A]``. 若 AA 部分省略,
      等于 FF, 即完全不透明. #RGBA 相当于 R/G/B/A 每个值重复一遍得到的
      标准形式.

    在 css4 中, rgba is an alias for rgb.

  * 在 HSL 柱座标系统下:

    - ``hsl()``, hue is ``<angle>``, 若没写单位认为是 ``deg``. saturation
      & lightness 是 ``<percentage>``.

    - ``hsla()``, alpha 和 rgba 中相同.

    In css4, hsla is an alias for hsl.

  * keyword values. case-insensitive.

    - ``<named-color>``, 除了常见颜色之外, 用得不多. 谁记那么多颜色名字啊.
      这些颜色都没有任何 transparency, 相当于 alpha channel == 1.

    - ``transparent``, 全透明. 等价于 ``rgba(0,0,0,0)``.

    - ``currentColor``. 当前 (元素) 的 color property value.

- ``<number>``, 实数. 可以是整数, 有限的有理数, 并支持 ``+n.m``, ``.m``,
  科学计数法等形式.

- ``<percentage>``, 百分数. ``<number>%``.

- ``<angle>``, ``[+|-]<number>deg|grad|rad|turn``. positive angle is clockwise,
  negative angle is counterclockwise.

- ``<family-name>``, font family name. Font family names containing whitespace
  should be quoted. 注意若一个字体名字完全是由 valid identifier name 和
  whitespace 组成, 则也可以不 quote (see: https://mathiasbynens.be/notes/unquoted-font-family).

- ``<generic-name>``, generic font family names are keywords and must not be
  quoted. values: serif, sans-serif, monospace, cursive (as in cursive writing),
  fantasy (decorative fonts), system-ui (the default user interface font on a
  given platform).

- ``<length>``,  ``<number><length-unit>?``, 数值是 0 时可以没有单位.

  * font-relative length: em (等于当前或父元素的 font-size), ex (x-height), rem.

  * viewport-percentage length: vh (1% of viewport height), vw (1% of viewport width),
    vmin (min of vh, vw), vmax (max of vh, vw).

  * absolute length: px, mm, cm, in, pt, pc. 注意由于不同屏幕分辨率等等烦人
    的情况, 除了 px, 这些单位可能并不代表它本意的尺寸. 所以尽量别用吧.

    对于 px, 标准情况下, 一个 px 就是一个 screen pixel. 所以是确定的. 除非使用了
    浏览器的缩放功能去放大和缩小整体页面. 此时, px 即 css pixel 与 physical pixel
    会有缩放的比例关系. 但由于本质上所有页面元素尺寸最终 used value 都转换
    成 pixel, 故效果是页面整体进行等比例缩放.

- ``<url>``, ``url(...)`` functional notation. It may be written without quotes,
  or surrounded by single or double quotes. Relative URLs are allowed, and are
  relative to the URL of the stylesheet.

- ``<string>``, any unicode chars with single or double quotes. 字符串支持通过
  ``\`` escape char, 尤其是可以 escape newline 来做到跨行.

- ``<counter>``, 值是 css function.

  * ``counter(name[, style])``. 输出一个 counter value.
    name 是选择输出的 css counter variable, 是 identifier, 不是字符串.
    style 是 counter style, 可以是 list-style-type 允许的任何值.

  * ``counters(name, string[, style])``. 输出每层的同名 counter 的值.
    string 是每层 counter value 之间的分隔符.

- ``<custom-ident>``. an arbitrary user-defined valid CSS identifier.
  But it's case-sensitive.

  根据 identifier 作为哪个 property 的值, 相应地具有一些 identifier 是不能
  使用的. 这是为了避免与 property 的 predefined keyword value 冲突.

- ``<time>``::

    [+|-]?<number>[s|ms]

- ``<timing-function>``. A function that defines how value changes during
  transition/animation. A timing function is defined as::

    x = f(t)

  边界条件::

    0 = f(0)
    1 = f(1)

  where x 的值是值变化的比例, 即 ``change/(v2 - v1)``. 根据具体函数, 该值可能小
  于 0 或大于 1; t 是时间比例, 即 ``time/duration``, 定义域为 ``[0, 1]``.
 
  CSS supports mainly two classes of timing functions:

  * cubic Bézier curves (三阶贝塞尔曲线), a.k.a., easing functions. They are
    smooth (连续而处处可导). 三阶 Bezier 需要 4 个 control point 定义. 在时域
    实际上已经有两个 control point 是确定的即边界条件 ``(0, 0), (1, 1)``.
    这里只需要指定两个中间的控制点::

      cubic-bezier(x1, y1, x2, y2)

    x1, x2 必须在 ``[0, 1]`` 之内. 这是为了保证对 P1, P2 控制点的选取导致生成的
    cubic bezier curve 是合法函数.  这需要保证 P1, P2 的横座标在 ``[0, 1]`` 之
    内 (四个点的凸包不能跨越 ``t = 0``, ``t = 1`` 座标线). 而对纵座标没有要求.
    事实上, 如果纵座标在 ``[0, 1]`` 之外 , 能制造出 bouncing effect.

  * step functions. 阶跃函数.::

      steps(n[, direction])

    ``n`` is the number of steps, positive ``<integer>``, 这是指从起点开始, 需要
    走几步到达终点, 也就是说每步之间的时间间隔是 ``1/n``, 在函数上, 点的数目是
    ``n+1``; ``direction`` 是 ``start`` or ``end``, 指函数在每个阶跃点是左连续
    还是右连续, 也就是说开始时立即走第一步还是等待 ``1/n`` 间隔后再走. 默认是
    ``end``.

  CSS 以 keyword 形式提供了一些常用 timing function:

  * 3-n bezier curves:

    - linear. ``cubic-bezier(0,0,1,1)``

    - ease. 开始慢, 中间快, 最后慢. 开始时比 ease-in 要快一些.
      ``cubic-bezier(0.25, 0.1, 0.25, 1.0)``

    - ease-in. 开始慢, 逐渐提速, 突然停止. ``cubic-bezier(0.42, 0.0, 1.0, 1.0)``

    - ease-out. 开始快, 逐渐减速, 慢慢停止. ``cubic-bezier(0.0, 0.0, 0.58, 1.0)``

    - ease-in-out. 开始慢, 中间快, 最后慢. 相当于 ease-in + ease-out.
      ``cubic-bezier(0.42, 0.0, 0.58, 1.0)``

  * step functions:

    - step-start. 开始时直接跳到终态, 保持不变. ``step(1, start)``.

    - step-end. 保持初态, 到最后一刻跳到终态. ``step(1, end)``.

global values
^^^^^^^^^^^^^

- initial. 明确使用该属性的 initial value.

- inherit. 对于 inherited-property, 明确要求使用从 parent 继承来的 computed value;
  对于 non-inherited property, 要求从 parent 继承值.

- unset. 去掉由其他 css rulesets 明确定义的关于该属性的值. 也就是说, 若有继承值,
  则重置为继承值, 若没有则重置为初始值.

- revert. revert 该属性的 cascading, 使用相对于当前定义所在源的前一个定义源中的
  定义.

  The revert keyword is useful for isolating embedded widgets or components
  from the styles of the page that contains them. 也就是说, 对于嵌入的组件, 屏蔽
  author styles, revert to user 或 user-agent styles.

  ``all`` property 可以配合 revert value 使用, 比较方便.

  No stable UA support yet!!

Mobile
======
viewport
--------

concetps
^^^^^^^^
- viewport. The browser's viewport is area of the window in which web content
  can be seen.  The rendered page may be larger than the viewport, in which
  case a browser provides scrollbars to view content that couldn't fit in.

- 桌面端浏览器的 viewport 一般是浏览器窗口的实际尺寸, 比浏览器窗口略小.
  
- 移动端浏览器的一般把自己的 viewport 设置得比较大 (virtual viewport), 大于屏幕
  长宽 (in pixels), then shrink the rendered result down so it can all be seen
  at once. This is done because many pages are not mobile optimized, and break
  when rendered at a small viewport width.

- But virtual viewport is not so good for pages that are optimized for narrow
  screens using media queries. ``viewport`` meta tag 就是用于解决这个问题的.

- 在移动端, 如果屏幕分辨率很高, 浏览器经常 translating multiple hardware pixels
  to one CSS "pixel".

viewport meta tag
^^^^^^^^^^^^^^^^^
::

  <meta name="viewport" content="..."/>

- ``content`` is a comma separated list of ``key=val``.

- typical settings::

  <meta name="viewport" content="width=device-width, initial-scale=1">

keys
""""

- ``width``. control the width of viewport. value can be

  * a specific number of pixels.

  * ``device-width``

- ``height``. ditto. 相对少见. 因为一般不需考虑 height.

  * ``device-height``.

- ``initial-scale``. initial ratio between the device width and the viewport
  size.

- ``maximum-scale``.

- ``minimum-scale``.

- ``user-scalable``. yes or no.

Web Components
==============

- Why it took it so long for html to be finally programmable?

flash
=====

- obsolete technology.

- 一般通过 js 加载 flash 文件放在 div 中显示.

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

references
==========
.. [CSSTrickBoxSizing] `Box Sizing <https://css-tricks.com/box-sizing/>`_
.. [FlexMarginAuto] `Flexbox’s Best-Kept Secret <https://hackernoon.com/flexbox-s-best-kept-secret-bd3d892826b6>`_
.. [SOBodyOverflow] `body tag overflow (auto, visible?) <https://stackoverflow.com/questions/36794306/body-tag-overflow-auto-visible>`_
.. [TransitionVSAnimation] `Transition or Animation: Which One Should You Use? <http://www.adobepress.com/articles/article.asp?p=2300569>`_
