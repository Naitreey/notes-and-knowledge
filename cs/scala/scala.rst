basic types
===========
Any
---
- The supertype of all types -- the top type.

- defines certain universal methods.

concrete value members
^^^^^^^^^^^^^^^^^^^^^^
- ``==(arg0: Any): Boolean``. Test two objects for equality. ``x == that`` is
  equivalent to ``if (x eq null) that eq null else x.equals(that)``. 注意这个
  方法已经做了 null check, 用户没必要自己再做 null check. 注意 ``==`` checks
  redirects to ``.equals()`` method for the type's specific implementation.

AnyVal
------
- subclass of Any.

- AnyVal represents value types.

- Scala compiles instances of value types that correspond to Java primitive
  types down to Java primitive type values or instances of wrapper types, in
  the bytecode it produces.

- 9 predefined value types and they are non-nullable:
  Double, Float, Long, Int, Short, Byte, Char, Unit, Boolean.

  * integral types: Byte, Short, Int, Long, Char.

  * numeric types: integral types plus Float and Double.

  Scala's basic types have the exact same ranges as the corresponding types in
  Java.

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

- Unit is usually used for method's result type, meaning nothing to return.
  (similar to void in Java and C.)

- 由于每个 scala expression/statement 都必须有值, 没有合适的返回值时就使用
  Unit.

- Every void-returning method in Java is mapped to a Unit-resulting method in
  Scala.

- A Unit-resulting function/method is only executed for its side effect.

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


Byte
----
- 8-bit signed 2's complement integer.

- Byte can compare with any numeric type values with relational methods.

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
arithmetic operations
"""""""""""""""""""""
常用的 infix ``+-*/%``, prefix ``+-``.

relational operation methods: ``<, >, <=, >=``

- ``unary_+: Int``. note return value is Int.

- ``unary_-: Int``. note return value is Int.

bitwise operations
""""""""""""""""""
- ``&(x: Byte): Int``. 注意 result type is Int.

- ``&(x: Short): Int``. 注意 result type is Int.

- ``&(x: Int): Int``. 注意 result type is Int.

- ``&(x: Char): Int``. 注意 result type is Int.

- ``&(x: Long): Long``

- ``|(x: Byte): Int``. 注意 result type is Int.

- ``|(x: Short): Int``. 注意 result type is Int.

- ``|(x: Int): Int``. 注意 result type is Int.

- ``|(x: Char): Int``. 注意 result type is Int.

- ``|(x: Long): Long``

- ``^(x: Byte): Int``. 注意 result type is Int.

- ``^(x: Short): Int``. 注意 result type is Int.

- ``^(x: Int): Int``. 注意 result type is Int.

- ``^(x: Char): Int``. 注意 result type is Int.

- ``^(x: Long): Long``.

- ``unary_~: Int``. 注意 result type is Int.

- ``<<(x: Int): Int``.

- ``>>(x: Int): Int``. signed shift right. fills the highest bit value as it
  shifts.

- ``>>>(x: Int): Int``. unsigned shift right.

Short
-----
- 16-bit signed 2's complement integer.

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
arithmetic operations
"""""""""""""""""""""
常用的 infix ``+-*/%``, prefix ``+-``.

relational operation methods: ``<, >, <=, >=``

- ``unary_+: Int``. note return value is Int.

- ``unary_-: Int``. note return value is Int.

bitwise operations
""""""""""""""""""
- ``&(x: Byte): Int``. 注意 result type is Int.

- ``&(x: Short): Int``. 注意 result type is Int.

- ``&(x: Int): Int``. 注意 result type is Int.

- ``&(x: Char): Int``. 注意 result type is Int.

- ``&(x: Long): Long``

- ``|(x: Byte): Int``. 注意 result type is Int.

- ``|(x: Short): Int``. 注意 result type is Int.

- ``|(x: Int): Int``. 注意 result type is Int.

- ``|(x: Char): Int``. 注意 result type is Int.

- ``|(x: Long): Long``

- ``^(x: Byte): Int``. 注意 result type is Int.

- ``^(x: Short): Int``. 注意 result type is Int.

- ``^(x: Int): Int``. 注意 result type is Int.

- ``^(x: Char): Int``. 注意 result type is Int.

- ``^(x: Long): Long``.

- ``unary_~: Int``. 注意 result type is Int.

- ``<<(x: Int): Int``.

