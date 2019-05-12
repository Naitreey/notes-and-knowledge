Why study concepts of programming languages
===========================================
- 懂得越完善, 能使用/能表达的就越完善. 在编程时, 程序员的思路, 他所实现的算法形
  式, 他能使用的数据结构、控制结构等, 都受到他所使用的编程语言的限制. Awareness
  of a wider variety of programming language features can reduce such
  limitations in software development. the study of programming language
  concepts builds an appreciation for valuable language features and constructs
  and encourages programmers to use them, even when the language they are using
  does not directly support such features and constructs (in which case they
  can be simulated).

  在自然语言中也有类似现象, 即 the depth at which people can think is
  influenced by the expressive power of the language in which they communicate
  their thoughts. It is difficult for people to conceptualize structures they
  cannot describe, verbally or in writing.

- 了解更多种类的语言, 了解更多的语言特性, 有助于面对具体的项目需求选择最合适的
  语言. 如果程序员不能根据需要去选择合适的语言, 结果就是他们会选择使用自己最熟
  悉的语言, 即使该语言对具体项目而言并不合适.

- 学习编程语言概念有助于学习新语言. Once a thorough understanding of the
  fundamental concepts of languages is acquired, it becomes far easier to see
  how these concepts are incorporated into the design of the language being
  learned, 从而能够更快地掌握新语言.

  在自然语言中也有类似现象. The better you know the grammar of your native
  language, the easier it is to learn a second language. Furthermore, learning
  a second language has the benefit of teaching you more about your first
  language.

- Better understanding of the significance of implementation.
  
  In some cases, an understanding of implementation issues leads to an
  understanding of why languages are designed the way they are. In turn, this
  knowledge leads to the ability to use a language more intelligently, as it
  was designed to be used.

  Certain kinds of program bugs can be found and fixed only by a programmer who
  knows some related implementation details.

  In some cases, some knowledge of implementation issues provides hints about
  the relative efficiency of alternative constructs that may be chosen for a
  program.

- 学习编程语言概念, 有助于更好地使用已经学会的语言. 例如, learn about
  previously unknown and unused parts of the languages and begin to use those
  features.

- 学习编程语言概念, 有助于从宏观上了解计算机科学过去的发展历程和未来的方向.

Programming domains
===================
- scientific applications.

  * 科学计算是计算机编程的最早应用 (1940s - 1950s).

  * 科学计算要求大量的浮点数学运算.

  * 早期科学计算主要用汇编语言, 因效率是最重要因素.

  * Fortran 是最早用于科学计算的高级语言.

- Business applications.

  * 狭义的 Business application 主要指的是 producing elaborate reports, precise
    ways of describing and storing decimal numbers and character data, and the
    ability to specify decimal arithmetic operations. 这种狭义的商业应用后期没
    有多少发展, 因为它们被通用的办公软件如 office 等替代了.
    
  * 广义的商业应用指的是 any software or set of computer programs used by
    business users to perform various business functions. 这种广义的商业应用
    可由任意语言实现.

  * 始于 1950s.

  * COBOL 是最早用于商业应用的高级语言.

  * COBOL 至今仍然是商业应用领域最广泛使用的语言. 因为该编程领域被办公软件替代
    了.

- artificial intelligence.

  * 传统的人工智能专注于 symbolic computation rather than numeric computation.

  * symbolic computation is more conveniently done with linked lists of data
    rather than arrays. And it requires more flexibility.

  * Lisp 是最早用于 AI 应用的语言 (1960s).

  * Most AI applications developed prior to 1990 were written in Lisp or one of
    its close relatives.

  * 1970s, 出现了以 Prolog 为首的逻辑编程 (logic programming), 用于解决部分人工
    智能问题.

  * 最近, 一些 AI 应用开始用 C 等传统语言实现.

- web applications.

  * 涉及众多的语言, 包括多种标记语言 (html, xml, etc.), 数据格式 (json, xml,
    yaml, etc.), 通用编程语言 (java, php, javascript, python, etc.).

