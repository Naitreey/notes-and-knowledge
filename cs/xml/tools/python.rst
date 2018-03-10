xml.etree.ElementTree
=====================
ElementTree 和 Element 的区别: 前者只是一个 simple wrapper class, 用于处理在
tree level 的对 xml 文件的读写 (write/parse 等 methods), 是从 file 到 element
中间的过度. 后者则是对 xml element 结构的封装, 用于处理各种 xml 结构类操作.
从 tree 至 element, 通过 getroot, 从 element 至 tree 通过 ElementTree constructor.

Elements with no subelements will test as False. 以后会修改这个行为, 但是目前
只能通过明确地 ``element is None`` 来判断.

从一个 tree 取得的所有 elements 都是仍与这个 tree 相关联的. 所以可以做 in-place
modification.
