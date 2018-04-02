overview
========
- JavaScript, abbreviated JS.

- interpreted language. V8 implementation has JIT engine, JS code is
  pre-compiled to machine code then executed.

- weakly typed. type conversion may happen implicitly.

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

methods
^^^^^^^

- ``toFixed()``.

object
------

abstract operations
===================

type conversion
---------------
- implicit type conversion is designed to help you!!! (OK.) But it can create
  confusion if you haven't taken the time to learn the rules that govern its
  behavior.

to boolean
^^^^^^^^^^
- Undefined: false.

- Null: false.

- Boolean: argument.

- Number:

  * +0, -0, NaN: false.

  * otherwise: true.

- String:

  * emptry string: false.

  * otherwise: true.

- Symbol: true.

- Object: true.

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
Declarations create variables. Variables must be declared before being used.

- const.

- var.

block statement
---------------
::

  { [statements] }

- AKA compound statement.

- a block statement can be used anywhere a normal statement can. e.g.::

    var a = 1, b = 2; {
        console.log(a);
    }

- lexical scoping rules:

  * Variables declared with ``var`` do not have block scope.

  * Variables declared with ``let`` and ``const`` do have block scope.

- ``}`` marks the end of a block statement. Any other statement is free to show up
  after that. E.g.::

    {
        console.log(1);
    } let a=1; {
        console.log(a);
    } {
        console.log(a);
    }

conditional statements
----------------------

if statement
^^^^^^^^^^^^

switch statement
^^^^^^^^^^^^^^^^

iteration statements
--------------------

while statement
^^^^^^^^^^^^^^^

do-while statement
^^^^^^^^^^^^^^^^^^

for statement
^^^^^^^^^^^^^

flow control statements
-----------------------

return statement
^^^^^^^^^^^^^^^^

function statements
-------------------

function declaration statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  function <identifier> ([param, ...]) {
      [statements]
  }

- function declaration creates a lexical scope. (Can be interpreted as
  containing a block statement.)

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

Execution model
===============

Resolution of names
-------------------
- lexical scope rule: code in one scope can access identifiers of either that
  scope or any scope outside of it. This includes reading and writing to the 
  identifier.

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
