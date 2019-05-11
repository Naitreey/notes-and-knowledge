types
=====
- All of Java's primitive types (int, float, boolean, etc.) have corresponding
  classes in the ``scala`` package.

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

String
^^^^^^
instance methods
""""""""""""""""
- ``r``

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

