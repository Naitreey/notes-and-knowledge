indentation
===========
- prefered: 2 space indentation.

type
====
- It is generally considered more readable to declare the type of members
  exposed in a public API. Do not rely on type inference when defining public
  APIs.

- Sometimes the inferred type can be too specific that it prevent the variable
  to be useful in the following code. In those cases, declare types explicitly.

  .. code::

    var x = null
    x = 1  // do not compile

type annotation
---------------
- 关于 type annotation 信息的提供和省略.

  * 对于变量定义, 若表达式有清晰的合适的类型, 则变量本身的类型注释可省略.

  * 若表达式的类型与变量所需类型不完全相同, 则需要类型注释去指定.

  * 若变量类型需要用于作为清晰的 documentation 目的, 则可以明确注释类型.

  * 对于函数的 result type annotation, 即使能推断出类型也最好明确注释, 否则读者
    必须通过理解函数体表达式来推断结果类型, 这样降低了可读性.

- Application code 与 library code 在 type annotation 应用方面的区别.

  * application code 往往需要相对较少的类型注释, 因为它使用 library code, 后者
    一般具有明确的类型. 所以 type inference 经常足够确定变量的类型.

  * library code 的 API 部分, 应该提供明确的完整的类型注释. they constitute an
    essential part of the contract between the component and its clients.

method definition
=================
- 一般情况下, 函数体中不应出现 return statement, 使用函数体中最后一个表达式的值
  作为函数的结果值.

method call
===========
- keyword argument parameter binding syntax, 与 python 的风格不同, 这里 ``=``
  两边应该各空一格::

    func(a = 1, b = 2)

functional style
================
- 尽量多用 val, 少用 var. 但如果在具体场景下, var 就是更合适的选择, 就去使用.

  * If the code contains ``var``'s, it's probably in imperative style.

  * If the code contains only ``val``'s, it's probably in functional style.

- 尽量构建没有 side effect 的函数. 函数只对输入进行处理, 生成输出. Preferring
  methods without side effects encourages you to design programs where side
  effecting code is minimized.

  如果一个函数的 result type 是 Unit, 它很可能具有 side effect. 因为它不输出任
  何有用结果, 则它唯一可能具有的价值就是产生 side effect.

- 在大部分场景应该去尽量使用 FP paradigm. 然而若在具体场景, imperative
  programming paradigm 更合适, 则应该去使用. 重要的仍然是要根据具体问题, 选择最
  合适的工具. 不要具有 "一定要使用什么, 一定不使用什么" 的思维定势.

  Prefer vals, immutable objects, and methods without side effects. Reach for
  them ﬁrst. Use vars, mutable objects, and methods with side effects when you
  have a speciﬁc need and justiﬁcation for them.
packaging
=========
- In general, in the case of non-scripts, it's recommended style to name files
  after the classes they contain, as is done in Java.
