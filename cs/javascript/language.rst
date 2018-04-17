overview
========
- JavaScript, abbreviated JS.

- interpreted language. V8 implementation has JIT engine, JS code is
  pre-compiled to machine code then executed.

- weakly typed. type coercion may happen implicitly (WTFJS_).

- JS 与 C/Python/Java 的一大区别是, JS 强调 async 概念. 异步思想和
  编程范式深深嵌入 JS 的整个语言. 可以说, JS 最独特的思想就是单线程
  异步并发思想. JavaScript has a concurrency model based on an 
  "event loop". 常用的很多 builtin function 等都是异步的. JS engine
  has builtin event loop.

definitions
===========

- host object: object supplied by the host environment. e.g.,
  window, document, XMLHttpRequest, etc.
  
  Host objects are not defined by spec. They are implemented and provided by
  host environment, which is browser, nodejs interpreter, etc. These objects
  are implemented as builtin part of host environment. So they may be
  implemented in C/C++, and just a js wrapper.

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
  as basic as object type. object is not base type of *all* types
  (WTFJS_).

  Therefore, string, number, etc. does not have hash-map-like
  functionality.

- Majority of data types have a corresponding function that have
  two purpose:

  * as type constructor.

  * as type conversion function.

- autoboxing. When accessing a primitive value's property, it is
  automatically "boxed" by a wrapper object (WTFJS_).


undefined
---------

Some cases when undefined is resultant:

- an undefined variable's type is ``"undefined"`` (WTFJS_). But it results in
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

``function`` is a subtype of object. A function is a callable object.

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

- constructor ``Function()``.

abstract operations
===================

type coercion
-------------
- implicit type coercion is designed to help you!!! (WTFJS_) But it can create
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

- In JS, compiler only declares variables in scope during compilation stage;
  it's engine's job to assign variable to the specified value during runtime.

  Thus for a variable declaration with initial value, it's equivalent to two separate
  statement and executed separately (in different execution stage)::

    var x = 1;
    // ---
    var x; x = 1;

  Note: variables are declared at compile-time, doesn't mean variables can be
  referenced before reaching declaration statement at runtime. This hoisting
  behavior is only specific to ``var`` declaration.

  In other words, for ``var`` declarations, the following two are equivalent::

    function foo() {
        console.log(x);
        var x = 1;
    }

    function foo() {
        var x;
        console.log(x);
        x = 1;
    }

  But for ``let``, ``const`` declarations, hoisting does not happen at all::

    function foo() {
        console.log(x);
        let x = 1;
    }

    function foo() {
        console.log(x);
        let x; x = 1;
    }

  It is only for ``var`` statement that the declared variable is made available
  to entire scope; for ``let``, ``const`` statements, the declared variable is 
  only available from the point of declaration until the end of scope.

let
^^^
::

  let var1 [= value1] [, var2 [= value2]] ...;

- ``let`` declaration create variables that respect block scope.

- Within the same scope, duplicated ``let`` declarations raise ``SyntaxError``.

- Temporal dead zone (TDZ). ``let``-declared variables are only visible from
  the point of declaration until the end of block scope. from the beginning of
  block scope until before the point of declaration is called the variable's
  TDZ.

  Effects of TDZ:

  * Because of TDZ, ``let`` does not do hoisting.
    ``let`` declaration don't do hoisting::
  
      function foo() {
          console.log(x); // raise ReferenceError.
          let x = 1;
          console.log(x);
      }

  * Because of TDZ, using the ``typeof`` operator to check for the type of a
    variable in that variable's TDZ will throw a ``ReferenceError``, unlike
    those simply undefined variables.

  * Note TDZ starts from beginning of scope until the point of ``let`` **lvalue**
    resolution. some confusing examples::

      function test(){
         var foo = 33;
         if (true) {
            let foo = (foo + 55); // ReferenceError, rvalue `foo` still in TDZ.
         }
      }
      test();

      function go(n) {
        // n here is defined!
        console.log(n); // Object {a: [1,2,3]}
      
        for (let n of n.a) { // ReferenceError. this `n` is declared in an implicit block
          console.log(n);    // via ``let n = n.a;`` which makes rvalue `n.a` in TDZ.
        }
      }
      
      go({a: [1, 2, 3]});
      
