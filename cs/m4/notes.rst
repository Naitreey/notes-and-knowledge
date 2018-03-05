overview
========

- m4 is a macro/template language and a filter program.

- typical usage:

  * sendmail.cf

  * GNU Autoconf

  * SELinux

- **NOTE**: m4 在功能上与 python 的 jinja2 等 template language 是类似的.
  在可能的情况下, 尽可能选择使用 jinja2 而不是 m4 这种语法极其晦涩的工具.

  其实从这里我们可以看出, 如今 m4 的处境实际上和 awk/sed 之类的工具有些
  类似. 如果我们只是想快速地解决某些文本处理工作, 或者是主要和 shell 结合
  使用, 则 awk/sed 是很合适的; 但凡是其他情况, 使用 python 来处理都是更加
  合适的选择. m4 也是如此, 如果是快速地解决某些 macro/template 相关的问题,
  或是和 shell 结合使用, m4 很合适; 但其他情况下, python/jinja2 组合都会
  是更合适的选择.

syntax
======

parentheses
-----------

- ``(), [], {}`` 等若要作为文本使用, 应该 quoted, 避免出错.

whitespace handling
-------------------
- whitespace chars handling. 源文件中所有在 macro 之外出现的 space, tab,
  newline, etc. 任何 whitespace characters 都会保留至输出中.

- No whitespace is allowed between macro name and opening parenthesis
  of its argument part ``()``.
  
- 在 ``(...)`` 里面, 每个参数之前的 whitespaces 会被忽略, 但参数之后
  至 ``,``, ``)`` 的 whitespaces 不会被忽略, 也就是说它们仍然是参数的一部分.

quoting
-------

- m4 uses latex style quoting ``\`'``. Quoting suppresses macro
  expansion. 或者说, quoting makes content show up verbatim in output.
  quoted content can include newlines.

- macro definitions should be quoted, 避免 macro identifier 被别的 macro
  expansion 错误替换掉.

comment
-------

- ``#`` starts a line comment. In m4, ``#`` comments are echoed to
  the output.

- comment char can be changed by ``changecom`` macro.

escaping
--------
m4 has no escape character. 所以对于 backtick quoting char, 若需要用在其他
地方, 首先应该先使用 ``changequote``, 让 backtick 不再是特殊字符.

macro call
----------

- 在 argument list 中, empty argument 表示相应位置的参数为 empty string,
  等价于 ``\`'``::
    ifelse(macro,,`empty', `not empty')

- a pair of empty parentheses does NOT mean no argument, rather it means
  ONE argument whose value is empty string::
    define(`show', ``$0': $# args: $@')dnl
    show()hey                   # -> show: 1 args: hey
  若要 call macro function 不带参数, 需要去掉括号. 这可以看出 m4 中不区分
  变量和函数, 两者是一个概念, 不同使用方式产生不同结果. 例如::
    define(`func', `ifelse($#, 0, `variable', ``$0': function, args: $@')')
    func
    func()
    func(1,2,3)
    
scope
-----
All macros have global scope.

若要类似 local macro 的效果, 可以使用 pushdef & popdef.

workflow
========

tokenization
------------
Inputs are tokenized into quoted strings, macro arguments, identifiers,
numbers and other symbols (punctuation characters).

Whitespace (including newlines), numbers and punctuation usually mark token
boundaries.

由于 numbers 也是 token boundaries, 注意例如 ``99Version9`` 实际上是 2 个
token ``99`` 和 ``Version9``, 并且是合法的.

processing
----------
In general, m4 passes input tokens and separators straight through to the
output, making no change except to

