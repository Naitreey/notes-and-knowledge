immutable
=========
class List
----------
- an immutable sequence of objects of the same type.

- A List is implemented by a singly-linked list.

concrete value members
^^^^^^^^^^^^^^^^^^^^^^
characteristics accessing
"""""""""""""""""""""""""
- ``apply(n: Int): A``. Returns name at index n.

- ``count(p: (A) => Boolean): Int``. Count the number of elements in the List
  satisfying the predicate p.

- ``exists(p: (A) => Boolean): Boolean``. Tests whether a predicate holds for
  at least one element of this sequence. false if this sequence is empty.

- ``forall(p: (A) => Boolean): Boolean``. Tests whether a predicate holds for
  all elements of this sequence. true if this sequence is empty.

- ``head: A``. returns the first element of this List.

- ``init: List[A]``. returns a List of all elements except the last.

- ``last: A``. returns the last element.

- ``tail: List[A]``. returns a List of all elements except the first.

- ``isEmpty: Boolean``. whether the List is empty.

- ``length: Int``. the length of the List.

manipulation
""""""""""""
- ``:::[B >: A](prefix: List[B]): List[B]``. concatenate the prefix List with
  this List, return a new concatenated List.

- ``::[B >: A](x: B): List[B]``. prepend element x to this List, return a new
  List. (CONS in Lisp) 由于是单向链表, ``::`` 是 O(1) 的.

- ``:+[B >: A, That](elem: B)(implicit bf: CanBuildFrom[List[A], B, That]): That``.
  A copy of this List with elem appended, returns the copy.

- ``drop(n: Int): List[A]``. drop first n elements from the List, returns the
  new List. Or else the empty list, if this list has less than n elements. If n
  is negative, don't drop any elements.

- ``dropRight(n: Int): List[A]``. drop last n elements from the List, returns
  the new List. Or else the empty list, if this list has less than n elements.
  If n is negative, don't drop any elements.

- ``filter(p: (A) => Boolean): List[A]``. Select all elements from this List
  which satisfy the predicate. Return the filtered list. The order of the
  elements is preserved.

- ``filterNot(p: (A) => Boolean): List[A]``. Selects all elements of this
  List which do not satisfy a predicate.

- ``reverse: List[A]``. return the reversed List.

- ``sortWith(lt: (A, A) => Boolean): List[A]``. sort the List according to the
  comparison function lt (注意返回值是 Boolean, 判断前者是否小于后者). The sort
  is stable. That is, elements that are equal appear in the same order in the
  sorted sequence as in the original. 注意这里 lt 无需接收 B >: A 类型, 因为排
  序操作不会引入新的元素, 不存在对父类元素的支持问题.

iteration
""""""""""
- ``foreach[U](f: (A) => U): Unit``. apply function f to each element of this
  List. The function that is applied for its side-effect to every element. The
  result of function f is discarded.

operations
""""""""""
- ``map[B, That](f: (A) => B)(implicit bf: CanBuildFrom[List[A], B, That]): That``
  map function to each element of the List, returns the result List.

- ``reduceLeft[B >: A](op: (B, A) => B): B``. Applies a binary operator to all
  elements of this sequence, going left to right. 注意 B >: A, 需要这个条件的
  原因是 op 的前一次输入值是作为后一次输入值. 因此 op 的第一个参数只需支持任意
  A 的任意父类即可.

- ``mkString: String``. display all elements in a string, elements are
  separated by empty string.

- ``mkString(sep: String): String``. display all elements in a string, elements
  are separated by sep.

- ``mkString(start: String, sep: String, end: String): String``. display all
  elements in a string, starting with start, ending with end. elements are
  separated by sep.

object List
-----------
value members
^^^^^^^^^^^^^
- ``apply[A](xs: A*): List[A]``. create a List with the specified elements.

object Nil
----------
- an object representing the empty List.

- It's a subclass of ``List[Nothing]``. 因此, Nil 与 ``List()`` 其实是相同的.


trait Set
---------
abstract value members
^^^^^^^^^^^^^^^^^^^^^^
- ``+(elem: A): Set[A]``. Create a new set with additional element elem.

object Set
----------
value members
^^^^^^^^^^^^^
- ``apply[A](elems: A*): Set[A]``. create a new set with elems of the default
  Set implementation.

trait Map
---------
::

  trait Map[K, +V] extends Iterable[(K, V)] with collection.Map[K, V] with MapLike[K, V, Map[K, V]]

- 注意 immutable Map is invariant on K type, and covariant on V type.

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
- ``+[V1 >: V](kv: (K, V1)): Map[K, V1]``. add ``(k, v)`` pair to this Map,
  returns the new Map.

object Map
----------
value members
^^^^^^^^^^^^^
- ``apply[A, B](elems: (A, B)*): Map[A, B]``. generate a Map containing key,
  value pairs as specified by elems.

- ``empty[K, V]: Map[K, V]``. Create an empty immutable map with the specified
  type parameters.

HashMap
-------

TreeMap
-------

ParMap
------

mutable
=======
trait Set
---------
abstract value members
^^^^^^^^^^^^^^^^^^^^^^
- ``+=(elem: A): Set.this.type``. add elem to this Set.

trait Map
---------
::

  trait Map[K, V] extends Iterable[(K, V)] with collection.Map[K, V] with MapLike[K, V, Map[K, V]]

- 注意 mutable Map is invariant on both K and V types.

abstract value members
^^^^^^^^^^^^^^^^^^^^^^
- ``+=(kv: (K, V)): Map.this.type``. Add ``(k, v)`` pair to this map,
  overriding original mapping value if k exists.
class WeakHashMap
-----------------
- A hash map with references to entries which are weakly reachable. Entries are
  removed from this map when the key is no longer (strongly) referenced. This
  class wraps java.util.WeakHashMap.
