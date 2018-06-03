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
- different paradigms of programming are essentially different design
  patterns, i.e. different ways to organize your code.

procedural programming
----------------------


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
- Class is an optional design pattern in software design. You can use it or
  not.

concepts
^^^^^^^^

class
""""""
- class (or data structure), as the unit of encapsulation, which contains
  data and its associated operations (例如你能对这个类 (或者它的实例) 做什么,
  或者这个类 (或者它的实例) 能为你做什么 -- 根据它所包含的数据、状态).

- class instance. 一般来讲 class 是对象的模板. 而对象, 即实例才是真正能为你办事
  的小黄人. (当然, class 作为另一种更抽象的对象, 本身也可包含 class-level 的数据
  和操作, 即 class-level attributes 和 methods.)

three properties of OOP
""""""""""""""""""""""""

- encapsulation. 封装是 class 的天然属性. 很显然, 将一组数据和一组相应操作整理在了
  一个类这个创建的概念下. 封装也是一种模块化思想.

- inheritance. 继承是子类和父类之间的共性. 它们可以有共同的数据, 共同的方法 (即操作).

- polymorphism. 多态是子类相比父类的特性. 同一个操作, 子类可以与父类相比略有调整
  或完全不相同, 却保持相同的 API. 多态可以看作是 duck typing 的弱化形式.

  个人认为, 多态还可以指子类相比父类原创的部分, 即增加的、在父类中完全不存在的
  数据和功能. 这也是一种分化, 一种演化, 也即多态.


一个好的类体系的设计, 是一种艺术. 在一个系统中, 如何将多个相互关联的概念整理
成一个个相互作用的实体 (即 class), 如何设计实体之间的相互作用, 如何设计一系列
同类实体之间的共性和特性 (即设计抽象类与具体类的继承和多态). 这些学问, 都是
需要不断思考、不断体会的.

other concepts
""""""""""""""
- introspection. Introspection is an operation that inspects an instance at
  runtime for its class hierarchy and other static information.

- duck typing. Duck typing 是 interface/protocol 的一般化, 是一种更广泛的多态性.

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
