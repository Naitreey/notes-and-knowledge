map
===
- map 的含义. a simple operation is applied to all elements of a sequence.

- 这与 functional programming language 中类似, 不同的是, 这些 application
  operation 可能是并行地发生的.

- 并行应用可能在多个线程、多个进程、多个计算节点上进行.

reduce
======
overview
--------
- reduce 的含义. combine multiple vector into one, using the specified
  associative binary operator.

- 这与 functional programming language 中的 reduce/fold 等操作类似, 也与数据库
  中的聚合操作类似, 不同的是, the set of input vectors may reside on distinct
  processors in the beginning.

definition
----------
With input set

.. math::

  V=\{
    v_{0}={\begin{pmatrix}e_{0}^{0}\\ \vdots \\ e_{0}^{m-1}\end{pmatrix}},
    v_{1}={\begin{pmatrix}e_{1}^{0}\\ \vdots \\ e_{1}^{m-1}\end{pmatrix}},
    \dots,
    v_{p-1}={\begin{pmatrix}e_{p-1}^{0}\\ \vdots \\ e_{p-1}^{m-1}\end{pmatrix}}
  \}

and associative operator :math:`\oplus`, the reduction operation produces
the following result

.. math::

  r={
    \begin{pmatrix}
      e_{0}^{0} \oplus e_{1}^{0} \oplus \dots \oplus e_{p-1}^{0} \\
      \vdots \\
      e_{0}^{m-1}\oplus e_{1}^{m-1} \oplus \dots \oplus e_{p-1}^{m-1}
      \end{pmatrix}
  }={
    \begin{pmatrix}
      \bigoplus _{i=0}^{p-1} e_{i}^{0} \\
      \vdots \\
      \bigoplus _{i=0}^{p-1} e_{i}^{m-1}
    \end{pmatrix}
  }

which is stored at a specified root processor.

If the result :math:`r` has to be available at every processor after the
computation has finished, it is often called Allreduce.

reduction algorithms
--------------------
Binomial tree algorithm
^^^^^^^^^^^^^^^^^^^^^^^
在 reduce 过程中, 各个节点作为二叉树的 leaves, 这些节点上的 vector 就是 reduce
的初始输入. 每次 reduce 在该层的两个相邻节点上执行. 像二叉树那样不断上行, 最终
达到 root node.

Pipeline algorithm
^^^^^^^^^^^^^^^^^^

Pipelined tree algorithm
^^^^^^^^^^^^^^^^^^^^^^^^