- ``>>(x: Int): Int``. signed shift right. fills the highest bit value as it
  shifts.

- ``>>>(x: Int): Int``. unsigned shift right.

Int
---
- 32-bit signed 2's complement integer.

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
arithmetic operations
"""""""""""""""""""""
常用的 infix ``+-*/%``, prefix ``+-``.

relational operation methods: ``<, >, <=, >=``

- ``unary_+: Int``.

- ``unary_-: Int``.

bitwise operations
""""""""""""""""""
- ``&(x: Byte): Int``. 注意 result type is Int.

- ``&(x: Short): Int``. 注意 result type is Int.

- ``&(x: Int): Int``. 注意 result type is Int.

- ``&(x: Char): Int``. 注意 result type is Int.

- ``&(x: Long): Long``

- ``|(x: Byte): Int``. 注意 result type is Int.

- ``|(x: Short): Int``. 注意 result type is Int.

- ``|(x: Int): Int``. 注意 result type is Int.

- ``|(x: Char): Int``. 注意 result type is Int.

- ``|(x: Long): Long``

- ``^(x: Byte): Int``. 注意 result type is Int.

- ``^(x: Short): Int``. 注意 result type is Int.

- ``^(x: Int): Int``. 注意 result type is Int.

- ``^(x: Char): Int``. 注意 result type is Int.

- ``^(x: Long): Long``.

- ``unary_~: Int``. 注意 result type is Int.

- ``<<(x: Int): Int``.

- ``>>(x: Int): Int``. signed shift right. fills the highest bit value as it
  shifts.

- ``>>>(x: Int): Int``. unsigned shift right.

concrete value members
^^^^^^^^^^^^^^^^^^^^^^
- ``to(end: Int): Inclusive``.

  Returns: A scala.collection.immutable.Range from this up to and including
  end.

- ``min(that: Int): Int``. return the smaller one between this and that int.

- ``max(that: Int): Int``. return the greater one between this and that int.

- ``abs: Int``. absolute value of this.

Long
----
- 64-bit signed 2's complement integer.

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
arithmetic operations
"""""""""""""""""""""
常用的 infix ``+-*/%``, prefix ``+-``.

relational operation methods: ``<, >, <=, >=``

- ``unary_+: Long``.

- ``unary_-: Long``.

bitwise operations
""""""""""""""""""
- ``&(x: Byte): Long``. 注意 result type is Long.

- ``&(x: Short): Long``. 注意 result type is Long.

- ``&(x: Int): Long``. 注意 result type is Long.

- ``&(x: Char): Long``. 注意 result type is Long.

- ``&(x: Long): Long``

- ``|(x: Byte): Long``. 注意 result type is Long.

- ``|(x: Short): Long``. 注意 result type is Long.

- ``|(x: Int): Long``. 注意 result type is Long.

- ``|(x: Char): Long``. 注意 result type is Long.

- ``|(x: Long): Long``

- ``^(x: Byte): Long``. 注意 result type is Long.

- ``^(x: Short): Long``. 注意 result type is Long.

- ``^(x: Int): Long``. 注意 result type is Long.

- ``^(x: Char): Long``. 注意 result type is Long.

- ``^(x: Long): Long``.

- ``unary_~: Long``. 注意 result type is Long.

- ``<<(x: Int): Long``.

- ``<<(x: Long): Long``.

- ``>>(x: Int): Long``. signed shift right. fills the highest bit value as it
  shifts.

- ``>>(x: Long): Long``. signed shift right. fills the highest bit value as it
  shifts.

- ``>>>(x: Int): Long``. unsigned shift right.

- ``>>>(x: Long): Long``. unsigned shift right.

Char
----
- Char 是一种 integer type. 它存储的实际是 16-bit unsigned integer, 对应于
  相应的 unicode codepoint. 即 0 - 65535.

- 注意到 Scala/Java 的一个 Char 只能保存 BMP 上的字符.

- 由于 Char 是一种 integer type, 常用的 arithmetic operation is allowed on
  Char.

String
------
value members
^^^^^^^^^^^^^
- ``*(n: Int): String``. return this string repeated n times.

- ``r: Regex``. return a Regex with string as pattern.

- ``stripMargin: String``. For every line (``\n``-terminated) in this string:
  Strip a leading prefix consisting of blanks or control characters followed by
  ``|``.

