entity
======
- first-class entity and second-class entity. it is a term that barely has a
  technical meaning.  The meaning, when present, is usually comparative, and it
  applies to a thing in a language that has more privileges than a comparable
  thing.[SOFST]_

  Usually, first-class entity is an entity that can be passed as argument to
  functions, returned from function, modified, assigned a value, etc.
  
  But this is not always the case. The exact meaning of first-class/second-class
  thing is only made clear through context.

.. [SOFST] `About first-,second- and third-class value Ask Question <https://stackoverflow.com/questions/2578872/about-first-second-and-third-class-value/2582804#2582804>`_

paradigms
=========

functional programming
----------------------
- Functional programming 似乎可以很好地使用 tail recursion, 让递归代码十分高效.
  所以 FP 从来不怕递归.

- the essence of functional programming: function as first-class entity --
  functions can be passed as arguments, can be returned from functions.

- higher-order functions: Functions which take other functions as arguments,
  and/or which return other functions as their results

object-oriented programming
---------------------------

scope
=====
- Scope is a set of nested lookup table.

- lvalue & rvalue.
  
  * lvalue. lvalue resolution aims to find the target variable container in memory.
    It happens during variable assignment.

  * rvalue. rvalue resolution aims to find the target variable's value.

lexical scope
-------------
- lexical scope is scope that is defined at lexing time.  In other words, scope
  is well-defined by variable/function/etc. declarations at author-time.

- In lexical scoping model, value resolution is performed by traversing the
  nesting of "scopes" in program text.

- Compiler construct scope structure during compilation.  Runtime engine
  lookups scope structure to resolve lvalues and rvalues.

dynamic scope
-------------
- In dynamic scoping is defined only at runtime. And it's dynamic, because the
  current scope depends on the current call stack, so it changes as program
  runs.

- value resolution is performed by traversing down stack frames.

evaluation
==========

- 两种运算类型: strict evaluation, lazy evaluation.

strict evaluation
-----------------
- all parts of an evaluation will be evaluated completely before the value of
  the expression as a whole is determined.

lazy evaluation
---------------
- In order to evaluate an expression in the language, you only evaluate as much
  of the expression as is needed to get the final result.

typing
======

- static typing and dynamic typing

- strong typing and weak typing
