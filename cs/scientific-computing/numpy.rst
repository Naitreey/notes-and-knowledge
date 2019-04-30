overview
========
- fundamental package for scientific computing with python.

- features:

  * vectorization & broadcasting -- basis of much of numpy's power.

  * a multidimensional array object, various derived objects (such as masked
    arrays and matrices)

  * an assortment of routines for fast operations on arrays, including
    mathematical, logical, shape manipulation, sorting, selecting, I/O,
    discrete Fourier transforms, basic linear algebra, basic statistical
    operations, random simulation and much more.

  * tools for C/C++, Fortran code integration.

  * multi-dimensional container of generic data. Arbitrary data-types can be
    defined.

- At the core of numpy is the ``ndarray``.

terms
=====
- vectorization: Vectorization describes the absence of any explicit looping,
  indexing, etc., in the code.

- broadcasting: Broadcasting is the term used to describe the implicit
  element-by-element behavior of operations.

- rank: the number of dimensions.

Routines
========
Array creation routines
-----------------------
ones and zeros
^^^^^^^^^^^^^^
- ``zeros(shape, dtype=float, order="C")``. Return a new array of given shape
  and type, filled with zeros.

  * ``shape``. int or tuple of ints.

  * ``dtype``.

  * ``order="C"``.

- ``ones(shape, dtype=None, order="C")``. return a new array of ones.
  parameters see above.

- ``empty(shape, dtype=float, order="C")``. returns a new array without
  initializing entries, the initial values depend on the state of the memory.

from existing data
^^^^^^^^^^^^^^^^^^
- ``array(object, dtype=None, copy=True, order="K", subok=False, ndmin=0)``.
  create an ndarray.

  * ``object``. any array-like object, an object implemented ``__array__``
    method, or any nested sequences.

  * ``dtype``. desired data type for the array. If not given, then the type
    will be determined as the minimum type required to hold the objects in the
    sequence. This argument can only be used to ‘upcast’ the original array.
    For downcasting, use the ``.astype(t)`` method.

  * ``copy``. whether to copy the object. If False, a copy will only be made if
    ``__array__`` returns a copy, if obj is a nested sequence, or if a copy is
    needed to satisfy any of the other requirements.

  * ``order``. Specify the memory layout of the array.

  * ``subok``. If True, then sub-classes will be passed-through, otherwise the
    returned array will be forced to be a base-class array (default).

  * ``ndmin``. Specifies the minimum number of dimensions that the resulting
    array should have. Ones will be pre-pended to the shape as needed to meet
    this requirement.

- ``fromfunction()``, 给出一个 ndarray, 其任一元素的值是该座标点上的函数值.
  即给出了 index 定义域下的值数组.

numerical ranges
^^^^^^^^^^^^^^^^
- ``arange([start, ]stop, [step, ]dtype=None)``. array range, 类似 builtin
  ``range()``, 给出 ndarray (eager evaluation). 支持 floating point number.

  对于整数参数, 与 ``range()`` 行为一致.

  对于 floating point 参数, 由于精度问题, it is generally not possible to
  predict the number of elements obtained, due to the finite floating point
  precision. 并且, 得到的数组中的最后一个元素可能 ``>= stop``.  所以对于非整型
  参数, 应该使用 ``linspace()`` 得到精确数列.

  * ``start``. default is 0.

  * ``stop``. stop value is excluded.

  * ``step``. default is 1. can be passed as kwargs. If passed as positional,
    ``start`` must be given as well.

  * ``dtype``. If dtype is not given, infer the data type from the other input
    arguments.

- ``linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0)``.
  Return linearly spaced numbers/arrays from start to stop, the total number of
  samples is ``num``.

  * ``start``. a number or array-like.

  * ``stop``. a number or array-like.

  * ``num``. default is 50. must be non-negative.

  * ``endpoint``. When False, the sequence consists of all but the last of
    ``num + 1`` evenly spaced samples, so that stop is excluded. 注意到
    endpoint is False 时, stop - start 的长度被分了 ``num+1`` 份.

  * ``retstep``. If True, return (samples, step), where step is the spacing
    between samples. When start/stop is array-like, step is also an array-like
    of the same shape.

  * ``dtype``. If dtype is not given, infer the data type from the other input
    arguments.

  * ``axis``.

  When start/stop is array-like, start/stop array 中的对应元素作为范围进行等分.
  效果是, 从 start array 至 stop array, 等分平移, 每个节点都是一个同等 shape
  的 ndarray.

