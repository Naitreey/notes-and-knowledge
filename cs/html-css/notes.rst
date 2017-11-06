general
=======
- html/css 的相对性和 (la)tex 的绝对性.
  webpage 和 pdf 应用场景最大的区别是: 一个是面向显示器的, 具有适应性, 因此里面的尺寸
  大部分都是相对的; 另一个是面向纸张和印刷的, 具有精确性, 因此里面的尺寸大部分
  都是绝对的.

- 别指望用户会使用最新版本的浏览器, 所以一般选择使用主流浏览器支持的功能.

- 很多公司并不自己购买服务器 serve 网站, 而是购买 web hosting company 的服务,
  例如云服务公司.

html versions
-------------
html can be seen as a loosely formatted xml variants for the web.

xhtml 是应用 xml 语法, 对 html 进行部分严格化和修正而发明的. xhtml 可以看作是
xml 的严格子集, 是 html's serialized format. 不过 xhtml 已经死了. 根本没人 care,
大家去用 json 了.

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

- ``accesskey``, 用于生成 keyboard shortcut for the current element.
  配合浏览器预设的激活键 (Alt, Alt + Shift, etc.) 使用.

comment
~~~~~~~

- ``<!-- comment -->``

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

  * ``name``

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

