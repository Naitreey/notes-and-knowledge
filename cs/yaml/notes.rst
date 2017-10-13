YAML Character Stream
---------------------
- Documents

  * A YAML character stream may contain several documents. Each document is
    completely independent from the rest. 也即, 一个 yaml file 中可以包含
    多个 yaml document.

  * directive end marker: ``---``. 表示 directive 部分结束, document 部分开始.

  * document end marker: ``...``. 表示 document 部分结束, 后面可以继续 directive
    或者新的 document.