- advantages to declaring variables using block scope.

  * the principle of least privilege/exposure.

  * to be more memory-efficient. out of scope stuffs are garbage-collected.

const
^^^^^
- const is just like let, except that the const-declared variables are read-only.
  Any attempt to modify its value will raise a ``TypeError`` exception.

var
^^^
::

  var var1 [= value1] [, var2 [= value2]] ...;

- **let is new var. Stop using var.** (ES6)
  There is basically no use for ``var`` given ``let`` is available.

- variables declared by ``var`` have function scope or global scope, but not
  block scope.

- Within the same scope, duplicated ``var`` declarations are ignored (WTFJS_).
  But note the assignment is not ignored.

- hoisting. Wherever a ``var`` appears inside a scope, that declaration is
  taken to belong to the entire scope and accessible everywhere throughout
  (WTFJS_).

  It is effectively equivalent to say ``var`` declarations are displaced to
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

  Note that only declaration is hoisted, assignment part is left in place.
  Otherwise, program logic would be different.

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
- for loop 实际上创建了两个 block scope. header 位于 outer block,
  loop body 是 inner block.::

    for (<h1>; <h2>; <h3>) {
        <body>
    }
    // conceptually similar to
    {
        <h1>
        while (<h3>) {
            <body>
            <h2>
        }
    }

  In other words, 在 header 中创建的变量, 只创建一次. 在各次循环中
  可用.

- ``let`` for loop vs ``var`` for loop.

  * let confines loop variables in block scope, which is good.

  * let for loop has a weird rebinding behavior, which should be avoided.
    在每次循环进入 body block 时, 与 header variable 同名的变量被创建,
    初始化为 loop variable 当前值. 在退出 body block 时, 该变量的当前值赋值
    给 loop variable. [SOLetLoop]_ (WTFJS_)::

      for (let i = 0; i < 3; i++) {
          console.log(i);
      }
      // prints 012
      // equivalents to the following sanity version
      for (let i = 0; i < 3; i++) {
          let j = i;
          console.log(j);
          i = j;
      }

flow control statements
-----------------------

return statement
^^^^^^^^^^^^^^^^

try statement
-------------
::

  try {
    ...
  }
  catch (exc) {
    ...
  }
  finally {
    ...
  }

- at least one of ``catch`` and ``finally`` must be present with ``try``.

- ``catch`` block creates a block scope. The ``exc`` exception variable
  is declared in the block scope, thus not available outside of it.

- JS does not support multi-catch statement based on exception class, as
  they do in Python. We can manually construct it using conditionals::

    try {
        ...
    }
    catch (e) {
        if (e instanceof ...) {
            ...
        }
        ...
        else {
            ...
        }
    }

function statements
-------------------

function declaration statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  function <identifier> ([param=default, ...]) {
      [statements]
  }

- function declaration creates a lexical scope. (a function scope.)

- ``var`` declarations in function has function scope.
  
  ``var`` + function scope is fine enough for normal programming requirements.
  That's almost all we have in Python.

- hoisting. Wherever a function declaration is inside a scope, that declaration
  is taken to belong to the entire scope and accessible everywhere throughout
  (WTFJS_).

  Function variable and function definition is hoisted together. This is
  different from ``var`` hoisting.

  Function declaration is hoisted before ``var`` declaration. For duplicate
  function declarations, the latter override the former.

  Note that function expression does not hoist of course. The following code
  may trick you::

    func(); // `TypeError`, NOT `ReferenceError`. As `func` is hoisted.
    var func = function func() {
        ...
    }

- Special note on block-level function declaration (ES6) [SOBLKFUNC]_ (WTFJS_).

  * In strict mode, function declared in block scope is hoisted in the scope,
    and only visible inside the block scope. Reference the same identifier
    outside of defining scope raises ``ReferenceError``.::

      "use strict";
      foo(); //ReferenceError
      if (true) {
         function foo() { console.log( "a" ); }
      }
      else {
         function foo() { console.log( "b" ); }
      }
      foo(); //ReferenceError

  * In non-strict mode, function identifier is hoisted to the nearest function
    or global scope, but function definition is not visible until declaration
    statement is reached. After that, the definition is visible until the end
    of nearst function or global scope.::

      /* var foo; */ // implicit hoisting.
      foo(); // TypeError
      if (true) {
         function foo() { console.log( "a" ); }
      }
      else {
         function foo() { console.log( "b" ); }
      }
      foo(); // a