Language evaluation criteria
============================
- Readability. 可读性很重要是因为在软件的生命周期中, 对代码的维护工作占很大的部
  分. 而软件是否容易维护基本上是由可读性决定的. (1970 年代, 发展出了 software
  life cycle 概念, 编程从 computer-oriented 转向了 human-oriented.)

  * overall simplicity. 包含以下方面:
   
    - 语言中 basic constructs 的数目多少. A language with a large number of
      basic constructs is more difficult to learn than one with a smaller
      number.

    - feature multiplicity -- having more than one way to accomplish a
      particular operation.

    - operator overloading. Although this is often useful, it can lead to
      reduced readability if users are allowed to create their own overloading
      and do not do it sensibly.

    Simplicity in languages can, of course, be carried too far. E.g., 汇编语言
    往往都很简单, 但正因为过于简单, 需要大量代码表达一个基本的操作, 反而降低了
    可读性.

  * orthogonality (正交性) -- a relatively small set of primitive constructs
    can be combined in a relatively small number of ways to build the control
    and data structures of the language. Furthermore, every possible
    combination of primitives is legal and meaningful. Orthogonality follows
    from a symmetry of relationships among primitives. A lack of orthogonality
    leads to exceptions to the rules of the language.

    Orthogonality is closely related to simplicity: The more orthogonal the
    design of a language, the fewer exceptions the language rules require.
    Fewer exceptions mean a higher degree of regularity in the design, which
    makes the language easier to learn, read, and understand.

    例如, C 语言的数据类型设计是有比较强的正交性的, 而在一些其他方面缺乏正交性.
    structs and arrays 是 C 具有的 structured data types, structs 可作为函数
    返回值, 但 arrays 不可以. C 中参数一般是 pass-by-value, 而对于数组却是
    pass-by-reference.

    Too much orthogonality can also cause problems. The most orthogonal
    language is ALGOL 68. In combinational freedom allows extremely complex
    constructs. And even if the combinations are simple, the sheer numbers
    lead to complexity.

  * data type. It improves readability that a language has adequate facilities
    for defining data types and data structures.

  * syntax design. 例如以下语法设计决策会影响可读性.

    - special words. program appearance and thus program readability are
      strongly influenced by the forms of a language's special words.

      复合语句的结构设计尤其重要. 一些语言采用 matching pairs of special words
      or symbols to form compound statement, 这有助于提高可读性. C and its
      descendants use braces to specify compound statements. All of these
      languages have diminished readability.

    - form and meaning. Designing statements so that their appearance at least
      partially indicates their purpose is an obvious aid to readability.
      Semantics, or meaning, should follow directly from syntax, or form.

      反例, C 中 static 在不同的语境下意义不同.

- writability. Writability is a measure of how easily a language can be used
  to create programs for a chosen problem domain. 影响 readability 的各个语言
  特性同样影响 writability, 这是因为写代码的过程中就需要重读已经写下的代码.

  * overall simplicity and orthogonality. a smaller number of primitive
    constructs and a consistent set of rules for combining them (that is,
    orthogonality) is much better than simply having a large number of
    primitives.

    If a language has a large number of different constructs, some programmers
    might not be familiar with all of them. This situation can lead to a misuse
    of some features and a disuse of others that may be either more elegant or
    more efficient, or both, than those that are used.

    too much orthogonality can be a detriment to writability. Errors in
    programs can go undetected when nearly any combination of primitives is
    legal.

  * Expressivity -- a language has relatively convenient, rather than
    cumbersome, ways of specifying computations

- reliability. a program is reliable if it performs to its specifications under
  all conditions.

  * type checking. testing for type errors in a given program, either by the
    compiler or by the runtime. Run-time type checking is expensive,
    compile-time type checking is more desirable. the earlier errors in
    programs are detected, the less expensive it is to make the required
    repairs.

  * exception handling. the ability to intercept runtime errors (as well as
    other unusual conditions detectable by the program), take corrective
    measures, and then continue.

  * aliasing. aliasing is having two or more distinct names in a program that
    can be used to access the same memory cell. Aliasing is a dangerous
    feature.

  * readability and writability. The easier a program is to write, the more
    likely it is to be correct. Readability affects reliability in both the
    writing and maintenance phases of the life cycle.

- cost.

  * the cost of training programmers to use the language, which is a function
    of the simplicity and orthogonality of the language and the experience of
    the programmers.

  * the cost of writing programs in the language, which is a function of the
    writability of the language. (早期设计 high-level languages 的一个重要目的
    就是降低软件开发成本.)

  * the cost of compiling programs in the language.

  * the cost of executing programs written in a language is greatly influenced
    by that language's design. A language that requires many runtype checks
    will prohibit fast code execution, regardless of the quality of the
    compiler.

  * the cost of the language implementation system. A language whose
    implementation system is either expensive or runs only on expensive
    hardware will have a much smaller chance of becoming widely used (e.g.,
    mathematica).

  * the cost of poor reliability.

  * the cost of maintaining programs, which includes both corrections and
    modifications to add new functionality. The cost maintenance depends on
    readability. Because maintenance is often done by individuals other than
    the original author of the software, poor readability can make the task
    extremely challenging.

