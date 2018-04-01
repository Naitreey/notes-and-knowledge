overview
========
- JavaScript, abbreviated JS.

- interpreted language. V8 implementation has JIT engine, JS code is
  pre-compiled to machine code then executed.

lexical grammer
===============

comment
-------
support both types of C comment syntaxes:

- single-line: ``//``

- multi-line: ``/* */``. Can appear anywhere on a line.

data types
==========

undefined
---------

null
----

boolean
-------

string
------

symbol
------

number
------

object
------

abstract operations
===================

type conversion
---------------
- implicit type conversion is designed to help you!!! (OK.) But it can create
  confusion if you haven't taken the time to learn the rules that govern its
  behavior.

testing and comparison
----------------------

equality comparison
^^^^^^^^^^^^^^^^^^^
- loose equality.

- type conversion may be performed under the hood.

strict equality comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^
- strict equality.

- type conversion is not performed.

statements
==========
In js, statement normally ends with ``;``.

declarations and variable statements
------------------------------------
Declarations create variables. variables must be declared before being used.

variable statement
^^^^^^^^^^^^^^^^^^
var

expressions
===========

- operators::

    + - * / %
    = += *= /=
    ++ --
    . []
    == === != !==
    < > <= >=
    && ||

assignment opoerators
---------------------
assignments are operators. thus assignment is an expression, unlike python.

security
========
- 在比较老的浏览器中, 存在 JSON array 带来的 vulnerability.

  原理是, 使用 ``<script src="">`` tag 获取一个 json response,
  这个 json 是 array, 浏览器会当作 js array 去构建这个元素.
  若在其他 script 部分, 对 Array 进行了部分重定义, 则可以截取
  到 json array response 的内容. 因此, 推荐做法是 json response
  顶层一定要是 {}, 不能是 [].

  注意这种执行行为在 ES5 中已经被禁止了, 这个漏洞和 workaround
  不再必要.