- ``indexOf[B >: Char](elem: B): Int``. index of first occurrence of elem in
  the string. 注意 B >: Char 条件, 这是因为 String is immutable sequence of
  Char. 相当于它是 covariant 的. 所以理论上要支持 Char 的父类为参数的情况.

- ``indexOf[B >: Char](elem: B, from: Int): Int``. ditto, starting from
  ``from`` index.

- ``captialize: String``.

Float
-----
- 32-bit IEEE 754 single-precision float

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
arithmetic operations
"""""""""""""""""""""
常用的 infix ``+-*/%``, prefix ``+-``.

Float can compute modulo operation (``%``). The ﬂoating-point remainder you
get with ``%`` is not the one deﬁned by the IEEE 754 standard. The IEEE 754
remainder uses rounding division, not truncating division, in calculating the
remainder. Use ``scala.math.IEEEremainder``.

relational operation methods: ``<, >, <=, >=``

- ``unary_+: Float``.

- ``unary_-: Float``.

Double
------
- 64-bit IEEE 754 double-precision float

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
arithmetic operations
"""""""""""""""""""""
常用的 infix ``+-*/%``, prefix ``+-``.

Double can compute modulo operation (``%``). The ﬂoating-point remainder you
get with ``%`` is not the one deﬁned by the IEEE 754 standard. The IEEE 754
remainder uses rounding division, not truncating division, in calculating the
remainder. Use ``scala.math.IEEEremainder``.

relational operation methods: ``<, >, <=, >=``

- ``unary_+: Double``.

- ``unary_-: Double``.

concrete value members
^^^^^^^^^^^^^^^^^^^^^^
- ``round: Long``.

- ``isInfinity: Boolean``.

Boolean
-------
abstract value members
^^^^^^^^^^^^^^^^^^^^^^
注意 ``&`` 和 ``|`` 在 integral types 中是 bitwise operator methods, 在 boolean
type 中是 non-short-circuit logical operator methods.

- ``unary_!: Boolean``. negate the boolean.

- ``&&(x: => Boolean): Boolean``. This method uses short-circuit evaluation,
  meaning if this instance is false, pass-by-name parameter ``x`` won't be
  evaluated.

- ``||(x: => Boolean): Boolean``. This method uses short-circuit evaluation,
  meaning if this instance is true, pass-by-name parameter ``x`` won't be
  evaluated.

- ``&(x: Boolean): Boolean``. Both this instance and ``x`` are evaluated, even
  if this instance is already false.

- ``|(x: Boolean): Boolean``. Both this instance and ``x`` are evaluated, even
  if this instance is already true.

class Symbol
------------
- A symbol is a unique object for equal strings.

- Symbols are interned. They can be compared using reference equality. 
  注意到同一个 symbol name 只有一个实例.

- Usage.

  * Symbol 可用于代表 a name for code, 而不是数据. 例如需要 method name,
    identifier name, etc. 这是将 code 与 data 做一个区分. 又考虑到 interned
    性质, 这种唯一性也适合用于需要表示 name/identifier 等的场景.

    A Symbol Literal comes into play where it clearly differentiates just any
    old string data with a construct being used in the code. It's just really
    there where you want to indicate, this isn't just some string data, but in
    fact in some way part of the code. [SOScalaSymbol1]_

  * Symbols are used where you have a closed set of identifiers that you want
    to be able to compare quickly. With Symbol instances, comparisons are a
    simple eq check (i.e. == in Java), so they are constant time (i.e. O(1)) to
    look up. [SOScalaSymbol2]_

value members
^^^^^^^^^^^^^
- ``name: String``. symbol's name string.

object Symbol
-------------
value members
^^^^^^^^^^^^^
- ``apply(name: String): Symbol``. factory method to create a Symbol instance.

type casting
------------
- rules:

  * Byte -> Short -> Int -> Long -> Float -> Double

  * Char -> Int

- Casting is unidirectional. 即不能向下做 type casting.

- 注意不存在从 Boolean 向任何 integral types 的 type casting.

literals
--------
integer literals
^^^^^^^^^^^^^^^^
- base: decimal and hexadecimal. 注意 scala 不支持 octal literal.

  * decimal: decimal literal may *not* have a leading zero.

  * hexadecimal: hexadecimal literal starts with a ``0x`` or ``0X``; letters
    can be any any combination of uppercase and lowercase.