Mathematical functions
----------------------
sum, product, differences
^^^^^^^^^^^^^^^^^^^^^^^^^
- ``sum(a, axis=None, dtype=None, out=None, keepdims=<no value>, initial=<no value>, where=<no value>)``.
  sum of an array, over a given axis.

  * ``a``. array-like to sum.

  * ``axis``. see ndarray `calculation`_ 部分.

  * ``dtype``. see ndarray `calculation`_ 部分.

  * ``out``. see ndarray `calculation`_ 部分.

  * ``keepdims``. If this is set to True, the axes which are reduced are left
    in the result as dimensions with size one. If the default value is passed,
    then keepdims will not be passed through to the sum method of sub-classes
    of ndarray, however any non-default value will be.

  * ``initial``. Starting value for sum of each axis. see
    `numpy.ufunc.reduce`_.

  * ``where``. array-like of bool. Elements to include in the sum. see
    `numpy.ufunc.reduce`_.

- ``cumsum(a, axis=None, dtype=None, out=None)``. Return the cumulative sum of
  the elements along a given axis.

  * ``axis``. see ndarray `calculation`_ 部分.

  * ``dtype``. see ndarray `calculation`_ 部分.

  * ``out``. see ndarray `calculation`_ 部分.

Statistics
----------
Order statistics
^^^^^^^^^^^^^^^^
- ``amin(a, axis=None, out=None, keepdims=<no-value>, initial=<no-value>, where=<no-value>)``.
  Return the minimum of an array or minimum along an axis. See `numpy.sum`_ for
  parameters. NaN values are propagated, that is if at least one item is NaN,
  the corresponding min value will be NaN as well.

ndarray
=======
- ``np.ndarray``: it encapsulates n-dimensional arrays of homogeneous data
  types, with many operations being performed in compiled code for performance.

- A ndarray is a table of elements, all of the same type, indexed by a tuple
  of positive integers.

- An axis of a ndarray is one of its dimensions.

attributes
----------
- ``ndim``. the rank of the ndarray, i.e., the number of dimensions.

- ``shape``. a tuple of axis lengthes. length of shape is ndim.

- ``size``. total number of element in array, equal to product of shape tuple.

- ``dtype``. element data type.

- ``itemsize``. size in bytes of each array element. also ``ndarray.dtype.itemsize``.

- ``data``. a ``memoryview`` of data buffer of this ndarray, containing the
  actual elements of the array.

- flat. an iterator over array as if it's 1-dimensional.

methods
-------
- ``reshape(shape, order="C")``.

representation
^^^^^^^^^^^^^^
- ``__str__()``. ndarray 的 string 形式定义为:

  * the last axis is printed from left to right,

  * the second-to-last is printed from top to bottom,

  * the rest are also printed from top to bottom, with each slice separated
    from the next by an empty line.

  * if array is too large, only corners are displayed and central parts are
    skipped.

arithmetic, matrix multiplication, comparison operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
common mathematical and logical operators are element-wise/broadcasted.

- mathematical and logical operators::

    +, -, *, /, //, %, divmod, **, <<, >>, &, ^, |, <, <=, >, >=, ==, !=,
    +=, -=, *=, /=, //=, %=, **=, >>=, <<=, &=, |=, ^=

  * Upcasting. When operating with arrays of different types, the type of the
    resulting array corresponds to the more general or precise one.

- matrix product can be performed using ``@`` or ``.dot()`` method.

- ``dot()``. matrix product.

calculation
^^^^^^^^^^^
Calculations are implemented as methods of ndarray. Common parameters:

``axis`` 参数.

- If axis is None (the default), the array is treated as a 1-D array and the
  operation is performed over the entire array. This behavior is also the
  default if self is a 0-dimensional array or array scalar.
  
- If axis is an integer, 它指定操作沿哪个轴进行 (for each 1-D subarray that can
  be created along the given axis). 作为结果的 ndarray 的 shape 是剩下的
  dimensions.