- portability -- the ease with which programs can be moved from one
  implementation to another. Portability is most strongly influenced by the
  degree of standardization of the language.

- generality. the applicability of language to a wide range of applications.

- well-definedness. the completeness and precision of the language's official
  document.

Language evolutions
===================
Fortran
-------
- Fortran 且至今仍然被科学计算领域使用. 这有以下几个原因:
  
  * 在科学计算领域, 效率是最主要考虑的因素, 而在这个方面后来的语言并没有显著提
    高.

  * Many legacy code are written in Fortran.

  * Fortran is easy to learn.

entity
======
- first-class entity and second-class entity. it is a term that barely has a
  technical meaning.  The meaning, when present, is usually comparative, and it
  applies to a thing in a language that has more privileges than a comparable
  thing.[SOFST]_

  Usually, first-class entity is an entity that can be passed as argument to
  functions, returned from function, modified, assigned a value, etc.
  
  But this is not always the case. The exact meaning of first-class/second-class
  thing is only made clear through context.

.. [SOFST] `About first-,second- and third-class value Ask Question <https://stackoverflow.com/questions/2578872/about-first-second-and-third-class-value/2582804#2582804>`_

subprogram
==========
- recursion. A function is recursive if it calls itself. If the only place the
  function calls itself is the last expression of the function, then the
  function is tail-recursive.
paradigms
=========
- different paradigms of programming are essentially different design
  patterns, i.e. different ways to organize your code.

imperative programming
----------------------
- A programming paradigm that uses statements that changes a program's
  state. In imperative languages, programmer gives imperative commands
  to computer, to mutate program's state.

- procedural programming is a type of imperative programming.

- 注意 OOP 不一定就是 imperative programming. 主流的 OOP 语言基本上都是
  imperative 的, 但 OOP 概念本身并不意味着 imperative programming. 例如
  scala 就可以是 OOP + FP.

procedural programming
----------------------


object-oriented programming
---------------------------
- Class is an optional design pattern in software design. You can use it or
  not.

- In principle, the motivation for object-oriented programming is very simple:
  all but the most trivial programs need some sort of structure. The most
  straightforward way to do this is to put data and operations into some form
  of containers. The great idea of object-oriented programming is to make these
  containers fully general, so that they can contain operations as well as
  data, and that they are themselves values that can be stored in other
  containers, or passed as parameters to operations. In this way the simplest
  object has the same construction principle as a full computer: it combines
  data with operations under a formalized interface.

- The concept of OOP is very natural. It simulates the structure of the real
  world and the interactions of real world objects.

- 一门语言支持 OOP, 有助于提高它的可扩展性 (scalability). 因为实行 OOP 的相关设
  计概念有助于提高程序的结构性, 让它更清晰, 更易读, 更易写, 更易维护.

- deviations from OOP.

  * primitive values that are not objects.

  * static fields and methods that are not members of any object.

  These deviations have an tendency to complicate things and limit scalability.

concepts
^^^^^^^^

class
""""""
- class (or data structure), as the unit of encapsulation, which contains
  data and its associated operations (例如你能对这个类 (或者它的实例) 做什么,
  或者这个类 (或者它的实例) 能为你做什么 -- 根据它所包含的数据、状态).

- class instance. 一般来讲 class 是对象的模板. 而对象, 即实例才是真正能为你办事
  的小黄人. (当然, class 作为另一种更抽象的对象, 本身也可包含 class-level 的数据
  和操作, 即 class-level attributes 和 methods.)

three properties of OOP
""""""""""""""""""""""""

- encapsulation. 封装是 class 的天然属性. 很显然, 将一组数据和一组相应操作整理在了
  一个类这个创建的概念下. 封装也是一种模块化思想.

- inheritance. 继承是子类和父类之间的共性. 它们可以有共同的数据, 共同的方法 (即操作).

- polymorphism. 多态是子类相比父类的特性. 同一个操作, 子类可以与父类相比略有调整
  或完全不相同, 却保持相同的 API. 多态可以看作是 duck typing 的弱化形式.

  个人认为, 多态还可以指子类相比父类原创的部分, 即增加的、在父类中完全不存在的
  数据和功能. 这也是一种分化, 一种演化, 也即多态.


