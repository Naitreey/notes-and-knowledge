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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~

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

- ``<style>``, 属于 metadata content, 从 html 规范上讲, 只能放在 head element 中.
  Although in practice, every browser allows style element in body.

  attributes.

  * ``type``, mime type of styling language.

  * ``media``, a media query defining which media the style applies to.

  * ``title``, 定义该 style definition 所属的 alternative stylesheet set.

sectioning root
~~~~~~~~~~~~~~~

- ``<body>``, body 里的内容才显示在页面上.

  attributes.

  * 一系列 callback function 定义.

content sectioning
~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~

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
  chars 都会被保留下来.

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
    ``application/x-www-form-urlencoded`` 默认; 若有 file input, 自动变成
    ``multipart/form-data``; ``text/plain``.
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

- ``<label>`` label for a form control.
  One form control can be associated with multiple labels.

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

  * ``checked``, 对于 checkbox 和 radio, 默认选中.

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

  * ``maxlength``, ditto.

  * ``multiple``, user can enter more than one value. for email, file.

  * ``name``, 若一个 form 中多个 form control 有相同的 ``name``, 则
    form data 中出现多个 name/value 数据, 且这些数据按 form control 的先后顺序
    而出现. 服务端有义务保持这个数据顺序.

  * ``value``, 注意它是 input 的初始值. form 里实际输入的值也不会更新到这里.
    若没默认值可以不设置.

  * ``pattern``, 在各个 type 的基本格式要求之外, 详细的 validation 要求.
    regexp. 使用 ``title`` attribute 添加对 pattern 的输入提示.

  * ``placeholder``, 提示用户可输入的内容.

  * ``readonly``, 不同于 disabled. readonly 会 submit 至服务端. disabled 不会.

  * ``required``.

  * ``spellcheck``, 是否检查输入内容的拼写.

  * ``tabindex``, tabbling navigation order.

- ``<input type="text">`` 用于 single-line value, 并且没有更合适的具体类型时.

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

- ``<input type="checkbox">``

  checkbox 除了可以处于 checked/unchecked 状态之外, 还可以处于 indeterminate
  状态. Like... a Schrödinger's checkbox... A checkbox in the indeterminate
  state has a horizontal line in the box. (这种状态的 checkbox 在 submit 时
  等价于 unchecked, 即不会有数据在 post data 中.)

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

- ``<input type="color">``, color is selected by a visual color picker or
  ``#rrggbb`` (1600 万色) hex format. No alpha channel is allowed.

  color input element 的值是 ``#rrggbb`` string (always lowercase). The value
  is never in any other form, and is never empty.

  A color input's value is considered to be invalid if the user agent is unable
  to convert the user's input into seven-character lower-case hexadecimal
  notation. 任何非法值导致颜色值成为 ``#000000`` 即黑色.

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

- ``<input type="email">`` 自动根据 email format 进行验证.

  attributes.

  * ``multiple``, 允许输入多个 email address, separated by commas (and possible
    whitespaces). 此时, ``pattern`` attribute 须对每个值都匹配.

- ``<input type="hidden">`` include data that cannot be seen or modified by
  users when a form is submitted. 常见的应用场景是 security token (e.g. CSRF token),
  或 object id.

  没有任何方法 (除非修改源代码) 能够在页面上显示 hidden input.

  由于没有可修改的值, 没有 validation.

  attributes.

  * ``value``, 不能修改的数据值.

- ``<input type="number">``

  built-in validation to reject non-numerical entries.
  合法的输入可通过 min, max, step 等进一步限制.

  注意默认情况下 step == 1, 合法输入只能是整数. 调整 step 为小数后, 就可以输入
  floating point number (包含 1.5e3 形式), 但要注意精度与 step 一致.

  number input 不支持 pattern attribute, 理由是反正只能输入 number, 而且 min,
  step, max 已经足够.

- ``<input type="range">`` 指定一个从 min ~ max 之间的数值, 而这个数值到底
  是多大并不重要. As a rule, if the user is more likely to be interested in the
  percentage of the distance between minimum and maximum values than the actual
  number itself, a range input is a great candidate.

  attributes.

  * ``value``, 默认初始值是 (min+max)/2.

  * ``min``, ``max``, ``step``, 默认值分别是 0, 100, 1.
    step == any 可以指定任意精度.

    设置关联的 datalist element 可以给 range control 加上刻度.

- ``<input type="password">`` the text is obscured so that it cannot be read.
  mobile devices often display the typed character for a moment before obscuring
  it.

  attributes.

  * ``autocomplete``. on: allow autocomplete. off: 对于 password input 浏览器会
    忽略这个值. current-password: 自动补全当前密码, 而不是建议生成新密码.
    new-password: 允许浏览器建议生成新密码, 禁止使用当前密码进行自动补全.

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

- ``<input type="search">`` 本质上跟 text input 一样, 单独分类是因为浏览器
  可能进行与 text 稍不同的一些处理方式: 一些浏览器在输入框右边设置一个 x;
  浏览器可能保存在不同地方的 search input 的输入, 用于提供 autocomplete.

  ``name`` of search input is often ``q``.

- ``<input type="tel">`` telephone number. 没有 validation 因为 telphone
  在全世界没有统一格式.

  tel input 实际上和 text input 相同, 但是它的作用在于移动设备可根据 tel type
  选择专门的 virtual keyboard; 以及便于进行 css, js 等 manipulation.

- ``<input type="url">`` 支持 absolute url, 还支持 relative url.

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

