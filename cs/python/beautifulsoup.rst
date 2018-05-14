parser
======
html
----
- python builtin html.parser

- lxml -- recommended, for speed.

- html5lib

xml
---
- lxml-xml, xml

BeautifulSoup
=============
- A BeautifulSoup object represents the document as a whole.

- After instantiation, html entities are converted to unicode chars.

- 从 tree structure 角度看, BeautifulSoup object 可看作是只包含一个
  child 即 ``<html>`` root element 的 Tag. 它支持各种 Tag operations.

constructor options
-------------------

- data to parse. a file-like object or string.

- parser. optional. If not provided, appropriate parser is chosen.

attributes
----------

- name. fixed to ``[document]``.

Tag
===

- A Tag object is a HTML/XML element tag.

- html attributes.
 
  * element's html attributes can be accessed using key-ed index syntax.

  * If an attribute has multiple value, a list is used. For XML, there are no
    multi-valued attributes.

attributes
----------

- name. tag name.

- attrs. An element's all html attributes.

methods
-------

- ``get_attribute_list(attr)``.

navigation
----------

Going down
^^^^^^^^^^
- ``Tag.<child-tag-name>``.
  
  Tag 具有它所有 direct children elements 的名字作为该 Tag 的属性.
  注意如果有多个相同 name 的 children tags, 这样只能获取到第一个.

- ``Tag.contents``.

  给出一个 Tag 的所有 children, 包含 child elements 以及 text.

- ``Tag.children``. ditto as an iterator.

- ``Tag.descendants``. A tag's all descendants, direct and non-direct.
  As an iterator, in a left-to-right, depth-first fashion.

- ``Tag.string``. text within tag. 只有当 tag 里面只有 pure text
  没有其他内容时才设置. 否则是 None.

- ``Tag.strings``. All segments of text within all descendants of Tag.
  as a generator.

- ``Tag.stripped_strings``. ditto but strings are stripped.

Going up
^^^^^^^^

- ``Tag.parent``. The direct parent of Tag. The parent of html root element is
  BeautifulSoup object.  The parent of BeautifulSoup is None.

- ``Tag.parents``. direct and indirect parents of Tag. depth-first fashion.
  As a generator.

Going sideways
^^^^^^^^^^^^^^

- ``Tag.next_sibling``. If no next sibling, None. 注意 text 部分是算作同级 Tag
  的 sibling.

- ``Tag.previous_sibling``. ditto.

- ``Tag.next_siblings``. Successive siblings of Tag. As a generator.

- ``Tag.previous_siblings``. ditto.

In parsing order
^^^^^^^^^^^^^^^^
按照 parse-time 各个 object 的解析顺序, 来给出 next/previous element 的定义.
而不是按照 tree structure 的 siblings 关系.

例如::

  <p>a</p>b

的 ``p.next_sibling`` 是 ``b``, 但 ``p.next_element`` 是 ``a``, 这是解析的顺序.

- ``Tag.next_element``

- ``Tag.previous_element``

- ``Tag.next_elements``

- ``Tag.previous_elements``

Searching
^^^^^^^^^

filters
""""""""
以下 filters 在不同使用场景下匹配不同的内容, 可能是 Tag.name,
tag attributes etc.

- A string. matching the exact string.

- A regex object. matching the regex pattern.  regex object's ``search()``
  method is used for matching.

- A list of strings. matching any one of the exact strings.

- boolean True. Match all that has a value.

- A function object that takes one argument, returning True
  if matches.

searching methods
""""""""""""""""""
- ``find_all(name, *, attrs, recursive, string, limit, **kwargs)``

  * name. matching with tag name. All `filters`_ can be used.

  * attrs. A dict of attribute name to filter, matching attributes. All
    `filters`_ can be used for attribute match.

    - html ``class`` attribute is modified as ``class_``.

    - When a attribute has multiple values, 可以 matches any of its values
      或者也可以匹配 exact string.

  * string. search for text content (``Tag.string``). All `filters`_ can be
    used.

  * limit. limit the number of matches.

  * recursive. whether search all descendents or only direct children. default
    is True.

  * Any kwargs that’s not recognized will be turned into a filter on one of a
    tag’s attributes. which is ditto.

  All filter conditions are AND-ed.

  If you treat the BeautifulSoup object or a Tag object as though it were a
  function, then it’s the same as calling find_all() on that object.

- ``find()``

- ``find_parents()``

- ``find_parent()``

- ``find_next_siblings()``

- ``find_next_sibling()``

- ``find_previous_siblings()``

- ``find_previous_sibling()``

- ``find_all_next()``
  
- ``find_next()``

- ``find_all_previous()``
  
- ``find_previous()``

- ``select()``

NavigableString
===============

- A NavigableString object is the text within a html element.

- A NavigableString is immutable, but can be replaced.

- A NavigableString contains reference to its belongging
  BeautifulSoup parse tree object. 如果 parse tree 已经不再需要,
  在单独使用 NavigableString 时应该先转换成 pure string.

methods
-------

- ``__str__``. convert to pure python string.

- ``replace_with(string)``.

Comment
=======

- A Comment object is just a special type of NavigableString.

Other NavigableString subclasses
================================

- CData, ProcessingInstruction, Declaration, Doctype.

Modifying the tree
==================

Output
======

Guess encoding
==============
