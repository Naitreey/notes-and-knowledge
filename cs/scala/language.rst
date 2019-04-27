overview
========
- A general-purpose language

- invented by Martin Odersky, maintained by ScalaCenter (at EPFL) and
  LightBend.

- scala the name: scalable language -- signifying that it is designed to grow
  with the demands of its users.

- support OOP and FP programming paradigms.

  * its OOP support: every value is an object, traits, Classes are extended by
    subclassing and a flexible mixin-based composition mechanism as a clean
    replacement for multiple inheritance.

  * its FP is strongly influenced by Scheme, Standard ML, Haskell etc.,
    including: every function is a value, no distinction between statements and
    expressions, currying, higher-order functions, type inference,
    immutability, lazy evaluation, case classes, pattern matching.

- type system.
  
  * strong type checking, static typing system

  * Advanced type system, supporting algebraic data types, covariance and
    contravariance, higher-order types, annoymous types.

  * support: inner classes and abstract type members as object members,
    structural types, path-dependent types, compound types, explicitly typed
    self references, generic classes, polymorphic methods, upper and lower type
    bounds, variance, annotations, implicit parameters, conversions, views.

type hierarchy
==============
Any
---
- The supertype of all types -- the top type.

- defines certain universal methods.

AnyVal
------
- subclass of Any.

- AnyVal represents value types.

- 9 predefined value types and they are non-nullable:
  Double, Float, Long, Int, Short, Byte, Char, Unit, Boolean.

- Like in Java, AnyVal *subclasses* are stack allocated, wherever possible (例
  如作为 local variable 等 automatic storage duration 的量就可以是
  stack-allocated, 作为类成员、实例成员等 dynamic storage duration 的量就需要
  dump-allocated).

- AnyVal 子类的实例 (注意不是 AnyVal 本身的实例) 当在栈上分配时, 不使用指针
  引用的方式. 而是变量本身就是值.

AnyRef
------
- subclass of Any.

- AnyRef represents reference types. In Java runtime, AnyRef corresponds to
  java.lang.Object.

- Every user-defined type in Scala is a subtype of AnyRef.

Unit
----
- Subclass of AnyVal.

- Unit type has exactly one singleton value ``()``.

- usually used for method's return type, meaning nothing to return. (similar to
  void in Java and C.)

- 由于每个 scala expression/statement 都必须有值, 没有合适的返回值时就使用
  Unit.

Tuple
-----
- A tuple is a value that contains a fixed number of elements, each with a
  distinct type.

- Tuples are immutable.

- A tuple type is associated with its elements' types:

  * ``TupleN[e1_type, e2_type, ...]``, N 从 1-22, inclusive.

  * Shorthand form: ``(e1_type, e2_type, ...)``

- instantiation.

  * N = 1 时, 必须使用 ``Tuple1(e)`` 形式

  * N >= 2 时, 可以使用 ``TupleN(e1, e2, ...)``, 或 ``(e1, e2, ...)``.

- Access elements. 每个元素是 tuple instance 上名为 ``_n`` 的属性值. 所以, 对于
  获取第 n 个元素, 使用 ``tuple._<n>``.

pattern matching on tuples
^^^^^^^^^^^^^^^^^^^^^^^^^^
- scala 支持类似 python 中的 iterable unpacking assignment 语法. 在 scala 这
  属于 pattern matching 的一种形式.

  .. code:: scala

    val (a, b) = tuple

Null
----
- Null is a special subtype of all reference types.

- Null has a singleton value ``null``.

- Null is provided mostly for interoperability with other JVM languages and
  should almost never be used in Scala code.

Nothing
-------
- Nothing is a special subtype of all types -- bottom type.

- There's no value that has type Nothing.

- It is the type of an expression which does not evaluate to a value, or a
  method that does not return normally. A common use is to signal
  non-termination such as a thrown exception, program exit, or an infinite
  loop.

type casting
------------
- rules:

  * Byte -> Short -> Int -> Long -> Float -> Double

  * Char -> Int

- Casting is unidirectional. 即不能向下做 type casting.

expression
==========
- expressions are computable statements.

named values
------------
::

  val x[: <type>] = <expression>

- 从 FP 的角度来看, 在对函数的一次运算过程中, 它参数的输入值是固定不变的. 因此
  一个 ``val`` 量不能被重新赋值.

- type can be ignored if it can be correctly inferred from the computation.

blocks
======
::

  { ... }

- A block is a multi-line expression.

- The result of the last expression in the block is the result of the overall
  block.

functions
=========
- Functions are expressions that take parameters.

anonymous function -- lambda expression
---------------------------------------
::

  (<param>, ...) => <expression>

- On the left of => is a list of parameters. On the right is an expression
  involving the parameters.