- When function is called, its formal parameters are set values sequentially
  corresponding to argument list. All remaining formal parameters fall back to
  their default values. If ``default`` is unspecified, it's ``undefined``.

- Differing from variable declaration with initial value, function declaration
  is handled entirely by compiler: compiler handles both the function name
  declaration in scope and function body definition during code-generation.

- JS 中, 由于 ``this`` 是根据调用情况自动赋值的, 一个函数本身可以既做单纯的
  函数来使用, 也可以作为 object bound method 使用. 而如果要作为 class unbound
  method 使用, 需要使用 ``Function.prototype.call()``, ``Function.prototype.apply()``.

with statement
--------------
deprecated.

It makes compiler disable compile-time optimization, leading to slower code.

In strict mode, ``with`` statement is disallowed.

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

Primary expression
------------------

this keyword
^^^^^^^^^^^^
- ``this`` can not be assigned directly. It is a special keyword, rather than
  a variable (unlike ``self`` in python). Its value is assigned by JS engine,
  and dependent on its current runtime environment.

- the value of ``this``.

  * global context. ``this`` refers to global object.
  
  * function context. depends on how function is called (call-site and context
    object).

    - simple call. ``this`` defaults to global object, except when its value is
      set by the call. In strict mode, ``this`` remains at whatever it was set
      to when entering the execution context, which defaults to undefined.

    - with ``Function.prototype.call()``, ``Function.prototype.apply()``. set
      ``this`` value for function call. 这个用法相当于在 python 中, 给 class
      unbound method 传递 self 对象来直接调用. 假装对象有这个方法.

    - ``Function.prototype.bind()``. create a new function with ``this`` bound
      to the specified object, regardless how the new function is being used.

    - called via a context object's method reference. ``this`` is set to the
      context object.

      注意如果 method reference 之后没有直接 call function, 而是通过 simple
      call 的方式去调用, 这是符合 simple call 的情况的. 此时 ``this`` 是 global
      object. (WTFJS_) 这是因为无论函数在哪里定义 (单独声明, 还是在 object
      attribute 赋值 function expression), 创建的结果都是相同的 function object.
      只有调用的方式最终决定 ``this`` binding.::

        var x = {};
        var m = function () { console.log(this) };
        x.m = m;
        x.m(); // {m: [Function]}
        var y = x.m;
        y(); // global object or undefined.

    - as a constructor. ``this`` is bound to the new object being created.
        
    - as a DOM event handler. ``this`` is set to the element the event fired from.

    - When ``this`` appears in an inline event handler, ``this`` is set to the DOM
      element on which the listener is placed. Note only the outer code has its
      ``this`` set this way.

  * arrow function. In arrow functions, ``this`` retains the value of the enclosing
    lexical scope's ``this``.

left-hand-side expressions
--------------------------

function call expression
^^^^^^^^^^^^^^^^^^^^^^^^
::

  <call-expression> ( [argument-list] )

``(...)`` indicates ``<call-expression>`` should be executed, thus requires it callable.
Otherwise, ``TypeError`` is raised.

unary operators
---------------

typeof
^^^^^^
return string name of the type of the operand.

- Undefined: "undefined"

- Null: "object". **Note** it's not "null"[1]_ (WTFJS_).

- Boolean: "boolean".

- Number: "number"

- String: "string"

- Symbol: "symbol"

- Object:

  * host object: implementation-dependent

  * object that implements Call: "function"

  * otherwise: "object" (WTFJS_)

.. [1] In the first implementation of JavaScript, JavaScript values were
       represented as a type tag and a value, with the type tag for objects being 0,
       and null was represented as the NULL pointer (0x00 on most platforms). As a
       result, null had 0 as a type tag, hence the bogus typeof return value.

void
^^^^
evaluates the given expression and then returns ``undefined``.

equality operators
------------------

- ``===`` vs ``==``. when use which?

  when you want to allow certain degree of fuzziness in equality checking, use ``==``,
  otherwise if you wanna restrict allowed values, use ``===``.

  In other words, when you really know what you are doing (by understanding every possible
  cases that may occur as your operands), you may use ``==``; othwerwise stick to ``==``.