- If axis is a tuple of ints, a sum is performed on all of the axes specified
  in the tuple. 作为结果的 ndarray 的 shape 是剩下的 dimensions.

- Each axis number can be negative, which counts from the last to the first
  axis.

``dtype`` 参数. The parameter ``dtype`` specifies the data type over which a
reduction operation (like summing) should take place. The default reduce data
type is the same as the data type of self, unless a has an integer dtype of
less precision than the default platform integer. In that case, if a is signed
then the platform integer is used while if a is unsigned then an unsigned
integer of the same precision as the platform integer is used. To avoid
overflow, it can be useful to perform the reduction using a larger data type.

``out`` 参数. For several methods, an optional ``out`` argument can also be
provided and the result will be placed into the output array given. The out
argument must be an ndarray and have the same number of elements. It can have a
different data type in which case casting will be performed.

- ``sum(axis=None, dtype=None, out=None, keepdims=False, initial=0, where=True)``.
  Return the sum of the array elements over the given axis. See above and
  ``numpy.sum()`` for parameters.

- ``min(axis=None, out=None, keepdims=False, initial=<no-value>, where=True)``.
  return the minimum along a given axis.
 
- ``max()``.

- ``cumsum(axis=None, dtype=None, out=None)``. Return cumulative sum of the
  elements along the given axis.

subscription & slicing
----------------------
- get:
 
  * 支持标准的 subscription & slicing. 返回一个新的 ndarray.

  * 对于高阶的数组 (rank >= 2), 支持 python language 定义的广义 slicing syntax.
    即 ``[  ]`` 里面可以是一个 slice tuple. 对于每个 axis, 在 tuple 中至多出现
    一项.
    
    若某个 trailing axis 在 slice tuple 缺失, 则认为是 complete slice ``:``.
    注意根据 slicing syntax, 中间的 axis 的 slice item 不能缺失, 即不能是
    ``[1,,3]`` 形状.

    别忘了任何一个 axis 上可以只是单纯的 subscription, 此时则在该维度上只取
    一个元素. 故结果数组会降维.

  * 对于 ndarray, ``...`` 即 ``Ellipsis`` 是一个合法的 slice item. 此时它的
    意义是 represent as many colons as needed to produce a complete indexing
    tuple. 主要用于省略多个无需 slice 的中间维度. 注意显然 ``...`` 只能出现
    一次, 否则有歧义.

  e.g.,
  .. code:: python
    a[2,:,5::-1]
    a[2,5:11:5,...,3:7]
    a[2,...]

- set:

  * 对于单项的 subscription 或多项的 slicing, 都支持单个元素形式的赋值.
    即此时, 赋值操作是 elementwise 的. 对于 slicing, 匹配到的所有元素位置都
    替换成新值.

  * 对于多项的 slicing, 支持赋值一个 sequence or ndarray. 前提是赋值操作两侧
    的数组的 shape 必须相同.

iteration
---------
- Iterating over multidimensional arrays is done with respect to the first axis.

- 若需要挨个元素的 iterator, 使用 ``ndarray.flat`` attribute.

ndarray vs python list
----------------------
- Fixed size. NumPy arrays have a fixed size at creation, unlike Python lists
  (which can grow dynamically). Changing the size of an ndarray will create a
  new array and delete the original.

- Same data type. The elements in a NumPy array are all required to be of the
  same data type, and thus will be the same size in memory.

- Advanced and fast operations. NumPy arrays facilitate advanced mathematical
  and other types of operations on large numbers of data. Typically, such
  operations are executed more efficiently and with less code than is possible
  using Python’s built-in sequences.

- Foundation of python scientific computing. A growing plethora of scientific
  and mathematical Python-based packages are using NumPy arrays; though these
  typically support Python-sequence input, they convert such input to NumPy
  arrays prior to processing, and they often output NumPy arrays. 

universal functions
===================
- common mathematical functions and operations as module level operations.

- 很多作为 ndarray instance method 出现的操作, 也有相应的 universal function
  去对应. 即支持不同的 programming paradigm.

- 它们是 ``np.ufunc`` class instance.

- ufunc's operation on array is elementwise.

functions
---------

- Trigonometric functions.

- ``np.exp()``

- ``np.sqrt()``

- ``np.add()``

options
=======

- set_printoptions