- ``<textarea>`` multiline plain-text. 许多属性与 input 的相应属性相同.

  它的初始值直接写在 open/closing tag 内部.

  注意 textarea 中, 所有 newline 都是 CRLF 的. 所以后端必须按照业务需要
  进行转换, 不可不加考虑地直接使用.

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

  * ``rows``, ``cols``, 行列数.

  * ``spellcheck``

  * ``wrap``, 如何 wrap text.

    ``hard``: 自动添加 CRLF 以保证每行宽度不大于 cols.
    ``soft``: 不自动添加, 只是保证 linebreaks 都是 CRLF, 这是默认值.

- ``<select>`` select one or more choices from options. 这类似于 radio group
  或 checkbox group.

  它里面是 option/optgroup elements.

  设置 multiple 或 size 后不使用下拉列表, 使用滚动列表.

  attributes.

  * ``autofocus``

  * ``disabled``

  * ``form``

  * ``multiple``, 允许选择多个.

  * ``name``

  * ``required``

  * ``size``, 设置滚动列表中可见行数.

- ``<datalist>``, 表示一系列可选的值, 需要配合其他 form control 使用.
  里面是 zero or more option elements.

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

- ``<fieldset>`` form controls groups.
  里面允许是一个 optional legend element followed by flow content.

  attributes.

  * ``disabled``

  * ``form``

  * ``name``, name of the group.

- ``<legend>``, title of parent fieldset.

- ``<meter>``, 包含一个值, 表示它在两个值 (min/max) 之间的程度.

  meter & progress element 本身都不是 form control, 而是配合其他 form control
  的状态指示.

  meter 可以做例如输入密码的强度提示.

  attributes.

  * ``value``

  * ``min``, default 0.

  * ``max``, default 1.

  * ``low``

  * ``high``

  * ``optimum``

- ``<progress>``, 包含一个值, 表示一项任务的完成进度. 注意它的最小值固定是 0.

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
~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~


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
  若包含 ``-``, key 须去掉 ``-`` 并将 dash 后面第一个字符大写.

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

- 每个 html element 都是由一个 invisible box 包裹起来的.

- CSS statement:
  a css statement begins with any non-space characters and ends at the first
  closing brace or semi-colon.

  一个 css 文件由多个 css statement 构成.

  css statement 包含两类: at-rules & rulesets.

- css ruleset:
  一个 css ruleset (or simply rule) 由 a group of selectors + declaration block
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

- shorthand property. a css property that let you set the values of several
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

- at-rules:
  starts with an at sign, followed by an identifier and then continuing up to
  the next semi-colon outside of a block or the end of the next block.

  若 at-rule 后面是 block, 可能里面是一系列 descriptor/value pairs, 也可能是
  别的.

- comment. c-style ``/* */``.

- value definition syntax (类似 BNF notation, 用于定义 property 的允许值).

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

- 各种 values.

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

selector
--------

- basic selectors

  * universal selector. ``*``

  * type selector. ``element-name``

  * class selector. ``.class``

  * id selector. ``#id``

  * attribute selector. ``[attr=value]``

- combinators

  * child combinator. ``a > b``

  * descendant combinator. ``a b``

  * adjacent sibling combinator. ``a + b``

  * general sibling combinator. ``a ~ b``

cascade, specificity, inheritance
---------------------------------


when to put css definitions at XXX?

最终决定一套生效的 css 规则的基本流程:

1. 首先应用 cascade algorithm.

2. 结果中优先级相同的通过 specificity algorithm 进一步筛选.

3. 结果中再有具体性相同的, 通过定义顺序筛选.

4. 对于没有直接指定值的属性, 若是 inherited property, 从 parent element
   继承值或对于 root element 使用初始值; 若是 non-inherited property,
   使用初始值.

cascade
~~~~~~~

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
~~~~~~~~~~~

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
~~~~~~~~~~~

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

at-rule
-------

- 一些 at-rule 可以 nested, 即构成 nested at-rules.

properties
----------

text
~~~~~
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

  * relative-size keywords:

    - xx-small, x-small, small, medium, large, x-large, xx-large. 这些大小
      是基于 medium 值进行放大和缩小的. medium 的值是用户设置的浏览器默认
      字体大小 (which is usually 16px).

    - larger, smaller. 比 parent element 字体大或者小. 比例与 small/medium/large
      等变化比例一致.

  * relative ``<percentage>`` or ``<length>``, 与 parent element 或 root element
    的 font-size 的关系.

    对于单位是 ``em`` ``rem`` ``ex`` 的长度 em, ex 相对于 parent element, rem
    相对于 root html element. rem 相比 em 的好处是, 前者不存在叠加效应. 即结果
    是稳定的 (因相对的是 root, 是确定的元素).

  * absolute ``<length>``, 绝对长度.

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

  values: normal, ``<length>``. length may be negative.

  User agents may not further increase or decrease the inter-character space in
  order to justify text.

- word-spacing

background
~~~~~~~~~~

- background-color

element
~~~~~~~
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

special
~~~~~~~
- all. a shorthand property representing all properties, apart from
  ``unicode-bidi`` and ``direction``.

  values: initial, inherit, unset, revert. 这属性用于方便地重置某元素
  的所有属性值.

  non-inherited property.

value data types
----------------
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
    会有缩放的比例关系. 但由于本质上所有页面元素尺寸最终 computed value 都转换
    成 pixel, 故效果是页面整体进行等比例缩放.

- ``<url>``, ``url(...)`` functional notation. It may be written without quotes,
  or surrounded by single or double quotes. Relative URLs are allowed, and are
  relative to the URL of the stylesheet.

- ``<string>``, any unicode chars with single or double quotes. 字符串支持通过
  ``\`` escape char, 尤其是可以 escape newline 来做到跨行.

global values
~~~~~~~~~~~~~

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