equality comparison
^^^^^^^^^^^^^^^^^^^
::

  == !=

- loose equality.

- type coercion is allowed under the hood (WTFJS_).

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

- type coercion is allowed (WTFJS_).

- logic.

  * if both are strings, they are compared lexicographically.

  * if at least one of both is not string, they are coerced to numbers
    then compared.

assignment operators
---------------------
assignments are operators. thus assignment is an expression, unlike python.

conditional operator
--------------------
::

  <boolean-expression> ? <expr1> : <expr2>

function expressions
--------------------

function expression
^^^^^^^^^^^^^^^^^^^
only issues specific function expression is recorded here.
For all other aspects and descriptions refer to `function declaration statement`_
section.

- ``function`` keyword can be used to define a function expression inside
  another expression.

- function name. You should always provide a name to your function expression.
  [SOnamedFuncExp1]_ [SOnamedFuncExp2]_

  * function name is local to function body::

      let func = function func() {
        ...
      }
      // equivalent to
      let func = function () {
        var func = // some kind of self reference
      }

  * function name is required if function is recursive, i.e. it needs to call
    itself inside function body.

  * function name is required when an event handler function wants to unbind itself
    after it fires.

  * anonymous function:
    If function name is omitted in function expression, it is inferred based on
    defining context, e.g., used as RHS of assignment, as object property value,
    etc., which eventually becomes ``function.name`` attribute. If not inferred,
    ``function.name`` is ``""``, which is anonymous function.

  * named function can be seen in stack traces, call stacks, list of breakpoints, etc.

  * Even if name is not required, sometimes it helps to document your intent, e.g.::

      some_operation_with_callback(function success() {...}, function failed() {...})

  * if function expression is used for assignment, name is not very useful::

      let foo = function () {...};

    But why needs assignment anyway? Just use function declaration statement is fine
    enough::

      function foo() {
          ...
      }

- Immediately invoked function expression (IIFE)::

    (function IIFE() {
        ...
    })();

  or::

    (function IIFE() {
        ...
    }())

  The outer ``(...)`` that surrounds IIFE is needed to prevent it from being
  treated as a function declaration statement.

  IIFE is often used as a purely executed chunk of code, to prevent polluting
  global namespace. Many libraries use this trick.

arrow function expression
^^^^^^^^^^^^^^^^^^^^^^^^^


modules
=======

historical notes
----------------
There are two kinds of JS modules:

- ES5 module pattern: Before ES6, JS language has no builtin module mechanism
  (WTFJS_).  Using function and closure to emulate lousy module/class
  interface. These are standardized by AMD, CommonJS and UMD libraries. See
  `modules <modules.rst>`_.

- ES6 builtin module syntax.

The most important difference between the two is that:

* module pattern is a hack that works well. They are essentially normal objects,
  functions with closures and so forth. They just looks like modules or
  classes. They works like module/class (rather than normal objects/functions)
  only at runtime. For compiler, they are not any special than other functions,
  objects. In other words, the "module/class" semantics 是由程序员赋予的, 并且
  只在 runtime 存在.

* ES6 module syntax is defined at language level and implemented by interpreter.
  The semantics is recognized by compiler at compile-time. Compiler is responsible
  to perform necessary checks/optimizations and throw early errors if one exists.

Here we focus on ES6 modules.

overview
--------

- Each JS source file is a module.

- Each module can import another module entirely or only individual members of it.

- Each module can export a set of public APIs that is importable by other modules.


built-in objects
================

built-in functions
------------------

eval()
^^^^^^
take JS code in string and execute it at current runtime execution point.  Code
can contain an expression or a suite of statements.  Return value is the return
value of executed JS code::

  eval('2+2') -> 4
  eval('var x = 1;') -> undefined

Disadvantages:

- makes JS code slow.

  * it has to invoke the JS interpreter.

  * modern javascript interpreters convert javascript to machine code. This
    means that any concept of variable naming gets obliterated. Thus, any use
    of eval will force the browser to do long expensive variable name lookups
    to figure out where the variable exists in the machine code and set it's
    value. Additonally, new things can be introduced to that variable through
    eval() such as changing the type of that variable, forcing the browser to
    reevaluate all of the generated machine code to compensate.

