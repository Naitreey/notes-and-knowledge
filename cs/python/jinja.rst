language
========

以下主要记录需要注意的点以及与 django template 的不同之处.

jinja 由于应用场景更加宽泛, 不仅仅是 render html, 因此它的一些默认配置和设计
决策与 django template 有所不同. (例如, 是否 automatic html escaping.)

- ``{{# ... #}}`` 是 block comment.

- 访问 attribute/key 值时, 除了 ``.`` operator 之外, python 的 index syntax
  ``[]`` 也是支持的.

  * ``foo.bar`` 的解析顺序:

    - getattr(foo, bar)

    - foo.__getitem__(bar)

    - undefined value

  * ``foo['bar']`` 的解析顺序:

    - foo.__getitem__(bar)

    - getattr(foo, bar)

    - undefined value

- filter 的参数放在 ``()`` 中: ``val|filter(arg)``

- 多次输出同一个 block: 使用 ``{{ self.<blockname>() }}``, 其中 blockname 是要
  重复输出的 block 名字.

- super block ``{{ super() }}``.

- jinja 默认不对输出做 automatic html escaping.

- 若要输出 literal 的 template control syntax, 可以直接作为字符串写出, 或用
  ``raw`` statement.

- control structure
