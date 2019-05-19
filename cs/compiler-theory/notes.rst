architecture overview
=====================
machine language
----------------
- processor. A processor is a collection of circuits that provides a
  realization of a set of primitive machine instructions.

- macro-instruction. 一个处理器对外支持的指令集. macro-instructions 可能是
  直接由硬件集成电路实现, 或由 micro-instructions 实现. 后者属于更底层的指令集.
  micro-instructions 是直接由硬件集成电路实现的. macro-instructions 相当于是处
  理器的 API, 而 micro-instructions 相当于处理器的实现细节.
  
- The machine language of a computer is its instruction set. 这是一台物理计算机
  能识别的唯一语言. 机器语言一般是非常底层的. 对所有高级语言的支持, 都是由虚拟
  计算机 (virtual computer) 实现的.

- 为什么机器语言一定要非常底层?

  理论上和实际上, 处理器确实可以使用高级语言来设计和实现. 例如 Lisp machine.
  但是这样有两个弊端:
  
  * 基于高级语言的处理器的硬件实现会很复杂、很贵, 底层的、简单的指令用硬件会简
    单很多, 从而成本也更低.

  * 基于高级语言的处理器只能适用用于特定高级语言的编程, 灵活性差. 这是因为它很
    难用于其他任意高级语言, 要开发以该高级语言为目的语言的编译器, 这样很不合理,
    增加了不必要的复杂度. (这类似于矢量数学中, 利用一组任意非平行矢量作为基矢
    不是不行, 只是会比单位正交基矢麻烦很多.)

virtual computer
----------------
- virtual computer. 由处理器, 机器语言, 操作系统, 特定编程语言的 implementation
  software 层叠而成的一整套系统, 它接受该语言的源程序. 这样的一个系统即虚拟计算
  机. 例如, 处理器 + 指令集 + 操作系统 + JVM + javac 编译器构成一个 virtual
  Java computer.

language implementation methods
-------------------------------
compilation
^^^^^^^^^^^
- Source language program is translated into machine language code, and
  executed on physical processor.

- advantages: very fast execution.

- general procedure

  1. Lexical analysis. The lexical analyzer gathers the characters of the
     source program into lexical units (tokens). lexical units include:
     identifiers, special words, operators, punctuation symbols.

     Lexical analyzer ignores comments in the source program.

  2. Syntax analysis. The syntax analyzer takes the lexical units from the
     lexical analyzer and uses them to construct parse trees. Parse trees
     represent the syntactic structure of the program. In many cases, no actual
     parse tree structure is constructed; rather, the information that would be
     required to build a tree is generated and used directly.

  3. Semantic analysis, intermediate code generation and optimization.
       
     The semantic analyzer is an integral part of the intermediate code
     generator. The semantic analyzer checks for errors, such as type errors,
     that are difficult, if not impossible, to detect during syntax analysis.

     The intermediate code generator produces a program in a different
     language, at an intermediate level. Intermediate languages sometimes look
     very much like assembly languages, and in fact, sometimes are actual
     assembly languages.

     Optional optimization. Most optimization is done on the intermediate code,
     because many kinds of optimization are difficult to do on machine
     language.

  4. The code generator translates the (optimized) intermediate code into
     machine language program.

  5. linking. The linker connects the user program to the system programs and
     pre-compiled user programs (in the form of libraries) by placing the
     addresses of the entry points of the external subroutines in the calls to
     them in the user program.

  Other notes:

  * symbol table. a database for the compilation process. contains type and
    attribute information of user-defined names. Symbol table is built by
    lexical analyzer and syntax analyzer, and is used by semantic analyzer
    and code generator.

pure interpretation
^^^^^^^^^^^^^^^^^^^

hybrid implementation
^^^^^^^^^^^^^^^^^^^^^

misc
====
steps:

- tokenization/lexing. breaking up a string of characters into meaningful
  chunks, called tokens. 

  The difference of tokenization and lexing is between stateless and stateful
  way of doing things.  If the tokenizer were to invoke stateful parsing rules
  to figure out whether a should be considered a distinct token or just part of
  another token, that would be lexing.

- Parsing. taking a stream (array) of tokens and turning it into a tree of
  nested elements, which collectively represent the grammatical structure of
  the program. This tree is called an "AST" (Abstract Syntax Tree).

- Code generation. the process of taking an AST and turning it into executable
  code.
