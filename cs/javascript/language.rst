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

identifier
----------
If we consider only ASCII chars, identifier must consists of
a-z, A-Z, 0-9, $, or _. And it must not starts with number.

data types
==========

- Unlike python, object is just one of the basic builtin types.
  In other words, string, number, etc. are all distinct types
  as basic as object type. object is not base type of all types.

  Therefore, string, number, etc. does not have hash-map-like
  functionality.

- Majority of data types have a corresponding function that have
  two purpose:

  * as type constructor.

  * as type conversion function.

- autoboxing. When accessing a primitive value's property, it is
  automatically "boxed" by a wrapper object.


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

array
^^^^^
``array`` is a subtype of ``object``.

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

function
^^^^^^^^

``function`` is a subtype of object.

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

statements
==========
In js, statement normally ends with ``;``.

declarations and variable statements
------------------------------------
- Declarations create variables. Variables must be declared before being used.

const
^^^^^

let
^^^

- ``let`` declaration create variables that respect block scope.

- ``let`` declaration don't do hoisting::

    function foo() {
        console.log(x); // raise ReferenceError.
        let x = 1;
        console.log(x);
    }

var
^^^

- variables declared by ``var`` have function scope or global scope, but not
  block scope.

- hoisting. Wherever a ``var`` appears inside a scope, that declaration is
  taken to belong to the entire scope and accessible everywhere throughout.

  In other words, ``var`` declarations are always replaced by compiler to
  the top of the current effective scope. If variable is initialized at
  declaration, the initialization part remains at the original location::

    function foo() {
        console.log(x); // undefined
        var x = 1;
        console.log(x); // 1
    }

    // equivalent to

    function foo() {
        var x;
        console.log(x);
        x = 1;
        console.log(x);
    }

  Var hoisting should NOT be relied upon.

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

- function declaration creates a lexical scope. (a function scope.)

- ``var`` declarations in function has function scope.

- hoisting. Wherever a function declaration is inside a scope, that declaration
  is taken to belong to the entire scope and accessible everywhere throughout.

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

equality operators
------------------

equality comparison
^^^^^^^^^^^^^^^^^^^
::

  == !=

- loose equality.

- type coercion is allowed under the hood.

- logic:

  * if both types are the same, perform strict equality comparison.

  * coerce one or both values to a different type until the types match, where
    then a simple value equality can be checked.

strict equality comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  === !==

- strict equality.

- type coercion is not allowed.

- When both types are the same:

  * if both are objects, comparisons will simply check whether the references
    match, not anything about the underlying values.

relational operators
--------------------
::
 
  < > <= >=

- type coercion is allowed.

- logic.

  * if both are strings, they are compared lexicographically.

  * if at least one of both is not string, they are coerced to numbers
    then compared.

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

- If an identifier is not found, ReferenceError exception is raised,
  except when it is used as operand of ``typeof`` operator.

- Setting a variable that hasn't been declared will create the variable
  in global scope. DON'T DO IT.

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