- type: Int or Long.

  * If an integer literal ends with ``L`` or ``l``, then it's Long literal.

  * otherwise it's Int literal.

  * 不存在自动类型转换. 若 Int literal 超过了 Int 值域, 会编译出错, 而不是自动
    转换至 Long.

  * 不存在 Byte, Short 类型的 literal.

- Int literal 可以赋值给 Byte, Short 类型变量. 前提是 literal 的值在相应类型的
  范围内, 否则会编译错误. 注意必须是 Int literal 才可以. 若是 Long literal, 不
  能赋值给 Byte 或 Short.

floating point literals
^^^^^^^^^^^^^^^^^^^^^^^
- decimal digits, optionally containing a decimal point, optionally followed
  by an E or e and an exponent.

- type:

  * If a floating-point literal ends with a ``F`` or ``f``, then it's a Float.

  * otherwise it's a Double.

  * A Double can optionally ends with a ``D`` or ``d``.

character literals
^^^^^^^^^^^^^^^^^^
- A BMP unicode char within a single quote.

- A unicode escape sequence within a single quote::

    '\uXXXX'

  ``X`` can be uppercase or lowercase hexadecimal digit.

  this syntax is intended to allow Scala source ﬁles that include non-ASCII
  Unicode characters to be represented in ASCII.

- Special backslash escape sequences.::

    \n \r \b \t \f \r \" \' \\

string literals
^^^^^^^^^^^^^^^
- normal strings:

  * characters surrounded by double quotes.

  * allowable characters are the same as character literals.

  * normal string 是不能跨行的, 若要跨行的字符串, 必须使用 multiline string.

- multiline strings:

  * Any characters, including newline, surrounded by triple double quotes::

      """sefsef
         sefsefsef"""

  * 里面的所有字符, 包括 newline, 都 literally kept.

processed string literals
^^^^^^^^^^^^^^^^^^^^^^^^^
::

  <expr>"string"
  <expr>"""string"""

- ``<expr>`` is a string interpolator expression.

- 注意 normal string and multiline string literals 都支持 interpolation.

- string interpolation is a more readable alternative to string concatenation.

- string interpolation is implemented by rewriting code at compile time. The
  compiler will treat any expression consisting of an identiﬁer followed
  immediately by the open double quote of a string literal as a string
  interpolator expression.

- builtin string interpolators:

  * ``s``. evaluate each embedded expressions, invoke ``.toString`` to each
    result, and replace the embedded expressions with the stringified results.

    支持的 interpolation 格式:
    
    - ``$expr``. value of the named variable. ``expr`` is the name of variable,
      the name is composed of all characters up to the first non-identifier
      character.
     
    - ``${expr}``. value of general expression.

  * ``raw``. like ``s``, except all characters are preserved in raw form,
    including backslash escape sequences.

  * ``f``. a formatted ``s``::

      $expr<format-specifier>
      ${expr}<format-specifier>

    format specifier is in printf-style, and is optional. format specifier
    uses java.util.Formatter. If no format specifier is specified, default to
    ``%s``.

symbol literals
^^^^^^^^^^^^^^^
- Any legal identifier prefixed by a single quote char::

    'ident

- They are literals of scala.Symbol type.

- A ``'ident`` literal is equivalent to ``Symbol("ident")``.

boolean literals
^^^^^^^^^^^^^^^^
- ``true`` and ``false``.

container types
===============
class Array
-----------
instance constructor
^^^^^^^^^^^^^^^^^^^^
- ``length: Int``. 数组长度.

value members
^^^^^^^^^^^^^
- ``apply(i: Int): T``. 输入 index, 输出相应的数组元素.

iteration
^^^^^^^^^
- ``foreach(f: (A) => Unit): Unit``. apply f to each element of the array.

object Array
------------
value members
^^^^^^^^^^^^^
- ``apply[T](xs: T*)(implicit arg0: ClassTag[T]): Array[T]``. A factory method
  for Array class. Create an array with given elements.

tuples
------
- Tuples are immutable.

- Tuple can contain different types of elements.

- Tuple's type 由三个因素决定: 每个元素的类型、元素的顺序、元素的个数.

- Element access.

  * one-based indexing.

  * 使用 ``_<index>`` 属性名来获取相应位置的元素.

  * 为什么使用这么奇怪的方式访问元素? 而不是 ``array(n)`` 类似语法?

    - 首先, tuple 元素类型可以任意, 若支持 ``apply()`` 方法, 则只能设置
      result type 为 Any.

    - Tuple 在实例化时, scala 能确定每个属性的类型, 通过访问属性的方式可以做静
      态类型检查.

    - index is 1-based because this is a tradition set by other languages with
      statically typed tuples, such as Haskell and ML.