- lambda expression 的定义可以通过 ``_`` placeholder 来简化. 此时只需在
  expression 中需要参数化的位置用 ``_`` 来代替即可.

partial application -- currying
-------------------------------
- 使用 ``_`` placeholder 参数化的方式是构建 partial application (currying) 的一
  种方式. 如果转化成 ``=>`` 的完整形式, 就会发现这样本质上不过是定义了一个
  function wrapper, 固化了部分参数而已.

- ``f _`` 是另一种构建 partial application 的方式.

methods
=======
::

  def <name>[(<param>, ...)[(<param>, ...)]...][: <type>] = <expression>

- Methods are defined with the ``def`` keyword. ``def`` is followed by a name,
  parameter lists, a return type, and a body.

- A method can take 0 to many parameter lists.

- parameter definition syntax.

  * a parameter can have default value, which makes it optional at call site.

- Scala allows nested method definition.

- When a method takes 0 parameters, the parameter list can be omitted during
  method call.

- parameter passing syntax.

  * can be positional form.

  * can be keyword argument form.

  * can be a mixture of positional and kwargs form.

main method
-----------
- The ``main`` method is an entry point of a program.
  
- JVM requires a main method to be named ``main`` and take one argument, an
  array of strings.

classes
=======
::

  class <name>[(<param>, ...)][ {
    // definitions
  }]

- Constructor.
  
  * Unlike many other languages, the primary constructor is in the class
    signature.

  * Constructor definition syntax is the same as normal methods.

  * names in constructor list automatically become the data members of the
    class.

  * When the constructor list is not specified, a default constructor with no
    parameters is used.

- members accessibility.

  * members are public by default.

  * Can be made private by ``private`` access modifier.

  * Primary constructor parameters without ``val`` or ``var`` are private;
    whereas with ``val`` or ``var`` are public by default.

- inheritance.

  * A class can inherit only one base class with ``extends`` keyword.

  * A class can be composed with multiple trait mixins with ``with`` keyword.

  * The mixin traits and base class can have the same superclass.

- The simplest class definition::

    class <name>

- class instantiation.
  
  * instantiate a class with ``new``.

  * constructor call syntax is the same as normal method calls.

- To override a parent class's method, use prefix ``override`` keyword to
  method definition.

- getter/setter syntax.

  * getter: a parameterless method whose name is property name to get and whose
    body returns a value.::

      def property = <expression>

  * setter: a method whose name is ``<property>_=`` and that takes a value to
    set.::

      def property_=(value) = <expression>

    注意 ``_=`` suffix 代表这是 setter method.

case classes
============
::

  case class <name>(<param>, ...)

- member accessibility.

  * constructor parameters are public and immutable (``val``) by default.

  * It's possible to make members mutable by ``var``, but it's discouraged.

- comparison.

  * Case classes are compared by structure and not by reference.

- instantiation.
  
  * Case classes can be instantiated with or without ``new`` keyword. This is
    because case classes have an apply method by default which takes care of
    object construction.

- A minimal case class::

    case class A()

- Tuple 与 case class 之间的选择.
 
  * Case class 的意义在于属性可由名称获取. The names can improve the
    readability of some kinds of code.

  * Tuple 可用于 easy unpacking and pattern matching.

- Case classes are good for modeling immutable data.

instance methods
----------------
- ``copy()``. create a shallow copy of this instance.

objects
=======
::

  object <name> {
    // definitions
  }

- Objects are single instances of their own definitions.

- The object can be accessed by its name.

traits
======
::

  trait <name> {
    // definitions
  }

- Traits are used to share interfaces and fields between classes.

- Traits are types containing certain fields and methods. Multiple traits can
  be combined.  Traits can also be defined as generic types.

- Trait/Class can extend traits with the ``extends`` keyword and implement
  abstract methods or override the default implementation with the ``override``
  keyword.

- Class can be composed by traits as mixins, with ``with`` keyword.
  
- Trait itself is abstract, therefore can not be instantiated.

- Abstract methods of traits can have default implementations.

runtime systems
===============
JVM runtime
-----------
- compiles to Java bytecode. executable code runs on JVM. In fact, Scala code
  can be decompiled to readable Java code, with the exception of certain
  constructor operations. To the Java virtual machine (JVM), Scala code and
  Java code are indistinguishable.

- interoperability with Java. libraries written in Java or Scala may be
  referenced in code of either language.

JavaScript runtime
------------------
- Scala.js -- A scala compiler that compiles scala source to js code, making
  it possible to run on browser.

Native runtime
--------------
- Scala Native -- A scala compiler that targets the LLVM compiler
  infrastructure.

tools
=====
- sbt

- scastie

- scaladex

- scala.js

- scalafiddle