- remove the quotes surrounding quoted string tokens. 注意 quote removal
  是在 scan 的过程中处理的. 考虑以下情况::
    define(AUTHOR, you)
    ``AUTHOR'' is AUTHOR. # -> `AUTHOR' is you.

    define(`x', ``xyz'')
    x                     # -> xyz
  在第二个例子中, 由于对 xyz 部分 scan 了两遍, 去掉了两层 quotes.
 
- processing macros with by following procedure

  * it reads in the macro's arguments (if any)
  
  * it determines the expansion of the macro (with arguments) and inserts this
    expansion at the beginning of its input. 对于 macro name 的 expansion 本身
    不受 ``()`` 部分的影响. macro call 整体的 side effect 是另外计算的.
  
  * m4 continues scanning the input, starting with the expansion. 也就是说
    替换的结果仍然接受 macro expansion 检查.
  
  If while reading in a macro's arguments, m4 encounters another macro then it
  repeats this process for the nested macro. Unless a nested macro is quoted, it
  is expanded immediately::
    # unquoted
    define(`definenum', define(`num', `99'))
    num       # -> 99
    definenum # ->    (empty string)

    # quoted
    define(`definenum', `define(`num', `99')')
    num           # -> num (not touched)
    definenum num # ->  99 (space + 99)
  
  Arbitrary nesting is possible -- with (ordinarily) an extra layer of protective
  quotes at each level of nesting::
    define(`definedefineX',`define(`defineX',`define(`X',`xxx')')')
    defineX X           # -> defineX X
    definedefineX X     # ->  X
    defineX X           # ->  xxx

  若要避免在 macro expansion result 中 rescan possible macro expansion, 需要用
  两层 quotes::
    define(`stmt', ``define(`Y', `yyy')'')
    stmt                # -> define(`Y',`yyy')
    Y                   # -> Y

  注意 macro call 时, macro name 和后面 ``(...)`` 是一起处理的, 一起从 input
  stream 中删除掉, 再将结果插入到 input stream 中::
    define(`plus', `+')
    define(`oper', `plus')
    oper()oper  # -> plusoper

If ever m4 seems to hang or stop working, it is probably because a faulty macro
has sent it into an infinite loop.

m4's usual approach of rescanning the expansion of a macro can be a problem
with macros that operate on strings. Because there's no direct way to prevent
rescaning on the output string of these operations.

buitlin macros
==============

- A macro consists of a sequence of ASCII letters, underscores, and digits,
  where the first letter must be underscore or letter.

- 所有必须要有 arguments 的 builtin macros 的定义中, 保证了如果 invoke macro
  时没有提供参数, 即没有 ``()`` 部分, 则 expands to macro name itself. 这样
  避免了对输入文字错误处理.

  这种行为可以在 user-defined macro 中效仿. 例如::
    define(
        `reverse',
        `ifelse($#, 0, ``$0'', $1, , , `reverse(substr($1, 1))`'substr($1, 0, 1)')')dnl

- 所有 builtin macros 可通过 ``-P`` flag 转换成 ``m4_`` prefix 的另外形式.
  这用于避免 macros 和输入文字冲突, 进行了不该进行的 macro expansion.

macro definition
----------------
- For each macro, m4 actually creates a stack of definitions – the current
  definition is just the one on top of the stack. The definition stack can
  be manipulated by ``pushdef`` & ``popdef``::
    define(`X', 1) # global
    pushdef(`X', 2)dnl
    # use X
    popdef(`X')dnl

define
~~~~~~
::
  define(MACRO, EXPANSION)

- define macro definitions. ``define`` macro itself expands to empty string.

- m4 中不区分变量和函数, 定义的 MACRO 既可以单独使用, 也可以后面加上 ``(...)`` 进行
  macro call.

- 定义函数形式 macro 时, EXPANSION 部分支持以下参数:
  ``$0`` 为 macro name, ``$1`` - ``$N`` 为位置参数, ``$#`` 为参数数目,
  ``$*`` expands to the list of arguments, ``$@`` does the same but protects
  each one with quotes to prevent them being expanded.


- 由于 EXPANSION 会进行 rescaning, 可定义 recursive macro. 例如::
    define(`len',`ifelse($1,,0,`eval(1+len(substr($1,1)))')')

- In GNU m4, ``define(X, Y)`` works like ``popdef(X)pushdef(X, Y)``,
  i.e., it replaces only the topmost definition on the stack.

- 在 macro definition 中, 必要时可以加入 empty string ``\`'`` 作为
  token 之间的 separator. 避免 macro expansion 之后两个 token 连在一起
  了, 无法识别为预先定义的 macro. 例如::
    define(
        `reverse',
        `ifelse($#, 0, ``$0'', $1, , , `reverse(substr($1, 1))`'substr($1, 0, 1)')')dnl

undefine
~~~~~~~~
::
  undefine(MACRO)

only work correctly when its argument is quoted.
If MACRO isn't defined, nothing happens.

shift
~~~~~
::
  shift(MARCO, ...)
expands to the same list of arguments with the first one removed.
注意对一个参数的 list shift 结果仍然是一个参数, 只是参数变成了 empty string.
shift 无法得到 0 个参数的情况.

pushdef
~~~~~~~
::
  pushdef(MACRO, VALUE)

push a definition on top of the stack of MACRO definitions.

If the macro hasn't yet been defined then pushdef is equivalent to define.

popdef
~~~~~~
::
  popdef(MACRO1, MACRO2, ...)

pop out topmost definition of the specified macros from their stacks.

It is not an error to popdef a macro which isn't currently defined; it simply
has no effect.

runtime manipulation
--------------------

dnl
~~~
- dnl -- delete newline.

- 同时 discard everything up to the newline. 这 tm 才是真正的 comment char in m4.

- 因为默认情况下 m4 源文件中的所有 newline 会被原样搬到输出中, 若想要删掉某个
  newline, 则需要使用 dnl macro 在行尾.

changequote
~~~~~~~~~~~
::
  changequote(LEFT, RIGHT)
  changequote

LEFT/RIGHT can be multi-char sequence.

without parameters, quotes are restored to default.

Don't choose the same delimiter for the left and right quotes: doing so makes
it impossible to have nested quotes.

Don't change a quote delimiter to anything that begins with a letter or
underscore or a digit; m4 won't complain but it only recognizes a delimiter if
it starts with a punctuation character. 

changecom
~~~~~~~~~
::
  changecom(START)
  changecom(START, END)
  changecom

change comment delimiter. defaults are restored without args.

include
~~~~~~~
::
  include(file)

include path can be specified by ``-I`` option or environ ``M4PATH``.

sinclude
~~~~~~~~
::
  sinclude(file)

silent include, doesn't complain if the file does not exist.

builtin
~~~~~~~
::
  builtin(MACRO, arg, ...)

access builtin MACRO and pass through args via ``builtin`` macro.

indir
~~~~~
::
  indir(MACRO, arg, ...)

call macro indirectly, useful where the name of the macro to be called is
derived dynamically or where it does not correspond to a token (i.e., a macro
name with spaces or punctuation).

redirection
-----------

- There is an implicit ``divert`` and ``undivert`` when m4 reaches the end of the
  input, i.e., all buffers are flushed to the standard output.

divert
~~~~~~
::
  divert(N)
  divert

divert output according to ``N``.
without arg equals to ``divert(0)``.

possible values:

- -1. process input source but do not output anything.
  common usage::
    divert(-1)
    <definitions...>
    divert(0)dnl

- 0. restore default, i.e., divert to stdout.

- positive number. temporary buffers which are output in numeric order at the
  end of processing.

undivert
~~~~~~~~
::
  undivert(N)
  undivert(file)
  undivert

appends the contents of diversion N to the current diversion, then emptying it.

argument 还可以是文件路径. 这样是把 file 的内容引入当前 stream, 注意文件内容不会
解析. 这是与 ``include`` macro 的区别.

Without arguments, undivert retrieves all diversions in numeric order.

``undivert(0)`` has no effect: diversion 0 is stdout which is effectively an
empty buffer.

divnum
~~~~~~
expands to the number of the currently active diversion

conditionals
------------

ifdef
~~~~~
::
  ifdef(MACRO, TEXT1, TEXT2)
  ifdef(MACRO, TEXT1)

output TEXT1 if MACRO is defined, output TEXT2 (when exists) if undefined.

ifelse
~~~~~~
::
  ifelse(MACRO1, MACRO2, TEXT1, TEXT2)
  ifelse(MACRO1, MACRO2, TEXT1, MACRO3, MACRO4, TEXT2, TEXT3)

output TEXT1 if MACRO1 equals to MACRO2, otherwise output TEXT2.
第二种形式相当于 nested ifelse.

arithmetics
-----------

eval
~~~~
::
  eval()

其参数为算数表达式, 输出计算结果.

incr, decr
~~~~~~~~~~
::
  incr(MACRO) -> eval(MACRO+1)
  decr(MACRO) -> eval(MACRO-1)
对 MACRO 值加减 1.

strings
-------

len
~~~
::
  len(TEXT)

substr
~~~~~~
::
  substr(TEXT, START, END)
  substr(TEXT, START)

index
~~~~~
::
  index(TEXT, SUB)

若 SUB 不在 TEXT 中, 输出 -1.

translit
~~~~~~~~
::
  translit(TEXT, SET1, SET2)

define map from SET1 to SET2, with TEXT as input.

system access
-------------

syscmd
~~~~~~
::
  syscmd(...)

output of syscmd is not interpreted.

esyscmd
~~~~~~~

output of esyscmd is executed.

sysval
~~~~~~

expands to exit status of the last shell command.

mkstemp
~~~~~~~
::
  mkstemp(pattern)

creates a temporary file and expands to the filename – this name will be the
(optional) prefix with the six X's replaced by six random letters and digits. 

debugging and error
-------------------

debugmode
~~~~~~~~~
::
  debugmode(flags)
  debugmode

turn on debug mode for a section of m4 source. without argument turns off debug
mode. e.g.,::
  debugmode(V)
  ...
  debugmode

dumpdef
~~~~~~~
::
  dumpdef(MACRO, ...)
  dumpdef

outputs to standard error the formatted definition of each argument – or just
<macro> if macro is a builtin; dumpdef without arguments dumps all definitions
to stderr, including builtins. 

注意这个不是 expansion.

defn
~~~~
::
  defn(MACRO, ...)

expand to definition of macros.

m4exit
~~~~~~
::
  m4exit(N)

exit now with status N.

errprint
~~~~~~~~
::
  errprint(msg)

print msg to stderr.

useful custom macros
====================

flow control macros
-------------------

for
~~~
::
  define(`for',`ifelse($#,0,``$0'',`ifelse(eval($2<=$3),1,
  `pushdef(`$1',$2)$4`'popdef(`$1')$0(`$1',incr($2),$3,`$4')')')')

  for(`x',1,3,`for(`x',0,4,`eval(5-x)') ') # -> 54321 54321 54321

foreach
~~~~~~~
::
  define(`foreach',`ifelse(eval($#>2),1,
    `pushdef(`$1',`$3')$2`'popdef(`$1')dnl
  `'ifelse(eval($#>3),1,`$0(`$1',`$2',shift(shift(shift($@))))')')')

while
~~~~~
::
  define(`while',`ifelse($#,0,``$0'',eval($1+0),1,`$2`'$0($@)')')


CLI usage
=========

- m4 read from FILEs or stdin.

- ``-D``, ``--define``. 可以在命令行上 define macro.

- ``-P``, ``--prefix-builtins``. prefix all builtins with ``m4_``.

- ``-I``, ``--include``. add m4 include path.

- ``-d``, ``--debug``. 常用 debug level: ``V``, which turns on all debug info.
