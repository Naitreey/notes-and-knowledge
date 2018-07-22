General
=======

markdown & web 的关系
---------------------
- Markdown’s syntax is intended for one purpose: to be used as a format for
  writing for the web.  The idea for Markdown is to make it easy to read,
  write, and edit prose. HTML is a publishing format; Markdown is a writing
  format. Thus, Markdown’s formatting syntax only addresses issues that can be
  conveyed in plain text.

- 由于 markdown 本身就是为了 writing for the web 而存在. 它的目标语言就是 html.
  For any markup that is not covered by Markdown’s syntax, you simply use HTML
  itself. There’s no need to preface it or delimit it to indicate that you’re
  switching from Markdown to HTML; you just use the tags.

- markdown 和 html/css/js 一起使用, 才可以解决所有问题. markdown 只解决书写部分
  的问题, 即让 web content 更容易书写.

- 书写 markdown 时, 需要时常想着它生成的 html elements 是什么, 才能对最终效果有信心.

syntax
======

escaping
--------
- ``\`` escape. use backslash escapes to generate literal characters which
  would otherwise have special meaning in Markdown’s formatting syntax.

inline html
-----------
- block-level html elements must be separated from surrounding content by blank
  lines, and the start and end tags of the block should not be indented with
  tabs or spaces.

- inline-level HTML tags can be used anywhere in a Markdown paragraph, list item,
  or header. If you want, you can even use HTML tags instead of Markdown
  formatting.

- markdown syntax is not processed within block-level elements; and it is processed
  within inline-level elements.

- special characters: ``&`` ``<`` 两个特殊 html 字符. 对于 ``&``, 除了它构成 html
  entity 的起始字符时, 都会自动被 escape. 对于 ``<``, 除了它构成 html tag 的起始
  字符时, 都会被 escape.

block elements
--------------
- paragraph. one or more consecutive lines of text, separated by one or more
  blank lines. A blank line is any line that looks like a blank line — a line
  containing nothing but spaces or tabs is considered blank.
  
  若需要在段内添加 强制的 linebreak, you end a line with two or more spaces,
  then type return.

- headers. 两种风格.

  第一种使用 ``=`` & ``-`` 在 title 下面. 故只支持两层 header. Any number of
  ``=`` & ``-`` will work.

  第二种使用 1-6 个 ``#`` 在 title 行起始和结束位置, 对应 1-6 level headers.
  结束位置的 ``#``-s are optional 并且没必要和起始位置的数量相同.

- blockquotes. 使用 ``>`` for blockquotes. 对于每个 quoted 整段文字, 只需在段首
  添加一个 ``>``. But it looks best if you hard wrap the text and put a ``>``
  before every line.

  Blockquotes can be nested. Blockquotes can contain other Markdown elements,
  including headers, lists, and code blocks.

- lists. ``*`` ``-`` ``+`` as unordered list markders.
  ``N.`` as ordered list markers. 注意 oderdered list 中序号的值实际上并没有效果.
  因生成的 ``<li/>`` item 没有序号值.

  一个 list item 若有多行, 可以采用 hanging indents 与首行对齐, 也可以不对齐, 并
  没有影响.

  若 list item 之间存在 blank lines, 则每个 item 会自成一段, 即 wrapped in ``<p/>``
  tag.

  一个 list item 也可以由多段构成, 每段的第一行必须缩进 4 spaces.  因此, 为了统
  一, list item marker 和它后面的空格也应该是 4 spaces 长度.
  
  list item 中出现的任何其他 markup element, e.g. blockquote, code block 等都要
  基于 list item 段首的缩进量进行. 例如 blockquote 需要相对于 list item 起始处
  缩进 4 spaces or a tab; code block 本身需要缩进 4-space/1-tab, 所以相对于
  list item 起始处需要缩进 8-spaces/2-tabs.

verbatim blocks
---------------
- Indent every line of the block by at least 4 spaces.

- Regular Markdown syntax is not processed within code blocks.

horizontal rules
----------------
- 多个 ``*`` 或 ``-`` 或 ``_`` 在单独的一行. 注意与 heading 的情况区分.

links
-----
- inline link. ``[link text](url "title")``. ``"title"`` part is optional.

- reference link. ``[link text][id]``. 可以在中间加空格: ``[...] [..]``.
  在任何地方使用独立的行定义 link label: ``[id]: url "title"``. title is also
  optional.

  Link definition names may consist of letters, numbers, spaces, and
  punctuation.
 
  Link names are not case sensitive.

  注意对于 reference link, title 部分的 quoting 可以使用 double quote, single
  quote, 或者 parentheses. url 的部分可以 optionally surrounded by ``<>``.

  You can put the title attribute on the next line and use extra spaces or tabs
  for padding, which tends to look better with longer URLs.

  Link definitions are only used for creating links during Markdown processing,
  and are stripped from your document in the HTML output.

  implicit link name shortcut: omit the name of the link, in which case the
  link text itself is used as the name. Just use an empty set of square
  brackets.
  
  .. code:: markdown
  blah blah [link text][].

  [link text]: url "title"

- url can be absolute or relative or url fragment or whatnot.

- automatic link. for url and email: simply surround the URL or email address
  with angle brackets. ``<url>``, 这样 url 本身同时为 href & link text.

emphasis
--------
- ``*`` or ``_``. 一对时等于 ``<em/>``, 两对时等于 ``<strong/>``.

inline code
-----------
- use backtick. To include a literal backtick character within a code span, you
  can use multiple backticks as the opening and closing delimiters.

  The backtick delimiters surrounding a code span may include spaces — one
  after the opening, one before the closing. This allows you to place literal
  backtick characters at the beginning or end of a code span.

images
------
- inline image: ``![alt text](url "title")``.

- reference image: ``![alt text][id]``. 然后使用 link reference 完全相同的方式
  定义 id.

comment
-------
- markdown 没有 comment syntax. 但我们可以 hack:

  * method 1. 使用标准 html comment ``<!-- eee -->``.

  * method 2. abuse reference link syntax::

        [//]: # (comment)
