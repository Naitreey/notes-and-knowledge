# language
## overview

-   bash/shell script is an interpreted language.
    并且不包含预编译阶段. 不仅如此, bash 是依次对每个 logical line 进行 read, parse, execute
    操作的. 而不是对整个脚本进行这三个步骤. 所以只有执行到特定一行时才知道该行有没有语法错误.
    (这也给调试带来了很多麻烦.) 这是与 Python, JavaScript 等 interpreted language 的一个区别.
    [[interpreted]](#interpreted).

## scope

bash script 使用的是 dynamic scope, 而不是 lexical scope. 因而在 name resolution 方面与常见
现代语言不同.

name resolution 时, 依据 call stack, 从顶层 (即当前函数) 开始, 向下搜索 (caller 方向), 直至
global scope. 若最终没找到该变量, 对于 rvalue resolution, expands to empty string; 对于 lvalue
resolution, 在 global scope 创建该变量 (这一点类似 js 中 lvalue 的处理).

在 nested scope 中, inner scope 声明的变量在相应 scope 中覆盖 outer scope 的同名变量. 但只要
出了 scope (即 return to caller stack 后), outer scope 中的变量赋值就继续有效.

以 dynamic scope 思想为基础, 我们可以理解以下几个 statement 的清晰含义

```sh
x=1
declare x=1
declare x; x=1
```

-   第一个 statement 经常用于声明全局变量 `x` 并赋值, 但实际上它不是变量声明而是一种偷懒的赋值.
    实际上, 这是对 lvalue 的赋值. 根据 lvalue resolution 机制, `x` 变量可能是在 caller function
    中声明的, 或者在全局中声明的, 或者是没有声明的. 却不一定是全局的. 总之, 这个 statement
    只应该用于变量赋值而不该是代替变量声明.
-   第二个 statement 是标准的变量声明. 并且具有清晰的 scope -- 出现在 global scope, 就是声明
    global variable; 出现在 function scope, 就是声明 function-scope variable.
-   第三个 statement 是标准的先声明再赋值.

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
*   never use "``" for command substitution, it's not properly nested. Use `$()`
*   方便地输出多行信息可以使用 `cat` + here document 的方式.
*   `hash` builtin 的用处: 提高 shell 找命令的速度. 若将一个命令在 PATH 的不同路径之间移动,
    可能需要更新 hash.
`h  ash` 还可以用来临时地让某个程序可以被 shell 找到, 而无需修改 PATH.
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
    
-   在 double quoting 中, 只有 $, `, \, !, 字符有特殊含义. 注意没有 ', 所以 $'\n' 形式的
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

# shell 初始化文件的执行流程

* bash 初始化文件的执行.

  - login shell:

    * interactive:

      - /etc/profile
      - ~/.bash_profile | ~/.bash_login | ~/.profile

      logout 时, 执行 ~/.bash_logout

    * non-interactive:

      - /etc/profile
      - ~/.bash_profile | ~/.bash_login | ~/.profile
      - BASH_ENV

      logout 时, 执行 ~/.bash_logout

  - nonlogin shell:

    * interactive:

      - ~/.bashrc

    * non-interactive:

      - BASH_ENV

* sh 初始化文件的执行.

  - login shell:

    * interactive:

      - /etc/profile
      - ~/.profile
      - ENV

    * non-interactive:

      - /etc/profile
      - ~/.profile

  - nonlogin shell:

    * interactive:

      - ENV

    * non-interactive: nothing.

* 各初始化文件的执行流程:

  - /etc/profile -> /etc/profile.d/*.sh

  - ~/.bash_profile -> ~/.bashrc

  - ~/.bashrc -> -> /etc/bashrc -> /etc/profile.d/*.sh (nonlogin shell)

  以下文件不存在: ~/.bash_login, ~/.bash_logout, ~/.profile

* 总结:

  - 对于 bash

    * interactive shell (无论 login 或 nonlogin) 的初始化结果是基本相同的,
      他们都执行了 /etc/profile.d/*.sh, ~/.bashrc, /etc/bashrc .

    * non-interactive shell 对于 login 和 nonlogin 初始化结果不同. 前者与
      interactive shell 相同, 后者基本不执行初始化.

  - 对于 sh

    * login shell 会执行 /etc/profile 全局初始化.

    * 对于 nonlogin shell 基本不会执行初始化.

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
<a id="interpreted">[interpreted]</a> [Is bash an interpreted language?](https://stackoverflow.com/a/30156987/1602266)
<a id="SEBashSuid">[SEBashSuid]</a> [Setuid bit seems to have no effect on bash](https://unix.stackexchange.com/questions/74527/setuid-bit-seems-to-have-no-effect-on-bash)
