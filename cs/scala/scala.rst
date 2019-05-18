basic types
===========
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

Int
---
concrete value members
^^^^^^^^^^^^^^^^^^^^^^
- ``to(end: Int): Inclusive``.
  
  Returns: A scala.collection.immutable.Range from this up to and including
  end.

- ``max(that: Int): Int``. return the greater one between this and that int.

String
------
value members
^^^^^^^^^^^^^
- ``*(n: Int): String``. return this string repeated n times.

- ``r: Regex``. return a Regex with string as pattern.

type casting
------------
- rules:

  * Byte -> Short -> Int -> Long -> Float -> Double

  * Char -> Int

- Casting is unidirectional. 即不能向下做 type casting.


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
