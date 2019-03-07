# overview

-   BASH -- Bourne-Again SHell

-   bash/shell script as a language is an interpreted command language.

-   Bash as a shell is the interpreter of the bash command language.

    *   bash 对脚本的解析不包含预编译阶段. 不仅如此, bash 是依次对每个 logical
        line 进行 read, parse, execute 操作的. 而不是对整个脚本进行这三个步骤.
        所以只有执行到特定一行时才知道该行有没有语法错误.  (这也给调试带来了很
        多麻烦.) 这是与 Python, JavaScript 等 interpreted language 的一个区别.
        [[interpreted]](#interpreted).

-   Bash incorporates useful features from Korn shell `ksh`, C shell `csh` and
    Z shell `zsh`.

# terms

```
                   +------------+       token       +--------------+
                   |                                               |
                   |                                               |
                   |                                               |
                   +                                               +

    +------+     word     +-------+                  +-----+    operator    +---------+
    |                             |                  |                                |
    |                             |                  |                                |
    |                             |                  |                                |
    |                             |                  |                                |
    +                             +                  +                                +

identifier                     value           control operator             redirection operator

```

-   token. A sequence of characters considered a single unit by the shell. It's
    a word or a operator.

-   word. A sequence of characters treated as a unit by the shell. Words are
    separated by metacharacters.

-   reserved word. A word that is reserved by shell.

-   identifier (name). A word consisting solely of letters, numbers, and
    underscores, and beginning with a letter or underscore. Names are used as
    shell variable and function names.

-   metacharacter. A character that, when unquoted, separates words. the followings
    are metacharacters:

    ```sh
     (blank: space or tab) | & ; ( ) < >
    ```

-   operator. A control operator or redirection operator. Operators consist of
    one or more unquoted metacharacter.

-   control operator. A token that performs execution controls. the followings are
    control operators

    ```sh
    (newline) || && & ; ;; ;& ;;& | |& ( )
    ```

-   blank. a space or tab char.

## examples

```sh
git config --global user.name 'Naitree Zhu'      # 5 tokens: 5 words
sleep 10 && foo=1 systemctl poweroff&            # 7 tokens: 5 words, 2 operators
```

# shell's execution workflow

1.  Read input. from stdin, or a file argument, or argument string of `-c` option.

2.  Breaks input into tokens (obeying [quoting](#quoting) rules), 识别 words
    and operators. 即 lexical analysis.

    *   [Aliases](#aliases) are expanded in this stage. 因 alias 中可以包含各种复
        杂的多种 words and operators.

3.  Parse tokens into command structures, including [simple](#simple-commands)
    and [compound](#compound-commands) commands. 此时只是界定出了不同命令的分界
    点, 以及 compound command 与 simple commands 的嵌套结构. 对每条 simple
    command 本身的机构还不清楚.

4.  对于每条 simple command,

    *   确定是否有 [variable assignments](#variables). 只有 leading words of the form
        `identifier=value` 被认为是变量赋值, 其中 `identifier` 必须是合法的
        identifier. 若有, 保留至命令执行阶段, 并从 simple command 中删除.

    *   确定是否有 [redirections](#redirections). 若有, 相关的 operator &
        operands 保留到命令 执行阶段使用, 并从 simple command 中删除.

    *   Perform various [shell expansions](#shell-expansions). If any words
        remain after expansion, the first word is taken to be the name of the
        command and the remaining words are the arguments.

        由于 expansion 时 assignment & redirection 已经移除, 所以它们的位置不影响
        command name 的确定.

5.  Perform redirections. From left to right.

    由于 redirection 在命令执行之前进行, 所以类似以下操作不成立:

    ```sh
    grep pattern file >file
    ```

6.  For simple command, try to locate the command name. If command name
    contains `/`, 不需要定位. 否则, 按照以下步骤定位.

    *   Use [shell function](#functions) of that name, if one exists.

    *   Use [shell builtin](#builtins) of that name, if one exists.

    *   Search an in-memory hash table for remembered commands.

    *   Search each directory in `$PATH`, in that order, for an executable
        file of the same name.

7.  Execute command, pass in arguments. variable assignment 修改命令的环境变量.
    如果在 expansion 后 command name 为空, variable assignment 修改当前 scope
    的 shell variables.

8.  If command executes, wait for command to complete or carry on (for
    background job).

# quoting <a id="quoting"></a>

-   不该将 quoted words 称为字符串. 在 shell language 中, 所有 words 都是字符串,
    语言本身不包含其他任何数据类型.  并不存在所谓字符串和其他数据类型的区分.

-   在 shell language 中, quoting 的主要目的是转义, 而不是创建 (并不存在的) 字
    符串. 也就是说, 将 metacharacter 转义为 literal 字符, 从而影响 shell 对
    input 的 tokenization 结果.

    *   这带来的一个用法是, 使用 quoting 跳过对 alias 的替换. 例如

        ```sh
        \rm /path
        ```

-   shell 识别三个 quoting character, 注意它们不是 metacharacter, 所以不会
    separate words:

    ```sh
    \ ' "
    ```

-   shell 提供了 5 种 quoting 机制. 分别是: escaping, single quotes, double quotes,
    ANSI-C quoting, locale-specific translation.

## escaping

-   `\\`  preserves the literal value of the next character that follows.

-   注意到 `\\` 并不是 metacharacter.

-   For ``newline``, because the literal meaning of ``newline`` is just generating
    a newline, without its control operator effect, 因此 ``\newline`` 的效果是
    line continuation.

## single quotes

-   All characters between a pair of single quotes preserve their literal meanings.
    Including `'` itself, therefore any `'` char terminates a single quoted
    sequence.

## double quotes

-   All characters except for `$`, `\``, `\\` and `!` between double quotes preserve
    their literal meanings.

-   注意 `$`, `\``, and `!` 并不是 metacharacter.

-   `\\` 平时在 double quotes 里面其实仍保持 literal meaning, 只有当位于 `$`,
    `\``, `"`, `\\`, `newline` 这些具有特殊意义的字符前面时, 具有 escaping 的作用.

    ```sh
    echo "\n" # print two chars
    ```

-   The backslash preceding the ‘!’ is not removed.

## ANSI-C quotes
```sh
$'string'
```

-   Characters remains their literal meanings, except that `\<char>` escape
    sequences are replaced by actual escape character according to C standard
    (with extensions). Rather than leaving as two separate characters.

    ```sh
    echo 'You piece of shit\U1F644'
    echo $'You piece of shit\U1F644'
    ```

-   notable escape sequences.

    *   `\nnn`

    *   `\xHH`

    *   `\uHHHH` BMP chars. leading zeros can be omitted.

    *   `\UHHHHHHHH`. leading zeros can be omitted.

# comments

Line comments `#` is enabled in

- non-interactive shell

- interactive shell with `interactive_comments` shopt set.

# commands

Commands 分两类

*   command lists

    -   一个 command list 包含一个或多个 pipeline.

    -   一个 pipeline 包含一个或多个 simple commands.

    -   一个 simple command 是一个 compound command 或者是一个命令和它的参数的
        组合.

*   compound commands

    -   一个 compound command 包含一个或多个 command lists.

## simple commands <a id="simple-commands"></a>
-   a simple command is a sequence of words separated by blanks, terminated by
    control operators.

-   a simple command's exit status.

    *   若命令自行结束, exit status 根据 waitpid(3) 得到. 即 0~255.

    *   若命令 is killed by a signal, exit status 是 128+signum.

-   examples:

    ```sh
    ls -ld abc
    ```

## pipelines
-   A pipeline is a sequence of simple commands, separated by control operator
    `|` or `|&`.

    ```sh
    [time [-p]] [!] simple_command [ | or |& simple_command ]*
    ```

    注意, `time` is bash keyword, rather than builtin.

-   `|&` 等价于 `2>&1 |`.

-   在一个 pipeline 中,

    *   如果两个命令通过 `|` 连接, 前一个命令的 stdout 与后一个命令的 stdin
        通过 pipe 连接. This connection is performed before any redirections
        specified by the command.

    *   如果两个命令通过 `|&` 连接, 前一个命令的 stdout 和 stderr 都通过 pipe
        与后一个命令的 stdin 连接. 由于它本质上是 `2>&1 |`, 所以可以看出,
        `2>&1` 部分是在 `|` 以及 command 本身的 redirection 之后才进行的.

-   注意, 当 redirection 出现在 pipeline 中的时候, 最后应用的 pipe/redirection
    才是决定最终效果的.

## command lists

## compound compands <a id="compound-commands"></a>

# variables <a id="variables"></a>

## data types

## variable attributes

## scope

bash script 使用的是 dynamic scope, 而不是 lexical scope. 因而在 name
resolution 方面与常见 现代语言不同.

name resolution 时, 依据 call stack, 从顶层 (即当前函数) 开始, 向下搜索 (caller
方向), 直至 global scope. 若最终没找到该变量, 对于 rvalue resolution, expands
to empty string; 对于 lvalue resolution, 在 global scope 创建该变量 (这一点类似
js 中 lvalue 的处理).

在 nested scope 中, inner scope 声明的变量在相应 scope 中覆盖 outer scope 的同
名变量. 但只要 出了 scope (即 return to caller stack 后), outer scope 中的变量
赋值就继续有效.

以 dynamic scope 思想为基础, 我们可以理解以下几个 statement 的清晰含义

```sh
x=1
declare x=1
declare x; x=1
```

-   第一个 statement 经常用于声明全局变量 `x` 并赋值, 但实际上它不是变量声明而
    是一种偷懒的赋值.  实际上, 这是对 lvalue 的赋值. 根据 lvalue resolution 机
    制, `x` 变量可能是在 caller function 中声明的, 或者在全局中声明的, 或者是没
    有声 明的. 却不一定是全局的. 总之, 这个 statement 只应该用于变量赋值而不该
    是代替变量声明.

-   第二个 statement 是标准的变量声明. 并且具有清晰的 scope -- 出现在 global
    scope, 就是声明 global variable; 出现在 function scope, 就是声明
    function-scope variable.

-   第三个 statement 是标准的先声明再赋值.


## special variables

-   `PROMPT_COMMAND`. a command to execute before each time `$PS1` is printed.
    该变量的用处:
    *   设置需要在 PS1 中引用的参数. 注意不该在 `PROMPT_COMMAND` 中直接设置 PS1 
        的值.
    *   执行任意命令, 这取决于 shell plugin 的功能. 例如 autojump 更新路径数据库.
    *   设置 terminal title.
    `PROMPT_COMMAND` generally should not be used to print characters directly
    to the prompt. Characters printed outside of PS1 are not counted by Bash,
    which will cause it to incorrectly place the cursor and clear characters.
    See also [this](#prompt-command).

# expansions <a id="shell-expansions"></a>

# redirections <a id="redirections"></a>

-   注意 redirection 是从左至右来执行的.

-   要清楚 redirection 的本质:

    *   对于 `n>&m`, 本质是:

        ```c
        dup2(m, n);
        close(m);
        ```

    *   对于 `n>file`, 本质是:

        ```c
        m = open(file, mode)
        dup2(m, n);
        close(m);
        ```

-   例如

    ```sh
    echo a 1>&2 2>/dev/null
    ```

    仍然会有输出, 因为从左至右先把 stderr fd 对应的 file description 赋给了 stdout fd,
    此时这个 file description 仍然是某个 tty; 后把 /dev/null 文件打开后生成的 file
    description 赋给了 stderr fd. 如果把两个 redirection 反过来才是正确的.

# functions <a id="functions"></a>

# flow control

# builtins <a id="builtins"></a>

-   Builtins are commands that are actually executed by bash shell itself, rather than
    by an external program.

-   Why bash needs builtin commands:

    *   some functionalities need to modify the runtime environment of the shell itself.
        Therefore impossible to implement as separate utility. E.g., `cd` changes
        shell's CWD.

    *   The essential language constructs needs to be executed by shell itself, because:

        -   Language constructs shows up every frequent in shell script. This
            is the most efficient way, without spawning a subprocess.

        -   Language constructs control the workflow of command execution. 这属于控制类的
            meta operation. 因此应该由 shell 统一控制. 例如:

            ```sh
            if true; then
                cmd1
            else
                cmd2
            fi
            ```

            应该是 shell 去控制该执行 cmd1 or cmd2, 并且由 shell 直接去 spawn cmd1 or cmd2.
            而不是由 `if` program 去控制和执行.

# analysis by examples

```sh
grep pattern file >file

cat ~/Documents/'Bash 'Reference\ Manual.pdf

alias rm='rm -i'
\rm /tmp/a

echo a 1>&2 2>/dev/null
echo a 2>/dev/null 1>&2

read -r name version _ < <(uname -sv)

tot() { IFS=$'\n' read -d "" -ra pkgs < <("$@");((packages+="${#pkgs[@]}"));pac "${#pkgs[@]}"; }

IFS=$'\n' read -d "" -ra gpus <<< "$gpu_cmd"

IFS=$'\n'"| " read -d "" -ra mem_stat <<< "$(svmon -G -O unit=MB)"

read -r w h \
    < <(xwininfo -root | awk -F':' '/Width|Height/ {printf $2}')

term_font="$(grep -i "${term/d}"'\**\.*font' <<< "$xrdb")"

has() { type -p "$1" >/dev/null && manager="$_"; }
        has "snap" && ps -e | grep -qFm 1 "snapd" >/dev/null && tot snap list && ((packages-=1))

mpc &>/dev/null && song="$(mpc -f '%artist% \n %album% \n %title%' current)"
    type -p df &>/dev/null ||\
        { err "Disk requires 'df' to function. Install 'df' to get disk info."; return; }

[[ "$image_backend" != "off" ]] && ! type -p convert &>/dev/null && \
    { image_backend="ascii"; err "Image: Imagemagick not found, falling back to ascii mode."; }

case "$os" in
    "Linux" | "BSD" | "iPhone OS" | "Solaris")
        # Package Manager Programs.
        has "pacman-key" && tot pacman -Qq --color never
        has "tazpkg"     && tot tazpkg list && ((packages-=6))

        # Other (Needs complex command)
        has "kpm-pkg" && ((packages+="$(kpm  --get-selections | grep -cv deinstall$)"))

        case "$kernel_name" in
            "FreeBSD") has "pkg"     && tot pkg info ;;
            "SunOS")   has "pkginfo" && tot pkginfo -i ;;
            *)
                has "pkg" && dir /var/db/pkg/*

                ((packages == 0)) && \
                    has "pkg" && tot pkg list
            ;;
        esac

        # Snap hangs if the command is run without the daemon running.
        # Only run snap if the daemon is also running.
        has "snap" && ps -e | grep -qFm 1 "snapd" >/dev/null && tot snap list && ((packages-=1))
    ;;

    "Windows")
        case "$kernel_name" in
            "CYGWIN"*) has "cygcheck" && tot cygcheck -cd ;;
            "MSYS"*)   has "pacman"   && tot pacman -Qq --color never ;;
        esac

        # Count chocolatey packages.
        [[ -d "/cygdrive/c/ProgramData/chocolatey/lib" ]] && \
            dir /cygdrive/c/ProgramData/chocolatey/lib/*
    ;;
esac
```

# job control

-   A job is a pipeline and any processes descended from it, that are all in
    the same process group.


# command line editing

# command history

# aliases <a id="aliases"></a>

# compatibility

-   basically compatible with Bourne shell `sh`.
-   POSIX compliant.

--------------------------------

# Design pattern
*   将要实现的功能分类, 提炼出功能模块.
*   从各种要实现的功能中抽象出一般化的辅助组件.
*   将各个功能模块分别在独立的脚本中实现.
    -   实现的方法是: 在脚本中构建需要的变量; 将所需功能构建为函数, 而不要在脚本中直接进行操作.
*   在主控脚本中 source 各个功能脚本, 并执行各个功能函数.
*   函数的返回值用于判断函数 (即命令) 的运行状态, 不能返回函数的计算结果.
*   函数与环境交互的几种方式:
    -   函数内直接使用或修改 outer scope's variables (including global variables), 不显性传入或传出.
        常用于在程序中具有特定含义的一些量的使用和操纵. 缺点是难以维护.
    -   为了体现变量在函数中被修改, 可以使用 nameref 或 `{!var}` indirection 语法, 明显地将
        变量传入函数, 再进行赋值等操作.
    -   将输入以 positional params 传入函数, 结果输出至 stdout, 然后用 `$()` 之类的结构捕获
        函数的输出.
    -   函数执行的状态通过 return 来返回, 成功则返回 0, 其他则返回非 0, 适当时可定义返回值
        的意义.
*   传入函数的变量若不是为了改变自身的值, 应尽快赋值给名字 make sense 的局域变量, 而不要一直使用 `$1, $2` 这种东西.
*   可以用 `readonly`, `declare -r` 实现变量值、数组值和函数定义不能被更改, 类似 `const`.
*   Use XXXHandler function and `trap` to catch signal and take actions before exiting. Also, echo a message signifying that the signal is caught.
*   如果一个功能适合看作是函数, 各个参数适合看作是变量, 就应使用函数的形式 `func(x,y,z)`;
    若适合看作是命令, 各个参数适合看作是设置项, 就应使用命令的形式 `foo -p1 bla -p2 bla ...`.
*   For both consistency and functionality, always use `declare` to declare a variable. 注意一点, declare 是一个(built-in) 命令, 它有自己的返回值, 因此获取不到 $() 的返回值.
*   属于统一类型的多个变量可以用 `associative array` 来统一表示. 这么做的好处一个是变量统一分类, 有实际意义的是便于循环时统一代码. 若达不到这第二个好处, 就不一定要倾向于 associative array.
*   deal carefully with rm, mv, cp. 不是因为它们危险, 而是因为如果处于 interactive mode, 那么如果不添加 `-f`, 它们会 fail fucking silently.
*   如果需要给多个独立的变量同时赋值, 可以用 `read` 给多个变量, 结合 while 后:
    ```
    while read a b c d; then
        ...
    done < some-input
    ```
    类似于 python 中 `for a, b, c, d in some-input`
*   By convention, environment variables (PAGER, EDITOR, ..) and internal shell variables (SHELL, BASH_VERSION, ..) are capitalized. All other variable names should be lower case. Keeping to this convention, you can rest assured that you don't need to know every environment variable used by UNIX tools or shells in order to avoid overwriting them. If it's your variable, lowercase it. If you export it, uppercase it.
*   当一个命令/函数的 stdout 被捕获时, 为了提示可以向 stderr 输出错误信息. 通过 `1>&2`
*   为了对脚本尽量安全地 debug 或安全地运行, 可以 `set -e`
*   函数最好有明确的返回值
*   构造 associative array 是从 sed/awk 等工具中一次性返回多个值的清晰方法; 此外也可以将输出构造成 key=value 形式并结合 eval 来赋值
*   you can never be too careful dealling with `>` and `>>`, 看清楚自己用的他妈是哪个
*   never use `\`\`` for command substitution, it's not properly nested. Use `$()`
*   方便地输出多行信息可以使用 `cat` + here document 的方式.
*   `hash` builtin 的用处: 提高 shell 找命令的速度. 若将一个命令在 PATH 的不同路径之间移动,
    可能需要更新 hash. `hash` 还可以用来临时地让某个程序可以被 shell 找到, 而无需修改 PATH.
*   一些有助于发现变成错误、规范化流程的脚本初始设定:
    ```
    set -o pipefail
    shopt -s globasciiranges
    export LC_COLLATE=C
    unalias rm cp mv &>/dev/null || true
    ```
*   其他常用的初始设定:
    ```
    shopt -s extglob
    shopt -s globstar
    ```
*   debug shell script:
    -   执行脚本之前用 `bash -n` (或 `set -n`) 来检验有无基本 shell 语法错误
    -   使用 `set -x` 来检验每个命令的执行情况
    -   使用 `set -e` 和 `shopt -s inherit_errexit` 来避免出错后未即使终止, 使威胁扩大.
    -   使用 `shopt -s extdebug` 来增加 debug 强度 (相当于, `set -ET`), 并配合 trap on DEBUG,
        RETURN, ERR 检测每层命令的执行情况
    -   使用 `set -u` 来检查变量拼写错误等情况
    -   使用 `caller` builtin 实现类似 python traceback 的 stack trace 效果.
        See [](bash-utils/raise.sh)
    -   `PS4='${BASH_SOURCE[0]}@${LINENO}(${FUNCNAME[0]}): '`
*   profile shell script:
      - `PS4='+ $(date "+%s.%N") ${BASH_SOURCE}@${LINENO}: '`
    
*   About collating sequence and pattern matching:
    -   设置 `export LC_COLLATE=C` 保证 collating sequence 为正常的 numeric value order.
    -   为避免 range expression ([m-n]) 中由于 locale 导致包含非预期字符, 合适时尽量使用
        posix character class ([:alpha:], [:lower:], etc), 而不是显性的 [a-z] 之类的 range.
*   对于局部的或临时的或内部使用的量, 可以像 python 那样以 `_` 起始, 例如 `_cdpath`.
*   构造 true/false 的方式以及条件分支处理方式:
    -   对于简单的 if 条件处理, 例如只是执行一个 pipeline 或一个 compound command,
        可以使用 && 或 || 这种 operator 构成 command list.
        如 `true && do_something`, `false || do_something`,
        `[[ ... ]] && something` 这比 if 条件语句高效.
        对于简单的 if else 逻辑, 也可以使用 `condition && ... || ...`.
    -   对于复杂的条件分支处理, 考虑到可读性最好使用 if/else 的方式.
    -   对于简单的 true/false flag, 可以直接将 true/false 命令赋值之. 再所需的地方执行命令.
        也可以通过赋任意字符串表示 true, 不赋值或不定义表示 false. 通过 [[ $var ]] 来检查.
    -   对于函数, 通过返回 0/非0 来表示返回成功/失败.
*   shell 中在可能的情况下, 和保证可读性的情况下避免使用 `for`, `while` 等循环, 因为太慢,
    可以使用 `find`, `xargs` 之类的来代替. 意思是, 尽量将循环的流程在工具中执行, 即用 C 来
    完成.
*   对纯数值的比较应尽量使用 `(( ... ))` 结构.
*   类似传递指针进函数的方式:
    -   `declare -n nameref`, 然后传递 `nameref` 进函数. 这可以完全指针化.
    -   在函数里执行 `read "$1" <<< "$2"`, 其中 `$1` 是参数名, `$2` 是参数值.
*   dracut source is a great place to learn bash (and many more).
*   declare 中不该包含可能出错的赋值操作. 若赋值部分执行了可能出错的命令, declare 的返回值
    会掩盖这些错误. 这种情况下, 将 declare 声明与赋值操作分开写.
    
*   在任意命令中使用 bash 的 background jobspec: `jobs -x COMMAND [args]`
    
*   fork 执行一个子进程, 并希望它能 detach from current session: `(cmd &)`
    
*   在一组 pipeline 的构建过程中, 如果只是想要快速地将左边命令的 stdout 和 stderr
    一起传入 pipe, 可以使用 `|&`. 但要记住本质上 `command |&` 是 `command 2>&1 |` 的简写.
    正因为它是 `command 2>&1 |` 的 shortcut, 而且 redirection operator 的执行顺序是从左至右,
    因此隐含的 `2>&1` 操作会 override 一切 command 中对 fd 2 的 redirection.
    
*   directory 和 file 的本质是相同的, 在 shell 中的表达方式也是相同的, 都是通过
    相同规则的文件命名规则来指定. 而恰恰因为这样, 在命令行上指定一个目录, 而不是
    指定一个同名的 regular file 时, 应该在目录名后面加一个 `/` 符号. 这样不仅仅
    对于脚本读者更清晰, 而且有助于及时发现程序逻辑错误, 增强鲁棒性. 例如
    `mv a b` vs `mv a b/`.

# Notes

-   PS0: Expanded and displayed by interactive shells after
         reading a complete command but before executing it.
    PS1: normal prompt.
    PS2: line continuation prompt.
    PS3: prompt for `select`.
    PS4: prompt for debug output.
    
-   在 double quote 内部以及在赋值右端, 不会进行 word splitting. 因此字符串会 verbatim
    保存下来. 没有任何 $IFS 相关的转换等. 例如多行 (包含 newline) 仍是多行.
    
-   必须要明确, 在 shell 中, 所有内容本身就是字符串, 不同的 quoting 本质上都是为了附加
    别的作用的 (而不是表示 XXX 是字符串).
    
-   在 double quoting 中, 只有 $, \`, \\, !, 字符有特殊含义. 注意没有 ', 所以 $'\n' 形式的
    ANSI-C quoting 不能在 double quoting 中使用.

-   command grouping: `()` vs `{}`, 各自在什么时候使用?

    *   `()` 和 `{}` 都是 command grouping. 即将多个 command list 组成一个整体去执行.
        这个整体相当于一个 simple command.

    *   `(cmdlist)` 中的命令在 subshell environment 中执行. 即 bash 会 fork 一个 subshell 去执行
        里面的命令. 因此 subshell 中的 side effects 不会影响当前 shell 环境. 因此这适用于
        需要执行一些操作, 但不想影响、不想手动恢复当前 shell 环境的时候. 比如, cd dir 执行
        一个命令然后再回来.

    *   `{ cmdlist; }` 中的命令在当前 shell environment 中执行. 因此 side effects 影响当前
        shell 环境. 注意两侧的空格和 `;` 或者 newline 是必须的. This is historical.

    *   两者都可以在定义函数时使用. (函数不过是给一个 command group 加了一个名字) 相应函数
        在执行时具有上述各自的特点.

-   在 bash 中, `$0` 始终是 name of shell or shell script. 对于 interactive
    login shell, `$0` 会以 `-` prefix. 

    注意即使在函数中, `$0` 也不会重命名为函数名, 仍然是初始值.

-   process substitution 中, `>()` stdin connection 的一个用处. sudo 时将 stdout/stderr
    分别写到两个当前用户不可写的路径.

    ```sh
    sudo command > >(sudo tee /log.out >/dev/null) 2> >(sudo tee/log.err >/dev/null)
    ```

-   setuid bit on bash does not have any effect. Bash detects that it has been
    started SUID root (UID!=EUID) and uses its root power to throw this power
    away, resetting EUID to UID.[[SEBashSuid]](#SEBashSuid)

-   若需要加载一个 shell variables 配置文件, 并且希望所有加载的量 export 成环境变量,
    可以使用 `set -a` 方便地进行, 例如:

    ```sh
    set -a
    . some_config_file
    set +a
    ```

# initialization files

## shell modes
initialization files 的加载取决于 shell 的执行模式. 有以下两种 shell modes,
它们的组合成为 4 种可能的执行模式:

*   login. user logs in to the system, e.g., via terminal, via ssh. 或者
    ``-l``, ``--login`` options are specified.
*   interactive. shell has a prompt and its stdout and stderr are connected
    to a terminal. 或者 ``-i`` option are specified.

Common scenarios:

-   login via ssh: login, interactive
-   execute a shell script, without special options: non-login,
    non-interactive.
-   start a new shell process without special options: non-login,
    interactive.
-   open a graphical terminal: login/non-login based on terminal app's
    settings, interactive.

See also [Unix shell initialization](#unix-shell-init).

## For bash

*   interactive shell (无论 login 或 nonlogin) 的初始化结果是基本相同的, 他
    们都执行了 /etc/profile.d/*.sh, ~/.bashrc, /etc/bashrc 或
    /etc/bash.bashrc.
*   non-interactive shell 对于 login 和 nonlogin 初始化结果不同. 前者与
    interactive shell 相同, 后者基本不执行初始化.

### login shell

#### interactive

-   /etc/profile
    *   /etc/profile.d/*.sh
    *   /etc/bash.bashrc
        -   /usr/share/bash-completion/bash_completion

-   ~/.bash_profile | ~/.bash_login | ~/.profile
    *   ~/.bashrc
        -   /etc/bashrc (RHEL)

logout 时, 执行 ~/.bash_logout

#### non-interactive

-   /etc/profile
-   ~/.bash_profile | ~/.bash_login | ~/.profile
-   BASH_ENV

logout 时, 执行 ~/.bash_logout

### nonlogin shell

#### interactive

-   /etc/bash.bashrc (一些版本的 bash 首先要读, 一般注意系统中是否有该文件即可
    判断.) [See this](#bash.bashrc)
-   ~/.bashrc

#### non-interactive

- BASH_ENV

## sh emulation mode

*   login shell 会执行 /etc/profile 全局初始化.
*   对于 nonlogin shell 基本不会执行初始化.

### login shell

#### interactive

-   /etc/profile
-   ~/.profile
-   ENV

#### non-interactive

-   /etc/profile
-   ~/.profile

### nonlogin shell

#### interactive

-   ENV

#### non-interactive
nothing

# mock shell script
- 我见过的 shell script 大部分都很 messy.
- 函数返回值问题.
- 只有整数运算.
- true/false, success/failure 0,1
- 空格不能随便加. sef=, { sef; }
- 分号不能忘
- until loop? Are you kidding me?
- # comment 不能随便放置在行末
- no (decent) debugger (bash -x)
- awkward arithmetic comparison in `[ ]`.
- how many ways to declare a variable, or even not to do that?
	- `declare`
	- `local`
	- `readonly`
	- not at all

# references
<span id="interpreted">[interpreted]</span> [Is bash an interpreted language?](https://stackoverflow.com/a/30156987/1602266)

<span id="SEBashSuid">[SEBashSuid]</span> [Setuid bit seems to have no effect on bash](https://unix.stackexchange.com/questions/74527/setuid-bit-seems-to-have-no-effect-on-bash)

<span id="prompt-command">bash prompt command</span> [What is the difference between PS1 and PROMPT_COMMAND](https://stackoverflow.com/questions/3058325/what-is-the-difference-between-ps1-and-prompt-command)

<span id="bash.bashrc">bash.bashrc</span> [When is /etc/bash.bashrc invoked?](https://unix.stackexchange.com/questions/187369/when-is-etc-bash-bashrc-invoked)

<span id="unix-shell-init">[shell-init]</span> [Unix shell initialization](https://github.com/pyenv/pyenv/wiki/Unix-shell-initialization)