- ``scala`` package 定义了从 Tuple1 至 Tuple22 这 22 种 tuple generic types.

- Tuple in scala is very different from tuple in Python. In python,
  tuple is just like an immutable list. tuple 中元素的个数没有限制,
  不同长度和元素的 tuple 类型没有区别. Python 中, 在合适的抽象层级
  下, namedtuple 是一种更方便、更清晰的数据结构.

  而在 scala 中, tuple 是限制性更强的一种数据类型. 不同长度、不同
  元素类型的 tuple 都是不同类型的 tuple. 在使用时, 应当是首先清楚
  要存放的元素类型和长度才能去使用.

- Tuple 类型常用于:
  
  * 函数的 result type, 从而从函数能够输出多个值. 虽然 case class 可能在大部分
    情况下更合适 (见下).

  * 构建 Map.

  * 构建 Value class.

- tuple vs case class.
  
  * 何时使用 tuple, 何时使用 case class?
  
    对于任意一个数据结构的选择, 应与应用场景所需的抽象层级来对应. Tuple 更适合
    相对高的抽象层级的场景, 例如写一个 sufficiently abstract generic framework,
    这时用 tuple 来传递数据就比 case class 合适. 因为 tuple 各个元素的含义在这
    个场景下可能是 generic 的, 没有确定的含义. 如果是对特定应用场景中的对象进行
    建模, 则 case class 可能是更合适的选择, 因为场景足够具体, case class 能更清
    晰地表达语义. See also [SOTupleVSCaseClass]_.

  * tuple 相对于 case class 的一些问题.

    tuple 缺乏语义, 缺少语境时, 元素的意义不明确. 而 case class 本身即附有明确
    的语义.

    在代码迭代中, tuple 无法保持数据类型的向后兼容性. If you want to evolve the
    tuple to hold more info (meaning, adding a new value to the tuple), you
    break code everywhere because now you have a new type. If you have a case
    class, you can add a new field, and the code will compile everywhere; now
    you’d just need to use the new field everywhere you want the extra info,
    and the remaining code can be left exactly the same.
  
utilities
=========
object Console
--------------
io defaults
^^^^^^^^^^^
- ``in: BufferedReader``

- ``out: PrintStream``

- ``err: PrintStream``

console output
^^^^^^^^^^^^^^
convenient methods handling on default output (``Console.out``).

- ``print(obj: Any): Unit``. Print obj to ``out``, using its toString method.

- ``println(obj: Any): Unit``. like ``print``, with a newline.
  
- ``println(): Unit``. ditto, only newline is printed.

object Predef
-------------
- provides definitions accessible to all scala compilation units without
  explicit qualification.

type aliases
^^^^^^^^^^^^
aliases of commonly used types.

console output
^^^^^^^^^^^^^^
- ``print(x: Any): Unit``. redirect to Console.print

- ``printf(text: String, xs: Any*): Unit``. redirect to Console.printf.

- ``println(x: Any): Unit``. redirect to Console.println

- ``println(): Unit``. redirect to Console.println.

assertions
^^^^^^^^^^
Invocations of assert can be elided at compile time by providing the command
line option ``-Xdisable-assertions``, which raises ``-Xelide-below`` above
``elidable.ASSERTION``, to the scalac command.

Variants of assert intended for use with static analysis tools are also
provided.

utility methods
^^^^^^^^^^^^^^^

trait App
---------
- can be used to quickly turn objects into executable programs.::

    object Main extends App {
      // main body
    }

- ``args`` returns the current command line arguments as an array.

- the main method should not be overridden: the whole class body becomes the “
  main method”.

references
==========
.. [SOTupleVSCaseClass] `When does it make sense to use tuples over case class <https://stackoverflow.com/questions/49054094/when-does-it-make-sense-to-use-tuples-over-case-class>`_
.. [SOScalaSymbol1] `What are some example use cases for symbol literals in Scala? <https://stackoverflow.com/a/780485/1602266>`_
.. [SOScalaSymbol2] `Purpose of Scala's Symbol? <https://stackoverflow.com/a/3555381/1602266>`_