一个好的类体系的设计, 是一种艺术. 在一个系统中, 如何将多个相互关联的概念整理
成一个个相互作用的实体 (即 class), 如何设计实体之间的相互作用, 如何设计一系列
同类实体之间的共性和特性 (即设计抽象类与具体类的继承和多态). 这些学问, 都是
需要不断思考、不断体会的.

other concepts
""""""""""""""
- introspection. Introspection is an operation that inspects an instance at
  runtime for its class hierarchy and other static information.

- duck typing. Duck typing 是 interface/protocol 的一般化, 是一种更广泛的多态性.

functional programming
----------------------
- The foundation of FP: Alonzo Church's lambda calculus (1930s).

- Lisp is the first FP language.

- Popular FP languages: Lisp, Scheme, Standard ML, Erlang, Haskell, OCaml, F#.

- Functional programming 似乎可以很好地使用 tail recursion, 让递归代码十分高效.
  所以 FP 从来不怕递归.

- Two main ideas of FP: 
  
  * function as first-class entity, meaning that:
   
    - functions can be passed as arguments, like other values.
     
    - functions can be returned from functions, like other values.

    - functions can be stored in variables, like other values.

    - functions can be defined inside another function, like other value
      definitions.

    - functions can be used without a name -- function literals, like other
      value literals.

    This property provides great expressiveness to a language, which often
    leads to very concise and legible programs.

  * functions shouldn't have side effects. They should only map input values
    to output values, rather than change data in place.

    This property 意味着 immutable data structures.

- higher-order functions: Functions which take other functions as arguments,
  and/or which return other functions as their results

- referential transparency. A property of functions that are independent of
  temporal context and have no side effects. An invocation of a referentially
  transparent function could be replaced by its result without affecting the
  program's semantics.

- Functional languages encourage immutable data structures and referentially
  transparent functions.

scope
=====
- Scope is a set of nested lookup table.

- lvalue & rvalue.
  
  * lvalue. lvalue resolution aims to find the target variable container in memory.
    It happens during variable assignment.

  * rvalue. rvalue resolution aims to find the target variable's value.

lexical scope
-------------
- lexical scope is scope that is defined at lexing time.  In other words, scope
  is well-defined by variable/function/etc. declarations at author-time.

- In lexical scoping model, value resolution is performed by traversing the
  nesting of "scopes" in program text.

- Compiler construct scope structure during compilation.  Runtime engine
  lookups scope structure to resolve lvalues and rvalues.

dynamic scope
-------------
- In dynamic scoping is defined only at runtime. And it's dynamic, because the
  current scope depends on the current call stack, so it changes as program
  runs.

- value resolution is performed by traversing down stack frames.

evaluation
==========

- 两种运算类型: strict evaluation, lazy evaluation.

strict evaluation
-----------------
- all parts of an evaluation will be evaluated completely before the value of
  the expression as a whole is determined.

lazy evaluation
---------------
- In order to evaluate an expression in the language, you only evaluate as much
  of the expression as is needed to get the final result.

data types
==========
type checking
-------------
- the benefits of static type checking system.

  * verifiable properties. Static type systems can prove the absence of certain
    run-time errors. E.g., 一个运算符的两个算子类型是否相符; 函数调用与它的定义
    signature 是否相符等问题.

    可以看到, 静态类型检查能做的只是一些相对简单的检查. 那么静态类型检查又有
    什么用呢? 这些检查完全可以由单元测试覆盖到 (还能覆盖更多问题). 答案是:

    - static type checking 可以减少单元测试的数量, 一些性质由静态类型检查来
      保证即可.

    - 单元测试不能取代静态类型检查带来的保证. 因为测试永远不能证明没有 bug, 而
      静态类型检查虽然能提供的保证很有限, 却是在数学上可证明的正确性保证. (the
      guarantees that static typing gives may be simple, but they are real
      guarantees of a form no amount of testing can deliver.)

  * Safe refactorings. A static type system provides a safety net that lets you
    make changes to a codebase with a high degree of conﬁdence. 对于很多简单重
    构, 所做的修改会让类型检查失败, 对所有 type checking violation 的地方进行
    更正, 即是对所有需要修改的地方做了相应的修改.

  * Documentation. Static types are program documentation that is checked by
    the compiler for correctness.

Language constructs
===================
Programs of different sizes tend to require different programming constructs.
