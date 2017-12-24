overview
========

- fundamental package for scientific computing with python.

- 核心是 ``ndarray``.

- vectorization & broadcasting.

- tools for C/C++, Fortran code integration.

- linear algebra, Fourier transform, random number capabilities.

- multi-dimensional container of generic data.

terms
=====
- axis: one dimension.

- rank: the number of dimensions.

e.g. 下面这个是 2-rank, the first axis's length is 2, second axis's
length is 3.
.. code:: python
  [[1, 0, 0],
   [0, 1, 2],]

ndarray
=======

- ``np.ndarray``.

- 主要对象.

- a homogeneous multidimensional array of same type elements.

- concepts of methods.

  * common mathematical and logical operators are elementwise/broadcasting.
  
  * Many unary operations are implemented as methods of ndarray. 默认情况下
    将 array 看作 a flattened list of numbers; ``axis`` 参数指定操作沿哪个
    轴进行. 即结果的 shape 是剩下的 dimensions.
    这相当于把整个数组进行某种转置, 让指定的 axis 成为最后一个轴, 再计算.
  
  * 运算结果数组的 dtype 是输入数组里面更一般化的那个.

attributes
----------

- ndim. rank.

- shape. a tuple of axes. length of shape is ndim.

- size. total number of element in array. product of shape tuple is size.

- dtype. element data type.

- itemsize. size in bytes of each array element. also ``ndarray.dtype.itemsize``.

- data. a ``memoryview`` of data buffer of this ndarray.

- flat. an iterator over array as if it's 1-dimensional.

methods
-------

- reshape().

- ``__str__()``. ndarray 的 string 形式定义为:

  * the last axis is printed from left to right,

  * the second-to-last is printed from top to bottom,

  * the rest are also printed from top to bottom, with each slice separated
    from the next by an empty line.

  * if array is too large, only corners are displayed and central parts are
    skipped.

- dot(). matrix product. 注意相对的 ``*`` 只是 brodcasting 元素之间的乘法.

- sum().

- min(), max().

- cumsum(). cumulative sum.

factory functions
-----------------

- ``array()``, 输入数组值, 给出 ndarray. dtype is based on elements from input.

- ``zeros()``, 输入数组形状, 给出 ndarray. dtype by default is float64.

- ``ones()``, 输入数组形状, 给出 ndarray. dtype by default is float64.

- ``empty()``, 输入数组形状, 给出 ndarray. dtype by default is float64.

- ``arange()``, (array range), 类似 builtin range(), 给出 ndarray. 支持 non-integer.
  对于 floating point 参数, 由于精度问题, 得到的数组中的最后一个元素可能 ``>= stop``.
  所以对于非整型参数, 应该使用 ``linspace``.

- ``linspace()``, linearly spaced numbers from start to stop.

- ``fromfunction()``, 给出一个 ndarray, 其任一元素的值是该座标点上的函数值.
  即给出了 index 定义域下的值数组.

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
