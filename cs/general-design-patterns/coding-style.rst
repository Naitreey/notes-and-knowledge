Comment
=======
- 珍惜你的注释. 只有在代码本身不能充分解释逻辑的地方才加注释.

  注释不能代替清晰可读的代码. 不能因为写了注释, 就允许它相应的代码写得混乱.
  
  You should always write your code as if comments didn't exist. This forces you to
  write your code in the simplest, plainest, most self-documenting way you can humanly
  come up with.

  when you can't possibly imagine any conceivable way your code could be changed to
  become more straightforward and obvious -- then, and only then, should you feel
  compelled to add a comment explaining what your code does.

- Comment isn't there to explain *what*, it's there to explain *why*.
  注释解释的是为什么要这样做, 以及它是怎么做的 (如果说确实逻辑很复杂的话).
  注释不解释 代码做的是什么, 那是代码本身的功能.

- Too many comments (one per line, for example) is probably a sign of poorly written code.

Naming
======
- application/package naming.

  * 给应用或 package 一个比较容易区分的名字.
  
  * 避免使用比较通用的名字.

  * 如果一个应用本身的功能就是偏向于某种通用的内容, 则需要创新性地
    从另一个角度对应用命名. 例如如果一个 app 是处理配置文件的, 那
    如果也叫 ``config...``, 很可能就会跟真正的配置文件目录名字相近,
    就要换个更有识别性的名字.
