overview
========
- A general-purpose language

- invented by Martin Odersky, maintained by ScalaCenter (at EPFL) and
  LightBend.

- scala the name: scalable language -- signifying that it is designed to grow
  with the demands of its users.

programming paradigms
---------------------
- support OOP and FP programming paradigms.

- Scala's FP constructs make it easy to build interesting things quickly from
  simple parts; its OOP constructs make it easy to structure larger systems
  and adapt them to new demands.

OOP
^^^
- Scala is an OOP language in pure form -- every value is an object and every
  operation is a method call (it doesn't have static fields/methods).

- OOP support: every value is an object, traits, Classes are extended by
  subclassing and a flexible mixin-based composition mechanism as a clean
  replacement for multiple inheritance.

FP
^^
- scala's FP is strongly influenced by Scheme, Standard ML, Haskell etc.,
  including: every function is a value, no distinction between statements and
  expressions, currying, higher-order functions, type inference, immutability,
  lazy evaluation, case classes, pattern matching.

type system
-----------
- strong type checking, static typing system

- advanced type system, supporting: type inference, algebraic data types,
  higher-order types, annoymous types, inner classes and abstract type members
  as object members, structural types, path-dependent types, compound types,
  explicitly typed self references, generic classes, polymorphic methods, upper
  and lower type bounds, variance, annotations, implicit parameters,
  conversions, views.

- assess static typing system of scala.

  * 静态类型系统的好处. 见 `cs/programming-language-concepts/notes.rst#data-types`_

  * static typing system 经常具有 verbose 和 inflexible 的问题. 然而, scala 通
    过 type inference 避免了 verbosity 问题, 通过 pattern matching and several
    new ways to write and compose types 来提供了 type flexibility.

  * scala 具有静态类型系统的好处, 又解决了静态类型系统的一些常见问题, 这样在
    整体上具有较好的使用效果.

  * It’s not uncommon for user code to have no explicit types at all.
    Therefore, Scala programs often look a bit like programs written in a
    dynamically typed scripting language.

- Design choice for postfix type syntax. 这是因为 type inference, 要允许 omit
  type annotation. ``var|val variable: Type`` 可以比较方便、无歧义地支持 omit
  type annotation. C-style ``Type variable``, 就不太方便, 因为省去 ``Type``
  的话, 需要其他 keyword 来与 variable assignment 等语法区别开来. 这样降低了
  语言的统一感.

scalability
-----------
- scalability of types

- scalability of control structures

- OOP provides better structure of programs, improves scalability.

- Because of scalability (including scalability of types and control
  constructs), Scala allows users to grow and adapt the language in the
  directions they need by defining easy-to-use libraries that *feel* like
  native language support.

conciseness
-----------
compared to java: less typing -- on average about half number of the lines.

- Scala's syntax avoids boilerplate that burdens Java program.

- Scala's type inference contributes to its conciseness

- powerful libraries that let you capture and factor out common behavior. For
  instance, different aspects of library classes can be separated out into
  traits, which can then be mixed together in ﬂexible ways.

Influences on scala's design
----------------------------
- only a few features of Scala are genuinely new; most have been already
  applied in some form in other languages. Scala’s innovations come primarily
  from how its constructs are put together.

- Scala adopts a large part of the syntax of Java and C#. Expressions,
  statements, blocks, syntax of classes, packages and imports are mostly as in
  Java. Besides syntax, Scala adopts other elements of Java, such as its basic
  types, its class libraries, and its execution model.

- Scala's uniform object model -- Smalltalk and Ruby.

- universal nesting -- almost every construct in scala can be nested inside
  any other construct -- ALGOL 60/68, Simula, Beta, gbeta.

- uniform access principle for method invocation and ﬁeld selection -- Eiffel.

- Functional programming approach -- ML family of languages, Standard ML,
  OCaml, F#. Many higher-order functions in Scala’s standard library are also
  present in ML or Haskell.

- Scala’s main actor-based concurrency library, Akka -- Erlang.

- Extensible language -- Iswim.

- The idea of treating an inﬁx operator as a function, permit a function
  literal (or block) as a parameter -- Iswim and Smalltalk.

- postfix type annoatation -- Pascal, Modula-2, Eiffel.

- integrate OOP and FP -- Ruby, Smalltalk, Python, Pizza, NIce, Multi-Java,
  OCaml, F#, PLT-Scheme.

- scala's original innovations -- its abstract types provide a more
  object-oriented alternative to generic types, its traits allow for ﬂexible
  component assembly, and its extractors provide a representation-independent
  way to do pattern matching.

lexical analysis
================
semicolon handling
------------------
- scala 中, semicolon 用于结束一个 statement.

- 一行中可以有多个 statements. statements 之间用 semicolon 终结.

- 出现以下情况之一时, 一个 statement 可以跨行书写:

  * A line ends in a word that would not be legal as the end of a statement,
    such as a period or an infix operator.

  * The next line begins with a word that cannot start a statement.

  * A line ends while inside parentheses or brackets.

- 否则, line ending 自动被识别为 semicolon, 以终结一个 statement.

type inference
==============
- Type inference means the scala compiler can often infer the type of an
  expression when it's declared explicitly by programmer.

- Situations where type inference is performed:

  * variable declaration missing type (val, var, etc.)

  * method definition missing result type.

  * polymorphic method call without passing type parameters. compiler will
    infer such missing type parameters from the context and from the types of
    the actual method parameters.

  * generic class instantiation without passing type parameters. compiler will
    infer such missing type parameters from the context and from the types of
    the actual constructor parameters.

  * In certain cases, anonymous function parameter types can be inferred when
    the function is passed as argument.

- Situation where type inference is not performed:

  * method parameter types are not inferred.

  * When a function/method is recursive, its result type must be specified
    explicitly. 这是因为, 函数表达式本身使用了函数的结果值, 而函数的结果值
    类型是未知的, 从而表达式整体的类型是未知的.

expressions
===========
- expressions are computable statements.

variables
---------
::

  var x[: <type>] = <expression>

- 在 scala REPL 中, 为了方便使用, 可以用 var 重新定义新的 variable. 即::

    var x = 1
    var x = 2

named values
------------
::

  val x[: <type>] = <expression>

- 从 FP 的角度来看, 在对函数的一次运算过程中, 它参数的输入值是固定不变的. 因此
  一个 ``val`` 量不能被重新赋值.

- type can be ignored if it can be correctly inferred from the computation.

- 在 scala REPL 中, 为了方便使用, 可以用 val 重新定义新的 named value. 即::

    val x = 1
    val x = 2

if expression
-------------
::

  if (<boolean-expr>)
    <then-expr>
  [else
    <else-expr>]

match expression
----------------
::

  <expr> match {
    case <pattern> => <expr>
    ...
  }

- A way of doing pattern matching in scala.

- pattern can be:

  * literal values

  * case class patterns::

      <name>(param, ...) [if <boolean-expr>]

    - case class 匹配后, 相应位置的值赋值给 pattern 中相应位置的参数.
      
    - 支持 ``_`` 作为参数名来忽略相应位置的值.
      
    - Optional ``if`` 部分是 pattern guards.

  * 任意 object constructor call, 当该 object 具有 ``unapply()`` method 时.

  * 任意变量作为 pattern 时是 catchall pattern, 包括 ``_``.

  * 任意变量后可加 ``: <type>`` 类型限制, 只有类型匹配时才匹配 pattern. This is
    useful when the case needs to call a method on the pattern. It is also a
    convention to use the first letter of the type as the case identifier.

for comprehensions
------------------
::

  for (enumerators) <expression>

- enumerators refers to a semicolon-separated list of enumerators. An
  enumerator is either a generator which introduces new named values, or it is
  a filter.::

    enumerators := enumerator[; enumerator]...
    enumerator := <val> <- <expr> [if <boolean-expr>]

- ``<val>`` used in for comprehension is locally defined in expression's scope.
  注意在 enumerator 中, 定义的量实为 named value ``val``. 在每次循环中定义一个
  新的 ``<val>`` 量, 赋予新的值. 在 ``expression`` 中, 不能修改 ``<val>`` 的值.

- For comprehension generates a List.

- 当 ``enumerators`` 中由 semicolon 分隔多个 generator 时, 相当于多层嵌套的
  for loop::

    val x = for (i <- List(1,2,3); j <- List(4,5,6)) yield (i, j)
    // equals to pseudo-code
    for (i <- List(1, 2, 3))
      for (j <- List(4, 5, 6))
        ...

- ``yield`` expression can be omitted in a for comprehension. In that case,
  comprehension will result in Unit.

- ``(arg <- args)`` 形式, 可以读为 "for arg in args".

while expression
----------------
::

  while (<boolean-expr>)
    <expr>

- work like a normal while statement in imperative languages.

equality checking
-----------------
content equality
^^^^^^^^^^^^^^^^
- In scala, ``==``, ``!=`` operators apply to all objects. 这是因为所有类型都是
  实现这些方法.

- ``==``, ``!=`` have been carefully crafted so that it tests content equality
  rather than referential equality. Content equality checks are actually
  implemented by ``.equals()`` method of each specific type.

- ``==``, ``!=`` 已经做了 null check, 用户不需要再 prepend 一个 null check.

- ``==``, ``!=`` operator 的这种 content equality 检测机制是由各个类型的 ``==``
  ``!=``, ``.equals()`` 等方法来具体实现的. 这需要各个类型去配合实现.

referential equality
^^^^^^^^^^^^^^^^^^^^
- implemented by ``AnyRef.eq()`` method.

blocks
======
::

  { ... }

- A block is a multi-line expression, including one or more expressions and
  declarations. Another definition: A block is an encapsulation construct
  for which you can only see side effects and a result value.

- The result of the last expression in the block is the result of the overall
  block.

- blocks are commonly used as the expression of function/method body, for
  expressions, while expressions, etc.

- Note that the curly braces surrounding a class or object definition do not
  form a block, but a template (for class instances), because fields and
  methods may be visible from the outside.

functions
=========
- Functions are expressions that take parameters.

function literal -- anonymous function -- lambda expression
------------------------------------------------------------
::

  (<param>, ...) => <expression>

- On the left of => is a list of parameters. On the right is an expression
  involving the parameters.

- lambda expression 的定义可以通过 ``_`` placeholder 来简化. 此时只需在
  expression 中需要参数化的位置用 ``_`` 来代替即可.

- Because in scala function is a first-class entity, they have literals just
  like does any other standard data types. This is function literals.

partial application -- currying
-------------------------------
- 使用 ``_`` placeholder 参数化的方式是构建 partial application (currying) 的一
  种方式. 如果转化成 ``=>`` 的完整形式, 就会发现这样本质上不过是定义了一个
  function wrapper, 固化了部分参数而已.

- ``f _`` 是另一种构建 partial application 的方式.

methods
=======
method definition
-----------------
::

  def <name>[([implicit] <param>, ...)[([implicit] <param>, ...)]...][: <type>] = <expression>

- Methods are defined with the ``def`` keyword. ``def`` is followed by a name,
  parameter lists, a result type, and a body.

- A method can take 0 to many parameter lists.

- Scala allows nested method definition.

parameter definition syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- 对于每个 parameter, 必须有 type annotation. scala 不会 infer 函数和方法参数的
  类型.

- a parameter can be defined as pass-by-value parameter (default) or
  pass-by-name parameter. (two different parameter-passing methods.)

- pass-by-value parameter::

    <var-name>: <type> [= <default>]

  * pass-by-value parameters are ``val``'s. 也就是说, 在函数体中不可变. 这才符
    合 FP 思路.

- pass-by-name parameter::

    <var-name>: => <type> [= <default>]

  * 注意 ``=> <type>`` 的意义: 这相当于是声明一个函数类型 -- 该函数不接收任何
    参数, 返回一个 ``<type>`` 类型的值. 这也就是 pass-by-name 下, 对参数表达式
    的要求. 从这点来看, ``=> <type>`` 并不是特殊的语法, 与 pass-by-value 的类型
    声明是统一的.

  * pass-by-name parameter 接收一个任意结构, 只要求其返回值与声明的类型一致.

  * pass-by-name parameters have the advantage that they are not evaluated if
    they are not used in the function body. This can be desirable for example
    when the parameter's value involves computationally intensive or
    long-running procedures.
    
    On the other hand, pass-by-value parameters have the advantage that they
    are evaluated only once.

  * pass-by-name parameter 的一个很好的用例是 Boolean type 上 ``&&`` ``||``
    方法的 short-circuit 定义.

- a parameter can have default value, which makes it optional at call site.
  Both pass-by-value and pass-by-name parameters can have default values.

  * Unlike python, in scala a parameter with default value can be followed by
    parameters without default values.
    
    Naturally, if the former parameters are omitted in method call, the latter
    parameters must be bound by keyword argument form.

  * Where you might do overloaded methods in Java, you can use methods with
    optional parameters to achieve the same effect.

  * Default parameters in Scala are not optional when called from Java code.

method body
-----------
- 注意到, 在语法上, method body 相当于是通过 ``=`` 赋值给 method name. 从 FP 角
  度来看, a function/method defines an expression that results in a value. 这
  类似于数学上 ``f(x) = expr`` 的定义形式.

- 函数体表达式可以是单个表达式, 或者 complex expressions wrapped by curly
  braces.

method result type and value
----------------------------
- 从 FP 角度看, 函数、方法映射输入值至输出值, 输出的类型称为 result type, 应避
  免使用 stateful statement 性质的 return type 这种术语. (函数生成一个值, 即称
  为 a function results in a value.)

- 从 FP 角度看, 我们说函数的结果值, 而不说函数的返回值. 函数体就是一个表达式,
  它可能由多个更小的表达式构成. 函数的结果值即最后一个表达式的值.

- Scala 函数中, ``return`` statement 一般情况下是多余的, 不必要的, 把函数体看作
  表达式即可. 这有助于将函数逻辑设计得更为精炼 (compact), to factor larger
  methods into multiple smaller ones.

  而另一方面, 也应记得具体情况具体分析, 若在一些情况下, return 是合适的, 则应使
  用.

method call
-----------
- When calling a method, it can be parameterized with types and values. To
  parameterize the instance with types: specify types in square brackets; To
  parameterize the instance with values: specify values in parentheses. Type
  parameterization comes before value parameterization.

- When a method takes 0 value parameters, the parameter list can be omitted
  during method call. 这是因为, scala 的设计思路认为, ``(value, ...)`` 表示对
  method call 进行参数化, 若无需参数化, 则无需 ``(value, ...)`` 参数化部分.

- parameter binding syntax. Scala supports two parameter binding methods --
  positional arguments and keyword arguments. And they can be mixed in a single
  function call.

  * keyword argument parameter binding syntax does not work with calls to Java
    code.

implicit parameter list
-----------------------
- A method can have an implicit parameter list starting with ``implicit``
  keyword.

- If the parameters in that parameter list are not passed as usual, Scala
  will look if it can get *an implicit value of the correct type*, and if it
  can, pass it automatically.

  注意只要能找到正确类型的值, 就会被当作隐性参数值来使用.

- implicit parameter value lookup procedure:

  * Scala will first look for implicit definitions and implicit parameters that
    can be accessed directly (without a prefix) at the point the method with
    the implicit parameter block is called.

  * Then it looks for members marked implicit in all the companion objects
    associated with the implicit candidate type.

- implicit value definition:

  * prefix normal instance member definition with ``implicit`` keyword.

polymorphic methods
-------------------
::

  def method[<type-param>, ...](param, ...)

- Methods can take type parameters, which are enclosed in square brackets,
  similar to generic types.

- When calling a type-parametrized method, concrete types can be provided to
  make confinement. Type parameter isn't needed necessarily. The compiler can
  often infer it based on context or on the types of the value arguments.

methods in operator form
------------------------
- Scala doesn't technically have operators in the traditional sense. Operators
  are just normal method calls in prefix/infix/suffix forms. Therefore, There's
  technically no operator overloading.

- Any method can be used in operator form.

  * 当 method 接收 1 个参数时, 可作为 infix operator 使用, 以参数为 right
    operand 即可.

  * 当 method 接收多个参数时, 可作为 infix operator 使用, 必须将这些参数放在
    parenthenses 中, 整体作为右参数.

  * 当 method 名为 ``unary_<ident>``, 不接受任何参数, 且 ``ident`` 只包含
    ``+-!~`` 字符时, ``<ident>`` 可作为 prefix operator 使用. 注意 ident 包含这
    4 个字符即可, 可以任意排列组合. 若 ident 包含其他任何字符, 都只能作为一般
    方法使用或 postfix operator 使用, 不能作为 prefix operator.

  * 当 method 不接受任何参数时, 均可作为 postfix operator 使用. 使用方式可以是
    以下 4 种::

      obj.m()
      obj.m
      obj m()
      obj m

    The convention is that you include parentheses if the method has side
    effects, but you can leave them off if the method has no side effects.

- operator precedence: operator precedence is evaluated based on the priority
  of its first character (from highest to lowest)::

    (all other special characters)
    * / %
    + -
    :
    = !
    < >
    &
    ^
    |
    (all letters)
    (all assignment operators)

  * operators on the same line have the same precedence.

  * assignment operators 指的是 operator that ends in an ``=`` character, and
    the operator is not one of the ``<=, >=, ==, !=``, i.e., ``=, +=, -=, *=,
    /=`` etc. 这些 operator 具有最低的优先级, 且与 ``=`` 的优先级相同.

- operator associativity.

  * any operator that ends in a ``:`` is invoked on its right operand, passing
    the left operand as argument.

  * operator that ends in any other character is invoked on its left operand,
    passing the right operand as argument.

  * No matter what associativity an operator has, its operands are always
    evaluated left to right. 对于一个 right-associative 的算符, 这等价于以下特
    殊操作步骤::

      a op: b
      // equivalent to
      { val x = a; b.op:(x) }

- it is good style to use parentheses to clarify what operators are operating
  upon what expressions.

classes
=======
normal class
------------
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

  * member's default access level: public.

  * members can be made private with ``private`` access modifier.

  * constructor parameters without ``val`` or ``var`` are private; whereas with
    ``val`` or ``var`` are public by default.

- The part between curly braces is the template for class intances, it's not
  a block expression.

- inheritance.

  * A class can inherit only one base class with ``extends`` keyword.

  * A class can be composed with multiple trait mixins with ``with`` keyword.

  * The mixin traits and base class can have the same superclass.

- The simplest class definition::

    class <name>

- class instantiation.
  
  * instantiate a class with ``new``.

  * When instantiating an instance, it can be parameterized with types and
    values. To parameterize the instance with types: specify types in square
    brackets; To parameterize the instance with values: specify values in
    parentheses. Type parameterization comes before value parameterization.

- To override a parent class's method, use prefix ``override`` keyword to
  method definition.

- getter/setter syntax.

  * getter: a parameterless method whose name is property name to get and whose
    body results in a value.::

      def property = <expression>

  * setter: a method whose name is ``<property>_=`` and that takes a value to
    set.::

      def property_=(value) = <expression>

    注意 ``_=`` suffix 代表这是 setter method.

case classes
------------
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
^^^^^^^^^^^^^^^^
- ``copy()``. create a shallow copy of this instance.

singleton objects
-----------------
::

  object <name> {
    // definitions
  }

- ``object`` keyword defines a singleton object of ``<name>``.
  
- singleton object 的类型是一个由编译器生成的 internal synthetic class, 名为
  ``<name>$``. 在 ``object`` 语法中可以像普通 ``class`` definition 语法一样地
  extends superclass, mix in traits etc. 这实际上就是在对这个 ``<name>$`` 类型
  操作. 而 singleton object ``<name>`` 是这个类型的唯一实例.

- ``object`` definition 不能定义 constructor signature. 因为是自动实例化的.

- The singleton object is created lazily when it's first time referenced.

- As a top-level value, an object is a singleton.  As a member of an enclosing
  class or as a local value, it behaves exactly like a lazy val.

standalone object
^^^^^^^^^^^^^^^^^
- A singleton object that doesn't have a companion class is a standalone
  object.

- Usage.

  * collecting utility methods.

  * defining entrypoint to a program.

companion object and companion class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- When a class and a singleton object with the same name as the class are
  defined in the same source file, the object is the class's companion object,
  and the class is the object's companion class.

- Note that for a class and singleton object to be each other's companion, both
  must be defined in the same file.
  
  To define companions in the REPL, either define them on the same line or
  enter :paste mode.

- A companion class or object can access the private members of its companion.

- 在 companion class 中一般会去 import companion object 中的所有成员至 class
  namespace 下.::

    case class Circle(radius: Double) {
        import Circle._
        def area: Double = calculateArea(radius)
    }

    object Circle {
        private def calculateArea(radius: Double): Double = Pi * pow(radius, 2)
    }

- Usage.

  * Use a companion object for methods and values which are not specific to
    instances of the companion class. 这类似于其他 OOP 语言中的静态成员 (包含
    静态数据和静态方法).


extractor objects
^^^^^^^^^^^^^^^^^
- An extractor object is an object with an ``unapply()`` or ``unapplySeq()``
  method.

- ``unapply()`` takes an object and tries to give back the arguments.
  The result value of ``unapply()`` method:

  * If it is just a test, result in a ``Boolean``. E.g., ``case even()``.

  * If it generates a single sub-value of type ``T``, result in an
    ``Option[T]``.

  * If you want to generate several sub-values ``T1,...,Tn``, group them in an
    optional tuple ``Option[(T1,...,Tn)]``.

- ``unapplySeq()`` takes an object and tries to give back the arguments, useful
  when the number of values to extract isn’t fixed and we would like to
  generate an arbitrary number of arguments.

  * Result in an ``Option[Seq[T]]``. e.g., ``case List(x, y, z)``.

- Usage:

  * pattern matching.

  * partial function.

traits
------
::

  trait <name> {
    // definitions
  }

- Traits are used to share interfaces and fields between classes. They are like
  interfaces in Java but have more features.

- Traits are types containing certain fields and methods. Multiple traits can
  be combined.  Traits can also be defined as generic types.

- Trait/Class can extend traits with the ``extends`` keyword and implement
  abstract methods or override the default implementation with the ``override``
  keyword.

- mixin composition. Class/trait can be composed by traits as mixins, with
  ``with`` keyword. Traits and mixin composition avoids the diamond inheritance
  problems of multiple inheritance. When a trait is being mixed into a class or
  trait, it's called a mixin.

- A trait is abstract, it can not take any value parameters, i.e., can not be
  instantiated.

- A trait may take type parameters, in that case, ``trait[type]`` is a type,
  and ``trait`` is the trait of ``trait[type]`` type.

- Abstract methods of traits can have default implementations.

sealed clases
-------------
- Traits and classes can be marked sealed which means all subtypes must be
  declared in the same file. This assures that all subtypes are known (So that
  the definitions are sealed).

- Sealed classes are useful for pattern matching, because when left operand of
  ``match`` expression is confined as the base class of sealed classes, the
  ``match`` expression does not need a catch-all case.

generic classes
---------------
- defining generic class: Generic classes take a type parameter within square
  brackets.

- Use generic class: Generic class name followed by a concrete type in the
  square brackets.

variance
^^^^^^^^
- Scala supports variance annotations of type parameters of generic classes.

- All three variances are defined: covariant, contravariant and invariant.

- generic classes are invariant by default.

- Syntax to annotate variances of generic class::

    class Foo[A]  // invariant
    class Foo[+A] // covariant
    class Foo[-A] // contravariant

type bounds
-----------
- Type parameters and abstract type members may be constrained by a type bound.

- Upper type bound::

    T <: A

  T must be a subtype of A.

- Lower type bound::

    T >: A

  T must be a supertype of A.

- 对于 lower type bound ``T >: A``, 常用于以下场景: generic type is covariant
  on type parameter, and at least one of the generic type's method's signature
  takes a value of parametrized type. 此时, 常见的类型声明效果是: A will be the
  type parameter of the generic class and B will be the type paramter of the
  method.

  例如, 理解以下单向链表的实现::

    trait Node[+B] {
      def prepend[U >: B](elem: U): Node[U]
    }

    case class ListNode[+B](h: B, t: Node[B]) extends Node[B] {
      def prepend[U >: B](elem: U): ListNode[U] = ListNode(elem, this)
      def head: B = h
      def tail: Node[B] = t
    }

    case class NilNode[+B]() extends Node[B] {
      def prepend[U >: B](elem: U): ListNode[U] = ListNode(elem, this)
    }

  对该实现的解释:

  * 由于 +B, Node, ListNode, NilNode 三个泛型都对 B 是协变的. 即对于 subtype C
    of B, Node[C] is subtype of Node[B].

  * Node[C] 若要是 Node[B] 的子类, 则要求可以用 Node[C] 的实例替换所有 Node[B]
    实例使用的情况 (principle of substitution). 由于 Node[B].prepend 应该可以接
    收所有 B 的子类, Node[C].prepend 也必须能接收所有 B 的子类. 所以要求
    prepend 允许的参数类型以 B 为下限, 即 ``U >: B``.

  * 注意 ``U >: B`` 意味着接收所有 B 的父类直到 ``Any`` type. 这是合理的, 因为
    Node[Any].prepend 接收所有类型实例, Node[B].prepend 也要这样.

  * ListNode 和 NilNode 是 Node 的子类泛型. 对于 subtype C of B, 至少有以下关系
    成立:

              Node[B]
              /    \
             /      \
      ListNode[B]  Node[C]
             \      /
              \    /
            ListNode[C]

  * 使用测试::

      trait Bird
      case class AfricanSwallow() extends Bird
      case class EuropeanSwallow() extends Bird

      val africanSwallowList= ListNode[AfricanSwallow](AfricanSwallow(), NilNode())
      val birdList: Node[Bird] = africanSwallowList
      birdList.prepend(new EuropeanSwallow)

    注意到, birdList.prepend 调用的是 (via dynamic dispatch)
    ListNode[AfricanSwallow].prepend. 后者接收所有 Bird 类型实例 (事实上任意类
    型实例, 包括 1, 2.3, "sef", etc.).


inner classes
-------------
- A inner class is an instance member defined inside another class.

- Inner classes are path-depedent types. They are instance members rather than
  class members, and bound to the instances of the outer class. Each outer
  class's instance has distinct inner class, which makes it path-dependent.

- 对于 outer class ``Outer`` 的不同 instance ``x, y`` 中, inner class ``Inner``
  是不同的类型, 即 ``x.Inner`` 与 ``y.Inner`` 是不同的类型, 但是它们都是同一个
  class 级别的 inner class ``Outer#Inner`` 的子类.

abstract type members
---------------------
- abstract types (traits, abstract classes, etc.) can have abstract type
  members.

- Subclass can redefine abstract type members, e.g., to add constraints to it.
  The concrete subclass must have all abstract type members defined.

- Traits or classes with abstract type members are often used in combination
  with anonymous class instantiations. 

- In some cases, it's possible to turn abstract type members into type
  parameters of classes and vice versa.

compound types
--------------
::

  A with B with C

- A compound type is a mixin of several types (classes and traits).

- A compound type can be used in:
 
  * type declaration.

  * type definition along with class inheritance.

self-types
----------
::

  identifier: otherTrait1 with otherTrait2 ... =>

- Self-types are a way to declare that a trait must be mixed into another
  trait, even though it doesn’t directly extend it. 

- Cake pattern. dependency injection.

special methods
---------------
- ``apply()``. 对任意实例的 call ``()`` syntax 会转换成对实例的 ``apply()``
  方法的调用.

- ``update()``. 对任意实例的 call ``()`` syntax 赋值的操作会转换成对实例的
  ``update()`` 方法的调用.

annotations
===========
- Annotations associate meta-information with definitions.

- An annotation clause applies to the first definition or declaration following
  it. More than one annotation clause may precede a definition and declaration.
  The order in which these clauses are given does not matter.

builtin annotations
-------------------
- ``@deprecated``

- ``@tailrec``

- ``@inline``

package and import
==================
terms
-----
- simple name. A class's simple name is its defining name -- its identifier.

- full name. A class's full name is its package path plus its simple name.

packages
--------
- Packages partition the global namespace and provide a mechanism for
  information hiding.

- Packages are created by declaring one or more package names at the top of a
  Scala file. Each Scala file in the package could have the same package
  declaration.

- One convention is to name the package the same as the directory containing
  the Scala file. However, Scala is agnostic to file layout. 

- Package declaration can be nested.

- The package name should be all lower case.

- If the code is being developed within an organization which has a website, it
  should be the following format convention::

    <top-level-domain>.<domain-name>.<project-name>

imports
-------
- import can be used anywhere, both globally and locally.

- 一个 class/trait 的 companion object 与 class/trait 本身一同 import.

- scala 中除了可以 import 一个 package 中定义的全局的 entity 之外, 还可以
  import members from any object.

syntax
^^^^^^
- import everything from a package/object::

    import package_or_object._

- import single entity from a package/object::

    import package_or_object.entity

- import multiple entities from a package/object::

    import package_or_object.{entity1, entity2, ...}

- import entities from a package/object and rename::

    import package_or_object.{entity1 => name1, entity2 => name2, ...}

auto-imported entities
^^^^^^^^^^^^^^^^^^^^^^
The following entities are imported automatically into every scala
source file.

- entities from ``scala`` package

- entities from ``java.lang`` package

- members of ``scala.Predef`` singleton object.

package object
--------------
::

  package object <package-name> {
    ...
  }

- A package object is a special object, containing arbitrary definitions, used
  for extending the referenced package.

- Package objects can inherit Scala classes and traits like a normal object.
  Method overloading doesn’t work in package objects.

- By convention, the source code for a package object is usually put in a
  source file named ``package.scala`` under the same package.

- Each package is allowed to have one package object. Any definitions placed in
  a package object are considered members of the package itself.

compilation unit
----------------
- 一个 compilation unit 中, 可以包含任何 class, code etc.

- In general, in the case of non-scripts, it's recommended style to name files
  after the classes they contain, as is done in Java.

comments
========
- line comment: ``//``

- block comment: ``/* ... */``

scala application
=================
- To run a compiled scala application, the name of a standalone singleton
  object with a ``main`` method of following signature, must be supplied to
  runtime system.::

    def main(args: Array[String]): Unit

- The ``main`` method is the entry point of a program.

- 对于 scala script, 无需指定这个 standalone singleton object 的名字, 解释器
  会自动寻找符合的 singleton object.

tools
=====
- sbt

- scastie

- scaladex

- scala.js

- scalafiddle
