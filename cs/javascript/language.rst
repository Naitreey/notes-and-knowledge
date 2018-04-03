overview
========
- JavaScript, abbreviated JS.

- interpreted language. V8 implementation has JIT engine, JS code is
  pre-compiled to machine code then executed.

- weakly typed. type coercion may happen implicitly.

definitions
===========

- host object: object supplied by the host environment. e.g.,
  window, document, XMLHttpRequest, etc.

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

Some cases when undefined is resultant:

- an undefined variable's type is ``"undefined"``. But it results in
  ``ReferenceError`` if used directly.

- an declared variable's default value is ``undefined``.

- A function returns ``undefined`` if nothing is returned explicitly via
  ``return`` statement.

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
a dict, a hash map. like a python object and dict combination.

- properties can be accessed as attributes (dot notation) or
  keys (bracket notation).

- dot notation can be used only when property name is a valid identifier,
  and is a known literal.

- object keys can only be string.

Array
^^^^^
``Array`` is a subtype of ``object``.

- Because array is object, it is theoretically possible to use array like
  an object, i.e., save named property in an array object::

    > var x = [];
    undefined
    > x.sef = "xxx";
    'xxx'
    > x
    [ sef: 'xxx' ]
    > x[0]='rrr';
    'rrr'
    > x
    [ 'rrr', sef: 'xxx' ]
    > x[2]='yyy';
    'yyy'
    > x
    [ 'rrr', <1 empty item>, 'yyy', sef: 'xxx' ]
    > x['bbb'] = 'aaa';
    'aaa'
    > x
    [ 'rrr', <1 empty item>, 'yyy', sef: 'xxx', bbb: 'aaa' ]

  However, this would generally be considered improper usage of the respective
  types.

Function
^^^^^^^^

``Function`` is a subtype of object.

- function object can store properties like normal object. This is sometimes
  useful::

    > function x() {}
    undefined
    > x
    [Function: x]
    > x.r
    undefined
    > x.r=1
    1
    > x
    { [Function: x] r: 1 }
    > x.p=2
    2
    > x
    { [Function: x] r: 1, p: 2 }

abstract operations
===================

type coercion
-------------
- implicit type coercion is designed to help you!!! (OK.) But it can create
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

- type coercion may be performed under the hood.

strict equality comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^
- strict equality.

- type coercion is not performed.

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

unary operators
---------------

typeof
^^^^^^
return string name of the type of the operand.

- Undefined: "undefined"

- Null: "object". **Note** it's not "null"[1]_.

- Boolean: "boolean".

- Number: "number"

- String: "string"

- Symbol: "symbol"

- Object:

  * host object: implementation-dependent

  * object that implements Call: "function"

  * otherwise: "object"

.. [1] In the first implementation of JavaScript, JavaScript values were
       represented as a type tag and a value, with the type tag for objects being 0,
       and null was represented as the NULL pointer (0x00 on most platforms). As a
       result, null had 0 as a type tag, hence the bogus typeof return value.

void
^^^^
evaluates the given expression and then returns ``undefined``.

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
