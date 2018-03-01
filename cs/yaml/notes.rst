YAML Character Stream
=====================
Documents
---------

* A YAML character stream may contain several documents. Each document is
  completely independent from the rest. 也即, 一个 yaml file 中可以包含
  多个 yaml document.

* directive end marker: ``---``. 表示 directive 部分结束, document 部分开始.

* document end marker: ``...``. 表示 document 部分结束, 后面可以继续 directive
  或者新的 document.

Structure
=========

Node properties
---------------

anchors
~~~~~~~

- ``&`` marks a node for furture reference.

- ``*`` marks a an alias node, which refers to the most recent preceding
  node having the same anchor.

- ``<<`` extends a node with alias node.

examples::
    foo: &anchor
        k1: 1
        k2: 2

    bar:
        <<: *anchor
        k3: 3
        k4: 4

anchor 和 alias 为 YAML 提供了变量赋值和引用功能.