- security risk.

In strict mode, ``eval()`` is executed in its own lexical scope, which makes it
impossible to modify program's lexical scope. In this case, only ``eval()``
program logic's side effect and its return value have impact on calling program.

compilation
===========
- modern JS interpreters convert JS code to machine code (JIT) during execution.

Execution model
===============

- code execution is managed by javascript runtime engine. It is distinct from
  js compiler.

Scope
-----
- JS use lexical scope.
  lexical scope rule: code in one scope can access identifiers of either that
  scope or any scope outside of it. This includes both lvalue & rvalue
  resolution.

  * For rvalue, if an identifier is not found, ``ReferenceError`` exception is
    raised, except when it is used as operand of ``typeof`` operator.
  
  * For lvalue, if a variable could not be found by traversing nested scope until
    global scope, it will be created in global scope. DON'T DO IT.
  
    Unless in strict mode, this will raise ``ReferenceError``.
  
- An identifier defined in inner scope shadows the identifier of the same name
  defined in the outer scope.

- Global scope is represented by global object. In browser, it's ``window``. In
  nodejs, it's ``global``.

- lexical scope and iteration statements. Iteraction statements typically contains
  a block scope (with block statement). The point is that for every loop iteration,
  a different lexical block scope is created. 这对于 closure 非常重要, 当一个函数
  的执行涉及 closure over loop-created lexical scope 时, 它只能访问函数定义时对应
  的 iteration 的 block scope.
  
  Compare::

    for (var i=1; i<=5; i++) {
        setTimeout( function timer(){
            console.log( i );
        }, i*1000 );
    }

    for (var i=1; i<=5; i++) {
        let j = i;
        setTimeout( function timer(){
            console.log( j );
        }, j*1000 );
    }

    for (var i=1; i<=5; i++) {
        (function(j){
            setTimeout( function timer(){
                console.log( j );
            }, j*1000 );
        })( i );
    } 

- There are two ways lexical scope can be modified at runtime:

  * ``eval()``, ``setInterval()``, ``setTimeout()``, ``new Function()`` etc.
    that can execute program text at runtime.
  
  * ``with`` statement, which is deprecated.

Closure
^^^^^^^
- definition.
  A function is able to remember and access its lexical scope even
  when that function is executing outside its lexical scope. The function's
  reference to its defining lexical scope is called closure. In other words,
  a function has closure over its lexical scope.

- Here the aforementioned lexical scope might be some outer function scope, or
  even global scope.  As long as when the function is executing outside of its
  original defining scope, closure happens. For closure over global scope, it
  happens when the function is executed outside of its defining module.

  A function's reference to its outer lexical scope, prevents the scope's memory
  and whatnot being GC-ed.

strict mode
===========
- pragma::

    "use strict";

  can be used in a function scope or global scope.

- ``"use strict";`` pragma must be the first statement in a specific
  lexical scope, and it is effective until the end of the specified
  scope.

- The pragma conforms lexical scope rule. In other words, whether a
  piece of code runs in strict mode depends on whether its lexical
  scope is in strict mode.::

    function foo() {
        console.log( this.a ); // non-strict mode
    }

    var a = 2;

    (function(){
        "use strict";

        foo(); // strict mode
    })();
    // prints: 2

- keeping the code to a safer and more appropriate set of guidelines.

- generally more optimizable by the engine.

- it should be used for all your codes and declared at the top of source
  file.

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

weird designs
=============
.. _WTFJS:

WTFJS-related weird language designs are labeled WTFJS.

references
==========
.. [SOnamedFuncExp1] `Why use named function expressions? <https://stackoverflow.com/a/15336541/1602266>`_
.. [SOnamedFuncExp2] `What is the point of using a named function expression? <https://stackoverflow.com/questions/19303923/what-is-the-point-of-using-a-named-function-expression>`_
.. [SOBLKFUNC] `What are the precise semantics of block-level functions in ES6? <https://stackoverflow.com/questions/31419897/what-are-the-precise-semantics-of-block-level-functions-in-es6>`_
.. [SOLetLoop] `let keyword in the for loop <https://stackoverflow.com/questions/16473350/let-keyword-in-the-for-loop>`_
